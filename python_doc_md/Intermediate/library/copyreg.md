# `!copyreg`{.interpreted-text role="mod"} \-\-- Register `!pickle`{.interpreted-text role="mod"} support functions

::: {.module synopsis="Register pickle support functions."}
copyreg
:::

**Source code:** `Lib/copyreg.py`{.interpreted-text role="source"}

::: index
pair: module; pickle pair: module; copy
:::

------------------------------------------------------------------------

The `!copyreg`{.interpreted-text role="mod"} module offers a way to define functions used while pickling specific objects. The `pickle`{.interpreted-text role="mod"} and `copy`{.interpreted-text role="mod"} modules use those functions when pickling/copying those objects. The module provides configuration information about object constructors which are not classes. Such constructors may be factory functions or class instances.

::: function
constructor(object)

Declares *object* to be a valid constructor. If *object* is not callable (and hence not valid as a constructor), raises `TypeError`{.interpreted-text role="exc"}.
:::

::: function
pickle(type, function, constructor_ob=None)

Declares that *function* should be used as a \"reduction\" function for objects of type *type*. *function* must return either a string or a tuple containing between two and six elements. See the `~pickle.Pickler.dispatch_table`{.interpreted-text role="attr"} for more details on the interface of *function*.

The *constructor_ob* parameter is a legacy feature and is now ignored, but if passed it must be a callable.

Note that the `~pickle.Pickler.dispatch_table`{.interpreted-text role="attr"} attribute of a pickler object or subclass of `pickle.Pickler`{.interpreted-text role="class"} can also be used for declaring reduction functions.
:::

## Example

The example below would like to show how to register a pickle function and how it will be used:

> \>\>\> import copyreg, copy, pickle \>\>\> class C: \... def \_\_init\_\_(self, a): \... self.a = a \... \>\>\> def pickle_c(c): \... print(\"pickling a C instance\...\") \... return C, (c.a,) \... \>\>\> copyreg.pickle(C, pickle_c) \>\>\> c = C(1) \>\>\> d = copy.copy(c) \# doctest: +SKIP pickling a C instance\... \>\>\> p = pickle.dumps(c) \# doctest: +SKIP pickling a C instance\...
