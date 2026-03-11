# `!pdb`{.interpreted-text role="mod"} \-\-- The Python Debugger {#debugger}

::: {.module synopsis="The Python debugger for interactive interpreters."}
pdb
:::

**Source code:** `Lib/pdb.py`{.interpreted-text role="source"}

::: index
single: debugging
:::

------------------------------------------------------------------------

The module `!pdb`{.interpreted-text role="mod"} defines an interactive source code debugger for Python programs. It supports setting (conditional) breakpoints and single stepping at the source line level, inspection of stack frames, source code listing, and evaluation of arbitrary Python code in the context of any stack frame. It also supports post-mortem debugging and can be called under program control.

::: index
single: Pdb (class in pdb) pair: module; bdb pair: module; cmd
:::

The debugger is extensible \-- it is actually defined as the class `Pdb`{.interpreted-text role="class"}. This is currently undocumented but easily understood by reading the source. The extension interface uses the modules `bdb`{.interpreted-text role="mod"} and `cmd`{.interpreted-text role="mod"}.

::: seealso

Module `faulthandler`{.interpreted-text role="mod"}

:   Used to dump Python tracebacks explicitly, on a fault, after a timeout, or on a user signal.

Module `traceback`{.interpreted-text role="mod"}

:   Standard interface to extract, format and print stack traces of Python programs.
:::

The typical usage to break into the debugger is to insert:

    import pdb; pdb.set_trace()

Or:

    breakpoint()

at the location you want to break into the debugger, and then run the program. You can then step through the code following this statement, and continue running without the debugger using the `continue`{.interpreted-text role="pdbcmd"} command.

::: versionchanged
3.7 The built-in `breakpoint`{.interpreted-text role="func"}, when called with defaults, can be used instead of `import pdb; pdb.set_trace()`.
:::

    def double(x):
       breakpoint()
       return x * 2
    val = 3
    print(f"{val} * 2 is {double(val)}")

The debugger\'s prompt is `(Pdb)`, which is the indicator that you are in debug mode:

    > ...(2)double()
    -> breakpoint()
    (Pdb) p x
    3
    (Pdb) continue
    3 * 2 is 6

::: versionchanged
3.3 Tab-completion via the `readline`{.interpreted-text role="mod"} module is available for commands and command arguments, e.g. the current global and local names are offered as arguments of the `p` command.
:::

## Command-line interface {#pdb-cli}

::: program
pdb
:::

You can also invoke `!pdb`{.interpreted-text role="mod"} from the command line to debug other scripts. For example:

    python -m pdb [-c command] (-m module | -p pid | pyfile) [args ...]

When invoked as a module, pdb will automatically enter post-mortem debugging if the program being debugged exits abnormally. After post-mortem debugging (or after normal exit of the program), pdb will restart the program. Automatic restarting preserves pdb\'s state (such as breakpoints) and in most cases is more useful than quitting the debugger upon program\'s exit.

:::: option

`-c, --command <command>`

:   

To execute commands as if given in a `.pdbrc`{.interpreted-text role="file"} file; see `debugger-commands`{.interpreted-text role="ref"}.

::: versionchanged
3.2 Added the `-c` option.
:::
::::

:::: option

`-m <module>`

:   

To execute modules similar to the way `python -m` does. As with a script, the debugger will pause execution just before the first line of the module.

::: versionchanged
3.7 Added the `-m` option.
:::
::::

:::: option

`-p, --pid <pid>`

:   

Attach to the process with the specified PID.

::: versionadded
3.14
:::
::::

To attach to a running Python process for remote debugging, use the `-p` or `--pid` option with the target process\'s PID:

    python -m pdb -p 1234

:::: note
::: title
Note
:::

Attaching to a process that is blocked in a system call or waiting for I/O will only work once the next bytecode instruction is executed or when the process receives a signal.
::::

Typical usage to execute a statement under control of the debugger is:

    >>> import pdb
    >>> def f(x):
    ...     print(1 / x)
    >>> pdb.run("f(2)")
    > <string>(1)<module>()
    (Pdb) continue
    0.5
    >>>

The typical usage to inspect a crashed program is:

    >>> import pdb
    >>> def f(x):
    ...     print(1 / x)
    ...
    >>> f(0)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in f
    ZeroDivisionError: division by zero
    >>> pdb.pm()
    > <stdin>(2)f()
    (Pdb) p x
    0
    (Pdb)

::: versionchanged
3.13 The implementation of `667`{.interpreted-text role="pep"} means that name assignments made via `pdb` will immediately affect the active scope, even when running inside an `optimized scope`{.interpreted-text role="term"}.
:::

The module defines the following functions; each enters the debugger in a slightly different way:

::: function
run(statement, globals=None, locals=None)

Execute the *statement* (given as a string or a code object) under debugger control. The debugger prompt appears before any code is executed; you can set breakpoints and type `continue`{.interpreted-text role="pdbcmd"}, or you can step through the statement using `step`{.interpreted-text role="pdbcmd"} or `next`{.interpreted-text role="pdbcmd"} (all these commands are explained below). The optional *globals* and *locals* arguments specify the environment in which the code is executed; by default the dictionary of the module `__main__`{.interpreted-text role="mod"} is used. (See the explanation of the built-in `exec`{.interpreted-text role="func"} or `eval`{.interpreted-text role="func"} functions.)
:::

::: function
runeval(expression, globals=None, locals=None)

Evaluate the *expression* (given as a string or a code object) under debugger control. When `runeval`{.interpreted-text role="func"} returns, it returns the value of the *expression*. Otherwise this function is similar to `run`{.interpreted-text role="func"}.
:::

::: function
runcall(function, *args,*\*kwds)

Call the *function* (a function or method object, not a string) with the given arguments. When `runcall`{.interpreted-text role="func"} returns, it returns whatever the function call returned. The debugger prompt appears as soon as the function is entered.
:::

:::::: function
set_trace(\*, header=None, commands=None)

Enter the debugger at the calling stack frame. This is useful to hard-code a breakpoint at a given point in a program, even if the code is not otherwise being debugged (e.g. when an assertion fails). If given, *header* is printed to the console just before debugging begins. The *commands* argument, if given, is a list of commands to execute when the debugger starts.

::: versionchanged
3.7 The keyword-only argument *header*.
:::

::: versionchanged
3.13 `set_trace`{.interpreted-text role="func"} will enter the debugger immediately, rather than on the next line of code to be executed.
:::

::: versionadded
3.14 The *commands* argument.
:::
::::::

:::: awaitablefunction
set_trace_async(\*, header=None, commands=None)

async version of `set_trace`{.interpreted-text role="func"}. This function should be used inside an async function with `await`{.interpreted-text role="keyword"}.

``` python
async def f():
    await pdb.set_trace_async()
```

`await`{.interpreted-text role="keyword"} statements are supported if the debugger is invoked by this function.

::: versionadded
3.14
:::
::::

:::: function
post_mortem(t=None)

Enter post-mortem debugging of the given exception or `traceback object <traceback-objects>`{.interpreted-text role="ref"}. If no value is given, it uses the exception that is currently being handled, or raises `ValueError` if there isn't one.

::: versionchanged
3.13 Support for exception objects was added.
:::
::::

::: function
pm()

Enter post-mortem debugging of the exception found in `sys.last_exc`{.interpreted-text role="data"}.
:::

:::::: function
set_default_backend(backend)

There are two supported backends for pdb: `'settrace'` and `'monitoring'`. See `bdb.Bdb`{.interpreted-text role="class"} for details. The user can set the default backend to use if none is specified when instantiating `Pdb`{.interpreted-text role="class"}. If no backend is specified, the default is `'settrace'`.

:::: note
::: title
Note
:::

`breakpoint`{.interpreted-text role="func"} and `set_trace`{.interpreted-text role="func"} will not be affected by this function. They always use `'monitoring'` backend.
::::

::: versionadded
3.14
:::
::::::

:::: function
get_default_backend()

Returns the default backend for pdb.

::: versionadded
3.14
:::
::::

The `run*` functions and `set_trace`{.interpreted-text role="func"} are aliases for instantiating the `Pdb`{.interpreted-text role="class"} class and calling the method of the same name. If you want to access further features, you have to do this yourself:

:::::::::::: {.Pdb(completekey='tab', .stdin=None, .stdout=None, .skip=None, .\\ .nosigint=False, .readrc=True, .mode=None, .backend=None, .colorize=False)}
`Pdb`{.interpreted-text role="class"} is the debugger class.

The *completekey*, *stdin* and *stdout* arguments are passed to the underlying `cmd.Cmd`{.interpreted-text role="class"} class; see the description there.

The *skip* argument, if given, must be an iterable of glob-style module name patterns. The debugger will not step into frames that originate in a module that matches one of these patterns.[^1]

By default, Pdb sets a handler for the SIGINT signal (which is sent when the user presses `Ctrl-C`{.interpreted-text role="kbd"} on the console) when you give a `continue`{.interpreted-text role="pdbcmd"} command. This allows you to break into the debugger again by pressing `Ctrl-C`{.interpreted-text role="kbd"}. If you want Pdb not to touch the SIGINT handler, set *nosigint* to true.

The *readrc* argument defaults to true and controls whether Pdb will load .pdbrc files from the filesystem.

The *mode* argument specifies how the debugger was invoked. It impacts the workings of some debugger commands. Valid values are `'inline'` (used by the breakpoint() builtin), `'cli'` (used by the command line invocation) or `None` (for backwards compatible behaviour, as before the *mode* argument was added).

The *backend* argument specifies the backend to use for the debugger. If `None` is passed, the default backend will be used. See `set_default_backend`{.interpreted-text role="func"}. Otherwise the supported backends are `'settrace'` and `'monitoring'`.

The *colorize* argument, if set to `True`, will enable colorized output in the debugger, if color is supported. This will highlight source code displayed in pdb.

Example call to enable tracing with *skip*:

    import pdb; pdb.Pdb(skip=['django.*']).set_trace()

::: audit-event
pdb.Pdb \"\" pdb.Pdb
:::

::: versionchanged
3.1 Added the *skip* parameter.
:::

::: versionchanged
3.2 Added the *nosigint* parameter. Previously, a SIGINT handler was never set by Pdb.
:::

::: versionchanged
3.6 The *readrc* argument.
:::

::: versionadded
3.14 Added the *mode* argument.
:::

::: versionadded
3.14 Added the *backend* argument.
:::

::: versionadded
3.14 Added the *colorize* argument.
:::

::: versionchanged
3.14 Inline breakpoints like `breakpoint`{.interpreted-text role="func"} or `pdb.set_trace`{.interpreted-text role="func"} will always stop the program at calling frame, ignoring the *skip* pattern (if any).
:::

::: method
run(statement, globals=None, locals=None) runeval(expression, globals=None, locals=None) runcall(function, *args,*\*kwds) set_trace()

See the documentation for the functions explained above.
:::
::::::::::::

## Debugger commands

The commands recognized by the debugger are listed below. Most commands can be abbreviated to one or two letters as indicated; e.g. `h(elp)` means that either `h` or `help` can be used to enter the help command (but not `he` or `hel`, nor `H` or `Help` or `HELP`). Arguments to commands must be separated by whitespace (spaces or tabs). Optional arguments are enclosed in square brackets (`[]`) in the command syntax; the square brackets must not be typed. Alternatives in the command syntax are separated by a vertical bar (`|`).

Entering a blank line repeats the last command entered. Exception: if the last command was a `list`{.interpreted-text role="pdbcmd"} command, the next 11 lines are listed.

Commands that the debugger doesn\'t recognize are assumed to be Python statements and are executed in the context of the program being debugged. Python statements can also be prefixed with an exclamation point (`!`). This is a powerful way to inspect the program being debugged; it is even possible to change a variable or call a function. When an exception occurs in such a statement, the exception name is printed but the debugger\'s state is not changed.

::: versionchanged
3.13 Expressions/Statements whose prefix is a pdb command are now correctly identified and executed.
:::

The debugger supports `aliases <debugger-aliases>`{.interpreted-text role="ref"}. Aliases can have parameters which allows one a certain level of adaptability to the context under examination.

Multiple commands may be entered on a single line, separated by `;;`. (A single `;` is not used as it is the separator for multiple commands in a line that is passed to the Python parser.) No intelligence is applied to separating the commands; the input is split at the first `;;` pair, even if it is in the middle of a quoted string. A workaround for strings with double semicolons is to use implicit string concatenation `';'';'` or `";"";"`.

To set a temporary global variable, use a *convenience variable*. A *convenience variable* is a variable whose name starts with `$`. For example, `$foo = 1` sets a global variable `$foo` which you can use in the debugger session. The *convenience variables* are cleared when the program resumes execution so it\'s less likely to interfere with your program compared to using normal variables like `foo = 1`.

There are four preset *convenience variables*:

- `$_frame`: the current frame you are debugging
- `$_retval`: the return value if the frame is returning
- `$_exception`: the exception if the frame is raising an exception
- `$_asynctask`: the asyncio task if pdb stops in an async function

::: versionadded
3.12

Added the *convenience variable* feature.
:::

::: versionadded
3.14 Added the `$_asynctask` convenience variable.
:::

::: index
pair: .pdbrc; file triple: debugger; configuration; file
:::

If a file `.pdbrc`{.interpreted-text role="file"} exists in the user\'s home directory or in the current directory, it is read with `'utf-8'` encoding and executed as if it had been typed at the debugger prompt, with the exception that empty lines and lines starting with `#` are ignored. This is particularly useful for aliases. If both files exist, the one in the home directory is read first and aliases defined there can be overridden by the local file.

::: versionchanged
3.2 `.pdbrc`{.interpreted-text role="file"} can now contain commands that continue debugging, such as `continue`{.interpreted-text role="pdbcmd"} or `next`{.interpreted-text role="pdbcmd"}. Previously, these commands had no effect.
:::

::: versionchanged
3.11 `.pdbrc`{.interpreted-text role="file"} is now read with `'utf-8'` encoding. Previously, it was read with the system locale encoding.
:::

::: pdbcommand
h(elp) \[command\]

Without argument, print the list of available commands. With a *command* as argument, print help about that command. `help pdb` displays the full documentation (the docstring of the `pdb`{.interpreted-text role="mod"} module). Since the *command* argument must be an identifier, `help exec` must be entered to get help on the `!` command.
:::

:::: pdbcommand
w(here) \[count\]

Print a stack trace, with the most recent frame at the bottom. if *count* is 0, print the current frame entry. If *count* is negative, print the least recent - *count* frames. If *count* is positive, print the most recent *count* frames. An arrow (`>`) indicates the current frame, which determines the context of most commands.

::: versionchanged
3.14 *count* argument is added.
:::
::::

::: pdbcommand
d(own) \[count\]

Move the current frame *count* (default one) levels down in the stack trace (to a newer frame).
:::

::: pdbcommand
u(p) \[count\]

Move the current frame *count* (default one) levels up in the stack trace (to an older frame).
:::

::: pdbcommand
b(reak) \[(\[filename:\]lineno \| function) \[, condition\]\]

With a *lineno* argument, set a break at line *lineno* in the current file. The line number may be prefixed with a *filename* and a colon, to specify a breakpoint in another file (possibly one that hasn\'t been loaded yet). The file is searched on `sys.path`{.interpreted-text role="data"}. Acceptable forms of *filename* are `/abspath/to/file.py`, `relpath/file.py`, `module` and `package.module`.

With a *function* argument, set a break at the first executable statement within that function. *function* can be any expression that evaluates to a function in the current namespace.

If a second argument is present, it is an expression which must evaluate to true before the breakpoint is honored.

Without argument, list all breaks, including for each breakpoint, the number of times that breakpoint has been hit, the current ignore count, and the associated condition if any.

Each breakpoint is assigned a number to which all the other breakpoint commands refer.
:::

::: pdbcommand
tbreak \[(\[filename:\]lineno \| function) \[, condition\]\]

Temporary breakpoint, which is removed automatically when it is first hit. The arguments are the same as for `break`{.interpreted-text role="pdbcmd"}.
:::

::: pdbcommand
cl(ear) \[filename:lineno \| bpnumber \...\]

With a *filename:lineno* argument, clear all the breakpoints at this line. With a space separated list of breakpoint numbers, clear those breakpoints. Without argument, clear all breaks (but first ask confirmation).
:::

::: pdbcommand
disable bpnumber \[bpnumber \...\]

Disable the breakpoints given as a space separated list of breakpoint numbers. Disabling a breakpoint means it cannot cause the program to stop execution, but unlike clearing a breakpoint, it remains in the list of breakpoints and can be (re-)enabled.
:::

::: pdbcommand
enable bpnumber \[bpnumber \...\]

Enable the breakpoints specified.
:::

::: pdbcommand
ignore bpnumber \[count\]

Set the ignore count for the given breakpoint number. If *count* is omitted, the ignore count is set to 0. A breakpoint becomes active when the ignore count is zero. When non-zero, the *count* is decremented each time the breakpoint is reached and the breakpoint is not disabled and any associated condition evaluates to true.
:::

::: pdbcommand
condition bpnumber \[condition\]

Set a new *condition* for the breakpoint, an expression which must evaluate to true before the breakpoint is honored. If *condition* is absent, any existing condition is removed; i.e., the breakpoint is made unconditional.
:::

:::: pdbcommand
commands \[bpnumber\]

Specify a list of commands for breakpoint number *bpnumber*. The commands themselves appear on the following lines. Type a line containing just `end` to terminate the commands. An example:

    (Pdb) commands 1
    (com) p some_variable
    (com) end
    (Pdb)

To remove all commands from a breakpoint, type `commands` and follow it immediately with `end`; that is, give no commands.

With no *bpnumber* argument, `commands` refers to the most recently set breakpoint that still exists.

You can use breakpoint commands to start your program up again. Simply use the `continue`{.interpreted-text role="pdbcmd"} command, or `step`{.interpreted-text role="pdbcmd"}, or any other command that resumes execution.

Specifying any command resuming execution (currently `continue`{.interpreted-text role="pdbcmd"}, `step`{.interpreted-text role="pdbcmd"}, `next`{.interpreted-text role="pdbcmd"}, `return`{.interpreted-text role="pdbcmd"}, `until`{.interpreted-text role="pdbcmd"}, `jump`{.interpreted-text role="pdbcmd"}, `quit`{.interpreted-text role="pdbcmd"} and their abbreviations) terminates the command list (as if that command was immediately followed by end). This is because any time you resume execution (even with a simple next or step), you may encounter another breakpoint---which could have its own command list, leading to ambiguities about which list to execute.

If the list of commands contains the `silent` command, or a command that resumes execution, then the breakpoint message containing information about the frame is not displayed.

::: versionchanged
3.14 Frame information will not be displayed if a command that resumes execution is present in the command list.
:::
::::

::: pdbcommand
s(tep)

Execute the current line, stop at the first possible occasion (either in a function that is called or on the next line in the current function).
:::

::: pdbcommand
n(ext)

Continue execution until the next line in the current function is reached or it returns. (The difference between `next`{.interpreted-text role="pdbcmd"} and `step`{.interpreted-text role="pdbcmd"} is that `step`{.interpreted-text role="pdbcmd"} stops inside a called function, while `next`{.interpreted-text role="pdbcmd"} executes called functions at (nearly) full speed, only stopping at the next line in the current function.)
:::

:::: pdbcommand
unt(il) \[lineno\]

Without argument, continue execution until the line with a number greater than the current one is reached.

With *lineno*, continue execution until a line with a number greater or equal to *lineno* is reached. In both cases, also stop when the current frame returns.

::: versionchanged
3.2 Allow giving an explicit line number.
:::
::::

::: pdbcommand
r(eturn)

Continue execution until the current function returns.
:::

::: pdbcommand
c(ont(inue))

Continue execution, only stop when a breakpoint is encountered.
:::

::: pdbcommand
j(ump) lineno

Set the next line that will be executed. Only available in the bottom-most frame. This lets you jump back and execute code again, or jump forward to skip code that you don\'t want to run.

It should be noted that not all jumps are allowed \-- for instance it is not possible to jump into the middle of a `for`{.interpreted-text role="keyword"} loop or out of a `finally`{.interpreted-text role="keyword"} clause.
:::

:::: pdbcommand
l(ist) \[first\[, last\]\]

List source code for the current file. Without arguments, list 11 lines around the current line or continue the previous listing. With `.` as argument, list 11 lines around the current line. With one argument, list 11 lines around at that line. With two arguments, list the given range; if the second argument is less than the first, it is interpreted as a count.

The current line in the current frame is indicated by `->`. If an exception is being debugged, the line where the exception was originally raised or propagated is indicated by `>>`, if it differs from the current line.

::: versionchanged
3.2 Added the `>>` marker.
:::
::::

:::: pdbcommand
ll \| longlist

List all source code for the current function or frame. Interesting lines are marked as for `list`{.interpreted-text role="pdbcmd"}.

::: versionadded
3.2
:::
::::

::: pdbcommand
a(rgs)

Print the arguments of the current function and their current values.
:::

::::: pdbcommand
p expression

Evaluate *expression* in the current context and print its value.

:::: note
::: title
Note
:::

`print()` can also be used, but is not a debugger command \-\-- this executes the Python `print`{.interpreted-text role="func"} function.
::::
:::::

::: pdbcommand
pp expression

Like the `p`{.interpreted-text role="pdbcmd"} command, except the value of *expression* is pretty-printed using the `pprint`{.interpreted-text role="mod"} module.
:::

::: pdbcommand
whatis expression

Print the type of *expression*.
:::

:::: pdbcommand
source expression

Try to get source code of *expression* and display it.

::: versionadded
3.2
:::
::::

:::::: pdbcommand
display \[expression\]

Display the value of *expression* if it changed, each time execution stops in the current frame.

Without *expression*, list all display expressions for the current frame.

:::: note
::: title
Note
:::

Display evaluates *expression* and compares to the result of the previous evaluation of *expression*, so when the result is mutable, display may not be able to pick up the changes.
::::

Example:

    lst = []
    breakpoint()
    pass
    lst.append(1)
    print(lst)

Display won\'t realize `lst` has been changed because the result of evaluation is modified in place by `lst.append(1)` before being compared:

    > example.py(3)<module>()
    -> pass
    (Pdb) display lst
    display lst: []
    (Pdb) n
    > example.py(4)<module>()
    -> lst.append(1)
    (Pdb) n
    > example.py(5)<module>()
    -> print(lst)
    (Pdb)

You can do some tricks with copy mechanism to make it work:

    > example.py(3)<module>()
    -> pass
    (Pdb) display lst[:]
    display lst[:]: []
    (Pdb) n
    > example.py(4)<module>()
    -> lst.append(1)
    (Pdb) n
    > example.py(5)<module>()
    -> print(lst)
    display lst[:]: [1]  [old: []]
    (Pdb)

::: versionadded
3.2
:::
::::::

:::: pdbcommand
undisplay \[expression\]

Do not display *expression* anymore in the current frame. Without *expression*, clear all display expressions for the current frame.

::: versionadded
3.2
:::
::::

:::::::: pdbcommand
interact

Start an interactive interpreter (using the `code`{.interpreted-text role="mod"} module) in a new global namespace initialised from the local and global namespaces for the current scope. Use `exit()` or `quit()` to exit the interpreter and return to the debugger.

:::: note
::: title
Note
:::

As `interact` creates a new dedicated namespace for code execution, assignments to variables will not affect the original namespaces. However, modifications to any referenced mutable objects will be reflected in the original namespaces as usual.
::::

::: versionadded
3.2
:::

::: versionchanged
3.13 `exit()` and `quit()` can be used to exit the `interact`{.interpreted-text role="pdbcmd"} command.
:::

::: versionchanged
3.13 `interact`{.interpreted-text role="pdbcmd"} directs its output to the debugger\'s output channel rather than `sys.stderr`{.interpreted-text role="data"}.
:::
::::::::

:::: {#debugger-aliases}
::: pdbcommand
alias \[name \[command\]\]

Create an alias called *name* that executes *command*. The *command* must *not* be enclosed in quotes. Replaceable parameters can be indicated by `%1`, `%2`, \... and `%9`, while `%*` is replaced by all the parameters. If *command* is omitted, the current alias for *name* is shown. If no arguments are given, all aliases are listed.

Aliases may be nested and can contain anything that can be legally typed at the pdb prompt. Note that internal pdb commands *can* be overridden by aliases. Such a command is then hidden until the alias is removed. Aliasing is recursively applied to the first word of the command line; all other words in the line are left alone.

As an example, here are two useful aliases (especially when placed in the `.pdbrc`{.interpreted-text role="file"} file):

    # Print instance variables (usage "pi classInst")
    alias pi for k in %1.__dict__.keys(): print(f"%1.{k} = {%1.__dict__[k]}")
    # Print instance variables in self
    alias ps pi self
:::
::::

::: pdbcommand
unalias name

Delete the specified alias *name*.
:::

::: pdbcommand
! statement

Execute the (one-line) *statement* in the context of the current stack frame. The exclamation point can be omitted unless the first word of the statement resembles a debugger command, e.g.:

``` none
(Pdb) ! n=42
(Pdb)
```

To set a global variable, you can prefix the assignment command with a `global`{.interpreted-text role="keyword"} statement on the same line, e.g.:

``` none
(Pdb) global list_options; list_options = ['-l']
(Pdb)
```
:::

:::: pdbcommand
run \[args \...\] restart \[args \...\]

Restart the debugged Python program. If *args* is supplied, it is split with `shlex`{.interpreted-text role="mod"} and the result is used as the new `sys.argv`{.interpreted-text role="data"}. History, breakpoints, actions and debugger options are preserved. `restart`{.interpreted-text role="pdbcmd"} is an alias for `run`{.interpreted-text role="pdbcmd"}.

::: versionchanged
3.14 `run`{.interpreted-text role="pdbcmd"} and `restart`{.interpreted-text role="pdbcmd"} commands are disabled when the debugger is invoked in `'inline'` mode.
:::
::::

:::: pdbcommand
q(uit)

Quit from the debugger. The program being executed is aborted. An end-of-file input is equivalent to `quit`{.interpreted-text role="pdbcmd"}.

A confirmation prompt will be shown if the debugger is invoked in `'inline'` mode. Either `y`, `Y`, `<Enter>` or `EOF` will confirm the quit.

::: versionchanged
3.14 A confirmation prompt will be shown if the debugger is invoked in `'inline'` mode. After the confirmation, the debugger will call `sys.exit`{.interpreted-text role="func"} immediately, instead of raising `bdb.BdbQuit`{.interpreted-text role="exc"} in the next trace event.
:::
::::

::: pdbcommand
debug code

Enter a recursive debugger that steps through *code* (which is an arbitrary expression or statement to be executed in the current environment).
:::

::: pdbcommand
retval

Print the return value for the last return of the current function.
:::

:::: pdbcommand
exceptions \[excnumber\]

List or jump between chained exceptions.

When using `pdb.pm()` or `Pdb.post_mortem(...)` with a chained exception instead of a traceback, it allows the user to move between the chained exceptions using `exceptions` command to list exceptions, and `exceptions <number>` to switch to that exception.

Example:

    def out():
        try:
            middle()
        except Exception as e:
            raise ValueError("reraise middle() error") from e

    def middle():
        try:
            return inner(0)
        except Exception as e:
            raise ValueError("Middle fail")

    def inner(x):
        1 / x

     out()

calling `pdb.pm()` will allow to move between exceptions:

    > example.py(5)out()
    -> raise ValueError("reraise middle() error") from e

    (Pdb) exceptions
      0 ZeroDivisionError('division by zero')
      1 ValueError('Middle fail')
    > 2 ValueError('reraise middle() error')

    (Pdb) exceptions 0
    > example.py(16)inner()
    -> 1 / x

    (Pdb) up
    > example.py(10)middle()
    -> return inner(0)

::: versionadded
3.13
:::
::::

**Footnotes**

[^1]: Whether a frame is considered to originate in a certain module is determined by the `__name__` in the frame globals.
