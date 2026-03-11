# Dictionary objects {#dictobjects}

::: index
pair: object; dictionary
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python dictionary object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python dictionary type. This is the same object as `dict`{.interpreted-text role="class"} in the Python layer.

> Return true if *p* is a dict object or an instance of a subtype of the dict type. This function always succeeds.

> Return true if *p* is a dict object, but not an instance of a subtype of the dict type. This function always succeeds.

> Return a new empty dictionary, or `NULL` on failure.

> Return a `types.MappingProxyType`{.interpreted-text role="class"} object for a mapping which enforces read-only behavior. This is normally used to create a view to prevent modification of the dictionary for non-dynamic class types.

> The type object for mapping proxy objects created by `PyDictProxy_New`{.interpreted-text role="c:func"} and for the read-only `__dict__` attribute of many built-in types. A `PyDictProxy_Type`{.interpreted-text role="c:type"} instance provides a dynamic, read-only view of an underlying dictionary: changes to the underlying dictionary are reflected in the proxy, but the proxy itself does not support mutation operations. This corresponds to `types.MappingProxyType`{.interpreted-text role="class"} in Python.

> Empty an existing dictionary of all key-value pairs.
>
> Do nothing if the argument is not a `dict`{.interpreted-text role="class"} or a `!dict`{.interpreted-text role="class"} subclass.

> Determine if dictionary *p* contains *key*. If an item in *p* matches *key*, return `1`, otherwise return `0`. On error, return `-1`. This is equivalent to the Python expression `key in p`.

> This is the same as `PyDict_Contains`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Return a new dictionary that contains the same key-value pairs as *p*.

> Insert *val* into the dictionary *p* with a key of *key*. *key* must be `hashable`{.interpreted-text role="term"}; if it isn\'t, `TypeError`{.interpreted-text role="exc"} will be raised. Return `0` on success or `-1` on failure. This function *does not* steal a reference to *val*.

> This is the same as `PyDict_SetItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> Remove the entry in dictionary *p* with key *key*. *key* must be `hashable`{.interpreted-text role="term"}; if it isn\'t, `TypeError`{.interpreted-text role="exc"} is raised. If *key* is not in the dictionary, `KeyError`{.interpreted-text role="exc"} is raised. Return `0` on success or `-1` on failure.

> This is the same as `PyDict_DelItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> Return a new `strong reference`{.interpreted-text role="term"} to the object from dictionary *p* which has a key *key*:
>
> - If the key is present, set *\*result* to a new `strong reference`{.interpreted-text role="term"} to the value and return `1`.
> - If the key is missing, set *\*result* to `NULL` and return `0`.
> - On error, raise an exception and return `-1`.
>
> ::: versionadded
> 3.13
> :::
>
> See also the `PyObject_GetItem`{.interpreted-text role="c:func"} function.

> Return a `borrowed reference`{.interpreted-text role="term"} to the object from dictionary *p* which has a key *key*. Return `NULL` if the key *key* is missing *without* setting an exception.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions that occur while this calls `~object.__hash__`{.interpreted-text role="meth"} and `~object.__eq__`{.interpreted-text role="meth"} methods are silently ignored. Prefer the `PyDict_GetItemWithError`{.interpreted-text role="c:func"} function instead.
> ::::
>
> ::: versionchanged
> 3.10 Calling this API without an `attached thread state`{.interpreted-text role="term"} had been allowed for historical reason. It is no longer allowed.
> :::

> Variant of `PyDict_GetItem`{.interpreted-text role="c:func"} that does not suppress exceptions. Return `NULL` **with** an exception set if an exception occurred. Return `NULL` **without** an exception set if the key wasn\'t present.

> This is the same as `PyDict_GetItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions that occur while this calls `~object.__hash__`{.interpreted-text role="meth"} and `~object.__eq__`{.interpreted-text role="meth"} methods or while creating the temporary `str`{.interpreted-text role="class"} object are silently ignored. Prefer using the `PyDict_GetItemWithError`{.interpreted-text role="c:func"} function with your own `PyUnicode_FromString`{.interpreted-text role="c:func"} *key* instead.
> ::::

> Similar to `PyDict_GetItemRef`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> This is the same as the Python-level `dict.setdefault`{.interpreted-text role="meth"}. If present, it returns the value corresponding to *key* from the dictionary *p*. If the key is not in the dict, it is inserted with value *defaultobj* and *defaultobj* is returned. This function evaluates the hash function of *key* only once, instead of evaluating it independently for the lookup and the insertion.
>
> ::: versionadded
> 3.4
> :::

> Inserts *default_value* into the dictionary *p* with a key of *key* if the key is not already present in the dictionary. If *result* is not `NULL`, then *\*result* is set to a `strong reference`{.interpreted-text role="term"} to either *default_value*, if the key was not present, or the existing value, if *key* was already present in the dictionary. Returns `1` if the key was present and *default_value* was not inserted, or `0` if the key was not present and *default_value* was inserted. On failure, returns `-1`, sets an exception, and sets `*result` to `NULL`.
>
> For clarity: if you have a strong reference to *default_value* before calling this function, then after it returns, you hold a strong reference to both *default_value* and *\*result* (if it\'s not `NULL`). These may refer to the same object: in that case you hold two separate references to it.
>
> ::: versionadded
> 3.13
> :::

> Remove *key* from dictionary *p* and optionally return the removed value. Do not raise `KeyError`{.interpreted-text role="exc"} if the key is missing.
>
> - If the key is present, set *\*result* to a new reference to the removed value if *result* is not `NULL`, and return `1`.
> - If the key is missing, set *\*result* to `NULL` if *result* is not `NULL`, and return `0`.
> - On error, raise an exception and return `-1`.
>
> Similar to `dict.pop`{.interpreted-text role="meth"}, but without the default value and not raising `KeyError`{.interpreted-text role="exc"} if the key is missing.
>
> ::: versionadded
> 3.13
> :::

> Similar to `PyDict_Pop`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Return a `PyListObject`{.interpreted-text role="c:type"} containing all the items from the dictionary.

> Return a `PyListObject`{.interpreted-text role="c:type"} containing all the keys from the dictionary.

> Return a `PyListObject`{.interpreted-text role="c:type"} containing all the values from the dictionary *p*.

> ::: index
> pair: built-in function; len
> :::
>
> Return the number of items in the dictionary. This is equivalent to `len(p)` on a dictionary.

> Similar to `PyDict_Size`{.interpreted-text role="c:func"}, but without error checking.

> Iterate over all key-value pairs in the dictionary *p*. The `Py_ssize_t`{.interpreted-text role="c:type"} referred to by *ppos* must be initialized to `0` prior to the first call to this function to start the iteration; the function returns true for each pair in the dictionary, and false once all pairs have been reported. The parameters *pkey* and *pvalue* should either point to `PyObject*`{.interpreted-text role="c:expr"} variables that will be filled in with each key and value, respectively, or may be `NULL`. Any references returned through them are borrowed. *ppos* should not be altered during iteration. Its value represents offsets within the internal dictionary structure, and since the structure is sparse, the offsets are not consecutive.
>
> For example:
>
> ``` c
> PyObject *key, *value;
> Py_ssize_t pos = 0;
>
> while (PyDict_Next(self->dict, &pos, &key, &value)) {
>     /* do something interesting with the values... */
>     ...
> }
> ```
>
> The dictionary *p* should not be mutated during iteration. It is safe to modify the values of the keys as you iterate over the dictionary, but only so long as the set of keys does not change. For example:
>
> ``` c
> PyObject *key, *value;
> Py_ssize_t pos = 0;
>
> while (PyDict_Next(self->dict, &pos, &key, &value)) {
>     long i = PyLong_AsLong(value);
>     if (i == -1 && PyErr_Occurred()) {
>         return -1;
>     }
>     PyObject *o = PyLong_FromLong(i + 1);
>     if (o == NULL)
>         return -1;
>     if (PyDict_SetItem(self->dict, key, o) < 0) {
>         Py_DECREF(o);
>         return -1;
>     }
>     Py_DECREF(o);
> }
> ```
>
> The function is not thread-safe in the `free-threaded <free threading>`{.interpreted-text role="term"} build without external synchronization. You can use `Py_BEGIN_CRITICAL_SECTION`{.interpreted-text role="c:macro"} to lock the dictionary while iterating over it:
>
> ``` c
> Py_BEGIN_CRITICAL_SECTION(self->dict);
> while (PyDict_Next(self->dict, &pos, &key, &value)) {
>     ...
> }
> Py_END_CRITICAL_SECTION();
> ```
>
> :::: note
> ::: title
> Note
> :::
>
> On the free-threaded build, this function can be used safely inside a critical section. However, the references returned for *pkey* and *pvalue* are `borrowed <borrowed reference>`{.interpreted-text role="term"} and are only valid while the critical section is held. If you need to use these objects outside the critical section or when the critical section can be suspended, create a `strong reference <strong reference>`{.interpreted-text role="term"} (for example, using `Py_NewRef`{.interpreted-text role="c:func"}).
> ::::

> Iterate over mapping object *b* adding key-value pairs to dictionary *a*. *b* may be a dictionary, or any object supporting `PyMapping_Keys`{.interpreted-text role="c:func"} and `PyObject_GetItem`{.interpreted-text role="c:func"}. If *override* is true, existing pairs in *a* will be replaced if a matching key is found in *b*, otherwise pairs will only be added if there is not a matching key in *a*. Return `0` on success or `-1` if an exception was raised.

> This is the same as `PyDict_Merge(a, b, 1)` in C, and is similar to `a.update(b)` in Python except that `PyDict_Update`{.interpreted-text role="c:func"} doesn\'t fall back to the iterating over a sequence of key value pairs if the second argument has no \"keys\" attribute. Return `0` on success or `-1` if an exception was raised.

> Update or merge into dictionary *a*, from the key-value pairs in *seq2*. *seq2* must be an iterable object producing iterable objects of length 2, viewed as key-value pairs. In case of duplicate keys, the last wins if *override* is true, else the first wins. Return `0` on success or `-1` if an exception was raised. Equivalent Python (except for the return value):
>
> ``` c
> def PyDict_MergeFromSeq2(a, seq2, override):
>     for key, value in seq2:
>         if override or key not in a:
>             a[key] = value
> ```

> Register *callback* as a dictionary watcher. Return a non-negative integer id which must be passed to future calls to `PyDict_Watch`{.interpreted-text role="c:func"}. In case of error (e.g. no more watcher IDs available), return `-1` and set an exception.
>
> ::: versionadded
> 3.12
> :::

> Clear watcher identified by *watcher_id* previously returned from `PyDict_AddWatcher`{.interpreted-text role="c:func"}. Return `0` on success, `-1` on error (e.g. if the given *watcher_id* was never registered.)
>
> ::: versionadded
> 3.12
> :::

> Mark dictionary *dict* as watched. The callback granted *watcher_id* by `PyDict_AddWatcher`{.interpreted-text role="c:func"} will be called when *dict* is modified or deallocated. Return `0` on success or `-1` on error.
>
> ::: versionadded
> 3.12
> :::

> Mark dictionary *dict* as no longer watched. The callback granted *watcher_id* by `PyDict_AddWatcher`{.interpreted-text role="c:func"} will no longer be called when *dict* is modified or deallocated. The dict must previously have been watched by this watcher. Return `0` on success or `-1` on error.
>
> ::: versionadded
> 3.12
> :::

> Enumeration of possible dictionary watcher events: `PyDict_EVENT_ADDED`, `PyDict_EVENT_MODIFIED`, `PyDict_EVENT_DELETED`, `PyDict_EVENT_CLONED`, `PyDict_EVENT_CLEARED`, or `PyDict_EVENT_DEALLOCATED`.
>
> ::: versionadded
> 3.12
> :::

> Type of a dict watcher callback function.
>
> If *event* is `PyDict_EVENT_CLEARED` or `PyDict_EVENT_DEALLOCATED`, both *key* and *new_value* will be `NULL`. If *event* is `PyDict_EVENT_ADDED` or `PyDict_EVENT_MODIFIED`, *new_value* will be the new value for *key*. If *event* is `PyDict_EVENT_DELETED`, *key* is being deleted from the dictionary and *new_value* will be `NULL`.
>
> `PyDict_EVENT_CLONED` occurs when *dict* was previously empty and another dict is merged into it. To maintain efficiency of this operation, per-key `PyDict_EVENT_ADDED` events are not issued in this case; instead a single `PyDict_EVENT_CLONED` is issued, and *key* will be the source dictionary.
>
> The callback may inspect but must not modify *dict*; doing so could have unpredictable effects, including infinite recursion. Do not trigger Python code execution in the callback, as it could modify the dict as a side effect.
>
> If *event* is `PyDict_EVENT_DEALLOCATED`, taking a new reference in the callback to the about-to-be-destroyed dictionary will resurrect it and prevent it from being freed at this time. When the resurrected object is destroyed later, any watcher callbacks active at that time will be called again.
>
> Callbacks occur before the notified modification to *dict* takes place, so the prior state of *dict* can be inspected.
>
> If the callback sets an exception, it must return `-1`; this exception will be printed as an unraisable exception using `PyErr_WriteUnraisable`{.interpreted-text role="c:func"}. Otherwise it should return `0`.
>
> There may already be a pending exception set on entry to the callback. In this case, the callback should return `0` with the same exception still set. This means the callback may not call any other API that can set an exception unless it saves and clears the exception state first, and restores it before returning.
>
> ::: versionadded
> 3.12
> :::

## Dictionary view objects

> Return true if *op* is a view of a set inside a dictionary. This is currently equivalent to `PyDictKeys_Check(op) || PyDictItems_Check(op)`{.interpreted-text role="c:expr"}. This function always succeeds.

> Type object for a view of dictionary keys. In Python, this is the type of the object returned by `dict.keys`{.interpreted-text role="meth"}.

> Return true if *op* is an instance of a dictionary keys view. This function always succeeds.

> Type object for a view of dictionary values. In Python, this is the type of the object returned by `dict.values`{.interpreted-text role="meth"}.

> Return true if *op* is an instance of a dictionary values view. This function always succeeds.

> Type object for a view of dictionary items. In Python, this is the type of the object returned by `dict.items`{.interpreted-text role="meth"}.

> Return true if *op* is an instance of a dictionary items view. This function always succeeds.

## Frozen dictionary objects

::: versionadded
next
:::

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python frozen dictionary type. This is the same object as `frozendict`{.interpreted-text role="class"} in the Python layer.

> Return true if *p* is a `dict`{.interpreted-text role="class"} object, a `frozendict`{.interpreted-text role="class"} object, or an instance of a subtype of the `!dict`{.interpreted-text role="class"} or `!frozendict`{.interpreted-text role="class"} type. This function always succeeds.

> Return true if *p* is a `dict`{.interpreted-text role="class"} object or a `frozendict`{.interpreted-text role="class"} object, but not an instance of a subtype of the `!dict`{.interpreted-text role="class"} or `!frozendict`{.interpreted-text role="class"} type. This function always succeeds.

> Return true if *p* is a `frozendict`{.interpreted-text role="class"} object or an instance of a subtype of the `!frozendict`{.interpreted-text role="class"} type. This function always succeeds.

> Return true if *p* is a `frozendict`{.interpreted-text role="class"} object, but not an instance of a subtype of the `!frozendict`{.interpreted-text role="class"} type. This function always succeeds.

> Return a new `frozendict`{.interpreted-text role="class"} from an iterable, or `NULL` on failure with an exception set.
>
> Create an empty dictionary if *iterable* is `NULL`.

## Ordered dictionaries

Python\'s C API provides interface for `collections.OrderedDict`{.interpreted-text role="class"} from C. Since Python 3.7, dictionaries are ordered by default, so there is usually little need for these functions; prefer `PyDict*` where possible.

> Type object for ordered dictionaries. This is the same object as `collections.OrderedDict`{.interpreted-text role="class"} in the Python layer.

> Return true if *od* is an ordered dictionary object or an instance of a subtype of the `~collections.OrderedDict`{.interpreted-text role="class"} type. This function always succeeds.

> Return true if *od* is an ordered dictionary object, but not an instance of a subtype of the `~collections.OrderedDict`{.interpreted-text role="class"} type. This function always succeeds.

> Analogous to `PyDictKeys_Type`{.interpreted-text role="c:type"} for ordered dictionaries.

> Analogous to `PyDictValues_Type`{.interpreted-text role="c:type"} for ordered dictionaries.

> Analogous to `PyDictItems_Type`{.interpreted-text role="c:type"} for ordered dictionaries.

> Return a new empty ordered dictionary, or `NULL` on failure.
>
> This is analogous to `PyDict_New`{.interpreted-text role="c:func"}.

> Insert *value* into the ordered dictionary *od* with a key of *key*. Return `0` on success or `-1` with an exception set on failure.
>
> This is analogous to `PyDict_SetItem`{.interpreted-text role="c:func"}.

> Remove the entry in the ordered dictionary *od* with key *key*. Return `0` on success or `-1` with an exception set on failure.
>
> This is analogous to `PyDict_DelItem`{.interpreted-text role="c:func"}.

These are `soft deprecated`{.interpreted-text role="term"} aliases to `PyDict` APIs:

  `PyODict`   `PyDict`
  ----------- ------------------------------------------------------------
              `PyDict_GetItem`{.interpreted-text role="c:func"}
              `PyDict_GetItemWithError`{.interpreted-text role="c:func"}
              `PyDict_GetItemString`{.interpreted-text role="c:func"}
              `PyDict_Contains`{.interpreted-text role="c:func"}
              `PyDict_Size`{.interpreted-text role="c:func"}
              `PyDict_GET_SIZE`{.interpreted-text role="c:func"}
