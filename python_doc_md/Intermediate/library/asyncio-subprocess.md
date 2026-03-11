::: currentmodule
asyncio
:::

# Subprocesses {#asyncio-subprocess}

**Source code:** `Lib/asyncio/subprocess.py`{.interpreted-text role="source"}, `Lib/asyncio/base_subprocess.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This section describes high-level async/await asyncio APIs to create and manage subprocesses.

::: {#asyncio_example_subprocess_shell}
Here\'s an example of how asyncio can run a shell command and obtain its result:

    import asyncio

    async def run(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    asyncio.run(run('ls /zzz'))
:::

will print:

    ['ls /zzz' exited with 1]
    [stderr]
    ls: /zzz: No such file or directory

Because all asyncio subprocess functions are asynchronous and asyncio provides many tools to work with such functions, it is easy to execute and monitor multiple subprocesses in parallel. It is indeed trivial to modify the above example to run several commands simultaneously:

    async def main():
        await asyncio.gather(
            run('ls /zzz'),
            run('sleep 1; echo "hello"'))

    asyncio.run(main())

See also the [Examples](#examples) subsection.

## Creating Subprocesses

:::: {.function async=""}
create_subprocess_exec(program, *args, stdin=None, stdout=None, stderr=None, limit=None,*\*kwds)

Create a subprocess.

The *limit* argument sets the buffer limit for `StreamReader`{.interpreted-text role="class"} wrappers for `~asyncio.subprocess.Process.stdout`{.interpreted-text role="attr"} and `~asyncio.subprocess.Process.stderr`{.interpreted-text role="attr"} (if `subprocess.PIPE`{.interpreted-text role="const"} is passed to *stdout* and *stderr* arguments).

Return a `~asyncio.subprocess.Process`{.interpreted-text role="class"} instance.

See the documentation of `loop.subprocess_exec`{.interpreted-text role="meth"} for other parameters.

If the process object is garbage collected while the process is still running, the child process will be killed.

::: versionchanged
3.10 Removed the *loop* parameter.
:::
::::

:::::: {.function async=""}
create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, limit=None, \*\*kwds)

Run the *cmd* shell command.

The *limit* argument sets the buffer limit for `StreamReader`{.interpreted-text role="class"} wrappers for `~asyncio.subprocess.Process.stdout`{.interpreted-text role="attr"} and `~asyncio.subprocess.Process.stderr`{.interpreted-text role="attr"} (if `subprocess.PIPE`{.interpreted-text role="const"} is passed to *stdout* and *stderr* arguments).

Return a `~asyncio.subprocess.Process`{.interpreted-text role="class"} instance.

See the documentation of `loop.subprocess_shell`{.interpreted-text role="meth"} for other parameters.

If the process object is garbage collected while the process is still running, the child process will be killed.

:::: important
::: title
Important
:::

It is the application\'s responsibility to ensure that all whitespace and special characters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection) vulnerabilities. The `shlex.quote`{.interpreted-text role="func"} function can be used to properly escape whitespace and special shell characters in strings that are going to be used to construct shell commands.
::::

::: versionchanged
3.10 Removed the *loop* parameter.
:::
::::::

:::: note
::: title
Note
:::

Subprocesses are available for Windows if a `ProactorEventLoop`{.interpreted-text role="class"} is used. See `Subprocess Support on Windows <asyncio-windows-subprocess>`{.interpreted-text role="ref"} for details.
::::

::: seealso
asyncio also has the following *low-level* APIs to work with subprocesses: `loop.subprocess_exec`{.interpreted-text role="meth"}, `loop.subprocess_shell`{.interpreted-text role="meth"}, `loop.connect_read_pipe`{.interpreted-text role="meth"}, `loop.connect_write_pipe`{.interpreted-text role="meth"}, as well as the `Subprocess Transports <asyncio-subprocess-transports>`{.interpreted-text role="ref"} and `Subprocess Protocols <asyncio-subprocess-protocols>`{.interpreted-text role="ref"}.
:::

## Constants

::: {.data module=""}
asyncio.subprocess.PIPE

Can be passed to the *stdin*, *stdout* or *stderr* parameters.

If *PIPE* is passed to *stdin* argument, the `Process.stdin <asyncio.subprocess.Process.stdin>`{.interpreted-text role="attr"} attribute will point to a `~asyncio.StreamWriter`{.interpreted-text role="class"} instance.

If *PIPE* is passed to *stdout* or *stderr* arguments, the `Process.stdout <asyncio.subprocess.Process.stdout>`{.interpreted-text role="attr"} and `Process.stderr <asyncio.subprocess.Process.stderr>`{.interpreted-text role="attr"} attributes will point to `~asyncio.StreamReader`{.interpreted-text role="class"} instances.
:::

::: {.data module=""}
asyncio.subprocess.STDOUT

Special value that can be used as the *stderr* argument and indicates that standard error should be redirected into standard output.
:::

::: {.data module=""}
asyncio.subprocess.DEVNULL

Special value that can be used as the *stdin*, *stdout* or *stderr* argument to process creation functions. It indicates that the special file `os.devnull`{.interpreted-text role="data"} will be used for the corresponding subprocess stream.
:::

## Interacting with Subprocesses

Both `create_subprocess_exec`{.interpreted-text role="func"} and `create_subprocess_shell`{.interpreted-text role="func"} functions return instances of the *Process* class. *Process* is a high-level wrapper that allows communicating with subprocesses and watching for their completion.

:::::::::::::::::::: {.asyncio.subprocess.Process module=""}
An object that wraps OS processes created by the `~asyncio.create_subprocess_exec`{.interpreted-text role="func"} and `~asyncio.create_subprocess_shell`{.interpreted-text role="func"} functions.

This class is designed to have a similar API to the `subprocess.Popen`{.interpreted-text role="class"} class, but there are some notable differences:

- unlike Popen, Process instances do not have an equivalent to the `~subprocess.Popen.poll`{.interpreted-text role="meth"} method;
- the `~asyncio.subprocess.Process.communicate`{.interpreted-text role="meth"} and `~asyncio.subprocess.Process.wait`{.interpreted-text role="meth"} methods don\'t have a *timeout* parameter: use the `~asyncio.wait_for`{.interpreted-text role="func"} function;
- the `Process.wait() <asyncio.subprocess.Process.wait>`{.interpreted-text role="meth"} method is asynchronous, whereas `subprocess.Popen.wait`{.interpreted-text role="meth"} method is implemented as a blocking busy loop;
- the *universal_newlines* parameter is not supported.

This class is `not thread safe <asyncio-multithreading>`{.interpreted-text role="ref"}.

See also the `Subprocess and Threads <asyncio-subprocess-threads>`{.interpreted-text role="ref"} section.

::::: {.method async=""}
wait()

Wait for the child process to terminate.

Set and return the `returncode`{.interpreted-text role="attr"} attribute.

:::: note
::: title
Note
:::

This method can deadlock when using `stdout=PIPE` or `stderr=PIPE` and the child process generates so much output that it blocks waiting for the OS pipe buffer to accept more data. Use the `communicate`{.interpreted-text role="meth"} method when using pipes to avoid this condition.
::::
:::::

:::: {.method async=""}
communicate(input=None)

Interact with process:

1.  send data to *stdin* (if *input* is not `None`);
2.  closes *stdin*;
3.  read data from *stdout* and *stderr*, until EOF is reached;
4.  wait for process to terminate.

The optional *input* argument is the data (`bytes`{.interpreted-text role="class"} object) that will be sent to the child process.

Return a tuple `(stdout_data, stderr_data)`.

If either `BrokenPipeError`{.interpreted-text role="exc"} or `ConnectionResetError`{.interpreted-text role="exc"} exception is raised when writing *input* into *stdin*, the exception is ignored. This condition occurs when the process exits before all data are written into *stdin*.

If it is desired to send data to the process\' *stdin*, the process needs to be created with `stdin=PIPE`. Similarly, to get anything other than `None` in the result tuple, the process has to be created with `stdout=PIPE` and/or `stderr=PIPE` arguments.

Note, that the data read is buffered in memory, so do not use this method if the data size is large or unlimited.

::: versionchanged
3.12

*stdin* gets closed when `input=None` too.
:::
::::

::::: method
send_signal(signal)

Sends the signal *signal* to the child process.

:::: note
::: title
Note
:::

On Windows, `~signal.SIGTERM`{.interpreted-text role="py:const"} is an alias for `terminate`{.interpreted-text role="meth"}. `CTRL_C_EVENT` and `CTRL_BREAK_EVENT` can be sent to processes started with a *creationflags* parameter which includes `CREATE_NEW_PROCESS_GROUP`.
::::
:::::

::: method
terminate()

Stop the child process.

On POSIX systems this method sends `~signal.SIGTERM`{.interpreted-text role="py:const"} to the child process.

On Windows the Win32 API function `!TerminateProcess`{.interpreted-text role="c:func"} is called to stop the child process.
:::

::: method
kill()

Kill the child process.

On POSIX systems this method sends `~signal.SIGKILL`{.interpreted-text role="py:data"} to the child process.

On Windows this method is an alias for `terminate`{.interpreted-text role="meth"}.
:::

::: attribute
stdin

Standard input stream (`~asyncio.StreamWriter`{.interpreted-text role="class"}) or `None` if the process was created with `stdin=None`.
:::

::: attribute
stdout

Standard output stream (`~asyncio.StreamReader`{.interpreted-text role="class"}) or `None` if the process was created with `stdout=None`.
:::

::: attribute
stderr

Standard error stream (`~asyncio.StreamReader`{.interpreted-text role="class"}) or `None` if the process was created with `stderr=None`.
:::

:::: warning
::: title
Warning
:::

Use the `communicate`{.interpreted-text role="meth"} method rather than `process.stdin.write() <stdin>`{.interpreted-text role="attr"}, `await process.stdout.read() <stdout>`{.interpreted-text role="attr"} or `await process.stderr.read() <stderr>`{.interpreted-text role="attr"}. This avoids deadlocks due to streams pausing reading or writing and blocking the child process.
::::

::: attribute
pid

Process identification number (PID).

Note that for processes created by the `~asyncio.create_subprocess_shell`{.interpreted-text role="func"} function, this attribute is the PID of the spawned shell.
:::

::: attribute
returncode

Return code of the process when it exits.

A `None` value indicates that the process has not terminated yet.

A negative value `-N` indicates that the child was terminated by signal `N` (POSIX only).
:::
::::::::::::::::::::

### Subprocess and Threads {#asyncio-subprocess-threads}

Standard asyncio event loop supports running subprocesses from different threads by default.

On Windows subprocesses are provided by `ProactorEventLoop`{.interpreted-text role="class"} only (default), `SelectorEventLoop`{.interpreted-text role="class"} has no subprocess support.

Note that alternative event loop implementations might have own limitations; please refer to their documentation.

::: seealso
The `Concurrency and multithreading in asyncio
<asyncio-multithreading>`{.interpreted-text role="ref"} section.
:::

### Examples

An example using the `~asyncio.subprocess.Process`{.interpreted-text role="class"} class to control a subprocess and the `StreamReader`{.interpreted-text role="class"} class to read from its standard output.

::: {#asyncio_example_create_subprocess_exec}
The subprocess is created by the `create_subprocess_exec`{.interpreted-text role="func"} function:

    import asyncio
    import sys

    async def get_date():
        code = 'import datetime; print(datetime.datetime.now())'

        # Create the subprocess; redirect the standard output
        # into a pipe.
        proc = await asyncio.create_subprocess_exec(
            sys.executable, '-c', code,
            stdout=asyncio.subprocess.PIPE)

        # Read one line of output.
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()

        # Wait for the subprocess exit.
        await proc.wait()
        return line

    date = asyncio.run(get_date())
    print(f"Current date: {date}")
:::

See also the `same example <asyncio_example_subprocess_proto>`{.interpreted-text role="ref"} written using low-level APIs.
