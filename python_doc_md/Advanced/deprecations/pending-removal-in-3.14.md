# Pending removal in Python 3.14

- `argparse`{.interpreted-text role="mod"}: The *type*, *choices*, and *metavar* parameters of `!argparse.BooleanOptionalAction`{.interpreted-text role="class"} are deprecated and will be removed in 3.14. (Contributed by Nikita Sobolev in `92248`{.interpreted-text role="gh"}.)

- `ast`{.interpreted-text role="mod"}: The following features have been deprecated in documentation since Python 3.8, now cause a `DeprecationWarning`{.interpreted-text role="exc"} to be emitted at runtime when they are accessed or used, and will be removed in Python 3.14:

  - `!ast.Num`{.interpreted-text role="class"}
  - `!ast.Str`{.interpreted-text role="class"}
  - `!ast.Bytes`{.interpreted-text role="class"}
  - `!ast.NameConstant`{.interpreted-text role="class"}
  - `!ast.Ellipsis`{.interpreted-text role="class"}

  Use `ast.Constant`{.interpreted-text role="class"} instead. (Contributed by Serhiy Storchaka in `90953`{.interpreted-text role="gh"}.)

- `asyncio`{.interpreted-text role="mod"}:

  - The child watcher classes `!asyncio.MultiLoopChildWatcher`{.interpreted-text role="class"}, `!asyncio.FastChildWatcher`{.interpreted-text role="class"}, `!asyncio.AbstractChildWatcher`{.interpreted-text role="class"} and `!asyncio.SafeChildWatcher`{.interpreted-text role="class"} are deprecated and will be removed in Python 3.14. (Contributed by Kumar Aditya in `94597`{.interpreted-text role="gh"}.)
  - `!asyncio.set_child_watcher`{.interpreted-text role="func"}, `!asyncio.get_child_watcher`{.interpreted-text role="func"}, `!asyncio.AbstractEventLoopPolicy.set_child_watcher`{.interpreted-text role="meth"} and `!asyncio.AbstractEventLoopPolicy.get_child_watcher`{.interpreted-text role="meth"} are deprecated and will be removed in Python 3.14. (Contributed by Kumar Aditya in `94597`{.interpreted-text role="gh"}.)
  - The `~asyncio.get_event_loop`{.interpreted-text role="meth"} method of the default event loop policy now emits a `DeprecationWarning`{.interpreted-text role="exc"} if there is no current event loop set and it decides to create one. (Contributed by Serhiy Storchaka and Guido van Rossum in `100160`{.interpreted-text role="gh"}.)

- `email`{.interpreted-text role="mod"}: Deprecated the *isdst* parameter in `email.utils.localtime`{.interpreted-text role="func"}. (Contributed by Alan Williams in `72346`{.interpreted-text role="gh"}.)

- `importlib.abc`{.interpreted-text role="mod"} deprecated classes:

  - `!importlib.abc.ResourceReader`{.interpreted-text role="class"}
  - `!importlib.abc.Traversable`{.interpreted-text role="class"}
  - `!importlib.abc.TraversableResources`{.interpreted-text role="class"}

  Use `importlib.resources.abc`{.interpreted-text role="mod"} classes instead:

  - `importlib.resources.abc.Traversable`{.interpreted-text role="class"}
  - `importlib.resources.abc.TraversableResources`{.interpreted-text role="class"}

  (Contributed by Jason R. Coombs and Hugo van Kemenade in `93963`{.interpreted-text role="gh"}.)

- `itertools`{.interpreted-text role="mod"} had undocumented, inefficient, historically buggy, and inconsistent support for copy, deepcopy, and pickle operations. This will be removed in 3.14 for a significant reduction in code volume and maintenance burden. (Contributed by Raymond Hettinger in `101588`{.interpreted-text role="gh"}.)

- `multiprocessing`{.interpreted-text role="mod"}: The default start method will change to a safer one on Linux, BSDs, and other non-macOS POSIX platforms where `'fork'` is currently the default (`84559`{.interpreted-text role="gh"}). Adding a runtime warning about this was deemed too disruptive as the majority of code is not expected to care. Use the `~multiprocessing.get_context`{.interpreted-text role="func"} or `~multiprocessing.set_start_method`{.interpreted-text role="func"} APIs to explicitly specify when your code *requires* `'fork'`. See `multiprocessing-start-methods`{.interpreted-text role="ref"}.

- `pathlib`{.interpreted-text role="mod"}: `~pathlib.PurePath.is_relative_to`{.interpreted-text role="meth"} and `~pathlib.PurePath.relative_to`{.interpreted-text role="meth"}: passing additional arguments is deprecated.

- `pkgutil`{.interpreted-text role="mod"}: `!pkgutil.find_loader`{.interpreted-text role="func"} and `!pkgutil.get_loader`{.interpreted-text role="func"} now raise `DeprecationWarning`{.interpreted-text role="exc"}; use `importlib.util.find_spec`{.interpreted-text role="func"} instead. (Contributed by Nikita Sobolev in `97850`{.interpreted-text role="gh"}.)

- `pty`{.interpreted-text role="mod"}:

  - `master_open()`: use `pty.openpty`{.interpreted-text role="func"}.
  - `slave_open()`: use `pty.openpty`{.interpreted-text role="func"}.

- `sqlite3`{.interpreted-text role="mod"}:

  - `!version`{.interpreted-text role="data"} and `!version_info`{.interpreted-text role="data"}.
  - `~sqlite3.Cursor.execute`{.interpreted-text role="meth"} and `~sqlite3.Cursor.executemany`{.interpreted-text role="meth"} if `named placeholders <sqlite3-placeholders>`{.interpreted-text role="ref"} are used and *parameters* is a sequence instead of a `dict`{.interpreted-text role="class"}.

- `urllib`{.interpreted-text role="mod"}: `!urllib.parse.Quoter`{.interpreted-text role="class"} is deprecated: it was not intended to be a public API. (Contributed by Gregory P. Smith in `88168`{.interpreted-text role="gh"}.)
