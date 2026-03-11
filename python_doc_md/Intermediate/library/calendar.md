# `!calendar`{.interpreted-text role="mod"} \-\-- General calendar-related functions

::: {.module synopsis="Functions for working with calendars, including some emulation
of the Unix cal program."}
calendar
:::

**Source code:** `Lib/calendar.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module allows you to output calendars like the Unix `cal`{.interpreted-text role="program"} program, and provides additional useful functions related to the calendar. By default, these calendars have Monday as the first day of the week, and Sunday as the last (the European convention). Use `setfirstweekday`{.interpreted-text role="func"} to set the first day of the week to Sunday (6) or to any other weekday. Parameters that specify dates are given as integers. For related functionality, see also the `datetime`{.interpreted-text role="mod"} and `time`{.interpreted-text role="mod"} modules.

The functions and classes defined in this module use an idealized calendar, the current Gregorian calendar extended indefinitely in both directions. This matches the definition of the \"proleptic Gregorian\" calendar in Dershowitz and Reingold\'s book \"Calendrical Calculations\", where it\'s the base calendar for all computations. Zero and negative years are interpreted as prescribed by the ISO 8601 standard. Year 0 is 1 BC, year -1 is 2 BC, and so on.

:::::::::::::::::::: Calendar(firstweekday=0)
Creates a `Calendar`{.interpreted-text role="class"} object. *firstweekday* is an integer specifying the first day of the week. `MONDAY`{.interpreted-text role="const"} is `0` (the default), `SUNDAY`{.interpreted-text role="const"} is `6`.

A `Calendar`{.interpreted-text role="class"} object provides several methods that can be used for preparing the calendar data for formatting. This class doesn\'t do any formatting itself. This is the job of subclasses.

`Calendar`{.interpreted-text role="class"} instances have the following methods and attributes:

::: attribute
firstweekday

The first weekday as an integer (0\--6).

This property can also be set and read using `~Calendar.setfirstweekday`{.interpreted-text role="meth"} and `~Calendar.getfirstweekday`{.interpreted-text role="meth"} respectively.
:::

::: method
getfirstweekday()

Return an `int`{.interpreted-text role="class"} for the current first weekday (0\--6).

Identical to reading the `~Calendar.firstweekday`{.interpreted-text role="attr"} property.
:::

::: method
setfirstweekday(firstweekday)

Set the first weekday to *firstweekday*, passed as an `int`{.interpreted-text role="class"} (0\--6)

Identical to setting the `~Calendar.firstweekday`{.interpreted-text role="attr"} property.
:::

::: method
iterweekdays()

Return an iterator for the week day numbers that will be used for one week. The first value from the iterator will be the same as the value of the `~Calendar.firstweekday`{.interpreted-text role="attr"} property.
:::

::: method
itermonthdates(year, month)

Return an iterator for the month *month* (1\--12) in the year *year*. This iterator will return all days (as `datetime.date`{.interpreted-text role="class"} objects) for the month and all days before the start of the month or after the end of the month that are required to get a complete week.
:::

::: method
itermonthdays(year, month)

Return an iterator for the month *month* in the year *year* similar to `itermonthdates`{.interpreted-text role="meth"}, but not restricted by the `datetime.date`{.interpreted-text role="class"} range. Days returned will simply be day of the month numbers. For the days outside of the specified month, the day number is `0`.
:::

::: method
itermonthdays2(year, month)

Return an iterator for the month *month* in the year *year* similar to `itermonthdates`{.interpreted-text role="meth"}, but not restricted by the `datetime.date`{.interpreted-text role="class"} range. Days returned will be tuples consisting of a day of the month number and a week day number.
:::

:::: method
itermonthdays3(year, month)

Return an iterator for the month *month* in the year *year* similar to `itermonthdates`{.interpreted-text role="meth"}, but not restricted by the `datetime.date`{.interpreted-text role="class"} range. Days returned will be tuples consisting of a year, a month and a day of the month numbers.

::: versionadded
3.7
:::
::::

:::: method
itermonthdays4(year, month)

Return an iterator for the month *month* in the year *year* similar to `itermonthdates`{.interpreted-text role="meth"}, but not restricted by the `datetime.date`{.interpreted-text role="class"} range. Days returned will be tuples consisting of a year, a month, a day of the month, and a day of the week numbers.

::: versionadded
3.7
:::
::::

::: method
monthdatescalendar(year, month)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven `datetime.date`{.interpreted-text role="class"} objects.
:::

::: method
monthdays2calendar(year, month)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven tuples of day numbers and weekday numbers.
:::

::: method
monthdayscalendar(year, month)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven day numbers.
:::

::: method
yeardatescalendar(year, width=3)

Return the data for the specified year ready for formatting. The return value is a list of month rows. Each month row contains up to *width* months (defaulting to 3). Each month contains between 4 and 6 weeks and each week contains 1\--7 days. Days are `datetime.date`{.interpreted-text role="class"} objects.
:::

::: method
yeardays2calendar(year, width=3)

Return the data for the specified year ready for formatting (similar to `yeardatescalendar`{.interpreted-text role="meth"}). Entries in the week lists are tuples of day numbers and weekday numbers. Day numbers outside this month are zero.
:::

::: method
yeardayscalendar(year, width=3)

Return the data for the specified year ready for formatting (similar to `yeardatescalendar`{.interpreted-text role="meth"}). Entries in the week lists are day numbers. Day numbers outside this month are zero.
:::
::::::::::::::::::::

::::::::::::: TextCalendar(firstweekday=0)
This class can be used to generate plain text calendars.

`TextCalendar`{.interpreted-text role="class"} instances have the following methods:

::: method
prweek(theweek, width)

Print a week\'s calendar as returned by `formatweek`{.interpreted-text role="meth"} and without a final newline.
:::

::: method
formatday(theday, weekday, width)

Return a string representing a single day formatted with the given *width*. If *theday* is `0`, return a string of spaces of the specified width, representing an empty day. The *weekday* parameter is unused.
:::

::: method
formatweek(theweek, w=0)

Return a single week in a string with no newline. If *w* is provided, it specifies the width of the date columns, which are centered. Depends on the first weekday as specified in the constructor or set by the `setfirstweekday`{.interpreted-text role="meth"} method.
:::

::: method
formatweekday(weekday, width)

Return a string representing the name of a single weekday formatted to the specified *width*. The *weekday* parameter is an integer representing the day of the week, where `0` is Monday and `6` is Sunday.
:::

::: method
formatweekheader(width)

Return a string containing the header row of weekday names, formatted with the given *width* for each column. The names depend on the locale settings and are padded to the specified width.
:::

::: method
formatmonth(theyear, themonth, w=0, l=0)

Return a month\'s calendar in a multi-line string. If *w* is provided, it specifies the width of the date columns, which are centered. If *l* is given, it specifies the number of lines that each week will use. Depends on the first weekday as specified in the constructor or set by the `setfirstweekday`{.interpreted-text role="meth"} method.
:::

::: method
formatmonthname(theyear, themonth, width=0, withyear=True)

Return a string representing the month\'s name centered within the specified *width*. If *withyear* is `True`, include the year in the output. The *theyear* and *themonth* parameters specify the year and month for the name to be formatted respectively.
:::

::: method
prmonth(theyear, themonth, w=0, l=0)

Print a month\'s calendar as returned by `formatmonth`{.interpreted-text role="meth"}.
:::

::: method
formatyear(theyear, w=2, l=1, c=6, m=3)

Return a *m*-column calendar for an entire year as a multi-line string. Optional parameters *w*, *l*, and *c* are for date column width, lines per week, and number of spaces between month columns, respectively. Depends on the first weekday as specified in the constructor or set by the `setfirstweekday`{.interpreted-text role="meth"} method. The earliest year for which a calendar can be generated is platform-dependent.
:::

::: method
pryear(theyear, w=2, l=1, c=6, m=3)

Print the calendar for an entire year as returned by `formatyear`{.interpreted-text role="meth"}.
:::
:::::::::::::

:::::::::::::::::::: HTMLCalendar(firstweekday=0)
This class can be used to generate HTML calendars.

`!HTMLCalendar`{.interpreted-text role="class"} instances have the following methods:

::: method
formatmonth(theyear, themonth, withyear=True)

Return a month\'s calendar as an HTML table. If *withyear* is true the year will be included in the header, otherwise just the month name will be used.
:::

::: method
formatyear(theyear, width=3)

Return a year\'s calendar as an HTML table. *width* (defaulting to 3) specifies the number of months per row.
:::

::: method
formatyearpage(theyear, width=3, css=\'calendar.css\', encoding=None)

Return a year\'s calendar as a complete HTML page. *width* (defaulting to 3) specifies the number of months per row. *css* is the name for the cascading style sheet to be used. `None`{.interpreted-text role="const"} can be passed if no style sheet should be used. *encoding* specifies the encoding to be used for the output (defaulting to `'utf-8'`).
:::

::: method
formatmonthname(theyear, themonth, withyear=True)

Return a month name as an HTML table row. If *withyear* is true the year will be included in the row, otherwise just the month name will be used.
:::

`!HTMLCalendar`{.interpreted-text role="class"} has the following attributes you can override to customize the CSS classes used by the calendar:

::: attribute
cssclasses

A list of CSS classes used for each weekday. The default class list is:

    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

more styles can be added for each day:

    cssclasses = ["mon text-bold", "tue", "wed", "thu", "fri", "sat", "sun red"]

Note that the length of this list must be seven items.
:::

:::: attribute
cssclass_noday

The CSS class for a weekday occurring in the previous or coming month.

::: versionadded
3.7
:::
::::

:::: attribute
cssclasses_weekday_head

A list of CSS classes used for weekday names in the header row. The default is the same as `cssclasses`{.interpreted-text role="attr"}.

::: versionadded
3.7
:::
::::

:::: attribute
cssclass_month_head

The month\'s head CSS class (used by `formatmonthname`{.interpreted-text role="meth"}). The default value is `"month"`.

::: versionadded
3.7
:::
::::

:::: attribute
cssclass_month

The CSS class for the whole month\'s table (used by `formatmonth`{.interpreted-text role="meth"}). The default value is `"month"`.

::: versionadded
3.7
:::
::::

:::: attribute
cssclass_year

The CSS class for the whole year\'s table of tables (used by `formatyear`{.interpreted-text role="meth"}). The default value is `"year"`.

::: versionadded
3.7
:::
::::

:::: attribute
cssclass_year_head

The CSS class for the table head for the whole year (used by `formatyear`{.interpreted-text role="meth"}). The default value is `"year"`.

::: versionadded
3.7
:::
::::

Note that although the naming for the above described class attributes is singular (e.g. `cssclass_month` `cssclass_noday`), one can replace the single CSS class with a space separated list of CSS classes, for example:

    "text-bold text-red"

Here is an example how `!HTMLCalendar`{.interpreted-text role="class"} can be customized:

    class CustomHTMLCal(calendar.HTMLCalendar):
        cssclasses = [style + " text-nowrap" for style in
                      calendar.HTMLCalendar.cssclasses]
        cssclass_month_head = "text-center month-head"
        cssclass_month = "text-center month"
        cssclass_year = "text-italic lead"
::::::::::::::::::::

::: {.LocaleTextCalendar(firstweekday=0, .locale=None)}
This subclass of `TextCalendar`{.interpreted-text role="class"} can be passed a locale name in the constructor and will return month and weekday names in the specified locale.
:::

::: {.LocaleHTMLCalendar(firstweekday=0, .locale=None)}
This subclass of `HTMLCalendar`{.interpreted-text role="class"} can be passed a locale name in the constructor and will return month and weekday names in the specified locale.
:::

:::: note
::: title
Note
:::

The constructor, `!formatweekday`{.interpreted-text role="meth"} and `!formatmonthname`{.interpreted-text role="meth"} methods of these two classes temporarily change the `LC_TIME` locale to the given *locale*. Because the current locale is a process-wide setting, they are not thread-safe.
::::

For simple text calendars this module provides the following functions.

::: function
setfirstweekday(weekday)

Sets the weekday (`0` is Monday, `6` is Sunday) to start each week. The values `MONDAY`{.interpreted-text role="const"}, `TUESDAY`{.interpreted-text role="const"}, `WEDNESDAY`{.interpreted-text role="const"}, `THURSDAY`{.interpreted-text role="const"}, `FRIDAY`{.interpreted-text role="const"}, `SATURDAY`{.interpreted-text role="const"}, and `SUNDAY`{.interpreted-text role="const"} are provided for convenience. For example, to set the first weekday to Sunday:

    import calendar
    calendar.setfirstweekday(calendar.SUNDAY)
:::

::: function
firstweekday()

Returns the current setting for the weekday to start each week.
:::

::: function
isleap(year)

Returns `True`{.interpreted-text role="const"} if *year* is a leap year, otherwise `False`{.interpreted-text role="const"}.
:::

::: function
leapdays(y1, y2)

Returns the number of leap years in the range from *y1* to *y2* (exclusive), where *y1* and *y2* are years.

This function works for ranges spanning a century change.
:::

::: function
weekday(year, month, day)

Returns the day of the week (`0` is Monday) for *year* (`1970`\--\...), *month* (`1`\--`12`), *day* (`1`\--`31`).
:::

::: function
weekheader(n)

Return a header containing abbreviated weekday names. *n* specifies the width in characters for one weekday.
:::

::: function
monthrange(year, month)

Returns weekday of first day of the month and number of days in month, for the specified *year* and *month*.
:::

::: function
monthcalendar(year, month)

Returns a matrix representing a month\'s calendar. Each row represents a week; days outside of the month are represented by zeros. Each week begins with Monday unless set by `setfirstweekday`{.interpreted-text role="func"}.
:::

::: function
prmonth(theyear, themonth, w=0, l=0)

Prints a month\'s calendar as returned by `month`{.interpreted-text role="func"}.
:::

::: function
month(theyear, themonth, w=0, l=0)

Returns a month\'s calendar in a multi-line string using the `~TextCalendar.formatmonth`{.interpreted-text role="meth"} of the `TextCalendar`{.interpreted-text role="class"} class.
:::

::: function
prcal(year, w=0, l=0, c=6, m=3)

Prints the calendar for an entire year as returned by `calendar`{.interpreted-text role="func"}.
:::

::: function
calendar(year, w=2, l=1, c=6, m=3)

Returns a 3-column calendar for an entire year as a multi-line string using the `~TextCalendar.formatyear`{.interpreted-text role="meth"} of the `TextCalendar`{.interpreted-text role="class"} class.
:::

::: function
timegm(tuple)

An unrelated but handy function that takes a time tuple such as returned by the `~time.gmtime`{.interpreted-text role="func"} function in the `time`{.interpreted-text role="mod"} module, and returns the corresponding Unix timestamp value, assuming an epoch of 1970, and the POSIX encoding. In fact, `time.gmtime`{.interpreted-text role="func"} and `timegm`{.interpreted-text role="func"} are each others\' inverse.
:::

The `!calendar`{.interpreted-text role="mod"} module exports the following data attributes:

::: data
day_name

A sequence that represents the days of the week in the current locale, where Monday is day number 0.

> \>\>\> import calendar \>\>\> list(calendar.day_name) \[\'Monday\', \'Tuesday\', \'Wednesday\', \'Thursday\', \'Friday\', \'Saturday\', \'Sunday\'\]
:::

::: data
day_abbr

A sequence that represents the abbreviated days of the week in the current locale, where Mon is day number 0.

> \>\>\> import calendar \>\>\> list(calendar.day_abbr) \[\'Mon\', \'Tue\', \'Wed\', \'Thu\', \'Fri\', \'Sat\', \'Sun\'\]
:::

:::: data
MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY

Aliases for the days of the week, where `MONDAY` is `0` and `SUNDAY` is `6`.

::: versionadded
3.12
:::
::::

:::: Day
Enumeration defining days of the week as integer constants. The members of this enumeration are exported to the module scope as `MONDAY`{.interpreted-text role="data"} through `SUNDAY`{.interpreted-text role="data"}.

::: versionadded
3.12
:::
::::

::::: data
month_name

A sequence that represents the months of the year in the current locale. This follows normal convention of January being month number 1, so it has a length of 13 and `month_name[0]` is the empty string.

> \>\>\> import calendar \>\>\> list(calendar.month_name) \[\'\', \'January\', \'February\', \'March\', \'April\', \'May\', \'June\', \'July\', \'August\', \'September\', \'October\', \'November\', \'December\'\]

:::: caution
::: title
Caution
:::

In locales with alternative month names forms, the `!month_name`{.interpreted-text role="data"} sequence may not be suitable when a month name stands by itself and not as part of a date. For instance, in Greek and in many Slavic and Baltic languages, `!month_name`{.interpreted-text role="data"} will produce the month in genitive case. Use `standalone_month_name`{.interpreted-text role="data"} for a form suitable for standalone use.
::::
:::::

::::: data
month_abbr

A sequence that represents the abbreviated months of the year in the current locale. This follows normal convention of January being month number 1, so it has a length of 13 and `month_abbr[0]` is the empty string.

> \>\>\> import calendar \>\>\> list(calendar.month_abbr) \[\'\', \'Jan\', \'Feb\', \'Mar\', \'Apr\', \'May\', \'Jun\', \'Jul\', \'Aug\', \'Sep\', \'Oct\', \'Nov\', \'Dec\'\]

:::: caution
::: title
Caution
:::

In locales with alternative month names forms, the `!month_abbr`{.interpreted-text role="data"} sequence may not be suitable when a month name stands by itself and not as part of a date. Use `standalone_month_abbr`{.interpreted-text role="data"} for a form suitable for standalone use.
::::
:::::

:::: data
standalone_month_name

A sequence that represents the months of the year in the current locale in the standalone form if the locale provides one. Else it is equivalent to `month_name`{.interpreted-text role="data"}.

::: versionadded
3.15
:::
::::

:::: data
standalone_month_abbr

A sequence that represents the abbreviated months of the year in the current locale in the standalone form if the locale provides one. Else it is equivalent to `month_abbr`{.interpreted-text role="data"}.

::: versionadded
3.15
:::
::::

:::: data
JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER

Aliases for the months of the year, where `JANUARY` is `1` and `DECEMBER` is `12`.

::: versionadded
3.12
:::
::::

:::: Month
Enumeration defining months of the year as integer constants. The members of this enumeration are exported to the module scope as `JANUARY`{.interpreted-text role="data"} through `DECEMBER`{.interpreted-text role="data"}.

::: versionadded
3.12
:::
::::

The `!calendar`{.interpreted-text role="mod"} module defines the following exceptions:

:::: exception
IllegalMonthError(month)

A subclass of `ValueError`{.interpreted-text role="exc"}, raised when the given month number is outside of the range 1-12 (inclusive).

::: attribute
month

The invalid month number.
:::
::::

:::: exception
IllegalWeekdayError(weekday)

A subclass of `ValueError`{.interpreted-text role="exc"}, raised when the given weekday number is outside of the range 0-6 (inclusive).

::: attribute
weekday

The invalid weekday number.
:::
::::

::: seealso

Module `datetime`{.interpreted-text role="mod"}

:   Object-oriented interface to dates and times with similar functionality to the `time`{.interpreted-text role="mod"} module.

Module `time`{.interpreted-text role="mod"}

:   Low-level time related functions.
:::

## Command-line usage {#calendar-cli}

::: versionadded
2.5
:::

The `!calendar`{.interpreted-text role="mod"} module can be executed as a script from the command line to interactively print a calendar.

``` shell
python -m calendar [-h] [-L LOCALE] [-e ENCODING] [-t {text,html}]
                   [-w WIDTH] [-l LINES] [-s SPACING] [-m MONTHS] [-c CSS]
                   [-f FIRST_WEEKDAY] [year] [month]
```

For example, to print a calendar for the year 2000:

``` console
$ python -m calendar 2000
                                  2000

      January                   February                   March
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2          1  2  3  4  5  6             1  2  3  4  5
 3  4  5  6  7  8  9       7  8  9 10 11 12 13       6  7  8  9 10 11 12
10 11 12 13 14 15 16      14 15 16 17 18 19 20      13 14 15 16 17 18 19
17 18 19 20 21 22 23      21 22 23 24 25 26 27      20 21 22 23 24 25 26
24 25 26 27 28 29 30      28 29                     27 28 29 30 31
31

       April                      May                       June
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2       1  2  3  4  5  6  7                1  2  3  4
 3  4  5  6  7  8  9       8  9 10 11 12 13 14       5  6  7  8  9 10 11
10 11 12 13 14 15 16      15 16 17 18 19 20 21      12 13 14 15 16 17 18
17 18 19 20 21 22 23      22 23 24 25 26 27 28      19 20 21 22 23 24 25
24 25 26 27 28 29 30      29 30 31                  26 27 28 29 30

        July                     August                  September
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2          1  2  3  4  5  6                   1  2  3
 3  4  5  6  7  8  9       7  8  9 10 11 12 13       4  5  6  7  8  9 10
10 11 12 13 14 15 16      14 15 16 17 18 19 20      11 12 13 14 15 16 17
17 18 19 20 21 22 23      21 22 23 24 25 26 27      18 19 20 21 22 23 24
24 25 26 27 28 29 30      28 29 30 31               25 26 27 28 29 30
31

      October                   November                  December
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1             1  2  3  4  5                   1  2  3
 2  3  4  5  6  7  8       6  7  8  9 10 11 12       4  5  6  7  8  9 10
 9 10 11 12 13 14 15      13 14 15 16 17 18 19      11 12 13 14 15 16 17
16 17 18 19 20 21 22      20 21 22 23 24 25 26      18 19 20 21 22 23 24
23 24 25 26 27 28 29      27 28 29 30               25 26 27 28 29 30 31
30 31
```

The following options are accepted:

::: program
calendar
:::

::: option

`--help, -h`

:   

Show the help message and exit.
:::

::: option

`--locale LOCALE, -L LOCALE`

:   

The locale to use for month and weekday names. Defaults to English.
:::

::: option

`--encoding ENCODING, -e ENCODING`

:   

The encoding to use for output. `--encoding`{.interpreted-text role="option"} is required if `--locale`{.interpreted-text role="option"} is set.
:::

::: option
\--type {text,html}, -t {text,html}

Print the calendar to the terminal as text, or as an HTML document.
:::

:::: option

`--first-weekday FIRST_WEEKDAY, -f FIRST_WEEKDAY`

:   

The weekday to start each week. Must be a number between 0 (Monday) and 6 (Sunday). Defaults to 0.

::: versionadded
3.13
:::
::::

::: option
year

The year to print the calendar for. Defaults to the current year.
:::

::: option
month

The month of the specified `year`{.interpreted-text role="option"} to print the calendar for. Must be a number between 1 and 12. Defaults to printing a calendar for the full year.
:::

*Text-mode options:*

::: option

`--width WIDTH, -w WIDTH`

:   

The width of the date column in terminal columns. The date is printed centred in the column. Any value lower than 2 is ignored. Defaults to 2.
:::

::: option

`--lines LINES, -l LINES`

:   

The number of lines for each week in terminal rows. The date is printed top-aligned. Any value lower than 1 is ignored. Defaults to 1.
:::

::: option

`--spacing SPACING, -s SPACING`

:   

The space between months in columns. Any value lower than 2 is ignored. Defaults to 6.
:::

::: option

`--months MONTHS, -m MONTHS`

:   

The number of months printed per row. Defaults to 3.
:::

::: versionchanged
3.14 By default, today\'s date is highlighted in color and can be `controlled using environment variables <using-on-controlling-color>`{.interpreted-text role="ref"}.
:::

*HTML-mode options:*

::: option

`--css CSS, -c CSS`

:   

The path of a CSS stylesheet to use for the calendar. This must either be relative to the generated HTML, or an absolute HTTP or `file:///` URL.
:::
