::: currentmodule
asyncio
:::

# High-level API Index

This page lists all high-level async/await enabled asyncio APIs.

## Tasks

Utilities to run asyncio programs, create Tasks, and await on multiple things with timeouts.

  ----------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------
  `run`{.interpreted-text role="func"}                        Create event loop, run a coroutine, close the loop.

  `Runner`{.interpreted-text role="class"}                    A context manager that simplifies multiple async function calls.

  `Task`{.interpreted-text role="class"}                      Task object.

  `TaskGroup`{.interpreted-text role="class"}                 A context manager that holds a group of tasks. Provides a convenient and reliable way to wait for all tasks in the group to finish.

  `create_task`{.interpreted-text role="func"}                Start an asyncio Task, then returns it.

  `current_task`{.interpreted-text role="func"}               Return the current Task.

  `all_tasks`{.interpreted-text role="func"}                  Return all tasks that are not yet finished for an event loop.

  `await` `sleep`{.interpreted-text role="func"}              Sleep for a number of seconds.

  `await` `gather`{.interpreted-text role="func"}             Schedule and wait for things concurrently.

  `await` `wait_for`{.interpreted-text role="func"}           Run with a timeout.

  `await` `shield`{.interpreted-text role="func"}             Shield from cancellation.

  `await` `wait`{.interpreted-text role="func"}               Monitor for completion.

  `timeout`{.interpreted-text role="func"}                    Run with a timeout. Useful in cases when `wait_for` is not suitable.

  `to_thread`{.interpreted-text role="func"}                  Asynchronously run a function in a separate OS thread.

  `run_coroutine_threadsafe`{.interpreted-text role="func"}   Schedule a coroutine from another OS thread.

  `for in` `as_completed`{.interpreted-text role="func"}      Monitor for completion with a `for` loop.
  ----------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------

**Examples**

- `Using asyncio.gather() to run things in parallel
  <asyncio_example_gather>`{.interpreted-text role="ref"}.
- `Using asyncio.wait_for() to enforce a timeout
  <asyncio_example_waitfor>`{.interpreted-text role="ref"}.
- `Cancellation <asyncio_example_task_cancel>`{.interpreted-text role="ref"}.
- `Using asyncio.sleep() <asyncio_example_sleep>`{.interpreted-text role="ref"}.
- See also the main `Tasks documentation page <coroutine>`{.interpreted-text role="ref"}.

## Queues

Queues should be used to distribute work amongst multiple asyncio Tasks, implement connection pools, and pub/sub patterns.

  ------------------------------------------------- -----------------------------------
  `Queue`{.interpreted-text role="class"}           A FIFO queue.

  `PriorityQueue`{.interpreted-text role="class"}   A priority queue.

  `LifoQueue`{.interpreted-text role="class"}       A LIFO queue.
  ------------------------------------------------- -----------------------------------

**Examples**

- `Using asyncio.Queue to distribute workload between several
  Tasks <asyncio_example_queue_dist>`{.interpreted-text role="ref"}.
- See also the `Queues documentation page <asyncio-queues>`{.interpreted-text role="ref"}.

## Subprocesses

Utilities to spawn subprocesses and run shell commands.

  ------------------------------------------------------------------ -----------------------------------
  `await` `create_subprocess_exec`{.interpreted-text role="func"}    Create a subprocess.

  `await` `create_subprocess_shell`{.interpreted-text role="func"}   Run a shell command.
  ------------------------------------------------------------------ -----------------------------------

**Examples**

- `Executing a shell command <asyncio_example_subprocess_shell>`{.interpreted-text role="ref"}.
- See also the `subprocess APIs <asyncio-subprocess>`{.interpreted-text role="ref"} documentation.

## Streams

High-level APIs to work with network IO.

  --------------------------------------------------------------- --------------------------------------------------------
  `await` `open_connection`{.interpreted-text role="func"}        Establish a TCP connection.

  `await` `open_unix_connection`{.interpreted-text role="func"}   Establish a Unix socket connection.

  `await` `start_server`{.interpreted-text role="func"}           Start a TCP server.

  `await` `start_unix_server`{.interpreted-text role="func"}      Start a Unix socket server.

  `StreamReader`{.interpreted-text role="class"}                  High-level async/await object to receive network data.

  `StreamWriter`{.interpreted-text role="class"}                  High-level async/await object to send network data.
  --------------------------------------------------------------- --------------------------------------------------------

**Examples**

- `Example TCP client <asyncio_example_stream>`{.interpreted-text role="ref"}.
- See also the `streams APIs <asyncio-streams>`{.interpreted-text role="ref"} documentation.

## Synchronization

Threading-like synchronization primitives that can be used in Tasks.

  ---------------------------------------------------- -----------------------------------
  `Lock`{.interpreted-text role="class"}               A mutex lock.

  `Event`{.interpreted-text role="class"}              An event object.

  `Condition`{.interpreted-text role="class"}          A condition object.

  `Semaphore`{.interpreted-text role="class"}          A semaphore.

  `BoundedSemaphore`{.interpreted-text role="class"}   A bounded semaphore.

  `Barrier`{.interpreted-text role="class"}            A barrier object.
  ---------------------------------------------------- -----------------------------------

**Examples**

- `Using asyncio.Event <asyncio_example_sync_event>`{.interpreted-text role="ref"}.
- `Using asyncio.Barrier <asyncio_example_barrier>`{.interpreted-text role="ref"}.
- See also the documentation of asyncio `synchronization primitives <asyncio-sync>`{.interpreted-text role="ref"}.

## Exceptions

  ------------------------------------------------------------ ------------------------------------------------------------------------------------------
  `asyncio.CancelledError`{.interpreted-text role="exc"}       Raised when a Task is cancelled. See also `Task.cancel`{.interpreted-text role="meth"}.

  `asyncio.BrokenBarrierError`{.interpreted-text role="exc"}   Raised when a Barrier is broken. See also `Barrier.wait`{.interpreted-text role="meth"}.
  ------------------------------------------------------------ ------------------------------------------------------------------------------------------

**Examples**

- `Handling CancelledError to run code on cancellation request
  <asyncio_example_task_cancel>`{.interpreted-text role="ref"}.
- See also the full list of `asyncio-specific exceptions <asyncio-exceptions>`{.interpreted-text role="ref"}.
