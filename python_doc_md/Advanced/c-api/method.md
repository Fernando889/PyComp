# Instance Method Objects {#instancemethod-objects}

::: index
pair: object; instancemethod
:::

An instance method is a wrapper for a `PyCFunction`{.interpreted-text role="c:type"} and the new way to bind a `PyCFunction`{.interpreted-text role="c:type"} to a class object. It replaces the former call `PyMethod_New(func, NULL, class)`.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python instance method type. It is not exposed to Python programs.

> Return true if *o* is an instance method object (has type `PyInstanceMethod_Type`{.interpreted-text role="c:data"}). The parameter must not be `NULL`. This function always succeeds.

> Return a new instance method object, with *func* being any callable object. *func* is the function that will be called when the instance method is called.

> Return the function object associated with the instance method *im*.

> Macro version of `PyInstanceMethod_Function`{.interpreted-text role="c:func"} which avoids error checking.

# Method Objects

::: index
pair: object; method
:::

Methods are bound function objects. Methods are always bound to an instance of a user-defined class. Unbound methods (methods bound to a class object) are no longer available.

> ::: index
> single: MethodType (in module types)
> :::
>
> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python method type. This is exposed to Python programs as `types.MethodType`.

> Return true if *o* is a method object (has type `PyMethod_Type`{.interpreted-text role="c:data"}). The parameter must not be `NULL`. This function always succeeds.

> Return a new method object, with *func* being any callable object and *self* the instance the method should be bound. *func* is the function that will be called when the method is called. *self* must not be `NULL`.

> Return the function object associated with the method *meth*.

> Macro version of `PyMethod_Function`{.interpreted-text role="c:func"} which avoids error checking.

> Return the instance associated with the method *meth*.

> Macro version of `PyMethod_Self`{.interpreted-text role="c:func"} which avoids error checking.
