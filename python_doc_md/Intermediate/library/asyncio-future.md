::: currentmodule
asyncio
:::

# Futures {#asyncio-futures}

**Source code:** `Lib/asyncio/futures.py`{.interpreted-text role="source"}, `Lib/asyncio/base_futures.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

*Future* objects are used to bridge **low-level callback-based code** with high-level async/await code.

## Future Functions

:::: function
isfuture(obj)

Return `True` if *obj* is either of:

- an instance of `asyncio.Future`{.interpreted-text role="class"},
- an instance of `asyncio.Task`{.interpreted-text role="class"},
- a Future-like object with a `_asyncio_future_blocking` attribute.

::: versionadded
3.5
:::
::::

::::::: function
ensure_future(obj, \*, loop=None)

Return:

- *obj* argument as is, if *obj* is a `Future`{.interpreted-text role="class"}, a `Task`{.interpreted-text role="class"}, or a Future-like object (`isfuture`{.interpreted-text role="func"} is used for the test.)
- a `Task`{.interpreted-text role="class"} object wrapping *obj*, if *obj* is a coroutine (`iscoroutine`{.interpreted-text role="func"} is used for the test); in this case the coroutine will be scheduled by `ensure_future()`.
- a `Task`{.interpreted-text role="class"} object that would await on *obj*, if *obj* is an awaitable (`inspect.isawaitable`{.interpreted-text role="func"} is used for the test.)

If *obj* is neither of the above a `TypeError`{.interpreted-text role="exc"} is raised.

:::: important
::: title
Important
:::

Save a reference to the result of this function, to avoid a task disappearing mid-execution.

See also the `create_task`{.interpreted-text role="func"} function which is the preferred way for creating new tasks or use `asyncio.TaskGroup`{.interpreted-text role="class"} which keeps reference to the task internally.
::::

::: versionchanged
3.5.1 The function accepts any `awaitable`{.interpreted-text role="term"} object.
:::

::: deprecated
3.10 Deprecation warning is emitted if *obj* is not a Future-like object and *loop* is not specified and there is no running event loop.
:::
:::::::

:::: function
wrap_future(future, \*, loop=None)

Wrap a `concurrent.futures.Future`{.interpreted-text role="class"} object in a `asyncio.Future`{.interpreted-text role="class"} object.

::: deprecated
3.10 Deprecation warning is emitted if *future* is not a Future-like object and *loop* is not specified and there is no running event loop.
:::
::::

## Future Object {#asyncio-future-obj}

:::::::::::::::::: {.Future(*, .loop=None)}
A Future represents an eventual result of an asynchronous operation. Not thread-safe.

Future is an `awaitable`{.interpreted-text role="term"} object. Coroutines can await on Future objects until they either have a result or an exception set, or until they are cancelled. A Future can be awaited multiple times and the result is same.

Typically Futures are used to enable low-level callback-based code (e.g. in protocols implemented using asyncio `transports <asyncio-transports-protocols>`{.interpreted-text role="ref"}) to interoperate with high-level async/await code.

The rule of thumb is to never expose Future objects in user-facing APIs, and the recommended way to create a Future object is to call `loop.create_future`{.interpreted-text role="meth"}. This way alternative event loop implementations can inject their own optimized implementations of a Future object.

::: versionchanged
3.7 Added support for the `contextvars`{.interpreted-text role="mod"} module.
:::

::: deprecated
3.10 Deprecation warning is emitted if *loop* is not specified and there is no running event loop.
:::

::: method
result()

Return the result of the Future.

If the Future is *done* and has a result set by the `set_result`{.interpreted-text role="meth"} method, the result value is returned.

If the Future is *done* and has an exception set by the `set_exception`{.interpreted-text role="meth"} method, this method raises the exception.

If the Future has been *cancelled*, this method raises a `CancelledError`{.interpreted-text role="exc"} exception.

If the Future\'s result isn\'t yet available, this method raises an `InvalidStateError`{.interpreted-text role="exc"} exception.
:::

::: method
set_result(result)

Mark the Future as *done* and set its result.

Raises an `InvalidStateError`{.interpreted-text role="exc"} error if the Future is already *done*.
:::

::: method
set_exception(exception)

Mark the Future as *done* and set an exception.

Raises an `InvalidStateError`{.interpreted-text role="exc"} error if the Future is already *done*.
:::

::: method
done()

Return `True` if the Future is *done*.

A Future is *done* if it was *cancelled* or if it has a result or an exception set with `set_result`{.interpreted-text role="meth"} or `set_exception`{.interpreted-text role="meth"} calls.
:::

::: method
cancelled()

Return `True` if the Future was *cancelled*.

The method is usually used to check if a Future is not *cancelled* before setting a result or an exception for it:

    if not fut.cancelled():
        fut.set_result(42)
:::

:::: method
add_done_callback(callback, \*, context=None)

Add a callback to be run when the Future is *done*.

The *callback* is called with the Future object as its only argument.

If the Future is already *done* when this method is called, the callback is scheduled with `loop.call_soon`{.interpreted-text role="meth"}.

An optional keyword-only *context* argument allows specifying a custom `contextvars.Context`{.interpreted-text role="class"} for the *callback* to run in. The current context is used when no *context* is provided.

`functools.partial`{.interpreted-text role="func"} can be used to pass parameters to the callback, e.g.:

    # Call 'print("Future:", fut)' when "fut" is done.
    fut.add_done_callback(
        functools.partial(print, "Future:"))

::: versionchanged
3.7 The *context* keyword-only parameter was added. See `567`{.interpreted-text role="pep"} for more details.
:::
::::

::: method
remove_done_callback(callback)

Remove *callback* from the callbacks list.

Returns the number of callbacks removed, which is typically 1, unless a callback was added more than once.
:::

:::: method
cancel(msg=None)

Cancel the Future and schedule callbacks.

If the Future is already *done* or *cancelled*, return `False`. Otherwise, change the Future\'s state to *cancelled*, schedule the callbacks, and return `True`.

::: versionchanged
3.9 Added the *msg* parameter.
:::
::::

::: method
exception()

Return the exception that was set on this Future.

The exception (or `None` if no exception was set) is returned only if the Future is *done*.

If the Future has been *cancelled*, this method raises a `CancelledError`{.interpreted-text role="exc"} exception.

If the Future isn\'t *done* yet, this method raises an `InvalidStateError`{.interpreted-text role="exc"} exception.
:::

:::: method
get_loop()

Return the event loop the Future object is bound to.

::: versionadded
3.7
:::
::::
::::::::::::::::::

::: {#asyncio_example_future}
This example creates a Future object, creates and schedules an asynchronous Task to set result for the Future, and waits until the Future has a result:

    async def set_after(fut, delay, value):
        # Sleep for *delay* seconds.
        await asyncio.sleep(delay)

        # Set *value* as a result of *fut* Future.
        fut.set_result(value)

    async def main():
        # Get the current event loop.
        loop = asyncio.get_running_loop()

        # Create a new Future object.
        fut = loop.create_future()

        # Run "set_after()" coroutine in a parallel Task.
        # We are using the low-level "loop.create_task()" API here because
        # we already have a reference to the event loop at hand.
        # Otherwise we could have just used "asyncio.create_task()".
        loop.create_task(
            set_after(fut, 1, '... world'))

        print('hello ...')

        # Wait until *fut* has a result (1 second) and print it.
        print(await fut)

    asyncio.run(main())
:::

:::: important
::: title
Important
:::

The Future object was designed to mimic `concurrent.futures.Future`{.interpreted-text role="class"}. Key differences include:

- unlike asyncio Futures, `concurrent.futures.Future`{.interpreted-text role="class"} instances cannot be awaited.
- `asyncio.Future.result`{.interpreted-text role="meth"} and `asyncio.Future.exception`{.interpreted-text role="meth"} do not accept the *timeout* argument.
- `asyncio.Future.result`{.interpreted-text role="meth"} and `asyncio.Future.exception`{.interpreted-text role="meth"} raise an `InvalidStateError`{.interpreted-text role="exc"} exception when the Future is not *done*.
- Callbacks registered with `asyncio.Future.add_done_callback`{.interpreted-text role="meth"} are not called immediately. They are scheduled with `loop.call_soon`{.interpreted-text role="meth"} instead.
- asyncio Future is not compatible with the `concurrent.futures.wait`{.interpreted-text role="func"} and `concurrent.futures.as_completed`{.interpreted-text role="func"} functions.
- `asyncio.Future.cancel`{.interpreted-text role="meth"} accepts an optional `msg` argument, but `concurrent.futures.Future.cancel`{.interpreted-text role="meth"} does not.
::::
