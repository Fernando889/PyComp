# `!copy`{.interpreted-text role="mod"} \-\-- Shallow and deep copy operations

::: {.module synopsis="Shallow and deep copy operations."}
copy
:::

**Source code:** `Lib/copy.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

Assignment statements in Python do not copy objects, they create bindings between a target and an object. For collections that are mutable or contain mutable items, a copy is sometimes needed so one can change one copy without changing the other. This module provides generic shallow and deep copy operations (explained below).

Interface summary:

::: function
copy(obj)

Return a shallow copy of *obj*.
:::

::: function
deepcopy(obj\[, memo\])

Return a deep copy of *obj*.
:::

:::: function
replace(obj, /, \*\*changes)

Creates a new object of the same type as *obj*, replacing fields with values from *changes*.

::: versionadded
3.13
:::
::::

::: exception
Error

Raised for module specific errors.
:::

::: {#shallow_vs_deep_copy}
The difference between shallow and deep copying is only relevant for compound objects (objects that contain other objects, like lists or class instances):
:::

- A *shallow copy* constructs a new compound object and then (to the extent possible) inserts *references* into it to the objects found in the original.
- A *deep copy* constructs a new compound object and then, recursively, inserts *copies* into it of the objects found in the original.

Two problems often exist with deep copy operations that don\'t exist with shallow copy operations:

- Recursive objects (compound objects that, directly or indirectly, contain a reference to themselves) may cause a recursive loop.
- Because deep copy copies everything it may copy too much, such as data which is intended to be shared between copies.

The `deepcopy`{.interpreted-text role="func"} function avoids these problems by:

- keeping a `memo` dictionary of objects already copied during the current copying pass; and
- letting user-defined classes override the copying operation or the set of components copied.

This module does not copy types like module, method, stack trace, stack frame, file, socket, window, or any similar types. It does \"copy\" functions and classes (shallow and deeply), by returning the original object unchanged; this is compatible with the way these are treated by the `pickle`{.interpreted-text role="mod"} module.

Shallow copies of dictionaries can be made using `dict.copy`{.interpreted-text role="meth"}, and of lists by assigning a slice of the entire list, for example, `copied_list = original_list[:]`.

::: index
pair: module; pickle
:::

Classes can use the same interfaces to control copying that they use to control pickling. See the description of module `pickle`{.interpreted-text role="mod"} for information on these methods. In fact, the `!copy`{.interpreted-text role="mod"} module uses the registered pickle functions from the `copyreg`{.interpreted-text role="mod"} module.

::: index
single: \_\_copy\_\_() (copy protocol) single: \_\_deepcopy\_\_() (copy protocol)
:::

::: currentmodule
None
:::

In order for a class to define its own copy implementation, it can define special methods `~object.__copy__`{.interpreted-text role="meth"} and `~object.__deepcopy__`{.interpreted-text role="meth"}.

::: {.method noindexentry=""}
object.\_\_copy\_\_(self)

Called to implement the shallow copy operation; no additional arguments are passed.
:::

::: {.method noindexentry=""}
object.\_\_deepcopy\_\_(self, memo)

Called to implement the deep copy operation; it is passed one argument, the *memo* dictionary. If the `__deepcopy__` implementation needs to make a deep copy of a component, it should call the `~copy.deepcopy`{.interpreted-text role="func"} function with the component as first argument and the *memo* dictionary as second argument. The *memo* dictionary should be treated as an opaque object.
:::

::: index
single: \_\_replace\_\_() (replace protocol)
:::

Function `!copy.replace`{.interpreted-text role="func"} is more limited than `~copy.copy`{.interpreted-text role="func"} and `~copy.deepcopy`{.interpreted-text role="func"}, and only supports named tuples created by `~collections.namedtuple`{.interpreted-text role="func"}, `dataclasses`{.interpreted-text role="mod"}, and other classes which define method `~object.__replace__`{.interpreted-text role="meth"}.

:::: {.method noindexentry=""}
object.\_\_replace\_\_(self, /, \*\*changes)

This method should create a new object of the same type, replacing fields with values from *changes*.

::: versionadded
3.13
:::
::::

::: seealso

Module `pickle`{.interpreted-text role="mod"}

:   Discussion of the special methods used to support object state retrieval and restoration.
:::
