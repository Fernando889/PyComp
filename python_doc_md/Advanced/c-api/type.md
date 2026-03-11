# Type Objects {#typeobjects}

::: index
pair: object; type
:::

> The C structure of the objects used to describe built-in types.

> This is the type object for type objects; it is the same object as `type`{.interpreted-text role="class"} in the Python layer.

> Return non-zero if the object *o* is a type object, including instances of types derived from the standard type object. Return 0 in all other cases. This function always succeeds.

> Return non-zero if the object *o* is a type object, but not a subtype of the standard type object. Return 0 in all other cases. This function always succeeds.

> Clear the internal lookup cache. Return the current version tag.

> Return the `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"} member of *type*. This function is primarily meant for use with `Py_LIMITED_API`; the individual flag bits are guaranteed to be stable across Python releases, but access to `~PyTypeObject.tp_flags`{.interpreted-text role="c:member"} itself is not part of the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.4 The return type is now `unsigned long` rather than `long`.
> :::

> Return the type object\'s internal namespace, which is otherwise only exposed via a read-only proxy (`cls.__dict__ <type.__dict__>`{.interpreted-text role="attr"}). This is a replacement for accessing `~PyTypeObject.tp_dict`{.interpreted-text role="c:member"} directly. The returned dictionary must be treated as read-only.
>
> This function is meant for specific embedding and language-binding cases, where direct access to the dict is necessary and indirect access (e.g. via the proxy or `PyObject_GetAttr`{.interpreted-text role="c:func"}) isn\'t adequate.
>
> Extension modules should continue to use `tp_dict`, directly or indirectly, when setting up their own types.
>
> ::: versionadded
> 3.12
> :::

> Invalidate the internal lookup cache for the type and all of its subtypes. This function must be called after any manual modification of the attributes or base classes of the type.

> Register *callback* as a type watcher. Return a non-negative integer ID which must be passed to future calls to `PyType_Watch`{.interpreted-text role="c:func"}. In case of error (e.g. no more watcher IDs available), return `-1` and set an exception.
>
> In free-threaded builds, `PyType_AddWatcher`{.interpreted-text role="c:func"} is not thread-safe, so it must be called at start up (before spawning the first thread).
>
> ::: versionadded
> 3.12
> :::

> Clear watcher identified by *watcher_id* (previously returned from `PyType_AddWatcher`{.interpreted-text role="c:func"}). Return `0` on success, `-1` on error (e.g. if *watcher_id* was never registered.)
>
> An extension should never call `PyType_ClearWatcher` with a *watcher_id* that was not returned to it by a previous call to `PyType_AddWatcher`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.12
> :::

> Mark *type* as watched. The callback granted *watcher_id* by `PyType_AddWatcher`{.interpreted-text role="c:func"} will be called whenever `PyType_Modified`{.interpreted-text role="c:func"} reports a change to *type*. (The callback may be called only once for a series of consecutive modifications to *type*, if `!_PyType_Lookup`{.interpreted-text role="c:func"} is not called on *type* between the modifications; this is an implementation detail and subject to change.)
>
> An extension should never call `PyType_Watch` with a *watcher_id* that was not returned to it by a previous call to `PyType_AddWatcher`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.12
> :::

> Mark *type* as not watched. This undoes a previous call to `PyType_Watch`{.interpreted-text role="c:func"}. *type* must not be `NULL`.
>
> An extension should never call this function with a *watcher_id* that was not returned to it by a previous call to `PyType_AddWatcher`{.interpreted-text role="c:func"}.
>
> On success, this function returns `0`. On failure, this function returns `-1` with an exception set.
>
> ::: versionadded
> 3.12
> :::

> Type of a type-watcher callback function.
>
> The callback must not modify *type* or cause `PyType_Modified`{.interpreted-text role="c:func"} to be called on *type* or any type in its MRO; violating this rule could cause infinite recursion.
>
> ::: versionadded
> 3.12
> :::

> Return non-zero if the type object *o* sets the feature *feature*. Type features are denoted by single bit flags.

> Return non-zero if the type object *type* sets the subclass flag *flag*. Subclass flags are denoted by `Py_TPFLAGS_*_SUBCLASS <Py_TPFLAGS_LONG_SUBCLASS>`{.interpreted-text role="c:macro"}. This function is used by many `_Check` functions for common types.
>
> ::: seealso
> `PyObject_TypeCheck`{.interpreted-text role="c:func"}, which is used as a slower alternative in `_Check` functions for types that don\'t come with subclass flags.
> :::

> Return true if the type object includes support for the cycle detector; this tests the type flag `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"}.

> Return true if *a* is a subtype of *b*.
>
> This function only checks for actual subtypes, which means that `~type.__subclasscheck__`{.interpreted-text role="meth"} is not called on *b*. Call `PyObject_IsSubclass`{.interpreted-text role="c:func"} to do the same check that `issubclass`{.interpreted-text role="func"} would do.

> Generic handler for the `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot of a type object. Uses Python\'s default memory allocation mechanism to allocate memory for a new instance, zeros the memory, then initializes the memory as if by calling `PyObject_Init`{.interpreted-text role="c:func"} or `PyObject_InitVar`{.interpreted-text role="c:func"}.
>
> Do not call this directly to allocate memory for an object; call the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot instead.
>
> For types that support garbage collection (i.e., the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} flag is set), this function behaves like `PyObject_GC_New`{.interpreted-text role="c:macro"} or `PyObject_GC_NewVar`{.interpreted-text role="c:macro"} (except the memory is guaranteed to be zeroed before initialization), and should be paired with `PyObject_GC_Del`{.interpreted-text role="c:func"} in `~PyTypeObject.tp_free`{.interpreted-text role="c:member"}. Otherwise, it behaves like `PyObject_New`{.interpreted-text role="c:macro"} or `PyObject_NewVar`{.interpreted-text role="c:macro"} (except the memory is guaranteed to be zeroed before initialization) and should be paired with `PyObject_Free`{.interpreted-text role="c:func"} in `~PyTypeObject.tp_free`{.interpreted-text role="c:member"}.

> Generic handler for the `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} slot of a type object. Creates a new instance using the type\'s `~PyTypeObject.tp_alloc`{.interpreted-text role="c:member"} slot and returns the resulting object.

> Finalize a type object. This should be called on all type objects to finish their initialization. This function is responsible for adding inherited slots from a type\'s base class. Return `0` on success, or return `-1` and sets an exception on error.
>
> :::: note
> ::: title
> Note
> :::
>
> If some of the base classes implements the GC protocol and the provided type does not include the `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} in its flags, then the GC protocol will be automatically implemented from its parents. On the contrary, if the type being created does include `Py_TPFLAGS_HAVE_GC`{.interpreted-text role="c:macro"} in its flags then it **must** implement the GC protocol itself by at least implementing the `~PyTypeObject.tp_traverse`{.interpreted-text role="c:member"} handle.
> ::::

> Return the type\'s name. Equivalent to getting the type\'s `~type.__name__`{.interpreted-text role="attr"} attribute.
>
> ::: versionadded
> 3.11
> :::

> Return the type\'s qualified name. Equivalent to getting the type\'s `~type.__qualname__`{.interpreted-text role="attr"} attribute.
>
> ::: versionadded
> 3.11
> :::

> Return the type\'s fully qualified name. Equivalent to `f"{type.__module__}.{type.__qualname__}"`, or `type.__qualname__`{.interpreted-text role="attr"} if `type.__module__`{.interpreted-text role="attr"} is not a string or is equal to `"builtins"`.
>
> ::: versionadded
> 3.13
> :::

> Return the type\'s module name. Equivalent to getting the `type.__module__`{.interpreted-text role="attr"} attribute.
>
> ::: versionadded
> 3.13
> :::

> Return the function pointer stored in the given slot. If the result is `NULL`, this indicates that either the slot is `NULL`, or that the function was called with invalid parameters. Callers will typically cast the result pointer into the appropriate function type.
>
> See `PyType_Slot.slot`{.interpreted-text role="c:member"} for possible values of the *slot* argument.
>
> ::: versionadded
> 3.4
> :::
>
> ::: versionchanged
> 3.10 `PyType_GetSlot`{.interpreted-text role="c:func"} can now accept all types. Previously, it was limited to `heap types <heap-types>`{.interpreted-text role="ref"}.
> :::

> Return the module object associated with the given type when the type was created using `PyType_FromModuleAndSpec`{.interpreted-text role="c:func"}.
>
> If no module is associated with the given type, sets `TypeError`{.interpreted-text role="py:class"} and returns `NULL`.
>
> This function is usually used to get the module in which a method is defined. Note that in such a method, `PyType_GetModule(Py_TYPE(self))` may not return the intended result. `Py_TYPE(self)` may be a *subclass* of the intended class, and subclasses are not necessarily defined in the same module as their superclass. See `PyCMethod`{.interpreted-text role="c:type"} to get the class that defines the method. See `PyType_GetModuleByToken`{.interpreted-text role="c:func"} for cases when `!PyCMethod`{.interpreted-text role="c:type"} cannot be used.
>
> ::: versionadded
> 3.9
> :::

> Return the state of the module object associated with the given type. This is a shortcut for calling `PyModule_GetState()`{.interpreted-text role="c:func"} on the result of `PyType_GetModule`{.interpreted-text role="c:func"}.
>
> If no module is associated with the given type, sets `TypeError`{.interpreted-text role="py:class"} and returns `NULL`.
>
> If the *type* has an associated module but its state is `NULL`, returns `NULL` without setting an exception.
>
> ::: versionadded
> 3.9
> :::

> Find the first superclass whose module has the given `module token <ext-module-token>`{.interpreted-text role="ref"}, and return that module.
>
> If no module is found, raises a `TypeError`{.interpreted-text role="py:class"} and returns `NULL`.
>
> This function is intended to be used together with `PyModule_GetState()`{.interpreted-text role="c:func"} to get module state from slot methods (such as `~PyTypeObject.tp_init`{.interpreted-text role="c:member"} or `~PyNumberMethods.nb_add`{.interpreted-text role="c:member"}) and other places where a method\'s defining class cannot be passed using the `PyCMethod`{.interpreted-text role="c:type"} calling convention.
>
> ::: versionadded
> 3.15
> :::

> Find the first superclass whose module was created from the given `PyModuleDef`{.interpreted-text role="c:type"} *def*, or whose `module token <ext-module-token>`{.interpreted-text role="ref"} is equal to *def*, and return that module.
>
> Note that modules created from a `PyModuleDef`{.interpreted-text role="c:type"} always have their token set to the `PyModuleDef`{.interpreted-text role="c:type"}\'s address. In other words, this function is equivalent to `PyType_GetModuleByToken`{.interpreted-text role="c:func"}, except that it:
>
> - returns a borrowed reference, and
> - has a non-`void*` argument type (which is a cosmetic difference in C).
>
> The returned reference is `borrowed <borrowed reference>`{.interpreted-text role="term"} from *type*, and will be valid as long as you hold a reference to *type*. Do not release it with `Py_DECREF`{.interpreted-text role="c:func"} or similar.
>
> ::: versionadded
> 3.11
> :::

> Find the first superclass in *type*\'s `method resolution order`{.interpreted-text role="term"} whose `Py_tp_token`{.interpreted-text role="c:macro"} token is equal to *tp_token*.
>
> - If found, set *\*result* to a new `strong reference`{.interpreted-text role="term"} to it and return `1`.
> - If not found, set *\*result* to `NULL` and return `0`.
> - On error, set *\*result* to `NULL` and return `-1` with an exception set.
>
> The *result* argument may be `NULL`, in which case *\*result* is not set. Use this if you need only the return value.
>
> The *tp_token* argument may not be `NULL`.
>
> ::: versionadded
> 3.14
> :::

> Attempt to assign a version tag to the given type.
>
> Returns 1 if the type already had a valid version tag or a new one was assigned, or 0 if a new tag could not be assigned.
>
> ::: versionadded
> 3.12
> :::

> Return true if instances of *type* support creating weak references, false otherwise. This function always succeeds. *type* must not be `NULL`.
>
> ::: seealso
> \* `weakrefobjects`{.interpreted-text role="ref"} \* `weakref`{.interpreted-text role="py:mod"}
> :::

## Creating Heap-Allocated Types

The following functions and structs are used to create `heap types <heap-types>`{.interpreted-text role="ref"}.

> Create and return a `heap type <heap-types>`{.interpreted-text role="ref"} from the *spec* (see `Py_TPFLAGS_HEAPTYPE`{.interpreted-text role="c:macro"}).
>
> The metaclass *metaclass* is used to construct the resulting type object. When *metaclass* is `NULL`, the metaclass is derived from *bases* (or *Py_tp_base\[s\]* slots if *bases* is `NULL`, see below).
>
> Metaclasses that override `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} are not supported, except if `tp_new` is `NULL`.
>
> The *bases* argument can be used to specify base classes; it can either be only one class or a tuple of classes. If *bases* is `NULL`, the `Py_tp_bases`{.interpreted-text role="c:data"} slot is used instead. If that also is `NULL`, the `Py_tp_base`{.interpreted-text role="c:data"} slot is used instead. If that also is `NULL`, the new type derives from `object`{.interpreted-text role="class"}.
>
> The *module* argument can be used to record the module in which the new class is defined. It must be a module object or `NULL`. If not `NULL`, the module is associated with the new type and can later be retrieved with `PyType_GetModule`{.interpreted-text role="c:func"}. The associated module is not inherited by subclasses; it must be specified for each class individually.
>
> This function calls `PyType_Ready`{.interpreted-text role="c:func"} on the new type.
>
> Note that this function does *not* fully match the behavior of calling `type() <type>`{.interpreted-text role="py:class"} or using the `class`{.interpreted-text role="keyword"} statement. With user-provided base types or metaclasses, prefer `calling <capi-call>`{.interpreted-text role="ref"} `type`{.interpreted-text role="py:class"} (or the metaclass) over `PyType_From*` functions. Specifically:
>
> - `~object.__new__`{.interpreted-text role="py:meth"} is not called on the new class (and it must be set to `type.__new__`).
> - `~object.__init__`{.interpreted-text role="py:meth"} is not called on the new class.
> - `~object.__init_subclass__`{.interpreted-text role="py:meth"} is not called on any bases.
> - `~object.__set_name__`{.interpreted-text role="py:meth"} is not called on new descriptors.
>
> ::: versionadded
> 3.12
> :::

> Equivalent to `PyType_FromMetaclass(NULL, module, spec, bases)`.
>
> ::: versionadded
> 3.9
> :::
>
> ::: versionchanged
> 3.10
>
> The function now accepts a single class as the *bases* argument and `NULL` as the `tp_doc` slot.
> :::
>
> ::: versionchanged
> 3.12
>
> The function now finds and uses a metaclass corresponding to the provided base classes. Previously, only `type`{.interpreted-text role="class"} instances were returned.
>
> The `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} of the metaclass is *ignored*. which may result in incomplete initialization. Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is deprecated.
> :::
>
> ::: versionchanged
> 3.14
>
> Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is no longer allowed.
> :::

> Equivalent to `PyType_FromMetaclass(NULL, NULL, spec, bases)`.
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.12
>
> The function now finds and uses a metaclass corresponding to the provided base classes. Previously, only `type`{.interpreted-text role="class"} instances were returned.
>
> The `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} of the metaclass is *ignored*. which may result in incomplete initialization. Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is deprecated.
> :::
>
> ::: versionchanged
> 3.14
>
> Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is no longer allowed.
> :::

> Equivalent to `PyType_FromMetaclass(NULL, NULL, spec, NULL)`.
>
> ::: versionchanged
> 3.12
>
> The function now finds and uses a metaclass corresponding to the base classes provided in *Py_tp_base\[s\]* slots. Previously, only `type`{.interpreted-text role="class"} instances were returned.
>
> The `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} of the metaclass is *ignored*. which may result in incomplete initialization. Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is deprecated.
> :::
>
> ::: versionchanged
> 3.14
>
> Creating classes whose metaclass overrides `~PyTypeObject.tp_new`{.interpreted-text role="c:member"} is no longer allowed.
> :::

> Make a type immutable: set the `Py_TPFLAGS_IMMUTABLETYPE`{.interpreted-text role="c:macro"} flag.
>
> All base classes of *type* must be immutable.
>
> On success, return `0`. On error, set an exception and return `-1`.
>
> The type must not be used before it\'s made immutable. For example, type instances must not be created before the type is made immutable.
>
> ::: versionadded
> 3.14
> :::

<!-- Keep old URL fragments working (see gh-97908) -->
<span id='c.PyType_Spec.PyType_Spec.name'></span>
<span id='c.PyType_Spec.PyType_Spec.basicsize'></span>
<span id='c.PyType_Spec.PyType_Spec.itemsize'></span>
<span id='c.PyType_Spec.PyType_Spec.flags'></span>
<span id='c.PyType_Spec.PyType_Spec.slots'></span>

> Structure defining a type\'s behavior.
>
> > Name of the type, used to set `PyTypeObject.tp_name`{.interpreted-text role="c:member"}.
>
> > If positive, specifies the size of the instance in bytes. It is used to set `PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"}.
> >
> > If zero, specifies that `~PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"} should be inherited.
> >
> > If negative, the absolute value specifies how much space instances of the class need *in addition* to the superclass. Use `PyObject_GetTypeData`{.interpreted-text role="c:func"} to get a pointer to subclass-specific memory reserved this way. For negative `!basicsize`{.interpreted-text role="c:member"}, Python will insert padding when needed to meet `~PyTypeObject.tp_basicsize`{.interpreted-text role="c:member"}\'s alignment requirements.
> >
> > ::: versionchanged
> > 3.12
> >
> > Previously, this field could not be negative.
> > :::
>
> > Size of one element of a variable-size type, in bytes. Used to set `PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"}. See `tp_itemsize` documentation for caveats.
> >
> > If zero, `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"} is inherited. Extending arbitrary variable-sized classes is dangerous, since some types use a fixed offset for variable-sized memory, which can then overlap fixed-sized memory used by a subclass. To help prevent mistakes, inheriting `itemsize` is only possible in the following situations:
> >
> > - The base is not variable-sized (its `~PyTypeObject.tp_itemsize`{.interpreted-text role="c:member"}).
> > - The requested `PyType_Spec.basicsize`{.interpreted-text role="c:member"} is positive, suggesting that the memory layout of the base class is known.
> > - The requested `PyType_Spec.basicsize`{.interpreted-text role="c:member"} is zero, suggesting that the subclass does not access the instance\'s memory directly.
> > - With the `Py_TPFLAGS_ITEMS_AT_END`{.interpreted-text role="c:macro"} flag.
>
> > Type flags, used to set `PyTypeObject.tp_flags`{.interpreted-text role="c:member"}.
> >
> > If the `Py_TPFLAGS_HEAPTYPE` flag is not set, `PyType_FromSpecWithBases`{.interpreted-text role="c:func"} sets it automatically.
>
> > Array of `PyType_Slot`{.interpreted-text role="c:type"} structures. Terminated by the special slot value `{0, NULL}`.
> >
> > Each slot ID should be specified at most once.

<!-- Keep old URL fragments working (see gh-97908) -->
<span id='c.PyType_Slot.PyType_Slot.slot'></span>
<span id='c.PyType_Slot.PyType_Slot.pfunc'></span>

> Structure defining optional functionality of a type, containing a slot ID and a value pointer.
>
> > A slot ID.
> >
> > Slot IDs are named like the field names of the structures `PyTypeObject`{.interpreted-text role="c:type"}, `PyNumberMethods`{.interpreted-text role="c:type"}, `PySequenceMethods`{.interpreted-text role="c:type"}, `PyMappingMethods`{.interpreted-text role="c:type"} and `PyAsyncMethods`{.interpreted-text role="c:type"} with an added `Py_` prefix. For example, use:
> >
> > - `Py_tp_dealloc`{.interpreted-text role="c:data"} to set `PyTypeObject.tp_dealloc`{.interpreted-text role="c:member"}
> > - `Py_nb_add`{.interpreted-text role="c:data"} to set `PyNumberMethods.nb_add`{.interpreted-text role="c:member"}
> > - `Py_sq_length`{.interpreted-text role="c:data"} to set `PySequenceMethods.sq_length`{.interpreted-text role="c:member"}
> >
> > An additional slot is supported that does not correspond to a `!PyTypeObject`{.interpreted-text role="c:type"} struct field:
> >
> > - `Py_tp_token`{.interpreted-text role="c:data"}
> >
> > The following "offset" fields cannot be set using `PyType_Slot`{.interpreted-text role="c:type"}:
> >
> > - `~PyTypeObject.tp_weaklistoffset`{.interpreted-text role="c:member"} (use `Py_TPFLAGS_MANAGED_WEAKREF`{.interpreted-text role="c:macro"} instead if possible)
> > - `~PyTypeObject.tp_dictoffset`{.interpreted-text role="c:member"} (use `Py_TPFLAGS_MANAGED_DICT`{.interpreted-text role="c:macro"} instead if possible)
> > - `~PyTypeObject.tp_vectorcall_offset`{.interpreted-text role="c:member"} (use `"__vectorcalloffset__"` in `PyMemberDef <pymemberdef-offsets>`{.interpreted-text role="ref"})
> >
> > If it is not possible to switch to a `MANAGED` flag (for example, for vectorcall or to support Python older than 3.12), specify the offset in `Py_tp_members`{.interpreted-text role="c:data"}. See `PyMemberDef documentation <pymemberdef-offsets>`{.interpreted-text role="ref"} for details.
> >
> > The following internal fields cannot be set at all when creating a heap type:
> >
> > - `~PyTypeObject.tp_dict`{.interpreted-text role="c:member"}, `~PyTypeObject.tp_mro`{.interpreted-text role="c:member"}, `~PyTypeObject.tp_cache`{.interpreted-text role="c:member"}, `~PyTypeObject.tp_subclasses`{.interpreted-text role="c:member"}, and `~PyTypeObject.tp_weaklist`{.interpreted-text role="c:member"}.
> >
> > Setting `Py_tp_bases`{.interpreted-text role="c:data"} or `Py_tp_base`{.interpreted-text role="c:data"} may be problematic on some platforms. To avoid issues, use the *bases* argument of `PyType_FromSpecWithBases`{.interpreted-text role="c:func"} instead.
> >
> > ::: versionchanged
> > 3.9 Slots in `PyBufferProcs`{.interpreted-text role="c:type"} may be set in the unlimited API.
> > :::
> >
> > ::: versionchanged
> > 3.11 `~PyBufferProcs.bf_getbuffer`{.interpreted-text role="c:member"} and `~PyBufferProcs.bf_releasebuffer`{.interpreted-text role="c:member"} are now available under the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
> > :::
> >
> > ::: versionchanged
> > 3.14 The field `~PyTypeObject.tp_vectorcall`{.interpreted-text role="c:member"} can now be set using `Py_tp_vectorcall`{.interpreted-text role="c:data"}. See the field\'s documentation for details.
> > :::
>
> > The desired value of the slot. In most cases, this is a pointer to a function.
> >
> > *pfunc* values may not be `NULL`, except for the following slots:
> >
> > - `Py_tp_doc`{.interpreted-text role="c:data"}
> > - `Py_tp_token`{.interpreted-text role="c:data"} (for clarity, prefer `Py_TP_USE_SPEC`{.interpreted-text role="c:data"} rather than `NULL`)

> A `~PyType_Slot.slot`{.interpreted-text role="c:member"} that records a static memory layout ID for a class.
>
> If the `PyType_Spec`{.interpreted-text role="c:type"} of the class is statically allocated, the token can be set to the spec using the special value `Py_TP_USE_SPEC`{.interpreted-text role="c:data"}:
>
> ``` c
> static PyType_Slot foo_slots[] = {
>    {Py_tp_token, Py_TP_USE_SPEC},
> ```
>
> It can also be set to an arbitrary pointer, but you must ensure that:
>
> - The pointer outlives the class, so it\'s not reused for something else while the class exists.
> - It \"belongs\" to the extension module where the class lives, so it will not clash with other extensions.
>
> Use `PyType_GetBaseByToken`{.interpreted-text role="c:func"} to check if a class\'s superclass has a given token \-- that is, check whether the memory layout is compatible.
>
> To get the token for a given class (without considering superclasses), use `PyType_GetSlot`{.interpreted-text role="c:func"} with `Py_tp_token`.
>
> ::: versionadded
> 3.14
> :::
>
> > Used as a value with `Py_tp_token`{.interpreted-text role="c:data"} to set the token to the class\'s `PyType_Spec`{.interpreted-text role="c:type"}. Expands to `NULL`.
> >
> > ::: versionadded
> > 3.14
> > :::
