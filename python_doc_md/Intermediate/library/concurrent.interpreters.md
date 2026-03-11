# `!concurrent.interpreters`{.interpreted-text role="mod"} \-\-- Multiple interpreters in the same process

::: {.module synopsis="Multiple interpreters in the same process"}
concurrent.interpreters
:::

::: versionadded
3.14
:::

**Source code:** `Lib/concurrent/interpreters`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!concurrent.interpreters`{.interpreted-text role="mod"} module constructs higher-level interfaces on top of the lower level `!_interpreters`{.interpreted-text role="mod"} module.

The module is primarily meant to provide a basic API for managing interpreters (AKA \"subinterpreters\") and running things in them. Running mostly involves switching to an interpreter (in the current thread) and calling a function in that execution context.

For concurrency, interpreters themselves (and this module) don\'t provide much more than isolation, which on its own isn\'t useful. Actual concurrency is available separately through `threads <threading>`{.interpreted-text role="mod"} See [below](#interp-concurrency)

::: seealso

`~concurrent.futures.InterpreterPoolExecutor`{.interpreted-text role="class"}

:   Combines threads with interpreters in a familiar interface.

<!-- -->

`isolating-extensions-howto`{.interpreted-text role="ref"}

:   How to update an extension module to support multiple interpreters.

`554`{.interpreted-text role="pep"}

`734`{.interpreted-text role="pep"}

`684`{.interpreted-text role="pep"}
:::

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

## Key details

Before we dive in further, there are a small number of details to keep in mind about using multiple interpreters:

- [isolated](#interp-isolation), by default
- no implicit threads
- not all PyPI packages support use in multiple interpreters yet

## Introduction {#interpreters-intro}

An \"interpreter\" is effectively the execution context of the Python runtime. It contains all of the state the runtime needs to execute a program. This includes things like the import state and builtins. (Each thread, even if there\'s only the main thread, has some extra runtime state, in addition to the current interpreter, related to the current exception and the bytecode eval loop.)

The concept and functionality of the interpreter have been a part of Python since version 2.2, but the feature was only available through the C-API and not well known, and the [isolation](#interp-isolation) was relatively incomplete until version 3.12.

### Multiple Interpreters and Isolation {#interp-isolation}

A Python implementation may support using multiple interpreters in the same process. CPython has this support. Each interpreter is effectively isolated from the others (with a limited number of carefully managed process-global exceptions to the rule).

That isolation is primarily useful as a strong separation between distinct logical components of a program, where you want to have careful control of how those components interact.

:::: note
::: title
Note
:::

Interpreters in the same process can technically never be strictly isolated from one another since there are few restrictions on memory access within the same process. The Python runtime makes a best effort at isolation but extension modules may easily violate that. Therefore, do not use multiple interpreters in security-sensitive situations, where they shouldn\'t have access to each other\'s data.
::::

### Running in an Interpreter

Running in a different interpreter involves switching to it in the current thread and then calling some function. The runtime will execute the function using the current interpreter\'s state. The `!concurrent.interpreters`{.interpreted-text role="mod"} module provides a basic API for creating and managing interpreters, as well as the switch-and-call operation.

No other threads are automatically started for the operation. There is [a helper](#interp-call-in-thread) for that though. There is another dedicated helper for calling the builtin `exec`{.interpreted-text role="func"} in an interpreter.

When `exec`{.interpreted-text role="func"} (or `eval`{.interpreted-text role="func"}) are called in an interpreter, they run using the interpreter\'s `!__main__`{.interpreted-text role="mod"} module as the \"globals\" namespace. The same is true for functions that aren\'t associated with any module. This is the same as how scripts invoked from the command-line run in the `!__main__`{.interpreted-text role="mod"} module.

### Concurrency and Parallelism {#interp-concurrency}

As noted earlier, interpreters do not provide any concurrency on their own. They strictly represent the isolated execution context the runtime will use *in the current thread*. That isolation makes them similar to processes, but they still enjoy in-process efficiency, like threads.

All that said, interpreters do naturally support certain flavors of concurrency. There\'s a powerful side effect of that isolation. It enables a different approach to concurrency than you can take with async or threads. It\'s a similar concurrency model to CSP or the actor model, a model which is relatively easy to reason about.

You can take advantage of that concurrency model in a single thread, switching back and forth between interpreters, Stackless-style. However, this model is more useful when you combine interpreters with multiple threads. This mostly involves starting a new thread, where you switch to another interpreter and run what you want there.

Each actual thread in Python, even if you\'re only running in the main thread, has its own *current* execution context. Multiple threads can use the same interpreter or different ones.

At a high level, you can think of the combination of threads and interpreters as threads with opt-in sharing.

As a significant bonus, interpreters are sufficiently isolated that they do not share the `GIL`{.interpreted-text role="term"}, which means combining threads with multiple interpreters enables full multi-core parallelism. (This has been the case since Python 3.12.)

### Communication Between Interpreters

In practice, multiple interpreters are useful only if we have a way to communicate between them. This usually involves some form of message passing, but can even mean sharing data in some carefully managed way.

With this in mind, the `!concurrent.interpreters`{.interpreted-text role="mod"} module provides a `queue.Queue`{.interpreted-text role="class"} implementation, available through `create_queue`{.interpreted-text role="func"}.

### \"Sharing\" Objects {#interp-object-sharing}

Any data actually shared between interpreters loses the thread-safety provided by the `GIL`{.interpreted-text role="term"}. There are various options for dealing with this in extension modules. However, from Python code the lack of thread-safety means objects can\'t actually be shared, with a few exceptions. Instead, a copy must be created, which means mutable objects won\'t stay in sync.

By default, most objects are copied with `pickle`{.interpreted-text role="mod"} when they are passed to another interpreter. Nearly all of the immutable builtin objects are either directly shared or copied efficiently. For example:

- `None`{.interpreted-text role="const"}
- `bool`{.interpreted-text role="class"} (`True`{.interpreted-text role="const"} and `False`{.interpreted-text role="const"})
- `bytes`{.interpreted-text role="class"}
- `str`{.interpreted-text role="class"}
- `int`{.interpreted-text role="class"}
- `float`{.interpreted-text role="class"}
- `tuple`{.interpreted-text role="class"} (of similarly supported objects)

There is a small number of Python types that actually share mutable data between interpreters:

- `memoryview`{.interpreted-text role="class"}
- `Queue`{.interpreted-text role="class"}

## Reference

This module defines the following functions:

::: function
list_all()

Return a `list`{.interpreted-text role="class"} of `Interpreter`{.interpreted-text role="class"} objects, one for each existing interpreter.
:::

::: function
get_current()

Return an `Interpreter`{.interpreted-text role="class"} object for the currently running interpreter.
:::

::: function
get_main()

Return an `Interpreter`{.interpreted-text role="class"} object for the main interpreter. This is the interpreter the runtime created to run the `REPL`{.interpreted-text role="term"} or the script given at the command-line. It is usually the only one.
:::

::: function
create()

Initialize a new (idle) Python interpreter and return a `Interpreter`{.interpreted-text role="class"} object for it.
:::

::: function
create_queue()

Initialize a new cross-interpreter queue and return a `Queue`{.interpreted-text role="class"} object for it.
:::

### Interpreter objects

:::::::::::: Interpreter(id)
A single interpreter in the current process.

Generally, `Interpreter`{.interpreted-text role="class"} shouldn\'t be called directly. Instead, use `create`{.interpreted-text role="func"} or one of the other module functions.

::: attribute
id

(read-only)

The underlying interpreter\'s ID.
:::

::: attribute
whence

(read-only)

A string describing where the interpreter came from.
:::

::: method
is_running()

Return `True` if the interpreter is currently executing code in its `!__main__`{.interpreted-text role="mod"} module and `False` otherwise.
:::

::: method
close()

Finalize and destroy the interpreter.
:::

::: method
prepare_main(ns=None, \*\*kwargs)

Bind objects in the interpreter\'s `!__main__`{.interpreted-text role="mod"} module.

Some objects are actually shared and some are copied efficiently, but most are copied via `pickle`{.interpreted-text role="mod"}. See `interp-object-sharing`{.interpreted-text role="ref"}.
:::

::: method
exec(code, /, dedent=True)

Run the given source code in the interpreter (in the current thread).
:::

::: method
call(callable, /, *args,*\*kwargs)

Return the result of calling running the given function in the interpreter (in the current thread).
:::

:::: {#interp-call-in-thread}
::: method
call_in_thread(callable, /, *args,*\*kwargs)

Run the given function in the interpreter (in a new thread).
:::
::::
::::::::::::

### Exceptions

::: exception
InterpreterError

This exception, a subclass of `Exception`{.interpreted-text role="exc"}, is raised when an interpreter-related error happens.
:::

::: exception
InterpreterNotFoundError

This exception, a subclass of `InterpreterError`{.interpreted-text role="exc"}, is raised when the targeted interpreter no longer exists.
:::

:::: exception
ExecutionFailed

This exception, a subclass of `InterpreterError`{.interpreted-text role="exc"}, is raised when the running code raised an uncaught exception.

::: attribute
excinfo

A basic snapshot of the exception raised in the other interpreter.
:::
::::

::: exception
NotShareableError

This exception, a subclass of `TypeError`{.interpreted-text role="exc"}, is raised when an object cannot be sent to another interpreter.
:::

### Communicating Between Interpreters

:::: Queue(id)
A wrapper around a low-level, cross-interpreter queue, which implements the `queue.Queue`{.interpreted-text role="class"} interface. The underlying queue can only be created through `create_queue`{.interpreted-text role="func"}.

Some objects are actually shared and some are copied efficiently, but most are copied via `pickle`{.interpreted-text role="mod"}. See `interp-object-sharing`{.interpreted-text role="ref"}.

::: attribute
id

(read-only)

The queue\'s ID.
:::
::::

::: exception
QueueEmptyError

This exception, a subclass of `queue.Empty`{.interpreted-text role="exc"}, is raised from `!Queue.get`{.interpreted-text role="meth"} and `!Queue.get_nowait`{.interpreted-text role="meth"} when the queue is empty.
:::

::: exception
QueueFullError

This exception, a subclass of `queue.Full`{.interpreted-text role="exc"}, is raised from `!Queue.put`{.interpreted-text role="meth"} and `!Queue.put_nowait`{.interpreted-text role="meth"} when the queue is full.
:::

## Basic usage

Creating an interpreter and running code in it:

    from concurrent import interpreters

    interp = interpreters.create()

    # Run in the current OS thread.

    interp.exec('print("spam!")')

    interp.exec("""if True:
        print('spam!')
        """)

    from textwrap import dedent
    interp.exec(dedent("""
        print('spam!')
        """))

    def run(arg):
        return arg

    res = interp.call(run, 'spam!')
    print(res)

    def run():
        print('spam!')

    interp.call(run)

    # Run in new OS thread.

    t = interp.call_in_thread(run)
    t.join()
