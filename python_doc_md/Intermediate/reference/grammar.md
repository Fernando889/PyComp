# Full Grammar specification

This is the full Python grammar, derived directly from the grammar used to generate the CPython parser (see `Grammar/python.gram`{.interpreted-text role="source"}). The version here omits details related to code generation and error recovery.

The notation used here is the same as in the preceding docs, and is described in the `notation <notation>`{.interpreted-text role="ref"} section, except for an extra complication:

- `~` (\"cut\"): commit to the current alternative; fail the rule if the alternative fails to parse

  Python mainly uses cuts for optimizations or improved error messages. They often appear to be useless in the listing below.

  Cuts currently don\'t appear inside parentheses, brackets, lookaheads and similar. Their behavior in these contexts is deliberately left unspecified.

::: {.literalinclude language="peg"}
../../Grammar/python.gram
:::
