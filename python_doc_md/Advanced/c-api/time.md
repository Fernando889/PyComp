# PyTime C API {#c-api-time}

::: versionadded
3.13
:::

The clock C API provides access to system clocks. It is similar to the Python `time`{.interpreted-text role="mod"} module.

For C API related to the `datetime`{.interpreted-text role="mod"} module, see `datetimeobjects`{.interpreted-text role="ref"}.

## Types

> A timestamp or duration in nanoseconds, represented as a signed 64-bit integer.
>
> The reference point for timestamps depends on the clock used. For example, `PyTime_Time`{.interpreted-text role="c:func"} returns timestamps relative to the UNIX epoch.
>
> The supported range is around \[-292.3 years; +292.3 years\]. Using the Unix epoch (January 1st, 1970) as reference, the supported date range is around \[1677-09-21; 2262-04-11\]. The exact limits are exposed as constants:

> Minimum value of `PyTime_t`{.interpreted-text role="c:type"}.

> Maximum value of `PyTime_t`{.interpreted-text role="c:type"}.

## Clock Functions

The following functions take a pointer to a `PyTime_t`{.interpreted-text role="c:expr"} that they set to the value of a particular clock. Details of each clock are given in the documentation of the corresponding Python function.

The functions return `0` on success, or `-1` (with an exception set) on failure.

On integer overflow, they set the `PyExc_OverflowError`{.interpreted-text role="c:data"} exception and set `*result` to the value clamped to the `[PyTime_MIN; PyTime_MAX]` range. (On current systems, integer overflows are likely caused by misconfigured system time.)

As any other C API (unless otherwise specified), the functions must be called with an `attached thread state`{.interpreted-text role="term"}.

> Read the monotonic clock. See `time.monotonic`{.interpreted-text role="func"} for important details on this clock.

> Read the performance counter. See `time.perf_counter`{.interpreted-text role="func"} for important details on this clock.

> Read the "wall clock" time. See `time.time`{.interpreted-text role="func"} for details important on this clock.

## Raw Clock Functions

Similar to clock functions, but don\'t set an exception on error and don\'t require the caller to have an `attached thread state`{.interpreted-text role="term"}.

On success, the functions return `0`.

On failure, they set `*result` to `0` and return `-1`, *without* setting an exception. To get the cause of the error, `attach <attached thread state>`{.interpreted-text role="term"} a `thread state`{.interpreted-text role="term"}, and call the regular (non-`Raw`) function. Note that the regular function may succeed after the `Raw` one failed.

> Similar to `PyTime_Monotonic`{.interpreted-text role="c:func"}, but don\'t set an exception on error and don\'t require an `attached thread state`{.interpreted-text role="term"}.

> Similar to `PyTime_PerfCounter`{.interpreted-text role="c:func"}, but don\'t set an exception on error and don\'t require an `attached thread state`{.interpreted-text role="term"}.

> Similar to `PyTime_Time`{.interpreted-text role="c:func"}, but don\'t set an exception on error and don\'t require an `attached thread state`{.interpreted-text role="term"}.

## Conversion functions

> Convert a timestamp to a number of seconds as a C `double`{.interpreted-text role="c:expr"}.
>
> The function cannot fail, but note that `double`{.interpreted-text role="c:expr"} has limited accuracy for large values.
