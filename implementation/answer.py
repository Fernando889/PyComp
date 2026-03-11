# ================================
# Import Libraries
# ================================
import os
import torch
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import login
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace, HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    BitsAndBytesConfig,
    GenerationConfig,
)
from sentence_transformers import CrossEncoder

# ================================
# Environment Setup
# ================================
load_dotenv(override=True)
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("QWEN_MODELS")
login(token=HF_TOKEN, add_to_git_credential=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device Using: {device}")


# ================================
# Embedding Model
# ================================
EMBEDDING_MODELS = HuggingFaceEmbeddings(
    model_name=os.getenv("EMBEDDING_MODELS")
)

# ================================
# Vector Database
# ================================
DB_NAME = str(Path(__file__).parent.parent/"vector_db")

RETRIEVAL_K = 200
RERANK_K = 30

vectorstore = Chroma(
    persist_directory=DB_NAME,
    embedding_function=EMBEDDING_MODELS
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": RETRIEVAL_K
    }
)

# ================================
# Cross Encoder Reranker
# ================================
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-12-v2",
    device=device,
    max_length=512
)

# ================================
# LLM Setup (Qwen)
# ================================
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL,
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    quantization_config=bnb_config,
)

generation_config = GenerationConfig(
    max_new_tokens=512,
    temperature=0.0,
    top_p=0.9,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id
)

model.generation_config = generation_config


text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False
)

hf_llm = HuggingFacePipeline(pipeline=text_pipeline)
llm = ChatHuggingFace(llm=hf_llm)


# ================================
# System Prompt
# ================================
SYSTEM_PROMPT = """
You are a Python documentation assistant.

Answer the question using ONLY the provided context from the official Python documentation.

Rules:
- Use exact Python terms from the context (modules, functions, classes, exceptions).
- Do not add information not present in the context.
- If the answer is not in the context, respond exactly: I do not know.

Context:
{context}
"""


# ================================
# Query Rewrite Prompt
# ================================
QUERY_REWRITE_PROMPT = PromptTemplate.from_template(
    """
Rewrite the query for Python documentation retrieval.
Put the core concept first, then add related Python identifiers and keywords.
For comparisons, include both terms.
Keep output under 15 words, no punctuation.

Examples:
input: What is a lambda function?
output: lambda anonymous function expression syntax callable

input: What is the difference between a list and a tuple?
output: list tuple mutable immutable sequence difference

input: What is the purpose of __init__?
output: __init__ constructor initialization instance object class

Return only the rewritten query.

Query:
{question}
"""
)

# ================================
# Query Rewrite Chain
# ================================
query_rewrite_chain = QUERY_REWRITE_PROMPT | llm | StrOutputParser()


# ================================
# Cross Encoder Reranking
# ================================
def rerank_documents(query: str, docs: list[Document], top_k: int = RERANK_K):

    if not docs:
        return []

    pairs = [
        (query, doc.page_content)
        for doc in docs
    ]

    scores = reranker.predict(
        pairs,
        batch_size=4
    )

    ranked_docs = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked_docs[:top_k]]


def rewrite_query(question: str) -> str:

    # Step 1 — Rewrite Query
    rewritten_query = query_rewrite_chain.invoke({
        "question": question
    })

    return rewritten_query


# ================================
# Retrieval Pipeline
# ================================
def fetch_context(question: str) -> list[Document]:

    # Step 1 — Vector Retrieval
    docs = retriever.invoke(question)

    # Step 2 — CrossEncoder Rerank
    docs = rerank_documents(question, docs)

    return docs


# ================================
# Answer Question
# ================================
def answer_question(
    question: str,
    history: list[dict] = [],
    use_rewrite: bool = False,
    eval_mode: bool = False
) -> tuple[str, list[Document]]:

    history = history or []

    query = rewrite_query(question=question) if use_rewrite else question

    docs = fetch_context(question=query)

    if eval_mode:
        docs = docs[:10]

    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = SYSTEM_PROMPT.format(
        context=context
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    answer = llm.invoke(messages).content

    return answer, docs
