# Descriptor Objects

\"Descriptors\" are objects that describe some attribute of an object. They are found in the dictionary of type objects.

> The type object for member descriptor objects created from `PyMemberDef`{.interpreted-text role="c:type"} structures. These descriptors expose fields of a C struct as attributes on a type, and correspond to `types.MemberDescriptorType`{.interpreted-text role="class"} objects in Python.

> The type object for get/set descriptor objects created from `PyGetSetDef`{.interpreted-text role="c:type"} structures. These descriptors implement attributes whose value is computed by C getter and setter functions, and are used for many built-in type attributes.

> The type object for method descriptor objects created from `PyMethodDef`{.interpreted-text role="c:type"} structures. These descriptors expose C functions as methods on a type, and correspond to `types.MemberDescriptorType`{.interpreted-text role="class"} objects in Python.

> The type object for wrapper descriptor objects created by `PyDescr_NewWrapper`{.interpreted-text role="c:func"} and `PyWrapper_New`{.interpreted-text role="c:func"}. Wrapper descriptors are used internally to expose special methods implemented via wrapper structures, and appear in Python as `types.WrapperDescriptorType`{.interpreted-text role="class"} objects.

> Return non-zero if the descriptor object *descr* describes a data attribute, or `0` if it describes a method. *descr* must be a descriptor object; there is no error checking.

> This is a `soft deprecated`{.interpreted-text role="term"} macro including the common fields for a descriptor object.
>
> This was included in Python\'s C API by mistake; do not use it in extensions. For creating custom descriptor objects, create a class implementing the descriptor protocol (`~PyTypeObject.tp_descr_get`{.interpreted-text role="c:member"} and `~PyTypeObject.tp_descr_set`{.interpreted-text role="c:member"}).

## Built-in descriptors

> The type object for property objects. This is the same object as `property`{.interpreted-text role="class"} in the Python layer.

> The type object for super objects. This is the same object as `super`{.interpreted-text role="class"} in the Python layer.

> The type of class method objects. This is the same object as `classmethod`{.interpreted-text role="class"} in the Python layer.

> The type object for C-level class method descriptor objects. This is the type of the descriptors created for `classmethod`{.interpreted-text role="func"} defined in C extension types, and is the same object as `classmethod`{.interpreted-text role="class"} in Python.

> Create a new `classmethod`{.interpreted-text role="class"} object wrapping *callable*. *callable* must be a callable object and must not be `NULL`.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to a new class method descriptor. On failure, this function returns `NULL` with an exception set.

> The type of static method objects. This is the same object as `staticmethod`{.interpreted-text role="class"} in the Python layer.

> Create a new `staticmethod`{.interpreted-text role="class"} object wrapping *callable*. *callable* must be a callable object and must not be `NULL`.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to a new static method descriptor. On failure, this function returns `NULL` with an exception set.
