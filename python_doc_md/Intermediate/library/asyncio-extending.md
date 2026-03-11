::: currentmodule
asyncio
:::

# Extending

The main direction for `asyncio`{.interpreted-text role="mod"} extending is writing custom *event loop* classes. Asyncio has helpers that could be used to simplify this task.

:::: note
::: title
Note
:::

Third-parties should reuse existing asyncio code with caution, a new Python version is free to break backward compatibility in *internal* part of API.
::::

## Writing a Custom Event Loop

`asyncio.AbstractEventLoop`{.interpreted-text role="class"} declares very many methods. Implementing all them from scratch is a tedious job.

A loop can get many common methods implementation for free by inheriting from `asyncio.BaseEventLoop`{.interpreted-text role="class"}.

In turn, the successor should implement a bunch of *private* methods declared but not implemented in `asyncio.BaseEventLoop`{.interpreted-text role="class"}.

For example, `loop.create_connection()` checks arguments, resolves DNS addresses, and calls `loop._make_socket_transport()` that should be implemented by inherited class. The `_make_socket_transport()` method is not documented and is considered as an *internal* API.

## Future and Task private constructors

`asyncio.Future`{.interpreted-text role="class"} and `asyncio.Task`{.interpreted-text role="class"} should be never created directly, please use corresponding `loop.create_future`{.interpreted-text role="meth"} and `loop.create_task`{.interpreted-text role="meth"}, or `asyncio.create_task`{.interpreted-text role="func"} factories instead.

However, third-party *event loops* may *reuse* built-in future and task implementations for the sake of getting a complex and highly optimized code for free.

For this purpose the following, *private* constructors are listed:

::: method
Future.\_\_init\_\_(\*, loop=None)

Create a built-in future instance.

*loop* is an optional event loop instance.
:::

:::: method
Task.\_\_init\_\_(coro, \*, loop=None, name=None, context=None)

Create a built-in task instance.

*loop* is an optional event loop instance. The rest of arguments are described in `loop.create_task`{.interpreted-text role="meth"} description.

::: versionchanged
3.11

*context* argument is added.
:::
::::

## Task lifetime support

A third party task implementation should call the following functions to keep a task visible by `asyncio.all_tasks`{.interpreted-text role="func"} and `asyncio.current_task`{.interpreted-text role="func"}:

::: function
[register_task]{#register_task}(task)

Register a new *task* as managed by *asyncio*.

Call the function from a task constructor.
:::

::: function
[unregister_task]{#unregister_task}(task)

Unregister a *task* from *asyncio* internal structures.

The function should be called when a task is about to finish.
:::

::: function
[enter_task]{#enter_task}(loop, task)

Switch the current task to the *task* argument.

Call the function just before executing a portion of embedded *coroutine* (`coroutine.send`{.interpreted-text role="meth"} or `coroutine.throw`{.interpreted-text role="meth"}).
:::

::: function
[leave_task]{#leave_task}(loop, task)

Switch the current task back from *task* to `None`.

Call the function just after `coroutine.send`{.interpreted-text role="meth"} or `coroutine.throw`{.interpreted-text role="meth"} execution.
:::
