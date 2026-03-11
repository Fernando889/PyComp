::: currentmodule
asyncio
:::

# Queues {#asyncio-queues}

**Source code:** `Lib/asyncio/queues.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

asyncio queues are designed to be similar to classes of the `queue`{.interpreted-text role="mod"} module. Although asyncio queues are not thread-safe, they are designed to be used specifically in async/await code.

Note that methods of asyncio queues don\'t have a *timeout* parameter; use `asyncio.wait_for`{.interpreted-text role="func"} function to do queue operations with a timeout.

See also the [Examples](#examples) section below.

## Queue

:::::::::::::::: Queue(maxsize=0)
A first in, first out (FIFO) queue.

If *maxsize* is less than or equal to zero, the queue size is infinite. If it is an integer greater than `0`, then `await put()` blocks when the queue reaches *maxsize* until an item is removed by `get`{.interpreted-text role="meth"}.

Unlike the standard library threading `queue`{.interpreted-text role="mod"}, the size of the queue is always known and can be returned by calling the `qsize`{.interpreted-text role="meth"} method.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

This class is `not thread safe <asyncio-multithreading>`{.interpreted-text role="ref"}.

::: attribute
maxsize

Number of items allowed in the queue.
:::

::: method
empty()

Return `True` if the queue is empty, `False` otherwise.
:::

::: method
full()

Return `True` if there are `maxsize`{.interpreted-text role="attr"} items in the queue.

If the queue was initialized with `maxsize=0` (the default), then `full`{.interpreted-text role="meth"} never returns `True`.
:::

::: {.method async=""}
get()

Remove and return an item from the queue. If queue is empty, wait until an item is available.

Raises `QueueShutDown`{.interpreted-text role="exc"} if the queue has been shut down and is empty, or if the queue has been shut down immediately.
:::

::: method
get_nowait()

Return an item if one is immediately available, else raise `QueueEmpty`{.interpreted-text role="exc"}.
:::

::: {.method async=""}
join()

Block until all items in the queue have been received and processed.

The count of unfinished tasks goes up whenever an item is added to the queue. The count goes down whenever a consumer coroutine calls `task_done`{.interpreted-text role="meth"} to indicate that the item was retrieved and all work on it is complete. When the count of unfinished tasks drops to zero, `join`{.interpreted-text role="meth"} unblocks.
:::

::: {.method async=""}
put(item)

Put an item into the queue. If the queue is full, wait until a free slot is available before adding the item.

Raises `QueueShutDown`{.interpreted-text role="exc"} if the queue has been shut down.
:::

::: method
put_nowait(item)

Put an item into the queue without blocking.

If no free slot is immediately available, raise `QueueFull`{.interpreted-text role="exc"}.
:::

::: method
qsize()

Return the number of items in the queue.
:::

:::: method
shutdown(immediate=False)

Put a `Queue`{.interpreted-text role="class"} instance into a shutdown mode.

The queue can no longer grow. Future calls to `~Queue.put`{.interpreted-text role="meth"} raise `QueueShutDown`{.interpreted-text role="exc"}. Currently blocked callers of `~Queue.put`{.interpreted-text role="meth"} will be unblocked and will raise `QueueShutDown`{.interpreted-text role="exc"} in the formerly awaiting task.

If *immediate* is false (the default), the queue can be wound down normally with `~Queue.get`{.interpreted-text role="meth"} calls to extract tasks that have already been loaded.

And if `~Queue.task_done`{.interpreted-text role="meth"} is called for each remaining task, a pending `~Queue.join`{.interpreted-text role="meth"} will be unblocked normally.

Once the queue is empty, future calls to `~Queue.get`{.interpreted-text role="meth"} will raise `QueueShutDown`{.interpreted-text role="exc"}.

If *immediate* is true, the queue is terminated immediately. The queue is drained to be completely empty and the count of unfinished tasks is reduced by the number of tasks drained. If unfinished tasks is zero, callers of `~Queue.join`{.interpreted-text role="meth"} are unblocked. Also, blocked callers of `~Queue.get`{.interpreted-text role="meth"} are unblocked and will raise `QueueShutDown`{.interpreted-text role="exc"} because the queue is empty.

Use caution when using `~Queue.join`{.interpreted-text role="meth"} with *immediate* set to true. This unblocks the join even when no work has been done on the tasks, violating the usual invariant for joining a queue.

::: versionadded
3.13
:::
::::

::: method
task_done()

Indicate that a formerly enqueued work item is complete.

Used by queue consumers. For each `~Queue.get`{.interpreted-text role="meth"} used to fetch a work item, a subsequent call to `task_done`{.interpreted-text role="meth"} tells the queue that the processing on the work item is complete.

If a `join`{.interpreted-text role="meth"} is currently blocking, it will resume when all items have been processed (meaning that a `task_done`{.interpreted-text role="meth"} call was received for every item that had been `~Queue.put`{.interpreted-text role="meth"} into the queue).

Raises `ValueError`{.interpreted-text role="exc"} if called more times than there were items placed in the queue.
:::
::::::::::::::::

## Priority Queue

::: PriorityQueue
A variant of `Queue`{.interpreted-text role="class"}; retrieves entries in priority order (lowest first).

Entries are typically tuples of the form `(priority_number, data)`.
:::

## LIFO Queue

::: LifoQueue
A variant of `Queue`{.interpreted-text role="class"} that retrieves most recently added entries first (last in, first out).
:::

## Exceptions

::: exception
QueueEmpty

This exception is raised when the `~Queue.get_nowait`{.interpreted-text role="meth"} method is called on an empty queue.
:::

::: exception
QueueFull

Exception raised when the `~Queue.put_nowait`{.interpreted-text role="meth"} method is called on a queue that has reached its *maxsize*.
:::

:::: exception
QueueShutDown

Exception raised when `~Queue.put`{.interpreted-text role="meth"} or `~Queue.get`{.interpreted-text role="meth"} is called on a queue which has been shut down.

::: versionadded
3.13
:::
::::

## Examples

::: {#asyncio_example_queue_dist}
Queues can be used to distribute workload between several concurrent tasks:

    import asyncio
    import random
    import time


    async def worker(name, queue):
        while True:
            # Get a "work item" out of the queue.
            sleep_for = await queue.get()

            # Sleep for the "sleep_for" seconds.
            await asyncio.sleep(sleep_for)

            # Notify the queue that the "work item" has been processed.
            queue.task_done()

            print(f'{name} has slept for {sleep_for:.2f} seconds')


    async def main():
        # Create a queue that we will use to store our "workload".
        queue = asyncio.Queue()

        # Generate random timings and put them into the queue.
        total_sleep_time = 0
        for _ in range(20):
            sleep_for = random.uniform(0.05, 1.0)
            total_sleep_time += sleep_for
            queue.put_nowait(sleep_for)

        # Create three worker tasks to process the queue concurrently.
        tasks = []
        for i in range(3):
            task = asyncio.create_task(worker(f'worker-{i}', queue))
            tasks.append(task)

        # Wait until the queue is fully processed.
        started_at = time.monotonic()
        await queue.join()
        total_slept_for = time.monotonic() - started_at

        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)

        print('====')
        print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
        print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


    asyncio.run(main())
:::
