# Coroutine Objects {#coro-objects}

::: versionadded
3.5
:::

Coroutine objects are what functions declared with an `async` keyword return.

> The C structure used for coroutine objects.

> The type object corresponding to coroutine objects.

> Return true if *ob*\'s type is `PyCoro_Type`{.interpreted-text role="c:type"}; *ob* must not be `NULL`. This function always succeeds.

> Create and return a new coroutine object based on the *frame* object, with `__name__` and `__qualname__` set to *name* and *qualname*. A reference to *frame* is stolen by this function. The *frame* argument must not be `NULL`.
