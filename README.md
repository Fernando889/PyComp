# PyComp: Simple Python Companion

A local RAG-based Python documentation assistant. PyComp leverages semantic search, cross-encoder reranking, and a quantized LLM to deliver accurate answers from the Official Python Documentation — all running on consumer hardware with 4GB VRAM.

⚠️ Note: The live demo runs on HuggingFace Free Tier (CPU only). Response time may be significantly slower than local deployment due to the absence of GPU acceleration.

## 📌 Features

- **RAG Pipeline** — Retrieves relevant context from Official Python Documentation before generating answers
- **Cross-Encoder Reranking** — Reranks retrieved documents for higher precision using `ms-marco-MiniLM-L-12-v2`
- **Query Rewriting** — Expands user queries with Python-specific identifiers for better retrieval
- **4-bit Quantization** — Runs Qwen2.5-3B-Instruct on 4GB VRAM using BitsAndBytes NF4 quantization
- **Evaluation Dashboard** — Built-in retrieval and answer quality evaluation via Gradio UI
- **Chat Interface** — Clean Gradio-based chat UI with retrieved context display

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Query Rewriting (Qwen2.5-3B-Instruct)
    │
    ▼
Vector Retrieval (ChromaDB + BAAI/bge-base-en-v1.5)
    │   RETRIEVAL_K = 200
    ▼
Cross-Encoder Reranking (ms-marco-MiniLM-L-12-v2)
    │   RERANK_K = 30
    ▼
Answer Generation (Qwen2.5-3B-Instruct 4-bit)
    │
    ▼
Response
```

---

## 🛠️ Tech Stack

| Component       | Technology                            |
| --------------- | ------------------------------------- |
| LLM             | Qwen2.5-3B-Instruct (4-bit NF4)       |
| Embedding Model | BAAI/bge-base-en-v1.5                 |
| Reranker        | cross-encoder/ms-marco-MiniLM-L-12-v2 |
| Vector Database | ChromaDB                              |
| Framework       | LangChain                             |
| UI              | Gradio                                |
| Quantization    | BitsAndBytes (4-bit)                  |
| Knowledge Base  | Official Python Documentation         |

---

## 📊 Evaluation Results

### Retrieval Evaluation (100 questions)

| Metric                           | Score      |
| -------------------------------- | ---------- |
| Mean Reciprocal Rank (MRR)       | **0.8034** |
| Discounted Cumulative Gain (DCG) | **0.8185** |
| Keyword Coverage                 | **96.7%**  |

### Answer Evaluation (10 sample questions)

| Metric       | Score       |
| ------------ | ----------- |
| Accuracy     | **3.8 / 5** |
| Completeness | **4.4 / 5** |
| Relevance    | **4.1 / 5** |

> **Note:** Answer evaluation was conducted on a 10-question sample due to hardware constraints (4GB VRAM). Judge model: `qwen3:1.7b` via Ollama.

---

## ⚙️ RAG Configuration

| Parameter     | Value  |
| ------------- | ------ |
| Chunk Size    | 700    |
| Chunk Overlap | 100    |
| Total Vectors | 26,947 |
| RETRIEVAL_K   | 200    |
| RERANK_K      | 30     |

---

## 🚀 Installation

### Prerequisites

- Python 3.11
- CUDA-compatible GPU (minimum 4GB VRAM)
- [Ollama](https://ollama.com) (for answer evaluation only)

### 1. Clone the repository

```bash
git clone https://github.com/Fernando889/PyComp.git
cd PyComp
```

### 2. Install dependencies

```bash
pip install --extra-index-url https://download.pytorch.org/whl/cu121 torch==2.5.1+cu121
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
HF_TOKEN=your_huggingface_token
QWEN_MODELS=Qwen/Qwen2.5-3B-Instruct
EMBEDDING_MODELS=BAAI/bge-base-en-v1.5
```

### 4. Build the vector database

```bash
python implementation/ingest.py
```

### 5. Run the chat app

```bash
python app.py
```

### 6. Run the evaluation dashboard (optional)

```bash
python evaluator.py
```

---

## ⚠️ Limitations

- Response time is **30-120 seconds** per query due to local 4GB VRAM constraint
- Answer evaluation requires [Ollama](https://ollama.com) with `qwen3:1.7b` installed locally
- Vector database must be built locally by running `ingest.py`
- Answer evaluation sample size limited to 10 questions due to hardware constraints
