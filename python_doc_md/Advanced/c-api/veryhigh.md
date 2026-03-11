# The Very High Level Layer {#veryhigh}

The functions in this chapter will let you execute Python source code given in a file or a buffer, but they will not let you interact in a more detailed way with the interpreter.

Several of these functions accept a start symbol from the grammar as a parameter. The available start symbols are `Py_eval_input`{.interpreted-text role="c:data"}, `Py_file_input`{.interpreted-text role="c:data"}, `Py_single_input`{.interpreted-text role="c:data"}, and `Py_func_type_input`{.interpreted-text role="c:data"}. These are described following the functions which accept them as parameters.

Note also that several of these functions take `FILE*`{.interpreted-text role="c:expr"} parameters. One particular issue which needs to be handled carefully is that the `FILE`{.interpreted-text role="c:type"} structure for different C libraries can be different and incompatible. Under Windows (at least), it is possible for dynamically linked extensions to actually use different libraries, so care should be taken that `FILE*`{.interpreted-text role="c:expr"} parameters are only passed to these functions if it is certain that they were created by the same library that the Python runtime is using.

> This is a simplified interface to `PyRun_AnyFileExFlags`{.interpreted-text role="c:func"} below, leaving *closeit* set to `0` and *flags* set to `NULL`.

> This is a simplified interface to `PyRun_AnyFileExFlags`{.interpreted-text role="c:func"} below, leaving the *closeit* argument set to `0`.

> This is a simplified interface to `PyRun_AnyFileExFlags`{.interpreted-text role="c:func"} below, leaving the *flags* argument set to `NULL`.

> If *fp* refers to a file associated with an interactive device (console or terminal input or Unix pseudo-terminal), return the value of `PyRun_InteractiveLoop`{.interpreted-text role="c:func"}, otherwise return the result of `PyRun_SimpleFile`{.interpreted-text role="c:func"}. *filename* is decoded from the filesystem encoding (`sys.getfilesystemencoding`{.interpreted-text role="func"}). If *filename* is `NULL`, this function uses `"???"` as the filename. If *closeit* is true, the file is closed before `PyRun_SimpleFileExFlags()` returns.

> This is a simplified interface to `PyRun_SimpleStringFlags`{.interpreted-text role="c:func"} below, leaving the `PyCompilerFlags`{.interpreted-text role="c:struct"}\* argument set to `NULL`.

> Executes the Python source code from *command* in the `__main__`{.interpreted-text role="mod"} module according to the *flags* argument. If `__main__`{.interpreted-text role="mod"} does not already exist, it is created. Returns `0` on success or `-1` if an exception was raised. If there was an error, there is no way to get the exception information. For the meaning of *flags*, see below.
>
> Note that if an otherwise unhandled `SystemExit`{.interpreted-text role="exc"} is raised, this function will not return `-1`, but exit the process, as long as `PyConfig.inspect`{.interpreted-text role="c:member"} is zero.

> This is a simplified interface to `PyRun_SimpleFileExFlags`{.interpreted-text role="c:func"} below, leaving *closeit* set to `0` and *flags* set to `NULL`.

> This is a simplified interface to `PyRun_SimpleFileExFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> Similar to `PyRun_SimpleStringFlags`{.interpreted-text role="c:func"}, but the Python source code is read from *fp* instead of an in-memory string. *filename* should be the name of the file, it is decoded from `filesystem encoding and error handler`{.interpreted-text role="term"}. If *closeit* is true, the file is closed before `PyRun_SimpleFileExFlags()` returns.
>
> :::: note
> ::: title
> Note
> :::
>
> On Windows, *fp* should be opened as binary mode (e.g. `fopen(filename, "rb")`). Otherwise, Python may not handle script file with LF line ending correctly.
> ::::

> Read and execute a single statement from a file associated with an interactive device according to the *flags* argument. The user will be prompted using `sys.ps1` and `sys.ps2`. *filename* must be a Python `str`{.interpreted-text role="class"} object.
>
> Returns `0` when the input was executed successfully, `-1` if there was an exception, or an error code from the `errcode.h`{.interpreted-text role="file"} include file distributed as part of Python if there was a parse error. (Note that `errcode.h`{.interpreted-text role="file"} is not included by `Python.h`{.interpreted-text role="file"}, so must be included specifically if needed.)

> This is a simplified interface to `PyRun_InteractiveOneFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> Similar to `PyRun_InteractiveOneObject`{.interpreted-text role="c:func"}, but *filename* is a `const char*`{.interpreted-text role="c:expr"}, which is decoded from the `filesystem encoding and error handler`{.interpreted-text role="term"}.

> This is a simplified interface to `PyRun_InteractiveLoopFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> Read and execute statements from a file associated with an interactive device until EOF is reached. The user will be prompted using `sys.ps1` and `sys.ps2`. *filename* is decoded from the `filesystem encoding and
> error handler`{.interpreted-text role="term"}. Returns `0` at EOF or a negative number upon failure.

> Can be set to point to a function with the prototype `int func(void)`. The function will be called when Python\'s interpreter prompt is about to become idle and wait for user input from the terminal. The return value is ignored. Overriding this hook can be used to integrate the interpreter\'s prompt with other event loops, as done in `Modules/_tkinter.c`{.interpreted-text role="file"} in the Python source code.
>
> ::: versionchanged
> 3.12 This function is only called from the `main interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}.
> :::

> Can be set to point to a function with the prototype `char *func(FILE *stdin, FILE *stdout, char *prompt)`, overriding the default function used to read a single line of input at the interpreter\'s prompt. The function is expected to output the string *prompt* if it\'s not `NULL`, and then read a line of input from the provided standard input file, returning the resulting string. For example, The `readline`{.interpreted-text role="mod"} module sets this hook to provide line-editing and tab-completion features.
>
> The result must be a string allocated by `PyMem_RawMalloc`{.interpreted-text role="c:func"} or `PyMem_RawRealloc`{.interpreted-text role="c:func"}, or `NULL` if an error occurred.
>
> ::: versionchanged
> 3.4 The result must be allocated by `PyMem_RawMalloc`{.interpreted-text role="c:func"} or `PyMem_RawRealloc`{.interpreted-text role="c:func"}, instead of being allocated by `PyMem_Malloc`{.interpreted-text role="c:func"} or `PyMem_Realloc`{.interpreted-text role="c:func"}.
> :::
>
> ::: versionchanged
> 3.12 This function is only called from the `main interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}.
> :::

> This is a simplified interface to `PyRun_StringFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> Execute Python source code from *str* in the context specified by the objects *globals* and *locals* with the compiler flags specified by *flags*. *globals* must be a dictionary; *locals* can be any object that implements the mapping protocol. The parameter *start* specifies the start symbol and must be one of the `available start symbols <start-symbols>`{.interpreted-text role="ref"}.
>
> Returns the result of executing the code as a Python object, or `NULL` if an exception was raised.

> This is a simplified interface to `PyRun_FileExFlags`{.interpreted-text role="c:func"} below, leaving *closeit* set to `0` and *flags* set to `NULL`.

> This is a simplified interface to `PyRun_FileExFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> This is a simplified interface to `PyRun_FileExFlags`{.interpreted-text role="c:func"} below, leaving *closeit* set to `0`.

> Similar to `PyRun_StringFlags`{.interpreted-text role="c:func"}, but the Python source code is read from *fp* instead of an in-memory string. *filename* should be the name of the file, it is decoded from the `filesystem encoding and error handler`{.interpreted-text role="term"}. If *closeit* is true, the file is closed before `PyRun_FileExFlags`{.interpreted-text role="c:func"} returns.

> This is a simplified interface to `Py_CompileStringFlags`{.interpreted-text role="c:func"} below, leaving *flags* set to `NULL`.

> This is a simplified interface to `Py_CompileStringExFlags`{.interpreted-text role="c:func"} below, with *optimize* set to `-1`.

> Parse and compile the Python source code in *str*, returning the resulting code object. The start symbol is given by *start*; this can be used to constrain the code which can be compiled and should be `available start symbols
> <start-symbols>`{.interpreted-text role="ref"}. The filename specified by *filename* is used to construct the code object and may appear in tracebacks or `SyntaxError`{.interpreted-text role="exc"} exception messages. This returns `NULL` if the code cannot be parsed or compiled.
>
> The integer *optimize* specifies the optimization level of the compiler; a value of `-1` selects the optimization level of the interpreter as given by `-O`{.interpreted-text role="option"} options. Explicit levels are `0` (no optimization; `__debug__` is true), `1` (asserts are removed, `__debug__` is false) or `2` (docstrings are removed too).
>
> ::: versionadded
> 3.4
> :::

> Like `Py_CompileStringObject`{.interpreted-text role="c:func"}, but *filename* is a byte string decoded from the `filesystem encoding and error handler`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.2
> :::

> This is a simplified interface to `PyEval_EvalCodeEx`{.interpreted-text role="c:func"}, with just the code object, and global and local variables. The other arguments are set to `NULL`.

> Evaluate a precompiled code object, given a particular environment for its evaluation. This environment consists of a dictionary of global variables, a mapping object of local variables, arrays of arguments, keywords and defaults, a dictionary of default values for `keyword-only
> <keyword-only_parameter>`{.interpreted-text role="ref"} arguments and a closure tuple of cells.

> Evaluate an execution frame. This is a simplified interface to `PyEval_EvalFrameEx`{.interpreted-text role="c:func"}, for backward compatibility.

> This is the main, unvarnished function of Python interpretation. The code object associated with the execution frame *f* is executed, interpreting bytecode and executing calls as needed. The additional *throwflag* parameter can mostly be ignored - if true, then it causes an exception to immediately be thrown; this is used for the `~generator.throw`{.interpreted-text role="meth"} methods of generator objects.
>
> ::: versionchanged
> 3.4 This function now includes a debug assertion to help ensure that it does not silently discard an active exception.
> :::

> This function changes the flags of the current evaluation frame, and returns true on success, false on failure.

> This is the structure used to hold compiler flags. In cases where code is only being compiled, it is passed as `int flags`, and in cases where code is being executed, it is passed as `PyCompilerFlags *flags`. In this case, `from __future__ import` can modify *flags*.
>
> Whenever `PyCompilerFlags *flags` is `NULL`, `~PyCompilerFlags.cf_flags`{.interpreted-text role="c:member"} is treated as equal to `0`, and any modification due to `from __future__ import` is discarded.
>
> > Compiler flags.
>
> > *cf_feature_version* is the minor Python version. It should be initialized to `PY_MINOR_VERSION`.
> >
> > The field is ignored by default, it is used if and only if `PyCF_ONLY_AST` flag is set in `~PyCompilerFlags.cf_flags`{.interpreted-text role="c:member"}.
>
> ::: versionchanged
> 3.8 Added *cf_feature_version* field.
> :::
>
> The available compiler flags are accessible as macros:
>
> The \"`PyCF`\" flags above can be combined with \"`CO_FUTURE`\" flags such as `CO_FUTURE_ANNOTATIONS`{.interpreted-text role="c:macro"} to enable features normally selectable using `future statements <future>`{.interpreted-text role="ref"}. See `c_codeobject_flags`{.interpreted-text role="ref"} for a complete list.

## Available start symbols {#start-symbols}

> ::: index
> single: Py_CompileString (C function)
> :::
>
> The start symbol from the Python grammar for isolated expressions; for use with `Py_CompileString`{.interpreted-text role="c:func"}.

> ::: index
> single: Py_CompileString (C function)
> :::
>
> The start symbol from the Python grammar for sequences of statements as read from a file or other source; for use with `Py_CompileString`{.interpreted-text role="c:func"}. This is the symbol to use when compiling arbitrarily long Python source code.

> ::: index
> single: Py_CompileString (C function)
> :::
>
> The start symbol from the Python grammar for a single statement; for use with `Py_CompileString`{.interpreted-text role="c:func"}. This is the symbol used for the interactive interpreter loop.

> ::: index
> single: Py_CompileString (C function)
> :::
>
> The start symbol from the Python grammar for a function type; for use with `Py_CompileString`{.interpreted-text role="c:func"}. This is used to parse \"signature type comments\" from `484`{.interpreted-text role="pep"}.
>
> This requires the `PyCF_ONLY_AST`{.interpreted-text role="c:macro"} flag to be set.
>
> ::: seealso
> \* `ast.FunctionType`{.interpreted-text role="py:class"} \* `484`{.interpreted-text role="pep"}
> :::
>
> ::: versionadded
> 3.8
> :::

## Stack Effects

::: seealso
`dis.stack_effect`{.interpreted-text role="py:func"}
:::

> Sentinel value representing an invalid stack effect.
>
> This is currently equivalent to `INT_MAX`.
>
> ::: versionadded
> 3.8
> :::

> Compute the stack effect of *opcode* with argument *oparg*.
>
> On success, this function returns the stack effect; on failure, this returns `PY_INVALID_STACK_EFFECT`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.4
> :::

> Similar to `PyCompile_OpcodeStackEffect`{.interpreted-text role="c:func"}, but don\'t include the stack effect of jumping if *jump* is zero.
>
> If *jump* is `0`, this will not include the stack effect of jumping, but if *jump* is `1` or `-1`, this will include it.
>
> On success, this function returns the stack effect; on failure, this returns `PY_INVALID_STACK_EFFECT`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.8
> :::
