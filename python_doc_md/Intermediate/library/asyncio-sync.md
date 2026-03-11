::: currentmodule
asyncio
:::

# Synchronization Primitives {#asyncio-sync}

**Source code:** `Lib/asyncio/locks.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

asyncio synchronization primitives are designed to be similar to those of the `threading`{.interpreted-text role="mod"} module with two important caveats:

- asyncio primitives are not thread-safe, therefore they should not be used for OS thread synchronization (use `threading`{.interpreted-text role="mod"} for that);
- methods of these synchronization primitives do not accept the *timeout* argument; use the `asyncio.wait_for`{.interpreted-text role="func"} function to perform operations with timeouts.

asyncio has the following basic synchronization primitives:

- `Lock`{.interpreted-text role="class"}
- `Event`{.interpreted-text role="class"}
- `Condition`{.interpreted-text role="class"}
- `Semaphore`{.interpreted-text role="class"}
- `BoundedSemaphore`{.interpreted-text role="class"}
- `Barrier`{.interpreted-text role="class"}

------------------------------------------------------------------------

## Lock

::::::: Lock()
Implements a mutex lock for asyncio tasks. Not thread-safe.

An asyncio lock can be used to guarantee exclusive access to a shared resource.

The preferred way to use a Lock is an `async with`{.interpreted-text role="keyword"} statement:

    lock = asyncio.Lock()

    # ... later
    async with lock:
        # access shared state

which is equivalent to:

    lock = asyncio.Lock()

    # ... later
    await lock.acquire()
    try:
        # access shared state
    finally:
        lock.release()

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: {.method async=""}
acquire()

Acquire the lock.

This method waits until the lock is *unlocked*, sets it to *locked* and returns `True`.

When more than one coroutine is blocked in `acquire`{.interpreted-text role="meth"} waiting for the lock to be unlocked, only one coroutine eventually proceeds.

Acquiring a lock is *fair*: the coroutine that proceeds will be the first coroutine that started waiting on the lock.
:::

::: method
release()

Release the lock.

When the lock is *locked*, reset it to *unlocked* and return.

If the lock is *unlocked*, a `RuntimeError`{.interpreted-text role="exc"} is raised.
:::

::: method
locked()

Return `True` if the lock is *locked*.
:::
:::::::

## Event

::::::::: Event()
An event object. Not thread-safe.

An asyncio event can be used to notify multiple asyncio tasks that some event has happened.

An Event object manages an internal flag that can be set to *true* with the `~Event.set`{.interpreted-text role="meth"} method and reset to *false* with the `clear`{.interpreted-text role="meth"} method. The `~Event.wait`{.interpreted-text role="meth"} method blocks until the flag is set to *true*. The flag is set to *false* initially.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: {#asyncio_example_sync_event}
Example:

    async def waiter(event):
        print('waiting for it ...')
        await event.wait()
        print('... got it!')

    async def main():
        # Create an Event object.
        event = asyncio.Event()

        # Spawn a Task to wait until 'event' is set.
        waiter_task = asyncio.create_task(waiter(event))

        # Sleep for 1 second and set the event.
        await asyncio.sleep(1)
        event.set()

        # Wait until the waiter task is finished.
        await waiter_task

    asyncio.run(main())
:::

::: {.method async=""}
wait()

Wait until the event is set.

If the event is set, return `True` immediately. Otherwise block until another task calls `~Event.set`{.interpreted-text role="meth"}.
:::

::: method
set()

Set the event.

All tasks waiting for event to be set will be immediately awakened.
:::

::: method
clear()

Clear (unset) the event.

Subsequent tasks awaiting on `~Event.wait`{.interpreted-text role="meth"} will now block until the `~Event.set`{.interpreted-text role="meth"} method is called again.
:::

::: method
is_set()

Return `True` if the event is set.
:::
:::::::::

## Condition

::::::::::: Condition(lock=None)
A Condition object. Not thread-safe.

An asyncio condition primitive can be used by a task to wait for some event to happen and then get exclusive access to a shared resource.

In essence, a Condition object combines the functionality of an `Event`{.interpreted-text role="class"} and a `Lock`{.interpreted-text role="class"}. It is possible to have multiple Condition objects share one Lock, which allows coordinating exclusive access to a shared resource between different tasks interested in particular states of that shared resource.

The optional *lock* argument must be a `Lock`{.interpreted-text role="class"} object or `None`. In the latter case a new Lock object is created automatically.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

The preferred way to use a Condition is an `async with`{.interpreted-text role="keyword"} statement:

    cond = asyncio.Condition()

    # ... later
    async with cond:
        await cond.wait()

which is equivalent to:

    cond = asyncio.Condition()

    # ... later
    await cond.acquire()
    try:
        await cond.wait()
    finally:
        cond.release()

::: {.method async=""}
acquire()

Acquire the underlying lock.

This method waits until the underlying lock is *unlocked*, sets it to *locked* and returns `True`.
:::

::: method
notify(n=1)

Wake up *n* tasks (1 by default) waiting on this condition. If fewer than *n* tasks are waiting they are all awakened.

The lock must be acquired before this method is called and released shortly after. If called with an *unlocked* lock a `RuntimeError`{.interpreted-text role="exc"} error is raised.
:::

::: method
locked()

Return `True` if the underlying lock is acquired.
:::

::: method
notify_all()

Wake up all tasks waiting on this condition.

This method acts like `notify`{.interpreted-text role="meth"}, but wakes up all waiting tasks.

The lock must be acquired before this method is called and released shortly after. If called with an *unlocked* lock a `RuntimeError`{.interpreted-text role="exc"} error is raised.
:::

::: method
release()

Release the underlying lock.

When invoked on an unlocked lock, a `RuntimeError`{.interpreted-text role="exc"} is raised.
:::

::: {.method async=""}
wait()

Wait until notified.

If the calling task has not acquired the lock when this method is called, a `RuntimeError`{.interpreted-text role="exc"} is raised.

This method releases the underlying lock, and then blocks until it is awakened by a `notify`{.interpreted-text role="meth"} or `notify_all`{.interpreted-text role="meth"} call. Once awakened, the Condition re-acquires its lock and this method returns `True`.

Note that a task *may* return from this call spuriously, which is why the caller should always re-check the state and be prepared to `~Condition.wait`{.interpreted-text role="meth"} again. For this reason, you may prefer to use `~Condition.wait_for`{.interpreted-text role="meth"} instead.
:::

::: {.method async=""}
wait_for(predicate)

Wait until a predicate becomes *true*.

The predicate must be a callable which result will be interpreted as a boolean value. The method will repeatedly `~Condition.wait`{.interpreted-text role="meth"} until the predicate evaluates to *true*. The final value is the return value.
:::
:::::::::::

## Semaphore

::::::: Semaphore(value=1)
A Semaphore object. Not thread-safe.

A semaphore manages an internal counter which is decremented by each `acquire`{.interpreted-text role="meth"} call and incremented by each `release`{.interpreted-text role="meth"} call. The counter can never go below zero; when `acquire`{.interpreted-text role="meth"} finds that it is zero, it blocks, waiting until some task calls `release`{.interpreted-text role="meth"}.

The optional *value* argument gives the initial value for the internal counter (`1` by default). If the given value is less than `0` a `ValueError`{.interpreted-text role="exc"} is raised.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

The preferred way to use a Semaphore is an `async with`{.interpreted-text role="keyword"} statement:

    sem = asyncio.Semaphore(10)

    # ... later
    async with sem:
        # work with shared resource

which is equivalent to:

    sem = asyncio.Semaphore(10)

    # ... later
    await sem.acquire()
    try:
        # work with shared resource
    finally:
        sem.release()

::: {.method async=""}
acquire()

Acquire a semaphore.

If the internal counter is greater than zero, decrement it by one and return `True` immediately. If it is zero, wait until a `release`{.interpreted-text role="meth"} is called and return `True`.
:::

::: method
locked()

Returns `True` if semaphore can not be acquired immediately.
:::

::: method
release()

Release a semaphore, incrementing the internal counter by one. Can wake up a task waiting to acquire the semaphore.

Unlike `BoundedSemaphore`{.interpreted-text role="class"}, `Semaphore`{.interpreted-text role="class"} allows making more `release()` calls than `acquire()` calls.
:::
:::::::

## BoundedSemaphore

:::: BoundedSemaphore(value=1)
A bounded semaphore object. Not thread-safe.

Bounded Semaphore is a version of `Semaphore`{.interpreted-text role="class"} that raises a `ValueError`{.interpreted-text role="exc"} in `~Semaphore.release`{.interpreted-text role="meth"} if it increases the internal counter above the initial *value*.

::: versionchanged
3.10 Removed the *loop* parameter.
:::
::::

## Barrier

::::::::::: Barrier(parties)
A barrier object. Not thread-safe.

A barrier is a simple synchronization primitive that allows to block until *parties* number of tasks are waiting on it. Tasks can wait on the `~Barrier.wait`{.interpreted-text role="meth"} method and would be blocked until the specified number of tasks end up waiting on `~Barrier.wait`{.interpreted-text role="meth"}. At that point all of the waiting tasks would unblock simultaneously.

`async with`{.interpreted-text role="keyword"} can be used as an alternative to awaiting on `~Barrier.wait`{.interpreted-text role="meth"}.

The barrier can be reused any number of times.

::: {#asyncio_example_barrier}
Example:

    async def example_barrier():
       # barrier with 3 parties
       b = asyncio.Barrier(3)

       # create 2 new waiting tasks
       asyncio.create_task(b.wait())
       asyncio.create_task(b.wait())

       await asyncio.sleep(0)
       print(b)

       # The third .wait() call passes the barrier
       await b.wait()
       print(b)
       print("barrier passed")

       await asyncio.sleep(0)
       print(b)

    asyncio.run(example_barrier())
:::

Result of this example is:

    <asyncio.locks.Barrier object at 0x... [filling, waiters:2/3]>
    <asyncio.locks.Barrier object at 0x... [draining, waiters:0/3]>
    barrier passed
    <asyncio.locks.Barrier object at 0x... [filling, waiters:0/3]>

::: versionadded
3.11
:::

::: {.method async=""}
wait()

Pass the barrier. When all the tasks party to the barrier have called this function, they are all unblocked simultaneously.

When a waiting or blocked task in the barrier is cancelled, this task exits the barrier which stays in the same state. If the state of the barrier is \"filling\", the number of waiting task decreases by 1.

The return value is an integer in the range of 0 to `parties-1`, different for each task. This can be used to select a task to do some special housekeeping, e.g.:

    ...
    async with barrier as position:
       if position == 0:
          # Only one task prints this
          print('End of *draining phase*')

This method may raise a `BrokenBarrierError`{.interpreted-text role="class"} exception if the barrier is broken or reset while a task is waiting. It could raise a `CancelledError`{.interpreted-text role="exc"} if a task is cancelled.
:::

::: {.method async=""}
reset()

Return the barrier to the default, empty state. Any tasks waiting on it will receive the `BrokenBarrierError`{.interpreted-text role="class"} exception.

If a barrier is broken it may be better to just leave it and create a new one.
:::

::: {.method async=""}
abort()

Put the barrier into a broken state. This causes any active or future calls to `~Barrier.wait`{.interpreted-text role="meth"} to fail with the `BrokenBarrierError`{.interpreted-text role="class"}. Use this for example if one of the tasks needs to abort, to avoid infinite waiting tasks.
:::

::: attribute
parties

The number of tasks required to pass the barrier.
:::

::: attribute
n_waiting

The number of tasks currently waiting in the barrier while filling.
:::

::: attribute
broken

A boolean that is `True` if the barrier is in the broken state.
:::
:::::::::::

::: exception
BrokenBarrierError

This exception, a subclass of `RuntimeError`{.interpreted-text role="exc"}, is raised when the `Barrier`{.interpreted-text role="class"} object is reset or broken.
:::

------------------------------------------------------------------------

::: versionchanged
3.9

Acquiring a lock using `await lock` or `yield from lock` and/or `with`{.interpreted-text role="keyword"} statement (`with await lock`, `with (yield from lock)`) was removed. Use `async with lock` instead.
:::
