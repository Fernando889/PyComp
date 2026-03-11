::: currentmodule
asyncio
:::

# Exceptions {#asyncio-exceptions}

**Source code:** `Lib/asyncio/exceptions.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

:::: exception
TimeoutError

A deprecated alias of `TimeoutError`{.interpreted-text role="exc"}, raised when the operation has exceeded the given deadline.

::: versionchanged
3.11

This class was made an alias of `TimeoutError`{.interpreted-text role="exc"}.
:::
::::

:::: exception
CancelledError

The operation has been cancelled.

This exception can be caught to perform custom operations when asyncio Tasks are cancelled. In almost all situations the exception must be re-raised.

::: versionchanged
3.8

`CancelledError`{.interpreted-text role="exc"} is now a subclass of `BaseException`{.interpreted-text role="class"} rather than `Exception`{.interpreted-text role="class"}.
:::
::::

::: exception
InvalidStateError

Invalid internal state of `Task`{.interpreted-text role="class"} or `Future`{.interpreted-text role="class"}.

Can be raised in situations like setting a result value for a *Future* object that already has a result value set.
:::

::: exception
SendfileNotAvailableError

The \"sendfile\" syscall is not available for the given socket or file type.

A subclass of `RuntimeError`{.interpreted-text role="exc"}.
:::

::::: exception
IncompleteReadError

The requested read operation did not complete fully.

Raised by the `asyncio stream APIs<asyncio-streams>`{.interpreted-text role="ref"}.

This exception is a subclass of `EOFError`{.interpreted-text role="exc"}.

::: attribute
expected

The total number (`int`{.interpreted-text role="class"}) of expected bytes.
:::

::: attribute
partial

A string of `bytes`{.interpreted-text role="class"} read before the end of stream was reached.
:::
:::::

:::: exception
LimitOverrunError

Reached the buffer size limit while looking for a separator.

Raised by the `asyncio stream APIs <asyncio-streams>`{.interpreted-text role="ref"}.

::: attribute
consumed

The total number of to be consumed bytes.
:::
::::
