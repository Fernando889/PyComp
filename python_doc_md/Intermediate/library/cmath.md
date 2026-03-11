# `!cmath`{.interpreted-text role="mod"} \-\-- Mathematical functions for complex numbers

::: {.module synopsis="Mathematical functions for complex numbers."}
cmath
:::

------------------------------------------------------------------------

This module provides access to mathematical functions for complex numbers. The functions in this module accept integers, floating-point numbers or complex numbers as arguments. They will also accept any Python object that has either a `~object.__complex__`{.interpreted-text role="meth"} or a `~object.__float__`{.interpreted-text role="meth"} method: these methods are used to convert the object to a complex or floating-point number, respectively, and the function is then applied to the result of the conversion.

:::: note
::: title
Note
:::

For functions involving branch cuts, we have the problem of deciding how to define those functions on the cut itself. Following Kahan\'s \"Branch cuts for complex elementary functions\" paper, as well as Annex G of C99 and later C standards, we use the sign of zero to distinguish one side of the branch cut from the other: for a branch cut along (a portion of) the real axis we look at the sign of the imaginary part, while for a branch cut along the imaginary axis we look at the sign of the real part.

For example, the `cmath.sqrt`{.interpreted-text role="func"} function has a branch cut along the negative real axis. An argument of `-2-0j` is treated as though it lies *below* the branch cut, and so gives a result on the negative imaginary axis:

    >>> cmath.sqrt(-2-0j)
    -1.4142135623730951j

But an argument of `-2+0j` is treated as though it lies above the branch cut:

    >>> cmath.sqrt(-2+0j)
    1.4142135623730951j
::::

+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Conversions to and from polar coordinates**                                                                                                      |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `phase(z) <phase>`{.interpreted-text role="func"}                             | Return the phase of *z*                                            |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `polar(z) <polar>`{.interpreted-text role="func"}                             | Return the representation of *z* in polar coordinates              |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `rect(r, phi) <rect>`{.interpreted-text role="func"}                          | Return the complex number *z* with polar coordinates *r* and *phi* |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Power and logarithmic functions**                                                                                                                |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `exp(z) <exp>`{.interpreted-text role="func"}                                 | Return *e* raised to the power *z*                                 |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `log(z[, base]) <log>`{.interpreted-text role="func"}                         | Return the logarithm of *z* to the given *base* (*e* by default)   |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `log10(z) <log10>`{.interpreted-text role="func"}                             | Return the base-10 logarithm of *z*                                |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `sqrt(z) <sqrt>`{.interpreted-text role="func"}                               | Return the square root of *z*                                      |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Trigonometric functions**                                                                                                                        |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `acos(z) <acos>`{.interpreted-text role="func"}                               | Return the arc cosine of *z*                                       |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `asin(z) <asin>`{.interpreted-text role="func"}                               | Return the arc sine of *z*                                         |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `atan(z) <atan>`{.interpreted-text role="func"}                               | Return the arc tangent of *z*                                      |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `cos(z) <cos>`{.interpreted-text role="func"}                                 | Return the cosine of *z*                                           |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `sin(z) <sin>`{.interpreted-text role="func"}                                 | Return the sine of *z*                                             |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `tan(z) <tan>`{.interpreted-text role="func"}                                 | Return the tangent of *z*                                          |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Hyperbolic functions**                                                                                                                           |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `acosh(z) <acosh>`{.interpreted-text role="func"}                             | Return the inverse hyperbolic cosine of *z*                        |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `asinh(z) <asinh>`{.interpreted-text role="func"}                             | Return the inverse hyperbolic sine of *z*                          |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `atanh(z) <atanh>`{.interpreted-text role="func"}                             | Return the inverse hyperbolic tangent of *z*                       |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `cosh(z) <cosh>`{.interpreted-text role="func"}                               | Return the hyperbolic cosine of *z*                                |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `sinh(z) <sinh>`{.interpreted-text role="func"}                               | Return the hyperbolic sine of *z*                                  |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `tanh(z) <tanh>`{.interpreted-text role="func"}                               | Return the hyperbolic tangent of *z*                               |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Classification functions**                                                                                                                       |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `isfinite(z) <isfinite>`{.interpreted-text role="func"}                       | Check if all components of *z* are finite                          |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `isinf(z) <isinf>`{.interpreted-text role="func"}                             | Check if any component of *z* is infinite                          |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `isnan(z) <isnan>`{.interpreted-text role="func"}                             | Check if any component of *z* is a NaN                             |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `isclose(a, b, *, rel_tol, abs_tol) <isclose>`{.interpreted-text role="func"} | Check if the values *a* and *b* are close to each other            |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| **Constants**                                                                                                                                      |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `pi`{.interpreted-text role="data"}                                           | *π* = 3.141592\...                                                 |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `e`{.interpreted-text role="data"}                                            | *e* = 2.718281\...                                                 |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `tau`{.interpreted-text role="data"}                                          | *τ* = 2*π* = 6.283185\...                                          |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `inf`{.interpreted-text role="data"}                                          | Positive infinity                                                  |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `infj`{.interpreted-text role="data"}                                         | Pure imaginary infinity                                            |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `nan`{.interpreted-text role="data"}                                          | \"Not a number\" (NaN)                                             |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+
| `nanj`{.interpreted-text role="data"}                                         | Pure imaginary NaN                                                 |
+-------------------------------------------------------------------------------+--------------------------------------------------------------------+

## Conversions to and from polar coordinates

A Python complex number `z` is stored internally using *rectangular* or *Cartesian* coordinates. It is completely determined by its *real part* `z.real` and its *imaginary part* `z.imag`.

*Polar coordinates* give an alternative way to represent a complex number. In polar coordinates, a complex number *z* is defined by the modulus *r* and the phase angle *phi*. The modulus *r* is the distance from *z* to the origin, while the phase *phi* is the counterclockwise angle, measured in radians, from the positive x-axis to the line segment that joins the origin to *z*.

The following functions can be used to convert from the native rectangular coordinates to polar coordinates and back.

::: function
phase(z)

Return the phase of *z* (also known as the *argument* of *z*), as a float. `phase(z)` is equivalent to `math.atan2(z.imag, z.real)`. The result lies in the range \[-*π*, *π*\], and the branch cut for this operation lies along the negative real axis. The sign of the result is the same as the sign of `z.imag`, even when `z.imag` is zero:

    >>> phase(-1+0j)
    3.141592653589793
    >>> phase(-1-0j)
    -3.141592653589793
:::

:::: note
::: title
Note
:::

The modulus (absolute value) of a complex number *z* can be computed using the built-in `abs`{.interpreted-text role="func"} function. There is no separate `!cmath`{.interpreted-text role="mod"} module function for this operation.
::::

::: function
polar(z)

Return the representation of *z* in polar coordinates. Returns a pair `(r, phi)` where *r* is the modulus of *z* and *phi* is the phase of *z*. `polar(z)` is equivalent to `(abs(z), phase(z))`.
:::

::: function
rect(r, phi)

Return the complex number *z* with polar coordinates *r* and *phi*. Equivalent to `complex(r * math.cos(phi), r * math.sin(phi))`.
:::

## Power and logarithmic functions

::: function
exp(z)

Return *e* raised to the power *z*, where *e* is the base of natural logarithms.
:::

::: function
log(z\[, base\])

Return the logarithm of *z* to the given *base*. If the *base* is not specified, returns the natural logarithm of *z*. There is one branch cut, from 0 along the negative real axis to -∞.
:::

::: function
log10(z)

Return the base-10 logarithm of *z*. This has the same branch cut as `log`{.interpreted-text role="func"}.
:::

::: function
sqrt(z)

Return the square root of *z*. This has the same branch cut as `log`{.interpreted-text role="func"}.
:::

## Trigonometric functions

::: function
acos(z)

Return the arc cosine of *z*. There are two branch cuts: One extends right from 1 along the real axis to ∞. The other extends left from -1 along the real axis to -∞.
:::

::: function
asin(z)

Return the arc sine of *z*. This has the same branch cuts as `acos`{.interpreted-text role="func"}.
:::

::: function
atan(z)

Return the arc tangent of *z*. There are two branch cuts: One extends from `1j` along the imaginary axis to `∞j`. The other extends from `-1j` along the imaginary axis to `-∞j`.
:::

::: function
cos(z)

Return the cosine of *z*.
:::

::: function
sin(z)

Return the sine of *z*.
:::

::: function
tan(z)

Return the tangent of *z*.
:::

## Hyperbolic functions

::: function
acosh(z)

Return the inverse hyperbolic cosine of *z*. There is one branch cut, extending left from 1 along the real axis to -∞.
:::

::: function
asinh(z)

Return the inverse hyperbolic sine of *z*. There are two branch cuts: One extends from `1j` along the imaginary axis to `∞j`. The other extends from `-1j` along the imaginary axis to `-∞j`.
:::

::: function
atanh(z)

Return the inverse hyperbolic tangent of *z*. There are two branch cuts: One extends from `1` along the real axis to `∞`. The other extends from `-1` along the real axis to `-∞`.
:::

::: function
cosh(z)

Return the hyperbolic cosine of *z*.
:::

::: function
sinh(z)

Return the hyperbolic sine of *z*.
:::

::: function
tanh(z)

Return the hyperbolic tangent of *z*.
:::

## Classification functions

:::: function
isfinite(z)

Return `True` if both the real and imaginary parts of *z* are finite, and `False` otherwise.

::: versionadded
3.2
:::
::::

::: function
isinf(z)

Return `True` if either the real or the imaginary part of *z* is an infinity, and `False` otherwise.
:::

::: function
isnan(z)

Return `True` if either the real or the imaginary part of *z* is a NaN, and `False` otherwise.
:::

::::: function
isclose(a, b, \*, rel_tol=1e-09, abs_tol=0.0)

Return `True` if the values *a* and *b* are close to each other and `False` otherwise.

Whether or not two values are considered close is determined according to given absolute and relative tolerances. If no errors occur, the result will be: `abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`.

*rel_tol* is the relative tolerance \-- it is the maximum allowed difference between *a* and *b*, relative to the larger absolute value of *a* or *b*. For example, to set a tolerance of 5%, pass `rel_tol=0.05`. The default tolerance is `1e-09`, which assures that the two values are the same within about 9 decimal digits. *rel_tol* must be nonnegative and less than `1.0`.

*abs_tol* is the absolute tolerance; it defaults to `0.0` and it must be nonnegative. When comparing `x` to `0.0`, `isclose(x, 0)` is computed as `abs(x) <= rel_tol  * abs(x)`, which is `False` for any `x` and rel_tol less than `1.0`. So add an appropriate positive abs_tol argument to the call.

The IEEE 754 special values of `NaN`, `inf`, and `-inf` will be handled according to IEEE rules. Specifically, `NaN` is not considered close to any other value, including `NaN`. `inf` and `-inf` are only considered close to themselves.

::: versionadded
3.5
:::

::: seealso
`485`{.interpreted-text role="pep"} \-- A function for testing approximate equality
:::
:::::

## Constants

::: data
pi

The mathematical constant *π*, as a float.
:::

::: data
e

The mathematical constant *e*, as a float.
:::

:::: data
tau

The mathematical constant *τ*, as a float.

::: versionadded
3.6
:::
::::

:::: data
inf

Floating-point positive infinity. Equivalent to `float('inf')`.

::: versionadded
3.6
:::
::::

:::: data
infj

Complex number with zero real part and positive infinity imaginary part. Equivalent to `complex(0.0, float('inf'))`.

::: versionadded
3.6
:::
::::

:::: data
nan

A floating-point \"not a number\" (NaN) value. Equivalent to `float('nan')`. See also `math.nan`{.interpreted-text role="data"}.

::: versionadded
3.6
:::
::::

:::: data
nanj

Complex number with zero real part and NaN imaginary part. Equivalent to `complex(0.0, float('nan'))`.

::: versionadded
3.6
:::
::::

::: index
pair: module; math
:::

Note that the selection of functions is similar, but not identical, to that in module `math`{.interpreted-text role="mod"}. The reason for having two modules is that some users aren\'t interested in complex numbers, and perhaps don\'t even know what they are. They would rather have `math.sqrt(-1)` raise an exception than return a complex number. Also note that the functions defined in `!cmath`{.interpreted-text role="mod"} always return a complex number, even if the answer can be expressed as a real number (in which case the complex number has an imaginary part of zero).

A note on branch cuts: They are curves along which the given function fails to be continuous. They are a necessary feature of many complex functions. It is assumed that if you need to compute with complex functions, you will understand about branch cuts. Consult almost any (not too elementary) book on complex variables for enlightenment. For information of the proper choice of branch cuts for numerical purposes, a good reference should be the following:

::: seealso
Kahan, W: Branch cuts for complex elementary functions; or, Much ado about nothing\'s sign bit. In Iserles, A., and Powell, M. (eds.), The state of the art in numerical analysis. Clarendon Press (1987) pp165\--211.
:::
