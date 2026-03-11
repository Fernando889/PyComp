# List Objects {#listobjects}

::: index
pair: object; list
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python list object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python list type. This is the same object as `list`{.interpreted-text role="class"} in the Python layer.

> Return true if *p* is a list object or an instance of a subtype of the list type. This function always succeeds.

> Return true if *p* is a list object, but not an instance of a subtype of the list type. This function always succeeds.

> Return a new list of length *len* on success, or `NULL` on failure.
>
> :::: note
> ::: title
> Note
> :::
>
> If *len* is greater than zero, the returned list object\'s items are set to `NULL`. Thus you cannot use abstract API functions such as `PySequence_SetItem`{.interpreted-text role="c:func"} or expose the object to Python code before setting all items to a real object with `PyList_SetItem`{.interpreted-text role="c:func"} or `PyList_SET_ITEM()`{.interpreted-text role="c:func"}. The following APIs are safe APIs before the list is fully initialized: `PyList_SetItem()`{.interpreted-text role="c:func"} and `PyList_SET_ITEM()`{.interpreted-text role="c:func"}.
> ::::

> ::: index
> pair: built-in function; len
> :::
>
> Return the length of the list object in *list*; this is equivalent to `len(list)` on a list object.

> Similar to `PyList_Size`{.interpreted-text role="c:func"}, but without error checking.

> Return the object at position *index* in the list pointed to by *list*. The position must be non-negative; indexing from the end of the list is not supported. If *index* is out of bounds (`<0 or >=len(list)`), return `NULL` and set an `IndexError`{.interpreted-text role="exc"} exception.
>
> ::: versionadded
> 3.13
> :::

> Like `PyList_GetItemRef`{.interpreted-text role="c:func"}, but returns a `borrowed reference`{.interpreted-text role="term"} instead of a `strong reference`{.interpreted-text role="term"}.

> Similar to `PyList_GetItem`{.interpreted-text role="c:func"}, but without error checking.

> Set the item at index *index* in list to *item*. Return `0` on success. If *index* is out of bounds, return `-1` and set an `IndexError`{.interpreted-text role="exc"} exception.
>
> :::: note
> ::: title
> Note
> :::
>
> This function \"steals\" a reference to *item* and discards a reference to an item already in the list at the affected position.
> ::::

> Macro form of `PyList_SetItem`{.interpreted-text role="c:func"} without error checking. This is normally only used to fill in new lists where there is no previous content.
>
> Bounds checking is performed as an assertion if Python is built in `debug mode <debug-build>`{.interpreted-text role="ref"} or `with assertions
> <--with-assertions>`{.interpreted-text role="option"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This macro \"steals\" a reference to *item*, and, unlike `PyList_SetItem`{.interpreted-text role="c:func"}, does *not* discard a reference to any item that is being replaced; any reference in *list* at position *i* will be leaked.
> ::::

> Insert the item *item* into list *list* in front of index *index*. Return `0` if successful; return `-1` and set an exception if unsuccessful. Analogous to `list.insert(index, item)`.

> Append the object *item* at the end of list *list*. Return `0` if successful; return `-1` and set an exception if unsuccessful. Analogous to `list.append(item)`.

> Return a list of the objects in *list* containing the objects *between* *low* and *high*. Return `NULL` and set an exception if unsuccessful. Analogous to `list[low:high]`. Indexing from the end of the list is not supported.

> Set the slice of *list* between *low* and *high* to the contents of *itemlist*. Analogous to `list[low:high] = itemlist`. The *itemlist* may be `NULL`, indicating the assignment of an empty list (slice deletion). Return `0` on success, `-1` on failure. Indexing from the end of the list is not supported.

> Extend *list* with the contents of *iterable*. This is the same as `PyList_SetSlice(list, PY_SSIZE_T_MAX, PY_SSIZE_T_MAX, iterable)` and analogous to `list.extend(iterable)` or `list += iterable`.
>
> Raise an exception and return `-1` if *list* is not a `list`{.interpreted-text role="class"} object. Return 0 on success.
>
> ::: versionadded
> 3.13
> :::

> Remove all items from *list*. This is the same as `PyList_SetSlice(list, 0, PY_SSIZE_T_MAX, NULL)` and analogous to `list.clear()` or `del list[:]`.
>
> Raise an exception and return `-1` if *list* is not a `list`{.interpreted-text role="class"} object. Return 0 on success.
>
> ::: versionadded
> 3.13
> :::

> Sort the items of *list* in place. Return `0` on success, `-1` on failure. This is equivalent to `list.sort()`.

> Reverse the items of *list* in place. Return `0` on success, `-1` on failure. This is the equivalent of `list.reverse()`.

> ::: index
> pair: built-in function; tuple
> :::
>
> Return a new tuple object containing the contents of *list*; equivalent to `tuple(list)`.
