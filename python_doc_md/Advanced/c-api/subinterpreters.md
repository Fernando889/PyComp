# Multiple interpreters in a Python process {#sub-interpreter-support}

While in most uses, you will only embed a single Python interpreter, there are cases where you need to create several independent interpreters in the same process and perhaps even in the same thread. Sub-interpreters allow you to do that.

The \"main\" interpreter is the first one created when the runtime initializes. It is usually the only Python interpreter in a process. Unlike sub-interpreters, the main interpreter has unique process-global responsibilities like signal handling. It is also responsible for execution during runtime initialization and is usually the active interpreter during runtime finalization. The `PyInterpreterState_Main`{.interpreted-text role="c:func"} function returns a pointer to its state.

You can switch between sub-interpreters using the `PyThreadState_Swap`{.interpreted-text role="c:func"} function. You can create and destroy them using the following functions:

> Structure containing most parameters to configure a sub-interpreter. Its values are used only in `Py_NewInterpreterFromConfig`{.interpreted-text role="c:func"} and never modified by the runtime.
>
> ::: versionadded
> 3.12
> :::
>
> Structure fields:
>
> > If this is `0` then the sub-interpreter will use its own \"object\" allocator state. Otherwise it will use (share) the main interpreter\'s.
> >
> > If this is `0` then `~PyInterpreterConfig.check_multi_interp_extensions`{.interpreted-text role="c:member"} must be `1` (non-zero). If this is `1` then `~PyInterpreterConfig.gil`{.interpreted-text role="c:member"} must not be `PyInterpreterConfig_OWN_GIL`{.interpreted-text role="c:macro"}.
>
> > If this is `0` then the runtime will not support forking the process in any thread where the sub-interpreter is currently active. Otherwise fork is unrestricted.
> >
> > Note that the `subprocess`{.interpreted-text role="mod"} module still works when fork is disallowed.
>
> > If this is `0` then the runtime will not support replacing the current process via exec (e.g. `os.execv`{.interpreted-text role="func"}) in any thread where the sub-interpreter is currently active. Otherwise exec is unrestricted.
> >
> > Note that the `subprocess`{.interpreted-text role="mod"} module still works when exec is disallowed.
>
> > If this is `0` then the sub-interpreter\'s `threading`{.interpreted-text role="mod"} module won\'t create threads. Otherwise threads are allowed.
>
> > If this is `0` then the sub-interpreter\'s `threading`{.interpreted-text role="mod"} module won\'t create daemon threads. Otherwise daemon threads are allowed (as long as `~PyInterpreterConfig.allow_threads`{.interpreted-text role="c:member"} is non-zero).
>
> > If this is `0` then all extension modules may be imported, including legacy (single-phase init) modules, in any thread where the sub-interpreter is currently active. Otherwise only multi-phase init extension modules (see `489`{.interpreted-text role="pep"}) may be imported. (Also see `Py_mod_multiple_interpreters`{.interpreted-text role="c:macro"}.)
> >
> > This must be `1` (non-zero) if `~PyInterpreterConfig.use_main_obmalloc`{.interpreted-text role="c:member"} is `0`.
>
> > This determines the operation of the GIL for the sub-interpreter. It may be one of the following:
> >
> > > Use the default selection (`PyInterpreterConfig_SHARED_GIL`{.interpreted-text role="c:macro"}).
> >
> > > Use (share) the main interpreter\'s GIL.
> >
> > > Use the sub-interpreter\'s own GIL.
> >
> > If this is `PyInterpreterConfig_OWN_GIL`{.interpreted-text role="c:macro"} then `PyInterpreterConfig.use_main_obmalloc`{.interpreted-text role="c:member"} must be `0`.

> ::: index
> pair: module; builtins pair: module; \_\_main\_\_ pair: module; sys single: stdout (in module sys) single: stderr (in module sys) single: stdin (in module sys)
> :::
>
> Create a new sub-interpreter. This is an (almost) totally separate environment for the execution of Python code. In particular, the new interpreter has separate, independent versions of all imported modules, including the fundamental modules `builtins`{.interpreted-text role="mod"}, `__main__`{.interpreted-text role="mod"} and `sys`{.interpreted-text role="mod"}. The table of loaded modules (`sys.modules`) and the module search path (`sys.path`) are also separate. The new environment has no `sys.argv` variable. It has new standard I/O stream file objects `sys.stdin`, `sys.stdout` and `sys.stderr` (however these refer to the same underlying file descriptors).
>
> The given *config* controls the options with which the interpreter is initialized.
>
> Upon success, *tstate_p* will be set to the first `thread state`{.interpreted-text role="term"} created in the new sub-interpreter. This thread state is `attached <attached thread state>`{.interpreted-text role="term"}. Note that no actual thread is created; see the discussion of thread states below. If creation of the new interpreter is unsuccessful, *tstate_p* is set to `NULL`; no exception is set since the exception state is stored in the `attached thread state`{.interpreted-text role="term"}, which might not exist.
>
> Like all other Python/C API functions, an `attached thread state`{.interpreted-text role="term"} must be present before calling this function, but it might be detached upon returning. On success, the returned thread state will be `attached <attached thread state>`{.interpreted-text role="term"}. If the sub-interpreter is created with its own `GIL`{.interpreted-text role="term"} then the `attached thread state`{.interpreted-text role="term"} of the calling interpreter will be detached. When the function returns, the new interpreter\'s `thread state`{.interpreted-text role="term"} will be `attached <attached thread state>`{.interpreted-text role="term"} to the current thread and the previous interpreter\'s `attached thread state`{.interpreted-text role="term"} will remain detached.
>
> ::: versionadded
> 3.12
> :::
>
> Sub-interpreters are most effective when isolated from each other, with certain functionality restricted:
>
> ``` c
> PyInterpreterConfig config = {
>     .use_main_obmalloc = 0,
>     .allow_fork = 0,
>     .allow_exec = 0,
>     .allow_threads = 1,
>     .allow_daemon_threads = 0,
>     .check_multi_interp_extensions = 1,
>     .gil = PyInterpreterConfig_OWN_GIL,
> };
> PyThreadState *tstate = NULL;
> PyStatus status = Py_NewInterpreterFromConfig(&tstate, &config);
> if (PyStatus_Exception(status)) {
>     Py_ExitStatusException(status);
> }
> ```
>
> Note that the config is used only briefly and does not get modified. During initialization the config\'s values are converted into various `PyInterpreterState`{.interpreted-text role="c:type"} values. A read-only copy of the config may be stored internally on the `PyInterpreterState`{.interpreted-text role="c:type"}.
>
> ::: index
> single: Py_FinalizeEx (C function) single: Py_Initialize (C function)
> :::
>
> Extension modules are shared between (sub-)interpreters as follows:
>
> - For modules using multi-phase initialization, e.g. `PyModule_FromDefAndSpec`{.interpreted-text role="c:func"}, a separate module object is created and initialized for each interpreter. Only C-level static and global variables are shared between these module objects.
>
> - For modules using legacy `single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"}, e.g. `PyModule_Create`{.interpreted-text role="c:func"}, the first time a particular extension is imported, it is initialized normally, and a (shallow) copy of its module\'s dictionary is squirreled away. When the same extension is imported by another (sub-)interpreter, a new module is initialized and filled with the contents of this copy; the extension\'s `init` function is not called. Objects in the module\'s dictionary thus end up shared across (sub-)interpreters, which might cause unwanted behavior (see [Bugs and caveats](#bugs-and-caveats) below).
>
>   Note that this is different from what happens when an extension is imported after the interpreter has been completely re-initialized by calling `Py_FinalizeEx`{.interpreted-text role="c:func"} and `Py_Initialize`{.interpreted-text role="c:func"}; in that case, the extension\'s `initmodule` function *is* called again. As with multi-phase initialization, this means that only C-level static and global variables are shared between these modules.
>
> ::: index
> single: close (in module os)
> :::

> ::: index
> pair: module; builtins pair: module; \_\_main\_\_ pair: module; sys single: stdout (in module sys) single: stderr (in module sys) single: stdin (in module sys)
> :::
>
> Create a new sub-interpreter. This is essentially just a wrapper around `Py_NewInterpreterFromConfig`{.interpreted-text role="c:func"} with a config that preserves the existing behavior. The result is an unisolated sub-interpreter that shares the main interpreter\'s GIL, allows fork/exec, allows daemon threads, and allows single-phase init modules.

> ::: index
> single: Py_FinalizeEx (C function)
> :::
>
> Destroy the (sub-)interpreter represented by the given `thread state`{.interpreted-text role="term"}. The given thread state must be `attached <attached thread state>`{.interpreted-text role="term"}. When the call returns, there will be no `attached thread state`{.interpreted-text role="term"}. All thread states associated with this interpreter are destroyed.
>
> `Py_FinalizeEx`{.interpreted-text role="c:func"} will destroy all sub-interpreters that haven\'t been explicitly destroyed at that point.

## A per-interpreter GIL {#per-interpreter-gil}

::: versionadded
3.12
:::

Using `Py_NewInterpreterFromConfig`{.interpreted-text role="c:func"} you can create a sub-interpreter that is completely isolated from other interpreters, including having its own GIL. The most important benefit of this isolation is that such an interpreter can execute Python code without being blocked by other interpreters or blocking any others. Thus a single Python process can truly take advantage of multiple CPU cores when running Python code. The isolation also encourages a different approach to concurrency than that of just using threads. (See `554`{.interpreted-text role="pep"} and `684`{.interpreted-text role="pep"}.)

Using an isolated interpreter requires vigilance in preserving that isolation. That especially means not sharing any objects or mutable state without guarantees about thread-safety. Even objects that are otherwise immutable (e.g. `None`, `(1, 5)`) can\'t normally be shared because of the refcount. One simple but less-efficient approach around this is to use a global lock around all use of some state (or object). Alternately, effectively immutable objects (like integers or strings) can be made safe in spite of their refcounts by making them `immortal`{.interpreted-text role="term"}. In fact, this has been done for the builtin singletons, small integers, and a number of other builtin objects.

If you preserve isolation then you will have access to proper multi-core computing without the complications that come with free-threading. Failure to preserve isolation will expose you to the full consequences of free-threading, including races and hard-to-debug crashes.

Aside from that, one of the main challenges of using multiple isolated interpreters is how to communicate between them safely (not break isolation) and efficiently. The runtime and stdlib do not provide any standard approach to this yet. A future stdlib module would help mitigate the effort of preserving isolation and expose effective tools for communicating (and sharing) data between interpreters.

## Bugs and caveats

Because sub-interpreters (and the main interpreter) are part of the same process, the insulation between them isn\'t perfect \-\-- for example, using low-level file operations like `os.close`{.interpreted-text role="func"} they can (accidentally or maliciously) affect each other\'s open files. Because of the way extensions are shared between (sub-)interpreters, some extensions may not work properly; this is especially likely when using single-phase initialization or (static) global variables. It is possible to insert objects created in one sub-interpreter into a namespace of another (sub-)interpreter; this should be avoided if possible.

Special care should be taken to avoid sharing user-defined functions, methods, instances or classes between sub-interpreters, since import operations executed by such objects may affect the wrong (sub-)interpreter\'s dictionary of loaded modules. It is equally important to avoid sharing objects from which the above are reachable.

Also note that combining this functionality with `PyGILState_*` APIs is delicate, because these APIs assume a bijection between Python thread states and OS-level threads, an assumption broken by the presence of sub-interpreters. It is highly recommended that you don\'t switch sub-interpreters between a pair of matching `PyGILState_Ensure`{.interpreted-text role="c:func"} and `PyGILState_Release`{.interpreted-text role="c:func"} calls. Furthermore, extensions (such as `ctypes`{.interpreted-text role="mod"}) using these APIs to allow calling of Python code from non-Python created threads will probably be broken when using sub-interpreters.

## High-level APIs

> This data structure represents the state shared by a number of cooperating threads. Threads belonging to the same interpreter share their module administration and a few other internal items. There are no public members in this structure.
>
> Threads belonging to different interpreters initially share nothing, except process state like available memory, open file descriptors and such. The global interpreter lock is also shared by all threads, regardless of to which interpreter they belong.
>
> ::: versionchanged
> 3.12
>
> `684`{.interpreted-text role="pep"} introduced the possibility of a `per-interpreter GIL <per-interpreter-gil>`{.interpreted-text role="ref"}. See `Py_NewInterpreterFromConfig`{.interpreted-text role="c:func"}.
> :::

> Get the current interpreter.
>
> Issue a fatal error if there is no `attached thread state`{.interpreted-text role="term"}. It cannot return NULL.
>
> ::: versionadded
> 3.9
> :::

> Return the interpreter\'s unique ID. If there was any error in doing so then `-1` is returned and an error is set.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.7
> :::

> Return a dictionary in which interpreter-specific data may be stored. If this function returns `NULL` then no exception has been raised and the caller should assume no interpreter-specific dict is available.
>
> This is not a replacement for `PyModule_GetState()`{.interpreted-text role="c:func"}, which extensions should use to store interpreter-specific state information.
>
> The returned dictionary is borrowed from the interpreter and is valid until interpreter shutdown.
>
> ::: versionadded
> 3.8
> :::

> Type of a frame evaluation function.
>
> The *throwflag* parameter is used by the `throw()` method of generators: if non-zero, handle the current exception.
>
> ::: versionchanged
> 3.9 The function now takes a *tstate* parameter.
> :::
>
> ::: versionchanged
> 3.11 The *frame* parameter changed from `PyFrameObject*` to `_PyInterpreterFrame*`.
> :::

> Get the frame evaluation function.
>
> See the `523`{.interpreted-text role="pep"} \"Adding a frame evaluation API to CPython\".
>
> ::: versionadded
> 3.9
> :::

> Set the frame evaluation function.
>
> See the `523`{.interpreted-text role="pep"} \"Adding a frame evaluation API to CPython\".
>
> ::: versionadded
> 3.9
> :::

## Low-level APIs

All of the following functions must be called after `Py_Initialize`{.interpreted-text role="c:func"}.

::: versionchanged
3.7 `Py_Initialize()`{.interpreted-text role="c:func"} now initializes the `GIL`{.interpreted-text role="term"} and sets an `attached thread state`{.interpreted-text role="term"}.
:::

> Create a new interpreter state object. An `attached thread state`{.interpreted-text role="term"} is not needed, but may optionally exist if it is necessary to serialize calls to this function.
>
> ::: audit-event
> cpython.PyInterpreterState_New \"\" c.PyInterpreterState_New
> :::

> Reset all information in an interpreter state object. There must be an `attached thread state`{.interpreted-text role="term"} for the interpreter.
>
> ::: audit-event
> cpython.PyInterpreterState_Clear \"\" c.PyInterpreterState_Clear
> :::

> Destroy an interpreter state object. There **should not** be an `attached thread state`{.interpreted-text role="term"} for the target interpreter. The interpreter state must have been reset with a previous call to `PyInterpreterState_Clear`{.interpreted-text role="c:func"}.

## Advanced debugger support {#advanced-debugging}

These functions are only intended to be used by advanced debugging tools.

> Return the interpreter state object at the head of the list of all such objects.

> Return the main interpreter state object.

> Return the next interpreter state object after *interp* from the list of all such objects.

> Return the pointer to the first `PyThreadState`{.interpreted-text role="c:type"} object in the list of threads associated with the interpreter *interp*.

> Return the next thread state object after *tstate* from the list of all such objects belonging to the same `PyInterpreterState`{.interpreted-text role="c:type"} object.
