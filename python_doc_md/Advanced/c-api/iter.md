# Iterator Protocol {#iterator}

There are two functions specifically for working with iterators.

> Return non-zero if the object *o* can be safely passed to `PyIter_NextItem`{.interpreted-text role="c:func"} and `0` otherwise. This function always succeeds.

> Return non-zero if the object *o* provides the `AsyncIterator`{.interpreted-text role="class"} protocol, and `0` otherwise. This function always succeeds.
>
> ::: versionadded
> 3.10
> :::

> Return `1` and set *item* to a `strong reference`{.interpreted-text role="term"} of the next value of the iterator *iter* on success. Return `0` and set *item* to `NULL` if there are no remaining values. Return `-1`, set *item* to `NULL` and set an exception on error.
>
> ::: versionadded
> 3.14
> :::

> This is an older version of `!PyIter_NextItem`{.interpreted-text role="c:func"}, which is retained for backwards compatibility. Prefer `PyIter_NextItem`{.interpreted-text role="c:func"}.
>
> Return the next value from the iterator *o*. The object must be an iterator according to `PyIter_Check`{.interpreted-text role="c:func"} (it is up to the caller to check this). If there are no remaining values, returns `NULL` with no exception set. If an error occurs while retrieving the item, returns `NULL` and passes along the exception.

> The enum value used to represent different results of `PyIter_Send`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.10
> :::

> Sends the *arg* value into the iterator *iter*. Returns:
>
> - `PYGEN_RETURN` if iterator returns. Return value is returned via *presult*.
> - `PYGEN_NEXT` if iterator yields. Yielded value is returned via *presult*.
> - `PYGEN_ERROR` if iterator has raised an exception. *presult* is set to `NULL`.
>
> ::: versionadded
> 3.10
> :::
