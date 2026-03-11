# `!sys.monitoring`{.interpreted-text role="mod"} \-\-- Execution event monitoring

::: {.module synopsis="Access and control event monitoring"}
sys.monitoring
:::

::: versionadded
3.12
:::

------------------------------------------------------------------------

:::: note
::: title
Note
:::

`!sys.monitoring`{.interpreted-text role="mod"} is a namespace within the `sys`{.interpreted-text role="mod"} module, not an independent module, so there is no need to `import sys.monitoring`, simply `import sys` and then use `sys.monitoring`.
::::

This namespace provides access to the functions and constants necessary to activate and control event monitoring.

As programs execute, events occur that might be of interest to tools that monitor execution. The `!sys.monitoring`{.interpreted-text role="mod"} namespace provides means to receive callbacks when events of interest occur.

The monitoring API consists of three components:

- [Tool identifiers](#tool-identifiers)
- [Events](#events)
- `Callbacks <callbacks>`{.interpreted-text role="ref"}

## Tool identifiers

A tool identifier is an integer and the associated name. Tool identifiers are used to discourage tools from interfering with each other and to allow multiple tools to operate at the same time. Currently tools are completely independent and cannot be used to monitor each other. This restriction may be lifted in the future.

Before registering or activating events, a tool should choose an identifier. Identifiers are integers in the range 0 to 5 inclusive.

### Registering and using tools

::: function
use_tool_id(tool_id: int, name: str, /) -\> None

Must be called before *tool_id* can be used. *tool_id* must be in the range 0 to 5 inclusive. Raises a `ValueError`{.interpreted-text role="exc"} if *tool_id* is in use.
:::

::: function
clear_tool_id(tool_id: int, /) -\> None

Unregister all events and callback functions associated with *tool_id*.
:::

::: function
free_tool_id(tool_id: int, /) -\> None

Should be called once a tool no longer requires *tool_id*. Will call `clear_tool_id`{.interpreted-text role="func"} before releasing *tool_id*.
:::

::: function
get_tool(tool_id: int, /) -\> str \| None

Returns the name of the tool if *tool_id* is in use, otherwise it returns `None`. *tool_id* must be in the range 0 to 5 inclusive.
:::

All IDs are treated the same by the VM with regard to events, but the following IDs are pre-defined to make co-operation of tools easier:

    sys.monitoring.DEBUGGER_ID = 0
    sys.monitoring.COVERAGE_ID = 1
    sys.monitoring.PROFILER_ID = 2
    sys.monitoring.OPTIMIZER_ID = 5

## Events

The following events are supported:

::: monitoring-event
BRANCH_LEFT

A conditional branch goes left.

It is up to the tool to determine how to present \"left\" and \"right\" branches. There is no guarantee which branch is \"left\" and which is \"right\", except that it will be consistent for the duration of the program.
:::

::: monitoring-event
BRANCH_RIGHT

A conditional branch goes right.
:::

::: monitoring-event
CALL

A call in Python code (event occurs before the call).
:::

::: monitoring-event
C_RAISE

An exception raised from any callable, except for Python functions (event occurs after the exit).
:::

::: monitoring-event
C_RETURN

Return from any callable, except for Python functions (event occurs after the return).
:::

::: monitoring-event
EXCEPTION_HANDLED

An exception is handled.
:::

::: monitoring-event
INSTRUCTION

A VM instruction is about to be executed.
:::

::: monitoring-event
JUMP

An unconditional jump in the control flow graph is made.
:::

::: monitoring-event
LINE

An instruction is about to be executed that has a different line number from the preceding instruction.
:::

::: monitoring-event
PY_RESUME

Resumption of a Python function (for generator and coroutine functions), except for `throw()` calls.
:::

::: monitoring-event
PY_RETURN

Return from a Python function (occurs immediately before the return, the callee\'s frame will be on the stack).
:::

::: monitoring-event
PY_START

Start of a Python function (occurs immediately after the call, the callee\'s frame will be on the stack)
:::

::: monitoring-event
PY_THROW

A Python function is resumed by a `throw()` call.
:::

::: monitoring-event
PY_UNWIND

Exit from a Python function during exception unwinding. This includes exceptions raised directly within the function and that are allowed to continue to propagate.
:::

::: monitoring-event
PY_YIELD

Yield from a Python function (occurs immediately before the yield, the callee\'s frame will be on the stack).
:::

::: monitoring-event
RAISE

An exception is raised, except those that cause a `STOP_ITERATION`{.interpreted-text role="monitoring-event"} event.
:::

::: monitoring-event
RERAISE

An exception is re-raised, for example at the end of a `finally`{.interpreted-text role="keyword"} block.
:::

::: monitoring-event
STOP_ITERATION

An artificial `StopIteration`{.interpreted-text role="exc"} is raised; see [the STOP_ITERATION event](#the-stop_iteration-event).
:::

More events may be added in the future.

These events are attributes of the `!sys.monitoring.events`{.interpreted-text role="mod"} namespace. Each event is represented as a power-of-2 integer constant. To define a set of events, simply bitwise OR the individual events together. For example, to specify both `PY_RETURN`{.interpreted-text role="monitoring-event"} and `PY_START`{.interpreted-text role="monitoring-event"} events, use the expression `PY_RETURN | PY_START`.

::: monitoring-event
NO_EVENTS

An alias for `0` so users can do explicit comparisons like:

    if get_events(DEBUGGER_ID) == NO_EVENTS:
        ...

Setting this event deactivates all events.
:::

### Local events {#monitoring-event-local}

Local events are associated with normal execution of the program and happen at clearly defined locations. All local events can be disabled. The local events are:

- `PY_START`{.interpreted-text role="monitoring-event"}
- `PY_RESUME`{.interpreted-text role="monitoring-event"}
- `PY_RETURN`{.interpreted-text role="monitoring-event"}
- `PY_YIELD`{.interpreted-text role="monitoring-event"}
- `CALL`{.interpreted-text role="monitoring-event"}
- `LINE`{.interpreted-text role="monitoring-event"}
- `INSTRUCTION`{.interpreted-text role="monitoring-event"}
- `JUMP`{.interpreted-text role="monitoring-event"}
- `BRANCH_LEFT`{.interpreted-text role="monitoring-event"}
- `BRANCH_RIGHT`{.interpreted-text role="monitoring-event"}
- `STOP_ITERATION`{.interpreted-text role="monitoring-event"}

### Deprecated event

- `BRANCH`

The `BRANCH` event is deprecated in 3.14. Using `BRANCH_LEFT`{.interpreted-text role="monitoring-event"} and `BRANCH_RIGHT`{.interpreted-text role="monitoring-event"} events will give much better performance as they can be disabled independently.

### Ancillary events

Ancillary events can be monitored like other events, but are controlled by another event:

- `C_RAISE`{.interpreted-text role="monitoring-event"}
- `C_RETURN`{.interpreted-text role="monitoring-event"}

The `C_RETURN`{.interpreted-text role="monitoring-event"} and `C_RAISE`{.interpreted-text role="monitoring-event"} events are controlled by the `CALL`{.interpreted-text role="monitoring-event"} event. `C_RETURN`{.interpreted-text role="monitoring-event"} and `C_RAISE`{.interpreted-text role="monitoring-event"} events will only be seen if the corresponding `CALL`{.interpreted-text role="monitoring-event"} event is being monitored.

### Other events {#monitoring-event-global}

Other events are not necessarily tied to a specific location in the program and cannot be individually disabled via `DISABLE`{.interpreted-text role="data"}.

The other events that can be monitored are:

- `PY_THROW`{.interpreted-text role="monitoring-event"}
- `PY_UNWIND`{.interpreted-text role="monitoring-event"}
- `RAISE`{.interpreted-text role="monitoring-event"}
- `EXCEPTION_HANDLED`{.interpreted-text role="monitoring-event"}

### The STOP_ITERATION event

`PEP 380 <380#use-of-stopiteration-to-return-values>`{.interpreted-text role="pep"} specifies that a `StopIteration`{.interpreted-text role="exc"} exception is raised when returning a value from a generator or coroutine. However, this is a very inefficient way to return a value, so some Python implementations, notably CPython 3.12+, do not raise an exception unless it would be visible to other code.

To allow tools to monitor for real exceptions without slowing down generators and coroutines, the `STOP_ITERATION`{.interpreted-text role="monitoring-event"} event is provided. `STOP_ITERATION`{.interpreted-text role="monitoring-event"} can be locally disabled, unlike `RAISE`{.interpreted-text role="monitoring-event"}.

Note that the `STOP_ITERATION`{.interpreted-text role="monitoring-event"} event and the `RAISE`{.interpreted-text role="monitoring-event"} event for a `StopIteration`{.interpreted-text role="exc"} exception are equivalent, and are treated as interchangeable when generating events. Implementations will favor `STOP_ITERATION`{.interpreted-text role="monitoring-event"} for performance reasons, but may generate a `RAISE`{.interpreted-text role="monitoring-event"} event with a `StopIteration`{.interpreted-text role="exc"}.

## Turning events on and off

In order to monitor an event, it must be turned on and a corresponding callback must be registered. Events can be turned on or off by setting the events either globally and/or for a particular code object. An event will trigger only once, even if it is turned on both globally and locally.

### Setting events globally

Events can be controlled globally by modifying the set of events being monitored.

::: function
get_events(tool_id: int, /) -\> int

Returns the `int` representing all the active events.
:::

::: function
set_events(tool_id: int, event_set: int, /) -\> None

Activates all events which are set in *event_set*. Raises a `ValueError`{.interpreted-text role="exc"} if *tool_id* is not in use.
:::

No events are active by default.

### Per code object events

Events can also be controlled on a per code object basis. The functions defined below which accept a `types.CodeType`{.interpreted-text role="class"} should be prepared to accept a look-alike object from functions which are not defined in Python (see `c-api-monitoring`{.interpreted-text role="ref"}).

::: function
get_local_events(tool_id: int, code: CodeType, /) -\> int

Returns all the `local events <monitoring-event-local>`{.interpreted-text role="ref"} for *code*
:::

::: function
set_local_events(tool_id: int, code: CodeType, event_set: int, /) -\> None

Activates all the `local events <monitoring-event-local>`{.interpreted-text role="ref"} for *code* which are set in *event_set*. Raises a `ValueError`{.interpreted-text role="exc"} if *tool_id* is not in use.
:::

### Disabling events

::: data
DISABLE

A special value that can be returned from a callback function to disable events for the current code location.
:::

`Local events <monitoring-event-local>`{.interpreted-text role="ref"} can be disabled for a specific code location by returning `sys.monitoring.DISABLE`{.interpreted-text role="data"} from a callback function. This does not change which events are set, or any other code locations for the same event.

Disabling events for specific locations is very important for high performance monitoring. For example, a program can be run under a debugger with no overhead if the debugger disables all monitoring except for a few breakpoints.

If `DISABLE`{.interpreted-text role="data"} is returned by a callback for a `global event <monitoring-event-global>`{.interpreted-text role="ref"}, `ValueError`{.interpreted-text role="exc"} will be raised by the interpreter in a non-specific location (that is, no traceback will be provided).

::: function
restart_events() -\> None

Enable all the events that were disabled by `sys.monitoring.DISABLE`{.interpreted-text role="data"} for all tools.
:::

## Registering callback functions {#callbacks}

:::: function
register_callback(tool_id: int, event: int, func: Callable \| None, /) -\> Callable \| None

Registers the callable *func* for the *event* with the given *tool_id*

If another callback was registered for the given *tool_id* and *event*, it is unregistered and returned. Otherwise `register_callback`{.interpreted-text role="func"} returns `None`.

::: audit-event
sys.monitoring.register_callback func sys.monitoring.register_callback
:::
::::

Functions can be unregistered by calling `sys.monitoring.register_callback(tool_id, event, None)`.

Callback functions can be registered and unregistered at any time.

Callbacks are called only once regardless if the event is turned on both globally and locally. As such, if an event could be turned on for both global and local events by your code then the callback needs to be written to handle either trigger.

### Callback function arguments

::: data
MISSING

A special value that is passed to a callback function to indicate that there are no arguments to the call.
:::

When an active event occurs, the registered callback function is called. Callback functions returning an object other than `DISABLE`{.interpreted-text role="data"} will have no effect. Different events will provide the callback function with different arguments, as follows:

- `PY_START`{.interpreted-text role="monitoring-event"} and `PY_RESUME`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, instruction_offset: int) -> object

- `PY_RETURN`{.interpreted-text role="monitoring-event"} and `PY_YIELD`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, instruction_offset: int, retval: object) -> object

- `CALL`{.interpreted-text role="monitoring-event"}, `C_RAISE`{.interpreted-text role="monitoring-event"} and `C_RETURN`{.interpreted-text role="monitoring-event"} (*arg0* can be `MISSING`{.interpreted-text role="data"} specifically):

      func(code: CodeType, instruction_offset: int, callable: object, arg0: object) -> object

  *code* represents the code object where the call is being made, while *callable* is the object that is about to be called (and thus triggered the event). If there are no arguments, *arg0* is set to `sys.monitoring.MISSING`{.interpreted-text role="data"}.

  For instance methods, *callable* will be the function object as found on the class with *arg0* set to the instance (i.e. the `self` argument to the method).

- `RAISE`{.interpreted-text role="monitoring-event"}, `RERAISE`{.interpreted-text role="monitoring-event"}, `EXCEPTION_HANDLED`{.interpreted-text role="monitoring-event"}, `PY_UNWIND`{.interpreted-text role="monitoring-event"}, `PY_THROW`{.interpreted-text role="monitoring-event"} and `STOP_ITERATION`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, instruction_offset: int, exception: BaseException) -> object

- `LINE`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, line_number: int) -> object

- `BRANCH_LEFT`{.interpreted-text role="monitoring-event"}, `BRANCH_RIGHT`{.interpreted-text role="monitoring-event"} and `JUMP`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, instruction_offset: int, destination_offset: int) -> object

  Note that the *destination_offset* is where the code will next execute.

- `INSTRUCTION`{.interpreted-text role="monitoring-event"}:

      func(code: CodeType, instruction_offset: int) -> object
