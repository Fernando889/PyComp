# Abstract Objects Layer {#abstract}

The functions in this chapter interact with Python objects regardless of their type, or with wide classes of object types (e.g. all numerical types, or all sequence types). When used on object types for which they do not apply, they will raise a Python exception.

It is not possible to use these functions on objects that are not properly initialized, such as a list object that has been created by `PyList_New`{.interpreted-text role="c:func"}, but whose items have not been set to some non-`NULL` value yet.

::: toctree
object.rst call.rst number.rst sequence.rst mapping.rst iter.rst buffer.rst
:::
