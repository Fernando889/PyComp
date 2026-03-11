# `!select`{.interpreted-text role="mod"} \-\-- Waiting for I/O completion

::: {.module synopsis="Wait for I/O completion on multiple streams."}
select
:::

------------------------------------------------------------------------

This module provides access to the `!select`{.interpreted-text role="c:func"} and `!poll`{.interpreted-text role="c:func"} functions available in most operating systems, `!devpoll`{.interpreted-text role="c:func"} available on Solaris and derivatives, `!epoll`{.interpreted-text role="c:func"} available on Linux 2.5+ and `!kqueue`{.interpreted-text role="c:func"} available on most BSD. Note that on Windows, it only works for sockets; on other operating systems, it also works for other file types (in particular, on Unix, it works on pipes). It cannot be used on regular files to determine whether a file has grown since it was last read.

:::: note
::: title
Note
:::

The `selectors`{.interpreted-text role="mod"} module allows high-level and efficient I/O multiplexing, built upon the `!select`{.interpreted-text role="mod"} module primitives. Users are encouraged to use the `selectors`{.interpreted-text role="mod"} module instead, unless they want precise control over the OS-level primitives used.
::::

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

The module defines the following:

:::: exception
error

A deprecated alias of `OSError`{.interpreted-text role="exc"}.

::: versionchanged
3.3 Following `3151`{.interpreted-text role="pep"}, this class was made an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

::::: function
devpoll()

(Only supported on Solaris and derivatives.) Returns a `/dev/poll` polling object; see section `devpoll-objects`{.interpreted-text role="ref"} below for the methods supported by devpoll objects.

`!devpoll`{.interpreted-text role="c:func"} objects are linked to the number of file descriptors allowed at the time of instantiation. If your program reduces this value, `!devpoll`{.interpreted-text role="c:func"} will fail. If your program increases this value, `!devpoll`{.interpreted-text role="c:func"} may return an incomplete list of active file descriptors.

The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionadded
3.3
:::

::: versionchanged
3.4 The new file descriptor is now non-inheritable.
:::
:::::

:::::: function
epoll(sizehint=-1, flags=0)

(Only supported on Linux 2.5.44 and newer.) Return an edge polling object, which can be used as Edge or Level Triggered interface for I/O events.

*sizehint* informs epoll about the expected number of events to be registered. It must be positive, or `-1` to use the default. It is only used on older systems where `!epoll_create1`{.interpreted-text role="c:func"} is not available; otherwise it has no effect (though its value is still checked).

*flags* is deprecated and completely ignored. However, when supplied, its value must be `0` or `select.EPOLL_CLOEXEC`, otherwise `OSError` is raised.

See the `epoll-objects`{.interpreted-text role="ref"} section below for the methods supported by epolling objects.

`epoll` objects support the context management protocol: when used in a `with`{.interpreted-text role="keyword"} statement, the new file descriptor is automatically closed at the end of the block.

The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.3 Added the *flags* parameter.
:::

::: versionchanged
3.4 Support for the `with`{.interpreted-text role="keyword"} statement was added. The new file descriptor is now non-inheritable.
:::

::: deprecated
3.4 The *flags* parameter. `select.EPOLL_CLOEXEC` is used by default now. Use `os.set_inheritable`{.interpreted-text role="func"} to make the file descriptor inheritable.
:::
::::::

::: function
poll()

(Not supported by all operating systems.) Returns a polling object, which supports registering and unregistering file descriptors, and then polling them for I/O events; see section `poll-objects`{.interpreted-text role="ref"} below for the methods supported by polling objects.
:::

:::: function
kqueue()

(Only supported on BSD.) Returns a kernel queue object; see section `kqueue-objects`{.interpreted-text role="ref"} below for the methods supported by kqueue objects.

The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: versionchanged
3.4 The new file descriptor is now non-inheritable.
:::
::::

::: function
kevent(ident, filter=KQ_FILTER_READ, flags=KQ_EV_ADD, fflags=0, data=0, udata=0)

(Only supported on BSD.) Returns a kernel event object; see section `kevent-objects`{.interpreted-text role="ref"} below for the methods supported by kevent objects.
:::

::::::::: function
select(rlist, wlist, xlist, timeout=None)

This is a straightforward interface to the Unix `!select`{.interpreted-text role="c:func"} system call. The first three arguments are iterables of \'waitable objects\': either integers representing file descriptors or objects with a parameterless method named `~io.IOBase.fileno`{.interpreted-text role="meth"} returning such an integer:

- *rlist*: wait until ready for reading
- *wlist*: wait until ready for writing
- *xlist*: wait for an \"exceptional condition\" (see the manual page for what your system considers such a condition)

Empty iterables are allowed, but acceptance of three empty iterables is platform-dependent. (It is known to work on Unix but not on Windows.) The optional *timeout* argument specifies a time-out in seconds; it may be a non-integer to specify fractions of seconds. When the *timeout* argument is omitted or `None`, the function blocks until at least one file descriptor is ready. A time-out value of zero specifies a poll and never blocks.

The return value is a triple of lists of objects that are ready: subsets of the first three arguments. When the time-out is reached without a file descriptor becoming ready, three empty lists are returned.

::: index
single: socket() (in module socket) single: popen() (in module os)
:::

Among the acceptable object types in the iterables are Python `file
objects <file object>`{.interpreted-text role="term"} (e.g. `sys.stdin`, or objects returned by `open`{.interpreted-text role="func"} or `os.popen`{.interpreted-text role="func"}), socket objects returned by `socket.socket`{.interpreted-text role="func"}. You may also define a `wrapper`{.interpreted-text role="dfn"} class yourself, as long as it has an appropriate `~io.IOBase.fileno`{.interpreted-text role="meth"} method (that really returns a file descriptor, not just a random integer).

::::: note
::: title
Note
:::

::: index
single: WinSock
:::

File objects on Windows are not acceptable, but sockets are. On Windows, the underlying `!select`{.interpreted-text role="c:func"} function is provided by the WinSock library, and does not handle file descriptors that don\'t originate from WinSock.
:::::

::: versionchanged
3.5 The function is now retried with a recomputed timeout when interrupted by a signal, except if the signal handler raises an exception (see `475`{.interpreted-text role="pep"} for the rationale), instead of raising `InterruptedError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.15 Accepts any real number as *timeout*, not only integer or float.
:::
:::::::::

::::: data
PIPE_BUF

The minimum number of bytes which can be written without blocking to a pipe when the pipe has been reported as ready for writing by `~select.select`{.interpreted-text role="func"}, `!poll`{.interpreted-text role="func"} or another interface in this module. This doesn\'t apply to other kinds of file-like objects such as sockets.

This value is guaranteed by POSIX to be at least 512.

::: availability
Unix
:::

::: versionadded
3.2
:::
:::::

## `/dev/poll` Polling Objects {#devpoll-objects}

Solaris and derivatives have `/dev/poll`. While `!select`{.interpreted-text role="c:func"} is *O*(*highest file descriptor*) and `!poll`{.interpreted-text role="c:func"} is *O*(*number of file descriptors*), `/dev/poll` is *O*(*active file descriptors*).

`/dev/poll` behaviour is very close to the standard `!poll`{.interpreted-text role="c:func"} object.

:::: method
devpoll.close()

Close the file descriptor of the polling object.

::: versionadded
3.4
:::
::::

:::: attribute
devpoll.closed

`True` if the polling object is closed.

::: versionadded
3.4
:::
::::

:::: method
devpoll.fileno()

Return the file descriptor number of the polling object.

::: versionadded
3.4
:::
::::

::::: method
devpoll.register(fd\[, eventmask\])

Register a file descriptor with the polling object. Future calls to the `poll`{.interpreted-text role="meth"} method will then check whether the file descriptor has any pending I/O events. *fd* can be either an integer, or an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method that returns an integer. File objects implement `!fileno`{.interpreted-text role="meth"}, so they can also be used as the argument.

*eventmask* is an optional bitmask describing the type of events you want to check for. The constants are the same as with `!poll`{.interpreted-text role="c:func"} object. The default value is a combination of the constants `POLLIN`{.interpreted-text role="const"}, `POLLPRI`{.interpreted-text role="const"}, and `POLLOUT`{.interpreted-text role="const"}.

:::: warning
::: title
Warning
:::

Registering a file descriptor that\'s already registered is not an error, but the result is undefined. The appropriate action is to unregister or modify it first. This is an important difference compared with `!poll`{.interpreted-text role="c:func"}.
::::
:::::

::: method
devpoll.modify(fd\[, eventmask\])

This method does an `unregister`{.interpreted-text role="meth"} followed by a `register`{.interpreted-text role="meth"}. It is (a bit) more efficient than doing the same explicitly.
:::

::: method
devpoll.unregister(fd)

Remove a file descriptor being tracked by a polling object. Just like the `register`{.interpreted-text role="meth"} method, *fd* can be an integer or an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method that returns an integer.

Attempting to remove a file descriptor that was never registered is safely ignored.
:::

::::: method
devpoll.poll(\[timeout\])

Polls the set of registered file descriptors, and returns a possibly empty list containing `(fd, event)` 2-tuples for the descriptors that have events or errors to report. *fd* is the file descriptor, and *event* is a bitmask with bits set for the reported events for that descriptor \-\-- `POLLIN`{.interpreted-text role="const"} for waiting input, `POLLOUT`{.interpreted-text role="const"} to indicate that the descriptor can be written to, and so forth. An empty list indicates that the call timed out and no file descriptors had any events to report. If *timeout* is given, it specifies the length of time in milliseconds which the system will wait for events before returning. If *timeout* is omitted, -1, or `None`{.interpreted-text role="const"}, the call will block until there is an event for this poll object.

::: versionchanged
3.5 The function is now retried with a recomputed timeout when interrupted by a signal, except if the signal handler raises an exception (see `475`{.interpreted-text role="pep"} for the rationale), instead of raising `InterruptedError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.15 Accepts any real number as *timeout*, not only integer or float.
:::
:::::

## Edge and Level Trigger Polling (epoll) Objects {#epoll-objects}

> <https://linux.die.net/man/4/epoll>
>
> *eventmask*
>
>   --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>   Constant                                           Meaning
>   -------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------
>   `EPOLLIN`{.interpreted-text role="const"}          Available for read
>
>   `EPOLLOUT`{.interpreted-text role="const"}         Available for write
>
>   `EPOLLPRI`{.interpreted-text role="const"}         Urgent data for read
>
>   `EPOLLERR`{.interpreted-text role="const"}         Error condition happened on the assoc. fd
>
>   `EPOLLHUP`{.interpreted-text role="const"}         Hang up happened on the assoc. fd
>
>   `EPOLLET`{.interpreted-text role="const"}          Set Edge Trigger behavior, the default is Level Trigger behavior
>
>   `EPOLLONESHOT`{.interpreted-text role="const"}     Set one-shot behavior. After one event is pulled out, the fd is internally disabled
>
>   `EPOLLEXCLUSIVE`{.interpreted-text role="const"}   Wake only one epoll object when the associated fd has an event. The default (if this flag is not set) is to wake all epoll objects polling on a fd.
>
>   `EPOLLRDHUP`{.interpreted-text role="const"}       Stream socket peer closed connection or shut down writing half of connection.
>
>   `EPOLLRDNORM`{.interpreted-text role="const"}      Equivalent to `EPOLLIN`{.interpreted-text role="const"}
>
>   `EPOLLRDBAND`{.interpreted-text role="const"}      Priority data band can be read.
>
>   `EPOLLWRNORM`{.interpreted-text role="const"}      Equivalent to `EPOLLOUT`{.interpreted-text role="const"}
>
>   `EPOLLWRBAND`{.interpreted-text role="const"}      Priority data may be written.
>
>   `EPOLLMSG`{.interpreted-text role="const"}         Ignored.
>
>   `EPOLLWAKEUP`{.interpreted-text role="const"}      Prevents sleep during event waiting.
>   --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>
> ::: versionadded
> 3.6 `EPOLLEXCLUSIVE`{.interpreted-text role="const"} was added. It\'s only supported by Linux Kernel 4.5 or later.
> :::
>
> ::: versionadded
> 3.14 `EPOLLWAKEUP`{.interpreted-text role="const"} was added. It\'s only supported by Linux Kernel 3.5 or later.
> :::

::: method
epoll.close()

Close the control file descriptor of the epoll object.
:::

::: attribute
epoll.closed

`True` if the epoll object is closed.
:::

::: method
epoll.fileno()

Return the file descriptor number of the control fd.
:::

::: method
epoll.fromfd(fd)

Create an epoll object from a given file descriptor.
:::

::: method
epoll.register(fd\[, eventmask\])

Register a fd descriptor with the epoll object.
:::

::: method
epoll.modify(fd, eventmask)

Modify a registered file descriptor.
:::

:::: method
epoll.unregister(fd)

Remove a registered file descriptor from the epoll object.

::: versionchanged
3.9 The method no longer ignores the `~errno.EBADF`{.interpreted-text role="data"} error.
:::
::::

::::: method
epoll.poll(timeout=None, maxevents=-1)

Wait for events. If *timeout* is given, it specifies the length of time in seconds (may be non-integer) which the system will wait for events before returning.

::: versionchanged
3.5 The function is now retried with a recomputed timeout when interrupted by a signal, except if the signal handler raises an exception (see `475`{.interpreted-text role="pep"} for the rationale), instead of raising `InterruptedError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.15 Accepts any real number as *timeout*, not only integer or float.
:::
:::::

## Polling Objects {#poll-objects}

The `!poll`{.interpreted-text role="c:func"} system call, supported on most Unix systems, provides better scalability for network servers that service many, many clients at the same time. `!poll`{.interpreted-text role="c:func"} scales better because the system call only requires listing the file descriptors of interest, while `!select`{.interpreted-text role="c:func"} builds a bitmap, turns on bits for the fds of interest, and then afterward the whole bitmap has to be linearly scanned again. `!select`{.interpreted-text role="c:func"} is *O*(*highest file descriptor*), while `!poll`{.interpreted-text role="c:func"} is *O*(*number of file descriptors*).

::: method
poll.register(fd\[, eventmask\])

Register a file descriptor with the polling object. Future calls to the `poll`{.interpreted-text role="meth"} method will then check whether the file descriptor has any pending I/O events. *fd* can be either an integer, or an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method that returns an integer. File objects implement `!fileno`{.interpreted-text role="meth"}, so they can also be used as the argument.

*eventmask* is an optional bitmask describing the type of events you want to check for, and can be a combination of the constants `POLLIN`{.interpreted-text role="const"}, `POLLPRI`{.interpreted-text role="const"}, and `POLLOUT`{.interpreted-text role="const"}, described in the table below. If not specified, the default value used will check for all 3 types of events.

  -----------------------------------------------------------------------------------------------------------------------------
  Constant                                      Meaning
  --------------------------------------------- -------------------------------------------------------------------------------
  `POLLIN`{.interpreted-text role="const"}      There is data to read

  `POLLPRI`{.interpreted-text role="const"}     There is urgent data to read

  `POLLOUT`{.interpreted-text role="const"}     Ready for output: writing will not block

  `POLLERR`{.interpreted-text role="const"}     Error condition of some sort

  `POLLHUP`{.interpreted-text role="const"}     Hung up

  `POLLRDHUP`{.interpreted-text role="const"}   Stream socket peer closed connection, or shut down writing half of connection

  `POLLNVAL`{.interpreted-text role="const"}    Invalid request: descriptor not open
  -----------------------------------------------------------------------------------------------------------------------------

Registering a file descriptor that\'s already registered is not an error, and has the same effect as registering the descriptor exactly once.
:::

::: method
poll.modify(fd, eventmask)

Modifies an already registered fd. This has the same effect as `register(fd, eventmask)`. Attempting to modify a file descriptor that was never registered causes an `OSError`{.interpreted-text role="exc"} exception with errno `ENOENT`{.interpreted-text role="const"} to be raised.
:::

::: method
poll.unregister(fd)

Remove a file descriptor being tracked by a polling object. Just like the `register`{.interpreted-text role="meth"} method, *fd* can be an integer or an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method that returns an integer.

Attempting to remove a file descriptor that was never registered causes a `KeyError`{.interpreted-text role="exc"} exception to be raised.
:::

::::: method
poll.poll(\[timeout\])

Polls the set of registered file descriptors, and returns a possibly empty list containing `(fd, event)` 2-tuples for the descriptors that have events or errors to report. *fd* is the file descriptor, and *event* is a bitmask with bits set for the reported events for that descriptor \-\-- `POLLIN`{.interpreted-text role="const"} for waiting input, `POLLOUT`{.interpreted-text role="const"} to indicate that the descriptor can be written to, and so forth. An empty list indicates that the call timed out and no file descriptors had any events to report. If *timeout* is given, it specifies the length of time in milliseconds which the system will wait for events before returning. If *timeout* is omitted, negative, or `None`{.interpreted-text role="const"}, the call will block until there is an event for this poll object.

::: versionchanged
3.5 The function is now retried with a recomputed timeout when interrupted by a signal, except if the signal handler raises an exception (see `475`{.interpreted-text role="pep"} for the rationale), instead of raising `InterruptedError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.15 Accepts any real number as *timeout*, not only integer or float. If `ppoll()` function is available, *timeout* has a resolution of `1` ns (`1e-6` ms) instead of `1` ms.
:::
:::::

## Kqueue Objects

::: method
kqueue.close()

Close the control file descriptor of the kqueue object.
:::

::: attribute
kqueue.closed

`True` if the kqueue object is closed.
:::

::: method
kqueue.fileno()

Return the file descriptor number of the control fd.
:::

::: method
kqueue.fromfd(fd)

Create a kqueue object from a given file descriptor.
:::

::::: method
kqueue.control(changelist, max_events\[, timeout\]) -\> eventlist

Low level interface to kevent

- changelist must be an iterable of kevent objects or `None`
- max_events must be 0 or a positive integer
- timeout in seconds (non-integers are possible); the default is `None`, to wait forever

::: versionchanged
3.5 The function is now retried with a recomputed timeout when interrupted by a signal, except if the signal handler raises an exception (see `475`{.interpreted-text role="pep"} for the rationale), instead of raising `InterruptedError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.15 Accepts any real number as *timeout*, not only integer or float.
:::
:::::

## Kevent Objects

<https://man.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2>

::: attribute
kevent.ident

Value used to identify the event. The interpretation depends on the filter but it\'s usually the file descriptor. In the constructor ident can either be an int or an object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method. kevent stores the integer internally.
:::

::: attribute
kevent.filter

Name of the kernel filter.

  ---------------------------------------------------------------------------------------------------------------------------------
  Constant                                             Meaning
  ---------------------------------------------------- ----------------------------------------------------------------------------
  `KQ_FILTER_READ`{.interpreted-text role="const"}     Takes a descriptor and returns whenever there is data available to read

  `KQ_FILTER_WRITE`{.interpreted-text role="const"}    Takes a descriptor and returns whenever there is data available to write

  `KQ_FILTER_AIO`{.interpreted-text role="const"}      AIO requests

  `KQ_FILTER_VNODE`{.interpreted-text role="const"}    Returns when one or more of the requested events watched in *fflag* occurs

  `KQ_FILTER_PROC`{.interpreted-text role="const"}     Watch for events on a process id

  `KQ_FILTER_NETDEV`{.interpreted-text role="const"}   Watch for events on a network device \[not available on macOS\]

  `KQ_FILTER_SIGNAL`{.interpreted-text role="const"}   Returns whenever the watched signal is delivered to the process

  `KQ_FILTER_TIMER`{.interpreted-text role="const"}    Establishes an arbitrary timer
  ---------------------------------------------------------------------------------------------------------------------------------
:::

::: attribute
kevent.flags

Filter action.

  ------------------------------------------------------------------------------------------------
  Constant                                           Meaning
  -------------------------------------------------- ---------------------------------------------
  `KQ_EV_ADD`{.interpreted-text role="const"}        Adds or modifies an event

  `KQ_EV_DELETE`{.interpreted-text role="const"}     Removes an event from the queue

  `KQ_EV_ENABLE`{.interpreted-text role="const"}     Permits control() to return the event

  `KQ_EV_DISABLE`{.interpreted-text role="const"}    Disables event

  `KQ_EV_ONESHOT`{.interpreted-text role="const"}    Removes event after first occurrence

  `KQ_EV_CLEAR`{.interpreted-text role="const"}      Reset the state after an event is retrieved

  `KQ_EV_SYSFLAGS`{.interpreted-text role="const"}   internal event

  `KQ_EV_FLAG1`{.interpreted-text role="const"}      internal event

  `KQ_EV_EOF`{.interpreted-text role="const"}        Filter specific EOF condition

  `KQ_EV_ERROR`{.interpreted-text role="const"}      See return values
  ------------------------------------------------------------------------------------------------
:::

::: attribute
kevent.fflags

Filter specific flags.

`KQ_FILTER_READ`{.interpreted-text role="const"} and `KQ_FILTER_WRITE`{.interpreted-text role="const"} filter flags:

  ---------------------------------------------------------------------------------------------
  Constant                                          Meaning
  ------------------------------------------------- -------------------------------------------
  `KQ_NOTE_LOWAT`{.interpreted-text role="const"}   low water mark of a socket buffer

  ---------------------------------------------------------------------------------------------

`KQ_FILTER_VNODE`{.interpreted-text role="const"} filter flags:

  ----------------------------------------------------------------------------------------------
  Constant                                           Meaning
  -------------------------------------------------- -------------------------------------------
  `KQ_NOTE_DELETE`{.interpreted-text role="const"}   *unlink()* was called

  `KQ_NOTE_WRITE`{.interpreted-text role="const"}    a write occurred

  `KQ_NOTE_EXTEND`{.interpreted-text role="const"}   the file was extended

  `KQ_NOTE_ATTRIB`{.interpreted-text role="const"}   an attribute was changed

  `KQ_NOTE_LINK`{.interpreted-text role="const"}     the link count has changed

  `KQ_NOTE_RENAME`{.interpreted-text role="const"}   the file was renamed

  `KQ_NOTE_REVOKE`{.interpreted-text role="const"}   access to the file was revoked
  ----------------------------------------------------------------------------------------------

`KQ_FILTER_PROC`{.interpreted-text role="const"} filter flags:

  ------------------------------------------------------------------------------------------------------
  Constant                                              Meaning
  ----------------------------------------------------- ------------------------------------------------
  `KQ_NOTE_EXIT`{.interpreted-text role="const"}        the process has exited

  `KQ_NOTE_FORK`{.interpreted-text role="const"}        the process has called *fork()*

  `KQ_NOTE_EXEC`{.interpreted-text role="const"}        the process has executed a new process

  `KQ_NOTE_PCTRLMASK`{.interpreted-text role="const"}   internal filter flag

  `KQ_NOTE_PDATAMASK`{.interpreted-text role="const"}   internal filter flag

  `KQ_NOTE_TRACK`{.interpreted-text role="const"}       follow a process across *fork()*

  `KQ_NOTE_CHILD`{.interpreted-text role="const"}       returned on the child process for *NOTE_TRACK*

  `KQ_NOTE_TRACKERR`{.interpreted-text role="const"}    unable to attach to a child
  ------------------------------------------------------------------------------------------------------

`KQ_FILTER_NETDEV`{.interpreted-text role="const"} filter flags (not available on macOS):

  ------------------------------------------------------------------------------------------------
  Constant                                             Meaning
  ---------------------------------------------------- -------------------------------------------
  `KQ_NOTE_LINKUP`{.interpreted-text role="const"}     link is up

  `KQ_NOTE_LINKDOWN`{.interpreted-text role="const"}   link is down

  `KQ_NOTE_LINKINV`{.interpreted-text role="const"}    link state is invalid
  ------------------------------------------------------------------------------------------------
:::

::: attribute
kevent.data

Filter specific data.
:::

::: attribute
kevent.udata

User defined value.
:::
