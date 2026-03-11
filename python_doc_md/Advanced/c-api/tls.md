# Thread-local storage support {#thread-local-storage}

The Python interpreter provides low-level support for thread-local storage (TLS) which wraps the underlying native TLS implementation to support the Python-level thread-local storage API (`threading.local`{.interpreted-text role="class"}). The CPython C level APIs are similar to those offered by pthreads and Windows: use a thread key and functions to associate a `void*`{.interpreted-text role="c:expr"} value per thread.

A `thread state`{.interpreted-text role="term"} does *not* need to be `attached <attached thread state>`{.interpreted-text role="term"} when calling these functions; they supply their own locking.

Note that `Python.h`{.interpreted-text role="file"} does not include the declaration of the TLS APIs, you need to include `pythread.h`{.interpreted-text role="file"} to use thread-local storage.

:::: note
::: title
Note
:::

None of these API functions handle memory management on behalf of the `void*`{.interpreted-text role="c:expr"} values. You need to allocate and deallocate them yourself. If the `void*`{.interpreted-text role="c:expr"} values happen to be `PyObject*`{.interpreted-text role="c:expr"}, these functions don\'t do refcount operations on them either.
::::

## Thread-specific storage API

The thread-specific storage (TSS) API was introduced to supersede the use of the existing TLS API within the CPython interpreter. This API uses a new type `Py_tss_t`{.interpreted-text role="c:type"} instead of `int`{.interpreted-text role="c:expr"} to represent thread keys.

::: versionadded
3.7
:::

::: seealso
\"A New C-API for Thread-Local Storage in CPython\" (`539`{.interpreted-text role="pep"})
:::

> This data structure represents the state of a thread key, the definition of which may depend on the underlying TLS implementation, and it has an internal field representing the key\'s initialization state. There are no public members in this structure.
>
> When `Py_LIMITED_API <stable>`{.interpreted-text role="ref"} is not defined, static allocation of this type by `Py_tss_NEEDS_INIT`{.interpreted-text role="c:macro"} is allowed.

> This macro expands to the initializer for `Py_tss_t`{.interpreted-text role="c:type"} variables. Note that this macro won\'t be defined with `Py_LIMITED_API <stable>`{.interpreted-text role="ref"}.

## Dynamic allocation

Dynamic allocation of the `Py_tss_t`{.interpreted-text role="c:type"}, required in extension modules built with `Py_LIMITED_API <stable>`{.interpreted-text role="ref"}, where static allocation of this type is not possible due to its implementation being opaque at build time.

> Return a value which is the same state as a value initialized with `Py_tss_NEEDS_INIT`{.interpreted-text role="c:macro"}, or `NULL` in the case of dynamic allocation failure.

> Free the given *key* allocated by `PyThread_tss_alloc`{.interpreted-text role="c:func"}, after first calling `PyThread_tss_delete`{.interpreted-text role="c:func"} to ensure any associated thread locals have been unassigned. This is a no-op if the *key* argument is `NULL`.
>
> :::: note
> ::: title
> Note
> :::
>
> A freed key becomes a dangling pointer. You should reset the key to `NULL`.
> ::::

## Methods

The parameter *key* of these functions must not be `NULL`. Moreover, the behaviors of `PyThread_tss_set`{.interpreted-text role="c:func"} and `PyThread_tss_get`{.interpreted-text role="c:func"} are undefined if the given `Py_tss_t`{.interpreted-text role="c:type"} has not been initialized by `PyThread_tss_create`{.interpreted-text role="c:func"}.

> Return a non-zero value if the given `Py_tss_t`{.interpreted-text role="c:type"} has been initialized by `PyThread_tss_create`{.interpreted-text role="c:func"}.

> Return a zero value on successful initialization of a TSS key. The behavior is undefined if the value pointed to by the *key* argument is not initialized by `Py_tss_NEEDS_INIT`{.interpreted-text role="c:macro"}. This function can be called repeatedly on the same key \-- calling it on an already initialized key is a no-op and immediately returns success.

> Destroy a TSS key to forget the values associated with the key across all threads, and change the key\'s initialization state to uninitialized. A destroyed key is able to be initialized again by `PyThread_tss_create`{.interpreted-text role="c:func"}. This function can be called repeatedly on the same key \-- calling it on an already destroyed key is a no-op.

> Return a zero value to indicate successfully associating a `void*`{.interpreted-text role="c:expr"} value with a TSS key in the current thread. Each thread has a distinct mapping of the key to a `void*`{.interpreted-text role="c:expr"} value.

> Return the `void*`{.interpreted-text role="c:expr"} value associated with a TSS key in the current thread. This returns `NULL` if no value is associated with the key in the current thread.

## Legacy APIs {#thread-local-storage-api}

::: deprecated
3.7 This API is superseded by the `thread-specific storage (TSS) API <thread-specific-storage-api>`{.interpreted-text role="ref"}.
:::

:::: note
::: title
Note
:::

This version of the API does not support platforms where the native TLS key is defined in a way that cannot be safely cast to `int`. On such platforms, `PyThread_create_key`{.interpreted-text role="c:func"} will return immediately with a failure status, and the other TLS functions will all be no-ops on such platforms.
::::

Due to the compatibility problem noted above, this version of the API should not be used in new code.
