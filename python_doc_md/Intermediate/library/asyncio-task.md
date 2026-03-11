::: currentmodule
asyncio
:::

# Coroutines and Tasks

This section outlines high-level asyncio APIs to work with coroutines and Tasks.

::: {.contents depth="1" local=""}
:::

## Coroutines {#coroutine}

**Source code:** `Lib/asyncio/coroutines.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

`Coroutines <coroutine>`{.interpreted-text role="term"} declared with the async/await syntax is the preferred way of writing asyncio applications. For example, the following snippet of code prints \"hello\", waits 1 second, and then prints \"world\":

    >>> import asyncio

    >>> async def main():
    ...     print('hello')
    ...     await asyncio.sleep(1)
    ...     print('world')

    >>> asyncio.run(main())
    hello
    world

Note that simply calling a coroutine will not schedule it to be executed:

    >>> main()
    <coroutine object main at 0x1053bb7c8>

To actually run a coroutine, asyncio provides the following mechanisms:

- The `asyncio.run`{.interpreted-text role="func"} function to run the top-level entry point \"main()\" function (see the above example.)

- Awaiting on a coroutine. The following snippet of code will print \"hello\" after waiting for 1 second, and then print \"world\" after waiting for *another* 2 seconds:

      import asyncio
      import time

      async def say_after(delay, what):
          await asyncio.sleep(delay)
          print(what)

      async def main():
          print(f"started at {time.strftime('%X')}")

          await say_after(1, 'hello')
          await say_after(2, 'world')

          print(f"finished at {time.strftime('%X')}")

      asyncio.run(main())

  Expected output:

      started at 17:13:52
      hello
      world
      finished at 17:13:55

- The `asyncio.create_task`{.interpreted-text role="func"} function to run coroutines concurrently as asyncio `Tasks <Task>`{.interpreted-text role="class"}.

  Let\'s modify the above example and run two `say_after` coroutines *concurrently*:

      async def main():
          task1 = asyncio.create_task(
              say_after(1, 'hello'))

          task2 = asyncio.create_task(
              say_after(2, 'world'))

          print(f"started at {time.strftime('%X')}")

          # Wait until both tasks are completed (should take
          # around 2 seconds.)
          await task1
          await task2

          print(f"finished at {time.strftime('%X')}")

  Note that expected output now shows that the snippet runs 1 second faster than before:

      started at 17:14:32
      hello
      world
      finished at 17:14:34

- The `asyncio.TaskGroup`{.interpreted-text role="class"} class provides a more modern alternative to `create_task`{.interpreted-text role="func"}. Using this API, the last example becomes:

      async def main():
          async with asyncio.TaskGroup() as tg:
              task1 = tg.create_task(
                  say_after(1, 'hello'))

              task2 = tg.create_task(
                  say_after(2, 'world'))

              print(f"started at {time.strftime('%X')}")

          # The await is implicit when the context manager exits.

          print(f"finished at {time.strftime('%X')}")

  The timing and output should be the same as for the previous version.

  ::: versionadded
  3.11 `asyncio.TaskGroup`{.interpreted-text role="class"}.
  :::

## Awaitables {#asyncio-awaitables}

We say that an object is an **awaitable** object if it can be used in an `await`{.interpreted-text role="keyword"} expression. Many asyncio APIs are designed to accept awaitables.

There are three main types of *awaitable* objects: **coroutines**, **Tasks**, and **Futures**.

**Coroutines**

Python coroutines are *awaitables* and therefore can be awaited from other coroutines:

    import asyncio

    async def nested():
        return 42

    async def main():
        # Nothing happens if we just call "nested()".
        # A coroutine object is created but not awaited,
        # so it *won't run at all*.
        nested()  # will raise a "RuntimeWarning".

        # Let's do it differently now and await it:
        print(await nested())  # will print "42".

    asyncio.run(main())

:::: important
::: title
Important
:::

In this documentation the term \"coroutine\" can be used for two closely related concepts:

- a *coroutine function*: an `async def`{.interpreted-text role="keyword"} function;
- a *coroutine object*: an object returned by calling a *coroutine function*.
::::

**Tasks**

*Tasks* are used to schedule coroutines *concurrently*.

When a coroutine is wrapped into a *Task* with functions like `asyncio.create_task`{.interpreted-text role="func"} the coroutine is automatically scheduled to run soon:

    import asyncio

    async def nested():
        return 42

    async def main():
        # Schedule nested() to run soon concurrently
        # with "main()".
        task = asyncio.create_task(nested())

        # "task" can now be used to cancel "nested()", or
        # can simply be awaited to wait until it is complete:
        await task

    asyncio.run(main())

**Futures**

A `Future`{.interpreted-text role="class"} is a special **low-level** awaitable object that represents an **eventual result** of an asynchronous operation.

When a Future object is *awaited* it means that the coroutine will wait until the Future is resolved in some other place.

Future objects in asyncio are needed to allow callback-based code to be used with async/await.

Normally **there is no need** to create Future objects at the application level code.

Future objects, sometimes exposed by libraries and some asyncio APIs, can be awaited:

    async def main():
        await function_that_returns_a_future_object()

        # this is also valid:
        await asyncio.gather(
            function_that_returns_a_future_object(),
            some_python_coroutine()
        )

A good example of a low-level function that returns a Future object is `loop.run_in_executor`{.interpreted-text role="meth"}.

## Creating Tasks

**Source code:** `Lib/asyncio/tasks.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

::::::::::: function
create_task(coro, *, name=None, context=None, eager_start=None,*\*kwargs)

Wrap the *coro* `coroutine <coroutine>`{.interpreted-text role="ref"} into a `Task`{.interpreted-text role="class"} and schedule its execution. Return the Task object.

The full function signature is largely the same as that of the `Task`{.interpreted-text role="class"} constructor (or factory) - all of the keyword arguments to this function are passed through to that interface.

An optional keyword-only *context* argument allows specifying a custom `contextvars.Context`{.interpreted-text role="class"} for the *coro* to run in. The current context copy is created when no *context* is provided.

An optional keyword-only *eager_start* argument allows specifying if the task should execute eagerly during the call to create_task, or be scheduled later. If *eager_start* is not passed the mode set by `loop.set_task_factory`{.interpreted-text role="meth"} will be used.

The task is executed in the loop returned by `get_running_loop`{.interpreted-text role="func"}, `RuntimeError`{.interpreted-text role="exc"} is raised if there is no running loop in current thread.

:::: note
::: title
Note
:::

`asyncio.TaskGroup.create_task`{.interpreted-text role="meth"} is a new alternative leveraging structural concurrency; it allows for waiting for a group of related tasks with strong safety guarantees.
::::

:::: important
::: title
Important
:::

Save a reference to the result of this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks. A task that isn\'t referenced elsewhere may get garbage collected at any time, even before it\'s done. For reliable \"fire-and-forget\" background tasks, gather them in a collection:

    background_tasks = set()

    for i in range(10):
        task = asyncio.create_task(some_coro(param=i))

        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)

        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)
::::

::: versionadded
3.7
:::

::: versionchanged
3.8 Added the *name* parameter.
:::

::: versionchanged
3.11 Added the *context* parameter.
:::

::: versionchanged
3.14 Added the *eager_start* parameter by passing on all *kwargs*.
:::
:::::::::::

## Task Cancellation

Tasks can easily and safely be cancelled. When a task is cancelled, `asyncio.CancelledError`{.interpreted-text role="exc"} will be raised in the task at the next opportunity.

It is recommended that coroutines use `try/finally` blocks to robustly perform clean-up logic. In case `asyncio.CancelledError`{.interpreted-text role="exc"} is explicitly caught, it should generally be propagated when clean-up is complete. `asyncio.CancelledError`{.interpreted-text role="exc"} directly subclasses `BaseException`{.interpreted-text role="exc"} so most code will not need to be aware of it.

The asyncio components that enable structured concurrency, like `asyncio.TaskGroup`{.interpreted-text role="class"} and `asyncio.timeout`{.interpreted-text role="func"}, are implemented using cancellation internally and might misbehave if a coroutine swallows `asyncio.CancelledError`{.interpreted-text role="exc"}. Similarly, user code should not generally call `uncancel <asyncio.Task.uncancel>`{.interpreted-text role="meth"}. However, in cases when suppressing `asyncio.CancelledError`{.interpreted-text role="exc"} is truly desired, it is necessary to also call `uncancel()` to completely remove the cancellation state.

## Task Groups {#taskgroups}

Task groups combine a task creation API with a convenient and reliable way to wait for all tasks in the group to finish.

::::::: TaskGroup()
An `asynchronous context manager <async-context-managers>`{.interpreted-text role="ref"} holding a group of tasks. Tasks can be added to the group using `create_task`{.interpreted-text role="meth"}. All tasks are awaited when the context manager exits.

::: versionadded
3.11
:::

::::: method
create_task(coro, *, name=None, context=None, eager_start=None,*\*kwargs)

Create a task in this task group. The signature matches that of `asyncio.create_task`{.interpreted-text role="func"}. If the task group is inactive (e.g. not yet entered, already finished, or in the process of shutting down), we will close the given `coro`.

::: versionchanged
3.13

Close the given coroutine if the task group is not active.
:::

::: versionchanged
3.14

Passes on all *kwargs* to `loop.create_task`{.interpreted-text role="meth"}
:::
:::::
:::::::

Example:

    async def main():
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(some_coro(...))
            task2 = tg.create_task(another_coro(...))
        print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")

The `async with` statement will wait for all tasks in the group to finish. While waiting, new tasks may still be added to the group (for example, by passing `tg` into one of the coroutines and calling `tg.create_task()` in that coroutine). Once the last task has finished and the `async with` block is exited, no new tasks may be added to the group.

The first time any of the tasks belonging to the group fails with an exception other than `asyncio.CancelledError`{.interpreted-text role="exc"}, the remaining tasks in the group are cancelled. No further tasks can then be added to the group. At this point, if the body of the `async with` statement is still active (i.e., `~object.__aexit__`{.interpreted-text role="meth"} hasn\'t been called yet), the task directly containing the `async with` statement is also cancelled. The resulting `asyncio.CancelledError`{.interpreted-text role="exc"} will interrupt an `await`, but it will not bubble out of the containing `async with` statement.

Once all tasks have finished, if any tasks have failed with an exception other than `asyncio.CancelledError`{.interpreted-text role="exc"}, those exceptions are combined in an `ExceptionGroup`{.interpreted-text role="exc"} or `BaseExceptionGroup`{.interpreted-text role="exc"} (as appropriate; see their documentation) which is then raised.

Two base exceptions are treated specially: If any task fails with `KeyboardInterrupt`{.interpreted-text role="exc"} or `SystemExit`{.interpreted-text role="exc"}, the task group still cancels the remaining tasks and waits for them, but then the initial `KeyboardInterrupt`{.interpreted-text role="exc"} or `SystemExit`{.interpreted-text role="exc"} is re-raised instead of `ExceptionGroup`{.interpreted-text role="exc"} or `BaseExceptionGroup`{.interpreted-text role="exc"}.

If the body of the `async with` statement exits with an exception (so `~object.__aexit__`{.interpreted-text role="meth"} is called with an exception set), this is treated the same as if one of the tasks failed: the remaining tasks are cancelled and then waited for, and non-cancellation exceptions are grouped into an exception group and raised. The exception passed into `~object.__aexit__`{.interpreted-text role="meth"}, unless it is `asyncio.CancelledError`{.interpreted-text role="exc"}, is also included in the exception group. The same special case is made for `KeyboardInterrupt`{.interpreted-text role="exc"} and `SystemExit`{.interpreted-text role="exc"} as in the previous paragraph.

Task groups are careful not to mix up the internal cancellation used to \"wake up\" their `~object.__aexit__`{.interpreted-text role="meth"} with cancellation requests for the task in which they are running made by other parties. In particular, when one task group is syntactically nested in another, and both experience an exception in one of their child tasks simultaneously, the inner task group will process its exceptions, and then the outer task group will receive another cancellation and process its own exceptions.

In the case where a task group is cancelled externally and also must raise an `ExceptionGroup`{.interpreted-text role="exc"}, it will call the parent task\'s `~asyncio.Task.cancel`{.interpreted-text role="meth"} method. This ensures that a `asyncio.CancelledError`{.interpreted-text role="exc"} will be raised at the next `await`{.interpreted-text role="keyword"}, so the cancellation is not lost.

Task groups preserve the cancellation count reported by `asyncio.Task.cancelling`{.interpreted-text role="meth"}.

::: versionchanged
3.13

Improved handling of simultaneous internal and external cancellations and correct preservation of cancellation counts.
:::

### Terminating a Task Group

While terminating a task group is not natively supported by the standard library, termination can be achieved by adding an exception-raising task to the task group and ignoring the raised exception:

``` python
import asyncio
from asyncio import TaskGroup

class TerminateTaskGroup(Exception):
    """Exception raised to terminate a task group."""

async def force_terminate_task_group():
    """Used to force termination of a task group."""
    raise TerminateTaskGroup()

async def job(task_id, sleep_time):
    print(f'Task {task_id}: start')
    await asyncio.sleep(sleep_time)
    print(f'Task {task_id}: done')

async def main():
    try:
        async with TaskGroup() as group:
            # spawn some tasks
            group.create_task(job(1, 0.5))
            group.create_task(job(2, 1.5))
            # sleep for 1 second
            await asyncio.sleep(1)
            # add an exception-raising task to force the group to terminate
            group.create_task(force_terminate_task_group())
    except* TerminateTaskGroup:
        pass

asyncio.run(main())
```

Expected output:

``` text
Task 1: start
Task 2: start
Task 1: done
```

## Sleeping

:::::: {.function async=""}
sleep(delay, result=None)

Block for *delay* seconds.

If *result* is provided, it is returned to the caller when the coroutine completes.

`sleep()` always suspends the current task, allowing other tasks to run.

Setting the delay to 0 provides an optimized path to allow other tasks to run. This can be used by long-running functions to avoid blocking the event loop for the full duration of the function call.

::: {#asyncio_example_sleep}
Example of coroutine displaying the current date every second for 5 seconds:

    import asyncio
    import datetime

    async def display_date():
        loop = asyncio.get_running_loop()
        end_time = loop.time() + 5.0
        while True:
            print(datetime.datetime.now())
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)

    asyncio.run(display_date())
:::

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: versionchanged
3.13 Raises `ValueError`{.interpreted-text role="exc"} if *delay* is `~math.nan`{.interpreted-text role="data"}.
:::
::::::

## Running Tasks Concurrently

::::::::::: awaitablefunction
gather(\*aws, return_exceptions=False)

Run `awaitable objects <asyncio-awaitables>`{.interpreted-text role="ref"} in the *aws* sequence *concurrently*.

If any awaitable in *aws* is a coroutine, it is automatically scheduled as a Task.

If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in *aws*.

If *return_exceptions* is `False` (default), the first raised exception is immediately propagated to the task that awaits on `gather()`. Other awaitables in the *aws* sequence **won\'t be cancelled** and will continue to run.

If *return_exceptions* is `True`, exceptions are treated the same as successful results, and aggregated in the result list.

If `gather()` is *cancelled*, all submitted awaitables (that have not completed yet) are also *cancelled*.

If any Task or Future from the *aws* sequence is *cancelled*, it is treated as if it raised `CancelledError`{.interpreted-text role="exc"} \-- the `gather()` call is **not** cancelled in this case. This is to prevent the cancellation of one submitted Task/Future to cause other Tasks/Futures to be cancelled.

:::: note
::: title
Note
:::

A new alternative to create and run tasks concurrently and wait for their completion is `asyncio.TaskGroup`{.interpreted-text role="class"}. *TaskGroup* provides stronger safety guarantees than *gather* for scheduling a nesting of subtasks: if a task (or a subtask, a task scheduled by a task) raises an exception, *TaskGroup* will, while *gather* will not, cancel the remaining scheduled tasks).
::::

::: {#asyncio_example_gather}
Example:

    import asyncio

    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({number}), currently i={i}...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")
        return f

    async def main():
        # Schedule three calls *concurrently*:
        L = await asyncio.gather(
            factorial("A", 2),
            factorial("B", 3),
            factorial("C", 4),
        )
        print(L)

    asyncio.run(main())

    # Expected output:
    #
    #     Task A: Compute factorial(2), currently i=2...
    #     Task B: Compute factorial(3), currently i=2...
    #     Task C: Compute factorial(4), currently i=2...
    #     Task A: factorial(2) = 2
    #     Task B: Compute factorial(3), currently i=3...
    #     Task C: Compute factorial(4), currently i=3...
    #     Task B: factorial(3) = 6
    #     Task C: Compute factorial(4), currently i=4...
    #     Task C: factorial(4) = 24
    #     [2, 6, 24]
:::

:::: note
::: title
Note
:::

If *return_exceptions* is false, cancelling gather() after it has been marked done won\'t cancel any submitted awaitables. For instance, gather can be marked done after propagating an exception to the caller, therefore, calling `gather.cancel()` after catching an exception (raised by one of the awaitables) from gather won\'t cancel any other awaitables.
::::

::: versionchanged
3.7 If the *gather* itself is cancelled, the cancellation is propagated regardless of *return_exceptions*.
:::

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: deprecated
3.10 Deprecation warning is emitted if no positional arguments are provided or not all positional arguments are Future-like objects and there is no running event loop.
:::
:::::::::::

## Eager Task Factory

:::::: function
eager_task_factory(loop, coro, \*, name=None, context=None)

A task factory for eager task execution.

When using this factory (via `loop.set_task_factory(asyncio.eager_task_factory) <loop.set_task_factory>`{.interpreted-text role="meth"}), coroutines begin execution synchronously during `Task`{.interpreted-text role="class"} construction. Tasks are only scheduled on the event loop if they block. This can be a performance improvement as the overhead of loop scheduling is avoided for coroutines that complete synchronously.

A common example where this is beneficial is coroutines which employ caching or memoization to avoid actual I/O when possible.

:::: note
::: title
Note
:::

Immediate execution of the coroutine is a semantic change. If the coroutine returns or raises, the task is never scheduled to the event loop. If the coroutine execution blocks, the task is scheduled to the event loop. This change may introduce behavior changes to existing applications. For example, the application\'s task execution order is likely to change.
::::

::: versionadded
3.12
:::
::::::

:::: function
create_eager_task_factory(custom_task_constructor)

Create an eager task factory, similar to `eager_task_factory`{.interpreted-text role="func"}, using the provided *custom_task_constructor* when creating a new task instead of the default `Task`{.interpreted-text role="class"}.

*custom_task_constructor* must be a *callable* with the signature matching the signature of `Task.__init__ <Task>`{.interpreted-text role="class"}. The callable must return a `asyncio.Task`{.interpreted-text role="class"}-compatible object.

This function returns a *callable* intended to be used as a task factory of an event loop via `loop.set_task_factory(factory) <loop.set_task_factory>`{.interpreted-text role="meth"}).

::: versionadded
3.12
:::
::::

## Shielding From Cancellation

::::::: awaitablefunction
shield(aw)

Protect an `awaitable object <asyncio-awaitables>`{.interpreted-text role="ref"} from being `cancelled <Task.cancel>`{.interpreted-text role="meth"}.

If *aw* is a coroutine it is automatically scheduled as a Task.

The statement:

    task = asyncio.create_task(something())
    res = await shield(task)

is equivalent to:

    res = await something()

*except* that if the coroutine containing it is cancelled, the Task running in `something()` is not cancelled. From the point of view of `something()`, the cancellation did not happen. Although its caller is still cancelled, so the \"await\" expression still raises a `CancelledError`{.interpreted-text role="exc"}.

If `something()` is cancelled by other means (i.e. from within itself) that would also cancel `shield()`.

If it is desired to completely ignore cancellation (not recommended) the `shield()` function should be combined with a try/except clause, as follows:

    task = asyncio.create_task(something())
    try:
        res = await shield(task)
    except CancelledError:
        res = None

:::: important
::: title
Important
:::

Save a reference to tasks passed to this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks. A task that isn\'t referenced elsewhere may get garbage collected at any time, even before it\'s done.
::::

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: deprecated
3.10 Deprecation warning is emitted if *aw* is not Future-like object and there is no running event loop.
:::
:::::::

## Timeouts

::::::: function
timeout(delay)

Return an `asynchronous context manager <async-context-managers>`{.interpreted-text role="ref"} that can be used to limit the amount of time spent waiting on something.

*delay* can either be `None`, or a float/int number of seconds to wait. If *delay* is `None`, no time limit will be applied; this can be useful if the delay is unknown when the context manager is created.

In either case, the context manager can be rescheduled after creation using `Timeout.reschedule`{.interpreted-text role="meth"}.

Example:

    async def main():
        async with asyncio.timeout(10):
            await long_running_task()

If `long_running_task` takes more than 10 seconds to complete, the context manager will cancel the current task and handle the resulting `asyncio.CancelledError`{.interpreted-text role="exc"} internally, transforming it into a `TimeoutError`{.interpreted-text role="exc"} which can be caught and handled.

:::: note
::: title
Note
:::

The `asyncio.timeout`{.interpreted-text role="func"} context manager is what transforms the `asyncio.CancelledError`{.interpreted-text role="exc"} into a `TimeoutError`{.interpreted-text role="exc"}, which means the `TimeoutError`{.interpreted-text role="exc"} can only be caught *outside* of the context manager.
::::

Example of catching `TimeoutError`{.interpreted-text role="exc"}:

    async def main():
        try:
            async with asyncio.timeout(10):
                await long_running_task()
        except TimeoutError:
            print("The long operation timed out, but we've handled it.")

        print("This statement will run regardless.")

The context manager produced by `asyncio.timeout`{.interpreted-text role="func"} can be rescheduled to a different deadline and inspected.

::: Timeout(when)
An `asynchronous context manager <async-context-managers>`{.interpreted-text role="ref"} for cancelling overdue coroutines.

Prefer using `asyncio.timeout`{.interpreted-text role="func"} or `asyncio.timeout_at`{.interpreted-text role="func"} rather than instantiating `!Timeout`{.interpreted-text role="class"} directly.

`when` should be an absolute time at which the context should time out, as measured by the event loop\'s clock:

- If `when` is `None`, the timeout will never trigger.
- If `when < loop.time()`, the timeout will trigger on the next iteration of the event loop.

> ::: method
> when() -\> float \| None
>
> Return the current deadline, or `None` if the current deadline is not set.
> :::
>
> ::: method
> reschedule(when: float \| None)
>
> Reschedule the timeout.
> :::
>
> ::: method
> expired() -\> bool
>
> Return whether the context manager has exceeded its deadline (expired).
> :::
:::

Example:

    async def main():
        try:
            # We do not know the timeout when starting, so we pass ``None``.
            async with asyncio.timeout(None) as cm:
                # We know the timeout now, so we reschedule it.
                new_deadline = get_running_loop().time() + 10
                cm.reschedule(new_deadline)

                await long_running_task()
        except TimeoutError:
            pass

        if cm.expired():
            print("Looks like we haven't finished on time.")

Timeout context managers can be safely nested.

::: versionadded
3.11
:::
:::::::

:::: function
timeout_at(when)

Similar to `asyncio.timeout`{.interpreted-text role="func"}, except *when* is the absolute time to stop waiting, or `None`.

Example:

    async def main():
        loop = get_running_loop()
        deadline = loop.time() + 20
        try:
            async with asyncio.timeout_at(deadline):
                await long_running_task()
        except TimeoutError:
            print("The long operation timed out, but we've handled it.")

        print("This statement will run regardless.")

::: versionadded
3.11
:::
::::

::::::: {.function async=""}
wait_for(aw, timeout)

Wait for the *aw* `awaitable <asyncio-awaitables>`{.interpreted-text role="ref"} to complete with a timeout.

If *aw* is a coroutine it is automatically scheduled as a Task.

*timeout* can either be `None` or a float or int number of seconds to wait for. If *timeout* is `None`, block until the future completes.

If a timeout occurs, it cancels the task and raises `TimeoutError`{.interpreted-text role="exc"}.

To avoid the task `cancellation <Task.cancel>`{.interpreted-text role="meth"}, wrap it in `shield`{.interpreted-text role="func"}.

The function will wait until the future is actually cancelled, so the total wait time may exceed the *timeout*. If an exception happens during cancellation, it is propagated.

If the wait is cancelled, the future *aw* is also cancelled.

::: {#asyncio_example_waitfor}
Example:

    async def eternity():
        # Sleep for one hour
        await asyncio.sleep(3600)
        print('yay!')

    async def main():
        # Wait for at most 1 second
        try:
            await asyncio.wait_for(eternity(), timeout=1.0)
        except TimeoutError:
            print('timeout!')

    asyncio.run(main())

    # Expected output:
    #
    #     timeout!
:::

::: versionchanged
3.7 When *aw* is cancelled due to a timeout, `wait_for` waits for *aw* to be cancelled. Previously, it raised `TimeoutError`{.interpreted-text role="exc"} immediately.
:::

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: versionchanged
3.11 Raises `TimeoutError`{.interpreted-text role="exc"} instead of `asyncio.TimeoutError`{.interpreted-text role="exc"}.
:::
:::::::

## Waiting Primitives

:::::: {.function async=""}
wait(aws, \*, timeout=None, return_when=ALL_COMPLETED)

Run `~asyncio.Future`{.interpreted-text role="class"} and `~asyncio.Task`{.interpreted-text role="class"} instances in the *aws* iterable concurrently and block until the condition specified by *return_when*.

The *aws* iterable must not be empty.

Returns two sets of Tasks/Futures: `(done, pending)`.

Usage:

    done, pending = await asyncio.wait(aws)

*timeout* (a float or int), if specified, can be used to control the maximum number of seconds to wait before returning.

Note that this function does not raise `TimeoutError`{.interpreted-text role="exc"}. Futures or Tasks that aren\'t done when the timeout occurs are simply returned in the second set.

*return_when* indicates when this function should return. It must be one of the following constants:

+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Constant        | Description                                                                                                                                                                           |
+=================+=======================================================================================================================================================================================+
| ::: data        | The function will return when any future finishes or is cancelled.                                                                                                                    |
| FIRST_COMPLETED |                                                                                                                                                                                       |
| :::             |                                                                                                                                                                                       |
+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data        | The function will return when any future finishes by raising an exception. If no future raises an exception then it is equivalent to `ALL_COMPLETED`{.interpreted-text role="const"}. |
| FIRST_EXCEPTION |                                                                                                                                                                                       |
| :::             |                                                                                                                                                                                       |
+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: data        | The function will return when all futures finish or are cancelled.                                                                                                                    |
| ALL_COMPLETED   |                                                                                                                                                                                       |
| :::             |                                                                                                                                                                                       |
+-----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Unlike `~asyncio.wait_for`{.interpreted-text role="func"}, `wait()` does not cancel the futures when a timeout occurs.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: versionchanged
3.11 Passing coroutine objects to `wait()` directly is forbidden.
:::

::: versionchanged
3.12 Added support for generators yielding tasks.
:::
::::::

::::::: function
as_completed(aws, \*, timeout=None)

Run `awaitable objects <asyncio-awaitables>`{.interpreted-text role="ref"} in the *aws* iterable concurrently. The returned object can be iterated to obtain the results of the awaitables as they finish.

The object returned by `as_completed()` can be iterated as an `asynchronous iterator`{.interpreted-text role="term"} or a plain `iterator`{.interpreted-text role="term"}. When asynchronous iteration is used, the originally-supplied awaitables are yielded if they are tasks or futures. This makes it easy to correlate previously-scheduled tasks with their results. Example:

    ipv4_connect = create_task(open_connection("127.0.0.1", 80))
    ipv6_connect = create_task(open_connection("::1", 80))
    tasks = [ipv4_connect, ipv6_connect]

    async for earliest_connect in as_completed(tasks):
        # earliest_connect is done. The result can be obtained by
        # awaiting it or calling earliest_connect.result()
        reader, writer = await earliest_connect

        if earliest_connect is ipv6_connect:
            print("IPv6 connection established.")
        else:
            print("IPv4 connection established.")

During asynchronous iteration, implicitly-created tasks will be yielded for supplied awaitables that aren\'t tasks or futures.

When used as a plain iterator, each iteration yields a new coroutine that returns the result or raises the exception of the next completed awaitable. This pattern is compatible with Python versions older than 3.13:

    ipv4_connect = create_task(open_connection("127.0.0.1", 80))
    ipv6_connect = create_task(open_connection("::1", 80))
    tasks = [ipv4_connect, ipv6_connect]

    for next_connect in as_completed(tasks):
        # next_connect is not one of the original task objects. It must be
        # awaited to obtain the result value or raise the exception of the
        # awaitable that finishes next.
        reader, writer = await next_connect

A `TimeoutError`{.interpreted-text role="exc"} is raised if the timeout occurs before all awaitables are done. This is raised by the `async for` loop during asynchronous iteration or by the coroutines yielded during plain iteration.

::: versionchanged
3.10 Removed the *loop* parameter.
:::

::: deprecated
3.10 Deprecation warning is emitted if not all awaitable objects in the *aws* iterable are Future-like objects and there is no running event loop.
:::

::: versionchanged
3.12 Added support for generators yielding tasks.
:::

::: versionchanged
3.13 The result can now be used as either an `asynchronous iterator`{.interpreted-text role="term"} or as a plain `iterator`{.interpreted-text role="term"} (previously it was only a plain iterator).
:::
:::::::

## Running in Threads

:::::: {.function async=""}
to_thread(func, /, *args,*\*kwargs)

Asynchronously run function *func* in a separate thread.

Any \*args and \*\*kwargs supplied for this function are directly passed to *func*. Also, the current `contextvars.Context`{.interpreted-text role="class"} is propagated, allowing context variables from the event loop thread to be accessed in the separate thread.

Return a coroutine that can be awaited to get the eventual result of *func*.

This coroutine function is primarily intended to be used for executing IO-bound functions/methods that would otherwise block the event loop if they were run in the main thread. For example:

    def blocking_io():
        print(f"start blocking_io at {time.strftime('%X')}")
        # Note that time.sleep() can be replaced with any blocking
        # IO-bound operation, such as file operations.
        time.sleep(1)
        print(f"blocking_io complete at {time.strftime('%X')}")

    async def main():
        print(f"started main at {time.strftime('%X')}")

        await asyncio.gather(
            asyncio.to_thread(blocking_io),
            asyncio.sleep(1))

        print(f"finished main at {time.strftime('%X')}")


    asyncio.run(main())

    # Expected output:
    #
    # started main at 19:50:53
    # start blocking_io at 19:50:53
    # blocking_io complete at 19:50:54
    # finished main at 19:50:54

Directly calling `blocking_io()` in any coroutine would block the event loop for its duration, resulting in an additional 1 second of run time. Instead, by using `asyncio.to_thread()`, we can run it in a separate thread without blocking the event loop.

:::: note
::: title
Note
:::

Due to the `GIL`{.interpreted-text role="term"}, `asyncio.to_thread()` can typically only be used to make IO-bound functions non-blocking. However, for extension modules that release the GIL or alternative Python implementations that don\'t have one, `asyncio.to_thread()` can also be used for CPU-bound functions.
::::

::: versionadded
3.9
:::
::::::

## Scheduling From Other Threads

:::: function
run_coroutine_threadsafe(coro, loop)

Submit a coroutine to the given event loop. Thread-safe.

Return a `concurrent.futures.Future`{.interpreted-text role="class"} to wait for the result from another OS thread.

This function is meant to be called from a different OS thread than the one where the event loop is running. Example:

    def in_thread(loop: asyncio.AbstractEventLoop) -> None:
        # Run some blocking IO
        pathlib.Path("example.txt").write_text("hello world", encoding="utf8")

        # Create a coroutine
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result(timeout=2) == 3

    async def amain() -> None:
        # Get the running loop
        loop = asyncio.get_running_loop()

        # Run something in a thread
        await asyncio.to_thread(in_thread, loop)

It\'s also possible to run the other way around. Example:

    @contextlib.contextmanager
    def loop_in_thread() -> Generator[asyncio.AbstractEventLoop]:
        loop_fut = concurrent.futures.Future[asyncio.AbstractEventLoop]()
        stop_event = asyncio.Event()

        async def main() -> None:
            loop_fut.set_result(asyncio.get_running_loop())
            await stop_event.wait()

        with concurrent.futures.ThreadPoolExecutor(1) as tpe:
            complete_fut = tpe.submit(asyncio.run, main())
            for fut in concurrent.futures.as_completed((loop_fut, complete_fut)):
                if fut is loop_fut:
                    loop = loop_fut.result()
                    try:
                        yield loop
                    finally:
                        loop.call_soon_threadsafe(stop_event.set)
                else:
                    fut.result()

    # Create a loop in another thread
    with loop_in_thread() as loop:
        # Create a coroutine
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result(timeout=2) == 3

If an exception is raised in the coroutine, the returned Future will be notified. It can also be used to cancel the task in the event loop:

    try:
        result = future.result(timeout)
    except TimeoutError:
        print('The coroutine took too long, cancelling the task...')
        future.cancel()
    except Exception as exc:
        print(f'The coroutine raised an exception: {exc!r}')
    else:
        print(f'The coroutine returned: {result!r}')

See the `concurrency and multithreading <asyncio-multithreading>`{.interpreted-text role="ref"} section of the documentation.

Unlike other asyncio functions this function requires the *loop* argument to be passed explicitly.

::: versionadded
3.5.1
:::
::::

## Introspection

:::: function
current_task(loop=None)

Return the currently running `Task`{.interpreted-text role="class"} instance, or `None` if no task is running.

If *loop* is `None` `get_running_loop`{.interpreted-text role="func"} is used to get the current loop.

::: versionadded
3.7
:::
::::

:::: function
all_tasks(loop=None)

Return a set of not yet finished `Task`{.interpreted-text role="class"} objects run by the loop.

If *loop* is `None`, `get_running_loop`{.interpreted-text role="func"} is used for getting current loop.

::: versionadded
3.7
:::
::::

:::: function
iscoroutine(obj)

Return `True` if *obj* is a coroutine object.

::: versionadded
3.4
:::
::::

## Task Object {#asyncio-task-obj}

:::::::::::::::::::::::::::::::::::: {.Task(coro, .*, .loop=None, .name=None, .context=None, .eager_start=False)}
A `Future-like <Future>`{.interpreted-text role="class"} object that runs a Python `coroutine <coroutine>`{.interpreted-text role="ref"}. Not thread-safe.

Tasks are used to run coroutines in event loops. If a coroutine awaits on a Future, the Task suspends the execution of the coroutine and waits for the completion of the Future. When the Future is *done*, the execution of the wrapped coroutine resumes.

Event loops use cooperative scheduling: an event loop runs one Task at a time. While a Task awaits for the completion of a Future, the event loop runs other Tasks, callbacks, or performs IO operations.

Use the high-level `asyncio.create_task`{.interpreted-text role="func"} function to create Tasks, or the low-level `loop.create_task`{.interpreted-text role="meth"} or `ensure_future`{.interpreted-text role="func"} functions. Manual instantiation of Tasks is discouraged.

To cancel a running Task use the `cancel`{.interpreted-text role="meth"} method. Calling it will cause the Task to throw a `CancelledError`{.interpreted-text role="exc"} exception into the wrapped coroutine. If a coroutine is awaiting on a future-like object during cancellation, the awaited object will be cancelled.

`cancelled`{.interpreted-text role="meth"} can be used to check if the Task was cancelled. The method returns `True` if the wrapped coroutine did not suppress the `CancelledError`{.interpreted-text role="exc"} exception and was actually cancelled.

`asyncio.Task`{.interpreted-text role="class"} inherits from `Future`{.interpreted-text role="class"} all of its APIs except `Future.set_result`{.interpreted-text role="meth"} and `Future.set_exception`{.interpreted-text role="meth"}.

An optional keyword-only *context* argument allows specifying a custom `contextvars.Context`{.interpreted-text role="class"} for the *coro* to run in. If no *context* is provided, the Task copies the current context and later runs its coroutine in the copied context.

An optional keyword-only *eager_start* argument allows eagerly starting the execution of the `asyncio.Task`{.interpreted-text role="class"} at task creation time. If set to `True` and the event loop is running, the task will start executing the coroutine immediately, until the first time the coroutine blocks. If the coroutine returns or raises without blocking, the task will be finished eagerly and will skip scheduling to the event loop.

::: versionchanged
3.7 Added support for the `contextvars`{.interpreted-text role="mod"} module.
:::

::: versionchanged
3.8 Added the *name* parameter.
:::

::: deprecated
3.10 Deprecation warning is emitted if *loop* is not specified and there is no running event loop.
:::

::: versionchanged
3.11 Added the *context* parameter.
:::

::: versionchanged
3.12 Added the *eager_start* parameter.
:::

::: method
done()

Return `True` if the Task is *done*.

A Task is *done* when the wrapped coroutine either returned a value, raised an exception, or the Task was cancelled.
:::

::: method
result()

Return the result of the Task.

If the Task is *done*, the result of the wrapped coroutine is returned (or if the coroutine raised an exception, that exception is re-raised.)

If the Task has been *cancelled*, this method raises a `CancelledError`{.interpreted-text role="exc"} exception.

If the Task\'s result isn\'t yet available, this method raises an `InvalidStateError`{.interpreted-text role="exc"} exception.
:::

::: method
exception()

Return the exception of the Task.

If the wrapped coroutine raised an exception that exception is returned. If the wrapped coroutine returned normally this method returns `None`.

If the Task has been *cancelled*, this method raises a `CancelledError`{.interpreted-text role="exc"} exception.

If the Task isn\'t *done* yet, this method raises an `InvalidStateError`{.interpreted-text role="exc"} exception.
:::

::: method
add_done_callback(callback, \*, context=None)

Add a callback to be run when the Task is *done*.

This method should only be used in low-level callback-based code.

See the documentation of `Future.add_done_callback`{.interpreted-text role="meth"} for more details.
:::

::: method
remove_done_callback(callback)

Remove *callback* from the callbacks list.

This method should only be used in low-level callback-based code.

See the documentation of `Future.remove_done_callback`{.interpreted-text role="meth"} for more details.
:::

::: method
get_stack(\*, limit=None)

Return the list of stack frames for this Task.

If the wrapped coroutine is not done, this returns the stack where it is suspended. If the coroutine has completed successfully or was cancelled, this returns an empty list. If the coroutine was terminated by an exception, this returns the list of traceback frames.

The frames are always ordered from oldest to newest.

Only one stack frame is returned for a suspended coroutine.

The optional *limit* argument sets the maximum number of frames to return; by default all available frames are returned. The ordering of the returned list differs depending on whether a stack or a traceback is returned: the newest frames of a stack are returned, but the oldest frames of a traceback are returned. (This matches the behavior of the traceback module.)
:::

::: method
print_stack(\*, limit=None, file=None)

Print the stack or traceback for this Task.

This produces output similar to that of the traceback module for the frames retrieved by `get_stack`{.interpreted-text role="meth"}.

The *limit* argument is passed to `get_stack`{.interpreted-text role="meth"} directly.

The *file* argument is an I/O stream to which the output is written; by default output is written to `sys.stdout`{.interpreted-text role="data"}.
:::

::::::: method
get_coro()

Return the coroutine object wrapped by the `Task`{.interpreted-text role="class"}.

:::: note
::: title
Note
:::

This will return `None` for Tasks which have already completed eagerly. See the `Eager Task Factory <eager-task-factory>`{.interpreted-text role="ref"}.
::::

::: versionadded
3.8
:::

::: versionchanged
3.12

Newly added eager task execution means result may be `None`.
:::
:::::::

:::: method
get_context()

Return the `contextvars.Context`{.interpreted-text role="class"} object associated with the task.

::: versionadded
3.12
:::
::::

:::: method
get_name()

Return the name of the Task.

If no name has been explicitly assigned to the Task, the default asyncio Task implementation generates a default name during instantiation.

::: versionadded
3.8
:::
::::

:::: method
set_name(value)

Set the name of the Task.

The *value* argument can be any object, which is then converted to a string.

In the default Task implementation, the name will be visible in the `repr`{.interpreted-text role="func"} output of a task object.

::: versionadded
3.8
:::
::::

:::::: method
cancel(msg=None)

Request the Task to be cancelled.

If the Task is already *done* or *cancelled*, return `False`, otherwise, return `True`.

The method arranges for a `CancelledError`{.interpreted-text role="exc"} exception to be thrown into the wrapped coroutine on the next cycle of the event loop.

The coroutine then has a chance to clean up or even deny the request by suppressing the exception with a `try`{.interpreted-text role="keyword"} \... \... `except CancelledError` \... `finally`{.interpreted-text role="keyword"} block. Therefore, unlike `Future.cancel`{.interpreted-text role="meth"}, `Task.cancel`{.interpreted-text role="meth"} does not guarantee that the Task will be cancelled, although suppressing cancellation completely is not common and is actively discouraged. Should the coroutine nevertheless decide to suppress the cancellation, it needs to call `Task.uncancel`{.interpreted-text role="meth"} in addition to catching the exception.

If the Task being cancelled is currently awaiting on a future-like object, that awaited object will also be cancelled. This cancellation propagates down the entire chain of awaited objects.

::: versionchanged
3.9 Added the *msg* parameter.
:::

::: versionchanged
3.11 The `msg` parameter is propagated from cancelled task to its awaiter.
:::

::: {#asyncio_example_task_cancel}
The following example illustrates how coroutines can intercept the cancellation request:

    async def cancel_me():
        print('cancel_me(): before sleep')

        try:
            # Wait for 1 hour
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            print('cancel_me(): cancel sleep')
            raise
        finally:
            print('cancel_me(): after sleep')

    async def main():
        # Create a "cancel_me" Task
        task = asyncio.create_task(cancel_me())

        # Wait for 1 second
        await asyncio.sleep(1)

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("main(): cancel_me is cancelled now")

    asyncio.run(main())

    # Expected output:
    #
    #     cancel_me(): before sleep
    #     cancel_me(): cancel sleep
    #     cancel_me(): after sleep
    #     main(): cancel_me is cancelled now
:::
::::::

::: method
cancelled()

Return `True` if the Task is *cancelled*.

The Task is *cancelled* when the cancellation was requested with `cancel`{.interpreted-text role="meth"} and the wrapped coroutine propagated the `CancelledError`{.interpreted-text role="exc"} exception thrown into it.
:::

:::: method
uncancel()

Decrement the count of cancellation requests to this Task.

Returns the remaining number of cancellation requests.

Note that once execution of a cancelled task completed, further calls to `uncancel`{.interpreted-text role="meth"} are ineffective.

::: versionadded
3.11
:::

This method is used by asyncio\'s internals and isn\'t expected to be used by end-user code. In particular, if a Task gets successfully uncancelled, this allows for elements of structured concurrency like `taskgroups`{.interpreted-text role="ref"} and `asyncio.timeout`{.interpreted-text role="func"} to continue running, isolating cancellation to the respective structured block. For example:

    async def make_request_with_timeout():
        try:
            async with asyncio.timeout(1):
                # Structured block affected by the timeout:
                await make_request()
                await make_another_request()
        except TimeoutError:
            log("There was a timeout")
        # Outer code not affected by the timeout:
        await unrelated_code()

While the block with `make_request()` and `make_another_request()` might get cancelled due to the timeout, `unrelated_code()` should continue running even in case of the timeout. This is implemented with `uncancel`{.interpreted-text role="meth"}. `TaskGroup`{.interpreted-text role="class"} context managers use `uncancel`{.interpreted-text role="func"} in a similar fashion.

If end-user code is, for some reason, suppressing cancellation by catching `CancelledError`{.interpreted-text role="exc"}, it needs to call this method to remove the cancellation state.

When this method decrements the cancellation count to zero, the method checks if a previous `cancel`{.interpreted-text role="meth"} call had arranged for `CancelledError`{.interpreted-text role="exc"} to be thrown into the task. If it hasn\'t been thrown yet, that arrangement will be rescinded (by resetting the internal `_must_cancel` flag).
::::

::: versionchanged
3.13 Changed to rescind pending cancellation requests upon reaching zero.
:::

:::: method
cancelling()

Return the number of pending cancellation requests to this Task, i.e., the number of calls to `cancel`{.interpreted-text role="meth"} less the number of `uncancel`{.interpreted-text role="meth"} calls.

Note that if this number is greater than zero but the Task is still executing, `cancelled`{.interpreted-text role="meth"} will still return `False`. This is because this number can be lowered by calling `uncancel`{.interpreted-text role="meth"}, which can lead to the task not being cancelled after all if the cancellation requests go down to zero.

This method is used by asyncio\'s internals and isn\'t expected to be used by end-user code. See `uncancel`{.interpreted-text role="meth"} for more details.

::: versionadded
3.11
:::
::::
::::::::::::::::::::::::::::::::::::
