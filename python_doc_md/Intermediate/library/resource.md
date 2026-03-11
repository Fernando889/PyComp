# `!resource`{.interpreted-text role="mod"} \-\-- Resource usage information

::: {.module synopsis="An interface to provide resource usage information on the current process."}
resource
:::

------------------------------------------------------------------------

This module provides basic mechanisms for measuring and controlling system resources utilized by a program.

::: availability
Unix, not WASI.
:::

Symbolic constants are used to specify particular system resources and to request usage information about either the current process or its children.

An `OSError`{.interpreted-text role="exc"} is raised on syscall failure.

:::: exception
error

A deprecated alias of `OSError`{.interpreted-text role="exc"}.

::: versionchanged
3.3 Following `3151`{.interpreted-text role="pep"}, this class was made an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

## Resource Limits

Resources usage can be limited using the `setrlimit`{.interpreted-text role="func"} function described below. Each resource is controlled by a pair of limits: a soft limit and a hard limit. The soft limit is the current limit, and may be lowered or raised by a process over time. The soft limit can never exceed the hard limit. The hard limit can be lowered to any value greater than the soft limit, but not raised. (Only processes with the effective UID of the super-user can raise a hard limit.)

The specific resources that can be limited are system dependent. They are described in the `getrlimit(2)`{.interpreted-text role="manpage"} man page. The resources listed below are supported when the underlying operating system supports them; resources which cannot be checked or controlled by the operating system are not defined in this module for those platforms.

:::: data
RLIM_INFINITY

Constant used to represent the limit for an unlimited resource.

::: versionchanged
3.15 It is now always positive. Previously, it could be negative, such as -1 or -3.
:::
::::

::: data
RLIM_SAVED_CUR
:::

:::: data
RLIM_SAVED_MAX

Constants used to represent the soft and hard limit values if they cannot be represented in the `rlim_t` value in C. Can be equal to `RLIM_INFINITY`{.interpreted-text role="data"}.

::: versionadded
3.15
:::
::::

::: function
getrlimit(resource)

Returns a tuple `(soft, hard)` with the current soft and hard limits of *resource*. Raises `ValueError`{.interpreted-text role="exc"} if an invalid resource is specified, or `error`{.interpreted-text role="exc"} if the underlying system call fails unexpectedly.
:::

:::: function
setrlimit(resource, limits)

Sets new limits of consumption of *resource*. The *limits* argument must be a tuple `(soft, hard)` of two integers describing the new limits. A value of `~resource.RLIM_INFINITY`{.interpreted-text role="const"} can be used to request a limit that is unlimited.

Raises `ValueError`{.interpreted-text role="exc"} if an invalid resource is specified, if the new soft limit exceeds the hard limit, or if a process tries to raise its hard limit. Specifying a limit of `~resource.RLIM_INFINITY`{.interpreted-text role="const"} when the hard or system limit for that resource is not unlimited will result in a `ValueError`{.interpreted-text role="exc"}. A process with the effective UID of super-user can request any valid limit value, including unlimited, but `ValueError`{.interpreted-text role="exc"} will still be raised if the requested limit exceeds the system imposed limit.

`setrlimit` may also raise `error`{.interpreted-text role="exc"} if the underlying system call fails.

VxWorks only supports setting `RLIMIT_NOFILE`{.interpreted-text role="const"}.

::: audit-event
resource.setrlimit resource,limits resource.setrlimit
:::
::::

:::::: function
prlimit(pid, resource\[, limits\])

Combines `setrlimit`{.interpreted-text role="func"} and `getrlimit`{.interpreted-text role="func"} in one function and supports to get and set the resources limits of an arbitrary process. If *pid* is 0, then the call applies to the current process. *resource* and *limits* have the same meaning as in `setrlimit`{.interpreted-text role="func"}, except that *limits* is optional.

When *limits* is not given the function returns the *resource* limit of the process *pid*. When *limits* is given the *resource* limit of the process is set and the former resource limit is returned.

Raises `ProcessLookupError`{.interpreted-text role="exc"} when *pid* can\'t be found and `PermissionError`{.interpreted-text role="exc"} when the user doesn\'t have `CAP_SYS_RESOURCE` for the process.

::: audit-event
resource.prlimit pid,resource,limits resource.prlimit
:::

::: availability
Linux \>= 2.6.36 with glibc \>= 2.13.
:::

::: versionadded
3.4
:::
::::::

These symbols define resources whose consumption can be controlled using the `setrlimit`{.interpreted-text role="func"} and `getrlimit`{.interpreted-text role="func"} functions described below. The values of these symbols are exactly the constants used by C programs.

The Unix man page for `getrlimit(2)`{.interpreted-text role="manpage"} lists the available resources. Note that not all systems use the same symbol or same value to denote the same resource. This module does not attempt to mask platform differences \-\-- symbols not defined for a platform will not be available from this module on that platform.

::: data
RLIMIT_CORE

The maximum size (in bytes) of a core file that the current process can create. This may result in the creation of a partial core file if a larger core would be required to contain the entire process image.
:::

::: data
RLIMIT_CPU

The maximum amount of processor time (in seconds) that a process can use. If this limit is exceeded, a `~signal.SIGXCPU`{.interpreted-text role="const"} signal is sent to the process. (See the `signal`{.interpreted-text role="mod"} module documentation for information about how to catch this signal and do something useful, e.g. flush open files to disk.)
:::

::: data
RLIMIT_FSIZE

The maximum size of a file which the process may create.
:::

::: data
RLIMIT_DATA

The maximum size (in bytes) of the process\'s heap.
:::

::: data
RLIMIT_STACK

The maximum size (in bytes) of the call stack for the current process. This only affects the stack of the main thread in a multi-threaded process.
:::

::: data
RLIMIT_RSS

The maximum resident set size that should be made available to the process.
:::

::: data
RLIMIT_NPROC

The maximum number of processes the current process may create.
:::

::: data
RLIMIT_NOFILE

The maximum number of open file descriptors for the current process.
:::

::: data
RLIMIT_OFILE

The BSD name for `RLIMIT_NOFILE`{.interpreted-text role="const"}.
:::

::: data
RLIMIT_MEMLOCK

The maximum address space which may be locked in memory.
:::

:::: data
RLIMIT_VMEM

The largest area of mapped memory which the process may occupy. Usually an alias of `RLIMIT_AS`{.interpreted-text role="const"}.

::: availability
Solaris, FreeBSD, NetBSD.
:::
::::

::: data
RLIMIT_AS

The maximum area (in bytes) of address space which may be taken by the process.
:::

::::: data
RLIMIT_MSGQUEUE

The number of bytes that can be allocated for POSIX message queues.

::: availability
Linux \>= 2.6.8.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_NICE

The ceiling for the process\'s nice level (calculated as 20 - rlim_cur).

::: availability
Linux \>= 2.6.12.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_RTPRIO

The ceiling of the real-time priority.

::: availability
Linux \>= 2.6.12.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_RTTIME

The time limit (in microseconds) on CPU time that a process can spend under real-time scheduling without making a blocking syscall.

::: availability
Linux \>= 2.6.25.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_SIGPENDING

The number of signals which the process may queue.

::: availability
Linux \>= 2.6.8.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_SBSIZE

The maximum size (in bytes) of socket buffer usage for this user. This limits the amount of network memory, and hence the amount of mbufs, that this user may hold at any time.

::: availability
FreeBSD, NetBSD.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_SWAP

The maximum size (in bytes) of the swap space that may be reserved or used by all of this user id\'s processes. This limit is enforced only if bit 1 of the vm.overcommit sysctl is set. Please see [tuning(7)](https://man.freebsd.org/cgi/man.cgi?query=tuning&sektion=7) for a complete description of this sysctl.

::: availability
FreeBSD \>= 8.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_NPTS

The maximum number of pseudo-terminals created by this user id.

::: availability
FreeBSD \>= 8.
:::

::: versionadded
3.4
:::
:::::

::::: data
RLIMIT_KQUEUES

The maximum number of kqueues this user id is allowed to create.

::: availability
FreeBSD \>= 11.
:::

::: versionadded
3.10
:::
:::::

::::: data
RLIMIT_NTHR

The maximum number of threads for this user id, not counting the main and kernel threads.

::: availability
NetBSD \>= 7.0.
:::

::: versionadded
3.15
:::
:::::

::::: data
RLIMIT_PIPEBUF

The maximum total size of in-kernel buffers for bi-directional pipes/fifos that this user id is allowed to consume.

::: availability
FreeBSD \>= 14.2.
:::

::: versionadded
3.15
:::
:::::

::::: data
RLIMIT_THREADS

The maximum number of threads each process can create.

::: availability
AIX.
:::

::: versionadded
3.15
:::
:::::

::::: data
RLIMIT_UMTXP

The limit of the number of process-shared Posix thread library objects allocated by user id.

::: availability
FreeBSD \>= 11.
:::

::: versionadded
3.15
:::
:::::

## Resource Usage

These functions are used to retrieve resource usage information:

::: function
getrusage(who)

This function returns an object that describes the resources consumed by either the current process or its children, as specified by the *who* parameter. The *who* parameter should be specified using one of the `!RUSAGE_\*`{.interpreted-text role="const"} constants described below.

A simple example:

    from resource import *
    import time

    # a non CPU-bound task
    time.sleep(3)
    print(getrusage(RUSAGE_SELF))

    # a CPU-bound task
    for i in range(10 ** 8):
       _ = 1 + 1
    print(getrusage(RUSAGE_SELF))

The fields of the return value each describe how a particular system resource has been used, e.g. amount of time spent running in user mode or number of times the process was swapped out of main memory. Some values are dependent on the clock tick interval, e.g. the amount of memory the process is using.

For backward compatibility, the return value is also accessible as a tuple of 16 elements.

The fields `!ru_utime`{.interpreted-text role="attr"} and `!ru_stime`{.interpreted-text role="attr"} of the return value are floating-point values representing the amount of time spent executing in user mode and the amount of time spent executing in system mode, respectively. The remaining values are integers. Consult the `getrusage(2)`{.interpreted-text role="manpage"} man page for detailed information about these values. A brief summary is presented here:

  -----------------------------------------------------------------------------------------------
  Index    Field                                           Resource
  -------- ----------------------------------------------- --------------------------------------
  `0`      `!ru_utime`{.interpreted-text role="attr"}      time in user mode (float seconds)

  `1`      `!ru_stime`{.interpreted-text role="attr"}      time in system mode (float seconds)

  `2`      `!ru_maxrss`{.interpreted-text role="attr"}     maximum resident set size

  `3`      `!ru_ixrss`{.interpreted-text role="attr"}      shared memory size

  `4`      `!ru_idrss`{.interpreted-text role="attr"}      unshared memory size

  `5`      `!ru_isrss`{.interpreted-text role="attr"}      unshared stack size

  `6`      `!ru_minflt`{.interpreted-text role="attr"}     page faults not requiring I/O

  `7`      `!ru_majflt`{.interpreted-text role="attr"}     page faults requiring I/O

  `8`      `!ru_nswap`{.interpreted-text role="attr"}      number of swap outs

  `9`      `!ru_inblock`{.interpreted-text role="attr"}    block input operations

  `10`     `!ru_oublock`{.interpreted-text role="attr"}    block output operations

  `11`     `!ru_msgsnd`{.interpreted-text role="attr"}     messages sent

  `12`     `!ru_msgrcv`{.interpreted-text role="attr"}     messages received

  `13`     `!ru_nsignals`{.interpreted-text role="attr"}   signals received

  `14`     `!ru_nvcsw`{.interpreted-text role="attr"}      voluntary context switches

  `15`     `!ru_nivcsw`{.interpreted-text role="attr"}     involuntary context switches
  -----------------------------------------------------------------------------------------------

This function will raise a `ValueError`{.interpreted-text role="exc"} if an invalid *who* parameter is specified. It may also raise `error`{.interpreted-text role="exc"} exception in unusual circumstances.
:::

::: function
getpagesize()

Returns the number of bytes in a system page. (This need not be the same as the hardware page size.)
:::

The following `!RUSAGE_\*`{.interpreted-text role="const"} symbols are passed to the `getrusage`{.interpreted-text role="func"} function to specify which processes information should be provided for.

::: data
RUSAGE_SELF

Pass to `getrusage`{.interpreted-text role="func"} to request resources consumed by the calling process, which is the sum of resources used by all threads in the process.
:::

::: data
RUSAGE_CHILDREN

Pass to `getrusage`{.interpreted-text role="func"} to request resources consumed by child processes of the calling process which have been terminated and waited for.
:::

::: data
RUSAGE_BOTH

Pass to `getrusage`{.interpreted-text role="func"} to request resources consumed by both the current process and child processes. May not be available on all systems.
:::

:::: data
RUSAGE_THREAD

Pass to `getrusage`{.interpreted-text role="func"} to request resources consumed by the current thread. May not be available on all systems.

::: versionadded
3.2
:::
::::
