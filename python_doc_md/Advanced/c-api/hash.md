# PyHash API

See also the `PyTypeObject.tp_hash`{.interpreted-text role="c:member"} member and `numeric-hash`{.interpreted-text role="ref"}.

> Hash value type: signed integer.
>
> ::: versionadded
> 3.2
> :::

> Hash value type: unsigned integer.
>
> ::: versionadded
> 3.2
> :::

> A numerical value indicating the algorithm for hashing of `str`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"}, and `memoryview`{.interpreted-text role="class"}.
>
> The algorithm name is exposed by `sys.hash_info.algorithm`{.interpreted-text role="data"}.
>
> ::: versionadded
> 3.4
> :::

> Buffers of length in range `[1, Py_HASH_CUTOFF)` are hashed using DJBX33A instead of the algorithm described by `Py_HASH_ALGORITHM`{.interpreted-text role="c:macro"}.
>
> - A `!Py_HASH_CUTOFF`{.interpreted-text role="c:macro"} of 0 disables the optimization.
> - `!Py_HASH_CUTOFF`{.interpreted-text role="c:macro"} must be non-negative and less or equal than 7.
>
> 32-bit platforms should use a cutoff smaller than 64-bit platforms because it is easier to create colliding strings. A cutoff of 7 on 64-bit platforms and 5 on 32-bit platforms should provide a decent safety margin.
>
> This corresponds to the `sys.hash_info.cutoff`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.4
> :::

> The [Mersenne prime](https://en.wikipedia.org/wiki/Mersenne_prime) `P = 2**n -1`, used for numeric hash scheme.
>
> This corresponds to the `sys.hash_info.modulus`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.13
> :::

> The exponent `n` of `P` in `PyHASH_MODULUS`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.13
> :::

> Prime multiplier used in string and various other hashes.
>
> ::: versionadded
> 3.13
> :::

> The hash value returned for a positive infinity.
>
> This corresponds to the `sys.hash_info.inf`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.13
> :::

> The multiplier used for the imaginary part of a complex number.
>
> This corresponds to the `sys.hash_info.imag`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.13
> :::

> Hash function definition used by `PyHash_GetFuncDef`{.interpreted-text role="c:func"}.
>
> > Hash function.
>
> > Hash function name (UTF-8 encoded string).
> >
> > This corresponds to the `sys.hash_info.algorithm`{.interpreted-text role="data"} constant.
>
> > Internal size of the hash value in bits.
> >
> > This corresponds to the `sys.hash_info.hash_bits`{.interpreted-text role="data"} constant.
>
> > Size of seed input in bits.
> >
> > This corresponds to the `sys.hash_info.seed_bits`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.4
> :::

> Get the hash function definition.
>
> ::: seealso
> `456`{.interpreted-text role="pep"} \"Secure and interchangeable hash algorithm\".
> :::
>
> ::: versionadded
> 3.4
> :::

> Hash a pointer value: process the pointer value as an integer (cast it to `uintptr_t` internally). The pointer is not dereferenced.
>
> The function cannot fail: it cannot return `-1`.
>
> ::: versionadded
> 3.13
> :::

> Compute and return the hash value of a buffer of *len* bytes starting at address *ptr*. The hash is guaranteed to match that of `bytes`{.interpreted-text role="class"}, `memoryview`{.interpreted-text role="class"}, and other built-in objects that implement the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}.
>
> Use this function to implement hashing for immutable objects whose `~PyTypeObject.tp_richcompare`{.interpreted-text role="c:member"} function compares to another object\'s buffer.
>
> *len* must be greater than or equal to `0`.
>
> This function always succeeds.
>
> ::: versionadded
> 3.14
> :::

> Generic hashing function that is meant to be put into a type object\'s `tp_hash` slot. Its result only depends on the object\'s identity.
>
> ::: impl-detail
> In CPython, it is equivalent to `Py_HashPointer`{.interpreted-text role="c:func"}.
> :::
>
> ::: versionadded
> 3.13
> :::
