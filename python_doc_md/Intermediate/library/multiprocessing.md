# `!multiprocessing`{.interpreted-text role="mod"} \-\-- Process-based parallelism

::: {.module synopsis="Process-based parallelism."}
multiprocessing
:::

**Source code:** `Lib/multiprocessing/`{.interpreted-text role="source"}

------------------------------------------------------------------------

::: availability
not Android, not iOS, not WASI.

This module is not supported on `mobile platforms <mobile-availability>`{.interpreted-text role="ref"} or `WebAssembly platforms <wasm-availability>`{.interpreted-text role="ref"}.
:::

## Introduction

`!multiprocessing`{.interpreted-text role="mod"} is a package that supports spawning processes using an API similar to the `threading`{.interpreted-text role="mod"} module. The `!multiprocessing`{.interpreted-text role="mod"} package offers both local and remote concurrency, effectively side-stepping the `Global Interpreter Lock <global interpreter lock>`{.interpreted-text role="term"} by using subprocesses instead of threads. Due to this, the `!multiprocessing`{.interpreted-text role="mod"} module allows the programmer to fully leverage multiple processors on a given machine. It runs on both POSIX and Windows.

The `!multiprocessing`{.interpreted-text role="mod"} module also introduces the `~multiprocessing.pool.Pool`{.interpreted-text role="class"} object which offers a convenient means of parallelizing the execution of a function across multiple input values, distributing the input data across processes (data parallelism). The following example demonstrates the common practice of defining such functions in a module so that child processes can successfully import that module. This basic example of data parallelism using `~multiprocessing.pool.Pool`{.interpreted-text role="class"}, :

    from multiprocessing import Pool

    def f(x):
        return x*x

    if __name__ == '__main__':
        with Pool(5) as p:
            print(p.map(f, [1, 2, 3]))

will print to standard output :

    [1, 4, 9]

The `!multiprocessing`{.interpreted-text role="mod"} module also introduces APIs which do not have analogs in the `threading`{.interpreted-text role="mod"} module, like the ability to `terminate
<Process.terminate>`{.interpreted-text role="meth"}, `interrupt <Process.interrupt>`{.interpreted-text role="meth"} or `kill
<Process.kill>`{.interpreted-text role="meth"} a running process.

::: seealso
`concurrent.futures.ProcessPoolExecutor`{.interpreted-text role="class"} offers a higher level interface to push tasks to a background process without blocking execution of the calling process. Compared to using the `~multiprocessing.pool.Pool`{.interpreted-text role="class"} interface directly, the `concurrent.futures`{.interpreted-text role="mod"} API more readily allows the submission of work to the underlying process pool to be separated from waiting for the results.
:::

### The `Process`{.interpreted-text role="class"} class

In `!multiprocessing`{.interpreted-text role="mod"}, processes are spawned by creating a `Process`{.interpreted-text role="class"} object and then calling its `~Process.start`{.interpreted-text role="meth"} method. `Process`{.interpreted-text role="class"} follows the API of `threading.Thread`{.interpreted-text role="class"}. A trivial example of a multiprocess program is :

    from multiprocessing import Process

    def f(name):
        print('hello', name)

    if __name__ == '__main__':
        p = Process(target=f, args=('bob',))
        p.start()
        p.join()

To show the individual process IDs involved, here is an expanded example:

    from multiprocessing import Process
    import os

    def info(title):
        print(title)
        print('module name:', __name__)
        print('parent process:', os.getppid())
        print('process id:', os.getpid())

    def f(name):
        info('function f')
        print('hello', name)

    if __name__ == '__main__':
        info('main line')
        p = Process(target=f, args=('bob',))
        p.start()
        p.join()

For an explanation of why the `if __name__ == '__main__'` part is necessary, see `multiprocessing-programming`{.interpreted-text role="ref"}.

The arguments to `Process`{.interpreted-text role="class"} usually need to be unpickleable from within the child process. If you tried typing the above example directly into a REPL it could lead to an `AttributeError`{.interpreted-text role="exc"} in the child process trying to locate the *f* function in the `__main__` module.

### Contexts and start methods {#multiprocessing-start-methods}

Depending on the platform, `!multiprocessing`{.interpreted-text role="mod"} supports three ways to start a process. These *start methods* are

> ::: {#multiprocessing-start-method-spawn}
>
> *spawn*
>
> :   The parent process starts a fresh Python interpreter process. The child process will only inherit those resources necessary to run the process object\'s `~Process.run`{.interpreted-text role="meth"} method. In particular, unnecessary file descriptors and handles from the parent process will not be inherited. Starting a process using this method is rather slow compared to using *fork* or *forkserver*.
>
>     Available on POSIX and Windows platforms. The default on Windows and macOS.
> :::
>
> ::: {#multiprocessing-start-method-fork}
>
> *fork*
>
> :   The parent process uses `os.fork`{.interpreted-text role="func"} to fork the Python interpreter. The child process, when it begins, is effectively identical to the parent process. All resources of the parent are inherited by the child process. Note that safely forking a multithreaded process is problematic.
>
>     Available on POSIX systems.
>
>     ::: versionchanged
>     3.14 This is no longer the default start method on any platform. Code that requires *fork* must explicitly specify that via `get_context`{.interpreted-text role="func"} or `set_start_method`{.interpreted-text role="func"}.
>     :::
>
>     ::: versionchanged
>     3.12 If Python is able to detect that your process has multiple threads, the `os.fork`{.interpreted-text role="func"} function that this start method calls internally will raise a `DeprecationWarning`{.interpreted-text role="exc"}. Use a different start method. See the `os.fork`{.interpreted-text role="func"} documentation for further explanation.
>     :::
> :::
>
> ::: {#multiprocessing-start-method-forkserver}
>
> *forkserver*
>
> :   When the program starts and selects the *forkserver* start method, a server process is spawned. From then on, whenever a new process is needed, the parent process connects to the server and requests that it fork a new process. The fork server process is single threaded unless system libraries or preloaded imports spawn threads as a side-effect so it is generally safe for it to use `os.fork`{.interpreted-text role="func"}. No unnecessary resources are inherited.
>
>     Available on POSIX platforms which support passing file descriptors over Unix pipes such as Linux. The default on those.
>
>     ::: versionchanged
>     3.14 This became the default start method on POSIX platforms.
>     :::
> :::

::: versionchanged
3.4 *spawn* added on all POSIX platforms, and *forkserver* added for some POSIX platforms. Child processes no longer inherit all of the parents inheritable handles on Windows.
:::

::: versionchanged
3.8

On macOS, the *spawn* start method is now the default. The *fork* start method should be considered unsafe as it can lead to crashes of the subprocess as macOS system libraries may start threads. See `33725`{.interpreted-text role="issue"}.
:::

::: versionchanged
3.14

On POSIX platforms the default start method was changed from *fork* to *forkserver* to retain the performance but avoid common multithreaded process incompatibilities. See `84559`{.interpreted-text role="gh"}.
:::

On POSIX using the *spawn* or *forkserver* start methods will also start a *resource tracker* process which tracks the unlinked named system resources (such as named semaphores or `~multiprocessing.shared_memory.SharedMemory`{.interpreted-text role="class"} objects) created by processes of the program. When all processes have exited the resource tracker unlinks any remaining tracked object. Usually there should be none, but if a process was killed by a signal there may be some \"leaked\" resources. (Neither leaked semaphores nor shared memory segments will be automatically unlinked until the next reboot. This is problematic for both objects because the system allows only a limited number of named semaphores, and shared memory segments occupy some space in the main memory.)

To select a start method you use the `set_start_method`{.interpreted-text role="func"} in the `if __name__ == '__main__'` clause of the main module. For example:

    import multiprocessing as mp

    def foo(q):
        q.put('hello')

    if __name__ == '__main__':
        mp.set_start_method('spawn')
        q = mp.Queue()
        p = mp.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()

`set_start_method`{.interpreted-text role="func"} should not be used more than once in the program.

Alternatively, you can use `get_context`{.interpreted-text role="func"} to obtain a context object. Context objects have the same API as the multiprocessing module, and allow one to use multiple start methods in the same program. :

    import multiprocessing as mp

    def foo(q):
        q.put('hello')

    if __name__ == '__main__':
        ctx = mp.get_context('spawn')
        q = ctx.Queue()
        p = ctx.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()

Note that objects related to one context may not be compatible with processes for a different context. In particular, locks created using the *fork* context cannot be passed to processes started using the *spawn* or *forkserver* start methods.

Libraries using `!multiprocessing`{.interpreted-text role="mod"} or `~concurrent.futures.ProcessPoolExecutor`{.interpreted-text role="class"} should be designed to allow their users to provide their own multiprocessing context. Using a specific context of your own within a library can lead to incompatibilities with the rest of the library user\'s application. Always document if your library requires a specific start method.

:::: warning
::: title
Warning
:::

The `'spawn'` and `'forkserver'` start methods generally cannot be used with \"frozen\" executables (i.e., binaries produced by packages like **PyInstaller** and **cx_Freeze**) on POSIX systems. The `'fork'` start method may work if code does not use threads.
::::

### Exchanging objects between processes

`!multiprocessing`{.interpreted-text role="mod"} supports two types of communication channel between processes:

**Queues**

> The `Queue`{.interpreted-text role="class"} class is a near clone of `queue.Queue`{.interpreted-text role="class"}. For example:
>
>     from multiprocessing import Process, Queue
>
>     def f(q):
>         q.put([42, None, 'hello'])
>
>     if __name__ == '__main__':
>         q = Queue()
>         p = Process(target=f, args=(q,))
>         p.start()
>         print(q.get())    # prints "[42, None, 'hello']"
>         p.join()
>
> Queues are thread and process safe. Any object put into a `!multiprocessing`{.interpreted-text role="mod"} queue will be serialized.

**Pipes**

> The `Pipe`{.interpreted-text role="func"} function returns a pair of connection objects connected by a pipe which by default is duplex (two-way). For example:
>
>     from multiprocessing import Process, Pipe
>
>     def f(conn):
>         conn.send([42, None, 'hello'])
>         conn.close()
>
>     if __name__ == '__main__':
>         parent_conn, child_conn = Pipe()
>         p = Process(target=f, args=(child_conn,))
>         p.start()
>         print(parent_conn.recv())   # prints "[42, None, 'hello']"
>         p.join()
>
> The two connection objects returned by `Pipe`{.interpreted-text role="func"} represent the two ends of the pipe. Each connection object has `~Connection.send`{.interpreted-text role="meth"} and `~Connection.recv`{.interpreted-text role="meth"} methods (among others). Note that data in a pipe may become corrupted if two processes (or threads) try to read from or write to the *same* end of the pipe at the same time. Of course there is no risk of corruption from processes using different ends of the pipe at the same time.
>
> The `~Connection.send`{.interpreted-text role="meth"} method serializes the object and `~Connection.recv`{.interpreted-text role="meth"} re-creates the object.

### Synchronization between processes

`!multiprocessing`{.interpreted-text role="mod"} contains equivalents of all the synchronization primitives from `threading`{.interpreted-text role="mod"}. For instance one can use a lock to ensure that only one process prints to standard output at a time:

    from multiprocessing import Process, Lock

    def f(l, i):
        l.acquire()
        try:
            print('hello world', i)
        finally:
            l.release()

    if __name__ == '__main__':
        lock = Lock()

        for num in range(10):
            Process(target=f, args=(lock, num)).start()

Without using the lock output from the different processes is liable to get all mixed up.

### Sharing state between processes

As mentioned above, when doing concurrent programming it is usually best to avoid using shared state as far as possible. This is particularly true when using multiple processes.

However, if you really do need to use some shared data then `!multiprocessing`{.interpreted-text role="mod"} provides a couple of ways of doing so.

**Shared memory**

> Data can be stored in a shared memory map using `Value`{.interpreted-text role="class"} or `Array`{.interpreted-text role="class"}. For example, the following code :
>
>     from multiprocessing import Process, Value, Array
>
>     def f(n, a):
>         n.value = 3.1415927
>         for i in range(len(a)):
>             a[i] = -a[i]
>
>     if __name__ == '__main__':
>         num = Value('d', 0.0)
>         arr = Array('i', range(10))
>
>         p = Process(target=f, args=(num, arr))
>         p.start()
>         p.join()
>
>         print(num.value)
>         print(arr[:])
>
> will print :
>
>     3.1415927
>     [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
>
> The `'d'` and `'i'` arguments used when creating `num` and `arr` are typecodes of the kind used by the `array`{.interpreted-text role="mod"} module: `'d'` indicates a double precision float and `'i'` indicates a signed integer. These shared objects will be process and thread-safe.
>
> For more flexibility in using shared memory one can use the `multiprocessing.sharedctypes`{.interpreted-text role="mod"} module which supports the creation of arbitrary ctypes objects allocated from shared memory.

**Server process**

> A manager object returned by `Manager`{.interpreted-text role="func"} controls a server process which holds Python objects and allows other processes to manipulate them using proxies.
>
> A manager returned by `Manager`{.interpreted-text role="func"} will support types `list`{.interpreted-text role="class"}, `dict`{.interpreted-text role="class"}, `set`{.interpreted-text role="class"}, `~managers.Namespace`{.interpreted-text role="class"}, `Lock`{.interpreted-text role="class"}, `RLock`{.interpreted-text role="class"}, `Semaphore`{.interpreted-text role="class"}, `BoundedSemaphore`{.interpreted-text role="class"}, `Condition`{.interpreted-text role="class"}, `Event`{.interpreted-text role="class"}, `Barrier`{.interpreted-text role="class"}, `Queue`{.interpreted-text role="class"}, `Value`{.interpreted-text role="class"} and `Array`{.interpreted-text role="class"}. For example, :
>
>     from multiprocessing import Process, Manager
>
>     def f(d, l, s):
>         d[1] = '1'
>         d['2'] = 2
>         d[0.25] = None
>         l.reverse()
>         s.add('a')
>         s.add('b')
>
>     if __name__ == '__main__':
>         with Manager() as manager:
>             d = manager.dict()
>             l = manager.list(range(10))
>             s = manager.set()
>
>             p = Process(target=f, args=(d, l, s))
>             p.start()
>             p.join()
>
>             print(d)
>             print(l)
>             print(s)
>
> will print :
>
>     {0.25: None, 1: '1', '2': 2}
>     [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
>     {'a', 'b'}
>
> Server process managers are more flexible than using shared memory objects because they can be made to support arbitrary object types. Also, a single manager can be shared by processes on different computers over a network. They are, however, slower than using shared memory.

### Using a pool of workers

The `~multiprocessing.pool.Pool`{.interpreted-text role="class"} class represents a pool of worker processes. It has methods which allows tasks to be offloaded to the worker processes in a few different ways.

For example:

    from multiprocessing import Pool, TimeoutError
    import time
    import os

    def f(x):
        return x*x

    if __name__ == '__main__':
        # start 4 worker processes
        with Pool(processes=4) as pool:

            # print "[0, 1, 4,..., 81]"
            print(pool.map(f, range(10)))

            # print same numbers in arbitrary order
            for i in pool.imap_unordered(f, range(10)):
                print(i)

            # evaluate "f(20)" asynchronously
            res = pool.apply_async(f, (20,))      # runs in *only* one process
            print(res.get(timeout=1))             # prints "400"

            # evaluate "os.getpid()" asynchronously
            res = pool.apply_async(os.getpid, ()) # runs in *only* one process
            print(res.get(timeout=1))             # prints the PID of that process

            # launching multiple evaluations asynchronously *may* use more processes
            multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
            print([res.get(timeout=1) for res in multiple_results])

            # make a single worker sleep for 10 seconds
            res = pool.apply_async(time.sleep, (10,))
            try:
                print(res.get(timeout=1))
            except TimeoutError:
                print("We lacked patience and got a multiprocessing.TimeoutError")

            print("For the moment, the pool remains available for more work")

        # exiting the 'with'-block has stopped the pool
        print("Now the pool is closed and no longer available")

Note that the methods of a pool should only ever be used by the process which created it.

:::: note
::: title
Note
:::

Functionality within this package requires that the `__main__` module be importable by the children. This is covered in `multiprocessing-programming`{.interpreted-text role="ref"} however it is worth pointing out here. This means that some examples, such as the `multiprocessing.pool.Pool`{.interpreted-text role="class"} examples will not work in the interactive interpreter. For example:

    >>> from multiprocessing import Pool
    >>> p = Pool(5)
    >>> def f(x):
    ...     return x*x
    ...
    >>> with p:
    ...     p.map(f, [1,2,3])
    Process PoolWorker-1:
    Process PoolWorker-2:
    Process PoolWorker-3:
    Traceback (most recent call last):
    Traceback (most recent call last):
    Traceback (most recent call last):
    AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>
    AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>
    AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>

(If you try this it will actually output three full tracebacks interleaved in a semi-random fashion, and then you may have to stop the parent process somehow.)
::::

## Reference

The `!multiprocessing`{.interpreted-text role="mod"} package mostly replicates the API of the `threading`{.interpreted-text role="mod"} module.

### Global start method

Python supports several ways to create and initialize a process. The global start method sets the default mechanism for creating a process.

Several multiprocessing functions and methods that may also instantiate certain objects will implicitly set the global start method to the system\'s default, if it hasn't been set already. The global start method can only be set once. If you need to change the start method from the system default, you must proactively set the global start method before calling functions or methods, or creating these objects.

### `Process`{.interpreted-text role="class"} and exceptions

::::::::::::::::::::::::::: {.Process(group=None, .target=None, .name=None, .args=(), .kwargs={}, .\\ .*, .daemon=None)}
Process objects represent activity that is run in a separate process. The `Process`{.interpreted-text role="class"} class has equivalents of all the methods of `threading.Thread`{.interpreted-text role="class"}.

The constructor should always be called with keyword arguments. *group* should always be `None`; it exists solely for compatibility with `threading.Thread`{.interpreted-text role="class"}. *target* is the callable object to be invoked by the `run`{.interpreted-text role="meth"} method. It defaults to `None`, meaning nothing is called. *name* is the process name (see `name`{.interpreted-text role="attr"} for more details). *args* is the argument tuple for the target invocation. *kwargs* is a dictionary of keyword arguments for the target invocation. If provided, the keyword-only *daemon* argument sets the process `daemon`{.interpreted-text role="attr"} flag to `True` or `False`. If `None` (the default), this flag will be inherited from the creating process.

By default, no arguments are passed to *target*. The *args* argument, which defaults to `()`, can be used to specify a list or tuple of the arguments to pass to *target*.

If a subclass overrides the constructor, it must make sure it invokes the base class constructor (`super().__init__()`) before doing anything else to the process.

:::: note
::: title
Note
:::

In general, all arguments to `Process`{.interpreted-text role="class"} must be picklable. This is frequently observed when trying to create a `Process`{.interpreted-text role="class"} or use a `concurrent.futures.ProcessPoolExecutor`{.interpreted-text role="class"} from a REPL with a locally defined *target* function.

Passing a callable object defined in the current REPL session causes the child process to die via an uncaught `AttributeError`{.interpreted-text role="exc"} exception when starting as *target* must have been defined within an importable module in order to be loaded during unpickling.

Example of this uncatchable error from the child:

    >>> import multiprocessing as mp
    >>> def knigit():
    ...     print("Ni!")
    ...
    >>> process = mp.Process(target=knigit)
    >>> process.start()
    >>> Traceback (most recent call last):
      File ".../multiprocessing/spawn.py", line ..., in spawn_main
      File ".../multiprocessing/spawn.py", line ..., in _main
    AttributeError: module '__main__' has no attribute 'knigit'
    >>> process
    <SpawnProcess name='SpawnProcess-1' pid=379473 parent=378707 stopped exitcode=1>

See `multiprocessing-programming-spawn`{.interpreted-text role="ref"}. While this restriction is not true if using the `"fork"` start method, as of Python `3.14` that is no longer the default on any platform. See `multiprocessing-start-methods`{.interpreted-text role="ref"}. See also `132898`{.interpreted-text role="gh"}.
::::

::: versionchanged
3.3 Added the *daemon* parameter.
:::

::: method
run()

Method representing the process\'s activity.

You may override this method in a subclass. The standard `run`{.interpreted-text role="meth"} method invokes the callable object passed to the object\'s constructor as the target argument, if any, with sequential and keyword arguments taken from the *args* and *kwargs* arguments, respectively.

Using a list or tuple as the *args* argument passed to `Process`{.interpreted-text role="class"} achieves the same effect.

Example:

    >>> from multiprocessing import Process
    >>> p = Process(target=print, args=[1])
    >>> p.run()
    1
    >>> p = Process(target=print, args=(1,))
    >>> p.run()
    1
:::

::: method
start()

Start the process\'s activity.

This must be called at most once per process object. It arranges for the object\'s `run`{.interpreted-text role="meth"} method to be invoked in a separate process.
:::

::: method
join(\[timeout\])

If the optional argument *timeout* is `None` (the default), the method blocks until the process whose `join`{.interpreted-text role="meth"} method is called terminates. If *timeout* is a positive number, it blocks at most *timeout* seconds. Note that the method returns `None` if its process terminates or if the method times out. Check the process\'s `exitcode`{.interpreted-text role="attr"} to determine if it terminated.

A process can be joined many times.

A process cannot join itself because this would cause a deadlock. It is an error to attempt to join a process before it has been started.
:::

::: attribute
name

The process\'s name. The name is a string used for identification purposes only. It has no semantics. Multiple processes may be given the same name.

The initial name is set by the constructor. If no explicit name is provided to the constructor, a name of the form \'Process-N~1~:N~2~:\...:N~k~\' is constructed, where each N~k~ is the N-th child of its parent.
:::

::: method
is_alive

Return whether the process is alive.

Roughly, a process object is alive from the moment the `start`{.interpreted-text role="meth"} method returns until the child process terminates.
:::

::: attribute
daemon

The process\'s daemon flag, a Boolean value. This must be set before `start`{.interpreted-text role="meth"} is called.

The initial value is inherited from the creating process.

When a process exits, it attempts to terminate all of its daemonic child processes.

Note that a daemonic process is not allowed to create child processes. Otherwise a daemonic process would leave its children orphaned if it gets terminated when its parent process exits. Additionally, these are **not** Unix daemons or services, they are normal processes that will be terminated (and not joined) if non-daemonic processes have exited.
:::

In addition to the `threading.Thread`{.interpreted-text role="class"} API, `Process`{.interpreted-text role="class"} objects also support the following attributes and methods:

::: attribute
pid

Return the process ID. Before the process is spawned, this will be `None`.
:::

::: attribute
exitcode

The child\'s exit code. This will be `None` if the process has not yet terminated.

If the child\'s `run`{.interpreted-text role="meth"} method returned normally, the exit code will be 0. If it terminated via `sys.exit`{.interpreted-text role="func"} with an integer argument *N*, the exit code will be *N*.

If the child terminated due to an exception not caught within `run`{.interpreted-text role="meth"}, the exit code will be 1. If it was terminated by signal *N*, the exit code will be the negative value *-N*.
:::

::: attribute
authkey

The process\'s authentication key (a byte string).

When `!multiprocessing`{.interpreted-text role="mod"} is initialized the main process is assigned a random string using `os.urandom`{.interpreted-text role="func"}.

When a `Process`{.interpreted-text role="class"} object is created, it will inherit the authentication key of its parent process, although this may be changed by setting `authkey`{.interpreted-text role="attr"} to another byte string.

See `multiprocessing-auth-keys`{.interpreted-text role="ref"}.
:::

:::: attribute
sentinel

A numeric handle of a system object which will become \"ready\" when the process ends.

You can use this value if you want to wait on several events at once using `multiprocessing.connection.wait`{.interpreted-text role="func"}. Otherwise calling `join`{.interpreted-text role="meth"} is simpler.

On Windows, this is an OS handle usable with the `WaitForSingleObject` and `WaitForMultipleObjects` family of API calls. On POSIX, this is a file descriptor usable with primitives from the `select`{.interpreted-text role="mod"} module.

::: versionadded
3.3
:::
::::

:::: method
interrupt()

Terminate the process. Works on POSIX using the `~signal.SIGINT`{.interpreted-text role="py:const"} signal. Behavior on Windows is undefined.

By default, this terminates the child process by raising `KeyboardInterrupt`{.interpreted-text role="exc"}. This behavior can be altered by setting the respective signal handler in the child process `signal.signal`{.interpreted-text role="func"} for `~signal.SIGINT`{.interpreted-text role="py:const"}.

Note: if the child process catches and discards `KeyboardInterrupt`{.interpreted-text role="exc"}, the process will not be terminated.

Note: the default behavior will also set `exitcode`{.interpreted-text role="attr"} to `1` as if an uncaught exception was raised in the child process. To have a different `exitcode`{.interpreted-text role="attr"} you may simply catch `KeyboardInterrupt`{.interpreted-text role="exc"} and call `exit(your_code)`.

::: versionadded
3.14
:::
::::

::::: method
terminate()

Terminate the process. On POSIX this is done using the `~signal.SIGTERM`{.interpreted-text role="py:const"} signal; on Windows `!TerminateProcess`{.interpreted-text role="c:func"} is used. Note that exit handlers and finally clauses, etc., will not be executed.

Note that descendant processes of the process will *not* be terminated \-- they will simply become orphaned.

:::: warning
::: title
Warning
:::

If this method is used when the associated process is using a pipe or queue then the pipe or queue is liable to become corrupted and may become unusable by other process. Similarly, if the process has acquired a lock or semaphore etc. then terminating it is liable to cause other processes to deadlock.
::::
:::::

:::: method
kill()

Same as `terminate`{.interpreted-text role="meth"} but using the `SIGKILL` signal on POSIX.

::: versionadded
3.7
:::
::::

:::: method
close()

Close the `Process`{.interpreted-text role="class"} object, releasing all resources associated with it. `ValueError`{.interpreted-text role="exc"} is raised if the underlying process is still running. Once `close`{.interpreted-text role="meth"} returns successfully, most other methods and attributes of the `Process`{.interpreted-text role="class"} object will raise `ValueError`{.interpreted-text role="exc"}.

::: versionadded
3.7
:::
::::

Note that the `start`{.interpreted-text role="meth"}, `join`{.interpreted-text role="meth"}, `is_alive`{.interpreted-text role="meth"}, `terminate`{.interpreted-text role="meth"} and `exitcode`{.interpreted-text role="attr"} methods should only be called by the process that created the process object.

Example usage of some of the methods of `Process`{.interpreted-text role="class"}:

::: doctest
\>\>\> import multiprocessing, time, signal \>\>\> mp_context = multiprocessing.get_context(\'spawn\') \>\>\> p = mp_context.Process(target=time.sleep, args=(1000,)) \>\>\> print(p, p.is_alive()) \<\...Process \... initial\> False \>\>\> p.start() \>\>\> print(p, p.is_alive()) \<\...Process \... started\> True \>\>\> p.terminate() \>\>\> time.sleep(0.1) \>\>\> print(p, p.is_alive()) \<\...Process \... stopped exitcode=-SIGTERM\> False \>\>\> p.exitcode == -signal.SIGTERM True
:::
:::::::::::::::::::::::::::

::: exception
ProcessError

The base class of all `!multiprocessing`{.interpreted-text role="mod"} exceptions.
:::

::: exception
BufferTooShort

Exception raised by `Connection.recv_bytes_into`{.interpreted-text role="meth"} when the supplied buffer object is too small for the message read.

If `e` is an instance of `BufferTooShort`{.interpreted-text role="exc"} then `e.args[0]` will give the message as a byte string.
:::

::: exception
AuthenticationError

Raised when there is an authentication error.
:::

::: exception
TimeoutError

Raised by methods with a timeout when the timeout expires.
:::

### Pipes and Queues

When using multiple processes, one generally uses message passing for communication between processes and avoids having to use any synchronization primitives like locks.

For passing messages one can use `Pipe`{.interpreted-text role="func"} (for a connection between two processes) or a queue (which allows multiple producers and consumers).

The `Queue`{.interpreted-text role="class"}, `SimpleQueue`{.interpreted-text role="class"} and `JoinableQueue`{.interpreted-text role="class"} types are multi-producer, multi-consumer `FIFO (first-in, first-out)`{.interpreted-text role="abbr"} queues modelled on the `queue.Queue`{.interpreted-text role="class"} class in the standard library. They differ in that `Queue`{.interpreted-text role="class"} lacks the `~queue.Queue.task_done`{.interpreted-text role="meth"} and `~queue.Queue.join`{.interpreted-text role="meth"} methods introduced into Python 2.5\'s `queue.Queue`{.interpreted-text role="class"} class.

If you use `JoinableQueue`{.interpreted-text role="class"} then you **must** call `JoinableQueue.task_done`{.interpreted-text role="meth"} for each task removed from the queue or else the semaphore used to count the number of unfinished tasks may eventually overflow, raising an exception.

One difference from other Python queue implementations, is that `!multiprocessing`{.interpreted-text role="mod"} queues serializes all objects that are put into them using `pickle`{.interpreted-text role="mod"}. The object returned by the get method is a re-created object that does not share memory with the original object.

Note that one can also create a shared queue by using a manager object \-- see `multiprocessing-managers`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

`!multiprocessing`{.interpreted-text role="mod"} uses the usual `queue.Empty`{.interpreted-text role="exc"} and `queue.Full`{.interpreted-text role="exc"} exceptions to signal a timeout. They are not available in the `!multiprocessing`{.interpreted-text role="mod"} namespace so you need to import them from `queue`{.interpreted-text role="mod"}.
::::

:::: note
::: title
Note
:::

When an object is put on a queue, the object is pickled and a background thread later flushes the pickled data to an underlying pipe. This has some consequences which are a little surprising, but should not cause any practical difficulties \-- if they really bother you then you can instead use a queue created with a `manager <multiprocessing-managers>`{.interpreted-text role="ref"}.

(1) After putting an object on an empty queue there may be an infinitesimal delay before the queue\'s `~Queue.empty`{.interpreted-text role="meth"} method returns `False`{.interpreted-text role="const"} and `~Queue.get_nowait`{.interpreted-text role="meth"} can return without raising `queue.Empty`{.interpreted-text role="exc"}.
(2) If multiple processes are enqueuing objects, it is possible for the objects to be received at the other end out-of-order. However, objects enqueued by the same process will always be in the expected order with respect to each other.
::::

:::: warning
::: title
Warning
:::

If a process is killed using `Process.terminate`{.interpreted-text role="meth"} or `os.kill`{.interpreted-text role="func"} while it is trying to use a `Queue`{.interpreted-text role="class"}, then the data in the queue is likely to become corrupted. This may cause any other process to get an exception when it tries to use the queue later on.
::::

:::: warning
::: title
Warning
:::

As mentioned above, if a child process has put items on a queue (and it has not used `JoinableQueue.cancel_join_thread
<multiprocessing.Queue.cancel_join_thread>`{.interpreted-text role="meth"}), then that process will not terminate until all buffered items have been flushed to the pipe.

This means that if you try joining that process you may get a deadlock unless you are sure that all items which have been put on the queue have been consumed. Similarly, if the child process is non-daemonic then the parent process may hang on exit when it tries to join all its non-daemonic children.

Note that a queue created using a manager does not have this issue. See `multiprocessing-programming`{.interpreted-text role="ref"}.
::::

For an example of the usage of queues for interprocess communication see `multiprocessing-examples`{.interpreted-text role="ref"}.

::: function
Pipe(duplex=True)

Returns a pair `(conn1, conn2)` of `~multiprocessing.connection.Connection`{.interpreted-text role="class"} objects representing the ends of a pipe.

If *duplex* is `True` (the default) then the pipe is bidirectional. If *duplex* is `False` then the pipe is unidirectional: `conn1` can only be used for receiving messages and `conn2` can only be used for sending messages.

The `~multiprocessing.Connection.send`{.interpreted-text role="meth"} method serializes the object using `pickle`{.interpreted-text role="mod"} and the `~multiprocessing.Connection.recv`{.interpreted-text role="meth"} re-creates the object.
:::

::::::::::::::::: Queue([maxsize])
Returns a process shared queue implemented using a pipe and a few locks/semaphores. When a process first puts an item on the queue a feeder thread is started which transfers objects from a buffer into the pipe.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

The usual `queue.Empty`{.interpreted-text role="exc"} and `queue.Full`{.interpreted-text role="exc"} exceptions from the standard library\'s `queue`{.interpreted-text role="mod"} module are raised to signal timeouts.

`Queue`{.interpreted-text role="class"} implements all the methods of `queue.Queue`{.interpreted-text role="class"} except for `~queue.Queue.task_done`{.interpreted-text role="meth"} and `~queue.Queue.join`{.interpreted-text role="meth"}.

::: method
qsize()

Return the approximate size of the queue. Because of multithreading/multiprocessing semantics, this number is not reliable.

Note that this may raise `NotImplementedError`{.interpreted-text role="exc"} on platforms like macOS where `sem_getvalue()` is not implemented.
:::

::: method
empty()

Return `True` if the queue is empty, `False` otherwise. Because of multithreading/multiprocessing semantics, this is not reliable.

May raise an `OSError`{.interpreted-text role="exc"} on closed queues. (not guaranteed)
:::

::: method
full()

Return `True` if the queue is full, `False` otherwise. Because of multithreading/multiprocessing semantics, this is not reliable.
:::

:::: method
put(obj\[, block\[, timeout\]\])

Put obj into the queue. If the optional argument *block* is `True` (the default) and *timeout* is `None` (the default), block if necessary until a free slot is available. If *timeout* is a positive number, it blocks at most *timeout* seconds and raises the `queue.Full`{.interpreted-text role="exc"} exception if no free slot was available within that time. Otherwise (*block* is `False`), put an item on the queue if a free slot is immediately available, else raise the `queue.Full`{.interpreted-text role="exc"} exception (*timeout* is ignored in that case).

::: versionchanged
3.8 If the queue is closed, `ValueError`{.interpreted-text role="exc"} is raised instead of `AssertionError`{.interpreted-text role="exc"}.
:::
::::

::: method
put_nowait(obj)

Equivalent to `put(obj, False)`.
:::

:::: method
get(\[block\[, timeout\]\])

Remove and return an item from the queue. If optional args *block* is `True` (the default) and *timeout* is `None` (the default), block if necessary until an item is available. If *timeout* is a positive number, it blocks at most *timeout* seconds and raises the `queue.Empty`{.interpreted-text role="exc"} exception if no item was available within that time. Otherwise (block is `False`), return an item if one is immediately available, else raise the `queue.Empty`{.interpreted-text role="exc"} exception (*timeout* is ignored in that case).

::: versionchanged
3.8 If the queue is closed, `ValueError`{.interpreted-text role="exc"} is raised instead of `OSError`{.interpreted-text role="exc"}.
:::
::::

::: method
get_nowait()

Equivalent to `get(False)`.
:::

`multiprocessing.Queue`{.interpreted-text role="class"} has a few additional methods not found in `queue.Queue`{.interpreted-text role="class"}. These methods are usually unnecessary for most code:

::: method
close()

Close the queue: release internal resources.

A queue must not be used anymore after it is closed. For example, `~Queue.get`{.interpreted-text role="meth"}, `~Queue.put`{.interpreted-text role="meth"} and `~Queue.empty`{.interpreted-text role="meth"} methods must no longer be called.

The background thread will quit once it has flushed all buffered data to the pipe. This is called automatically when the queue is garbage collected.
:::

::: method
join_thread()

Join the background thread. This can only be used after `close`{.interpreted-text role="meth"} has been called. It blocks until the background thread exits, ensuring that all data in the buffer has been flushed to the pipe.

By default if a process is not the creator of the queue then on exit it will attempt to join the queue\'s background thread. The process can call `cancel_join_thread`{.interpreted-text role="meth"} to make `join_thread`{.interpreted-text role="meth"} do nothing.
:::

::: method
cancel_join_thread()

Prevent `join_thread`{.interpreted-text role="meth"} from blocking. In particular, this prevents the background thread from being joined automatically when the process exits \-- see `join_thread`{.interpreted-text role="meth"}.

A better name for this method might be `allow_exit_without_flush()`. It is likely to cause enqueued data to be lost, and you almost certainly will not need to use it. It is really only there if you need the current process to exit immediately without waiting to flush enqueued data to the underlying pipe, and you don\'t care about lost data.
:::

:::: note
::: title
Note
:::

This class\'s functionality requires a functioning shared semaphore implementation on the host operating system. Without one, the functionality in this class will be disabled, and attempts to instantiate a `Queue`{.interpreted-text role="class"} will result in an `ImportError`{.interpreted-text role="exc"}. See `3770`{.interpreted-text role="issue"} for additional information. The same holds true for any of the specialized queue types listed below.
::::
:::::::::::::::::

:::::::: SimpleQueue()
It is a simplified `Queue`{.interpreted-text role="class"} type, very close to a locked `Pipe`{.interpreted-text role="class"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

:::: method
close()

Close the queue: release internal resources.

A queue must not be used anymore after it is closed. For example, `get`{.interpreted-text role="meth"}, `put`{.interpreted-text role="meth"} and `empty`{.interpreted-text role="meth"} methods must no longer be called.

::: versionadded
3.9
:::
::::

::: method
empty()

Return `True` if the queue is empty, `False` otherwise.

Always raises an `OSError`{.interpreted-text role="exc"} if the SimpleQueue is closed.
:::

::: method
get()

Remove and return an item from the queue.
:::

::: method
put(item)

Put *item* into the queue.
:::
::::::::

::::: JoinableQueue([maxsize])
`JoinableQueue`{.interpreted-text role="class"}, a `Queue`{.interpreted-text role="class"} subclass, is a queue which additionally has `task_done`{.interpreted-text role="meth"} and `join`{.interpreted-text role="meth"} methods.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

::: method
task_done()

Indicate that a formerly enqueued task is complete. Used by queue consumers. For each `~Queue.get`{.interpreted-text role="meth"} used to fetch a task, a subsequent call to `task_done`{.interpreted-text role="meth"} tells the queue that the processing on the task is complete.

If a `~queue.Queue.join`{.interpreted-text role="meth"} is currently blocking, it will resume when all items have been processed (meaning that a `task_done`{.interpreted-text role="meth"} call was received for every item that had been `~Queue.put`{.interpreted-text role="meth"} into the queue).

Raises a `ValueError`{.interpreted-text role="exc"} if called more times than there were items placed in the queue.
:::

::: method
join()

Block until all items in the queue have been gotten and processed.

The count of unfinished tasks goes up whenever an item is added to the queue. The count goes down whenever a consumer calls `task_done`{.interpreted-text role="meth"} to indicate that the item was retrieved and all work on it is complete. When the count of unfinished tasks drops to zero, `~queue.Queue.join`{.interpreted-text role="meth"} unblocks.
:::
:::::

### Miscellaneous

::: function
active_children()

Return list of all live children of the current process.

Calling this has the side effect of \"joining\" any processes which have already finished.
:::

::::: function
cpu_count()

Return the number of CPUs in the system.

This number is not equivalent to the number of CPUs the current process can use. The number of usable CPUs can be obtained with `os.process_cpu_count`{.interpreted-text role="func"} (or `len(os.sched_getaffinity(0))`).

When the number of CPUs cannot be determined a `NotImplementedError`{.interpreted-text role="exc"} is raised.

::: seealso
`os.cpu_count`{.interpreted-text role="func"} `os.process_cpu_count`{.interpreted-text role="func"}
:::

::: versionchanged
3.13

The return value can also be overridden using the `-X cpu_count <-X>`{.interpreted-text role="option"} flag or `PYTHON_CPU_COUNT`{.interpreted-text role="envvar"} as this is merely a wrapper around the `os`{.interpreted-text role="mod"} cpu count APIs.
:::
:::::

::: function
current_process()

Return the `Process`{.interpreted-text role="class"} object corresponding to the current process.

An analogue of `threading.current_thread`{.interpreted-text role="func"}.
:::

:::: function
parent_process()

Return the `Process`{.interpreted-text role="class"} object corresponding to the parent process of the `current_process`{.interpreted-text role="func"}. For the main process, `parent_process` will be `None`.

::: versionadded
3.8
:::
::::

::: function
freeze_support()

Add support for when a program which uses `!multiprocessing`{.interpreted-text role="mod"} has been frozen to produce an executable. (Has been tested with **py2exe**, **PyInstaller** and **cx_Freeze**.)

One needs to call this function straight after the `if __name__ == '__main__'` line of the main module. For example:

    from multiprocessing import Process, freeze_support

    def f():
        print('hello world!')

    if __name__ == '__main__':
        freeze_support()
        Process(target=f).start()

If the `freeze_support()` line is omitted then trying to run the frozen executable will raise `RuntimeError`{.interpreted-text role="exc"}.

Calling `freeze_support()` has no effect when the start method is not *spawn*. In addition, if the module is being run normally by the Python interpreter (the program has not been frozen), then `freeze_support()` has no effect.
:::

:::: function
get_all_start_methods()

Returns a list of the supported start methods, the first of which is the default. The possible start methods are `'fork'`, `'spawn'` and `'forkserver'`. Not all platforms support all methods. See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::
::::

:::: function
get_context(method=None)

Return a context object which has the same attributes as the `!multiprocessing`{.interpreted-text role="mod"} module.

If *method* is `None` then the default context is returned. Note that if the global start method has not been set, this will set it to the system default See `global-start-method`{.interpreted-text role="ref"} for more details. Otherwise *method* should be `'fork'`, `'spawn'`, `'forkserver'`. `ValueError`{.interpreted-text role="exc"} is raised if the specified start method is not available. See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::
::::

::::: function
get_start_method(allow_none=False)

Return the name of start method used for starting processes.

If the global start method is not set and *allow_none* is `False`, the global start method is set to the default, and its name is returned. See `global-start-method`{.interpreted-text role="ref"} for more details.

The return value can be `'fork'`, `'spawn'`, `'forkserver'` or `None`. See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::

::: versionchanged
3.8

On macOS, the *spawn* start method is now the default. The *fork* start method should be considered unsafe as it can lead to crashes of the subprocess. See `33725`{.interpreted-text role="issue"}.
:::
:::::

::::: function
set_executable(executable)

Set the path of the Python interpreter to use when starting a child process. (By default `sys.executable`{.interpreted-text role="data"} is used). Embedders will probably need to do something like :

    set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))

before they can create child processes.

::: versionchanged
3.4 Now supported on POSIX when the `'spawn'` start method is used.
:::

::: versionchanged
3.11 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

::::: function
set_forkserver_preload(module_names, \*, on_error=\'ignore\')

Set a list of module names for the forkserver main process to attempt to import so that their already imported state is inherited by forked processes. This can be used as a performance enhancement to avoid repeated work in every process.

For this to work, it must be called before the forkserver process has been launched (before creating a `Pool`{.interpreted-text role="class"} or starting a `Process`{.interpreted-text role="class"}).

The *on_error* parameter controls how `ImportError`{.interpreted-text role="exc"} exceptions during module preloading are handled: `"ignore"` (default) silently ignores failures, `"warn"` causes the forkserver subprocess to emit an `ImportWarning`{.interpreted-text role="exc"} to stderr, and `"fail"` causes the forkserver subprocess to exit with the exception traceback on stderr, making subsequent process creation fail with `EOFError`{.interpreted-text role="exc"} or `ConnectionError`{.interpreted-text role="exc"}.

Only meaningful when using the `'forkserver'` start method. See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::

::: versionchanged
3.15 Added the *on_error* parameter.
:::
:::::

:::: function
set_start_method(method, force=False)

Set the method which should be used to start child processes. The *method* argument can be `'fork'`, `'spawn'` or `'forkserver'`. Raises `RuntimeError`{.interpreted-text role="exc"} if the start method has already been set and *force* is not `True`. If *method* is `None` and *force* is `True` then the start method is set to `None`. If *method* is `None` and *force* is `False` then the context is set to the default context.

Note that this should be called at most once, and it should be protected inside the `if __name__ == '__main__'` clause of the main module.

See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

::: versionadded
3.4
:::
::::

:::: note
::: title
Note
:::

`!multiprocessing`{.interpreted-text role="mod"} contains no analogues of `threading.active_count`{.interpreted-text role="func"}, `threading.enumerate`{.interpreted-text role="func"}, `threading.settrace`{.interpreted-text role="func"}, `threading.setprofile`{.interpreted-text role="func"}, `threading.Timer`{.interpreted-text role="class"}, or `threading.local`{.interpreted-text role="class"}.
::::

### Connection Objects

::: currentmodule
multiprocessing.connection
:::

Connection objects allow the sending and receiving of picklable objects or strings. They can be thought of as message oriented connected sockets.

Connection objects are usually created using `Pipe <multiprocessing.Pipe>`{.interpreted-text role="func"} \-- see also `multiprocessing-listeners-clients`{.interpreted-text role="ref"}.

::::::::::::: Connection
::: method
send(obj)

Send an object to the other end of the connection which should be read using `recv`{.interpreted-text role="meth"}.

The object must be picklable. Very large pickles (approximately 32 MiB+, though it depends on the OS) may raise a `ValueError`{.interpreted-text role="exc"} exception.
:::

::: method
recv()

Return an object sent from the other end of the connection using `send`{.interpreted-text role="meth"}. Blocks until there is something to receive. Raises `EOFError`{.interpreted-text role="exc"} if there is nothing left to receive and the other end was closed.
:::

::: method
fileno()

Return the file descriptor or handle used by the connection.
:::

::: method
close()

Close the connection.

This is called automatically when the connection is garbage collected.
:::

::: method
poll(\[timeout\])

Return whether there is any data available to be read.

If *timeout* is not specified then it will return immediately. If *timeout* is a number then this specifies the maximum time in seconds to block. If *timeout* is `None` then an infinite timeout is used.

Note that multiple connection objects may be polled at once by using `multiprocessing.connection.wait`{.interpreted-text role="func"}.
:::

::: method
send_bytes(buffer\[, offset\[, size\]\])

Send byte data from a `bytes-like object`{.interpreted-text role="term"} as a complete message.

If *offset* is given then data is read from that position in *buffer*. If *size* is given then that many bytes will be read from buffer. Very large buffers (approximately 32 MiB+, though it depends on the OS) may raise a `ValueError`{.interpreted-text role="exc"} exception
:::

:::: method
recv_bytes(\[maxlength\])

Return a complete message of byte data sent from the other end of the connection as a string. Blocks until there is something to receive. Raises `EOFError`{.interpreted-text role="exc"} if there is nothing left to receive and the other end has closed.

If *maxlength* is specified and the message is longer than *maxlength* then `OSError`{.interpreted-text role="exc"} is raised and the connection will no longer be readable.

::: versionchanged
3.3 This function used to raise `IOError`{.interpreted-text role="exc"}, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

::: method
recv_bytes_into(buffer\[, offset\])

Read into *buffer* a complete message of byte data sent from the other end of the connection and return the number of bytes in the message. Blocks until there is something to receive. Raises `EOFError`{.interpreted-text role="exc"} if there is nothing left to receive and the other end was closed.

*buffer* must be a writable `bytes-like object`{.interpreted-text role="term"}. If *offset* is given then the message will be written into the buffer from that position. Offset must be a non-negative integer less than the length of *buffer* (in bytes).

If the buffer is too short then a `BufferTooShort`{.interpreted-text role="exc"} exception is raised and the complete message is available as `e.args[0]` where `e` is the exception instance.
:::

::: versionchanged
3.3 Connection objects themselves can now be transferred between processes using `Connection.send`{.interpreted-text role="meth"} and `Connection.recv`{.interpreted-text role="meth"}.

Connection objects also now support the context management protocol \-- see `typecontextmanager`{.interpreted-text role="ref"}. `~contextmanager.__enter__`{.interpreted-text role="meth"} returns the connection object, and `~contextmanager.__exit__`{.interpreted-text role="meth"} calls `close`{.interpreted-text role="meth"}.
:::
:::::::::::::

For example:

::: doctest
\>\>\> from multiprocessing import Pipe \>\>\> a, b = Pipe() \>\>\> a.send(\[1, \'hello\', None\]) \>\>\> b.recv() \[1, \'hello\', None\] \>\>\> b.send_bytes(b\'thank you\') \>\>\> a.recv_bytes() b\'thank you\' \>\>\> import array \>\>\> arr1 = array.array(\'i\', range(5)) \>\>\> arr2 = array.array(\'i\', \[0\] \* 10) \>\>\> a.send_bytes(arr1) \>\>\> count = b.recv_bytes_into(arr2) \>\>\> assert count == len(arr1) \* arr1.itemsize \>\>\> arr2 array(\'i\', \[0, 1, 2, 3, 4, 0, 0, 0, 0, 0\])
:::

::::: {#multiprocessing-recv-pickle-security}
:::: warning
::: title
Warning
:::

The `Connection.recv`{.interpreted-text role="meth"} method automatically unpickles the data it receives, which can be a security risk unless you can trust the process which sent the message.

Therefore, unless the connection object was produced using `Pipe`{.interpreted-text role="func"} you should only use the `~Connection.recv`{.interpreted-text role="meth"} and `~Connection.send`{.interpreted-text role="meth"} methods after performing some sort of authentication. See `multiprocessing-auth-keys`{.interpreted-text role="ref"}.
::::
:::::

:::: warning
::: title
Warning
:::

If a process is killed while it is trying to read or write to a pipe then the data in the pipe is likely to become corrupted, because it may become impossible to be sure where the message boundaries lie.
::::

### Synchronization primitives

::: currentmodule
multiprocessing
:::

Generally synchronization primitives are not as necessary in a multiprocess program as they are in a multithreaded program. See the documentation for `threading`{.interpreted-text role="mod"} module.

Note that one can also create synchronization primitives by using a manager object \-- see `multiprocessing-managers`{.interpreted-text role="ref"}.

:::: {.Barrier(parties[, .action[, .timeout]])}
A barrier object: a clone of `threading.Barrier`{.interpreted-text role="class"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

::: versionadded
3.3
:::
::::

::::::: BoundedSemaphore([value])
A bounded semaphore object: a close analog of `threading.BoundedSemaphore`{.interpreted-text role="class"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

A solitary difference from its close analog exists: its `acquire` method\'s first argument is named *block*, as is consistent with `Lock.acquire`{.interpreted-text role="meth"}.

:::: method
locked()

Return a boolean indicating whether this object is locked right now.

::: versionadded
3.14
:::
::::

:::: note
::: title
Note
:::

On macOS, this is indistinguishable from `Semaphore`{.interpreted-text role="class"} because `sem_getvalue()` is not implemented on that platform.
::::
:::::::

:::: Condition([lock])
A condition variable: an alias for `threading.Condition`{.interpreted-text role="class"}.

If *lock* is specified then it should be a `Lock`{.interpreted-text role="class"} or `RLock`{.interpreted-text role="class"} object from `!multiprocessing`{.interpreted-text role="mod"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

::: versionchanged
3.3 The `~threading.Condition.wait_for`{.interpreted-text role="meth"} method was added.
:::
::::

::: Event()
A clone of `threading.Event`{.interpreted-text role="class"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.
:::

::::::: Lock()
A non-recursive lock object: a close analog of `threading.Lock`{.interpreted-text role="class"}. Once a process or thread has acquired a lock, subsequent attempts to acquire it from any process or thread will block until it is released; any process or thread may release it. The concepts and behaviors of `threading.Lock`{.interpreted-text role="class"} as it applies to threads are replicated here in `multiprocessing.Lock`{.interpreted-text role="class"} as it applies to either processes or threads, except as noted.

Note that `Lock`{.interpreted-text role="class"} is actually a factory function which returns an instance of `multiprocessing.synchronize.Lock` initialized with a default context.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

`Lock`{.interpreted-text role="class"} supports the `context manager`{.interpreted-text role="term"} protocol and thus may be used in `with`{.interpreted-text role="keyword"} statements.

::: method
acquire(block=True, timeout=None)

Acquire a lock, blocking or non-blocking.

With the *block* argument set to `True` (the default), the method call will block until the lock is in an unlocked state, then set it to locked and return `True`. Note that the name of this first argument differs from that in `threading.Lock.acquire`{.interpreted-text role="meth"}.

With the *block* argument set to `False`, the method call does not block. If the lock is currently in a locked state, return `False`; otherwise set the lock to a locked state and return `True`.

When invoked with a positive, floating-point value for *timeout*, block for at most the number of seconds specified by *timeout* as long as the lock can not be acquired. Invocations with a negative value for *timeout* are equivalent to a *timeout* of zero. Invocations with a *timeout* value of `None` (the default) set the timeout period to infinite. Note that the treatment of negative or `None` values for *timeout* differs from the implemented behavior in `threading.Lock.acquire`{.interpreted-text role="meth"}. The *timeout* argument has no practical implications if the *block* argument is set to `False` and is thus ignored. Returns `True` if the lock has been acquired or `False` if the timeout period has elapsed.
:::

::: method
release()

Release a lock. This can be called from any process or thread, not only the process or thread which originally acquired the lock.

Behavior is the same as in `threading.Lock.release`{.interpreted-text role="meth"} except that when invoked on an unlocked lock, a `ValueError`{.interpreted-text role="exc"} is raised.
:::

:::: method
locked()

Return a boolean indicating whether this object is locked right now.

::: versionadded
3.14
:::
::::
:::::::

::::::: RLock()
A recursive lock object: a close analog of `threading.RLock`{.interpreted-text role="class"}. A recursive lock must be released by the process or thread that acquired it. Once a process or thread has acquired a recursive lock, the same process or thread may acquire it again without blocking; that process or thread must release it once for each time it has been acquired.

Note that `RLock`{.interpreted-text role="class"} is actually a factory function which returns an instance of `multiprocessing.synchronize.RLock` initialized with a default context.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

`RLock`{.interpreted-text role="class"} supports the `context manager`{.interpreted-text role="term"} protocol and thus may be used in `with`{.interpreted-text role="keyword"} statements.

::: method
acquire(block=True, timeout=None)

Acquire a lock, blocking or non-blocking.

When invoked with the *block* argument set to `True`, block until the lock is in an unlocked state (not owned by any process or thread) unless the lock is already owned by the current process or thread. The current process or thread then takes ownership of the lock (if it does not already have ownership) and the recursion level inside the lock increments by one, resulting in a return value of `True`. Note that there are several differences in this first argument\'s behavior compared to the implementation of `threading.RLock.acquire`{.interpreted-text role="meth"}, starting with the name of the argument itself.

When invoked with the *block* argument set to `False`, do not block. If the lock has already been acquired (and thus is owned) by another process or thread, the current process or thread does not take ownership and the recursion level within the lock is not changed, resulting in a return value of `False`. If the lock is in an unlocked state, the current process or thread takes ownership and the recursion level is incremented, resulting in a return value of `True`.

Use and behaviors of the *timeout* argument are the same as in `Lock.acquire`{.interpreted-text role="meth"}. Note that some of these behaviors of *timeout* differ from the implemented behaviors in `threading.RLock.acquire`{.interpreted-text role="meth"}.
:::

::: method
release()

Release a lock, decrementing the recursion level. If after the decrement the recursion level is zero, reset the lock to unlocked (not owned by any process or thread) and if any other processes or threads are blocked waiting for the lock to become unlocked, allow exactly one of them to proceed. If after the decrement the recursion level is still nonzero, the lock remains locked and owned by the calling process or thread.

Only call this method when the calling process or thread owns the lock. An `AssertionError`{.interpreted-text role="exc"} is raised if this method is called by a process or thread other than the owner or if the lock is in an unlocked (unowned) state. Note that the type of exception raised in this situation differs from the implemented behavior in `threading.RLock.release`{.interpreted-text role="meth"}.
:::

:::: method
locked()

Return a boolean indicating whether this object is locked right now.

::: versionadded
3.14
:::
::::
:::::::

:::::: Semaphore([value])
A semaphore object: a close analog of `threading.Semaphore`{.interpreted-text role="class"}.

Instantiating this class may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

A solitary difference from its close analog exists: its `acquire` method\'s first argument is named *block*, as is consistent with `Lock.acquire`{.interpreted-text role="meth"}.

::: method
get_value()

Return the current value of semaphore.

Note that this may raise `NotImplementedError`{.interpreted-text role="exc"} on platforms like macOS where `sem_getvalue()` is not implemented.
:::

:::: method
locked()

Return a boolean indicating whether this object is locked right now.

::: versionadded
3.14
:::
::::
::::::

:::: note
::: title
Note
:::

On macOS, `sem_timedwait` is unsupported, so calling `acquire()` with a timeout will emulate that function\'s behavior using a sleeping loop.
::::

:::: note
::: title
Note
:::

Some of this package\'s functionality requires a functioning shared semaphore implementation on the host operating system. Without one, the `multiprocessing.synchronize`{.interpreted-text role="mod"} module will be disabled, and attempts to import it will result in an `ImportError`{.interpreted-text role="exc"}. See `3770`{.interpreted-text role="issue"} for additional information.
::::

### Shared `ctypes`{.interpreted-text role="mod"} Objects

It is possible to create shared objects using shared memory which can be inherited by child processes.

::: function
Value(typecode_or_type, \*args, lock=True)

Return a `ctypes`{.interpreted-text role="mod"} object allocated from shared memory. By default the return value is actually a synchronized wrapper for the object. The object itself can be accessed via the *value* attribute of a `Value`{.interpreted-text role="class"}.

*typecode_or_type* determines the type of the returned object: it is either a ctypes type or a one character typecode of the kind used by the `array`{.interpreted-text role="mod"} module. *\*args* is passed on to the constructor for the type.

If *lock* is `True` (the default) then a new recursive lock object is created to synchronize access to the value. If *lock* is a `Lock`{.interpreted-text role="class"} or `RLock`{.interpreted-text role="class"} object then that will be used to synchronize access to the value. If *lock* is `False` then access to the returned object will not be automatically protected by a lock, so it will not necessarily be \"process-safe\".

Operations like `+=` which involve a read and write are not atomic. So if, for instance, you want to atomically increment a shared value it is insufficient to just do :

    counter.value += 1

Assuming the associated lock is recursive (which it is by default) you can instead do :

    with counter.get_lock():
        counter.value += 1

Note that *lock* is a keyword-only argument.
:::

::: function
Array(typecode_or_type, size_or_initializer, \*, lock=True)

Return a ctypes array allocated from shared memory. By default the return value is actually a synchronized wrapper for the array.

*typecode_or_type* determines the type of the elements of the returned array: it is either a `ctypes type <ctypes-fundamental-data-types>`{.interpreted-text role="ref"} or a one character typecode of the kind used by the `array`{.interpreted-text role="mod"} module with the exception of `'w'`, which is not supported. In addition, the `'c'` typecode is an alias for `ctypes.c_char`{.interpreted-text role="class"}. If *size_or_initializer* is an integer, then it determines the length of the array, and the array will be initially zeroed. Otherwise, *size_or_initializer* is a sequence which is used to initialize the array and whose length determines the length of the array.

If *lock* is `True` (the default) then a new lock object is created to synchronize access to the value. If *lock* is a `Lock`{.interpreted-text role="class"} or `RLock`{.interpreted-text role="class"} object then that will be used to synchronize access to the value. If *lock* is `False` then access to the returned object will not be automatically protected by a lock, so it will not necessarily be \"process-safe\".

Note that *lock* is a keyword only argument.

Note that an array of `ctypes.c_char`{.interpreted-text role="data"} has *value* and *raw* attributes which allow one to use it to store and retrieve strings.
:::

#### The `!multiprocessing.sharedctypes`{.interpreted-text role="mod"} module

::: {.module synopsis="Allocate ctypes objects from shared memory."}
multiprocessing.sharedctypes
:::

The `!multiprocessing.sharedctypes`{.interpreted-text role="mod"} module provides functions for allocating `ctypes`{.interpreted-text role="mod"} objects from shared memory which can be inherited by child processes.

:::: note
::: title
Note
:::

Although it is possible to store a pointer in shared memory remember that this will refer to a location in the address space of a specific process. However, the pointer is quite likely to be invalid in the context of a second process and trying to dereference the pointer from the second process may cause a crash.
::::

::: function
RawArray(typecode_or_type, size_or_initializer)

Return a ctypes array allocated from shared memory.

*typecode_or_type* determines the type of the elements of the returned array: it is either a ctypes type or a one character typecode of the kind used by the `array`{.interpreted-text role="mod"} module. If *size_or_initializer* is an integer then it determines the length of the array, and the array will be initially zeroed. Otherwise *size_or_initializer* is a sequence which is used to initialize the array and whose length determines the length of the array.

Note that setting and getting an element is potentially non-atomic \-- use `Array`{.interpreted-text role="func"} instead to make sure that access is automatically synchronized using a lock.
:::

::: function
RawValue(typecode_or_type, \*args)

Return a ctypes object allocated from shared memory.

*typecode_or_type* determines the type of the returned object: it is either a ctypes type or a one character typecode of the kind used by the `array`{.interpreted-text role="mod"} module. *\*args* is passed on to the constructor for the type.

Note that setting and getting the value is potentially non-atomic \-- use `Value`{.interpreted-text role="func"} instead to make sure that access is automatically synchronized using a lock.

Note that an array of `ctypes.c_char`{.interpreted-text role="data"} has `value` and `raw` attributes which allow one to use it to store and retrieve strings \-- see documentation for `ctypes`{.interpreted-text role="mod"}.
:::

::: function
Array(typecode_or_type, size_or_initializer, \*, lock=True, ctx=None)

The same as `RawArray`{.interpreted-text role="func"} except that depending on the value of *lock* a process-safe synchronization wrapper may be returned instead of a raw ctypes array.

If *lock* is `True` (the default) then a new lock object is created to synchronize access to the value. If *lock* is a `~multiprocessing.Lock`{.interpreted-text role="class"} or `~multiprocessing.RLock`{.interpreted-text role="class"} object then that will be used to synchronize access to the value. If *lock* is `False` then access to the returned object will not be automatically protected by a lock, so it will not necessarily be \"process-safe\".

*ctx* is a context object, or `None` (use the current context). If `None`, calling this may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

Note that *lock* and *ctx* are keyword-only parameters.
:::

::: function
Value(typecode_or_type, \*args, lock=True, ctx=None)

The same as `RawValue`{.interpreted-text role="func"} except that depending on the value of *lock* a process-safe synchronization wrapper may be returned instead of a raw ctypes object.

If *lock* is `True` (the default) then a new lock object is created to synchronize access to the value. If *lock* is a `~multiprocessing.Lock`{.interpreted-text role="class"} or `~multiprocessing.RLock`{.interpreted-text role="class"} object then that will be used to synchronize access to the value. If *lock* is `False` then access to the returned object will not be automatically protected by a lock, so it will not necessarily be \"process-safe\".

*ctx* is a context object, or `None` (use the current context). If `None`, calling this may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

Note that *lock* and *ctx* are keyword-only parameters.
:::

::: function
copy(obj)

Return a ctypes object allocated from shared memory which is a copy of the ctypes object *obj*.
:::

:::: function
synchronized(obj, lock=None, ctx=None)

Return a process-safe wrapper object for a ctypes object which uses *lock* to synchronize access. If *lock* is `None` (the default) then a `multiprocessing.RLock`{.interpreted-text role="class"} object is created automatically.

*ctx* is a context object, or `None` (use the current context). If `None`, calling this may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

A synchronized wrapper will have two methods in addition to those of the object it wraps: `get_obj`{.interpreted-text role="meth"} returns the wrapped object and `get_lock`{.interpreted-text role="meth"} returns the lock object used for synchronization.

Note that accessing the ctypes object through the wrapper can be a lot slower than accessing the raw ctypes object.

::: versionchanged
3.5 Synchronized objects support the `context manager`{.interpreted-text role="term"} protocol.
:::
::::

The table below compares the syntax for creating shared ctypes objects from shared memory with the normal ctypes syntax. (In the table `MyStruct` is some subclass of `ctypes.Structure`{.interpreted-text role="class"}.)

  ctypes                  sharedctypes using type      sharedctypes using typecode
  ----------------------- ---------------------------- -----------------------------
  c_double(2.4)           RawValue(c_double, 2.4)      RawValue(\'d\', 2.4)
  MyStruct(4, 6)          RawValue(MyStruct, 4, 6)     
  (c_short \* 7)()        RawArray(c_short, 7)         RawArray(\'h\', 7)
  (c_int \* 3)(9, 2, 8)   RawArray(c_int, (9, 2, 8))   RawArray(\'i\', (9, 2, 8))

Below is an example where a number of ctypes objects are modified by a child process:

    from multiprocessing import Process, Lock
    from multiprocessing.sharedctypes import Value, Array
    from ctypes import Structure, c_double

    class Point(Structure):
        _fields_ = [('x', c_double), ('y', c_double)]

    def modify(n, x, s, A):
        n.value **= 2
        x.value **= 2
        s.value = s.value.upper()
        for a in A:
            a.x **= 2
            a.y **= 2

    if __name__ == '__main__':
        lock = Lock()

        n = Value('i', 7)
        x = Value(c_double, 1.0/3.0, lock=False)
        s = Array('c', b'hello world', lock=lock)
        A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)

        p = Process(target=modify, args=(n, x, s, A))
        p.start()
        p.join()

        print(n.value)
        print(x.value)
        print(s.value)
        print([(a.x, a.y) for a in A])

The results printed are :

``` none
49
0.1111111111111111
HELLO WORLD
[(3.515625, 39.0625), (33.0625, 4.0), (5.640625, 90.25)]
```

### Managers {#multiprocessing-managers}

Managers provide a way to create data which can be shared between different processes, including sharing over a network between processes running on different machines. A manager object controls a server process which manages *shared objects*. Other processes can access the shared objects by using proxies.

::: {.function module=""}
multiprocessing.Manager()

Returns a started `~multiprocessing.managers.SyncManager`{.interpreted-text role="class"} object which can be used for sharing objects between processes. The returned manager object corresponds to a spawned child process and has methods which will create shared objects and return corresponding proxies.
:::

::: {.module synopsis="Share data between process with shared objects."}
multiprocessing.managers
:::

Manager processes will be shutdown as soon as they are garbage collected or their parent process exits. The manager classes are defined in the `multiprocessing.managers`{.interpreted-text role="mod"} module:

::::::::::: {.BaseManager(address=None, .authkey=None, .serializer='pickle', .ctx=None, .*, .shutdown_timeout=1.0)}
Create a BaseManager object.

Once created one should call `start`{.interpreted-text role="meth"} or `get_server().serve_forever()` to ensure that the manager object refers to a started manager process.

*address* is the address on which the manager process listens for new connections. If *address* is `None` then an arbitrary one is chosen.

*authkey* is the authentication key which will be used to check the validity of incoming connections to the server process. If *authkey* is `None` then `current_process().authkey` is used. Otherwise *authkey* is used and it must be a byte string.

*serializer* must be `'pickle'` (use `pickle`{.interpreted-text role="mod"} serialization) or `'xmlrpclib'` (use `xmlrpc.client`{.interpreted-text role="mod"} serialization).

*ctx* is a context object, or `None` (use the current context). If `None`, calling this may set the global start method. See `global-start-method`{.interpreted-text role="ref"} for more details.

*shutdown_timeout* is a timeout in seconds used to wait until the process used by the manager completes in the `shutdown`{.interpreted-text role="meth"} method. If the shutdown times out, the process is terminated. If terminating the process also times out, the process is killed.

::: versionchanged
3.11 Added the *shutdown_timeout* parameter.
:::

::: method
start(\[initializer\[, initargs\]\])

Start a subprocess to start the manager. If *initializer* is not `None` then the subprocess will call `initializer(*initargs)` when it starts.
:::

::: method
get_server()

Returns a `Server`{.interpreted-text role="class"} object which represents the actual server under the control of the Manager. The `Server`{.interpreted-text role="class"} object supports the `serve_forever`{.interpreted-text role="meth"} method:

``` python3
>>> from multiprocessing.managers import BaseManager
>>> manager = BaseManager(address=('', 50000), authkey=b'abc')
>>> server = manager.get_server()
>>> server.serve_forever()
```

`Server`{.interpreted-text role="class"} additionally has an `address`{.interpreted-text role="attr"} attribute.
:::

::: method
connect()

Connect a local manager object to a remote manager process:

``` python3
>>> from multiprocessing.managers import BaseManager
>>> m = BaseManager(address=('127.0.0.1', 50000), authkey=b'abc')
>>> m.connect()
```
:::

::: method
shutdown()

Stop the process used by the manager. This is only available if `start`{.interpreted-text role="meth"} has been used to start the server process.

This can be called multiple times.
:::

::: method
register(typeid\[, callable\[, proxytype\[, exposed\[, method_to_typeid\[, create_method\]\]\]\]\])

A classmethod which can be used for registering a type or callable with the manager class.

*typeid* is a \"type identifier\" which is used to identify a particular type of shared object. This must be a string.

*callable* is a callable used for creating objects for this type identifier. If a manager instance will be connected to the server using the `connect`{.interpreted-text role="meth"} method, or if the *create_method* argument is `False` then this can be left as `None`.

*proxytype* is a subclass of `BaseProxy`{.interpreted-text role="class"} which is used to create proxies for shared objects with this *typeid*. If `None` then a proxy class is created automatically.

*exposed* is used to specify a sequence of method names which proxies for this typeid should be allowed to access using `BaseProxy._callmethod`{.interpreted-text role="meth"}. (If *exposed* is `None` then `proxytype._exposed_`{.interpreted-text role="attr"} is used instead if it exists.) In the case where no exposed list is specified, all \"public methods\" of the shared object will be accessible. (Here a \"public method\" means any attribute which has a `~object.__call__`{.interpreted-text role="meth"} method and whose name does not begin with `'_'`.)

*method_to_typeid* is a mapping used to specify the return type of those exposed methods which should return a proxy. It maps method names to typeid strings. (If *method_to_typeid* is `None` then `proxytype._method_to_typeid_`{.interpreted-text role="attr"} is used instead if it exists.) If a method\'s name is not a key of this mapping or if the mapping is `None` then the object returned by the method will be copied by value.

*create_method* determines whether a method should be created with name *typeid* which can be used to tell the server process to create a new shared object and return a proxy for it. By default it is `True`.
:::

`BaseManager`{.interpreted-text role="class"} instances also have one read-only property:

::: attribute
address

The address used by the manager.
:::

::: versionchanged
3.3 Manager objects support the context management protocol \-- see `typecontextmanager`{.interpreted-text role="ref"}. `~contextmanager.__enter__`{.interpreted-text role="meth"} starts the server process (if it has not already started) and then returns the manager object. `~contextmanager.__exit__`{.interpreted-text role="meth"} calls `shutdown`{.interpreted-text role="meth"}.

In previous versions `~contextmanager.__enter__`{.interpreted-text role="meth"} did not start the manager\'s server process if it was not already started.
:::
:::::::::::

::::::::::::::::::::: SyncManager
A subclass of `BaseManager`{.interpreted-text role="class"} which can be used for the synchronization of processes. Objects of this type are returned by `multiprocessing.Manager`{.interpreted-text role="func"}.

Its methods create and return `multiprocessing-proxy_objects`{.interpreted-text role="ref"} for a number of commonly used data types to be synchronized across processes. This notably includes shared lists and dictionaries.

:::: method
Barrier(parties\[, action\[, timeout\]\])

Create a shared `threading.Barrier`{.interpreted-text role="class"} object and return a proxy for it.

::: versionadded
3.3
:::
::::

::: method
BoundedSemaphore(\[value\])

Create a shared `threading.BoundedSemaphore`{.interpreted-text role="class"} object and return a proxy for it.
:::

:::: method
Condition(\[lock\])

Create a shared `threading.Condition`{.interpreted-text role="class"} object and return a proxy for it.

If *lock* is supplied then it should be a proxy for a `threading.Lock`{.interpreted-text role="class"} or `threading.RLock`{.interpreted-text role="class"} object.

::: versionchanged
3.3 The `~threading.Condition.wait_for`{.interpreted-text role="meth"} method was added.
:::
::::

::: method
Event()

Create a shared `threading.Event`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
Lock()

Create a shared `threading.Lock`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
Namespace()

Create a shared `Namespace`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
Queue(\[maxsize\])

Create a shared `queue.Queue`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
RLock()

Create a shared `threading.RLock`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
Semaphore(\[value\])

Create a shared `threading.Semaphore`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
Array(typecode, sequence)

Create an array and return a proxy for it.
:::

::: method
Value(typecode, value)

Create an object with a writable `value` attribute and return a proxy for it.
:::

::: method
dict() dict(mapping) dict(sequence)

Create a shared `dict`{.interpreted-text role="class"} object and return a proxy for it.
:::

::: method
list() list(sequence)

Create a shared `list`{.interpreted-text role="class"} object and return a proxy for it.
:::

:::: method
set() set(sequence) set(mapping)

Create a shared `set`{.interpreted-text role="class"} object and return a proxy for it.

::: versionadded
3.14 `set`{.interpreted-text role="class"} support was added.
:::
::::

::: versionchanged
3.6 Shared objects are capable of being nested. For example, a shared container object such as a shared list can contain other shared objects which will all be managed and synchronized by the `SyncManager`{.interpreted-text role="class"}.
:::
:::::::::::::::::::::

:::: Namespace
A type that can register with `SyncManager`{.interpreted-text role="class"}.

A namespace object has no public methods, but does have writable attributes. Its representation shows the values of its attributes.

However, when using a proxy for a namespace object, an attribute beginning with `'_'` will be an attribute of the proxy and not an attribute of the referent:

::: doctest
\>\>\> mp_context = multiprocessing.get_context(\'spawn\') \>\>\> manager = mp_context.Manager() \>\>\> Global = manager.Namespace() \>\>\> Global.x = 10 \>\>\> Global.y = \'hello\' \>\>\> Global.\_z = 12.3 \# this is an attribute of the proxy \>\>\> print(Global) Namespace(x=10, y=\'hello\')
:::
::::

#### Customized managers

To create one\'s own manager, one creates a subclass of `BaseManager`{.interpreted-text role="class"} and uses the `~BaseManager.register`{.interpreted-text role="meth"} classmethod to register new types or callables with the manager class. For example:

``` python3
from multiprocessing.managers import BaseManager

class MathsClass:
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)

if __name__ == '__main__':
    with MyManager() as manager:
        maths = manager.Maths()
        print(maths.add(4, 3))         # prints 7
        print(maths.mul(7, 8))         # prints 56
```

#### Using a remote manager

It is possible to run a manager server on one machine and have clients use it from other machines (assuming that the firewalls involved allow it).

Running the following commands creates a server for a single shared queue which remote clients can access:

``` python3
>>> from multiprocessing.managers import BaseManager
>>> from queue import Queue
>>> queue = Queue()
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue', callable=lambda:queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()
```

One client can access the server as follows:

``` python3
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.put('hello')
```

Another client can also use it:

``` python3
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.get()
'hello'
```

Local processes can also access that queue, using the code from above on the client to access it remotely:

``` python3
>>> from multiprocessing import Process, Queue
>>> from multiprocessing.managers import BaseManager
>>> class Worker(Process):
...     def __init__(self, q):
...         self.q = q
...         super().__init__()
...     def run(self):
...         self.q.put('local hello')
...
>>> queue = Queue()
>>> w = Worker(queue)
>>> w.start()
>>> class QueueManager(BaseManager): pass
...
>>> QueueManager.register('get_queue', callable=lambda: queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()
```

### Proxy Objects {#multiprocessing-proxy_objects}

A proxy is an object which *refers* to a shared object which lives (presumably) in a different process. The shared object is said to be the *referent* of the proxy. Multiple proxy objects may have the same referent.

A proxy object has methods which invoke corresponding methods of its referent (although not every method of the referent will necessarily be available through the proxy). In this way, a proxy can be used just like its referent can:

::: doctest
\>\>\> mp_context = multiprocessing.get_context(\'spawn\') \>\>\> manager = mp_context.Manager() \>\>\> l = manager.list(\[i\*i for i in range(10)\]) \>\>\> print(l) \[0, 1, 4, 9, 16, 25, 36, 49, 64, 81\] \>\>\> print(repr(l)) \<ListProxy object, typeid \'list\' at 0x\...\> \>\>\> l\[4\] 16 \>\>\> l\[2:5\] \[4, 9, 16\]
:::

Notice that applying `str`{.interpreted-text role="func"} to a proxy will return the representation of the referent, whereas applying `repr`{.interpreted-text role="func"} will return the representation of the proxy.

An important feature of proxy objects is that they are picklable so they can be passed between processes. As such, a referent can contain `multiprocessing-proxy_objects`{.interpreted-text role="ref"}. This permits nesting of these managed lists, dicts, and other `multiprocessing-proxy_objects`{.interpreted-text role="ref"}:

::: doctest
\>\>\> a = manager.list() \>\>\> b = manager.list() \>\>\> a.append(b) \# referent of a now contains referent of b \>\>\> print(a, b) \[\<ListProxy object, typeid \'list\' at \...\>\] \[\] \>\>\> b.append(\'hello\') \>\>\> print(a\[0\], b) \[\'hello\'\] \[\'hello\'\]
:::

Similarly, dict and list proxies may be nested inside one another:

``` python3
>>> l_outer = manager.list([ manager.dict() for i in range(2) ])
>>> d_first_inner = l_outer[0]
>>> d_first_inner['a'] = 1
>>> d_first_inner['b'] = 2
>>> l_outer[1]['c'] = 3
>>> l_outer[1]['z'] = 26
>>> print(l_outer[0])
{'a': 1, 'b': 2}
>>> print(l_outer[1])
{'c': 3, 'z': 26}
```

If standard (non-proxy) `list`{.interpreted-text role="class"} or `dict`{.interpreted-text role="class"} objects are contained in a referent, modifications to those mutable values will not be propagated through the manager because the proxy has no way of knowing when the values contained within are modified. However, storing a value in a container proxy (which triggers a `__setitem__` on the proxy object) does propagate through the manager and so to effectively modify such an item, one could re-assign the modified value to the container proxy:

``` python3
# create a list proxy and append a mutable object (a dictionary)
lproxy = manager.list()
lproxy.append({})
# now mutate the dictionary
d = lproxy[0]
d['a'] = 1
d['b'] = 2
# at this point, the changes to d are not yet synced, but by
# updating the dictionary, the proxy is notified of the change
lproxy[0] = d
```

This approach is perhaps less convenient than employing nested `multiprocessing-proxy_objects`{.interpreted-text role="ref"} for most use cases but also demonstrates a level of control over the synchronization.

::::: note
::: title
Note
:::

The proxy types in `!multiprocessing`{.interpreted-text role="mod"} do nothing to support comparisons by value. So, for instance, we have:

::: doctest
\>\>\> manager.list(\[1,2,3\]) == \[1,2,3\] False
:::

One should just use a copy of the referent instead when making comparisons.
:::::

:::::::: BaseProxy
Proxy objects are instances of subclasses of `BaseProxy`{.interpreted-text role="class"}.

:::: method
[callmethod]{#callmethod}(methodname\[, args\[, kwds\]\])

Call and return the result of a method of the proxy\'s referent.

If `proxy` is a proxy whose referent is `obj` then the expression :

``` python3
proxy._callmethod(methodname, args, kwds)
```

will evaluate the expression :

``` python3
getattr(obj, methodname)(*args, **kwds)
```

in the manager\'s process.

The returned value will be a copy of the result of the call or a proxy to a new shared object \-- see documentation for the *method_to_typeid* argument of `BaseManager.register`{.interpreted-text role="meth"}.

If an exception is raised by the call, then is re-raised by `_callmethod`{.interpreted-text role="meth"}. If some other exception is raised in the manager\'s process then this is converted into a `RemoteError`{.interpreted-text role="exc"} exception and is raised by `_callmethod`{.interpreted-text role="meth"}.

Note in particular that an exception will be raised if *methodname* has not been *exposed*.

An example of the usage of `_callmethod`{.interpreted-text role="meth"}:

::: doctest
\>\>\> l = manager.list(range(10)) \>\>\> l.\_callmethod(\'\_\_len\_\_\') 10 \>\>\> l.\_callmethod(\'\_\_getitem\_\_\', (slice(2, 7),)) \# equivalent to l\[2:7\] \[2, 3, 4, 5, 6\] \>\>\> l.\_callmethod(\'\_\_getitem\_\_\', (20,)) \# equivalent to l\[20\] Traceback (most recent call last): \... IndexError: list index out of range
:::
::::

::: method
[getvalue]{#getvalue}()

Return a copy of the referent.

If the referent is unpicklable then this will raise an exception.
:::

::: method
\_\_repr\_\_

Return a representation of the proxy object.
:::

::: method
\_\_str\_\_

Return the representation of the referent.
:::
::::::::

#### Cleanup

A proxy object uses a weakref callback so that when it gets garbage collected it deregisters itself from the manager which owns its referent.

A shared object gets deleted from the manager process when there are no longer any proxies referring to it.

### Process Pools

::: {.module synopsis="Create pools of processes."}
multiprocessing.pool
:::

One can create a pool of processes which will carry out tasks submitted to it with the `Pool`{.interpreted-text role="class"} class.

:::::::::::::::::::::::: {.Pool([processes[, .initializer[, .initargs[, .maxtasksperchild .[, .context]]]]])}
A process pool object which controls a pool of worker processes to which jobs can be submitted. It supports asynchronous results with timeouts and callbacks and has a parallel map implementation.

*processes* is the number of worker processes to use. If *processes* is `None` then the number returned by `os.process_cpu_count`{.interpreted-text role="func"} is used.

If *initializer* is not `None` then each worker process will call `initializer(*initargs)` when it starts.

*maxtasksperchild* is the number of tasks a worker process can complete before it will exit and be replaced with a fresh worker process, to enable unused resources to be freed. The default *maxtasksperchild* is `None`, which means worker processes will live as long as the pool.

*context* can be used to specify the context used for starting the worker processes. Usually a pool is created using the function `multiprocessing.Pool`{.interpreted-text role="func"} or the `Pool`{.interpreted-text role="meth"} method of a context object. In both cases *context* is set appropriately. If `None`, calling this function will have the side effect of setting the current global start method if it has not been set already. See the `get_context`{.interpreted-text role="func"} function.

Note that the methods of the pool object should only be called by the process which created the pool.

:::: warning
::: title
Warning
:::

`multiprocessing.pool`{.interpreted-text role="class"} objects have internal resources that need to be properly managed (like any other resource) by using the pool as a context manager or by calling `close`{.interpreted-text role="meth"} and `terminate`{.interpreted-text role="meth"} manually. Failure to do this can lead to the process hanging on finalization.

Note that it is **not correct** to rely on the garbage collector to destroy the pool as CPython does not assure that the finalizer of the pool will be called (see `object.__del__`{.interpreted-text role="meth"} for more information).
::::

::: versionchanged
3.2 Added the *maxtasksperchild* parameter.
:::

::: versionchanged
3.4 Added the *context* parameter.
:::

::: versionchanged
3.13 *processes* uses `os.process_cpu_count`{.interpreted-text role="func"} by default, instead of `os.cpu_count`{.interpreted-text role="func"}.
:::

:::: note
::: title
Note
:::

Worker processes within a `Pool`{.interpreted-text role="class"} typically live for the complete duration of the Pool\'s work queue. A frequent pattern found in other systems (such as Apache, mod_wsgi, etc) to free resources held by workers is to allow a worker within a pool to complete only a set amount of work before exiting, being cleaned up and a new process spawned to replace the old one. The *maxtasksperchild* argument to the `Pool`{.interpreted-text role="class"} exposes this ability to the end user.
::::

::: method
apply(func\[, args\[, kwds\]\])

Call *func* with arguments *args* and keyword arguments *kwds*. It blocks until the result is ready. Given this blocks, `apply_async`{.interpreted-text role="meth"} is better suited for performing work in parallel. Additionally, *func* is only executed in one of the workers of the pool.
:::

::: method
apply_async(func\[, args\[, kwds\[, callback\[, error_callback\]\]\]\])

A variant of the `apply`{.interpreted-text role="meth"} method which returns a `~multiprocessing.pool.AsyncResult`{.interpreted-text role="class"} object.

If *callback* is specified then it should be a callable which accepts a single argument. When the result becomes ready *callback* is applied to it, that is unless the call failed, in which case the *error_callback* is applied instead.

If *error_callback* is specified then it should be a callable which accepts a single argument. If the target function fails, then the *error_callback* is called with the exception instance.

Callbacks should complete immediately since otherwise the thread which handles the results will get blocked.
:::

::: method
map(func, iterable\[, chunksize\])

A parallel equivalent of the `map`{.interpreted-text role="func"} built-in function (it supports only one *iterable* argument though, for multiple iterables see `starmap`{.interpreted-text role="meth"}). It blocks until the result is ready.

This method chops the iterable into a number of chunks which it submits to the process pool as separate tasks. The (approximate) size of these chunks can be specified by setting *chunksize* to a positive integer.

Note that it may cause high memory usage for very long iterables. Consider using `imap`{.interpreted-text role="meth"} or `imap_unordered`{.interpreted-text role="meth"} with explicit *chunksize* option for better efficiency.
:::

::: method
map_async(func, iterable\[, chunksize\[, callback\[, error_callback\]\]\])

A variant of the `.map`{.interpreted-text role="meth"} method which returns a `~multiprocessing.pool.AsyncResult`{.interpreted-text role="class"} object.

If *callback* is specified then it should be a callable which accepts a single argument. When the result becomes ready *callback* is applied to it, that is unless the call failed, in which case the *error_callback* is applied instead.

If *error_callback* is specified then it should be a callable which accepts a single argument. If the target function fails, then the *error_callback* is called with the exception instance.

Callbacks should complete immediately since otherwise the thread which handles the results will get blocked.
:::

::: method
imap(func, iterable\[, chunksize\])

A lazier version of `.map`{.interpreted-text role="meth"}.

The *chunksize* argument is the same as the one used by the `.map`{.interpreted-text role="meth"} method. For very long iterables using a large value for *chunksize* can make the job complete **much** faster than using the default value of `1`.

Also if *chunksize* is `1` then the `!next`{.interpreted-text role="meth"} method of the iterator returned by the `imap`{.interpreted-text role="meth"} method has an optional *timeout* parameter: `next(timeout)` will raise `multiprocessing.TimeoutError`{.interpreted-text role="exc"} if the result cannot be returned within *timeout* seconds.
:::

::: method
imap_unordered(func, iterable\[, chunksize\])

The same as `imap`{.interpreted-text role="meth"} except that the ordering of the results from the returned iterator should be considered arbitrary. (Only when there is only one worker process is the order guaranteed to be \"correct\".)
:::

:::: method
starmap(func, iterable\[, chunksize\])

Like `~multiprocessing.pool.Pool.map`{.interpreted-text role="meth"} except that the elements of the *iterable* are expected to be iterables that are unpacked as arguments.

Hence an *iterable* of `[(1,2), (3, 4)]` results in `[func(1,2), func(3,4)]`.

::: versionadded
3.3
:::
::::

:::: method
starmap_async(func, iterable\[, chunksize\[, callback\[, error_callback\]\]\])

A combination of `starmap`{.interpreted-text role="meth"} and `map_async`{.interpreted-text role="meth"} that iterates over *iterable* of iterables and calls *func* with the iterables unpacked. Returns a result object.

::: versionadded
3.3
:::
::::

::: method
close()

Prevents any more tasks from being submitted to the pool. Once all the tasks have been completed the worker processes will exit.
:::

::: method
terminate()

Stops the worker processes immediately without completing outstanding work. When the pool object is garbage collected `terminate`{.interpreted-text role="meth"} will be called immediately.
:::

::: method
join()

Wait for the worker processes to exit. One must call `close`{.interpreted-text role="meth"} or `terminate`{.interpreted-text role="meth"} before using `join`{.interpreted-text role="meth"}.
:::

::: versionchanged
3.3 Pool objects now support the context management protocol \-- see `typecontextmanager`{.interpreted-text role="ref"}. `~contextmanager.__enter__`{.interpreted-text role="meth"} returns the pool object, and `~contextmanager.__exit__`{.interpreted-text role="meth"} calls `terminate`{.interpreted-text role="meth"}.
:::
::::::::::::::::::::::::

:::::::: AsyncResult
The class of the result returned by `Pool.apply_async`{.interpreted-text role="meth"} and `Pool.map_async`{.interpreted-text role="meth"}.

::: method
get(\[timeout\])

Return the result when it arrives. If *timeout* is not `None` and the result does not arrive within *timeout* seconds then `multiprocessing.TimeoutError`{.interpreted-text role="exc"} is raised. If the remote call raised an exception then that exception will be reraised by `get`{.interpreted-text role="meth"}.
:::

::: method
wait(\[timeout\])

Wait until the result is available or until *timeout* seconds pass.
:::

::: method
ready()

Return whether the call has completed.
:::

:::: method
successful()

Return whether the call completed without raising an exception. Will raise `ValueError`{.interpreted-text role="exc"} if the result is not ready.

::: versionchanged
3.7 If the result is not ready, `ValueError`{.interpreted-text role="exc"} is raised instead of `AssertionError`{.interpreted-text role="exc"}.
:::
::::
::::::::

The following example demonstrates the use of a pool:

``` python3
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # start 4 worker processes
        result = pool.apply_async(f, (10,)) # evaluate "f(10)" asynchronously in a single process
        print(result.get(timeout=1))        # prints "100" unless your computer is *very* slow

        print(pool.map(f, range(10)))       # prints "[0, 1, 4,..., 81]"

        it = pool.imap(f, range(10))
        print(next(it))                     # prints "0"
        print(next(it))                     # prints "1"
        print(it.next(timeout=1))           # prints "4" unless your computer is *very* slow

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError
```

### Listeners and Clients {#multiprocessing-listeners-clients}

::: {.module synopsis="API for dealing with sockets."}
multiprocessing.connection
:::

Usually message passing between processes is done using queues or by using `~Connection`{.interpreted-text role="class"} objects returned by `~multiprocessing.Pipe`{.interpreted-text role="func"}.

However, the `!multiprocessing.connection`{.interpreted-text role="mod"} module allows some extra flexibility. It basically gives a high level message oriented API for dealing with sockets or Windows named pipes. It also has support for *digest authentication* using the `hmac`{.interpreted-text role="mod"} module, and for polling multiple connections at the same time.

::: function
deliver_challenge(connection, authkey)

Send a randomly generated message to the other end of the connection and wait for a reply.

If the reply matches the digest of the message using *authkey* as the key then a welcome message is sent to the other end of the connection. Otherwise `~multiprocessing.AuthenticationError`{.interpreted-text role="exc"} is raised.
:::

::: function
answer_challenge(connection, authkey)

Receive a message, calculate the digest of the message using *authkey* as the key, and then send the digest back.

If a welcome message is not received, then `~multiprocessing.AuthenticationError`{.interpreted-text role="exc"} is raised.
:::

::: function
Client(address\[, family\[, authkey\]\])

Attempt to set up a connection to the listener which is using address *address*, returning a `~Connection`{.interpreted-text role="class"}.

The type of the connection is determined by *family* argument, but this can generally be omitted since it can usually be inferred from the format of *address*. (See `multiprocessing-address-formats`{.interpreted-text role="ref"})

If *authkey* is given and not `None`, it should be a byte string and will be used as the secret key for an HMAC-based authentication challenge. No authentication is done if *authkey* is `None`. `~multiprocessing.AuthenticationError`{.interpreted-text role="exc"} is raised if authentication fails. See `multiprocessing-auth-keys`{.interpreted-text role="ref"}.
:::

:::::::::: {.Listener([address[, .family[, .backlog[, .authkey]]]])}
A wrapper for a bound socket or Windows named pipe which is \'listening\' for connections.

*address* is the address to be used by the bound socket or named pipe of the listener object.

:::: note
::: title
Note
:::

If an address of \'0.0.0.0\' is used, the address will not be a connectable end point on Windows. If you require a connectable end-point, you should use \'127.0.0.1\'.
::::

*family* is the type of socket (or named pipe) to use. This can be one of the strings `'AF_INET'` (for a TCP socket), `'AF_UNIX'` (for a Unix domain socket) or `'AF_PIPE'` (for a Windows named pipe). Of these only the first is guaranteed to be available. If *family* is `None` then the family is inferred from the format of *address*. If *address* is also `None` then a default is chosen. This default is the family which is assumed to be the fastest available. See `multiprocessing-address-formats`{.interpreted-text role="ref"}. Note that if *family* is `'AF_UNIX'` and address is `None` then the socket will be created in a private temporary directory created using `tempfile.mkstemp`{.interpreted-text role="func"}.

If the listener object uses a socket then *backlog* (1 by default) is passed to the `~socket.socket.listen`{.interpreted-text role="meth"} method of the socket once it has been bound.

If *authkey* is given and not `None`, it should be a byte string and will be used as the secret key for an HMAC-based authentication challenge. No authentication is done if *authkey* is `None`. `~multiprocessing.AuthenticationError`{.interpreted-text role="exc"} is raised if authentication fails. See `multiprocessing-auth-keys`{.interpreted-text role="ref"}.

::: method
accept()

Accept a connection on the bound socket or named pipe of the listener object and return a `~Connection`{.interpreted-text role="class"} object. If authentication is attempted and fails, then `~multiprocessing.AuthenticationError`{.interpreted-text role="exc"} is raised.
:::

::: method
close()

Close the bound socket or named pipe of the listener object. This is called automatically when the listener is garbage collected. However it is advisable to call it explicitly.
:::

Listener objects have the following read-only properties:

::: attribute
address

The address which is being used by the Listener object.
:::

::: attribute
last_accepted

The address from which the last accepted connection came. If this is unavailable then it is `None`.
:::

::: versionchanged
3.3 Listener objects now support the context management protocol \-- see `typecontextmanager`{.interpreted-text role="ref"}. `~contextmanager.__enter__`{.interpreted-text role="meth"} returns the listener object, and `~contextmanager.__exit__`{.interpreted-text role="meth"} calls `close`{.interpreted-text role="meth"}.
:::
::::::::::

:::: function
wait(object_list, timeout=None)

Wait till an object in *object_list* is ready. Returns the list of those objects in *object_list* which are ready. If *timeout* is a float then the call blocks for at most that many seconds. If *timeout* is `None` then it will block for an unlimited period. A negative timeout is equivalent to a zero timeout.

For both POSIX and Windows, an object can appear in *object_list* if it is

- a readable `~multiprocessing.connection.Connection`{.interpreted-text role="class"} object;
- a connected and readable `socket.socket`{.interpreted-text role="class"} object; or
- the `~multiprocessing.Process.sentinel`{.interpreted-text role="attr"} attribute of a `~multiprocessing.Process`{.interpreted-text role="class"} object.

A connection or socket object is ready when there is data available to be read from it, or the other end has been closed.

**POSIX**: `wait(object_list, timeout)` almost equivalent `select.select(object_list, [], [], timeout)`. The difference is that, if `select.select`{.interpreted-text role="func"} is interrupted by a signal, it can raise `OSError`{.interpreted-text role="exc"} with an error number of `EINTR`, whereas `wait`{.interpreted-text role="func"} will not.

**Windows**: An item in *object_list* must either be an integer handle which is waitable (according to the definition used by the documentation of the Win32 function `WaitForMultipleObjects()`) or it can be an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method which returns a socket handle or pipe handle. (Note that pipe handles and socket handles are **not** waitable handles.)

::: versionadded
3.3
:::
::::

**Examples**

The following server code creates a listener which uses `'secret password'` as an authentication key. It then waits for a connection and sends some data to the client:

``` python3
from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'

with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        print('connection accepted from', listener.last_accepted)

        conn.send([2.25, None, 'junk', float])

        conn.send_bytes(b'hello')

        conn.send_bytes(array('i', [42, 1729]))
```

The following code connects to the server and receives some data from the server:

``` python3
from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)

with Client(address, authkey=b'secret password') as conn:
    print(conn.recv())                  # => [2.25, None, 'junk', float]

    print(conn.recv_bytes())            # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr))    # => 8
    print(arr)                          # => array('i', [42, 1729, 0, 0, 0])
```

The following code uses `~multiprocessing.connection.wait`{.interpreted-text role="func"} to wait for messages from multiple processes at once:

``` python3
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait

def foo(w):
    for i in range(10):
        w.send((i, current_process().name))
    w.close()

if __name__ == '__main__':
    readers = []

    for i in range(4):
        r, w = Pipe(duplex=False)
        readers.append(r)
        p = Process(target=foo, args=(w,))
        p.start()
        # We close the writable end of the pipe now to be sure that
        # p is the only process which owns a handle for it.  This
        # ensures that when p closes its handle for the writable end,
        # wait() will promptly report the readable end as being ready.
        w.close()

    while readers:
        for r in wait(readers):
            try:
                msg = r.recv()
            except EOFError:
                readers.remove(r)
            else:
                print(msg)
```

#### Address Formats {#multiprocessing-address-formats}

- An `'AF_INET'` address is a tuple of the form `(hostname, port)` where *hostname* is a string and *port* is an integer.
- An `'AF_UNIX'` address is a string representing a filename on the filesystem.
- An `'AF_PIPE'` address is a string of the form `r'\\\\\\.\\pipe\\\\{PipeName}'`{.interpreted-text role="samp"}. To use `Client`{.interpreted-text role="func"} to connect to a named pipe on a remote computer called *ServerName* one should use an address of the form `r'\\\\\\\\{ServerName}\\pipe\\\\{PipeName}'`{.interpreted-text role="samp"} instead.

Note that any string beginning with two backslashes is assumed by default to be an `'AF_PIPE'` address rather than an `'AF_UNIX'` address.

### Authentication keys {#multiprocessing-auth-keys}

When one uses `Connection.recv <Connection.recv>`{.interpreted-text role="meth"}, the data received is automatically unpickled. Unfortunately unpickling data from an untrusted source is a security risk. Therefore `Listener`{.interpreted-text role="class"} and `Client`{.interpreted-text role="func"} use the `hmac`{.interpreted-text role="mod"} module to provide digest authentication.

An authentication key is a byte string which can be thought of as a password: once a connection is established both ends will demand proof that the other knows the authentication key. (Demonstrating that both ends are using the same key does **not** involve sending the key over the connection.)

If authentication is requested but no authentication key is specified then the return value of `current_process().authkey` is used (see `~multiprocessing.Process`{.interpreted-text role="class"}). This value will be automatically inherited by any `~multiprocessing.Process`{.interpreted-text role="class"} object that the current process creates. This means that (by default) all processes of a multi-process program will share a single authentication key which can be used when setting up connections between themselves.

Suitable authentication keys can also be generated by using `os.urandom`{.interpreted-text role="func"}.

### Logging

Some support for logging is available. Note, however, that the `logging`{.interpreted-text role="mod"} package does not use process shared locks so it is possible (depending on the handler type) for messages from different processes to get mixed up.

::: currentmodule
multiprocessing
:::

::: function
get_logger()

Returns the logger used by `!multiprocessing`{.interpreted-text role="mod"}. If necessary, a new one will be created.

When first created the logger has level `logging.NOTSET`{.interpreted-text role="const"} and no default handler. Messages sent to this logger will not by default propagate to the root logger.

Note that on Windows child processes will only inherit the level of the parent process\'s logger \-- any other customization of the logger will not be inherited.
:::

::: currentmodule
multiprocessing
:::

::: function
log_to_stderr(level=None)

This function performs a call to `get_logger`{.interpreted-text role="func"} but in addition to returning the logger created by get_logger, it adds a handler which sends output to `sys.stderr`{.interpreted-text role="data"} using format `'[%(levelname)s/%(processName)s] %(message)s'`. You can modify `levelname` of the logger by passing a `level` argument.
:::

Below is an example session with logging turned on:

``` python3
>>> import multiprocessing, logging
>>> logger = multiprocessing.log_to_stderr()
>>> logger.setLevel(logging.INFO)
>>> logger.warning('doomed')
[WARNING/MainProcess] doomed
>>> m = multiprocessing.Manager()
[INFO/SyncManager-...] child process calling self.run()
[INFO/SyncManager-...] created temp directory /.../pymp-...
[INFO/SyncManager-...] manager serving at '/.../listener-...'
>>> del m
[INFO/MainProcess] sending shutdown message to manager
[INFO/SyncManager-...] manager exiting with exitcode 0
```

For a full table of logging levels, see the `logging`{.interpreted-text role="mod"} module.

### The `!multiprocessing.dummy`{.interpreted-text role="mod"} module

::: {.module synopsis="Dumb wrapper around threading."}
multiprocessing.dummy
:::

`!multiprocessing.dummy`{.interpreted-text role="mod"} replicates the API of `!multiprocessing`{.interpreted-text role="mod"} but is no more than a wrapper around the `threading`{.interpreted-text role="mod"} module.

::: currentmodule
multiprocessing.pool
:::

In particular, the `Pool` function provided by `!multiprocessing.dummy`{.interpreted-text role="mod"} returns an instance of `ThreadPool`{.interpreted-text role="class"}, which is a subclass of `Pool`{.interpreted-text role="class"} that supports all the same method calls but uses a pool of worker threads rather than worker processes.

::::: {.ThreadPool([processes[, .initializer[, .initargs]]])}
A thread pool object which controls a pool of worker threads to which jobs can be submitted. `ThreadPool`{.interpreted-text role="class"} instances are fully interface compatible with `Pool`{.interpreted-text role="class"} instances, and their resources must also be properly managed, either by using the pool as a context manager or by calling `~multiprocessing.pool.Pool.close`{.interpreted-text role="meth"} and `~multiprocessing.pool.Pool.terminate`{.interpreted-text role="meth"} manually.

*processes* is the number of worker threads to use. If *processes* is `None` then the number returned by `os.process_cpu_count`{.interpreted-text role="func"} is used.

If *initializer* is not `None` then each worker process will call `initializer(*initargs)` when it starts.

Unlike `Pool`{.interpreted-text role="class"}, *maxtasksperchild* and *context* cannot be provided.

:::: note
::: title
Note
:::

A `ThreadPool`{.interpreted-text role="class"} shares the same interface as `Pool`{.interpreted-text role="class"}, which is designed around a pool of processes and predates the introduction of the `concurrent.futures`{.interpreted-text role="class"} module. As such, it inherits some operations that don\'t make sense for a pool backed by threads, and it has its own type for representing the status of asynchronous jobs, `AsyncResult`{.interpreted-text role="class"}, that is not understood by any other libraries.

Users should generally prefer to use `concurrent.futures.ThreadPoolExecutor`{.interpreted-text role="class"}, which has a simpler interface that was designed around threads from the start, and which returns `concurrent.futures.Future`{.interpreted-text role="class"} instances that are compatible with many other libraries, including `asyncio`{.interpreted-text role="mod"}.
::::
:::::

## Programming guidelines {#multiprocessing-programming}

There are certain guidelines and idioms which should be adhered to when using `!multiprocessing`{.interpreted-text role="mod"}.

### All start methods

The following applies to all start methods.

Avoid shared state

> As far as possible one should try to avoid shifting large amounts of data between processes.
>
> It is probably best to stick to using queues or pipes for communication between processes rather than using the lower level synchronization primitives.

Picklability

> Ensure that the arguments to the methods of proxies are picklable.

Thread safety of proxies

> Do not use a proxy object from more than one thread unless you protect it with a lock.
>
> (There is never a problem with different processes using the *same* proxy.)

Joining zombie processes

> On POSIX when a process finishes but has not been joined it becomes a zombie. There should never be very many because each time a new process starts (or `~multiprocessing.active_children`{.interpreted-text role="func"} is called) all completed processes which have not yet been joined will be joined. Also calling a finished process\'s `Process.is_alive <multiprocessing.Process.is_alive>`{.interpreted-text role="meth"} will join the process. Even so it is probably good practice to explicitly join all the processes that you start.

Better to inherit than pickle/unpickle

> When using the *spawn* or *forkserver* start methods many types from `!multiprocessing`{.interpreted-text role="mod"} need to be picklable so that child processes can use them. However, one should generally avoid sending shared objects to other processes using pipes or queues. Instead you should arrange the program so that a process which needs access to a shared resource created elsewhere can inherit it from an ancestor process.

Avoid terminating processes

> Using the `Process.terminate <multiprocessing.Process.terminate>`{.interpreted-text role="meth"} method to stop a process is liable to cause any shared resources (such as locks, semaphores, pipes and queues) currently being used by the process to become broken or unavailable to other processes.
>
> Therefore it is probably best to only consider using `Process.terminate <multiprocessing.Process.terminate>`{.interpreted-text role="meth"} on processes which never use any shared resources.

Joining processes that use queues

> Bear in mind that a process that has put items in a queue will wait before terminating until all the buffered items are fed by the \"feeder\" thread to the underlying pipe. (The child process can call the `Queue.cancel_join_thread <multiprocessing.Queue.cancel_join_thread>`{.interpreted-text role="meth"} method of the queue to avoid this behaviour.)
>
> This means that whenever you use a queue you need to make sure that all items which have been put on the queue will eventually be removed before the process is joined. Otherwise you cannot be sure that processes which have put items on the queue will terminate. Remember also that non-daemonic processes will be joined automatically.
>
> An example which will deadlock is the following:
>
> ``` python3
> from multiprocessing import Process, Queue
>
> def f(q):
>     q.put('X' * 1000000)
>
> if __name__ == '__main__':
>     queue = Queue()
>     p = Process(target=f, args=(queue,))
>     p.start()
>     p.join()                    # this deadlocks
>     obj = queue.get()
> ```
>
> A fix here would be to swap the last two lines (or simply remove the `p.join()` line).

Explicitly pass resources to child processes

> On POSIX using the *fork* start method, a child process can make use of a shared resource created in a parent process using a global resource. However, it is better to pass the object as an argument to the constructor for the child process.
>
> Apart from making the code (potentially) compatible with Windows and the other start methods this also ensures that as long as the child process is still alive the object will not be garbage collected in the parent process. This might be important if some resource is freed when the object is garbage collected in the parent process.
>
> So for instance :
>
> ``` python3
> from multiprocessing import Process, Lock
>
> def f():
>     ... do something using "lock" ...
>
> if __name__ == '__main__':
>     lock = Lock()
>     for i in range(10):
>         Process(target=f).start()
> ```
>
> should be rewritten as :
>
> ``` python3
> from multiprocessing import Process, Lock
>
> def f(l):
>     ... do something using "l" ...
>
> if __name__ == '__main__':
>     lock = Lock()
>     for i in range(10):
>         Process(target=f, args=(lock,)).start()
> ```

Beware of replacing `sys.stdin`{.interpreted-text role="data"} with a \"file like object\"

> `!multiprocessing`{.interpreted-text role="mod"} originally unconditionally called:
>
> ``` python3
> os.close(sys.stdin.fileno())
> ```
>
> in the `multiprocessing.Process._bootstrap`{.interpreted-text role="meth"} method \-\-- this resulted in issues with processes-in-processes. This has been changed to:
>
> ``` python3
> sys.stdin.close()
> sys.stdin = open(os.open(os.devnull, os.O_RDONLY), closefd=False)
> ```
>
> Which solves the fundamental issue of processes colliding with each other resulting in a bad file descriptor error, but introduces a potential danger to applications which replace `sys.stdin`{.interpreted-text role="func"} with a \"file-like object\" with output buffering. This danger is that if multiple processes call `~io.IOBase.close`{.interpreted-text role="meth"} on this file-like object, it could result in the same data being flushed to the object multiple times, resulting in corruption.
>
> If you write a file-like object and implement your own caching, you can make it fork-safe by storing the pid whenever you append to the cache, and discarding the cache when the pid changes. For example:
>
> ``` python3
> @property
> def cache(self):
>     pid = os.getpid()
>     if pid != self._pid:
>         self._pid = pid
>         self._cache = []
>     return self._cache
> ```
>
> For more information, see `5155`{.interpreted-text role="issue"}, `5313`{.interpreted-text role="issue"} and `5331`{.interpreted-text role="issue"}

### The *spawn* and *forkserver* start methods[]{#multiprocessing-programming-spawn} {#multiprocessing-programming-forkserver}

There are a few extra restrictions which don\'t apply to the *fork* start method.

More picklability

> Ensure that all arguments to `~multiprocessing.Process`{.interpreted-text role="class"} are picklable. Also, if you subclass `Process.__init__`, you must make sure that instances will be picklable when the `Process.start <multiprocessing.Process.start>`{.interpreted-text role="meth"} method is called.

Global variables

> Bear in mind that if code run in a child process tries to access a global variable, then the value it sees (if any) may not be the same as the value in the parent process at the time that `Process.start
> <multiprocessing.Process.start>`{.interpreted-text role="meth"} was called.
>
> However, global variables which are just module level constants cause no problems.

::: {#multiprocessing-safe-main-import}
Safe importing of main module
:::

> Make sure that the main module can be safely imported by a new Python interpreter without causing unintended side effects (such as starting a new process).
>
> For example, using the *spawn* or *forkserver* start method running the following module would fail with a `RuntimeError`{.interpreted-text role="exc"}:
>
> ``` python3
> from multiprocessing import Process
>
> def foo():
>     print('hello')
>
> p = Process(target=foo)
> p.start()
> ```
>
> Instead one should protect the \"entry point\" of the program by using `if __name__ == '__main__':` as follows:
>
> ``` python3
> from multiprocessing import Process, freeze_support, set_start_method
>
> def foo():
>     print('hello')
>
> if __name__ == '__main__':
>     freeze_support()
>     set_start_method('spawn')
>     p = Process(target=foo)
>     p.start()
> ```
>
> (The `freeze_support()` line can be omitted if the program will be run normally instead of frozen.)
>
> This allows the newly spawned Python interpreter to safely import the module and then run the module\'s `foo()` function.
>
> Similar restrictions apply if a pool or manager is created in the main module.

## Examples {#multiprocessing-examples}

Demonstration of how to create and use customized managers and proxies:

::: {.literalinclude language="python3"}
../includes/mp_newtype.py
:::

Using `~multiprocessing.pool.Pool`{.interpreted-text role="class"}:

::: {.literalinclude language="python3"}
../includes/mp_pool.py
:::

An example showing how to use queues to feed tasks to a collection of worker processes and collect the results:

::: literalinclude
../includes/mp_workers.py
:::
