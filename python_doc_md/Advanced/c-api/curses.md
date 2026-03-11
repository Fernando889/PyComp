# Curses C API

`curses`{.interpreted-text role="mod"} exposes a small C interface for extension modules. Consumers must include the header file `py_curses.h`{.interpreted-text role="file"} (which is not included by default by `Python.h`{.interpreted-text role="file"}) and `import_curses`{.interpreted-text role="c:func"} must be invoked, usually as part of the module initialisation function, to populate `PyCurses_API`{.interpreted-text role="c:var"}.

:::: warning
::: title
Warning
:::

Neither the C API nor the pure Python `curses`{.interpreted-text role="mod"} module are compatible with subinterpreters.
::::

> Import the curses C API. The macro does not need a semi-colon to be called.
>
> On success, populate the `PyCurses_API`{.interpreted-text role="c:var"} pointer.
>
> On failure, set `PyCurses_API`{.interpreted-text role="c:var"} to NULL and set an exception. The caller must check if an error occurred via `PyErr_Occurred`{.interpreted-text role="c:func"}:
>
> ``` 
> import_curses();  // semi-colon is optional but recommended
> if (PyErr_Occurred()) { /* cleanup */ }
> ```

> Dynamically allocated object containing the curses C API. This variable is only available once `import_curses`{.interpreted-text role="c:macro"} succeeds.
>
> `PyCurses_API[0]` corresponds to `PyCursesWindow_Type`{.interpreted-text role="c:data"}.
>
> `PyCurses_API[1]`, `PyCurses_API[2]`, and `PyCurses_API[3]` are pointers to predicate functions of type `int (*)(void)`.
>
> When called, these predicates return whether `curses.setupterm`{.interpreted-text role="func"}, `curses.initscr`{.interpreted-text role="func"}, and `curses.start_color`{.interpreted-text role="func"} have been called respectively.
>
> See also the convenience macros `PyCursesSetupTermCalled`{.interpreted-text role="c:macro"}, `PyCursesInitialised`{.interpreted-text role="c:macro"}, and `PyCursesInitialisedColor`{.interpreted-text role="c:macro"}.
>
> :::: note
> ::: title
> Note
> :::
>
> The number of entries in this structure is subject to changes. Consider using `PyCurses_API_pointers`{.interpreted-text role="c:macro"} to check if new fields are available or not.
> ::::

> The number of accessible fields (`4`) in `PyCurses_API`{.interpreted-text role="c:var"}. This number is incremented whenever new fields are added.

> The `heap type <heap-types>`{.interpreted-text role="ref"} corresponding to `curses.window`{.interpreted-text role="class"}.

> Return true if *op* is a `curses.window`{.interpreted-text role="class"} instance, false otherwise.

The following macros are convenience macros expanding into C statements. In particular, they can only be used as `macro;` or `macro`, but not `macro()` or `macro();`.

> Macro checking if `curses.setupterm`{.interpreted-text role="func"} has been called.
>
> The macro expansion is roughly equivalent to:
>
> ``` 
> {
>     typedef int (*predicate_t)(void);
>     predicate_t was_setupterm_called = (predicate_t)PyCurses_API[1];
>     if (!was_setupterm_called()) {
>         return NULL;
>     }
> }
> ```

> Macro checking if `curses.initscr`{.interpreted-text role="func"} has been called.
>
> The macro expansion is roughly equivalent to:
>
> ``` 
> {
>     typedef int (*predicate_t)(void);
>     predicate_t was_initscr_called = (predicate_t)PyCurses_API[2];
>     if (!was_initscr_called()) {
>         return NULL;
>     }
> }
> ```

> Macro checking if `curses.start_color`{.interpreted-text role="func"} has been called.
>
> The macro expansion is roughly equivalent to:
>
> ``` 
> {
>     typedef int (*predicate_t)(void);
>     predicate_t was_start_color_called = (predicate_t)PyCurses_API[3];
>     if (!was_start_color_called()) {
>         return NULL;
>     }
> }
> ```

# Internal data

The following objects are exposed by the C API but should be considered internal-only.

> Name of the curses capsule to pass to `PyCapsule_Import`{.interpreted-text role="c:func"}.
>
> Internal usage only. Use `import_curses`{.interpreted-text role="c:macro"} instead.
