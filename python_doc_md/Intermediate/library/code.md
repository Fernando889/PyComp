# `!code`{.interpreted-text role="mod"} \-\-- Interpreter base classes

::: {.module synopsis="Facilities to implement read-eval-print loops."}
code
:::

**Source code:** `Lib/code.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `code` module provides facilities to implement read-eval-print loops in Python. Two classes and convenience functions are included which can be used to build applications which provide an interactive interpreter prompt.

::: InteractiveInterpreter(locals=None)
This class deals with parsing and interpreter state (the user\'s namespace); it does not deal with input buffering or prompting or input file naming (the filename is always passed in explicitly). The optional *locals* argument specifies a mapping to use as the namespace in which code will be executed; it defaults to a newly created dictionary with key `'__name__'` set to `'__console__'` and key `'__doc__'` set to `None`.

Note that functions and classes objects created under an `!InteractiveInterpreter`{.interpreted-text role="class"} instance will belong to the namespace specified by *locals*. They are only pickleable if *locals* is the namespace of an existing module.
:::

:::: {.InteractiveConsole(locals=None, .filename=\"<console>\", .*, .local_exit=False)}
Closely emulate the behavior of the interactive Python interpreter. This class builds on `InteractiveInterpreter`{.interpreted-text role="class"} and adds prompting using the familiar `sys.ps1` and `sys.ps2`, and input buffering. If *local_exit* is true, `exit()` and `quit()` in the console will not raise `SystemExit`{.interpreted-text role="exc"}, but instead return to the calling code.

::: versionchanged
3.13 Added *local_exit* parameter.
:::
::::

::::: function
interact(banner=None, readfunc=None, local=None, exitmsg=None, local_exit=False)

Convenience function to run a read-eval-print loop. This creates a new instance of `InteractiveConsole`{.interpreted-text role="class"} and sets *readfunc* to be used as the `InteractiveConsole.raw_input`{.interpreted-text role="meth"} method, if provided. If *local* is provided, it is passed to the `InteractiveConsole`{.interpreted-text role="class"} constructor for use as the default namespace for the interpreter loop. If *local_exit* is provided, it is passed to the `InteractiveConsole`{.interpreted-text role="class"} constructor. The `~InteractiveConsole.interact`{.interpreted-text role="meth"} method of the instance is then run with *banner* and *exitmsg* passed as the banner and exit message to use, if provided. The console object is discarded after use.

::: versionchanged
3.6 Added *exitmsg* parameter.
:::

::: versionchanged
3.13 Added *local_exit* parameter.
:::
:::::

::: function
compile_command(source, filename=\"\<input\>\", symbol=\"single\")

This function is useful for programs that want to emulate Python\'s interpreter main loop (a.k.a. the read-eval-print loop). The tricky part is to determine when the user has entered an incomplete command that can be completed by entering more text (as opposed to a complete command or a syntax error). This function *almost* always makes the same decision as the real interpreter main loop.

*source* is the source string; *filename* is the optional filename from which source was read, defaulting to `'<input>'`; and *symbol* is the optional grammar start symbol, which should be `'single'` (the default), `'eval'` or `'exec'`.

Returns a code object (the same as `compile(source, filename, symbol)`) if the command is complete and valid; `None` if the command is incomplete; raises `SyntaxError`{.interpreted-text role="exc"} if the command is complete and contains a syntax error, or raises `OverflowError`{.interpreted-text role="exc"} or `ValueError`{.interpreted-text role="exc"} if the command contains an invalid literal.
:::

## Interactive Interpreter Objects {#interpreter-objects}

::: method
InteractiveInterpreter.runsource(source, filename=\"\<input\>\", symbol=\"single\")

Compile and run some source in the interpreter. Arguments are the same as for `compile_command`{.interpreted-text role="func"}; the default for *filename* is `'<input>'`, and for *symbol* is `'single'`. One of several things can happen:

- The input is incorrect; `compile_command`{.interpreted-text role="func"} raised an exception (`SyntaxError`{.interpreted-text role="exc"} or `OverflowError`{.interpreted-text role="exc"}). A syntax traceback will be printed by calling the `showsyntaxerror`{.interpreted-text role="meth"} method. `runsource`{.interpreted-text role="meth"} returns `False`.
- The input is incomplete, and more input is required; `compile_command`{.interpreted-text role="func"} returned `None`. `runsource`{.interpreted-text role="meth"} returns `True`.
- The input is complete; `compile_command`{.interpreted-text role="func"} returned a code object. The code is executed by calling the `runcode`{.interpreted-text role="meth"} (which also handles run-time exceptions, except for `SystemExit`{.interpreted-text role="exc"}). `runsource`{.interpreted-text role="meth"} returns `False`.

The return value can be used to decide whether to use `sys.ps1` or `sys.ps2` to prompt the next line.
:::

::: method
InteractiveInterpreter.runcode(code)

Execute a code object. When an exception occurs, `showtraceback`{.interpreted-text role="meth"} is called to display a traceback. All exceptions are caught except `SystemExit`{.interpreted-text role="exc"}, which is allowed to propagate.

A note about `KeyboardInterrupt`{.interpreted-text role="exc"}: this exception may occur elsewhere in this code, and may not always be caught. The caller should be prepared to deal with it.
:::

::: method
InteractiveInterpreter.showsyntaxerror(filename=None)

Display the syntax error that just occurred. This does not display a stack trace because there isn\'t one for syntax errors. If *filename* is given, it is stuffed into the exception instead of the default filename provided by Python\'s parser, because it always uses `'<string>'` when reading from a string. The output is written by the `write`{.interpreted-text role="meth"} method.
:::

:::: method
InteractiveInterpreter.showtraceback()

Display the exception that just occurred. We remove the first stack item because it is within the interpreter object implementation. The output is written by the `write`{.interpreted-text role="meth"} method.

::: versionchanged
3.5 The full chained traceback is displayed instead of just the primary traceback.
:::
::::

::: method
InteractiveInterpreter.write(data)

Write a string to the standard error stream (`sys.stderr`). Derived classes should override this to provide the appropriate output handling as needed.
:::

## Interactive Console Objects {#console-objects}

The `InteractiveConsole`{.interpreted-text role="class"} class is a subclass of `InteractiveInterpreter`{.interpreted-text role="class"}, and so offers all the methods of the interpreter objects as well as the following additions.

::::: method
InteractiveConsole.interact(banner=None, exitmsg=None)

Closely emulate the interactive Python console. The optional *banner* argument specify the banner to print before the first interaction; by default it prints a banner similar to the one printed by the standard Python interpreter, followed by the class name of the console object in parentheses (so as not to confuse this with the real interpreter \-- since it\'s so close!).

The optional *exitmsg* argument specifies an exit message printed when exiting. Pass the empty string to suppress the exit message. If *exitmsg* is not given or `None`, a default message is printed.

::: versionchanged
3.4 To suppress printing any banner, pass an empty string.
:::

::: versionchanged
3.6 Print an exit message when exiting.
:::
:::::

::: method
InteractiveConsole.push(line)

Push a line of source text to the interpreter. The line should not have a trailing newline; it may have internal newlines. The line is appended to a buffer and the interpreter\'s `~InteractiveInterpreter.runsource`{.interpreted-text role="meth"} method is called with the concatenated contents of the buffer as source. If this indicates that the command was executed or invalid, the buffer is reset; otherwise, the command is incomplete, and the buffer is left as it was after the line was appended. The return value is `True` if more input is required, `False` if the line was dealt with in some way (this is the same as `!runsource`{.interpreted-text role="meth"}).
:::

::: method
InteractiveConsole.resetbuffer()

Remove any unhandled source text from the input buffer.
:::

::: method
InteractiveConsole.raw_input(prompt=\"\")

Write a prompt and read a line. The returned line does not include the trailing newline. When the user enters the EOF key sequence, `EOFError`{.interpreted-text role="exc"} is raised. The base implementation reads from `sys.stdin`; a subclass may replace this with a different implementation.
:::
