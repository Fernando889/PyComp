# `!pyclbr`{.interpreted-text role="mod"} \-\-- Python module browser support

::: {.module synopsis="Supports information extraction for a Python module browser."}
pyclbr
:::

**Source code:** `Lib/pyclbr.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!pyclbr`{.interpreted-text role="mod"} module provides limited information about the functions, classes, and methods defined in a Python-coded module. The information is sufficient to implement a module browser. The information is extracted from the Python source code rather than by importing the module, so this module is safe to use with untrusted code. This restriction makes it impossible to use this module with modules not implemented in Python, including all standard and optional extension modules.

::: function
readmodule(module, path=None)

Return a dictionary mapping module-level class names to class descriptors. If possible, descriptors for imported base classes are included. Parameter *module* is a string with the name of the module to read; it may be the name of a module within a package. If given, *path* is a sequence of directory paths prepended to `sys.path`, which is used to locate the module source code.

This function is the original interface and is only kept for back compatibility. It returns a filtered version of the following.
:::

::: function
readmodule_ex(module, path=None)

Return a dictionary-based tree containing a function or class descriptors for each function and class defined in the module with a `def` or `class` statement. The returned dictionary maps module-level function and class names to their descriptors. Nested objects are entered into the children dictionary of their parent. As with readmodule, *module* names the module to be read and *path* is prepended to sys.path. If the module being read is a package, the returned dictionary has a key `'__path__'` whose value is a list containing the package search path.
:::

::: versionadded
3.7 Descriptors for nested definitions. They are accessed through the new children attribute. Each has a new parent attribute.
:::

The descriptors returned by these functions are instances of Function and Class classes. Users are not expected to create instances of these classes.

## Function Objects {#pyclbr-function-objects}

::::::::::::: Function
Class `!Function`{.interpreted-text role="class"} instances describe functions defined by def statements. They have the following attributes:

::: attribute
file

Name of the file in which the function is defined.
:::

::: attribute
module

The name of the module defining the function described.
:::

::: attribute
name

The name of the function.
:::

::: attribute
lineno

The line number in the file where the definition starts.
:::

:::: attribute
parent

For top-level functions, `None`. For nested functions, the parent.

::: versionadded
3.7
:::
::::

:::: attribute
children

A `dictionary <dict>`{.interpreted-text role="class"} mapping names to descriptors for nested functions and classes.

::: versionadded
3.7
:::
::::

:::: attribute
is_async

`True` for functions that are defined with the `async <async def>`{.interpreted-text role="keyword"} prefix, `False` otherwise.

::: versionadded
3.10
:::
::::
:::::::::::::

## Class Objects {#pyclbr-class-objects}

::::::::::::: Class
Class `!Class`{.interpreted-text role="class"} instances describe classes defined by class statements. They have the same attributes as `Functions <Function>`{.interpreted-text role="class"} and two more.

::: attribute
file

Name of the file in which the class is defined.
:::

::: attribute
module

The name of the module defining the class described.
:::

::: attribute
name

The name of the class.
:::

::: attribute
lineno

The line number in the file where the definition starts.
:::

:::: attribute
parent

For top-level classes, `None`. For nested classes, the parent.

::: versionadded
3.7
:::
::::

:::: attribute
children

A dictionary mapping names to descriptors for nested functions and classes.

::: versionadded
3.7
:::
::::

::: attribute
super

A list of `!Class`{.interpreted-text role="class"} objects which describe the immediate base classes of the class being described. Classes which are named as superclasses but which are not discoverable by `readmodule_ex`{.interpreted-text role="func"} are listed as a string with the class name instead of as `!Class`{.interpreted-text role="class"} objects.
:::

::: attribute
methods

A `dictionary <dict>`{.interpreted-text role="class"} mapping method names to line numbers. This can be derived from the newer `children`{.interpreted-text role="attr"} dictionary, but remains for back-compatibility.
:::
:::::::::::::
