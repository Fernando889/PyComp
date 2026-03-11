# Thread states and the global interpreter lock {#threads}

::: index
single: global interpreter lock single: interpreter lock single: lock, interpreter
:::

Unless on a `free-threaded <free threading>`{.interpreted-text role="term"} build of `CPython`{.interpreted-text role="term"}, the Python interpreter is not fully thread-safe. In order to support multi-threaded Python programs, there\'s a global lock, called the `global
interpreter lock`{.interpreted-text role="term"} or `GIL`{.interpreted-text role="term"}, that must be held by the current thread before it can safely access Python objects. Without the lock, even the simplest operations could cause problems in a multi-threaded program: for example, when two threads simultaneously increment the reference count of the same object, the reference count could end up being incremented only once instead of twice.

::: index
single: setswitchinterval (in module sys)
:::

Therefore, the rule exists that only the thread that has acquired the `GIL`{.interpreted-text role="term"} may operate on Python objects or call Python/C API functions. In order to emulate concurrency of execution, the interpreter regularly tries to switch threads (see `sys.setswitchinterval`{.interpreted-text role="func"}). The lock is also released around potentially blocking I/O operations like reading or writing a file, so that other Python threads can run in the meantime.

::: index
single: PyThreadState (C type)
:::

The Python interpreter keeps some thread-specific bookkeeping information inside a data structure called `PyThreadState`{.interpreted-text role="c:type"}, known as a `thread state`{.interpreted-text role="term"}. Each OS thread has a thread-local pointer to a `PyThreadState`{.interpreted-text role="c:type"}; a thread state referenced by this pointer is considered to be `attached <attached thread state>`{.interpreted-text role="term"}.

A thread can only have one `attached thread state`{.interpreted-text role="term"} at a time. An attached thread state is typically analogous with holding the `GIL`{.interpreted-text role="term"}, except on `free-threaded <free threading>`{.interpreted-text role="term"} builds. On builds with the `GIL`{.interpreted-text role="term"} enabled, `attaching <attached thread state>`{.interpreted-text role="term"} a thread state will block until the `GIL`{.interpreted-text role="term"} can be acquired. However, even on builds with the `GIL`{.interpreted-text role="term"} disabled, it is still required to have an attached thread state to call most of the C API.

In general, there will always be an `attached thread state`{.interpreted-text role="term"} when using Python\'s C API. Only in some specific cases (such as in a `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} block) will the thread not have an attached thread state. If uncertain, check if `PyThreadState_GetUnchecked`{.interpreted-text role="c:func"} returns `NULL`.

## Detaching the thread state from extension code

Most extension code manipulating the `thread state`{.interpreted-text role="term"} has the following simple structure:

``` c
Save the thread state in a local variable.
... Do some blocking I/O operation ...
Restore the thread state from the local variable.
```

This is so common that a pair of macros exists to simplify it:

``` c
Py_BEGIN_ALLOW_THREADS
... Do some blocking I/O operation ...
Py_END_ALLOW_THREADS
```

::: index
single: Py_BEGIN_ALLOW_THREADS (C macro) single: Py_END_ALLOW_THREADS (C macro)
:::

The `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} macro opens a new block and declares a hidden local variable; the `Py_END_ALLOW_THREADS`{.interpreted-text role="c:macro"} macro closes the block.

The block above expands to the following code:

``` c
PyThreadState *_save;

_save = PyEval_SaveThread();
... Do some blocking I/O operation ...
PyEval_RestoreThread(_save);
```

::: index
single: PyEval_RestoreThread (C function) single: PyEval_SaveThread (C function)
:::

Here is how these functions work:

The `attached thread state`{.interpreted-text role="term"} holds the `GIL`{.interpreted-text role="term"} for the entire interpreter. When detaching the `attached thread state`{.interpreted-text role="term"}, the `GIL`{.interpreted-text role="term"} is released, allowing other threads to attach a thread state to their own thread, thus getting the `GIL`{.interpreted-text role="term"} and can start executing. The pointer to the prior `attached thread state`{.interpreted-text role="term"} is stored as a local variable. Upon reaching `Py_END_ALLOW_THREADS`{.interpreted-text role="c:macro"}, the thread state that was previously `attached <attached thread state>`{.interpreted-text role="term"} is passed to `PyEval_RestoreThread`{.interpreted-text role="c:func"}. This function will block until another releases its `thread state <attached thread state>`{.interpreted-text role="term"}, thus allowing the old `thread state <attached thread state>`{.interpreted-text role="term"} to get re-attached and the C API can be called again.

For `free-threaded <free threading>`{.interpreted-text role="term"} builds, the `GIL`{.interpreted-text role="term"} is normally out of the question, but detaching the `thread state <attached thread state>`{.interpreted-text role="term"} is still required for blocking I/O and long operations. The difference is that threads don\'t have to wait for the `GIL`{.interpreted-text role="term"} to be released to attach their thread state, allowing true multi-core parallelism.

:::: note
::: title
Note
:::

Calling system I/O functions is the most common use case for detaching the `thread state <attached thread state>`{.interpreted-text role="term"}, but it can also be useful before calling long-running computations which don\'t need access to Python objects, such as compression or cryptographic functions operating over memory buffers. For example, the standard `zlib`{.interpreted-text role="mod"} and `hashlib`{.interpreted-text role="mod"} modules detach the `thread state <attached thread state>`{.interpreted-text role="term"} when compressing or hashing data.
::::

### APIs

The following macros are normally used without a trailing semicolon; look for example usage in the Python source distribution.

:::: note
::: title
Note
:::

These macros are still necessary on the `free-threaded build`{.interpreted-text role="term"} to prevent deadlocks.
::::

> This macro expands to `{ PyThreadState *_save; _save = PyEval_SaveThread();`. Note that it contains an opening brace; it must be matched with a following `Py_END_ALLOW_THREADS`{.interpreted-text role="c:macro"} macro. See above for further discussion of this macro.

> This macro expands to `PyEval_RestoreThread(_save); }`. Note that it contains a closing brace; it must be matched with an earlier `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} macro. See above for further discussion of this macro.

> This macro expands to `PyEval_RestoreThread(_save);`: it is equivalent to `Py_END_ALLOW_THREADS`{.interpreted-text role="c:macro"} without the closing brace.

> This macro expands to `_save = PyEval_SaveThread();`: it is equivalent to `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} without the opening brace and variable declaration.

## Non-Python created threads {#gilstate}

When threads are created using the dedicated Python APIs (such as the `threading`{.interpreted-text role="mod"} module), a thread state is automatically associated to them and the code shown above is therefore correct. However, when threads are created from C (for example by a third-party library with its own thread management), they don\'t hold the `GIL`{.interpreted-text role="term"}, because they don\'t have an `attached thread state`{.interpreted-text role="term"}.

If you need to call Python code from these threads (often this will be part of a callback API provided by the aforementioned third-party library), you must first register these threads with the interpreter by creating an `attached thread state`{.interpreted-text role="term"} before you can start using the Python/C API. When you are done, you should detach the `thread state <attached thread state>`{.interpreted-text role="term"}, and finally free it.

The `PyGILState_Ensure`{.interpreted-text role="c:func"} and `PyGILState_Release`{.interpreted-text role="c:func"} functions do all of the above automatically. The typical idiom for calling into Python from a C thread is:

``` c
PyGILState_STATE gstate;
gstate = PyGILState_Ensure();

/* Perform Python actions here. */
result = CallSomeFunction();
/* evaluate result or handle exception */

/* Release the thread. No Python API allowed beyond this point. */
PyGILState_Release(gstate);
```

Note that the `PyGILState_*` functions assume there is only one global interpreter (created automatically by `Py_Initialize`{.interpreted-text role="c:func"}). Python supports the creation of additional interpreters (using `Py_NewInterpreter`{.interpreted-text role="c:func"}), but mixing multiple interpreters and the `PyGILState_*` API is unsupported. This is because `PyGILState_Ensure`{.interpreted-text role="c:func"} and similar functions default to `attaching <attached thread state>`{.interpreted-text role="term"} a `thread state`{.interpreted-text role="term"} for the main interpreter, meaning that the thread can\'t safely interact with the calling subinterpreter.

## Supporting subinterpreters in non-Python threads

If you would like to support subinterpreters with non-Python created threads, you must use the `PyThreadState_*` API instead of the traditional `PyGILState_*` API.

In particular, you must store the interpreter state from the calling function and pass it to `PyThreadState_New`{.interpreted-text role="c:func"}, which will ensure that the `thread state`{.interpreted-text role="term"} is targeting the correct interpreter:

``` c
/* The return value of PyInterpreterState_Get() from the
   function that created this thread. */
PyInterpreterState *interp = ThreadData->interp;
PyThreadState *tstate = PyThreadState_New(interp);
PyThreadState_Swap(tstate);

/* GIL of the subinterpreter is now held.
   Perform Python actions here. */
result = CallSomeFunction();
/* evaluate result or handle exception */

/* Destroy the thread state. No Python API allowed beyond this point. */
PyThreadState_Clear(tstate);
PyThreadState_DeleteCurrent();
```

## Cautions about fork() {#fork-and-threads}

Another important thing to note about threads is their behaviour in the face of the C `fork`{.interpreted-text role="c:func"} call. On most systems with `fork`{.interpreted-text role="c:func"}, after a process forks only the thread that issued the fork will exist. This has a concrete impact both on how locks must be handled and on all stored state in CPython\'s runtime.

The fact that only the \"current\" thread remains means any locks held by other threads will never be released. Python solves this for `os.fork`{.interpreted-text role="func"} by acquiring the locks it uses internally before the fork, and releasing them afterwards. In addition, it resets any `lock-objects`{.interpreted-text role="ref"} in the child. When extending or embedding Python, there is no way to inform Python of additional (non-Python) locks that need to be acquired before or reset after a fork. OS facilities such as `!pthread_atfork`{.interpreted-text role="c:func"} would need to be used to accomplish the same thing. Additionally, when extending or embedding Python, calling `fork`{.interpreted-text role="c:func"} directly rather than through `os.fork`{.interpreted-text role="func"} (and returning to or calling into Python) may result in a deadlock by one of Python\'s internal locks being held by a thread that is defunct after the fork. `PyOS_AfterFork_Child`{.interpreted-text role="c:func"} tries to reset the necessary locks, but is not always able to.

The fact that all other threads go away also means that CPython\'s runtime state there must be cleaned up properly, which `os.fork`{.interpreted-text role="func"} does. This means finalizing all other `PyThreadState`{.interpreted-text role="c:type"} objects belonging to the current interpreter and all other `PyInterpreterState`{.interpreted-text role="c:type"} objects. Due to this and the special nature of the `"main" interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}, `fork`{.interpreted-text role="c:func"} should only be called in that interpreter\'s \"main\" thread, where the CPython global runtime was originally initialized. The only exception is if `exec`{.interpreted-text role="c:func"} will be called immediately after.

## High-level APIs

These are the most commonly used types and functions when writing multi-threaded C extensions.

> This data structure represents the state of a single thread. The only public data member is:
>
> > This thread\'s interpreter state.

> ::: index
> single: PyEval_AcquireThread() single: PyEval_ReleaseThread() single: PyEval_SaveThread() single: PyEval_RestoreThread()
> :::
>
> Deprecated function which does nothing.
>
> In Python 3.6 and older, this function created the GIL if it didn\'t exist.
>
> ::: versionchanged
> 3.9 The function now does nothing.
> :::
>
> ::: versionchanged
> 3.7 This function is now called by `Py_Initialize()`{.interpreted-text role="c:func"}, so you don\'t have to call it yourself anymore.
> :::
>
> ::: versionchanged
> 3.2 This function cannot be called before `Py_Initialize()`{.interpreted-text role="c:func"} anymore.
> :::
>
> ::: deprecated
> 3.9
> :::
>
> ::: index
> pair: module; [thread]{#thread}
> :::

> Detach the `attached thread state`{.interpreted-text role="term"} and return it. The thread will have no `thread state`{.interpreted-text role="term"} upon returning.

> Set the `attached thread state`{.interpreted-text role="term"} to *tstate*. The passed `thread state`{.interpreted-text role="term"} **should not** be `attached <attached thread state>`{.interpreted-text role="term"}, otherwise deadlock ensues. *tstate* will be attached upon returning.
>
> :::: note
> ::: title
> Note
> :::
>
> Calling this function from a thread when the runtime is finalizing will hang the thread until the program exits, even if the thread was not created by Python. Refer to `cautions-regarding-runtime-finalization`{.interpreted-text role="ref"} for more details.
> ::::
>
> ::: versionchanged
> 3.14 Hangs the current thread, rather than terminating it, if called while the interpreter is finalizing.
> :::

> Return the `attached thread state`{.interpreted-text role="term"}. If the thread has no attached thread state, (such as when inside of `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} block), then this issues a fatal error (so that the caller needn\'t check for `NULL`).
>
> See also `PyThreadState_GetUnchecked`{.interpreted-text role="c:func"}.

> Similar to `PyThreadState_Get`{.interpreted-text role="c:func"}, but don\'t kill the process with a fatal error if it is NULL. The caller is responsible to check if the result is NULL.
>
> ::: versionadded
> 3.13 In Python 3.5 to 3.12, the function was private and known as `_PyThreadState_UncheckedGet()`.
> :::

> Set the `attached thread state`{.interpreted-text role="term"} to *tstate*, and return the `thread state`{.interpreted-text role="term"} that was attached prior to calling.
>
> This function is safe to call without an `attached thread state`{.interpreted-text role="term"}; it will simply return `NULL` indicating that there was no prior thread state.
>
> ::: seealso
> `PyEval_ReleaseThread`{.interpreted-text role="c:func"}
> :::
>
> :::: note
> ::: title
> Note
> :::
>
> Similar to `PyGILState_Ensure`{.interpreted-text role="c:func"}, this function will hang the thread if the runtime is finalizing.
> ::::

## GIL-state APIs

The following functions use thread-local storage, and are not compatible with sub-interpreters:

> The type of the value returned by `PyGILState_Ensure`{.interpreted-text role="c:func"} and passed to `PyGILState_Release`{.interpreted-text role="c:func"}.
>
> > The GIL was already held when `PyGILState_Ensure`{.interpreted-text role="c:func"} was called.
>
> > The GIL was not held when `PyGILState_Ensure`{.interpreted-text role="c:func"} was called.

> Ensure that the current thread is ready to call the Python C API regardless of the current state of Python, or of the `attached thread state`{.interpreted-text role="term"}. This may be called as many times as desired by a thread as long as each call is matched with a call to `PyGILState_Release`{.interpreted-text role="c:func"}. In general, other thread-related APIs may be used between `PyGILState_Ensure`{.interpreted-text role="c:func"} and `PyGILState_Release`{.interpreted-text role="c:func"} calls as long as the thread state is restored to its previous state before the Release(). For example, normal usage of the `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:macro"} and `Py_END_ALLOW_THREADS`{.interpreted-text role="c:macro"} macros is acceptable.
>
> The return value is an opaque \"handle\" to the `attached thread state`{.interpreted-text role="term"} when `PyGILState_Ensure`{.interpreted-text role="c:func"} was called, and must be passed to `PyGILState_Release`{.interpreted-text role="c:func"} to ensure Python is left in the same state. Even though recursive calls are allowed, these handles *cannot* be shared - each unique call to `PyGILState_Ensure`{.interpreted-text role="c:func"} must save the handle for its call to `PyGILState_Release`{.interpreted-text role="c:func"}.
>
> When the function returns, there will be an `attached thread state`{.interpreted-text role="term"} and the thread will be able to call arbitrary Python code. Failure is a fatal error.
>
> :::: warning
> ::: title
> Warning
> :::
>
> Calling this function when the runtime is finalizing is unsafe. Doing so will either hang the thread until the program ends, or fully crash the interpreter in rare cases. Refer to `cautions-regarding-runtime-finalization`{.interpreted-text role="ref"} for more details.
> ::::
>
> ::: versionchanged
> 3.14 Hangs the current thread, rather than terminating it, if called while the interpreter is finalizing.
> :::

> Release any resources previously acquired. After this call, Python\'s state will be the same as it was prior to the corresponding `PyGILState_Ensure`{.interpreted-text role="c:func"} call (but generally this state will be unknown to the caller, hence the use of the GILState API).
>
> Every call to `PyGILState_Ensure`{.interpreted-text role="c:func"} must be matched by a call to `PyGILState_Release`{.interpreted-text role="c:func"} on the same thread.

> Get the `attached thread state`{.interpreted-text role="term"} for this thread. May return `NULL` if no GILState API has been used on the current thread. Note that the main thread always has such a thread-state, even if no auto-thread-state call has been made on the main thread. This is mainly a helper/diagnostic function.
>
> :::: note
> ::: title
> Note
> :::
>
> This function may return non-`NULL` even when the `thread state`{.interpreted-text role="term"} is detached. Prefer `PyThreadState_Get`{.interpreted-text role="c:func"} or `PyThreadState_GetUnchecked`{.interpreted-text role="c:func"} for most cases.
> ::::
>
> ::: seealso
> `PyThreadState_Get`{.interpreted-text role="c:func"}
> :::

> Return `1` if the current thread is holding the `GIL`{.interpreted-text role="term"} and `0` otherwise. This function can be called from any thread at any time. Only if it has had its `thread state <attached thread state>`{.interpreted-text role="term"} initialized via `PyGILState_Ensure`{.interpreted-text role="c:func"} will it return `1`. This is mainly a helper/diagnostic function. It can be useful for example in callback contexts or memory allocation functions when knowing that the `GIL`{.interpreted-text role="term"} is locked can allow the caller to perform sensitive actions or otherwise behave differently.
>
> :::: note
> ::: title
> Note
> :::
>
> If the current Python process has ever created a subinterpreter, this function will *always* return `1`. Prefer `PyThreadState_GetUnchecked`{.interpreted-text role="c:func"} for most cases.
> ::::
>
> ::: versionadded
> 3.4
> :::

## Low-level APIs

> Create a new thread state object belonging to the given interpreter object. An `attached thread state`{.interpreted-text role="term"} is not needed.

> Reset all information in a `thread state`{.interpreted-text role="term"} object. *tstate* must be `attached <attached thread state>`{.interpreted-text role="term"}
>
> ::: versionchanged
> 3.9 This function now calls the `!PyThreadState.on_delete`{.interpreted-text role="c:member"} callback. Previously, that happened in `PyThreadState_Delete`{.interpreted-text role="c:func"}.
> :::
>
> ::: versionchanged
> 3.13 The `!PyThreadState.on_delete`{.interpreted-text role="c:member"} callback was removed.
> :::

> Destroy a `thread state`{.interpreted-text role="term"} object. *tstate* should not be `attached <attached thread state>`{.interpreted-text role="term"} to any thread. *tstate* must have been reset with a previous call to `PyThreadState_Clear`{.interpreted-text role="c:func"}.

> Detach the `attached thread state`{.interpreted-text role="term"} (which must have been reset with a previous call to `PyThreadState_Clear`{.interpreted-text role="c:func"}) and then destroy it.
>
> No `thread state`{.interpreted-text role="term"} will be `attached <attached thread state>`{.interpreted-text role="term"} upon returning.

> Get the current frame of the Python thread state *tstate*.
>
> Return a `strong reference`{.interpreted-text role="term"}. Return `NULL` if no frame is currently executing.
>
> See also `PyEval_GetFrame`{.interpreted-text role="c:func"}.
>
> *tstate* must not be `NULL`, and must be `attached <attached thread state>`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.9
> :::

> Get the unique `thread state`{.interpreted-text role="term"} identifier of the Python thread state *tstate*.
>
> *tstate* must not be `NULL`, and must be `attached <attached thread state>`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.9
> :::

> Get the interpreter of the Python thread state *tstate*.
>
> *tstate* must not be `NULL`, and must be `attached <attached thread state>`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.9
> :::

> Suspend tracing and profiling in the Python thread state *tstate*.
>
> Resume them using the `PyThreadState_LeaveTracing`{.interpreted-text role="c:func"} function.
>
> ::: versionadded
> 3.11
> :::

> Resume tracing and profiling in the Python thread state *tstate* suspended by the `PyThreadState_EnterTracing`{.interpreted-text role="c:func"} function.
>
> See also `PyEval_SetTrace`{.interpreted-text role="c:func"} and `PyEval_SetProfile`{.interpreted-text role="c:func"} functions.
>
> ::: versionadded
> 3.11
> :::

> Set the stack protection start address and stack protection size of a Python thread state.
>
> On success, return `0`. On failure, set an exception and return `-1`.
>
> CPython implements `recursion control <recursion>`{.interpreted-text role="ref"} for C code by raising `RecursionError`{.interpreted-text role="py:exc"} when it notices that the machine execution stack is close to overflow. See for example the `Py_EnterRecursiveCall`{.interpreted-text role="c:func"} function. For this, it needs to know the location of the current thread\'s stack, which it normally gets from the operating system. When the stack is changed, for example using context switching techniques like the Boost library\'s `boost::context`, you must call `~PyUnstable_ThreadState_SetStackProtection`{.interpreted-text role="c:func"} to inform CPython of the change.
>
> Call `~PyUnstable_ThreadState_SetStackProtection`{.interpreted-text role="c:func"} either before or after changing the stack. Do not call any other Python C API between the call and the stack change.
>
> See `PyUnstable_ThreadState_ResetStackProtection`{.interpreted-text role="c:func"} for undoing this operation.
>
> ::: versionadded
> 3.15
> :::

> Reset the stack protection start address and stack protection size of a Python thread state to the operating system defaults.
>
> See `PyUnstable_ThreadState_SetStackProtection`{.interpreted-text role="c:func"} for an explanation.
>
> ::: versionadded
> 3.15
> :::

> Return a dictionary in which extensions can store thread-specific state information. Each extension should use a unique key to use to store state in the dictionary. It is okay to call this function when no `thread state`{.interpreted-text role="term"} is `attached <attached thread state>`{.interpreted-text role="term"}. If this function returns `NULL`, no exception has been raised and the caller should assume no thread state is attached.

> `Attach <attached thread state>`{.interpreted-text role="term"} *tstate* to the current thread, which must not be `NULL` or already `attached <attached thread state>`{.interpreted-text role="term"}.
>
> The calling thread must not already have an `attached thread state`{.interpreted-text role="term"}.
>
> :::: note
> ::: title
> Note
> :::
>
> Calling this function from a thread when the runtime is finalizing will hang the thread until the program exits, even if the thread was not created by Python. Refer to `cautions-regarding-runtime-finalization`{.interpreted-text role="ref"} for more details.
> ::::
>
> ::: versionchanged
> 3.8 Updated to be consistent with `PyEval_RestoreThread`{.interpreted-text role="c:func"}, `Py_END_ALLOW_THREADS`{.interpreted-text role="c:func"}, and `PyGILState_Ensure`{.interpreted-text role="c:func"}, and terminate the current thread if called while the interpreter is finalizing.
> :::
>
> ::: versionchanged
> 3.14 Hangs the current thread, rather than terminating it, if called while the interpreter is finalizing.
> :::
>
> `PyEval_RestoreThread`{.interpreted-text role="c:func"} is a higher-level function which is always available (even when threads have not been initialized).

> Detach the `attached thread state`{.interpreted-text role="term"}. The *tstate* argument, which must not be `NULL`, is only used to check that it represents the `attached thread state`{.interpreted-text role="term"} \-\-- if it isn\'t, a fatal error is reported.
>
> `PyEval_SaveThread`{.interpreted-text role="c:func"} is a higher-level function which is always available (even when threads have not been initialized).

# Asynchronous notifications

A mechanism is provided to make asynchronous notifications to the main interpreter thread. These notifications take the form of a function pointer and a void pointer argument.

> Schedule a function to be called from the main interpreter thread. On success, `0` is returned and *func* is queued for being called in the main thread. On failure, `-1` is returned without setting any exception.
>
> When successfully queued, *func* will be *eventually* called from the main interpreter thread with the argument *arg*. It will be called asynchronously with respect to normally running Python code, but with both these conditions met:
>
> - on a `bytecode`{.interpreted-text role="term"} boundary;
> - with the main thread holding an `attached thread state`{.interpreted-text role="term"} (*func* can therefore use the full C API).
>
> *func* must return `0` on success, or `-1` on failure with an exception set. *func* won\'t be interrupted to perform another asynchronous notification recursively, but it can still be interrupted to switch threads if the `thread state <attached thread state>`{.interpreted-text role="term"} is detached.
>
> This function doesn\'t need an `attached thread state`{.interpreted-text role="term"}. However, to call this function in a subinterpreter, the caller must have an `attached thread state`{.interpreted-text role="term"}. Otherwise, the function *func* can be scheduled to be called from the wrong interpreter.
>
> :::: warning
> ::: title
> Warning
> :::
>
> This is a low-level function, only useful for very special cases. There is no guarantee that *func* will be called as quick as possible. If the main thread is busy executing a system call, *func* won\'t be called before the system call returns. This function is generally **not** suitable for calling Python code from arbitrary C threads. Instead, use the `PyGILState API<gilstate>`{.interpreted-text role="ref"}.
> ::::
>
> ::: versionadded
> 3.1
> :::
>
> ::: versionchanged
> 3.9 If this function is called in a subinterpreter, the function *func* is now scheduled to be called from the subinterpreter, rather than being called from the main interpreter. Each subinterpreter now has its own list of scheduled calls.
> :::
>
> ::: versionchanged
> 3.12 This function now always schedules *func* to be run in the main interpreter.
> :::

> Execute all pending calls. This is usually executed automatically by the interpreter.
>
> This function returns `0` on success, and returns `-1` with an exception set on failure.
>
> If this is not called in the main thread of the main interpreter, this function does nothing and returns `0`. The caller must hold an `attached thread state`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.1
> :::
>
> ::: versionchanged
> 3.12 This function only runs pending calls in the main interpreter.
> :::

> Asynchronously raise an exception in a thread. The *id* argument is the thread id of the target thread; *exc* is the exception object to be raised. This function does not steal any references to *exc*. To prevent naive misuse, you must write your own C extension to call this. Must be called with an `attached thread state`{.interpreted-text role="term"}. Returns the number of thread states modified; this is normally one, but will be zero if the thread id isn\'t found. If *exc* is `NULL`, the pending exception (if any) for the thread is cleared. This raises no exceptions.
>
> ::: versionchanged
> 3.7 The type of the *id* parameter changed from `long`{.interpreted-text role="c:expr"} to `unsigned long`{.interpreted-text role="c:expr"}.
> :::

# Operating system thread APIs

> Sentinel value for an invalid thread ID.
>
> This is currently equivalent to `(unsigned long)-1`.

> Start function *func* in a new thread with argument *arg*. The resulting thread is not intended to be joined.
>
> *func* must not be `NULL`, but *arg* may be `NULL`.
>
> On success, this function returns the identifier of the new thread; on failure, this returns `PYTHREAD_INVALID_THREAD_ID`{.interpreted-text role="c:macro"}.
>
> The caller does not need to hold an `attached thread state`{.interpreted-text role="term"}.

> Return the identifier of the current thread, which will never be zero.
>
> This function cannot fail, and the caller does not need to hold an `attached thread state`{.interpreted-text role="term"}.
>
> ::: seealso
> `threading.get_ident`{.interpreted-text role="py:func"}
> :::

> Get general information about the current thread in the form of a `struct sequence <struct-sequence-objects>`{.interpreted-text role="ref"} object. This information is accessible as `sys.thread_info`{.interpreted-text role="py:attr"} in Python.
>
> On success, this returns a new `strong reference`{.interpreted-text role="term"} to the thread information; on failure, this returns `NULL` with an exception set.
>
> The caller must hold an `attached thread state`{.interpreted-text role="term"}.

> This macro is defined when the system supports native thread IDs.

> Get the native identifier of the current thread as it was assigned by the operating system\'s kernel, which will never be less than zero.
>
> This function is only available when `PY_HAVE_THREAD_NATIVE_ID`{.interpreted-text role="c:macro"} is defined.
>
> This function cannot fail, and the caller does not need to hold an `attached thread state`{.interpreted-text role="term"}.
>
> ::: seealso
> `threading.get_native_id`{.interpreted-text role="py:func"}
> :::

> Terminate the current thread. This function is generally considered unsafe and should be avoided. It is kept solely for backwards compatibility.
>
> This function is only safe to call if all functions in the full call stack are written to safely allow it.
>
> :::: warning
> ::: title
> Warning
> :::
>
> If the current system uses POSIX threads (also known as \"pthreads\"), this calls `pthread_exit(3)`{.interpreted-text role="manpage"}, which attempts to unwind the stack and call C++ destructors on some libc implementations. However, if a `noexcept` function is reached, it may terminate the process. Other systems, such as macOS, do unwinding.
>
> On Windows, this function calls `_endthreadex()`, which kills the thread without calling C++ destructors.
>
> In any case, there is a risk of corruption on the thread\'s stack.
> ::::
>
> ::: deprecated
> 3.14
> :::

> Initialize `PyThread*` APIs. Python executes this function automatically, so there\'s little need to call it from an extension module.

> Set the stack size of the current thread to *size* bytes.
>
> This function returns `0` on success, `-1` if *size* is invalid, or `-2` if the system does not support changing the stack size. This function does not set exceptions.
>
> The caller does not need to hold an `attached thread state`{.interpreted-text role="term"}.

> Return the stack size of the current thread in bytes, or `0` if the system\'s default stack size is in use.
>
> The caller does not need to hold an `attached thread state`{.interpreted-text role="term"}.
