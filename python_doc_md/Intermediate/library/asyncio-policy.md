::: currentmodule
asyncio
:::

# Policies {#asyncio-policies}

:::: warning
::: title
Warning
:::

Policies are deprecated and will be removed in Python 3.16. Users are encouraged to use the `asyncio.run`{.interpreted-text role="func"} function or the `asyncio.Runner`{.interpreted-text role="class"} with *loop_factory* to use the desired loop implementation.
::::

An event loop policy is a global object used to get and set the current `event loop <asyncio-event-loop>`{.interpreted-text role="ref"}, as well as create new event loops. The default policy can be `replaced <asyncio-policy-get-set>`{.interpreted-text role="ref"} with `built-in alternatives <asyncio-policy-builtin>`{.interpreted-text role="ref"} to use different event loop implementations, or substituted by a `custom policy <asyncio-custom-policies>`{.interpreted-text role="ref"} that can override these behaviors.

The `policy object <asyncio-policy-objects>`{.interpreted-text role="ref"} gets and sets a separate event loop per *context*. This is per-thread by default, though custom policies could define *context* differently.

Custom event loop policies can control the behavior of `get_event_loop`{.interpreted-text role="func"}, `set_event_loop`{.interpreted-text role="func"}, and `new_event_loop`{.interpreted-text role="func"}.

Policy objects should implement the APIs defined in the `AbstractEventLoopPolicy`{.interpreted-text role="class"} abstract base class.

## Getting and Setting the Policy {#asyncio-policy-get-set}

The following functions can be used to get and set the policy for the current process:

:::: function
get_event_loop_policy()

Return the current process-wide policy.

::: deprecated
3.14 The `get_event_loop_policy`{.interpreted-text role="func"} function is deprecated and will be removed in Python 3.16.
:::
::::

:::: function
set_event_loop_policy(policy)

Set the current process-wide policy to *policy*.

If *policy* is set to `None`, the default policy is restored.

::: deprecated
3.14 The `set_event_loop_policy`{.interpreted-text role="func"} function is deprecated and will be removed in Python 3.16.
:::
::::

## Policy Objects {#asyncio-policy-objects}

The abstract event loop policy base class is defined as follows:

:::::::: AbstractEventLoopPolicy
An abstract base class for asyncio policies.

:::: method
get_event_loop()

Get the event loop for the current context.

Return an event loop object implementing the `AbstractEventLoop`{.interpreted-text role="class"} interface.

This method should never return `None`.

::: versionchanged
3.6
:::
::::

::: method
set_event_loop(loop)

Set the event loop for the current context to *loop*.
:::

::: method
new_event_loop()

Create and return a new event loop object.

This method should never return `None`.
:::

::: deprecated
3.14 The `AbstractEventLoopPolicy`{.interpreted-text role="class"} class is deprecated and will be removed in Python 3.16.
:::
::::::::

::: {#asyncio-policy-builtin}
asyncio ships with the following built-in policies:
:::

:::::: DefaultEventLoopPolicy
The default asyncio policy. Uses `SelectorEventLoop`{.interpreted-text role="class"} on Unix and `ProactorEventLoop`{.interpreted-text role="class"} on Windows.

There is no need to install the default policy manually. asyncio is configured to use the default policy automatically.

::: versionchanged
3.8

On Windows, `ProactorEventLoop`{.interpreted-text role="class"} is now used by default.
:::

::: versionchanged
3.14 The `get_event_loop`{.interpreted-text role="meth"} method of the default asyncio policy now raises a `RuntimeError`{.interpreted-text role="exc"} if there is no set event loop.
:::

::: deprecated
3.14 The `DefaultEventLoopPolicy`{.interpreted-text role="class"} class is deprecated and will be removed in Python 3.16.
:::
::::::

::::: WindowsSelectorEventLoopPolicy
An alternative event loop policy that uses the `SelectorEventLoop`{.interpreted-text role="class"} event loop implementation.

::: availability
Windows.
:::

::: deprecated
3.14 The `WindowsSelectorEventLoopPolicy`{.interpreted-text role="class"} class is deprecated and will be removed in Python 3.16.
:::
:::::

::::: WindowsProactorEventLoopPolicy
An alternative event loop policy that uses the `ProactorEventLoop`{.interpreted-text role="class"} event loop implementation.

::: availability
Windows.
:::

::: deprecated
3.14 The `WindowsProactorEventLoopPolicy`{.interpreted-text role="class"} class is deprecated and will be removed in Python 3.16.
:::
:::::

## Custom Policies {#asyncio-custom-policies}

To implement a new event loop policy, it is recommended to subclass `DefaultEventLoopPolicy`{.interpreted-text role="class"} and override the methods for which custom behavior is wanted, e.g.:

    class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

        def get_event_loop(self):
            """Get the event loop.

            This may be None or an instance of EventLoop.
            """
            loop = super().get_event_loop()
            # Do something with loop ...
            return loop

    asyncio.set_event_loop_policy(MyEventLoopPolicy())
