# `!datetime`{.interpreted-text role="mod"} \-\-- Basic date and time types

::: {.module synopsis="Basic date and time types."}
datetime
:::

**Source code:** `Lib/datetime.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!datetime`{.interpreted-text role="mod"} module supplies classes for manipulating dates and times.

While date and time arithmetic is supported, the focus of the implementation is on efficient attribute extraction for output formatting and manipulation.

:::: tip
::: title
Tip
:::

Skip to `the format codes <format-codes>`{.interpreted-text role="ref"}.
::::

::: seealso

Module `calendar`{.interpreted-text role="mod"}

:   General calendar related functions.

Module `time`{.interpreted-text role="mod"}

:   Time access and conversions.

Module `zoneinfo`{.interpreted-text role="mod"}

:   Concrete time zones representing the IANA time zone database.

Package [dateutil](https://dateutil.readthedocs.io/en/stable/)

:   Third-party library with expanded time zone and parsing support.

Package `DateType`{.interpreted-text role="pypi"}

:   Third-party library that introduces distinct static types to for example, allow `static type checkers <static type checker>`{.interpreted-text role="term"} to differentiate between naive and aware datetimes.
:::

## Aware and naive objects {#datetime-naive-aware}

Date and time objects may be categorized as \"aware\" or \"naive\" depending on whether or not they include time zone information.

With sufficient knowledge of applicable algorithmic and political time adjustments, such as time zone and daylight saving time information, an **aware** object can locate itself relative to other aware objects. An aware object represents a specific moment in time that is not open to interpretation.[^1]

A **naive** object does not contain enough information to unambiguously locate itself relative to other date/time objects. Whether a naive object represents Coordinated Universal Time (UTC), local time, or time in some other time zone is purely up to the program, just like it is up to the program whether a particular number represents metres, miles, or mass. Naive objects are easy to understand and to work with, at the cost of ignoring some aspects of reality.

For applications requiring aware objects, `.datetime`{.interpreted-text role="class"} and `.time`{.interpreted-text role="class"} objects have an optional time zone information attribute, `!tzinfo`{.interpreted-text role="attr"}, that can be set to an instance of a subclass of the abstract `tzinfo`{.interpreted-text role="class"} class. These `tzinfo`{.interpreted-text role="class"} objects capture information about the offset from UTC time, the time zone name, and whether daylight saving time is in effect.

Only one concrete `tzinfo`{.interpreted-text role="class"} class, the `timezone`{.interpreted-text role="class"} class, is supplied by the `!datetime`{.interpreted-text role="mod"} module. The `!timezone`{.interpreted-text role="class"} class can represent simple time zones with fixed offsets from UTC, such as UTC itself or North American EST and EDT time zones. Supporting time zones at deeper levels of detail is up to the application. The rules for time adjustment across the world are more political than rational, change frequently, and there is no standard suitable for every application aside from UTC.

## Constants

The `!datetime`{.interpreted-text role="mod"} module exports the following constants:

::: data
MINYEAR

The smallest year number allowed in a `date`{.interpreted-text role="class"} or `.datetime`{.interpreted-text role="class"} object. `MINYEAR`{.interpreted-text role="const"} is 1.
:::

::: data
MAXYEAR

The largest year number allowed in a `date`{.interpreted-text role="class"} or `.datetime`{.interpreted-text role="class"} object. `MAXYEAR`{.interpreted-text role="const"} is 9999.
:::

:::: data
UTC

Alias for the UTC time zone singleton `datetime.timezone.utc`{.interpreted-text role="attr"}.

::: versionadded
3.11
:::
::::

## Available types

::: {.date noindex=""}
An idealized naive date, assuming the current Gregorian calendar always was, and always will be, in effect. Attributes: `year`{.interpreted-text role="attr"}, `month`{.interpreted-text role="attr"}, and `day`{.interpreted-text role="attr"}.
:::

::: {.time noindex=""}
An idealized time, independent of any particular day, assuming that every day has exactly 24\*60\*60 seconds. (There is no notion of \"leap seconds\" here.) Attributes: `hour`{.interpreted-text role="attr"}, `minute`{.interpreted-text role="attr"}, `second`{.interpreted-text role="attr"}, `microsecond`{.interpreted-text role="attr"}, and `.tzinfo`{.interpreted-text role="attr"}.
:::

::: {.datetime noindex=""}
A combination of a date and a time. Attributes: `year`{.interpreted-text role="attr"}, `month`{.interpreted-text role="attr"}, `day`{.interpreted-text role="attr"}, `hour`{.interpreted-text role="attr"}, `minute`{.interpreted-text role="attr"}, `second`{.interpreted-text role="attr"}, `microsecond`{.interpreted-text role="attr"}, and `.tzinfo`{.interpreted-text role="attr"}.
:::

::: {.timedelta noindex=""}
A duration expressing the difference between two `.datetime`{.interpreted-text role="class"} or `date`{.interpreted-text role="class"} instances to microsecond resolution.
:::

::: {.tzinfo noindex=""}
An abstract base class for time zone information objects. These are used by the `.datetime`{.interpreted-text role="class"} and `.time`{.interpreted-text role="class"} classes to provide a customizable notion of time adjustment (for example, to account for time zone and/or daylight saving time).
:::

:::: {.timezone noindex=""}
A class that implements the `tzinfo`{.interpreted-text role="class"} abstract base class as a fixed offset from the UTC.

::: versionadded
3.2
:::
::::

Objects of these types are immutable.

Subclass relationships:

<figure class="invert-in-dark-modealign-center">
<img src="datetime-inheritance.svg" class="invert-in-dark-mode" alt="timedelta, tzinfo, time, and date inherit from object; timezone inherits from tzinfo; and datetime inherits from date." />
</figure>

### Common properties

The `date`{.interpreted-text role="class"}, `.datetime`{.interpreted-text role="class"}, `.time`{.interpreted-text role="class"}, and `timezone`{.interpreted-text role="class"} types share these common features:

- Objects of these types are immutable.
- Objects of these types are `hashable`{.interpreted-text role="term"}, meaning that they can be used as dictionary keys.
- Objects of these types support efficient pickling via the `pickle`{.interpreted-text role="mod"} module.

### Determining if an object is aware or naive

Objects of the `date`{.interpreted-text role="class"} type are always naive.

An object of type `.time`{.interpreted-text role="class"} or `.datetime`{.interpreted-text role="class"} may be aware or naive.

A `.datetime`{.interpreted-text role="class"} object `d` is aware if both of the following hold:

1.  `d.tzinfo` is not `None`
2.  `d.tzinfo.utcoffset(d)` does not return `None`

Otherwise, `d` is naive.

A `.time`{.interpreted-text role="class"} object `t` is aware if both of the following hold:

1.  `t.tzinfo` is not `None`
2.  `t.tzinfo.utcoffset(None)` does not return `None`.

Otherwise, `t` is naive.

The distinction between aware and naive doesn\'t apply to `timedelta`{.interpreted-text role="class"} objects.

## `!timedelta`{.interpreted-text role="class"} objects {#datetime-timedelta}

A `timedelta`{.interpreted-text role="class"} object represents a duration, the difference between two `.datetime`{.interpreted-text role="class"} or `date`{.interpreted-text role="class"} instances.

::: {.timedelta(days=0, .seconds=0, .microseconds=0, .milliseconds=0, .minutes=0, .hours=0, .weeks=0)}
All arguments are optional and default to 0. Arguments may be integers or floats, and may be positive or negative.

Only *days*, *seconds* and *microseconds* are stored internally. Arguments are converted to those units:

- A millisecond is converted to 1000 microseconds.
- A minute is converted to 60 seconds.
- An hour is converted to 3600 seconds.
- A week is converted to 7 days.

and days, seconds and microseconds are then normalized so that the representation is unique, with

- `0 <= microseconds < 1000000`
- `0 <= seconds < 3600*24` (the number of seconds in one day)
- `-999999999 <= days <= 999999999`

The following example illustrates how any arguments besides *days*, *seconds* and *microseconds* are \"merged\" and normalized into those three resulting attributes:

    >>> from datetime import timedelta
    >>> delta = timedelta(
    ...     days=50,
    ...     seconds=27,
    ...     microseconds=10,
    ...     milliseconds=29000,
    ...     minutes=5,
    ...     hours=8,
    ...     weeks=2
    ... )
    >>> # Only days, seconds, and microseconds remain
    >>> delta
    datetime.timedelta(days=64, seconds=29156, microseconds=10)

If any argument is a float and there are fractional microseconds, the fractional microseconds left over from all arguments are combined and their sum is rounded to the nearest microsecond using round-half-to-even tiebreaker. If no argument is a float, the conversion and normalization processes are exact (no information is lost).

If the normalized value of days lies outside the indicated range, `OverflowError`{.interpreted-text role="exc"} is raised.

Note that normalization of negative values may be surprising at first. For example:

    >>> from datetime import timedelta
    >>> d = timedelta(microseconds=-1)
    >>> (d.days, d.seconds, d.microseconds)
    (-1, 86399, 999999)

Since the string representation of `!timedelta`{.interpreted-text role="class"} objects can be confusing, use the following recipe to produce a more readable format:

``` pycon
>>> def pretty_timedelta(td):
...     if td.days >= 0:
...         return str(td)
...     return f'-({-td!s})'
...
>>> d = timedelta(hours=-1)
>>> str(d)  # not human-friendly
'-1 day, 23:00:00'
>>> pretty_timedelta(d)
'-(1:00:00)'
```
:::

Class attributes:

::: attribute
timedelta.min

The most negative `timedelta`{.interpreted-text role="class"} object, `timedelta(-999999999)`.
:::

::: attribute
timedelta.max

The most positive `timedelta`{.interpreted-text role="class"} object, `timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)`.
:::

::: attribute
timedelta.resolution

The smallest possible difference between non-equal `timedelta`{.interpreted-text role="class"} objects, `timedelta(microseconds=1)`.
:::

Note that, because of normalization, `timedelta.max` is greater than `-timedelta.min`. `-timedelta.max` is not representable as a `timedelta`{.interpreted-text role="class"} object.

Instance attributes (read-only):

::: attribute
timedelta.days

Between -999,999,999 and 999,999,999 inclusive.
:::

:::::: attribute
timedelta.seconds

Between 0 and 86,399 inclusive.

::::: caution
::: title
Caution
:::

It is a somewhat common bug for code to unintentionally use this attribute when it is actually intended to get a `~timedelta.total_seconds`{.interpreted-text role="meth"} value instead:

::: doctest
\>\>\> from datetime import timedelta \>\>\> duration = timedelta(seconds=11235813) \>\>\> duration.days, duration.seconds (130, 3813) \>\>\> duration.total_seconds() 11235813.0
:::
:::::
::::::

::: attribute
timedelta.microseconds

Between 0 and 999,999 inclusive.
:::

Supported operations:

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Operation                           Result
  ----------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `t1 = t2 + t3`                      Sum of `t2` and `t3`. Afterwards `t1 - t2 == t3` and `t1 - t3 == t2` are true. (1)

  `t1 = t2 - t3`                      Difference of `t2` and `t3`. Afterwards `t1 == t2 - t3` and `t2 == t1 + t3` are true. (1)(6)

  `t1 = t2 * i or t1 = i * t2`        Delta multiplied by an integer. Afterwards `t1 // i == t2` is true, provided `i != 0`.

                                      In general, `t1  * i == t1 * (i-1) + t1` is true. (1)

  `t1 = t2 * f or t1 = f * t2`        Delta multiplied by a float. The result is rounded to the nearest multiple of timedelta.resolution using round-half-to-even.

  `f = t2 / t3`                       Division (3) of overall duration `t2` by interval unit `t3`. Returns a `float`{.interpreted-text role="class"} object.

  `t1 = t2 / f or t1 = t2 / i`        Delta divided by a float or an int. The result is rounded to the nearest multiple of timedelta.resolution using round-half-to-even.

  `t1 = t2 // i` or `t1 = t2 // t3`   The floor is computed and the remainder (if any) is thrown away. In the second case, an integer is returned. (3)

  `t1 = t2 % t3`                      The remainder is computed as a `timedelta`{.interpreted-text role="class"} object. (3)

  `q, r = divmod(t1, t2)`             Computes the quotient and the remainder: `q = t1 // t2` (3) and `r = t1 % t2`. `q` is an integer and `r` is a `timedelta`{.interpreted-text role="class"} object.

  `+t1`                               Returns a `timedelta`{.interpreted-text role="class"} object with the same value. (2)

  `-t1`                               Equivalent to `timedelta(-t1.days, -t1.seconds, -t1.microseconds)`, and to `t1 * -1`. (1)(4)

  `abs(t)`                            Equivalent to `+t` when `t.days >= 0`, and to `-t` when `t.days < 0`. (2)

  `str(t)`                            Returns a string in the form `[D day[s], ][H]H:MM:SS[.UUUUUU]`, where D is negative for negative `t`. (5)

  `repr(t)`                           Returns a string representation of the `timedelta`{.interpreted-text role="class"} object as a constructor call with canonical attribute values.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Notes:

\(1\)

:   This is exact but may overflow.

\(2\)

:   This is exact and cannot overflow.

\(3\)

:   Division by zero raises `ZeroDivisionError`{.interpreted-text role="exc"}.

\(4\)

:   `-timedelta.max` is not representable as a `timedelta`{.interpreted-text role="class"} object.

\(5\)

:   String representations of `timedelta`{.interpreted-text role="class"} objects are normalized similarly to their internal representation. This leads to somewhat unusual results for negative timedeltas. For example:

        >>> timedelta(hours=-5)
        datetime.timedelta(days=-1, seconds=68400)
        >>> print(_)
        -1 day, 19:00:00

\(6\)

:   The expression `t2 - t3` will always be equal to the expression `t2 + (-t3)` except when t3 is equal to `timedelta.max`; in that case the former will produce a result while the latter will overflow.

In addition to the operations listed above, `timedelta`{.interpreted-text role="class"} objects support certain additions and subtractions with `date`{.interpreted-text role="class"} and `.datetime`{.interpreted-text role="class"} objects (see below).

::: versionchanged
3.2 Floor division and true division of a `timedelta`{.interpreted-text role="class"} object by another `timedelta`{.interpreted-text role="class"} object are now supported, as are remainder operations and the `divmod`{.interpreted-text role="func"} function. True division and multiplication of a `timedelta`{.interpreted-text role="class"} object by a `float`{.interpreted-text role="class"} object are now supported.
:::

`timedelta`{.interpreted-text role="class"} objects support equality and order comparisons.

In Boolean contexts, a `timedelta`{.interpreted-text role="class"} object is considered to be true if and only if it isn\'t equal to `timedelta(0)`.

Instance methods:

:::: method
timedelta.total_seconds()

Return the total number of seconds contained in the duration. Equivalent to `td / timedelta(seconds=1)`. For interval units other than seconds, use the division form directly (for example, `td / timedelta(microseconds=1)`).

Note that for very large time intervals (greater than 270 years on most platforms) this method will lose microsecond accuracy.

::: versionadded
3.2
:::
::::

### Examples of usage: `!timedelta`{.interpreted-text role="class"}

An additional example of normalization:

    >>> # Components of another_year add up to exactly 365 days
    >>> from datetime import timedelta
    >>> year = timedelta(days=365)
    >>> another_year = timedelta(weeks=40, days=84, hours=23,
    ...                          minutes=50, seconds=600)
    >>> year == another_year
    True
    >>> year.total_seconds()
    31536000.0

Examples of `timedelta`{.interpreted-text role="class"} arithmetic:

    >>> from datetime import timedelta
    >>> year = timedelta(days=365)
    >>> ten_years = 10 * year
    >>> ten_years
    datetime.timedelta(days=3650)
    >>> ten_years.days // 365
    10
    >>> nine_years = ten_years - year
    >>> nine_years
    datetime.timedelta(days=3285)
    >>> three_years = nine_years // 3
    >>> three_years, three_years.days // 365
    (datetime.timedelta(days=1095), 3)

## `!date`{.interpreted-text role="class"} objects {#datetime-date}

A `date`{.interpreted-text role="class"} object represents a date (year, month and day) in an idealized calendar, the current Gregorian calendar indefinitely extended in both directions.

January 1 of year 1 is called day number 1, January 2 of year 1 is called day number 2, and so on.[^2]

::: {.date(year, .month, .day)}
All arguments are required. Arguments must be integers, in the following ranges:

- `MINYEAR <= year <= MAXYEAR`
- `1 <= month <= 12`
- `1 <= day <= number of days in the given month and year`

If an argument outside those ranges is given, `ValueError`{.interpreted-text role="exc"} is raised.
:::

Other constructors, all class methods:

::: classmethod
date.today()

Return the current local date.

This is equivalent to `date.fromtimestamp(time.time())`.
:::

::::: classmethod
date.fromtimestamp(timestamp)

Return the local date corresponding to the POSIX *timestamp*, such as is returned by `time.time`{.interpreted-text role="func"}.

This may raise `OverflowError`{.interpreted-text role="exc"}, if the timestamp is out of the range of values supported by the platform C `localtime`{.interpreted-text role="c:func"} function, and `OSError`{.interpreted-text role="exc"} on `localtime`{.interpreted-text role="c:func"} failure. It\'s common for this to be restricted to years from 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by `fromtimestamp`{.interpreted-text role="meth"}.

::: versionchanged
3.3 Raise `OverflowError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} if the timestamp is out of the range of values supported by the platform C `localtime`{.interpreted-text role="c:func"} function. Raise `OSError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} on `localtime`{.interpreted-text role="c:func"} failure.
:::

::: versionchanged
3.15 Accepts any real number as *timestamp*, not only integer or float.
:::
:::::

::: classmethod
date.fromordinal(ordinal)

Return the date corresponding to the proleptic Gregorian *ordinal*, where January 1 of year 1 has ordinal 1.

`ValueError`{.interpreted-text role="exc"} is raised unless `1 <= ordinal <= date.max.toordinal()`. For any date `d`, `date.fromordinal(d.toordinal()) == d`.
:::

::::: classmethod
date.fromisoformat(date_string)

Return a `date`{.interpreted-text role="class"} corresponding to a *date_string* given in any valid ISO 8601 format, with the following exceptions:

1.  Reduced precision dates are not currently supported (`YYYY-MM`, `YYYY`).
2.  Extended date representations are not currently supported (`±YYYYYY-MM-DD`).
3.  Ordinal dates are not currently supported (`YYYY-OOO`).

Examples:

    >>> from datetime import date
    >>> date.fromisoformat('2019-12-04')
    datetime.date(2019, 12, 4)
    >>> date.fromisoformat('20191204')
    datetime.date(2019, 12, 4)
    >>> date.fromisoformat('2021-W01-1')
    datetime.date(2021, 1, 4)

::: versionadded
3.7
:::

::: versionchanged
3.11 Previously, this method only supported the format `YYYY-MM-DD`.
:::
:::::

:::: classmethod
date.fromisocalendar(year, week, day)

Return a `date`{.interpreted-text role="class"} corresponding to the ISO calendar date specified by *year*, *week* and *day*. This is the inverse of the function `date.isocalendar`{.interpreted-text role="meth"}.

::: versionadded
3.8
:::
::::

::::::: classmethod
date.strptime(date_string, format)

Return a `.date`{.interpreted-text role="class"} corresponding to *date_string*, parsed according to *format*. This is equivalent to:

    date(*(time.strptime(date_string, format)[0:3]))

`ValueError`{.interpreted-text role="exc"} is raised if the date_string and format can\'t be parsed by `time.strptime`{.interpreted-text role="func"} or if it returns a value which isn\'t a time tuple. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `date.fromisoformat`{.interpreted-text role="meth"}.

::::: note
::: title
Note
:::

If *format* specifies a day of month without a year a `DeprecationWarning`{.interpreted-text role="exc"} is emitted. This is to avoid a quadrennial leap year bug in code seeking to parse only a month and day as the default year used in absence of one in the format is not a leap year. Such *format* values may raise an error as of Python 3.15. The workaround is to always include a year in your *format*. If parsing *date_string* values that do not have a year, explicitly add a year that is a leap year before parsing:

::: doctest
\>\>\> from datetime import date \>\>\> date_string = \"02/29\" \>\>\> when = date.strptime(f\"{date_string};1984\", \"%m/%d;%Y\") \# Avoids leap year bug. \>\>\> when.strftime(\"%B %d\") \# doctest: +SKIP \'February 29\'
:::
:::::

::: versionadded
3.14
:::
:::::::

Class attributes:

::: attribute
date.min

The earliest representable date, `date(MINYEAR, 1, 1)`.
:::

::: attribute
date.max

The latest representable date, `date(MAXYEAR, 12, 31)`.
:::

::: attribute
date.resolution

The smallest possible difference between non-equal date objects, `timedelta(days=1)`.
:::

Instance attributes (read-only):

::: attribute
date.year

Between `MINYEAR`{.interpreted-text role="const"} and `MAXYEAR`{.interpreted-text role="const"} inclusive.
:::

::: attribute
date.month

Between 1 and 12 inclusive.
:::

::: attribute
date.day

Between 1 and the number of days in the given month of the given year.
:::

Supported operations:

+-----------------------------+--------------------------------------------------------------+
| Operation                   | Result                                                       |
+=============================+==============================================================+
| `date2 = date1 + timedelta` | `date2` will be `timedelta.days` days after `date1`. (1)     |
+-----------------------------+--------------------------------------------------------------+
| `date2 = date1 - timedelta` | Computes `date2` such that `date2 + timedelta == date1`. (2) |
+-----------------------------+--------------------------------------------------------------+
| `timedelta = date1 - date2` | \(3\)                                                        |
+-----------------------------+--------------------------------------------------------------+
| | `date1 == date2`          | Equality comparison. (4)                                     |
| | `date1 != date2`          |                                                              |
+-----------------------------+--------------------------------------------------------------+
| | `date1 < date2`           | Order comparison. (5)                                        |
| | `date1 > date2`           |                                                              |
| | `date1 <= date2`          |                                                              |
| | `date1 >= date2`          |                                                              |
+-----------------------------+--------------------------------------------------------------+

Notes:

\(1\)

:   *date2* is moved forward in time if `timedelta.days > 0`, or backward if `timedelta.days < 0`. Afterward `date2 - date1 == timedelta.days`. `timedelta.seconds` and `timedelta.microseconds` are ignored. `OverflowError`{.interpreted-text role="exc"} is raised if `date2.year` would be smaller than `MINYEAR`{.interpreted-text role="const"} or larger than `MAXYEAR`{.interpreted-text role="const"}.

\(2\)

:   `timedelta.seconds` and `timedelta.microseconds` are ignored.

\(3\)

:   This is exact, and cannot overflow. `timedelta.seconds` and `timedelta.microseconds` are 0, and `date2 + timedelta == date1` after.

\(4\)

:   `date`{.interpreted-text role="class"} objects are equal if they represent the same date.

    `!date`{.interpreted-text role="class"} objects that are not also `.datetime`{.interpreted-text role="class"} instances are never equal to `!datetime`{.interpreted-text role="class"} objects, even if they represent the same date.

\(5\)

:   *date1* is considered less than *date2* when *date1* precedes *date2* in time. In other words, `date1 < date2` if and only if `date1.toordinal() < date2.toordinal()`.

    Order comparison between a `!date`{.interpreted-text role="class"} object that is not also a `.datetime`{.interpreted-text role="class"} instance and a `!datetime`{.interpreted-text role="class"} object raises `TypeError`{.interpreted-text role="exc"}.

::: versionchanged
3.13 Comparison between `.datetime`{.interpreted-text role="class"} object and an instance of the `date`{.interpreted-text role="class"} subclass that is not a `!datetime`{.interpreted-text role="class"} subclass no longer converts the latter to `!date`{.interpreted-text role="class"}, ignoring the time part and the time zone. The default behavior can be changed by overriding the special comparison methods in subclasses.
:::

In Boolean contexts, all `date`{.interpreted-text role="class"} objects are considered to be true.

Instance methods:

::: method
date.replace(year=self.year, month=self.month, day=self.day)

Return a new `date`{.interpreted-text role="class"} object with the same values, but with specified parameters updated.

Example:

    >>> from datetime import date
    >>> d = date(2002, 12, 31)
    >>> d.replace(day=26)
    datetime.date(2002, 12, 26)

The generic function `copy.replace`{.interpreted-text role="func"} also supports `date`{.interpreted-text role="class"} objects.
:::

::: method
date.timetuple()

Return a `time.struct_time`{.interpreted-text role="class"} such as returned by `time.localtime`{.interpreted-text role="func"}.

The hours, minutes and seconds are 0, and the DST flag is -1.

`d.timetuple()` is equivalent to:

    time.struct_time((d.year, d.month, d.day, 0, 0, 0, d.weekday(), yday, -1))

where `yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1` is the day number within the current year starting with 1 for January 1st.
:::

::: method
date.toordinal()

Return the proleptic Gregorian ordinal of the date, where January 1 of year 1 has ordinal 1. For any `date`{.interpreted-text role="class"} object `d`, `date.fromordinal(d.toordinal()) == d`.
:::

::: method
date.weekday()

Return the day of the week as an integer, where Monday is 0 and Sunday is 6. For example, `date(2002, 12, 4).weekday() == 2`, a Wednesday. See also `isoweekday`{.interpreted-text role="meth"}.
:::

::: method
date.isoweekday()

Return the day of the week as an integer, where Monday is 1 and Sunday is 7. For example, `date(2002, 12, 4).isoweekday() == 3`, a Wednesday. See also `weekday`{.interpreted-text role="meth"}, `isocalendar`{.interpreted-text role="meth"}.
:::

:::: method
date.isocalendar()

Return a `named tuple`{.interpreted-text role="term"} object with three components: `year`, `week` and `weekday`.

The ISO calendar is a widely used variant of the Gregorian calendar.[^3]

The ISO year consists of 52 or 53 full weeks, and where a week starts on a Monday and ends on a Sunday. The first week of an ISO year is the first (Gregorian) calendar week of a year containing a Thursday. This is called week number 1, and the ISO year of that Thursday is the same as its Gregorian year.

For example, 2004 begins on a Thursday, so the first week of ISO year 2004 begins on Monday, 29 Dec 2003 and ends on Sunday, 4 Jan 2004:

    >>> from datetime import date
    >>> date(2003, 12, 29).isocalendar()
    datetime.IsoCalendarDate(year=2004, week=1, weekday=1)
    >>> date(2004, 1, 4).isocalendar()
    datetime.IsoCalendarDate(year=2004, week=1, weekday=7)

::: versionchanged
3.9 Result changed from a tuple to a `named tuple`{.interpreted-text role="term"}.
:::
::::

::: method
date.isoformat()

Return a string representing the date in ISO 8601 format, `YYYY-MM-DD`:

    >>> from datetime import date
    >>> date(2002, 12, 4).isoformat()
    '2002-12-04'
:::

::: method
date.\_\_str\_\_()

For a date `d`, `str(d)` is equivalent to `d.isoformat()`.
:::

::: method
date.ctime()

Return a string representing the date:

    >>> from datetime import date
    >>> date(2002, 12, 4).ctime()
    'Wed Dec  4 00:00:00 2002'

`d.ctime()` is equivalent to:

    time.ctime(time.mktime(d.timetuple()))

on platforms where the native C `ctime`{.interpreted-text role="c:func"} function (which `time.ctime`{.interpreted-text role="func"} invokes, but which `date.ctime`{.interpreted-text role="meth"} does not invoke) conforms to the C standard.
:::

::: method
date.strftime(format)

Return a string representing the date, controlled by an explicit format string. Format codes referring to hours, minutes or seconds will see 0 values. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `date.isoformat`{.interpreted-text role="meth"}.
:::

::: method
date.\_\_format\_\_(format)

Same as `.date.strftime`{.interpreted-text role="meth"}. This makes it possible to specify a format string for a `.date`{.interpreted-text role="class"} object in `formatted string
literals <f-strings>`{.interpreted-text role="ref"} and when using `str.format`{.interpreted-text role="meth"}. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `date.isoformat`{.interpreted-text role="meth"}.
:::

### Examples of usage: `!date`{.interpreted-text role="class"}

Example of counting days to an event:

    >>> import time
    >>> from datetime import date
    >>> today = date.today()
    >>> today
    datetime.date(2007, 12, 5)
    >>> today == date.fromtimestamp(time.time())
    True
    >>> my_birthday = date(today.year, 6, 24)
    >>> if my_birthday < today:
    ...     my_birthday = my_birthday.replace(year=today.year + 1)
    ...
    >>> my_birthday
    datetime.date(2008, 6, 24)
    >>> time_to_birthday = abs(my_birthday - today)
    >>> time_to_birthday.days
    202

More examples of working with `date`{.interpreted-text role="class"}:

::: doctest
\>\>\> from datetime import date \>\>\> d = date.fromordinal(730920) \# 730920th day after 1. 1. 0001 \>\>\> d datetime.date(2002, 3, 11)

\>\>\> \# Methods related to formatting string output \>\>\> d.isoformat() \'2002-03-11\' \>\>\> d.strftime(\"%d/%m/%y\") \'11/03/02\' \>\>\> d.strftime(\"%A %d. %B %Y\") \'Monday 11. March 2002\' \>\>\> d.ctime() \'Mon Mar 11 00:00:00 2002\' \>\>\> \'The {1} is {0:%d}, the {2} is {0:%B}.\'.format(d, \"day\", \"month\") \'The day is 11, the month is March.\'

\>\>\> \# Methods for extracting \'components\' under different calendars \>\>\> t = d.timetuple() \>\>\> for i in t: \# doctest: +SKIP \... print(i) 2002 \# year 3 \# month 11 \# day 0 0 0 0 \# weekday (0 = Monday) 70 \# 70th day in the year -1 \>\>\> ic = d.isocalendar() \>\>\> for i in ic: \# doctest: +SKIP \... print(i) 2002 \# ISO year 11 \# ISO week number 1 \# ISO day number ( 1 = Monday )

\>\>\> \# A date object is immutable; all operations produce a new object \>\>\> d.replace(year=2005) datetime.date(2005, 3, 11)
:::

## `!datetime`{.interpreted-text role="class"} objects {#datetime-datetime}

A `.datetime`{.interpreted-text role="class"} object is a single object containing all the information from a `date`{.interpreted-text role="class"} object and a `.time`{.interpreted-text role="class"} object.

Like a `date`{.interpreted-text role="class"} object, `.datetime`{.interpreted-text role="class"} assumes the current Gregorian calendar extended in both directions; like a `.time`{.interpreted-text role="class"} object, `.datetime`{.interpreted-text role="class"} assumes there are exactly 3600\*24 seconds in every day.

Constructor:

:::: {.datetime(year, .month, .day, .hour=0, .minute=0, .second=0, .microsecond=0, .tzinfo=None, .*, .fold=0)}
The *year*, *month* and *day* arguments are required. *tzinfo* may be `None`, or an instance of a `tzinfo`{.interpreted-text role="class"} subclass. The remaining arguments must be integers in the following ranges:

- `MINYEAR <= year <= MAXYEAR`,
- `1 <= month <= 12`,
- `1 <= day <= number of days in the given month and year`,
- `0 <= hour < 24`,
- `0 <= minute < 60`,
- `0 <= second < 60`,
- `0 <= microsecond < 1000000`,
- `fold in [0, 1]`.

If an argument outside those ranges is given, `ValueError`{.interpreted-text role="exc"} is raised.

::: versionchanged
3.6 Added the *fold* parameter.
:::
::::

Other constructors, all class methods:

::: classmethod
datetime.today()

Return the current local date and time, with `.tzinfo`{.interpreted-text role="attr"} `None`.

Equivalent to:

    datetime.fromtimestamp(time.time())

See also `now`{.interpreted-text role="meth"}, `fromtimestamp`{.interpreted-text role="meth"}.

This method is functionally equivalent to `now`{.interpreted-text role="meth"}, but without a `tz` parameter.
:::

::::: classmethod
datetime.now(tz=None)

Return the current local date and time.

If optional argument *tz* is `None` or not specified, this is like `today`{.interpreted-text role="meth"}, but, if possible, supplies more precision than can be gotten from going through a `time.time`{.interpreted-text role="func"} timestamp (for example, this may be possible on platforms supplying the C `gettimeofday`{.interpreted-text role="c:func"} function).

If *tz* is not `None`, it must be an instance of a `tzinfo`{.interpreted-text role="class"} subclass, and the current date and time are converted to *tz*'s time zone.

This function is preferred over `today`{.interpreted-text role="meth"} and `utcnow`{.interpreted-text role="meth"}.

:::: note
::: title
Note
:::

Subsequent calls to `!datetime.now`{.interpreted-text role="meth"} may return the same instant depending on the precision of the underlying clock.
::::
:::::

:::::: classmethod
datetime.utcnow()

Return the current UTC date and time, with `.tzinfo`{.interpreted-text role="attr"} `None`.

This is like `now`{.interpreted-text role="meth"}, but returns the current UTC date and time, as a naive `.datetime`{.interpreted-text role="class"} object. An aware current UTC datetime can be obtained by calling `datetime.now(timezone.utc)`. See also `now`{.interpreted-text role="meth"}.

:::: warning
::: title
Warning
:::

Because naive `datetime` objects are treated by many `datetime` methods as local times, it is preferred to use aware datetimes to represent times in UTC. As such, the recommended way to create an object representing the current time in UTC is by calling `datetime.now(timezone.utc)`.
::::

::: deprecated
3.12

Use `datetime.now`{.interpreted-text role="meth"} with `UTC`{.interpreted-text role="const"} instead.
:::
::::::

:::::: classmethod
datetime.fromtimestamp(timestamp, tz=None)

Return the local date and time corresponding to the POSIX timestamp, such as is returned by `time.time`{.interpreted-text role="func"}. If optional argument *tz* is `None` or not specified, the timestamp is converted to the platform\'s local date and time, and the returned `.datetime`{.interpreted-text role="class"} object is naive.

If *tz* is not `None`, it must be an instance of a `tzinfo`{.interpreted-text role="class"} subclass, and the timestamp is converted to *tz*'s time zone.

`fromtimestamp`{.interpreted-text role="meth"} may raise `OverflowError`{.interpreted-text role="exc"}, if the timestamp is out of the range of values supported by the platform C `localtime`{.interpreted-text role="c:func"} or `gmtime`{.interpreted-text role="c:func"} functions, and `OSError`{.interpreted-text role="exc"} on `localtime`{.interpreted-text role="c:func"} or `gmtime`{.interpreted-text role="c:func"} failure. It\'s common for this to be restricted to years in 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by `fromtimestamp`{.interpreted-text role="meth"}, and then it\'s possible to have two timestamps differing by a second that yield identical `.datetime`{.interpreted-text role="class"} objects. This method is preferred over `utcfromtimestamp`{.interpreted-text role="meth"}.

::: versionchanged
3.3 Raise `OverflowError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} if the timestamp is out of the range of values supported by the platform C `localtime`{.interpreted-text role="c:func"} or `gmtime`{.interpreted-text role="c:func"} functions. Raise `OSError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} on `localtime`{.interpreted-text role="c:func"} or `gmtime`{.interpreted-text role="c:func"} failure.
:::

::: versionchanged
3.6 `fromtimestamp`{.interpreted-text role="meth"} may return instances with `.fold`{.interpreted-text role="attr"} set to 1.
:::

::: versionchanged
3.15 Accepts any real number as *timestamp*, not only integer or float.
:::
::::::

:::::::: classmethod
datetime.utcfromtimestamp(timestamp)

Return the UTC `.datetime`{.interpreted-text role="class"} corresponding to the POSIX timestamp, with `.tzinfo`{.interpreted-text role="attr"} `None`. (The resulting object is naive.)

This may raise `OverflowError`{.interpreted-text role="exc"}, if the timestamp is out of the range of values supported by the platform C `gmtime`{.interpreted-text role="c:func"} function, and `OSError`{.interpreted-text role="exc"} on `gmtime`{.interpreted-text role="c:func"} failure. It\'s common for this to be restricted to years in 1970 through 2038.

To get an aware `.datetime`{.interpreted-text role="class"} object, call `fromtimestamp`{.interpreted-text role="meth"}:

    datetime.fromtimestamp(timestamp, timezone.utc)

On the POSIX compliant platforms, it is equivalent to the following expression:

    datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=timestamp)

except the latter formula always supports the full years range: between `MINYEAR`{.interpreted-text role="const"} and `MAXYEAR`{.interpreted-text role="const"} inclusive.

:::: warning
::: title
Warning
:::

Because naive `datetime` objects are treated by many `datetime` methods as local times, it is preferred to use aware datetimes to represent times in UTC. As such, the recommended way to create an object representing a specific timestamp in UTC is by calling `datetime.fromtimestamp(timestamp, tz=timezone.utc)`.
::::

::: versionchanged
3.3 Raise `OverflowError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} if the timestamp is out of the range of values supported by the platform C `gmtime`{.interpreted-text role="c:func"} function. Raise `OSError`{.interpreted-text role="exc"} instead of `ValueError`{.interpreted-text role="exc"} on `gmtime`{.interpreted-text role="c:func"} failure.
:::

::: versionchanged
3.15 Accepts any real number as *timestamp*, not only integer or float.
:::

::: deprecated
3.12

Use `datetime.fromtimestamp`{.interpreted-text role="meth"} with `UTC`{.interpreted-text role="const"} instead.
:::
::::::::

::: classmethod
datetime.fromordinal(ordinal)

Return the `.datetime`{.interpreted-text role="class"} corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1. `ValueError`{.interpreted-text role="exc"} is raised unless `1 <= ordinal <= datetime.max.toordinal()`. The hour, minute, second and microsecond of the result are all 0, and `.tzinfo`{.interpreted-text role="attr"} is `None`.
:::

:::: classmethod
datetime.combine(date, time, tzinfo=time.tzinfo)

Return a new `.datetime`{.interpreted-text role="class"} object whose date components are equal to the given `date`{.interpreted-text role="class"} object\'s, and whose time components are equal to the given `.time`{.interpreted-text role="class"} object\'s. If the *tzinfo* argument is provided, its value is used to set the `.tzinfo`{.interpreted-text role="attr"} attribute of the result, otherwise the `~.time.tzinfo`{.interpreted-text role="attr"} attribute of the *time* argument is used. If the *date* argument is a `.datetime`{.interpreted-text role="class"} object, its time components and `.tzinfo`{.interpreted-text role="attr"} attributes are ignored.

For any `.datetime`{.interpreted-text role="class"} object `d`, `d == datetime.combine(d.date(), d.time(), d.tzinfo)`.

::: versionchanged
3.6 Added the *tzinfo* argument.
:::
::::

::::: classmethod
datetime.fromisoformat(date_string)

Return a `.datetime`{.interpreted-text role="class"} corresponding to a *date_string* in any valid ISO 8601 format, with the following exceptions:

1.  Time zone offsets may have fractional seconds.
2.  The `T` separator may be replaced by any single unicode character.
3.  Fractional hours and minutes are not supported.
4.  Reduced precision dates are not currently supported (`YYYY-MM`, `YYYY`).
5.  Extended date representations are not currently supported (`±YYYYYY-MM-DD`).
6.  Ordinal dates are not currently supported (`YYYY-OOO`).

Examples:

    >>> from datetime import datetime
    >>> datetime.fromisoformat('2011-11-04')
    datetime.datetime(2011, 11, 4, 0, 0)
    >>> datetime.fromisoformat('20111104')
    datetime.datetime(2011, 11, 4, 0, 0)
    >>> datetime.fromisoformat('2011-11-04T00:05:23')
    datetime.datetime(2011, 11, 4, 0, 5, 23)
    >>> datetime.fromisoformat('2011-11-04T00:05:23Z')
    datetime.datetime(2011, 11, 4, 0, 5, 23, tzinfo=datetime.timezone.utc)
    >>> datetime.fromisoformat('20111104T000523')
    datetime.datetime(2011, 11, 4, 0, 5, 23)
    >>> datetime.fromisoformat('2011-W01-2T00:05:23.283')
    datetime.datetime(2011, 1, 4, 0, 5, 23, 283000)
    >>> datetime.fromisoformat('2011-11-04 00:05:23.283')
    datetime.datetime(2011, 11, 4, 0, 5, 23, 283000)
    >>> datetime.fromisoformat('2011-11-04 00:05:23.283+00:00')
    datetime.datetime(2011, 11, 4, 0, 5, 23, 283000, tzinfo=datetime.timezone.utc)
    >>> datetime.fromisoformat('2011-11-04T00:05:23+04:00')   # doctest: +NORMALIZE_WHITESPACE
    datetime.datetime(2011, 11, 4, 0, 5, 23,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=14400)))

::: versionadded
3.7
:::

::: versionchanged
3.11 Previously, this method only supported formats that could be emitted by `date.isoformat`{.interpreted-text role="meth"} or `datetime.isoformat`{.interpreted-text role="meth"}.
:::
:::::

:::: classmethod
datetime.fromisocalendar(year, week, day)

Return a `.datetime`{.interpreted-text role="class"} corresponding to the ISO calendar date specified by *year*, *week* and *day*. The non-date components of the datetime are populated with their normal default values. This is the inverse of the function `datetime.isocalendar`{.interpreted-text role="meth"}.

::: versionadded
3.8
:::
::::

::::: classmethod
datetime.strptime(date_string, format)

Return a `.datetime`{.interpreted-text role="class"} corresponding to *date_string*, parsed according to *format*.

If *format* does not contain microseconds or time zone information, this is equivalent to:

    datetime(*(time.strptime(date_string, format)[0:6]))

`ValueError`{.interpreted-text role="exc"} is raised if the date_string and format can\'t be parsed by `time.strptime`{.interpreted-text role="func"} or if it returns a value which isn\'t a time tuple. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `datetime.fromisoformat`{.interpreted-text role="meth"}.

:::: versionchanged
3.13

If *format* specifies a day of month without a year a `DeprecationWarning`{.interpreted-text role="exc"} is now emitted. This is to avoid a quadrennial leap year bug in code seeking to parse only a month and day as the default year used in absence of one in the format is not a leap year. Such *format* values may raise an error as of Python 3.15. The workaround is to always include a year in your *format*. If parsing *date_string* values that do not have a year, explicitly add a year that is a leap year before parsing:

::: doctest
\>\>\> from datetime import datetime \>\>\> date_string = \"02/29\" \>\>\> when = datetime.strptime(f\"{date_string};1984\", \"%m/%d;%Y\") \# Avoids leap year bug. \>\>\> when.strftime(\"%B %d\") \# doctest: +SKIP \'February 29\'
:::
::::
:::::

Class attributes:

::: attribute
datetime.min

The earliest representable `.datetime`{.interpreted-text role="class"}, `datetime(MINYEAR, 1, 1, tzinfo=None)`.
:::

::: attribute
datetime.max

The latest representable `.datetime`{.interpreted-text role="class"}, `datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None)`.
:::

::: attribute
datetime.resolution

The smallest possible difference between non-equal `.datetime`{.interpreted-text role="class"} objects, `timedelta(microseconds=1)`.
:::

Instance attributes (read-only):

::: attribute
datetime.year

Between `MINYEAR`{.interpreted-text role="const"} and `MAXYEAR`{.interpreted-text role="const"} inclusive.
:::

::: attribute
datetime.month

Between 1 and 12 inclusive.
:::

::: attribute
datetime.day

Between 1 and the number of days in the given month of the given year.
:::

::: attribute
datetime.hour

In `range(24)`.
:::

::: attribute
datetime.minute

In `range(60)`.
:::

::: attribute
datetime.second

In `range(60)`.
:::

::: attribute
datetime.microsecond

In `range(1000000)`.
:::

::: attribute
datetime.tzinfo

The object passed as the *tzinfo* argument to the `.datetime`{.interpreted-text role="class"} constructor, or `None` if none was passed.
:::

:::: attribute
datetime.fold

In `[0, 1]`. Used to disambiguate wall times during a repeated interval. (A repeated interval occurs when clocks are rolled back at the end of daylight saving time or when the UTC offset for the current zone is decreased for political reasons.) The values 0 and 1 represent, respectively, the earlier and later of the two moments with the same wall time representation.

::: versionadded
3.6
:::
::::

Supported operations:

+--------------------------------------+-------------------------------+
| Operation                            | Result                        |
+======================================+===============================+
| `datetime2 = datetime1 + timedelta`  | \(1\)                         |
+--------------------------------------+-------------------------------+
| `datetime2 = datetime1 - timedelta`  | \(2\)                         |
+--------------------------------------+-------------------------------+
| `timedelta = datetime1 - datetime2`  | \(3\)                         |
+--------------------------------------+-------------------------------+
| | `datetime1 == datetime2`           | Equality comparison. (4)      |
| | `datetime1 != datetime2`           |                               |
+--------------------------------------+-------------------------------+
| | `datetime1 < datetime2`            | Order comparison. (5)         |
| | `datetime1 > datetime2`            |                               |
| | `datetime1 <= datetime2`           |                               |
| | `datetime1 >= datetime2`           |                               |
+--------------------------------------+-------------------------------+

\(1\)

:   `datetime2` is a duration of `timedelta` removed from `datetime1`, moving forward in time if `timedelta.days > 0`, or backward if `timedelta.days < 0`. The result has the same `~.datetime.tzinfo`{.interpreted-text role="attr"} attribute as the input datetime, and `datetime2 - datetime1 == timedelta` after. `OverflowError`{.interpreted-text role="exc"} is raised if `datetime2.year` would be smaller than `MINYEAR`{.interpreted-text role="const"} or larger than `MAXYEAR`{.interpreted-text role="const"}. Note that no time zone adjustments are done even if the input is an aware object.

\(2\)

:   Computes the `datetime2` such that `datetime2 + timedelta == datetime1`. As for addition, the result has the same `~.datetime.tzinfo`{.interpreted-text role="attr"} attribute as the input datetime, and no time zone adjustments are done even if the input is aware.

\(3\)

:   Subtraction of a `.datetime`{.interpreted-text role="class"} from a `.datetime`{.interpreted-text role="class"} is defined only if both operands are naive, or if both are aware. If one is aware and the other is naive, `TypeError`{.interpreted-text role="exc"} is raised.

    If both are naive, or both are aware and have the same `~.datetime.tzinfo`{.interpreted-text role="attr"} attribute, the `~.datetime.tzinfo`{.interpreted-text role="attr"} attributes are ignored, and the result is a `timedelta`{.interpreted-text role="class"} object `t` such that `datetime2 + t == datetime1`. No time zone adjustments are done in this case.

    If both are aware and have different `~.datetime.tzinfo`{.interpreted-text role="attr"} attributes, `a-b` acts as if `a` and `b` were first converted to naive UTC datetimes. The result is `(a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None) - b.utcoffset())` except that the implementation never overflows.

\(4\)

:   `.datetime`{.interpreted-text role="class"} objects are equal if they represent the same date and time, taking into account the time zone.

    Naive and aware `!datetime`{.interpreted-text role="class"} objects are never equal.

    If both comparands are aware, and have the same `!tzinfo`{.interpreted-text role="attr"} attribute, the `!tzinfo`{.interpreted-text role="attr"} and `~.datetime.fold`{.interpreted-text role="attr"} attributes are ignored and the base datetimes are compared. If both comparands are aware and have different `~.datetime.tzinfo`{.interpreted-text role="attr"} attributes, the comparison acts as comparands were first converted to UTC datetimes except that the implementation never overflows. `!datetime`{.interpreted-text role="class"} instances in a repeated interval are never equal to `!datetime`{.interpreted-text role="class"} instances in other time zone.

\(5\)

:   *datetime1* is considered less than *datetime2* when *datetime1* precedes *datetime2* in time, taking into account the time zone.

    Order comparison between naive and aware `.datetime`{.interpreted-text role="class"} objects raises `TypeError`{.interpreted-text role="exc"}.

    If both comparands are aware, and have the same `!tzinfo`{.interpreted-text role="attr"} attribute, the `!tzinfo`{.interpreted-text role="attr"} and `~.datetime.fold`{.interpreted-text role="attr"} attributes are ignored and the base datetimes are compared. If both comparands are aware and have different `~.datetime.tzinfo`{.interpreted-text role="attr"} attributes, the comparison acts as comparands were first converted to UTC datetimes except that the implementation never overflows.

::: versionchanged
3.3 Equality comparisons between aware and naive `.datetime`{.interpreted-text role="class"} instances don\'t raise `TypeError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.13 Comparison between `.datetime`{.interpreted-text role="class"} object and an instance of the `date`{.interpreted-text role="class"} subclass that is not a `!datetime`{.interpreted-text role="class"} subclass no longer converts the latter to `!date`{.interpreted-text role="class"}, ignoring the time part and the time zone. The default behavior can be changed by overriding the special comparison methods in subclasses.
:::

Instance methods:

::: method
datetime.date()

Return `date`{.interpreted-text role="class"} object with same year, month and day.
:::

:::: method
datetime.time()

Return `.time`{.interpreted-text role="class"} object with same hour, minute, second, microsecond and fold. `.tzinfo`{.interpreted-text role="attr"} is `None`. See also method `timetz`{.interpreted-text role="meth"}.

::: versionchanged
3.6 The fold value is copied to the returned `.time`{.interpreted-text role="class"} object.
:::
::::

:::: method
datetime.timetz()

Return `.time`{.interpreted-text role="class"} object with same hour, minute, second, microsecond, fold, and tzinfo attributes. See also method `time`{.interpreted-text role="meth"}.

::: versionchanged
3.6 The fold value is copied to the returned `.time`{.interpreted-text role="class"} object.
:::
::::

:::: method
datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, \*, fold=0)

Return a new `datetime`{.interpreted-text role="class"} object with the same attributes, but with specified parameters updated. Note that `tzinfo=None` can be specified to create a naive datetime from an aware datetime with no conversion of date and time data.

`.datetime`{.interpreted-text role="class"} objects are also supported by generic function `copy.replace`{.interpreted-text role="func"}.

::: versionchanged
3.6 Added the *fold* parameter.
:::
::::

::::: method
datetime.astimezone(tz=None)

Return a `.datetime`{.interpreted-text role="class"} object with new `.tzinfo`{.interpreted-text role="attr"} attribute *tz*, adjusting the date and time data so the result is the same UTC time as *self*, but in *tz*\'s local time.

If provided, *tz* must be an instance of a `tzinfo`{.interpreted-text role="class"} subclass, and its `utcoffset`{.interpreted-text role="meth"} and `dst`{.interpreted-text role="meth"} methods must not return `None`. If *self* is naive, it is presumed to represent time in the system time zone.

If called without arguments (or with `tz=None`) the system local time zone is assumed for the target time zone. The `.tzinfo` attribute of the converted datetime instance will be set to an instance of `timezone`{.interpreted-text role="class"} with the zone name and offset obtained from the OS.

If `self.tzinfo` is *tz*, `self.astimezone(tz)` is equal to *self*: no adjustment of date or time data is performed. Else the result is local time in the time zone *tz*, representing the same UTC time as *self*: after `astz = dt.astimezone(tz)`, `astz - astz.utcoffset()` will have the same date and time data as `dt - dt.utcoffset()`.

If you merely want to attach a `timezone`{.interpreted-text role="class"} object *tz* to a datetime *dt* without adjustment of date and time data, use `dt.replace(tzinfo=tz)`. If you merely want to remove the `!timezone`{.interpreted-text role="class"} object from an aware datetime *dt* without conversion of date and time data, use `dt.replace(tzinfo=None)`.

Note that the default `tzinfo.fromutc`{.interpreted-text role="meth"} method can be overridden in a `tzinfo`{.interpreted-text role="class"} subclass to affect the result returned by `astimezone`{.interpreted-text role="meth"}. Ignoring error cases, `astimezone`{.interpreted-text role="meth"} acts like:

    def astimezone(self, tz):
        if self.tzinfo is tz:
            return self
        # Convert self to UTC, and attach the new timezone object.
        utc = (self - self.utcoffset()).replace(tzinfo=tz)
        # Convert from UTC to tz's local time.
        return tz.fromutc(utc)

::: versionchanged
3.3 *tz* now can be omitted.
:::

::: versionchanged
3.6 The `astimezone`{.interpreted-text role="meth"} method can now be called on naive instances that are presumed to represent system local time.
:::
:::::

:::: method
datetime.utcoffset()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.utcoffset(self)`, and raises an exception if the latter doesn\'t return `None` or a `timedelta`{.interpreted-text role="class"} object with magnitude less than one day.

::: versionchanged
3.7 The UTC offset is not restricted to a whole number of minutes.
:::
::::

:::: method
datetime.dst()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.dst(self)`, and raises an exception if the latter doesn\'t return `None` or a `timedelta`{.interpreted-text role="class"} object with magnitude less than one day.

::: versionchanged
3.7 The DST offset is not restricted to a whole number of minutes.
:::
::::

::: method
datetime.tzname()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.tzname(self)`, raises an exception if the latter doesn\'t return `None` or a string object,
:::

::: method
datetime.timetuple()

Return a `time.struct_time`{.interpreted-text role="class"} such as returned by `time.localtime`{.interpreted-text role="func"}.

`d.timetuple()` is equivalent to:

    time.struct_time((d.year, d.month, d.day,
                      d.hour, d.minute, d.second,
                      d.weekday(), yday, dst))

where `yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1` is the day number within the current year starting with 1 for January 1st. The `~time.struct_time.tm_isdst`{.interpreted-text role="attr"} flag of the result is set according to the `dst`{.interpreted-text role="meth"} method: `.tzinfo`{.interpreted-text role="attr"} is `None` or `dst`{.interpreted-text role="meth"} returns `None`, `!tm_isdst`{.interpreted-text role="attr"} is set to `-1`; else if `dst`{.interpreted-text role="meth"} returns a non-zero value, `!tm_isdst`{.interpreted-text role="attr"} is set to 1; else `!tm_isdst`{.interpreted-text role="attr"} is set to 0.
:::

::::: method
datetime.utctimetuple()

If `.datetime`{.interpreted-text role="class"} instance `d` is naive, this is the same as `d.timetuple()` except that `~.time.struct_time.tm_isdst`{.interpreted-text role="attr"} is forced to 0 regardless of what `d.dst()` returns. DST is never in effect for a UTC time.

If `d` is aware, `d` is normalized to UTC time, by subtracting `d.utcoffset()`, and a `time.struct_time`{.interpreted-text role="class"} for the normalized time is returned. `!tm_isdst`{.interpreted-text role="attr"} is forced to 0. Note that an `OverflowError`{.interpreted-text role="exc"} may be raised if `d.year` was `MINYEAR` or `MAXYEAR` and UTC adjustment spills over a year boundary.

:::: warning
::: title
Warning
:::

Because naive `datetime` objects are treated by many `datetime` methods as local times, it is preferred to use aware datetimes to represent times in UTC; as a result, using `datetime.utctimetuple`{.interpreted-text role="meth"} may give misleading results. If you have a naive `datetime` representing UTC, use `datetime.replace(tzinfo=timezone.utc)` to make it aware, at which point you can use `.datetime.timetuple`{.interpreted-text role="meth"}.
::::
:::::

::: method
datetime.toordinal()

Return the proleptic Gregorian ordinal of the date. The same as `self.date().toordinal()`.
:::

:::::::: method
datetime.timestamp()

Return POSIX timestamp corresponding to the `.datetime`{.interpreted-text role="class"} instance. The return value is a `float`{.interpreted-text role="class"} similar to that returned by `time.time`{.interpreted-text role="func"}.

Naive `.datetime`{.interpreted-text role="class"} instances are assumed to represent local time and this method relies on platform C functions to perform the conversion. Since `.datetime`{.interpreted-text role="class"} supports a wider range of values than the platform C functions on many platforms, this method may raise `OverflowError`{.interpreted-text role="exc"} or `OSError`{.interpreted-text role="exc"} for times far in the past or far in the future.

For aware `.datetime`{.interpreted-text role="class"} instances, the return value is computed as:

    (dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

:::: note
::: title
Note
:::

There is no method to obtain the POSIX timestamp directly from a naive `.datetime`{.interpreted-text role="class"} instance representing UTC time. If your application uses this convention and your system time zone is not set to UTC, you can obtain the POSIX timestamp by supplying `tzinfo=timezone.utc`:

    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

or by calculating the timestamp directly:

    timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
::::

::: versionadded
3.3
:::

::: versionchanged
3.6 The `timestamp`{.interpreted-text role="meth"} method uses the `.fold`{.interpreted-text role="attr"} attribute to disambiguate the times during a repeated interval.
:::

::: versionchanged
3.6 This method no longer relies on the platform C `mktime`{.interpreted-text role="c:func"} function to perform conversions.
:::
::::::::

::: method
datetime.weekday()

Return the day of the week as an integer, where Monday is 0 and Sunday is 6. The same as `self.date().weekday()`. See also `isoweekday`{.interpreted-text role="meth"}.
:::

::: method
datetime.isoweekday()

Return the day of the week as an integer, where Monday is 1 and Sunday is 7. The same as `self.date().isoweekday()`. See also `weekday`{.interpreted-text role="meth"}, `isocalendar`{.interpreted-text role="meth"}.
:::

::: method
datetime.isocalendar()

Return a `named tuple`{.interpreted-text role="term"} with three components: `year`, `week` and `weekday`. The same as `self.date().isocalendar()`.
:::

:::::: method
datetime.isoformat(sep=\'T\', timespec=\'auto\')

Return a string representing the date and time in ISO 8601 format:

- `YYYY-MM-DDTHH:MM:SS.ffffff`, if `microsecond`{.interpreted-text role="attr"} is not 0
- `YYYY-MM-DDTHH:MM:SS`, if `microsecond`{.interpreted-text role="attr"} is 0

If `utcoffset`{.interpreted-text role="meth"} does not return `None`, a string is appended, giving the UTC offset:

- `YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM[:SS[.ffffff]]`, if `microsecond`{.interpreted-text role="attr"} is not 0
- `YYYY-MM-DDTHH:MM:SS+HH:MM[:SS[.ffffff]]`, if `microsecond`{.interpreted-text role="attr"} is 0

Examples:

    >>> from datetime import datetime, timezone
    >>> datetime(2019, 5, 18, 15, 17, 8, 132263).isoformat()
    '2019-05-18T15:17:08.132263'
    >>> datetime(2019, 5, 18, 15, 17, tzinfo=timezone.utc).isoformat()
    '2019-05-18T15:17:00+00:00'

The optional argument *sep* (default `'T'`) is a one-character separator, placed between the date and time portions of the result. For example:

    >>> from datetime import tzinfo, timedelta, datetime
    >>> class TZ(tzinfo):
    ...     """A time zone with an arbitrary, constant -06:39 offset."""
    ...     def utcoffset(self, dt):
    ...         return timedelta(hours=-6, minutes=-39)
    ...
    >>> datetime(2002, 12, 25, tzinfo=TZ()).isoformat(' ')
    '2002-12-25 00:00:00-06:39'
    >>> datetime(2009, 11, 27, microsecond=100, tzinfo=TZ()).isoformat()
    '2009-11-27T00:00:00.000100-06:39'

The optional argument *timespec* specifies the number of additional components of the time to include (the default is `'auto'`). It can be one of the following:

- `'auto'`: Same as `'seconds'` if `microsecond`{.interpreted-text role="attr"} is 0, same as `'microseconds'` otherwise.
- `'hours'`: Include the `hour`{.interpreted-text role="attr"} in the two-digit `HH` format.
- `'minutes'`: Include `hour`{.interpreted-text role="attr"} and `minute`{.interpreted-text role="attr"} in `HH:MM` format.
- `'seconds'`: Include `hour`{.interpreted-text role="attr"}, `minute`{.interpreted-text role="attr"}, and `second`{.interpreted-text role="attr"} in `HH:MM:SS` format.
- `'milliseconds'`: Include full time, but truncate fractional second part to milliseconds. `HH:MM:SS.sss` format.
- `'microseconds'`: Include full time in `HH:MM:SS.ffffff` format.

:::: note
::: title
Note
:::

Excluded time components are truncated, not rounded.
::::

`ValueError`{.interpreted-text role="exc"} will be raised on an invalid *timespec* argument:

    >>> from datetime import datetime
    >>> datetime.now().isoformat(timespec='minutes')   # doctest: +SKIP
    '2002-12-25T00:00'
    >>> dt = datetime(2015, 1, 1, 12, 30, 59, 0)
    >>> dt.isoformat(timespec='microseconds')
    '2015-01-01T12:30:59.000000'

::: versionchanged
3.6 Added the *timespec* parameter.
:::
::::::

::: method
datetime.\_\_str\_\_()

For a `.datetime`{.interpreted-text role="class"} instance `d`, `str(d)` is equivalent to `d.isoformat(' ')`.
:::

::: method
datetime.ctime()

Return a string representing the date and time:

    >>> from datetime import datetime
    >>> datetime(2002, 12, 4, 20, 30, 40).ctime()
    'Wed Dec  4 20:30:40 2002'

The output string will *not* include time zone information, regardless of whether the input is aware or naive.

`d.ctime()` is equivalent to:

    time.ctime(time.mktime(d.timetuple()))

on platforms where the native C `ctime`{.interpreted-text role="c:func"} function (which `time.ctime`{.interpreted-text role="func"} invokes, but which `datetime.ctime`{.interpreted-text role="meth"} does not invoke) conforms to the C standard.
:::

::: method
datetime.strftime(format)

Return a string representing the date and time, controlled by an explicit format string. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `datetime.isoformat`{.interpreted-text role="meth"}.
:::

::: method
datetime.\_\_format\_\_(format)

Same as `.datetime.strftime`{.interpreted-text role="meth"}. This makes it possible to specify a format string for a `.datetime`{.interpreted-text role="class"} object in `formatted string
literals <f-strings>`{.interpreted-text role="ref"} and when using `str.format`{.interpreted-text role="meth"}. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `datetime.isoformat`{.interpreted-text role="meth"}.
:::

### Examples of usage: `!datetime`{.interpreted-text role="class"}

Examples of working with `.datetime`{.interpreted-text role="class"} objects:

::: doctest
\>\>\> from datetime import datetime, date, time, timezone

\>\>\> \# Using datetime.combine() \>\>\> d = date(2005, 7, 14) \>\>\> t = time(12, 30) \>\>\> datetime.combine(d, t) datetime.datetime(2005, 7, 14, 12, 30)

\>\>\> \# Using datetime.now() \>\>\> datetime.now() \# doctest: +SKIP datetime.datetime(2007, 12, 6, 16, 29, 43, 79043) \# GMT +1 \>\>\> datetime.now(timezone.utc) \# doctest: +SKIP datetime.datetime(2007, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)

\>\>\> \# Using datetime.strptime() \>\>\> dt = datetime.strptime(\"21/11/06 16:30\", \"%d/%m/%y %H:%M\") \>\>\> dt datetime.datetime(2006, 11, 21, 16, 30)

\>\>\> \# Using datetime.timetuple() to get tuple of all attributes \>\>\> tt = dt.timetuple() \>\>\> for it in tt: \# doctest: +SKIP \... print(it) \... 2006 \# year 11 \# month 21 \# day 16 \# hour 30 \# minute 0 \# second 1 \# weekday (0 = Monday) 325 \# number of days since 1st January -1 \# dst - method tzinfo.dst() returned None

\>\>\> \# Date in ISO format \>\>\> ic = dt.isocalendar() \>\>\> for it in ic: \# doctest: +SKIP \... print(it) \... 2006 \# ISO year 47 \# ISO week 2 \# ISO weekday

\>\>\> \# Formatting a datetime \>\>\> dt.strftime(\"%A, %d. %B %Y %I:%M%p\") \'Tuesday, 21. November 2006 04:30PM\' \>\>\> \'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.\'.format(dt, \"day\", \"month\", \"time\") \'The day is 21, the month is November, the time is 04:30PM.\'
:::

The example below defines a `tzinfo`{.interpreted-text role="class"} subclass capturing time zone information for Kabul, Afghanistan, which used +4 UTC until 1945 and then +4:30 UTC thereafter:

    from datetime import timedelta, datetime, tzinfo, timezone

    class KabulTz(tzinfo):
        # Kabul used +4 until 1945, when they moved to +4:30
        UTC_MOVE_DATE = datetime(1944, 12, 31, 20, tzinfo=timezone.utc)

        def utcoffset(self, dt):
            if dt.year < 1945:
                return timedelta(hours=4)
            elif (1945, 1, 1, 0, 0) <= dt.timetuple()[:5] < (1945, 1, 1, 0, 30):
                # An ambiguous ("imaginary") half-hour range representing
                # a 'fold' in time due to the shift from +4 to +4:30.
                # If dt falls in the imaginary range, use fold to decide how
                # to resolve. See PEP495.
                return timedelta(hours=4, minutes=(30 if dt.fold else 0))
            else:
                return timedelta(hours=4, minutes=30)

        def fromutc(self, dt):
            # Follow same validations as in datetime.tzinfo
            if not isinstance(dt, datetime):
                raise TypeError("fromutc() requires a datetime argument")
            if dt.tzinfo is not self:
                raise ValueError("dt.tzinfo is not self")

            # A custom implementation is required for fromutc as
            # the input to this function is a datetime with utc values
            # but with a tzinfo set to self.
            # See datetime.astimezone or fromtimestamp.
            if dt.replace(tzinfo=timezone.utc) >= self.UTC_MOVE_DATE:
                return dt + timedelta(hours=4, minutes=30)
            else:
                return dt + timedelta(hours=4)

        def dst(self, dt):
            # Kabul does not observe daylight saving time.
            return timedelta(0)

        def tzname(self, dt):
            if dt >= self.UTC_MOVE_DATE:
                return "+04:30"
            return "+04"

Usage of `KabulTz` from above:

    >>> tz1 = KabulTz()

    >>> # Datetime before the change
    >>> dt1 = datetime(1900, 11, 21, 16, 30, tzinfo=tz1)
    >>> print(dt1.utcoffset())
    4:00:00

    >>> # Datetime after the change
    >>> dt2 = datetime(2006, 6, 14, 13, 0, tzinfo=tz1)
    >>> print(dt2.utcoffset())
    4:30:00

    >>> # Convert datetime to another time zone
    >>> dt3 = dt2.astimezone(timezone.utc)
    >>> dt3
    datetime.datetime(2006, 6, 14, 8, 30, tzinfo=datetime.timezone.utc)
    >>> dt2
    datetime.datetime(2006, 6, 14, 13, 0, tzinfo=KabulTz())
    >>> dt2 == dt3
    True

## `!time`{.interpreted-text role="class"} objects {#datetime-time}

A `.time`{.interpreted-text role="class"} object represents a (local) time of day, independent of any particular day, and subject to adjustment via a `tzinfo`{.interpreted-text role="class"} object.

::: {.time(hour=0, .minute=0, .second=0, .microsecond=0, .tzinfo=None, .*, .fold=0)}
All arguments are optional. *tzinfo* may be `None`, or an instance of a `tzinfo`{.interpreted-text role="class"} subclass. The remaining arguments must be integers in the following ranges:

- `0 <= hour < 24`,
- `0 <= minute < 60`,
- `0 <= second < 60`,
- `0 <= microsecond < 1000000`,
- `fold in [0, 1]`.

If an argument outside those ranges is given, `ValueError`{.interpreted-text role="exc"} is raised. All default to 0 except *tzinfo*, which defaults to `None`.
:::

Class attributes:

::: attribute
time.min

The earliest representable `.time`{.interpreted-text role="class"}, `time(0, 0, 0, 0)`.
:::

::: attribute
time.max

The latest representable `.time`{.interpreted-text role="class"}, `time(23, 59, 59, 999999)`.
:::

::: attribute
time.resolution

The smallest possible difference between non-equal `.time`{.interpreted-text role="class"} objects, `timedelta(microseconds=1)`, although note that arithmetic on `.time`{.interpreted-text role="class"} objects is not supported.
:::

Instance attributes (read-only):

::: attribute
time.hour

In `range(24)`.
:::

::: attribute
time.minute

In `range(60)`.
:::

::: attribute
time.second

In `range(60)`.
:::

::: attribute
time.microsecond

In `range(1000000)`.
:::

::: attribute
time.tzinfo

The object passed as the tzinfo argument to the `.time`{.interpreted-text role="class"} constructor, or `None` if none was passed.
:::

:::: attribute
time.fold

In `[0, 1]`. Used to disambiguate wall times during a repeated interval. (A repeated interval occurs when clocks are rolled back at the end of daylight saving time or when the UTC offset for the current zone is decreased for political reasons.) The values 0 and 1 represent, respectively, the earlier and later of the two moments with the same wall time representation.

::: versionadded
3.6
:::
::::

`.time`{.interpreted-text role="class"} objects support equality and order comparisons, where `a` is considered less than `b` when `a` precedes `b` in time.

Naive and aware `!time`{.interpreted-text role="class"} objects are never equal. Order comparison between naive and aware `!time`{.interpreted-text role="class"} objects raises `TypeError`{.interpreted-text role="exc"}.

If both comparands are aware, and have the same `~.time.tzinfo`{.interpreted-text role="attr"} attribute, the `!tzinfo`{.interpreted-text role="attr"} and `!fold`{.interpreted-text role="attr"} attributes are ignored and the base times are compared. If both comparands are aware and have different `!tzinfo`{.interpreted-text role="attr"} attributes, the comparands are first adjusted by subtracting their UTC offsets (obtained from `self.utcoffset()`).

::: versionchanged
3.3 Equality comparisons between aware and naive `.time`{.interpreted-text role="class"} instances don\'t raise `TypeError`{.interpreted-text role="exc"}.
:::

In Boolean contexts, a `.time`{.interpreted-text role="class"} object is always considered to be true.

::: versionchanged
3.5 Before Python 3.5, a `.time`{.interpreted-text role="class"} object was considered to be false if it represented midnight in UTC. This behavior was considered obscure and error-prone and has been removed in Python 3.5. See `13936`{.interpreted-text role="issue"} for more information.
:::

Other constructors:

:::::: classmethod
time.fromisoformat(time_string)

Return a `.time`{.interpreted-text role="class"} corresponding to a *time_string* in any valid ISO 8601 format, with the following exceptions:

1.  Time zone offsets may have fractional seconds.
2.  The leading `T`, normally required in cases where there may be ambiguity between a date and a time, is not required.
3.  Fractional seconds may have any number of digits (anything beyond 6 will be truncated).
4.  Fractional hours and minutes are not supported.

Examples:

::: doctest
\>\>\> from datetime import time \>\>\> time.fromisoformat(\'04:23:01\') datetime.time(4, 23, 1) \>\>\> time.fromisoformat(\'T04:23:01\') datetime.time(4, 23, 1) \>\>\> time.fromisoformat(\'T042301\') datetime.time(4, 23, 1) \>\>\> time.fromisoformat(\'04:23:01.000384\') datetime.time(4, 23, 1, 384) \>\>\> time.fromisoformat(\'04:23:01,000384\') datetime.time(4, 23, 1, 384) \>\>\> time.fromisoformat(\'04:23:01+04:00\') datetime.time(4, 23, 1, tzinfo=datetime.timezone(datetime.timedelta(seconds=14400))) \>\>\> time.fromisoformat(\'04:23:01Z\') datetime.time(4, 23, 1, tzinfo=datetime.timezone.utc) \>\>\> time.fromisoformat(\'04:23:01+00:00\') datetime.time(4, 23, 1, tzinfo=datetime.timezone.utc)
:::

::: versionadded
3.7
:::

::: versionchanged
3.11 Previously, this method only supported formats that could be emitted by `time.isoformat`{.interpreted-text role="meth"}.
:::
::::::

:::: classmethod
time.strptime(date_string, format)

Return a `.time`{.interpreted-text role="class"} corresponding to *date_string*, parsed according to *format*.

If *format* does not contain microseconds or timezone information, this is equivalent to:

    time(*(time.strptime(date_string, format)[3:6]))

`ValueError`{.interpreted-text role="exc"} is raised if the *date_string* and *format* cannot be parsed by `time.strptime`{.interpreted-text role="func"} or if it returns a value which is not a time tuple. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `time.fromisoformat`{.interpreted-text role="meth"}.

::: versionadded
3.14
:::
::::

Instance methods:

:::: method
time.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, \*, fold=0)

Return a new `.time`{.interpreted-text role="class"} with the same values, but with specified parameters updated. Note that `tzinfo=None` can be specified to create a naive `.time`{.interpreted-text role="class"} from an aware `.time`{.interpreted-text role="class"}, without conversion of the time data.

`.time`{.interpreted-text role="class"} objects are also supported by generic function `copy.replace`{.interpreted-text role="func"}.

::: versionchanged
3.6 Added the *fold* parameter.
:::
::::

:::::: method
time.isoformat(timespec=\'auto\')

Return a string representing the time in ISO 8601 format, one of:

- `HH:MM:SS.ffffff`, if `microsecond`{.interpreted-text role="attr"} is not 0
- `HH:MM:SS`, if `microsecond`{.interpreted-text role="attr"} is 0
- `HH:MM:SS.ffffff+HH:MM[:SS[.ffffff]]`, if `utcoffset`{.interpreted-text role="meth"} does not return `None`
- `HH:MM:SS+HH:MM[:SS[.ffffff]]`, if `microsecond`{.interpreted-text role="attr"} is 0 and `utcoffset`{.interpreted-text role="meth"} does not return `None`

The optional argument *timespec* specifies the number of additional components of the time to include (the default is `'auto'`). It can be one of the following:

- `'auto'`: Same as `'seconds'` if `microsecond`{.interpreted-text role="attr"} is 0, same as `'microseconds'` otherwise.
- `'hours'`: Include the `hour`{.interpreted-text role="attr"} in the two-digit `HH` format.
- `'minutes'`: Include `hour`{.interpreted-text role="attr"} and `minute`{.interpreted-text role="attr"} in `HH:MM` format.
- `'seconds'`: Include `hour`{.interpreted-text role="attr"}, `minute`{.interpreted-text role="attr"}, and `second`{.interpreted-text role="attr"} in `HH:MM:SS` format.
- `'milliseconds'`: Include full time, but truncate fractional second part to milliseconds. `HH:MM:SS.sss` format.
- `'microseconds'`: Include full time in `HH:MM:SS.ffffff` format.

:::: note
::: title
Note
:::

Excluded time components are truncated, not rounded.
::::

`ValueError`{.interpreted-text role="exc"} will be raised on an invalid *timespec* argument.

Example:

    >>> from datetime import time
    >>> time(hour=12, minute=34, second=56, microsecond=123456).isoformat(timespec='minutes')
    '12:34'
    >>> dt = time(hour=12, minute=34, second=56, microsecond=0)
    >>> dt.isoformat(timespec='microseconds')
    '12:34:56.000000'
    >>> dt.isoformat(timespec='auto')
    '12:34:56'

::: versionchanged
3.6 Added the *timespec* parameter.
:::
::::::

::: method
time.\_\_str\_\_()

For a time `t`, `str(t)` is equivalent to `t.isoformat()`.
:::

::: method
time.strftime(format)

Return a string representing the time, controlled by an explicit format string. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `time.isoformat`{.interpreted-text role="meth"}.
:::

::: method
time.\_\_format\_\_(format)

Same as `.time.strftime`{.interpreted-text role="meth"}. This makes it possible to specify a format string for a `.time`{.interpreted-text role="class"} object in `formatted string
literals <f-strings>`{.interpreted-text role="ref"} and when using `str.format`{.interpreted-text role="meth"}. See also `strftime-strptime-behavior`{.interpreted-text role="ref"} and `time.isoformat`{.interpreted-text role="meth"}.
:::

:::: method
time.utcoffset()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.utcoffset(None)`, and raises an exception if the latter doesn\'t return `None` or a `timedelta`{.interpreted-text role="class"} object with magnitude less than one day.

::: versionchanged
3.7 The UTC offset is not restricted to a whole number of minutes.
:::
::::

:::: method
time.dst()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.dst(None)`, and raises an exception if the latter doesn\'t return `None`, or a `timedelta`{.interpreted-text role="class"} object with magnitude less than one day.

::: versionchanged
3.7 The DST offset is not restricted to a whole number of minutes.
:::
::::

::: method
time.tzname()

If `.tzinfo`{.interpreted-text role="attr"} is `None`, returns `None`, else returns `self.tzinfo.tzname(None)`, or raises an exception if the latter doesn\'t return `None` or a string object.
:::

### Examples of usage: `!time`{.interpreted-text role="class"}

Examples of working with a `.time`{.interpreted-text role="class"} object:

    >>> from datetime import time, tzinfo, timedelta
    >>> class TZ1(tzinfo):
    ...     def utcoffset(self, dt):
    ...         return timedelta(hours=1)
    ...     def dst(self, dt):
    ...         return timedelta(0)
    ...     def tzname(self,dt):
    ...         return "+01:00"
    ...     def  __repr__(self):
    ...         return f"{self.__class__.__name__}()"
    ...
    >>> t = time(12, 10, 30, tzinfo=TZ1())
    >>> t
    datetime.time(12, 10, 30, tzinfo=TZ1())
    >>> t.isoformat()
    '12:10:30+01:00'
    >>> t.dst()
    datetime.timedelta(0)
    >>> t.tzname()
    '+01:00'
    >>> t.strftime("%H:%M:%S %Z")
    '12:10:30 +01:00'
    >>> 'The {} is {:%H:%M}.'.format("time", t)
    'The time is 12:10.'

## `!tzinfo`{.interpreted-text role="class"} objects {#datetime-tzinfo}

::: tzinfo()
This is an `abstract base class`{.interpreted-text role="term"}, meaning that this class should not be instantiated directly. Define a subclass of `tzinfo`{.interpreted-text role="class"} to capture information about a particular time zone.

An instance of (a concrete subclass of) `tzinfo`{.interpreted-text role="class"} can be passed to the constructors for `.datetime`{.interpreted-text role="class"} and `.time`{.interpreted-text role="class"} objects. The latter objects view their attributes as being in local time, and the `tzinfo`{.interpreted-text role="class"} object supports methods revealing offset of local time from UTC, the name of the time zone, and DST offset, all relative to a date or time object passed to them.

You need to derive a concrete subclass, and (at least) supply implementations of the standard `tzinfo`{.interpreted-text role="class"} methods needed by the `.datetime`{.interpreted-text role="class"} methods you use. The `!datetime`{.interpreted-text role="mod"} module provides `timezone`{.interpreted-text role="class"}, a simple concrete subclass of `tzinfo`{.interpreted-text role="class"} which can represent time zones with fixed offset from UTC such as UTC itself or North American EST and EDT.

Special requirement for pickling: A `tzinfo`{.interpreted-text role="class"} subclass must have an `~object.__init__`{.interpreted-text role="meth"} method that can be called with no arguments, otherwise it can be pickled but possibly not unpickled again. This is a technical requirement that may be relaxed in the future.

A concrete subclass of `tzinfo`{.interpreted-text role="class"} may need to implement the following methods. Exactly which methods are needed depends on the uses made of aware `!datetime`{.interpreted-text role="mod"} objects. If in doubt, simply implement all of them.
:::

:::: method
tzinfo.utcoffset(dt)

Return offset of local time from UTC, as a `timedelta`{.interpreted-text role="class"} object that is positive east of UTC. If local time is west of UTC, this should be negative.

This represents the *total* offset from UTC; for example, if a `tzinfo`{.interpreted-text role="class"} object represents both time zone and DST adjustments, `utcoffset`{.interpreted-text role="meth"} should return their sum. If the UTC offset isn\'t known, return `None`. Else the value returned must be a `timedelta`{.interpreted-text role="class"} object strictly between `-timedelta(hours=24)` and `timedelta(hours=24)` (the magnitude of the offset must be less than one day). Most implementations of `utcoffset`{.interpreted-text role="meth"} will probably look like one of these two:

    return CONSTANT                 # fixed-offset class
    return CONSTANT + self.dst(dt)  # daylight-aware class

If `utcoffset`{.interpreted-text role="meth"} does not return `None`, `dst`{.interpreted-text role="meth"} should not return `None` either.

The default implementation of `utcoffset`{.interpreted-text role="meth"} raises `NotImplementedError`{.interpreted-text role="exc"}.

::: versionchanged
3.7 The UTC offset is not restricted to a whole number of minutes.
:::
::::

:::: method
tzinfo.dst(dt)

Return the daylight saving time (DST) adjustment, as a `timedelta`{.interpreted-text role="class"} object or `None` if DST information isn\'t known.

Return `timedelta(0)` if DST is not in effect. If DST is in effect, return the offset as a `timedelta`{.interpreted-text role="class"} object (see `utcoffset`{.interpreted-text role="meth"} for details). Note that DST offset, if applicable, has already been added to the UTC offset returned by `utcoffset`{.interpreted-text role="meth"}, so there\'s no need to consult `dst`{.interpreted-text role="meth"} unless you\'re interested in obtaining DST info separately. For example, `datetime.timetuple`{.interpreted-text role="meth"} calls its `~.datetime.tzinfo`{.interpreted-text role="attr"} attribute\'s `dst`{.interpreted-text role="meth"} method to determine how the `~time.struct_time.tm_isdst`{.interpreted-text role="attr"} flag should be set, and `tzinfo.fromutc`{.interpreted-text role="meth"} calls `dst`{.interpreted-text role="meth"} to account for DST changes when crossing time zones.

An instance *tz* of a `tzinfo`{.interpreted-text role="class"} subclass that models both standard and daylight times must be consistent in this sense:

`tz.utcoffset(dt) - tz.dst(dt)`

must return the same result for every `.datetime`{.interpreted-text role="class"} *dt* with `dt.tzinfo == tz`. For sane `tzinfo`{.interpreted-text role="class"} subclasses, this expression yields the time zone\'s \"standard offset\", which should not depend on the date or the time, but only on geographic location. The implementation of `datetime.astimezone`{.interpreted-text role="meth"} relies on this, but cannot detect violations; it\'s the programmer\'s responsibility to ensure it. If a `tzinfo`{.interpreted-text role="class"} subclass cannot guarantee this, it may be able to override the default implementation of `tzinfo.fromutc`{.interpreted-text role="meth"} to work correctly with `~.datetime.astimezone`{.interpreted-text role="meth"} regardless.

Most implementations of `dst`{.interpreted-text role="meth"} will probably look like one of these two:

    def dst(self, dt):
        # a fixed-offset class:  doesn't account for DST
        return timedelta(0)

or:

    def dst(self, dt):
        # Code to set dston and dstoff to the time zone's DST
        # transition times based on the input dt.year, and expressed
        # in standard local time.

        if dston <= dt.replace(tzinfo=None) < dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

The default implementation of `dst`{.interpreted-text role="meth"} raises `NotImplementedError`{.interpreted-text role="exc"}.

::: versionchanged
3.7 The DST offset is not restricted to a whole number of minutes.
:::
::::

::: method
tzinfo.tzname(dt)

Return the time zone name corresponding to the `.datetime`{.interpreted-text role="class"} object *dt*, as a string. Nothing about string names is defined by the `!datetime`{.interpreted-text role="mod"} module, and there\'s no requirement that it mean anything in particular. For example, `"GMT"`, `"UTC"`, `"-500"`, `"-5:00"`, `"EDT"`, `"US/Eastern"`, `"America/New York"` are all valid replies. Return `None` if a string name isn\'t known. Note that this is a method rather than a fixed string primarily because some `tzinfo`{.interpreted-text role="class"} subclasses will wish to return different names depending on the specific value of *dt* passed, especially if the `tzinfo`{.interpreted-text role="class"} class is accounting for daylight time.

The default implementation of `tzname`{.interpreted-text role="meth"} raises `NotImplementedError`{.interpreted-text role="exc"}.
:::

These methods are called by a `.datetime`{.interpreted-text role="class"} or `.time`{.interpreted-text role="class"} object, in response to their methods of the same names. A `.datetime`{.interpreted-text role="class"} object passes itself as the argument, and a `.time`{.interpreted-text role="class"} object passes `None` as the argument. A `tzinfo`{.interpreted-text role="class"} subclass\'s methods should therefore be prepared to accept a *dt* argument of `None`, or of class `.datetime`{.interpreted-text role="class"}.

When `None` is passed, it\'s up to the class designer to decide the best response. For example, returning `None` is appropriate if the class wishes to say that time objects don\'t participate in the `tzinfo`{.interpreted-text role="class"} protocols. It may be more useful for `utcoffset(None)` to return the standard UTC offset, as there is no other convention for discovering the standard offset.

When a `.datetime`{.interpreted-text role="class"} object is passed in response to a `.datetime`{.interpreted-text role="class"} method, `dt.tzinfo` is the same object as *self*. `tzinfo`{.interpreted-text role="class"} methods can rely on this, unless user code calls `tzinfo`{.interpreted-text role="class"} methods directly. The intent is that the `tzinfo`{.interpreted-text role="class"} methods interpret *dt* as being in local time, and not need worry about objects in other time zones.

There is one more `tzinfo`{.interpreted-text role="class"} method that a subclass may wish to override:

::: method
tzinfo.fromutc(dt)

This is called from the default `datetime.astimezone`{.interpreted-text role="meth"} implementation. When called from that, `dt.tzinfo` is *self*, and *dt*\'s date and time data are to be viewed as expressing a UTC time. The purpose of `fromutc`{.interpreted-text role="meth"} is to adjust the date and time data, returning an equivalent datetime in *self*\'s local time.

Most `tzinfo`{.interpreted-text role="class"} subclasses should be able to inherit the default `fromutc`{.interpreted-text role="meth"} implementation without problems. It\'s strong enough to handle fixed-offset time zones, and time zones accounting for both standard and daylight time, and the latter even if the DST transition times differ in different years. An example of a time zone the default `fromutc`{.interpreted-text role="meth"} implementation may not handle correctly in all cases is one where the standard offset (from UTC) depends on the specific date and time passed, which can happen for political reasons. The default implementations of `~.datetime.astimezone`{.interpreted-text role="meth"} and `fromutc`{.interpreted-text role="meth"} may not produce the result you want if the result is one of the hours straddling the moment the standard offset changes.

Skipping code for error cases, the default `fromutc`{.interpreted-text role="meth"} implementation acts like:

    def fromutc(self, dt):
        # raise ValueError error if dt.tzinfo is not self
        dtoff = dt.utcoffset()
        dtdst = dt.dst()
        # raise ValueError if dtoff is None or dtdst is None
        delta = dtoff - dtdst  # this is self's standard offset
        if delta:
            dt += delta   # convert to standard local time
            dtdst = dt.dst()
            # raise ValueError if dtdst is None
        if dtdst:
            return dt + dtdst
        else:
            return dt
:::

In the following `tzinfo_examples.py
<../includes/tzinfo_examples.py>`{.interpreted-text role="download"} file there are some examples of `tzinfo`{.interpreted-text role="class"} classes:

::: literalinclude
../includes/tzinfo_examples.py
:::

Note that there are unavoidable subtleties twice per year in a `tzinfo`{.interpreted-text role="class"} subclass accounting for both standard and daylight time, at the DST transition points. For concreteness, consider US Eastern (UTC -0500), where EDT begins the minute after 1:59 (EST) on the second Sunday in March, and ends the minute after 1:59 (EDT) on the first Sunday in November:

    UTC   3:MM  4:MM  5:MM  6:MM  7:MM  8:MM
    EST  22:MM 23:MM  0:MM  1:MM  2:MM  3:MM
    EDT  23:MM  0:MM  1:MM  2:MM  3:MM  4:MM

    start  22:MM 23:MM  0:MM  1:MM  3:MM  4:MM

    end  23:MM  0:MM  1:MM  1:MM  2:MM  3:MM

When DST starts (the \"start\" line), the local wall clock leaps from 1:59 to 3:00. A wall time of the form 2:MM doesn\'t really make sense on that day, so `astimezone(Eastern)` won\'t deliver a result with `hour == 2` on the day DST begins. For example, at the Spring forward transition of 2016, we get:

    >>> from datetime import datetime, timezone
    >>> from tzinfo_examples import HOUR, Eastern
    >>> u0 = datetime(2016, 3, 13, 5, tzinfo=timezone.utc)
    >>> for i in range(4):
    ...     u = u0 + i*HOUR
    ...     t = u.astimezone(Eastern)
    ...     print(u.time(), 'UTC =', t.time(), t.tzname())
    ...
    05:00:00 UTC = 00:00:00 EST
    06:00:00 UTC = 01:00:00 EST
    07:00:00 UTC = 03:00:00 EDT
    08:00:00 UTC = 04:00:00 EDT

When DST ends (the \"end\" line), there\'s a potentially worse problem: there\'s an hour that can\'t be spelled unambiguously in local wall time: the last hour of daylight time. In Eastern, that\'s times of the form 5:MM UTC on the day daylight time ends. The local wall clock leaps from 1:59 (daylight time) back to 1:00 (standard time) again. Local times of the form 1:MM are ambiguous. `~.datetime.astimezone`{.interpreted-text role="meth"} mimics the local clock\'s behavior by mapping two adjacent UTC hours into the same local hour then. In the Eastern example, UTC times of the form 5:MM and 6:MM both map to 1:MM when converted to Eastern, but earlier times have the `~.datetime.fold`{.interpreted-text role="attr"} attribute set to 0 and the later times have it set to 1. For example, at the Fall back transition of 2016, we get:

    >>> u0 = datetime(2016, 11, 6, 4, tzinfo=timezone.utc)
    >>> for i in range(4):
    ...     u = u0 + i*HOUR
    ...     t = u.astimezone(Eastern)
    ...     print(u.time(), 'UTC =', t.time(), t.tzname(), t.fold)
    ...
    04:00:00 UTC = 00:00:00 EDT 0
    05:00:00 UTC = 01:00:00 EDT 0
    06:00:00 UTC = 01:00:00 EST 1
    07:00:00 UTC = 02:00:00 EST 0

Note that the `.datetime`{.interpreted-text role="class"} instances that differ only by the value of the `~.datetime.fold`{.interpreted-text role="attr"} attribute are considered equal in comparisons.

Applications that can\'t bear wall-time ambiguities should explicitly check the value of the `~.datetime.fold`{.interpreted-text role="attr"} attribute or avoid using hybrid `tzinfo`{.interpreted-text role="class"} subclasses; there are no ambiguities when using `timezone`{.interpreted-text role="class"}, or any other fixed-offset `tzinfo`{.interpreted-text role="class"} subclass (such as a class representing only EST (fixed offset -5 hours), or only EDT (fixed offset -4 hours)).

::: seealso

`zoneinfo`{.interpreted-text role="mod"}

:   The `!datetime`{.interpreted-text role="mod"} module has a basic `timezone`{.interpreted-text role="class"} class (for handling arbitrary fixed offsets from UTC) and its `timezone.utc`{.interpreted-text role="attr"} attribute (a UTC `!timezone`{.interpreted-text role="class"} instance).

    `zoneinfo` brings the *IANA time zone database* (also known as the Olson database) to Python, and its usage is recommended.

[IANA time zone database](https://www.iana.org/time-zones)

:   The Time Zone Database (often called tz, tzdata or zoneinfo) contains code and data that represent the history of local time for many representative locations around the globe. It is updated periodically to reflect changes made by political bodies to time zone boundaries, UTC offsets, and daylight-saving rules.
:::

## `!timezone`{.interpreted-text role="class"} objects {#datetime-timezone}

The `timezone`{.interpreted-text role="class"} class is a subclass of `tzinfo`{.interpreted-text role="class"}, each instance of which represents a time zone defined by a fixed offset from UTC.

Objects of this class cannot be used to represent time zone information in the locations where different offsets are used in different days of the year or where historical changes have been made to civil time.

::::: {.timezone(offset[, .name])}
The *offset* argument must be specified as a `timedelta`{.interpreted-text role="class"} object representing the difference between the local time and UTC. It must be strictly between `-timedelta(hours=24)` and `timedelta(hours=24)`, otherwise `ValueError`{.interpreted-text role="exc"} is raised.

The *name* argument is optional. If specified it must be a string that will be used as the value returned by the `datetime.tzname`{.interpreted-text role="meth"} method.

::: versionadded
3.2
:::

::: versionchanged
3.7 The UTC offset is not restricted to a whole number of minutes.
:::
:::::

:::: method
timezone.utcoffset(dt)

Return the fixed value specified when the `timezone`{.interpreted-text role="class"} instance is constructed.

The *dt* argument is ignored. The return value is a `timedelta`{.interpreted-text role="class"} instance equal to the difference between the local time and UTC.

::: versionchanged
3.7 The UTC offset is not restricted to a whole number of minutes.
:::
::::

:::: method
timezone.tzname(dt)

Return the fixed value specified when the `timezone`{.interpreted-text role="class"} instance is constructed.

If *name* is not provided in the constructor, the name returned by `tzname(dt)` is generated from the value of the `offset` as follows. If *offset* is `timedelta(0)`, the name is \"UTC\", otherwise it is a string in the format `UTC±HH:MM`, where ± is the sign of `offset`, HH and MM are two digits of `offset.hours` and `offset.minutes` respectively.

::: versionchanged
3.6 Name generated from `offset=timedelta(0)` is now plain `'UTC'`, not `'UTC+00:00'`.
:::
::::

::: method
timezone.dst(dt)

Always returns `None`.
:::

::: method
timezone.fromutc(dt)

Return `dt + offset`. The *dt* argument must be an aware `.datetime`{.interpreted-text role="class"} instance, with `tzinfo` set to `self`.
:::

Class attributes:

::: attribute
timezone.utc

The UTC time zone, `timezone(timedelta(0))`.
:::

::: index
single: % (percent); datetime format
:::

## `!strftime`{.interpreted-text role="meth"} and `!strptime`{.interpreted-text role="meth"} behavior {#strftime-strptime-behavior}

`date`{.interpreted-text role="class"}, `.datetime`{.interpreted-text role="class"}, and `.time`{.interpreted-text role="class"} objects all support a `strftime(format)` method, to create a string representing the time under the control of an explicit format string.

Conversely, the `date.strptime`{.interpreted-text role="meth"}, `datetime.strptime`{.interpreted-text role="meth"} and `time.strptime`{.interpreted-text role="meth"} class methods create an object from a string representing the time and a corresponding format string.

The table below provides a high-level comparison of `~.datetime.strftime`{.interpreted-text role="meth"} versus `~.datetime.strptime`{.interpreted-text role="meth"}:

  --------------------------------------------------------------------------------------------------------------------------------------
                   `strftime`                                               `strptime`
  ---------------- -------------------------------------------------------- ------------------------------------------------------------
  Usage            Convert object to a string according to a given format   Parse a string into an object given a corresponding format

  Type of method   Instance method                                          Class method

  Signature        `strftime(format)`                                       `strptime(date_string, format)`
  --------------------------------------------------------------------------------------------------------------------------------------

> 

### `!strftime`{.interpreted-text role="meth"} and `!strptime`{.interpreted-text role="meth"} format codes

These methods accept format codes that can be used to parse and format dates:

    >>> datetime.strptime('31/01/22 23:59:59.999999',
    ...                   '%d/%m/%y %H:%M:%S.%f')
    datetime.datetime(2022, 1, 31, 23, 59, 59, 999999)
    >>> _.strftime('%a %d %b %Y, %I:%M%p')
    'Mon 31 Jan 2022, 11:59PM'

The following is a list of all the format codes that the 2011 C standard requires, and these work on all supported platforms.

+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| Directive | > Meaning                                                                                                                                                                        | > Example                                             | Notes    |
+===========+==================================================================================================================================================================================+=======================================================+==========+
| > `%a`    | Weekday as locale\'s abbreviated name.                                                                                                                                           | | Sun, Mon, \..., Sat (en_US);                        | \(1\)    |
|           |                                                                                                                                                                                  | | So, Mo, \..., Sa (de_DE)                            |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%A`    | Weekday as locale\'s full name.                                                                                                                                                  | | Sunday, Monday, \..., Saturday (en_US);             | \(1\)    |
|           |                                                                                                                                                                                  | | Sonntag, Montag, \..., Samstag (de_DE)              |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%b`    | Month as locale\'s abbreviated name.                                                                                                                                             | | Jan, Feb, \..., Dec (en_US);                        | \(1\)    |
|           |                                                                                                                                                                                  | | Jan, Feb, \..., Dez (de_DE)                         |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%B`    | Month as locale\'s full name.                                                                                                                                                    | | January, February, \..., December (en_US);          | \(1\)    |
|           |                                                                                                                                                                                  | | Januar, Februar, \..., Dezember (de_DE)             |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%c`    | Locale\'s appropriate date and time representation.                                                                                                                              | | Tue Aug 16 21:30:00 1988 (en_US);                   | \(1\)    |
|           |                                                                                                                                                                                  | | Di 16 Aug 21:30:00 1988 (de_DE)                     |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%C`    | The year divided by 100 and truncated to an integer as a zero-padded decimal number.                                                                                             | 01, 02, \..., 99                                      | \(0\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%d`    | Day of the month as a zero-padded decimal number.                                                                                                                                | 01, 02, \..., 31                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%D`    | Equivalent to `%m/%d/%y`.                                                                                                                                                        | 11/28/25                                              | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%e`    | The day of the month as a space-padded decimal number.                                                                                                                           | ␣1, ␣2, \..., 31                                      |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%F`    | Equivalent to `%Y-%m-%d`, the ISO 8601 format.                                                                                                                                   | 2025-10-11, 1001-12-30                                |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%g`    | Last 2 digits of ISO 8601 year representing the year that contains the greater part of the ISO week (`%V`).                                                                      | 00, 01, \..., 99                                      | \(0\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%G`    | ISO 8601 year with century representing the year that contains the greater part of the ISO week (`%V`).                                                                          | 0001, 0002, \..., 2013, 2014, \..., 9998, 9999        | \(8\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%h`    | Equivalent to `%b`.                                                                                                                                                              | See `%b`.                                             | \(0\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%H`    | Hour (24-hour clock) as a zero-padded decimal number.                                                                                                                            | 00, 01, \..., 23                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%I`    | Hour (12-hour clock) as a zero-padded decimal number.                                                                                                                            | 01, 02, \..., 12                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%j`    | Day of the year as a zero-padded decimal number.                                                                                                                                 | 001, 002, \..., 366                                   | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%m`    | Month as a zero-padded decimal number.                                                                                                                                           | 01, 02, \..., 12                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%M`    | Minute as a zero-padded decimal number.                                                                                                                                          | 00, 01, \..., 59                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%n`    | The newline character (`'\n'`).                                                                                                                                                  | `\n`                                                  | \(0\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%p`    | Locale\'s equivalent of either AM or PM.                                                                                                                                         | | AM, PM (en_US);                                     | (1), (3) |
|           |                                                                                                                                                                                  | | am, pm (de_DE)                                      |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%r`    | Locale\'s 12-hour clock time.                                                                                                                                                    | 12:00:00 AM                                           | (1), (0) |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%R`    | Equivalent to `%H:%M`.                                                                                                                                                           | 10:01                                                 |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%S`    | Second as a zero-padded decimal number.                                                                                                                                          | 00, 01, \..., 59                                      | (4), (9) |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%t`    | The tab character (`'\t'`).                                                                                                                                                      | `\t`                                                  | \(0\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%T`    | ISO 8601 time format, equivalent to `%H:%M:%S`.                                                                                                                                  | 10:01:59                                              |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%u`    | ISO 8601 weekday as a decimal number where 1 is Monday.                                                                                                                          | 1, 2, \..., 7                                         |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%U`    | Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, \..., 53                                      | (7), (9) |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%V`    | ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.                                                                | 01, 02, \..., 53                                      | (8), (9) |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%w`    | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                | 0, 1, \..., 6                                         |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%W`    | Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0. | 00, 01, \..., 53                                      | (7), (9) |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%x`    | Locale\'s appropriate date representation.                                                                                                                                       | | 08/16/88 (None);                                    | \(1\)    |
|           |                                                                                                                                                                                  | | 08/16/1988 (en_US);                                 |          |
|           |                                                                                                                                                                                  | | 16.08.1988 (de_DE)                                  |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%X`    | Locale\'s appropriate time representation.                                                                                                                                       | | 21:30:00 (en_US);                                   | \(1\)    |
|           |                                                                                                                                                                                  | | 21:30:00 (de_DE)                                    |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%y`    | Year without century as a zero-padded decimal number.                                                                                                                            | 00, 01, \..., 99                                      | \(9\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%Y`    | Year with century as a decimal number.                                                                                                                                           | 0001, 0002, \..., 2013, 2014, \..., 9998, 9999        | \(2\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%z`    | UTC offset in the form `±HHMM[SS[.ffffff]]` (empty string if the object is naive).                                                                                               | (empty), +0000, -0400, +1030, +063415, -030712.345216 | \(6\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%Z`    | Time zone name (empty string if the object is naive).                                                                                                                            | (empty), UTC, GMT                                     | \(6\)    |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+
| > `%%`    | A literal `'%'` character.                                                                                                                                                       | \%                                                    |          |
+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+----------+

The ISO 8601 year and ISO 8601 week directives are not interchangeable with the year and week number directives above. Calling `~.datetime.strptime`{.interpreted-text role="meth"} with incomplete or ambiguous ISO 8601 directives will raise a `ValueError`{.interpreted-text role="exc"}.

Several additional directives not required by the C11 standard are included for convenience.

+-----------+--------------------------------------------------------------------------------------+--------------------------------------------------------------+-------+
| Directive | Meaning                                                                              | Example                                                      | Notes |
+===========+======================================================================================+==============================================================+=======+
| > `%f`    | Microsecond as a decimal number, zero-padded to 6 digits.                            | 000000, 000001, \..., 999999                                 | \(5\) |
+-----------+--------------------------------------------------------------------------------------+--------------------------------------------------------------+-------+
| `%:z`     | UTC offset in the form `±HH:MM[:SS[.ffffff]]` (empty string if the object is naive). | (empty), +00:00, -04:00, +10:30, +06:34:15, -03:07:12.345216 | \(6\) |
+-----------+--------------------------------------------------------------------------------------+--------------------------------------------------------------+-------+

The full set of format codes supported varies across platforms, because Python calls the platform C library\'s `strftime`{.interpreted-text role="c:func"} function, and platform variations are common. To see the full set of format codes supported on your platform, consult the `strftime(3)`{.interpreted-text role="manpage"} documentation. There are also differences between platforms in handling of unsupported format specifiers.

::: versionadded
3.6 `%G`, `%u` and `%V` were added.
:::

::: versionadded
3.12 `%:z` was added for `~.datetime.strftime`{.interpreted-text role="meth"}.
:::

::: versionadded
3.15 `%:z`, `%F`, and `%D` were added for `~.datetime.strptime`{.interpreted-text role="meth"}.
:::

### Technical detail

Broadly speaking, `d.strftime(fmt)` acts like the `time`{.interpreted-text role="mod"} module\'s `time.strftime(fmt, d.timetuple())` although not all objects support a `~date.timetuple`{.interpreted-text role="meth"} method.

For the `.datetime.strptime`{.interpreted-text role="meth"} and `.date.strptime`{.interpreted-text role="meth"} class methods, the default value is `1900-01-01T00:00:00.000`: any components not specified in the format string will be pulled from the default value.

:::: note
::: title
Note
:::

Format strings without separators can be ambiguous for parsing. For example, with `%Y%m%d`, the string `2026111` may be parsed either as `2026-11-01` or as `2026-01-11`. Use separators to ensure the input is parsed as intended.
::::

:::: note
::: title
Note
:::

When used to parse partial dates lacking a year, `.datetime.strptime`{.interpreted-text role="meth"} and `.date.strptime`{.interpreted-text role="meth"} will raise when encountering February 29 because the default year of 1900 is *not* a leap year. Always add a default leap year to partial date strings before parsing.
::::

::: testsetup
\# doctest seems to turn the warning into an error which makes it \# show up and require matching and prevents the actual interesting \# exception from being raised. \# Manually apply the catch_warnings context manager import warnings catch_warnings = warnings.catch_warnings() catch_warnings.\_\_enter\_\_() warnings.simplefilter(\"ignore\")
:::

::: testcleanup
catch_warnings.\_\_exit\_\_()
:::

::: doctest
\>\>\> from datetime import datetime \>\>\> value = \"2/29\" \>\>\> datetime.strptime(value, \"%m/%d\") Traceback (most recent call last): \... ValueError: day 29 must be in range 1..28 for month 2 in year 1900 \>\>\> datetime.strptime(f\"1904 {value}\", \"%Y %m/%d\") datetime.datetime(1904, 2, 29, 0, 0)
:::

Using `datetime.strptime(date_string, format)` is equivalent to:

    datetime(*(time.strptime(date_string, format)[0:6]))

except when the format includes sub-second components or time zone offset information, which are supported in `datetime.strptime` but are discarded by `time.strptime`.

For `.time`{.interpreted-text role="class"} objects, the format codes for year, month, and day should not be used, as `!time`{.interpreted-text role="class"} objects have no such values. If they\'re used anyway, 1900 is substituted for the year, and 1 for the month and day.

For `date`{.interpreted-text role="class"} objects, the format codes for hours, minutes, seconds, and microseconds should not be used, as `date`{.interpreted-text role="class"} objects have no such values. If they\'re used anyway, 0 is substituted for them.

For the same reason, handling of format strings containing Unicode code points that can\'t be represented in the charset of the current locale is also platform-dependent. On some platforms such code points are preserved intact in the output, while on others `strftime` may raise `UnicodeError`{.interpreted-text role="exc"} or return an empty string instead.

Notes:

\(0\)

:   This format code is currently unsupported by `~.datetime.strptime`{.interpreted-text role="meth"}.

\(1\)

:   Because the format depends on the current locale, care should be taken when making assumptions about the output value. Field orderings will vary (for example, \"month/day/year\" versus \"day/month/year\"), and the output may contain non-ASCII characters.

\(2\)

:   The `~.datetime.strptime`{.interpreted-text role="meth"} method can parse years in the full \[1, 9999\] range, but years \< 1000 must be zero-filled to 4-digit width.

    ::: versionchanged
    3.2 In previous versions, `~.datetime.strftime`{.interpreted-text role="meth"} method was restricted to years \>= 1900.
    :::

    ::: versionchanged
    3.3 In version 3.2, `~.datetime.strftime`{.interpreted-text role="meth"} method was restricted to years \>= 1000.
    :::

\(3\)

:   When used with the `~.datetime.strptime`{.interpreted-text role="meth"} method, the `%p` directive only affects the output hour field if the `%I` directive is used to parse the hour.

\(4\)

:   Unlike the `time`{.interpreted-text role="mod"} module, the `!datetime`{.interpreted-text role="mod"} module does not support leap seconds.

\(5\)

:   When used with the `~.datetime.strptime`{.interpreted-text role="meth"} method, the `%f` directive accepts from one to six digits and zero pads on the right. `%f` is an extension to the set of format characters in the C standard (but implemented separately in datetime objects, and therefore always available).

\(6\)

:   For a naive object, the `%z`, `%:z` and `%Z` format codes are replaced by empty strings.

    For an aware object:

    `%z`

    :   `~.datetime.utcoffset`{.interpreted-text role="meth"} is transformed into a string of the form `±HHMM[SS[.ffffff]]`, where `HH` is a 2-digit string giving the number of UTC offset hours, `MM` is a 2-digit string giving the number of UTC offset minutes, `SS` is a 2-digit string giving the number of UTC offset seconds and `ffffff` is a 6-digit string giving the number of UTC offset microseconds. The `ffffff` part is omitted when the offset is a whole number of seconds and both the `ffffff` and the `SS` part is omitted when the offset is a whole number of minutes. For example, if `~.datetime.utcoffset`{.interpreted-text role="meth"} returns `timedelta(hours=-3, minutes=-30)`, `%z` is replaced with the string `'-0330'`.

    ::: versionchanged
    3.7 The UTC offset is not restricted to a whole number of minutes.
    :::

    ::: versionchanged
    3.7 When the `%z` directive is provided to the `~.datetime.strptime`{.interpreted-text role="meth"} method, the UTC offsets can have a colon as a separator between hours, minutes and seconds. For example, both `'+010000'` and `'+01:00:00'` will be parsed as an offset of one hour. In addition, providing `'Z'` is identical to `'+00:00'`.
    :::

    `%:z`

    :   When used with `~.datetime.strftime`{.interpreted-text role="meth"}, behaves exactly as `%z`, except that a colon separator is added between hours, minutes and seconds.

        When used with `~.datetime.strptime`{.interpreted-text role="meth"}, the UTC offset is *required* to have a colon as a separator between hours, minutes and seconds. For example, `'+01:00:00'` (but *not* `'+010000'`) will be parsed as an offset of one hour. In addition, providing `'Z'` is identical to `'+00:00'`.

    `%Z`

    :   In `~.datetime.strftime`{.interpreted-text role="meth"}, `%Z` is replaced by an empty string if `~.datetime.tzname`{.interpreted-text role="meth"} returns `None`; otherwise `%Z` is replaced by the returned value, which must be a string.

        `~.datetime.strptime`{.interpreted-text role="meth"} only accepts certain values for `%Z`:

        1.  any value in `time.tzname` for your machine\'s locale
        2.  the hard-coded values `UTC` and `GMT`

        So someone living in Japan may have `JST`, `UTC`, and `GMT` as valid values, but probably not `EST`. It will raise `ValueError` for invalid values.

    ::: versionchanged
    3.2 When the `%z` directive is provided to the `~.datetime.strptime`{.interpreted-text role="meth"} method, an aware `.datetime`{.interpreted-text role="class"} object will be produced. The `tzinfo` of the result will be set to a `timezone`{.interpreted-text role="class"} instance.
    :::

\(7\)

:   When used with the `~.datetime.strptime`{.interpreted-text role="meth"} method, `%U` and `%W` are only used in calculations when the day of the week and the calendar year (`%Y`) are specified.

\(8\)

:   Similar to `%U` and `%W`, `%V` is only used in calculations when the day of the week and the ISO year (`%G`) are specified in a `~.datetime.strptime`{.interpreted-text role="meth"} format string. Also note that `%G` and `%Y` are not interchangeable.

\(9\)

:   When used with the `~.datetime.strptime`{.interpreted-text role="meth"} method, the leading zero is optional for formats `%d`, `%m`, `%H`, `%I`, `%M`, `%S`, `%j`, `%U`, `%W`, and `%V`. Format `%y` does require a leading zero.

\(10\)

:   When parsing a month and day using `~.datetime.strptime`{.interpreted-text role="meth"}, always include a year in the format. If the value you need to parse lacks a year, append an explicit dummy leap year. Otherwise your code will raise an exception when it encounters leap day because the default year used by the parser (1900) is not a leap year. Users run into that bug every leap year.

    ::: doctest
    \>\>\> month_day = \"02/29\" \>\>\> datetime.strptime(f\"{month_day};1984\", \"%m/%d;%Y\") \# No leap year bug. datetime.datetime(1984, 2, 29, 0, 0)
    :::

    ::: deprecated-removed
    3.13 3.15 `~.datetime.strptime`{.interpreted-text role="meth"} calls using a format string containing a day of month without a year now emit a `DeprecationWarning`{.interpreted-text role="exc"}. In 3.15 or later we may change this into an error or change the default year to a leap year. See `70647`{.interpreted-text role="gh"}.
    :::

**Footnotes**

[^1]: If, that is, we ignore the effects of Relativity

[^2]: This matches the definition of the \"proleptic Gregorian\" calendar in Dershowitz and Reingold\'s book *Calendrical Calculations*, where it\'s the base calendar for all computations. See the book for algorithms for converting between proleptic Gregorian ordinals and many other calendar systems.

[^3]: See R. H. van Gent\'s [guide to the mathematics of the ISO 8601 calendar](https://web.archive.org/web/20220531051136/https://webspace.science.uu.nl/~gent0113/calendar/isocalendar.htm) for a good explanation.
