# `!math.integer`{.interpreted-text role="mod"} \-\-- integer-specific mathematics functions

::: {.module synopsis="Integer-specific mathematics functions."}
math.integer
:::

::: versionadded
3.15
:::

------------------------------------------------------------------------

This module provides access to the mathematical functions defined for integer arguments. These functions accept integers and objects that implement the `~object.__index__`{.interpreted-text role="meth"} method which is used to convert the object to an integer number.

The following functions are provided by this module. All return values are computed exactly and are integers.

::: function
comb(n, k, /)

Return the number of ways to choose *k* items from *n* items without repetition and without order.

Evaluates to `n! / (k! * (n - k)!)` when `k <= n` and evaluates to zero when `k > n`.

Also called the binomial coefficient because it is equivalent to the coefficient of k-th term in polynomial expansion of `(1 + x)ⁿ`.

Raises `ValueError`{.interpreted-text role="exc"} if either of the arguments are negative.
:::

::: function
factorial(n, /)

Return factorial of the nonnegative integer *n*.
:::

::: function
gcd(\*integers)

Return the greatest common divisor of the specified integer arguments. If any of the arguments is nonzero, then the returned value is the largest positive integer that is a divisor of all arguments. If all arguments are zero, then the returned value is `0`. `gcd()` without arguments returns `0`.
:::

::: function
isqrt(n, /)

Return the integer square root of the nonnegative integer *n*. This is the floor of the exact square root of *n*, or equivalently the greatest integer *a* such that *a*²   ≤   *n*.

For some applications, it may be more convenient to have the least integer *a* such that *n*   ≤   *a*², or in other words the ceiling of the exact square root of *n*. For positive *n*, this can be computed using `a = 1 + isqrt(n - 1)`.
:::

::: function
lcm(\*integers)

Return the least common multiple of the specified integer arguments. If all arguments are nonzero, then the returned value is the smallest positive integer that is a multiple of all arguments. If any of the arguments is zero, then the returned value is `0`. `lcm()` without arguments returns `1`.
:::

::: function
perm(n, k=None, /)

Return the number of ways to choose *k* items from *n* items without repetition and with order.

Evaluates to `n! / (n - k)!` when `k <= n` and evaluates to zero when `k > n`.

If *k* is not specified or is `None`, then *k* defaults to *n* and the function returns `n!`.

Raises `ValueError`{.interpreted-text role="exc"} if either of the arguments are negative.
:::
