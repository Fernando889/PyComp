# Iterator Objects

Python provides two general-purpose iterator objects. The first, a sequence iterator, works with an arbitrary sequence supporting the `~object.__getitem__`{.interpreted-text role="meth"} method. The second works with a callable object and a sentinel value, calling the callable for each item in the sequence, and ending the iteration when the sentinel value is returned.

> Type object for iterator objects returned by `PySeqIter_New`{.interpreted-text role="c:func"} and the one-argument form of the `iter`{.interpreted-text role="func"} built-in function for built-in sequence types.

> Return true if the type of *op* is `PySeqIter_Type`{.interpreted-text role="c:data"}. This function always succeeds.

> Return an iterator that works with a general sequence object, *seq*. The iteration ends when the sequence raises `IndexError`{.interpreted-text role="exc"} for the subscripting operation.

> Type object for iterator objects returned by `PyCallIter_New`{.interpreted-text role="c:func"} and the two-argument form of the `iter`{.interpreted-text role="func"} built-in function.

> Return true if the type of *op* is `PyCallIter_Type`{.interpreted-text role="c:data"}. This function always succeeds.

> Return a new iterator. The first parameter, *callable*, can be any Python callable object that can be called with no parameters; each call to it should return the next item in the iteration. When *callable* returns a value equal to *sentinel*, the iteration will be terminated.

## Range Objects

> The type object for `range`{.interpreted-text role="class"} objects.

> Return true if the object *o* is an instance of a `range`{.interpreted-text role="class"} object. This function always succeeds.

## Builtin Iterator Types

These are built-in iteration types that are included in Python\'s C API, but provide no additional functions. They are here for completeness.

  C type   Python type
  -------- ------------------------------------------------
           `enumerate`{.interpreted-text role="py:class"}
           `filter`{.interpreted-text role="py:class"}
           `map`{.interpreted-text role="py:class"}
           `reversed`{.interpreted-text role="py:class"}
           `zip`{.interpreted-text role="py:class"}

## Other Iterator Objects

> Type objects for iterators of various built-in objects.
>
> Do not create instances of these directly; prefer calling `PyObject_GetIter`{.interpreted-text role="c:func"} instead.
>
> Note that there is no guarantee that a given built-in type uses a given iterator type. For example, iterating over `range`{.interpreted-text role="class"} will use one of two iterator types depending on the size of the range. Other types may start using a similar scheme in the future, without warning.
