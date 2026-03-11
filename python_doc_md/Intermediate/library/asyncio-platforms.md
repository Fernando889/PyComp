::: currentmodule
asyncio
:::

# Platform Support {#asyncio-platform-support}

The `asyncio`{.interpreted-text role="mod"} module is designed to be portable, but some platforms have subtle differences and limitations due to the platforms\' underlying architecture and capabilities.

## All Platforms

- `loop.add_reader`{.interpreted-text role="meth"} and `loop.add_writer`{.interpreted-text role="meth"} cannot be used to monitor file I/O.

## Windows

**Source code:** `Lib/asyncio/proactor_events.py`{.interpreted-text role="source"}, `Lib/asyncio/windows_events.py`{.interpreted-text role="source"}, `Lib/asyncio/windows_utils.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

::: versionchanged
3.8

On Windows, `ProactorEventLoop`{.interpreted-text role="class"} is now the default event loop.
:::

All event loops on Windows do not support the following methods:

- `loop.create_unix_connection`{.interpreted-text role="meth"} and `loop.create_unix_server`{.interpreted-text role="meth"} are not supported. The `socket.AF_UNIX`{.interpreted-text role="const"} socket family is specific to Unix.
- `loop.add_signal_handler`{.interpreted-text role="meth"} and `loop.remove_signal_handler`{.interpreted-text role="meth"} are not supported.

`SelectorEventLoop`{.interpreted-text role="class"} has the following limitations:

- `~selectors.SelectSelector`{.interpreted-text role="class"} is used to wait on socket events: it supports sockets and is limited to 512 sockets.
- `loop.add_reader`{.interpreted-text role="meth"} and `loop.add_writer`{.interpreted-text role="meth"} only accept socket handles (e.g. pipe file descriptors are not supported).
- Pipes are not supported, so the `loop.connect_read_pipe`{.interpreted-text role="meth"} and `loop.connect_write_pipe`{.interpreted-text role="meth"} methods are not implemented.
- `Subprocesses <asyncio-subprocess>`{.interpreted-text role="ref"} are not supported, i.e. `loop.subprocess_exec`{.interpreted-text role="meth"} and `loop.subprocess_shell`{.interpreted-text role="meth"} methods are not implemented.

`ProactorEventLoop`{.interpreted-text role="class"} has the following limitations:

- The `loop.add_reader`{.interpreted-text role="meth"} and `loop.add_writer`{.interpreted-text role="meth"} methods are not supported.

The resolution of the monotonic clock on Windows is usually around 15.6 milliseconds. The best resolution is 0.5 milliseconds. The resolution depends on the hardware (availability of [HPET](https://en.wikipedia.org/wiki/High_Precision_Event_Timer)) and on the Windows configuration.

### Subprocess Support on Windows {#asyncio-windows-subprocess}

On Windows, the default event loop `ProactorEventLoop`{.interpreted-text role="class"} supports subprocesses, whereas `SelectorEventLoop`{.interpreted-text role="class"} does not.

## macOS

Modern macOS versions are fully supported.

**macOS \<= 10.8**

On macOS 10.6, 10.7 and 10.8, the default event loop uses `selectors.KqueueSelector`{.interpreted-text role="class"}, which does not support character devices on these versions. The `SelectorEventLoop`{.interpreted-text role="class"} can be manually configured to use `~selectors.SelectSelector`{.interpreted-text role="class"} or `~selectors.PollSelector`{.interpreted-text role="class"} to support character devices on these older versions of macOS. Example:

    import asyncio
    import selectors

    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
