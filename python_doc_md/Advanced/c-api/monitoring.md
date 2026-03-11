# Monitoring C API {#c-api-monitoring}

Added in version 3.13.

An extension may need to interact with the event monitoring system. Subscribing to events and registering callbacks can be done via the Python API exposed in `sys.monitoring`{.interpreted-text role="mod"}.

# Generating Execution Events

The functions below make it possible for an extension to fire monitoring events as it emulates the execution of Python code. Each of these functions accepts a `PyMonitoringState` struct which contains concise information about the activation state of events, as well as the event arguments, which include a `PyObject*` representing the code object, the instruction offset and sometimes additional, event-specific arguments (see `sys.monitoring`{.interpreted-text role="mod"} for details about the signatures of the different event callbacks). The `codelike` argument should be an instance of `types.CodeType`{.interpreted-text role="class"} or of a type that emulates it.

The VM disables tracing when firing an event, so there is no need for user code to do that.

Monitoring functions should not be called with an exception set, except those listed below as working with the current exception.

> Representation of the state of an event type. It is allocated by the user while its contents are maintained by the monitoring API functions described below.

All of the functions below return 0 on success and -1 (with an exception set) on error.

See `sys.monitoring`{.interpreted-text role="mod"} for descriptions of the events.

> Fire a `PY_START` event.

> Fire a `PY_RESUME` event.

> Fire a `PY_RETURN` event.

> Fire a `PY_YIELD` event.

> Fire a `CALL` event.

> Fire a `LINE` event.

> Fire a `JUMP` event.

> Fire a `BRANCH_LEFT` event.

> Fire a `BRANCH_RIGHT` event.

> Fire a `C_RETURN` event.

> Fire a `PY_THROW` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire a `RAISE` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire a `C_RAISE` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire a `RERAISE` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire an `EXCEPTION_HANDLED` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire a `PY_UNWIND` event with the current exception (as returned by `PyErr_GetRaisedException`{.interpreted-text role="c:func"}).

> Fire a `STOP_ITERATION` event. If `value` is an instance of `StopIteration`{.interpreted-text role="exc"}, it is used. Otherwise, a new `StopIteration`{.interpreted-text role="exc"} instance is created with `value` as its argument.

## Managing the Monitoring State

Monitoring states can be managed with the help of monitoring scopes. A scope would typically correspond to a Python function.

> Enter a monitored scope. `event_types` is an array of the event IDs for events that may be fired from the scope. For example, the ID of a `PY_START` event is the value `PY_MONITORING_EVENT_PY_START`, which is numerically equal to the base-2 logarithm of `sys.monitoring.events.PY_START`. `state_array` is an array with a monitoring state entry for each event in `event_types`, it is allocated by the user but populated by `!PyMonitoring_EnterScope`{.interpreted-text role="c:func"} with information about the activation state of the event. The size of `event_types` (and hence also of `state_array`) is given in `length`.
>
> The `version` argument is a pointer to a value which should be allocated by the user together with `state_array` and initialized to 0, and then set only by `!PyMonitoring_EnterScope`{.interpreted-text role="c:func"} itself. It allows this function to determine whether event states have changed since the previous call, and to return quickly if they have not.
>
> The scopes referred to here are lexical scopes: a function, class or method. `!PyMonitoring_EnterScope`{.interpreted-text role="c:func"} should be called whenever the lexical scope is entered. Scopes can be reentered, reusing the same *state_array* and *version*, in situations like when emulating a recursive Python function. When a code-like\'s execution is paused, such as when emulating a generator, the scope needs to be exited and re-entered.
>
> The macros for *event_types* are:
>
>   Macro   Event
>   ------- ----------------------------------------------------------------
>           `BRANCH_LEFT`{.interpreted-text role="monitoring-event"}
>           `BRANCH_RIGHT`{.interpreted-text role="monitoring-event"}
>           `CALL`{.interpreted-text role="monitoring-event"}
>           `C_RAISE`{.interpreted-text role="monitoring-event"}
>           `C_RETURN`{.interpreted-text role="monitoring-event"}
>           `EXCEPTION_HANDLED`{.interpreted-text role="monitoring-event"}
>           `INSTRUCTION`{.interpreted-text role="monitoring-event"}
>           `JUMP`{.interpreted-text role="monitoring-event"}
>           `LINE`{.interpreted-text role="monitoring-event"}
>           `PY_RESUME`{.interpreted-text role="monitoring-event"}
>           `PY_RETURN`{.interpreted-text role="monitoring-event"}
>           `PY_START`{.interpreted-text role="monitoring-event"}
>           `PY_THROW`{.interpreted-text role="monitoring-event"}
>           `PY_UNWIND`{.interpreted-text role="monitoring-event"}
>           `PY_YIELD`{.interpreted-text role="monitoring-event"}
>           `RAISE`{.interpreted-text role="monitoring-event"}
>           `RERAISE`{.interpreted-text role="monitoring-event"}
>           `STOP_ITERATION`{.interpreted-text role="monitoring-event"}

> Exit the last scope that was entered with `!PyMonitoring_EnterScope`{.interpreted-text role="c:func"}.

> Return true if the event corresponding to the event ID *ev* is a `local event <monitoring-event-local>`{.interpreted-text role="ref"}.
>
> ::: versionadded
> 3.13
> :::
>
> ::: deprecated
> 3.14
>
> This function is `soft deprecated`{.interpreted-text role="term"}.
> :::
