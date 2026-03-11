# Number Protocol {#number}

> Returns `1` if the object *o* provides numeric protocols, and false otherwise. This function always succeeds.
>
> ::: versionchanged
> 3.8 Returns `1` if *o* is an index integer.
> :::

> Returns the result of adding *o1* and *o2*, or `NULL` on failure. This is the equivalent of the Python expression `o1 + o2`.

> Returns the result of subtracting *o2* from *o1*, or `NULL` on failure. This is the equivalent of the Python expression `o1 - o2`.

> Returns the result of multiplying *o1* and *o2*, or `NULL` on failure. This is the equivalent of the Python expression `o1 * o2`.

> Returns the result of matrix multiplication on *o1* and *o2*, or `NULL` on failure. This is the equivalent of the Python expression `o1 @ o2`.
>
> ::: versionadded
> 3.5
> :::

> Return the floor of *o1* divided by *o2*, or `NULL` on failure. This is the equivalent of the Python expression `o1 // o2`.

> Return a reasonable approximation for the mathematical value of *o1* divided by *o2*, or `NULL` on failure. The return value is \"approximate\" because binary floating-point numbers are approximate; it is not possible to represent all real numbers in base two. This function can return a floating-point value when passed two integers. This is the equivalent of the Python expression `o1 / o2`.

> Returns the remainder of dividing *o1* by *o2*, or `NULL` on failure. This is the equivalent of the Python expression `o1 % o2`.

> ::: index
> pair: built-in function; divmod
> :::
>
> See the built-in function `divmod`{.interpreted-text role="func"}. Returns `NULL` on failure. This is the equivalent of the Python expression `divmod(o1, o2)`.

> ::: index
> pair: built-in function; pow
> :::
>
> See the built-in function `pow`{.interpreted-text role="func"}. Returns `NULL` on failure. This is the equivalent of the Python expression `pow(o1, o2, o3)`, where *o3* is optional. If *o3* is to be ignored, pass `Py_None`{.interpreted-text role="c:data"} in its place (passing `NULL` for *o3* would cause an illegal memory access).

> Returns the negation of *o* on success, or `NULL` on failure. This is the equivalent of the Python expression `-o`.

> Returns *o* on success, or `NULL` on failure. This is the equivalent of the Python expression `+o`.

> ::: index
> pair: built-in function; abs
> :::
>
> Returns the absolute value of *o*, or `NULL` on failure. This is the equivalent of the Python expression `abs(o)`.

> Returns the bitwise negation of *o* on success, or `NULL` on failure. This is the equivalent of the Python expression `~o`.

> Returns the result of left shifting *o1* by *o2* on success, or `NULL` on failure. This is the equivalent of the Python expression `o1 << o2`.

> Returns the result of right shifting *o1* by *o2* on success, or `NULL` on failure. This is the equivalent of the Python expression `o1 >> o2`.

> Returns the \"bitwise and\" of *o1* and *o2* on success and `NULL` on failure. This is the equivalent of the Python expression `o1 & o2`.

> Returns the \"bitwise exclusive or\" of *o1* by *o2* on success, or `NULL` on failure. This is the equivalent of the Python expression `o1 ^ o2`.

> Returns the \"bitwise or\" of *o1* and *o2* on success, or `NULL` on failure. This is the equivalent of the Python expression `o1 | o2`.

> Returns the result of adding *o1* and *o2*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 += o2`.

> Returns the result of subtracting *o2* from *o1*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 -= o2`.

> Returns the result of multiplying *o1* and *o2*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 *= o2`.

> Returns the result of matrix multiplication on *o1* and *o2*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 @= o2`.
>
> ::: versionadded
> 3.5
> :::

> Returns the mathematical floor of dividing *o1* by *o2*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 //= o2`.

> Return a reasonable approximation for the mathematical value of *o1* divided by *o2*, or `NULL` on failure. The return value is \"approximate\" because binary floating-point numbers are approximate; it is not possible to represent all real numbers in base two. This function can return a floating-point value when passed two integers. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 /= o2`.

> Returns the remainder of dividing *o1* by *o2*, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 %= o2`.

> ::: index
> pair: built-in function; pow
> :::
>
> See the built-in function `pow`{.interpreted-text role="func"}. Returns `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 **= o2` when o3 is `Py_None`{.interpreted-text role="c:data"}, or an in-place variant of `pow(o1, o2, o3)` otherwise. If *o3* is to be ignored, pass `Py_None`{.interpreted-text role="c:data"} in its place (passing `NULL` for *o3* would cause an illegal memory access).

> Returns the result of left shifting *o1* by *o2* on success, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 <<= o2`.

> Returns the result of right shifting *o1* by *o2* on success, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 >>= o2`.

> Returns the \"bitwise and\" of *o1* and *o2* on success and `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 &= o2`.

> Returns the \"bitwise exclusive or\" of *o1* by *o2* on success, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 ^= o2`.

> Returns the \"bitwise or\" of *o1* and *o2* on success, or `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python statement `o1 |= o2`.

> ::: index
> pair: built-in function; int
> :::
>
> Returns the *o* converted to an integer object on success, or `NULL` on failure. This is the equivalent of the Python expression `int(o)`.

> ::: index
> pair: built-in function; float
> :::
>
> Returns the *o* converted to a float object on success, or `NULL` on failure. This is the equivalent of the Python expression `float(o)`.

> Returns the *o* converted to a Python int on success or `NULL` with a `TypeError`{.interpreted-text role="exc"} exception raised on failure.
>
> ::: versionchanged
> 3.10 The result always has exact type `int`{.interpreted-text role="class"}. Previously, the result could have been an instance of a subclass of `int`.
> :::

> Returns the integer *n* converted to base *base* as a string. The *base* argument must be one of 2, 8, 10, or 16. For base 2, 8, or 16, the returned string is prefixed with a base marker of `'0b'`, `'0o'`, or `'0x'`, respectively. If *n* is not a Python int, it is converted with `PyNumber_Index`{.interpreted-text role="c:func"} first.

> Returns *o* converted to a `Py_ssize_t`{.interpreted-text role="c:type"} value if *o* can be interpreted as an integer. If the call fails, an exception is raised and `-1` is returned.
>
> If *o* can be converted to a Python int but the attempt to convert to a `Py_ssize_t`{.interpreted-text role="c:type"} value would raise an `OverflowError`{.interpreted-text role="exc"}, then the *exc* argument is the type of exception that will be raised (usually `IndexError`{.interpreted-text role="exc"} or `OverflowError`{.interpreted-text role="exc"}). If *exc* is `NULL`, then the exception is cleared and the value is clipped to `PY_SSIZE_T_MIN` for a negative integer or `PY_SSIZE_T_MAX` for a positive integer.

> Returns `1` if *o* is an index integer (has the `nb_index` slot of the `tp_as_number` structure filled in), and `0` otherwise. This function always succeeds.
