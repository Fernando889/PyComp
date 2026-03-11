# Complex Number Objects {#complexobjects}

::: index
pair: object; complex number
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python complex number object.
>
> > The complex number value, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
> >
> > ::: deprecated-removed
> > 3.15 3.20 Use `PyComplex_AsCComplex`{.interpreted-text role="c:func"} and `PyComplex_FromCComplex`{.interpreted-text role="c:func"} to convert a Python complex number to/from the C `Py_complex`{.interpreted-text role="c:type"} representation.
> > :::

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python complex number type. It is the same object as `complex`{.interpreted-text role="class"} in the Python layer.

> Return true if its argument is a `PyComplexObject`{.interpreted-text role="c:type"} or a subtype of `PyComplexObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Return true if its argument is a `PyComplexObject`{.interpreted-text role="c:type"}, but not a subtype of `PyComplexObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Return a new `PyComplexObject`{.interpreted-text role="c:type"} object from *real* and *imag*. Return `NULL` with an exception set on error.

> Return the real part of *op* as a C `double`{.interpreted-text role="c:expr"}.
>
> If *op* is not a Python complex number object but has a `~object.__complex__`{.interpreted-text role="meth"} method, this method will first be called to convert *op* to a Python complex number object. If `!__complex__`{.interpreted-text role="meth"} is not defined then it falls back to call `PyFloat_AsDouble`{.interpreted-text role="c:func"} and returns its result.
>
> Upon failure, this method returns `-1.0` with an exception set, so one should call `PyErr_Occurred`{.interpreted-text role="c:func"} to check for errors.
>
> ::: versionchanged
> 3.13 Use `~object.__complex__`{.interpreted-text role="meth"} if available.
> :::

> Return the imaginary part of *op* as a C `double`{.interpreted-text role="c:expr"}.
>
> If *op* is not a Python complex number object but has a `~object.__complex__`{.interpreted-text role="meth"} method, this method will first be called to convert *op* to a Python complex number object. If `!__complex__`{.interpreted-text role="meth"} is not defined then it falls back to call `PyFloat_AsDouble`{.interpreted-text role="c:func"} and returns `0.0` on success.
>
> Upon failure, this method returns `-1.0` with an exception set, so one should call `PyErr_Occurred`{.interpreted-text role="c:func"} to check for errors.
>
> ::: versionchanged
> 3.13 Use `~object.__complex__`{.interpreted-text role="meth"} if available.
> :::

> This C structure defines an export format for a Python complex number object.
>
> The structure is defined as:
>
> ``` c
> typedef struct {
>     double real;
>     double imag;
> } Py_complex;
> ```

> Create a new Python complex number object from a C `Py_complex`{.interpreted-text role="c:type"} value. Return `NULL` with an exception set on error.

> Return the `Py_complex`{.interpreted-text role="c:type"} value of the complex number *op*.
>
> If *op* is not a Python complex number object but has a `~object.__complex__`{.interpreted-text role="meth"} method, this method will first be called to convert *op* to a Python complex number object. If `!__complex__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__float__`{.interpreted-text role="meth"}. If `!__float__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__index__`{.interpreted-text role="meth"}.
>
> Upon failure, this method returns `Py_complex`{.interpreted-text role="c:type"} with `~Py_complex.real`{.interpreted-text role="c:member"} set to `-1.0` and with an exception set, so one should call `PyErr_Occurred`{.interpreted-text role="c:func"} to check for errors.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::

## Complex Numbers as C Structures

The API also provides functions for working with complex numbers, using the `Py_complex`{.interpreted-text role="c:type"} representation. Note that the functions which accept these structures as parameters and return them as results do so *by value* rather than dereferencing them through pointers.

Please note, that these functions are `soft deprecated`{.interpreted-text role="term"} since Python 3.15. Avoid using this API in a new code to do complex arithmetic: either use the [Number Protocol](number) API or use native complex types, like `double complex`{.interpreted-text role="c:expr"}.

> Return the sum of two complex numbers, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> ::: deprecated
> 3.15
> :::

> Return the difference between two complex numbers, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> ::: deprecated
> 3.15
> :::

> Return the negation of the complex number *num*, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> ::: deprecated
> 3.15
> :::

> Return the product of two complex numbers, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> ::: deprecated
> 3.15
> :::

> Return the quotient of two complex numbers, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> If *divisor* is null, this method returns zero and sets `errno`{.interpreted-text role="c:data"} to `!EDOM`{.interpreted-text role="c:macro"}.
>
> ::: deprecated
> 3.15
> :::

> Return the exponentiation of *num* by *exp*, using the C `Py_complex`{.interpreted-text role="c:type"} representation.
>
> If *num* is null and *exp* is not a positive real number, this method returns zero and sets `errno`{.interpreted-text role="c:data"} to `!EDOM`{.interpreted-text role="c:macro"}.
>
> Set `errno`{.interpreted-text role="c:data"} to `!ERANGE`{.interpreted-text role="c:macro"} on overflows.
>
> ::: deprecated
> 3.15
> :::

> Return the absolute value of the complex number *num*.
>
> Set `errno`{.interpreted-text role="c:data"} to `!ERANGE`{.interpreted-text role="c:macro"} on overflows.
>
> ::: deprecated
> 3.15
> :::
