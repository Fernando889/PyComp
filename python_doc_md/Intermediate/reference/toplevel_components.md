# Top-level components {#top-level}

::: index
single: interpreter
:::

The Python interpreter can get its input from a number of sources: from a script passed to it as standard input or as program argument, typed in interactively, from a module source file, etc. This chapter gives the syntax used in these cases.

## Complete Python programs {#programs}

::: index
single: program
:::

::: index
pair: module; sys pair: module; \_\_main\_\_ pair: module; builtins
:::

While a language specification need not prescribe how the language interpreter is invoked, it is useful to have a notion of a complete Python program. A complete Python program is executed in a minimally initialized environment: all built-in and standard modules are available, but none have been initialized, except for `sys`{.interpreted-text role="mod"} (various system services), `builtins`{.interpreted-text role="mod"} (built-in functions, exceptions and `None`) and `__main__`{.interpreted-text role="mod"}. The latter is used to provide the local and global namespace for execution of the complete program.

The syntax for a complete Python program is that for file input, described in the next section.

::: index
single: interactive mode pair: module; \_\_main\_\_
:::

The interpreter may also be invoked in interactive mode; in this case, it does not read and execute a complete program but reads and executes one statement (possibly compound) at a time. The initial environment is identical to that of a complete program; each statement is executed in the namespace of `__main__`{.interpreted-text role="mod"}.

::: index
single: UNIX single: Windows single: command line single: standard input
:::

A complete program can be passed to the interpreter in three forms: with the `-c`{.interpreted-text role="option"} *string* command line option, as a file passed as the first command line argument, or as standard input. If the file or standard input is a tty device, the interpreter enters interactive mode; otherwise, it executes the file as a complete program.

## File input

All input read from non-interactive files has the same form:

::: {.grammar-snippet group="python-grammar"}
file_input: (NEWLINE \| [statement]{.title-ref})\* ENDMARKER
:::

This syntax is used in the following situations:

- when parsing a complete Python program (from a file or from a string);
- when parsing a module;
- when parsing a string passed to the `exec`{.interpreted-text role="func"} function;

## Interactive input {#interactive}

Input in interactive mode is parsed using the following grammar:

::: {.grammar-snippet group="python-grammar"}
interactive_input: \[[stmt_list]{.title-ref}\] NEWLINE \| [compound_stmt]{.title-ref} NEWLINE \| ENDMARKER
:::

Note that a (top-level) compound statement must be followed by a blank line in interactive mode; this is needed to help the parser detect the end of the input.

## Expression input

::: index
single: input
:::

::: index
pair: built-in function; eval
:::

`eval`{.interpreted-text role="func"} is used for expression input. It ignores leading whitespace. The string argument to `eval`{.interpreted-text role="func"} must have the following form:

::: {.grammar-snippet group="python-grammar"}
eval_input: [expression_list]{.title-ref} NEWLINE\* ENDMARKER
:::
