# `!token`{.interpreted-text role="mod"} \-\-- Constants used with Python parse trees

::: {.module synopsis="Constants representing terminal nodes of the parse tree."}
token
:::

**Source code:** `Lib/token.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides constants which represent the numeric values of leaf nodes of the parse tree (terminal tokens). Refer to the file `Grammar/Tokens`{.interpreted-text role="file"} in the Python distribution for the definitions of the names in the context of the language grammar. The specific numeric values which the names map to may change between Python versions.

The module also provides a mapping from numeric codes to names and some functions. The functions mirror definitions in the Python C header files.

Note that a token\'s value may depend on tokenizer options. For example, a `"+"` token may be reported as either `PLUS`{.interpreted-text role="data"} or `OP`{.interpreted-text role="data"}, or a `"match"` token may be either `NAME`{.interpreted-text role="data"} or `SOFT_KEYWORD`{.interpreted-text role="data"}.

::: data
tok_name

Dictionary mapping the numeric values of the constants defined in this module back to name strings, allowing more human-readable representation of parse trees to be generated.
:::

::: function
ISTERMINAL(x)

Return `True` for terminal token values.
:::

::: function
ISNONTERMINAL(x)

Return `True` for non-terminal token values.
:::

::: function
ISEOF(x)

Return `True` if *x* is the marker indicating the end of input.
:::

The token constants are:

::: data
NAME

Token value that indicates an `identifier or keyword <identifiers>`{.interpreted-text role="ref"}.
:::

::: data
NUMBER

Token value that indicates a `numeric literal <numbers>`{.interpreted-text role="ref"}
:::

::: data
STRING

Token value that indicates a `string or byte literal <strings>`{.interpreted-text role="ref"}, excluding `formatted string literals <f-strings>`{.interpreted-text role="ref"}. The token string is not interpreted: it includes the surrounding quotation marks and the prefix (if given); backslashes are included literally, without processing escape sequences.
:::

:::: data
OP

A generic token value that indicates an `operator <operators>`{.interpreted-text role="ref"} or `delimiter <delimiters>`{.interpreted-text role="ref"}.

::: impl-detail
This value is only reported by the `tokenize`{.interpreted-text role="mod"} module. Internally, the tokenizer uses `exact token types <token_operators_delimiters>`{.interpreted-text role="ref"} instead.
:::
::::

::: data
COMMENT

Token value used to indicate a comment. The parser ignores `!COMMENT`{.interpreted-text role="data"} tokens.
:::

::: data
NEWLINE

Token value that indicates the end of a `logical line <logical-lines>`{.interpreted-text role="ref"}.
:::

::: data
NL

Token value used to indicate a non-terminating newline. `!NL`{.interpreted-text role="data"} tokens are generated when a logical line of code is continued over multiple physical lines. The parser ignores `!NL`{.interpreted-text role="data"} tokens.
:::

::: data
INDENT

Token value used at the beginning of a `logical line <logical-lines>`{.interpreted-text role="ref"} to indicate the start of an `indented block <indentation>`{.interpreted-text role="ref"}.
:::

::: data
DEDENT

Token value used at the beginning of a `logical line <logical-lines>`{.interpreted-text role="ref"} to indicate the end of an `indented block <indentation>`{.interpreted-text role="ref"}.
:::

:::: data
FSTRING_START

Token value used to indicate the beginning of an `f-string literal <f-strings>`{.interpreted-text role="ref"}.

::: impl-detail
The token string includes the prefix and the opening quote(s), but none of the contents of the literal.
:::
::::

:::: data
FSTRING_MIDDLE

Token value used for literal text inside an `f-string literal <f-strings>`{.interpreted-text role="ref"}, including format specifications.

::: impl-detail
Replacement fields (that is, the non-literal parts of f-strings) use the same tokens as other expressions, and are delimited by `LBRACE`{.interpreted-text role="data"}, `RBRACE`{.interpreted-text role="data"}, `EXCLAMATION`{.interpreted-text role="data"} and `COLON`{.interpreted-text role="data"} tokens.
:::
::::

:::: data
FSTRING_END

Token value used to indicate the end of a `f-string <f-strings>`{.interpreted-text role="ref"}.

::: impl-detail
The token string contains the closing quote(s).
:::
::::

::::: data
TSTRING_START

Token value used to indicate the beginning of a template string literal.

::: impl-detail
The token string includes the prefix and the opening quote(s), but none of the contents of the literal.
:::

::: versionadded
3.14
:::
:::::

::::: data
TSTRING_MIDDLE

Token value used for literal text inside a template string literal including format specifications.

::: impl-detail
Replacement fields (that is, the non-literal parts of t-strings) use the same tokens as other expressions, and are delimited by `LBRACE`{.interpreted-text role="data"}, `RBRACE`{.interpreted-text role="data"}, `EXCLAMATION`{.interpreted-text role="data"} and `COLON`{.interpreted-text role="data"} tokens.
:::

::: versionadded
3.14
:::
:::::

::::: data
TSTRING_END

Token value used to indicate the end of a template string literal.

::: impl-detail
The token string contains the closing quote(s).
:::

::: versionadded
3.14
:::
:::::

::: data
ENDMARKER

Token value that indicates the end of input. Used in `top-level grammar rules <top-level>`{.interpreted-text role="ref"}.
:::

:::: data
ENCODING

Token value that indicates the encoding used to decode the source bytes into text. The first token returned by `tokenize.tokenize`{.interpreted-text role="func"} will always be an `ENCODING` token.

::: impl-detail
This token type isn\'t used by the C tokenizer but is needed for the `tokenize`{.interpreted-text role="mod"} module.
:::
::::

The following token types are not produced by the `tokenize`{.interpreted-text role="mod"} module, and are defined for special uses in the tokenizer or parser:

::: data
TYPE_IGNORE

Token value indicating that a `type: ignore` comment was recognized. Such tokens are produced instead of regular `COMMENT`{.interpreted-text role="data"} tokens only with the `~ast.PyCF_TYPE_COMMENTS`{.interpreted-text role="data"} flag.
:::

::: data
TYPE_COMMENT

Token value indicating that a type comment was recognized. Such tokens are produced instead of regular `COMMENT`{.interpreted-text role="data"} tokens only with the `~ast.PyCF_TYPE_COMMENTS`{.interpreted-text role="data"} flag.
:::

::: data
SOFT_KEYWORD

Token value indicating a `soft keyword <soft-keywords>`{.interpreted-text role="ref"}.

The tokenizer never produces this value. To check for a soft keyword, pass a `NAME`{.interpreted-text role="data"} token\'s string to `keyword.issoftkeyword`{.interpreted-text role="func"}.
:::

::: data
ERRORTOKEN

Token value used to indicate wrong input.

The `tokenize`{.interpreted-text role="mod"} module generally indicates errors by raising exceptions instead of emitting this token. It can also emit tokens such as `OP`{.interpreted-text role="data"} or `NAME`{.interpreted-text role="data"} with strings that are later rejected by the parser.
:::

::: {#token_operators_delimiters}
The remaining tokens represent specific `operators <operators>`{.interpreted-text role="ref"} and `delimiters <delimiters>`{.interpreted-text role="ref"}. (The `tokenize`{.interpreted-text role="mod"} module reports these as `OP`{.interpreted-text role="data"}; see `exact_type` in the `tokenize`{.interpreted-text role="mod"} documentation for details.)
:::

+------------------+---------+
| Token            | Value   |
+==================+=========+
| ::: data         | `"("`   |
| LPAR             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `")"`   |
| RPAR             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"["`   |
| LSQB             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"]"`   |
| RSQB             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `":"`   |
| COLON            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `","`   |
| COMMA            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `";"`   |
| SEMI             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"+"`   |
| PLUS             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"-"`   |
| MINUS            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"*"`   |
| STAR             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"/"`   |
| SLASH            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"|"`   |
| VBAR             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"&"`   |
| AMPER            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"<"`   |
| LESS             |         |
| :::              |         |
+------------------+---------+
| ::: data         | `">"`   |
| GREATER          |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"="`   |
| EQUAL            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"."`   |
| DOT              |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"%"`   |
| PERCENT          |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"{"`   |
| LBRACE           |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"}"`   |
| RBRACE           |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"=="`  |
| EQEQUAL          |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"!="`  |
| NOTEQUAL         |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"<="`  |
| LESSEQUAL        |         |
| :::              |         |
+------------------+---------+
| ::: data         | `">="`  |
| GREATEREQUAL     |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"~"`   |
| TILDE            |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"^"`   |
| CIRCUMFLEX       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"<<"`  |
| LEFTSHIFT        |         |
| :::              |         |
+------------------+---------+
| ::: data         | `">>"`  |
| RIGHTSHIFT       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"**"`  |
| DOUBLESTAR       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"+="`  |
| PLUSEQUAL        |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"-="`  |
| MINEQUAL         |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"*="`  |
| STAREQUAL        |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"/="`  |
| SLASHEQUAL       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"%="`  |
| PERCENTEQUAL     |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"&="`  |
| AMPEREQUAL       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"|="`  |
| VBAREQUAL        |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"^="`  |
| CIRCUMFLEXEQUAL  |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"<<="` |
| LEFTSHIFTEQUAL   |         |
| :::              |         |
+------------------+---------+
| ::: data         | `">>="` |
| RIGHTSHIFTEQUAL  |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"**="` |
| DOUBLESTAREQUAL  |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"//"`  |
| DOUBLESLASH      |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"//="` |
| DOUBLESLASHEQUAL |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"@"`   |
| AT               |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"@="`  |
| ATEQUAL          |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"->"`  |
| RARROW           |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"..."` |
| ELLIPSIS         |         |
| :::              |         |
+------------------+---------+
| ::: data         | `":="`  |
| COLONEQUAL       |         |
| :::              |         |
+------------------+---------+
| ::: data         | `"!"`   |
| EXCLAMATION      |         |
| :::              |         |
+------------------+---------+

The following non-token constants are provided:

::: data
N_TOKENS

The number of token types defined in this module.
:::

:::: data
EXACT_TOKEN_TYPES

A dictionary mapping the string representation of a token to its numeric code.

::: versionadded
3.8
:::
::::

::: versionchanged
3.5 Added `!AWAIT`{.interpreted-text role="data"} and `!ASYNC`{.interpreted-text role="data"} tokens.
:::

::: versionchanged
3.7 Added `COMMENT`{.interpreted-text role="data"}, `NL`{.interpreted-text role="data"} and `ENCODING`{.interpreted-text role="data"} tokens.
:::

::: versionchanged
3.7 Removed `!AWAIT`{.interpreted-text role="data"} and `!ASYNC`{.interpreted-text role="data"} tokens. \"async\" and \"await\" are now tokenized as `NAME`{.interpreted-text role="data"} tokens.
:::

::: versionchanged
3.8 Added `TYPE_COMMENT`{.interpreted-text role="data"}, `TYPE_IGNORE`{.interpreted-text role="data"}, `COLONEQUAL`{.interpreted-text role="data"}. Added `!AWAIT`{.interpreted-text role="data"} and `!ASYNC`{.interpreted-text role="data"} tokens back (they\'re needed to support parsing older Python versions for `ast.parse`{.interpreted-text role="func"} with `feature_version` set to 6 or lower).
:::

::: versionchanged
3.12 Added `EXCLAMATION`{.interpreted-text role="data"}.
:::

::: versionchanged
3.13 Removed `!AWAIT`{.interpreted-text role="data"} and `!ASYNC`{.interpreted-text role="data"} tokens again.
:::
