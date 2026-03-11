# DateTime Objects {#datetimeobjects}

Various date and time objects are supplied by the `datetime`{.interpreted-text role="mod"} module. Before using any of these functions, the header file `datetime.h`{.interpreted-text role="file"} must be included in your source (note that this is not included by `Python.h`{.interpreted-text role="file"}), and the macro `PyDateTime_IMPORT`{.interpreted-text role="c:macro"} must be invoked, usually as part of the module initialisation function. The macro puts a pointer to a C structure into a static variable, `PyDateTimeAPI`{.interpreted-text role="c:data"}, that is used by the following macros.

> Import the datetime C API.
>
> On success, populate the `PyDateTimeAPI`{.interpreted-text role="c:var"} pointer. On failure, set `PyDateTimeAPI`{.interpreted-text role="c:var"} to `NULL` and set an exception. The caller must check if an error occurred via `PyErr_Occurred`{.interpreted-text role="c:func"}:
>
> ``` 
> PyDateTime_IMPORT;
> if (PyErr_Occurred()) { /* cleanup */ }
> ```
>
> :::: warning
> ::: title
> Warning
> :::
>
> This is not compatible with subinterpreters.
> ::::
>
> ::: versionchanged
> 3.15
>
> This macro is now thread safe.
> :::

> Structure containing the fields for the datetime C API.
>
> The fields of this structure are private and subject to change.
>
> Do not use this directly; prefer `PyDateTime_*` APIs instead.

> Dynamically allocated object containing the datetime C API.
>
> This variable is only available once `PyDateTime_IMPORT`{.interpreted-text role="c:macro"} succeeds.
>
> ::: versionchanged
> 3.15
>
> This variable should not be accessed directly as direct access is not thread-safe. Use `PyDateTime_IMPORT`{.interpreted-text role="c:func"} instead.
> :::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python date object.

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python datetime object.

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python time object.

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents the difference between two datetime values.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python date type; it is the same object as `datetime.date`{.interpreted-text role="class"} in the Python layer.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python datetime type; it is the same object as `datetime.datetime`{.interpreted-text role="class"} in the Python layer.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python time type; it is the same object as `datetime.time`{.interpreted-text role="class"} in the Python layer.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python type for the difference between two datetime values; it is the same object as `datetime.timedelta`{.interpreted-text role="class"} in the Python layer.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python time zone info type; it is the same object as `datetime.tzinfo`{.interpreted-text role="class"} in the Python layer.

Macro for access to the UTC singleton:

> Returns the time zone singleton representing UTC, the same object as `datetime.timezone.utc`{.interpreted-text role="attr"}.
>
> ::: versionadded
> 3.7
> :::

Type-check macros:

> Return true if *ob* is of type `PyDateTime_DateType`{.interpreted-text role="c:data"} or a subtype of `!PyDateTime_DateType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_DateType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_DateTimeType`{.interpreted-text role="c:data"} or a subtype of `!PyDateTime_DateTimeType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_DateTimeType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_TimeType`{.interpreted-text role="c:data"} or a subtype of `!PyDateTime_TimeType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_TimeType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_DeltaType`{.interpreted-text role="c:data"} or a subtype of `!PyDateTime_DeltaType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_DeltaType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_TZInfoType`{.interpreted-text role="c:data"} or a subtype of `!PyDateTime_TZInfoType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob* is of type `PyDateTime_TZInfoType`{.interpreted-text role="c:data"}. *ob* must not be `NULL`. This function always succeeds.

Macros to create objects:

> Return a `datetime.date`{.interpreted-text role="class"} object with the specified year, month and day.

> Return a `datetime.datetime`{.interpreted-text role="class"} object with the specified year, month, day, hour, minute, second and microsecond.

> Return a `datetime.datetime`{.interpreted-text role="class"} object with the specified year, month, day, hour, minute, second, microsecond and fold.
>
> ::: versionadded
> 3.6
> :::

> Return a `datetime.time`{.interpreted-text role="class"} object with the specified hour, minute, second and microsecond.

> Return a `datetime.time`{.interpreted-text role="class"} object with the specified hour, minute, second, microsecond and fold.
>
> ::: versionadded
> 3.6
> :::

> Return a `datetime.timedelta`{.interpreted-text role="class"} object representing the given number of days, seconds and microseconds. Normalization is performed so that the resulting number of microseconds and seconds lie in the ranges documented for `datetime.timedelta`{.interpreted-text role="class"} objects.

> Return a `datetime.timezone`{.interpreted-text role="class"} object with an unnamed fixed offset represented by the *offset* argument.
>
> ::: versionadded
> 3.7
> :::

> Return a `datetime.timezone`{.interpreted-text role="class"} object with a fixed offset represented by the *offset* argument and with tzname *name*.
>
> ::: versionadded
> 3.7
> :::

Macros to extract fields from date objects. The argument must be an instance of `PyDateTime_Date`{.interpreted-text role="c:type"}, including subclasses (such as `PyDateTime_DateTime`{.interpreted-text role="c:type"}). The argument must not be `NULL`, and the type is not checked:

> Return the year, as a positive int.

> Return the month, as an int from 1 through 12.

> Return the day, as an int from 1 through 31.

Macros to extract fields from datetime objects. The argument must be an instance of `PyDateTime_DateTime`{.interpreted-text role="c:type"}, including subclasses. The argument must not be `NULL`, and the type is not checked:

> Return the hour, as an int from 0 through 23.

> Return the minute, as an int from 0 through 59.

> Return the second, as an int from 0 through 59.

> Return the microsecond, as an int from 0 through 999999.

> Return the fold, as an int from 0 through 1.
>
> ::: versionadded
> 3.6
> :::

> Return the tzinfo (which may be `None`).
>
> ::: versionadded
> 3.10
> :::

Macros to extract fields from time objects. The argument must be an instance of `PyDateTime_Time`{.interpreted-text role="c:type"}, including subclasses. The argument must not be `NULL`, and the type is not checked:

> Return the hour, as an int from 0 through 23.

> Return the minute, as an int from 0 through 59.

> Return the second, as an int from 0 through 59.

> Return the microsecond, as an int from 0 through 999999.

> Return the fold, as an int from 0 through 1.
>
> ::: versionadded
> 3.6
> :::

> Return the tzinfo (which may be `None`).
>
> ::: versionadded
> 3.10
> :::

Macros to extract fields from time delta objects. The argument must be an instance of `PyDateTime_Delta`{.interpreted-text role="c:type"}, including subclasses. The argument must not be `NULL`, and the type is not checked:

> Return the number of days, as an int from -999999999 to 999999999.
>
> ::: versionadded
> 3.3
> :::

> Return the number of seconds, as an int from 0 through 86399.
>
> ::: versionadded
> 3.3
> :::

> Return the number of microseconds, as an int from 0 through 999999.
>
> ::: versionadded
> 3.3
> :::

Macros for the convenience of modules implementing the DB API:

> Create and return a new `datetime.datetime`{.interpreted-text role="class"} object given an argument tuple suitable for passing to `datetime.datetime.fromtimestamp`{.interpreted-text role="meth"}.

> Create and return a new `datetime.date`{.interpreted-text role="class"} object given an argument tuple suitable for passing to `datetime.date.fromtimestamp`{.interpreted-text role="meth"}.

# Internal data

The following symbols are exposed by the C API but should be considered internal-only.

> Name of the datetime capsule to pass to `PyCapsule_Import`{.interpreted-text role="c:func"}.
>
> Internal usage only. Use `PyDateTime_IMPORT`{.interpreted-text role="c:macro"} instead.
