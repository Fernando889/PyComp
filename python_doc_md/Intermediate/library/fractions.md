# `!fractions`{.interpreted-text role="mod"} \-\-- Rational numbers

::: {.module synopsis="Rational numbers."}
fractions
:::

**Source code:** `Lib/fractions.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!fractions`{.interpreted-text role="mod"} module provides support for rational number arithmetic.

A Fraction instance can be constructed from a pair of rational numbers, from a single number, or from a string.

::: index
single: as_integer_ratio()
:::

:::::::::::::::::::::::::::::: {.Fraction(numerator=0, .denominator=1) .Fraction(number) .Fraction(string)}
The first version requires that *numerator* and *denominator* are instances of `numbers.Rational`{.interpreted-text role="class"} and returns a new `Fraction`{.interpreted-text role="class"} instance with a value equal to `numerator/denominator`. If *denominator* is zero, it raises a `ZeroDivisionError`{.interpreted-text role="exc"}.

The second version requires that *number* is an instance of `numbers.Rational`{.interpreted-text role="class"} or has the `!as_integer_ratio`{.interpreted-text role="meth"} method (this includes `float`{.interpreted-text role="class"} and `decimal.Decimal`{.interpreted-text role="class"}). It returns a `Fraction`{.interpreted-text role="class"} instance with exactly the same value. Assumed, that the `!as_integer_ratio`{.interpreted-text role="meth"} method returns a pair of coprime integers and last one is positive. Note that due to the usual issues with binary point (see `tut-fp-issues`{.interpreted-text role="ref"}), the argument to `Fraction(1.1)` is not exactly equal to 11/10, and so `Fraction(1.1)` does *not* return `Fraction(11, 10)` as one might expect. (But see the documentation for the `limit_denominator`{.interpreted-text role="meth"} method below.)

The last version of the constructor expects a string. The usual form for this instance is:

    [sign] numerator ['/' denominator]

where the optional `sign` may be either \'+\' or \'-\' and `numerator` and `denominator` (if present) are strings of decimal digits (underscores may be used to delimit digits as with integral literals in code). In addition, any string that represents a finite value and is accepted by the `float`{.interpreted-text role="class"} constructor is also accepted by the `Fraction`{.interpreted-text role="class"} constructor. In either form the input string may also have leading and/or trailing whitespace. Here are some examples:

    >>> from fractions import Fraction
    >>> Fraction(16, -10)
    Fraction(-8, 5)
    >>> Fraction(123)
    Fraction(123, 1)
    >>> Fraction()
    Fraction(0, 1)
    >>> Fraction('3/7')
    Fraction(3, 7)
    >>> Fraction(' -3/7 ')
    Fraction(-3, 7)
    >>> Fraction('1.414213 \t\n')
    Fraction(1414213, 1000000)
    >>> Fraction('-.125')
    Fraction(-1, 8)
    >>> Fraction('7e-6')
    Fraction(7, 1000000)
    >>> Fraction(2.25)
    Fraction(9, 4)
    >>> Fraction(1.1)
    Fraction(2476979795053773, 2251799813685248)
    >>> from decimal import Decimal
    >>> Fraction(Decimal('1.1'))
    Fraction(11, 10)

The `Fraction`{.interpreted-text role="class"} class inherits from the abstract base class `numbers.Rational`{.interpreted-text role="class"}, and implements all of the methods and operations from that class. `Fraction`{.interpreted-text role="class"} instances are `hashable`{.interpreted-text role="term"}, and should be treated as immutable. In addition, `Fraction`{.interpreted-text role="class"} has the following properties and methods:

::: versionchanged
3.2 The `Fraction`{.interpreted-text role="class"} constructor now accepts `float`{.interpreted-text role="class"} and `decimal.Decimal`{.interpreted-text role="class"} instances.
:::

::: versionchanged
3.9 The `math.gcd`{.interpreted-text role="func"} function is now used to normalize the *numerator* and *denominator*. `math.gcd`{.interpreted-text role="func"} always returns an `int`{.interpreted-text role="class"} type. Previously, the GCD type depended on *numerator* and *denominator*.
:::

::: versionchanged
3.11 Underscores are now permitted when creating a `Fraction`{.interpreted-text role="class"} instance from a string, following [PEP 515](http://www.python.org/dev/peps/pep-0515/ "PEP 515") rules.
:::

::: versionchanged
3.11 `Fraction`{.interpreted-text role="class"} implements `__int__` now to satisfy `typing.SupportsInt` instance checks.
:::

::: versionchanged
3.12 Space is allowed around the slash for string inputs: `Fraction('2 / 3')`.
:::

::: versionchanged
3.12 `Fraction`{.interpreted-text role="class"} instances now support float-style formatting, with presentation types `"e"`, `"E"`, `"f"`, `"F"`, `"g"`, `"G"` and `"%""`.
:::

::: versionchanged
3.13 Formatting of `Fraction`{.interpreted-text role="class"} instances without a presentation type now supports fill, alignment, sign handling, minimum width and grouping.
:::

::: versionchanged
3.14 The `Fraction`{.interpreted-text role="class"} constructor now accepts any objects with the `!as_integer_ratio`{.interpreted-text role="meth"} method.
:::

::: attribute
numerator

Numerator of the Fraction in lowest term.
:::

::: attribute
denominator

Denominator of the Fraction in lowest terms. Guaranteed to be positive.
:::

:::: method
as_integer_ratio()

Return a tuple of two integers, whose ratio is equal to the original Fraction. The ratio is in lowest terms and has a positive denominator.

::: versionadded
3.8
:::
::::

:::: method
is_integer()

Return `True` if the Fraction is an integer.

::: versionadded
3.12
:::
::::

::::: classmethod
from_float(f)

Alternative constructor which only accepts instances of `float`{.interpreted-text role="class"} or `numbers.Integral`{.interpreted-text role="class"}. Beware that `Fraction.from_float(0.3)` is not the same value as `Fraction(3, 10)`.

:::: note
::: title
Note
:::

From Python 3.2 onwards, you can also construct a `Fraction`{.interpreted-text role="class"} instance directly from a `float`{.interpreted-text role="class"}.
::::
:::::

::::: classmethod
from_decimal(dec)

Alternative constructor which only accepts instances of `decimal.Decimal`{.interpreted-text role="class"} or `numbers.Integral`{.interpreted-text role="class"}.

:::: note
::: title
Note
:::

From Python 3.2 onwards, you can also construct a `Fraction`{.interpreted-text role="class"} instance directly from a `decimal.Decimal`{.interpreted-text role="class"} instance.
::::
:::::

:::: classmethod
from_number(number)

Alternative constructor which only accepts instances of `numbers.Integral`{.interpreted-text role="class"}, `numbers.Rational`{.interpreted-text role="class"}, `float`{.interpreted-text role="class"} or `decimal.Decimal`{.interpreted-text role="class"}, and objects with the `!as_integer_ratio`{.interpreted-text role="meth"} method, but not strings.

::: versionadded
3.14
:::
::::

::: method
limit_denominator(max_denominator=1000000)

Finds and returns the closest `Fraction`{.interpreted-text role="class"} to `self` that has denominator at most max_denominator. This method is useful for finding rational approximations to a given floating-point number:

> \>\>\> from fractions import Fraction \>\>\> Fraction(\'3.1415926535897932\').limit_denominator(1000) Fraction(355, 113)

or for recovering a rational number that\'s represented as a float:

> \>\>\> from math import pi, cos \>\>\> Fraction(cos(pi/3)) Fraction(4503599627370497, 9007199254740992) \>\>\> Fraction(cos(pi/3)).limit_denominator() Fraction(1, 2) \>\>\> Fraction(1.1).limit_denominator() Fraction(11, 10)
:::

::: method
\_\_floor\_\_()

Returns the greatest `int`{.interpreted-text role="class"} `<= self`. This method can also be accessed through the `math.floor`{.interpreted-text role="func"} function:

> \>\>\> from math import floor \>\>\> floor(Fraction(355, 113)) 3
:::

::: method
\_\_ceil\_\_()

Returns the least `int`{.interpreted-text role="class"} `>= self`. This method can also be accessed through the `math.ceil`{.interpreted-text role="func"} function.
:::

::: method
\_\_round\_\_() \_\_round\_\_(ndigits)

The first version returns the nearest `int`{.interpreted-text role="class"} to `self`, rounding half to even. The second version rounds `self` to the nearest multiple of `Fraction(1, 10**ndigits)` (logically, if `ndigits` is negative), again rounding half toward even. This method can also be accessed through the `round`{.interpreted-text role="func"} function.
:::

::: method
\_\_format\_\_(format_spec, /)

Provides support for formatting of `Fraction`{.interpreted-text role="class"} instances via the `str.format`{.interpreted-text role="meth"} method, the `format`{.interpreted-text role="func"} built-in function, or `Formatted string literals <f-strings>`{.interpreted-text role="ref"}.

If the `format_spec` format specification string does not end with one of the presentation types `'e'`, `'E'`, `'f'`, `'F'`, `'g'`, `'G'` or `'%'` then formatting follows the general rules for fill, alignment, sign handling, minimum width, and grouping as described in the `format specification mini-language <formatspec>`{.interpreted-text role="ref"}. The \"alternate form\" flag `'#'` is supported: if present, it forces the output string to always include an explicit denominator, even when the value being formatted is an exact integer. The zero-fill flag `'0'` is not supported.

If the `format_spec` format specification string ends with one of the presentation types `'e'`, `'E'`, `'f'`, `'F'`, `'g'`, `'G'` or `'%'` then formatting follows the rules outlined for the `float`{.interpreted-text role="class"} type in the `formatspec`{.interpreted-text role="ref"} section.

Here are some examples:

    >>> from fractions import Fraction
    >>> format(Fraction(103993, 33102), '_')
    '103_993/33_102'
    >>> format(Fraction(1, 7), '.^+10')
    '...+1/7...'
    >>> format(Fraction(3, 1), '')
    '3'
    >>> format(Fraction(3, 1), '#')
    '3/1'
    >>> format(Fraction(1, 7), '.40g')
    '0.1428571428571428571428571428571428571429'
    >>> format(Fraction('1234567.855'), '_.2f')
    '1_234_567.86'
    >>> f"{Fraction(355, 113):*>20.6e}"
    '********3.141593e+00'
    >>> old_price, new_price = 499, 672
    >>> "{:.2%} price increase".format(Fraction(new_price, old_price) - 1)
    '34.67% price increase'
:::
::::::::::::::::::::::::::::::

::: seealso

Module `numbers`{.interpreted-text role="mod"}

:   The abstract base classes making up the numeric tower.
:::
