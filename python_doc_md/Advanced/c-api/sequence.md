# Sequence Protocol {#sequence}

> Return `1` if the object provides the sequence protocol, and `0` otherwise. Note that it returns `1` for Python classes with a `~object.__getitem__`{.interpreted-text role="meth"} method, unless they are `dict`{.interpreted-text role="class"} subclasses, since in general it is impossible to determine what type of keys the class supports. This function always succeeds.

> Return the concatenation of *o1* and *o2* on success, and `NULL` on failure. This is the equivalent of the Python expression `o1 + o2`.

> Return the result of repeating sequence object *o* *count* times, or `NULL` on failure. This is the equivalent of the Python expression `o * count`.

> Return the concatenation of *o1* and *o2* on success, and `NULL` on failure. The operation is done *in-place* when *o1* supports it. This is the equivalent of the Python expression `o1 += o2`.

> Return the result of repeating sequence object *o* *count* times, or `NULL` on failure. The operation is done *in-place* when *o* supports it. This is the equivalent of the Python expression `o *= count`.

> Return the *i*th element of *o*, or `NULL` on failure. This is the equivalent of the Python expression `o[i]`.

> Return the slice of sequence object *o* between *i1* and *i2*, or `NULL` on failure. This is the equivalent of the Python expression `o[i1:i2]`.

> Assign object *v* to the *i*th element of *o*. Raise an exception and return `-1` on failure; return `0` on success. This is the equivalent of the Python statement `o[i] = v`. This function *does not* steal a reference to *v*.
>
> If *v* is `NULL`, the element is deleted, but this feature is deprecated in favour of using `PySequence_DelItem`{.interpreted-text role="c:func"}.

> Delete the *i*th element of object *o*. Returns `-1` on failure. This is the equivalent of the Python statement `del o[i]`.

> Assign the sequence object *v* to the slice in sequence object *o* from *i1* to *i2*. This is the equivalent of the Python statement `o[i1:i2] = v`.

> Delete the slice in sequence object *o* from *i1* to *i2*. Returns `-1` on failure. This is the equivalent of the Python statement `del o[i1:i2]`.

> Return the number of occurrences of *value* in *o*, that is, return the number of keys for which `o[key] == value`. On failure, return `-1`. This is equivalent to the Python expression `o.count(value)`.

> Determine if *o* contains *value*. If an item in *o* is equal to *value*, return `1`, otherwise return `0`. On error, return `-1`. This is equivalent to the Python expression `value in o`.

> Alias for `PySequence_Contains`{.interpreted-text role="c:func"}.
>
> ::: deprecated
> 3.14 The function is `soft deprecated`{.interpreted-text role="term"} and should no longer be used to write new code.
> :::

> Return the first index *i* for which `o[i] == value`. On error, return `-1`. This is equivalent to the Python expression `o.index(value)`.

> Return a list object with the same contents as the sequence or iterable *o*, or `NULL` on failure. The returned list is guaranteed to be new. This is equivalent to the Python expression `list(o)`.

> ::: index
> pair: built-in function; tuple
> :::
>
> Return a tuple object with the same contents as the sequence or iterable *o*, or `NULL` on failure. If *o* is a tuple, a new reference will be returned, otherwise a tuple will be constructed with the appropriate contents. This is equivalent to the Python expression `tuple(o)`.

> Return the sequence or iterable *o* as an object usable by the other `PySequence_Fast*` family of functions. If the object is not a sequence or iterable, raises `TypeError`{.interpreted-text role="exc"} with *m* as the message text. Returns `NULL` on failure.
>
> The `PySequence_Fast*` functions are thus named because they assume *o* is a `PyTupleObject`{.interpreted-text role="c:type"} or a `PyListObject`{.interpreted-text role="c:type"} and access the data fields of *o* directly.
>
> As a CPython implementation detail, if *o* is already a sequence or list, it will be returned.

> Returns the length of *o*, assuming that *o* was returned by `PySequence_Fast`{.interpreted-text role="c:func"} and that *o* is not `NULL`. The size can also be retrieved by calling `PySequence_Size`{.interpreted-text role="c:func"} on *o*, but `PySequence_Fast_GET_SIZE`{.interpreted-text role="c:func"} is faster because it can assume *o* is a list or tuple.

> Return the *i*th element of *o*, assuming that *o* was returned by `PySequence_Fast`{.interpreted-text role="c:func"}, *o* is not `NULL`, and that *i* is within bounds.

> Return the underlying array of PyObject pointers. Assumes that *o* was returned by `PySequence_Fast`{.interpreted-text role="c:func"} and *o* is not `NULL`.
>
> Note, if a list gets resized, the reallocation may relocate the items array. So, only use the underlying array pointer in contexts where the sequence cannot change.

> Return the *i*th element of *o* or `NULL` on failure. Faster form of `PySequence_GetItem`{.interpreted-text role="c:func"} but without checking that `PySequence_Check`{.interpreted-text role="c:func"} on *o* is true and without adjustment for negative indices.
