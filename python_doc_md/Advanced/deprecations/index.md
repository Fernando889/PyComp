# Deprecations

## Pending removal in Python 3.15

- The import system:
  - Setting `__cached__` on a module while failing to set `__spec__.cached <importlib.machinery.ModuleSpec.cached>`{.interpreted-text role="attr"} is deprecated. In Python 3.15, `__cached__` will cease to be set or take into consideration by the import system or standard library. (`97879`{.interpreted-text role="gh"})
  - Setting `~module.__package__`{.interpreted-text role="attr"} on a module while failing to set `__spec__.parent <importlib.machinery.ModuleSpec.parent>`{.interpreted-text role="attr"} is deprecated. In Python 3.15, `!__package__`{.interpreted-text role="attr"} will cease to be set or take into consideration by the import system or standard library. (`97879`{.interpreted-text role="gh"})
- `ctypes`{.interpreted-text role="mod"}:
  - The undocumented `!ctypes.SetPointerType`{.interpreted-text role="func"} function has been deprecated since Python 3.13.
- `http.server`{.interpreted-text role="mod"}:
  - The obsolete and rarely used `!CGIHTTPRequestHandler`{.interpreted-text role="class"} has been deprecated since Python 3.13. No direct replacement exists. *Anything* is better than CGI to interface a web server with a request handler.
  - The `!--cgi`{.interpreted-text role="option"} flag to the `python -m http.server`{.interpreted-text role="program"} command-line interface has been deprecated since Python 3.13.
- `importlib`{.interpreted-text role="mod"}:
  - `load_module()` method: use `exec_module()` instead.
- `pathlib`{.interpreted-text role="mod"}:
  - `!.PurePath.is_reserved`{.interpreted-text role="meth"} has been deprecated since Python 3.13. Use `os.path.isreserved`{.interpreted-text role="func"} to detect reserved paths on Windows.
- `platform`{.interpreted-text role="mod"}:
  - `!platform.java_ver`{.interpreted-text role="func"} has been deprecated since Python 3.13. This function is only useful for Jython support, has a confusing API, and is largely untested.
- `sysconfig`{.interpreted-text role="mod"}:
  - The *check_home* argument of `sysconfig.is_python_build`{.interpreted-text role="func"} has been deprecated since Python 3.12.
- `threading`{.interpreted-text role="mod"}:
  - `~threading.RLock`{.interpreted-text role="func"} will take no arguments in Python 3.15. Passing any arguments has been deprecated since Python 3.14, as the Python version does not permit any arguments, but the C version allows any number of positional or keyword arguments, ignoring every argument.
- `types`{.interpreted-text role="mod"}:
  - `types.CodeType`{.interpreted-text role="class"}: Accessing `~codeobject.co_lnotab`{.interpreted-text role="attr"} was deprecated in `626`{.interpreted-text role="pep"} since 3.10 and was planned to be removed in 3.12, but it only got a proper `DeprecationWarning`{.interpreted-text role="exc"} in 3.12. May be removed in 3.15. (Contributed by Nikita Sobolev in `101866`{.interpreted-text role="gh"}.)
- `typing`{.interpreted-text role="mod"}:
  - The undocumented keyword argument syntax for creating `~typing.NamedTuple`{.interpreted-text role="class"} classes (for example, `Point = NamedTuple("Point", x=int, y=int)`) has been deprecated since Python 3.13. Use the class-based syntax or the functional syntax instead.
  - When using the functional syntax of `~typing.TypedDict`{.interpreted-text role="class"}s, failing to pass a value to the *fields* parameter (`TD = TypedDict("TD")`) or passing `None` (`TD = TypedDict("TD", None)`) has been deprecated since Python 3.13. Use `class TD(TypedDict): pass` or `TD = TypedDict("TD", {})` to create a TypedDict with zero field.
  - The `!typing.no_type_check_decorator`{.interpreted-text role="func"} decorator function has been deprecated since Python 3.13. After eight years in the `typing`{.interpreted-text role="mod"} module, it has yet to be supported by any major type checker.
- `!sre_compile`{.interpreted-text role="mod"}, `!sre_constants`{.interpreted-text role="mod"} and `!sre_parse`{.interpreted-text role="mod"} modules.
- `wave`{.interpreted-text role="mod"}:
  - The `getmark()`, `setmark()` and `getmarkers()` methods of the `~wave.Wave_read`{.interpreted-text role="class"} and `~wave.Wave_write`{.interpreted-text role="class"} classes have been deprecated since Python 3.13.
- `zipimport`{.interpreted-text role="mod"}:
  - `!zipimport.zipimporter.load_module`{.interpreted-text role="meth"} has been deprecated since Python 3.10. Use `~zipimport.zipimporter.exec_module`{.interpreted-text role="meth"} instead. (`125746`{.interpreted-text role="gh"}.)

## Pending removal in Python 3.16

- The import system:
  - Setting `~module.__loader__`{.interpreted-text role="attr"} on a module while failing to set `__spec__.loader <importlib.machinery.ModuleSpec.loader>`{.interpreted-text role="attr"} is deprecated. In Python 3.16, `!__loader__`{.interpreted-text role="attr"} will cease to be set or taken into consideration by the import system or the standard library.
- `array`{.interpreted-text role="mod"}:
  - The `'u'` format code (`wchar_t`{.interpreted-text role="c:type"}) has been deprecated in documentation since Python 3.3 and at runtime since Python 3.13. Use the `'w'` format code (`Py_UCS4`{.interpreted-text role="c:type"}) for Unicode characters instead.
- `asyncio`{.interpreted-text role="mod"}:
  - `!asyncio.iscoroutinefunction`{.interpreted-text role="func"} is deprecated and will be removed in Python 3.16; use `inspect.iscoroutinefunction`{.interpreted-text role="func"} instead. (Contributed by Jiahao Li and Kumar Aditya in `122875`{.interpreted-text role="gh"}.)

  - `asyncio`{.interpreted-text role="mod"} policy system is deprecated and will be removed in Python 3.16. In particular, the following classes and functions are deprecated:

    - `asyncio.AbstractEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.DefaultEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.WindowsSelectorEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.WindowsProactorEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.get_event_loop_policy`{.interpreted-text role="func"}
    - `asyncio.set_event_loop_policy`{.interpreted-text role="func"}

    Users should use `asyncio.run`{.interpreted-text role="func"} or `asyncio.Runner`{.interpreted-text role="class"} with *loop_factory* to use the desired event loop implementation.

    For example, to use `asyncio.SelectorEventLoop`{.interpreted-text role="class"} on Windows:

        import asyncio

        async def main():
            ...

        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)

    (Contributed by Kumar Aditya in `127949`{.interpreted-text role="gh"}.)
- `builtins`{.interpreted-text role="mod"}:
  - Bitwise inversion on boolean types, `~True` or `~False` has been deprecated since Python 3.12, as it produces surprising and unintuitive results (`-2` and `-1`). Use `not x` instead for the logical negation of a Boolean. In the rare case that you need the bitwise inversion of the underlying integer, convert to `int` explicitly (`~int(x)`).
- `functools`{.interpreted-text role="mod"}:
  - Calling the Python implementation of `functools.reduce`{.interpreted-text role="func"} with *function* or *sequence* as keyword arguments has been deprecated since Python 3.14.
- `logging`{.interpreted-text role="mod"}:
  - Support for custom logging handlers with the *strm* argument is deprecated and scheduled for removal in Python 3.16. Define handlers with the *stream* argument instead. (Contributed by Mariusz Felisiak in `115032`{.interpreted-text role="gh"}.)
- `mimetypes`{.interpreted-text role="mod"}:
  - Valid extensions start with a \'.\' or are empty for `mimetypes.MimeTypes.add_type`{.interpreted-text role="meth"}. Undotted extensions are deprecated and will raise a `ValueError`{.interpreted-text role="exc"} in Python 3.16. (Contributed by Hugo van Kemenade in `75223`{.interpreted-text role="gh"}.)
- `shutil`{.interpreted-text role="mod"}:
  - The `!ExecError`{.interpreted-text role="class"} exception has been deprecated since Python 3.14. It has not been used by any function in `!shutil`{.interpreted-text role="mod"} since Python 3.4, and is now an alias of `RuntimeError`{.interpreted-text role="exc"}.
- `symtable`{.interpreted-text role="mod"}:
  - The `Class.get_methods <symtable.Class.get_methods>`{.interpreted-text role="meth"} method has been deprecated since Python 3.14.
- `sys`{.interpreted-text role="mod"}:
  - The `~sys._enablelegacywindowsfsencoding`{.interpreted-text role="func"} function has been deprecated since Python 3.13. Use the `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} environment variable instead.
- `sysconfig`{.interpreted-text role="mod"}:
  - The `!sysconfig.expand_makefile_vars`{.interpreted-text role="func"} function has been deprecated since Python 3.14. Use the `vars` argument of `sysconfig.get_paths`{.interpreted-text role="func"} instead.
- `tarfile`{.interpreted-text role="mod"}:
  - The undocumented and unused `!TarFile.tarfile`{.interpreted-text role="attr"} attribute has been deprecated since Python 3.13.

## Pending removal in Python 3.17

- `collections.abc`{.interpreted-text role="mod"}:
  - `collections.abc.ByteString`{.interpreted-text role="class"} is scheduled for removal in Python 3.17.

    Use `isinstance(obj, collections.abc.Buffer)` to test if `obj` implements the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"} at runtime. For use in type annotations, either use `~collections.abc.Buffer`{.interpreted-text role="class"} or a union that explicitly specifies the types your code supports (e.g., `bytes | bytearray | memoryview`).

    `!ByteString`{.interpreted-text role="class"} was originally intended to be an abstract class that would serve as a supertype of both `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"}. However, since the ABC never had any methods, knowing that an object was an instance of `!ByteString`{.interpreted-text role="class"} never actually told you anything useful about the object. Other common buffer types such as `memoryview`{.interpreted-text role="class"} were also never understood as subtypes of `!ByteString`{.interpreted-text role="class"} (either at runtime or by static type checkers).

    See `PEP 688 <688#current-options>`{.interpreted-text role="pep"} for more details. (Contributed by Shantanu Jain in `91896`{.interpreted-text role="gh"}.)
- `encodings`{.interpreted-text role="mod"}:
  - Passing non-ascii *encoding* names to `encodings.normalize_encoding`{.interpreted-text role="func"} is deprecated and scheduled for removal in Python 3.17. (Contributed by Stan Ulbrych in `136702`{.interpreted-text role="gh"})
- `typing`{.interpreted-text role="mod"}:
  - Before Python 3.14, old-style unions were implemented using the private class `typing._UnionGenericAlias`. This class is no longer needed for the implementation, but it has been retained for backward compatibility, with removal scheduled for Python 3.17. Users should use documented introspection helpers like `typing.get_origin`{.interpreted-text role="func"} and `typing.get_args`{.interpreted-text role="func"} instead of relying on private implementation details.

  - `typing.ByteString`{.interpreted-text role="class"}, deprecated since Python 3.9, is scheduled for removal in Python 3.17.

    Use `isinstance(obj, collections.abc.Buffer)` to test if `obj` implements the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"} at runtime. For use in type annotations, either use `~collections.abc.Buffer`{.interpreted-text role="class"} or a union that explicitly specifies the types your code supports (e.g., `bytes | bytearray | memoryview`).

    `!ByteString`{.interpreted-text role="class"} was originally intended to be an abstract class that would serve as a supertype of both `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"}. However, since the ABC never had any methods, knowing that an object was an instance of `!ByteString`{.interpreted-text role="class"} never actually told you anything useful about the object. Other common buffer types such as `memoryview`{.interpreted-text role="class"} were also never understood as subtypes of `!ByteString`{.interpreted-text role="class"} (either at runtime or by static type checkers).

    See `PEP 688 <688#current-options>`{.interpreted-text role="pep"} for more details. (Contributed by Shantanu Jain in `91896`{.interpreted-text role="gh"}.)

## Pending removal in Python 3.18

- `decimal`{.interpreted-text role="mod"}:
  - The non-standard and undocumented `~decimal.Decimal`{.interpreted-text role="class"} format specifier `'N'`, which is only supported in the `!decimal`{.interpreted-text role="mod"} module\'s C implementation, has been deprecated since Python 3.13. (Contributed by Serhiy Storchaka in `89902`{.interpreted-text role="gh"}.)

## Pending removal in Python 3.19

- `ctypes`{.interpreted-text role="mod"}:
  - Implicitly switching to the MSVC-compatible struct layout by setting `~ctypes.Structure._pack_`{.interpreted-text role="attr"} but not `~ctypes.Structure._layout_`{.interpreted-text role="attr"} on non-Windows platforms.
- `hashlib`{.interpreted-text role="mod"}:
  - In hash function constructors such as `~hashlib.new`{.interpreted-text role="func"} or the direct hash-named constructors such as `~hashlib.md5`{.interpreted-text role="func"} and `~hashlib.sha256`{.interpreted-text role="func"}, their optional initial data parameter could also be passed a keyword argument named `data=` or `string=` in various `!hashlib`{.interpreted-text role="mod"} implementations.

    Support for the `string` keyword argument name is now deprecated and slated for removal in Python 3.19.

    Before Python 3.13, the `string` keyword parameter was not correctly supported depending on the backend implementation of hash functions. Prefer passing the initial data as a positional argument for maximum backwards compatibility.

## Pending removal in Python 3.20

- The `__version__`, `version` and `VERSION` attributes have been deprecated in these standard library modules and will be removed in Python 3.20. Use `sys.version_info`{.interpreted-text role="py:data"} instead.

  - `argparse`{.interpreted-text role="mod"}
  - `csv`{.interpreted-text role="mod"}
  - `ctypes`{.interpreted-text role="mod"}
  - `!ctypes.macholib`{.interpreted-text role="mod"}
  - `decimal`{.interpreted-text role="mod"} (use `decimal.SPEC_VERSION`{.interpreted-text role="data"} instead)
  - `http.server`{.interpreted-text role="mod"}
  - `imaplib`{.interpreted-text role="mod"}
  - `ipaddress`{.interpreted-text role="mod"}
  - `json`{.interpreted-text role="mod"}
  - `logging`{.interpreted-text role="mod"} (`__date__` also deprecated)
  - `optparse`{.interpreted-text role="mod"}
  - `pickle`{.interpreted-text role="mod"}
  - `platform`{.interpreted-text role="mod"}
  - `re`{.interpreted-text role="mod"}
  - `socketserver`{.interpreted-text role="mod"}
  - `tabnanny`{.interpreted-text role="mod"}
  - `tkinter.font`{.interpreted-text role="mod"}
  - `tkinter.ttk`{.interpreted-text role="mod"}
  - `wsgiref.simple_server`{.interpreted-text role="mod"}
  - `xml.etree.ElementTree`{.interpreted-text role="mod"}
  - `!xml.sax.expatreader`{.interpreted-text role="mod"}
  - `xml.sax.handler`{.interpreted-text role="mod"}
  - `zlib`{.interpreted-text role="mod"}

  (Contributed by Hugo van Kemenade and Stan Ulbrych in `76007`{.interpreted-text role="gh"}.)

## Pending removal in future versions

The following APIs will be removed in the future, although there is currently no date scheduled for their removal.

- `argparse`{.interpreted-text role="mod"}:
  - Nesting argument groups and nesting mutually exclusive groups are deprecated.
  - Passing the undocumented keyword argument *prefix_chars* to `~argparse.ArgumentParser.add_argument_group`{.interpreted-text role="meth"} is now deprecated.
  - The `argparse.FileType`{.interpreted-text role="class"} type converter is deprecated.
- `builtins`{.interpreted-text role="mod"}:
  - Generators: `throw(type, exc, tb)` and `athrow(type, exc, tb)` signature is deprecated: use `throw(exc)` and `athrow(exc)` instead, the single argument signature.
  - Currently Python accepts numeric literals immediately followed by keywords, for example `0in x`, `1or x`, `0if 1else 2`. It allows confusing and ambiguous expressions like `[0x1for x in y]` (which can be interpreted as `[0x1 for x in y]` or `[0x1f or x in y]`). A syntax warning is raised if the numeric literal is immediately followed by one of keywords `and`{.interpreted-text role="keyword"}, `else`{.interpreted-text role="keyword"}, `for`{.interpreted-text role="keyword"}, `if`{.interpreted-text role="keyword"}, `in`{.interpreted-text role="keyword"}, `is`{.interpreted-text role="keyword"} and `or`{.interpreted-text role="keyword"}. In a future release it will be changed to a syntax error. (`87999`{.interpreted-text role="gh"})
  - Support for `__index__()` and `__int__()` method returning non-int type: these methods will be required to return an instance of a strict subclass of `int`{.interpreted-text role="class"}.
  - Support for `__float__()` method returning a strict subclass of `float`{.interpreted-text role="class"}: these methods will be required to return an instance of `float`{.interpreted-text role="class"}.
  - Support for `__complex__()` method returning a strict subclass of `complex`{.interpreted-text role="class"}: these methods will be required to return an instance of `complex`{.interpreted-text role="class"}.
  - Passing a complex number as the *real* or *imag* argument in the `complex`{.interpreted-text role="func"} constructor is now deprecated; it should only be passed as a single positional argument. (Contributed by Serhiy Storchaka in `109218`{.interpreted-text role="gh"}.)
- `calendar`{.interpreted-text role="mod"}: `calendar.January` and `calendar.February` constants are deprecated and replaced by `calendar.JANUARY`{.interpreted-text role="data"} and `calendar.FEBRUARY`{.interpreted-text role="data"}. (Contributed by Prince Roshan in `103636`{.interpreted-text role="gh"}.)
- `codecs`{.interpreted-text role="mod"}: use `open`{.interpreted-text role="func"} instead of `codecs.open`{.interpreted-text role="func"}. (`133038`{.interpreted-text role="gh"})
- `codeobject.co_lnotab`{.interpreted-text role="attr"}: use the `codeobject.co_lines`{.interpreted-text role="meth"} method instead.
- `datetime`{.interpreted-text role="mod"}:
  - `~datetime.datetime.utcnow`{.interpreted-text role="meth"}: use `datetime.datetime.now(tz=datetime.UTC)`.
  - `~datetime.datetime.utcfromtimestamp`{.interpreted-text role="meth"}: use `datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)`.
- `gettext`{.interpreted-text role="mod"}: Plural value must be an integer.
- `importlib`{.interpreted-text role="mod"}:
  - `~importlib.util.cache_from_source`{.interpreted-text role="func"} *debug_override* parameter is deprecated: use the *optimization* parameter instead.
- `importlib.metadata`{.interpreted-text role="mod"}:
  - `EntryPoints` tuple interface.
  - Implicit `None` on return values.
- `logging`{.interpreted-text role="mod"}: the `warn()` method has been deprecated since Python 3.3, use `~logging.warning`{.interpreted-text role="meth"} instead.
- `mailbox`{.interpreted-text role="mod"}: Use of StringIO input and text mode is deprecated, use BytesIO and binary mode instead.
- `os`{.interpreted-text role="mod"}: Calling `os.register_at_fork`{.interpreted-text role="func"} in a multi-threaded process.
- `os.path`{.interpreted-text role="mod"}: `os.path.commonprefix`{.interpreted-text role="func"} is deprecated, use `os.path.commonpath`{.interpreted-text role="func"} for path prefixes. The `os.path.commonprefix`{.interpreted-text role="func"} function is being deprecated due to having a misleading name and module. The function is not safe to use for path prefixes despite being included in a module about path manipulation, meaning it is easy to accidentally introduce path traversal vulnerabilities into Python programs by using this function.
- `!pydoc.ErrorDuringImport`{.interpreted-text role="class"}: A tuple value for *exc_info* parameter is deprecated, use an exception instance.
- `re`{.interpreted-text role="mod"}: More strict rules are now applied for numerical group references and group names in regular expressions. Only sequence of ASCII digits is now accepted as a numerical reference. The group name in bytes patterns and replacement strings can now only contain ASCII letters and digits and underscore. (Contributed by Serhiy Storchaka in `91760`{.interpreted-text role="gh"}.)
- `shutil`{.interpreted-text role="mod"}: `~shutil.rmtree`{.interpreted-text role="func"}\'s *onerror* parameter is deprecated in Python 3.12; use the *onexc* parameter instead.
- `ssl`{.interpreted-text role="mod"} options and protocols:
  - `ssl.SSLContext`{.interpreted-text role="class"} without protocol argument is deprecated.
  - `ssl.SSLContext`{.interpreted-text role="class"}: `~ssl.SSLContext.set_npn_protocols`{.interpreted-text role="meth"} and `!selected_npn_protocol`{.interpreted-text role="meth"} are deprecated: use ALPN instead.
  - `ssl.OP_NO_SSL*` options
  - `ssl.OP_NO_TLS*` options
  - `ssl.PROTOCOL_SSLv3`
  - `ssl.PROTOCOL_TLS`
  - `ssl.PROTOCOL_TLSv1`
  - `ssl.PROTOCOL_TLSv1_1`
  - `ssl.PROTOCOL_TLSv1_2`
  - `ssl.TLSVersion.SSLv3`
  - `ssl.TLSVersion.TLSv1`
  - `ssl.TLSVersion.TLSv1_1`
- `threading`{.interpreted-text role="mod"} methods:
  - `!threading.Condition.notifyAll`{.interpreted-text role="meth"}: use `~threading.Condition.notify_all`{.interpreted-text role="meth"}.
  - `!threading.Event.isSet`{.interpreted-text role="meth"}: use `~threading.Event.is_set`{.interpreted-text role="meth"}.
  - `!threading.Thread.isDaemon`{.interpreted-text role="meth"}, `threading.Thread.setDaemon`{.interpreted-text role="meth"}: use `threading.Thread.daemon`{.interpreted-text role="attr"} attribute.
  - `!threading.Thread.getName`{.interpreted-text role="meth"}, `threading.Thread.setName`{.interpreted-text role="meth"}: use `threading.Thread.name`{.interpreted-text role="attr"} attribute.
  - `!threading.currentThread`{.interpreted-text role="meth"}: use `threading.current_thread`{.interpreted-text role="meth"}.
  - `!threading.activeCount`{.interpreted-text role="meth"}: use `threading.active_count`{.interpreted-text role="meth"}.
- `typing.Text`{.interpreted-text role="class"} (`92332`{.interpreted-text role="gh"}).
- The internal class `typing._UnionGenericAlias` is no longer used to implement `typing.Union`{.interpreted-text role="class"}. To preserve compatibility with users using this private class, a compatibility shim will be provided until at least Python 3.17. (Contributed by Jelle Zijlstra in `105499`{.interpreted-text role="gh"}.)
- `unittest.IsolatedAsyncioTestCase`{.interpreted-text role="class"}: it is deprecated to return a value that is not `None` from a test case.
- `urllib.parse`{.interpreted-text role="mod"} deprecated functions: `~urllib.parse.urlparse`{.interpreted-text role="func"} instead
  - `splitattr()`
  - `splithost()`
  - `splitnport()`
  - `splitpasswd()`
  - `splitport()`
  - `splitquery()`
  - `splittag()`
  - `splittype()`
  - `splituser()`
  - `splitvalue()`
  - `to_bytes()`
- `wsgiref`{.interpreted-text role="mod"}: `SimpleHandler.stdout.write()` should not do partial writes.
- `xml.etree.ElementTree`{.interpreted-text role="mod"}: Testing the truth value of an `~xml.etree.ElementTree.Element`{.interpreted-text role="class"} is deprecated. In a future release it will always return `True`. Prefer explicit `len(elem)` or `elem is not None` tests instead.
- `sys._clear_type_cache`{.interpreted-text role="func"} is deprecated: use `sys._clear_internal_caches`{.interpreted-text role="func"} instead.

## C API deprecations

### Pending removal in Python 3.15

- The `!PyImport_ImportModuleNoBlock`{.interpreted-text role="c:func"}: Use `PyImport_ImportModule`{.interpreted-text role="c:func"} instead.

- `!PyWeakref_GetObject`{.interpreted-text role="c:func"} and `!PyWeakref_GET_OBJECT`{.interpreted-text role="c:func"}: Use `PyWeakref_GetRef`{.interpreted-text role="c:func"} instead. The [pythoncapi-compat project](https://github.com/python/pythoncapi-compat/) can be used to get `PyWeakref_GetRef`{.interpreted-text role="c:func"} on Python 3.12 and older.

- `Py_UNICODE`{.interpreted-text role="c:type"} type and the `!Py_UNICODE_WIDE`{.interpreted-text role="c:macro"} macro: Use `wchar_t`{.interpreted-text role="c:type"} instead.

- `!PyUnicode_AsDecodedObject`{.interpreted-text role="c:func"}: Use `PyCodec_Decode`{.interpreted-text role="c:func"} instead.

- `!PyUnicode_AsDecodedUnicode`{.interpreted-text role="c:func"}: Use `PyCodec_Decode`{.interpreted-text role="c:func"} instead; Note that some codecs (for example, \"base64\") may return a type other than `str`{.interpreted-text role="class"}, such as `bytes`{.interpreted-text role="class"}.

- `!PyUnicode_AsEncodedObject`{.interpreted-text role="c:func"}: Use `PyCodec_Encode`{.interpreted-text role="c:func"} instead.

- `!PyUnicode_AsEncodedUnicode`{.interpreted-text role="c:func"}: Use `PyCodec_Encode`{.interpreted-text role="c:func"} instead; Note that some codecs (for example, \"base64\") may return a type other than `bytes`{.interpreted-text role="class"}, such as `str`{.interpreted-text role="class"}.

- Python initialization functions, deprecated in Python 3.13:

  - `!Py_GetPath`{.interpreted-text role="c:func"}: Use `PyConfig_Get("module_search_paths") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.path`{.interpreted-text role="data"}) instead.
  - `!Py_GetPrefix`{.interpreted-text role="c:func"}: Use `PyConfig_Get("base_prefix") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.base_prefix`{.interpreted-text role="data"}) instead. Use `PyConfig_Get("prefix")
    <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.prefix`{.interpreted-text role="data"}) if `virtual environments
    <venv-def>`{.interpreted-text role="ref"} need to be handled.
  - `!Py_GetExecPrefix`{.interpreted-text role="c:func"}: Use `PyConfig_Get("base_exec_prefix") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.base_exec_prefix`{.interpreted-text role="data"}) instead. Use `PyConfig_Get("exec_prefix") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.exec_prefix`{.interpreted-text role="data"}) if `virtual environments <venv-def>`{.interpreted-text role="ref"} need to be handled.
  - `!Py_GetProgramFullPath`{.interpreted-text role="c:func"}: Use `PyConfig_Get("executable") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.executable`{.interpreted-text role="data"}) instead.
  - `!Py_GetProgramName`{.interpreted-text role="c:func"}: Use `PyConfig_Get("executable") <PyConfig_Get>`{.interpreted-text role="c:func"} (`sys.executable`{.interpreted-text role="data"}) instead.
  - `!Py_GetPythonHome`{.interpreted-text role="c:func"}: Use `PyConfig_Get("home") <PyConfig_Get>`{.interpreted-text role="c:func"} or the `PYTHONHOME`{.interpreted-text role="envvar"} environment variable instead.

  The [pythoncapi-compat project](https://github.com/python/pythoncapi-compat/) can be used to get `PyConfig_Get`{.interpreted-text role="c:func"} on Python 3.13 and older.

- Functions to configure Python\'s initialization, deprecated in Python 3.11:

  - `!PySys_SetArgvEx()`{.interpreted-text role="c:func"}: Set `PyConfig.argv`{.interpreted-text role="c:member"} instead.
  - `!PySys_SetArgv()`{.interpreted-text role="c:func"}: Set `PyConfig.argv`{.interpreted-text role="c:member"} instead.
  - `!Py_SetProgramName()`{.interpreted-text role="c:func"}: Set `PyConfig.program_name`{.interpreted-text role="c:member"} instead.
  - `!Py_SetPythonHome()`{.interpreted-text role="c:func"}: Set `PyConfig.home`{.interpreted-text role="c:member"} instead.
  - `!PySys_ResetWarnOptions`{.interpreted-text role="c:func"}: Clear `sys.warnoptions`{.interpreted-text role="data"} and `!warnings.filters`{.interpreted-text role="data"} instead.

  The `Py_InitializeFromConfig`{.interpreted-text role="c:func"} API should be used with `PyConfig`{.interpreted-text role="c:type"} instead.

- Global configuration variables:

  - `Py_DebugFlag`{.interpreted-text role="c:var"}: Use `PyConfig.parser_debug`{.interpreted-text role="c:member"} or `PyConfig_Get("parser_debug") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_VerboseFlag`{.interpreted-text role="c:var"}: Use `PyConfig.verbose`{.interpreted-text role="c:member"} or `PyConfig_Get("verbose") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_QuietFlag`{.interpreted-text role="c:var"}: Use `PyConfig.quiet`{.interpreted-text role="c:member"} or `PyConfig_Get("quiet") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_InteractiveFlag`{.interpreted-text role="c:var"}: Use `PyConfig.interactive`{.interpreted-text role="c:member"} or `PyConfig_Get("interactive") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_InspectFlag`{.interpreted-text role="c:var"}: Use `PyConfig.inspect`{.interpreted-text role="c:member"} or `PyConfig_Get("inspect") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_OptimizeFlag`{.interpreted-text role="c:var"}: Use `PyConfig.optimization_level`{.interpreted-text role="c:member"} or `PyConfig_Get("optimization_level") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_NoSiteFlag`{.interpreted-text role="c:var"}: Use `PyConfig.site_import`{.interpreted-text role="c:member"} or `PyConfig_Get("site_import") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_BytesWarningFlag`{.interpreted-text role="c:var"}: Use `PyConfig.bytes_warning`{.interpreted-text role="c:member"} or `PyConfig_Get("bytes_warning") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_FrozenFlag`{.interpreted-text role="c:var"}: Use `PyConfig.pathconfig_warnings`{.interpreted-text role="c:member"} or `PyConfig_Get("pathconfig_warnings") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_IgnoreEnvironmentFlag`{.interpreted-text role="c:var"}: Use `PyConfig.use_environment`{.interpreted-text role="c:member"} or `PyConfig_Get("use_environment") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_DontWriteBytecodeFlag`{.interpreted-text role="c:var"}: Use `PyConfig.write_bytecode`{.interpreted-text role="c:member"} or `PyConfig_Get("write_bytecode") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_NoUserSiteDirectory`{.interpreted-text role="c:var"}: Use `PyConfig.user_site_directory`{.interpreted-text role="c:member"} or `PyConfig_Get("user_site_directory") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_UnbufferedStdioFlag`{.interpreted-text role="c:var"}: Use `PyConfig.buffered_stdio`{.interpreted-text role="c:member"} or `PyConfig_Get("buffered_stdio") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_HashRandomizationFlag`{.interpreted-text role="c:var"}: Use `PyConfig.use_hash_seed`{.interpreted-text role="c:member"} and `PyConfig.hash_seed`{.interpreted-text role="c:member"} or `PyConfig_Get("hash_seed") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_IsolatedFlag`{.interpreted-text role="c:var"}: Use `PyConfig.isolated`{.interpreted-text role="c:member"} or `PyConfig_Get("isolated") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_LegacyWindowsFSEncodingFlag`{.interpreted-text role="c:var"}: Use `PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} or `PyConfig_Get("legacy_windows_fs_encoding") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `Py_LegacyWindowsStdioFlag`{.interpreted-text role="c:var"}: Use `PyConfig.legacy_windows_stdio`{.interpreted-text role="c:member"} or `PyConfig_Get("legacy_windows_stdio") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `!Py_FileSystemDefaultEncoding`{.interpreted-text role="c:var"}, `!Py_HasFileSystemDefaultEncoding`{.interpreted-text role="c:var"}: Use `PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} or `PyConfig_Get("filesystem_encoding") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `!Py_FileSystemDefaultEncodeErrors`{.interpreted-text role="c:var"}: Use `PyConfig.filesystem_errors`{.interpreted-text role="c:member"} or `PyConfig_Get("filesystem_errors") <PyConfig_Get>`{.interpreted-text role="c:func"} instead.
  - `!Py_UTF8Mode`{.interpreted-text role="c:var"}: Use `PyPreConfig.utf8_mode`{.interpreted-text role="c:member"} or `PyConfig_Get("utf8_mode") <PyConfig_Get>`{.interpreted-text role="c:func"} instead. (see `Py_PreInitialize`{.interpreted-text role="c:func"})

  The `Py_InitializeFromConfig`{.interpreted-text role="c:func"} API should be used with `PyConfig`{.interpreted-text role="c:type"} to set these options. Or `PyConfig_Get`{.interpreted-text role="c:func"} can be used to get these options at runtime.

### Pending removal in Python 3.16

- The bundled copy of `libmpdec`.

### Pending removal in Python 3.18

- The following private functions are deprecated and planned for removal in Python 3.18:

  - `!_PyBytes_Join`{.interpreted-text role="c:func"}: use `PyBytes_Join`{.interpreted-text role="c:func"}.
  - `!_PyDict_GetItemStringWithError`{.interpreted-text role="c:func"}: use `PyDict_GetItemStringRef`{.interpreted-text role="c:func"}.
  - `!_PyDict_Pop()`{.interpreted-text role="c:func"}: use `PyDict_Pop`{.interpreted-text role="c:func"}.
  - `!_PyLong_Sign()`{.interpreted-text role="c:func"}: use `PyLong_GetSign`{.interpreted-text role="c:func"}.
  - `!_PyLong_FromDigits`{.interpreted-text role="c:func"} and `!_PyLong_New`{.interpreted-text role="c:func"}: use `PyLongWriter_Create`{.interpreted-text role="c:func"}.
  - `!_PyThreadState_UncheckedGet`{.interpreted-text role="c:func"}: use `PyThreadState_GetUnchecked`{.interpreted-text role="c:func"}.
  - `!_PyUnicode_AsString`{.interpreted-text role="c:func"}: use `PyUnicode_AsUTF8`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_Init`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_Init(&writer)` with `writer = PyUnicodeWriter_Create(0) <PyUnicodeWriter_Create>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_Finish`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_Finish(&writer)` with `PyUnicodeWriter_Finish(writer) <PyUnicodeWriter_Finish>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_Dealloc`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_Dealloc(&writer)` with `PyUnicodeWriter_Discard(writer) <PyUnicodeWriter_Discard>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_WriteChar`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_WriteChar(&writer, ch)` with `PyUnicodeWriter_WriteChar(writer, ch) <PyUnicodeWriter_WriteChar>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_WriteStr`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_WriteStr(&writer, str)` with `PyUnicodeWriter_WriteStr(writer, str) <PyUnicodeWriter_WriteStr>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_WriteSubstring`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_WriteSubstring(&writer, str, start, end)` with `PyUnicodeWriter_WriteSubstring(writer, str, start, end) <PyUnicodeWriter_WriteSubstring>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_WriteASCIIString`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_WriteASCIIString(&writer, str)` with `PyUnicodeWriter_WriteASCII(writer, str) <PyUnicodeWriter_WriteASCII>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_WriteLatin1String`{.interpreted-text role="c:func"}: replace `_PyUnicodeWriter_WriteLatin1String(&writer, str)` with `PyUnicodeWriter_WriteUTF8(writer, str) <PyUnicodeWriter_WriteUTF8>`{.interpreted-text role="c:func"}.
  - `!_PyUnicodeWriter_Prepare`{.interpreted-text role="c:func"}: (no replacement).
  - `!_PyUnicodeWriter_PrepareKind`{.interpreted-text role="c:func"}: (no replacement).
  - `!_Py_HashPointer`{.interpreted-text role="c:func"}: use `Py_HashPointer`{.interpreted-text role="c:func"}.
  - `!_Py_fopen_obj`{.interpreted-text role="c:func"}: use `Py_fopen`{.interpreted-text role="c:func"}.

  The [pythoncapi-compat project](https://github.com/python/pythoncapi-compat/) can be used to get these new public functions on Python 3.13 and older. (Contributed by Victor Stinner in `128863`{.interpreted-text role="gh"}.)

### Pending removal in Python 3.19

- `456`{.interpreted-text role="pep"} embedders support for the string hashing scheme definition.

### Pending removal in Python 3.20

- `!_PyObject_CallMethodId`{.interpreted-text role="c:func"}, `!_PyObject_GetAttrId`{.interpreted-text role="c:func"} and `!_PyUnicode_FromId`{.interpreted-text role="c:func"} are deprecated since 3.15 and will be removed in 3.20. Instead, use `PyUnicode_InternFromString()`{.interpreted-text role="c:func"} and cache the result in the module state, then call `PyObject_CallMethod`{.interpreted-text role="c:func"} or `PyObject_GetAttr`{.interpreted-text role="c:func"}. (Contributed by Victor Stinner in `141049`{.interpreted-text role="gh"}.)
- The `cval` field in `PyComplexObject`{.interpreted-text role="c:type"} (`128813`{.interpreted-text role="gh"}). Use `PyComplex_AsCComplex`{.interpreted-text role="c:func"} and `PyComplex_FromCComplex`{.interpreted-text role="c:func"} to convert a Python complex number to/from the C `Py_complex`{.interpreted-text role="c:type"} representation.
- Macros `!Py_MATH_PIl`{.interpreted-text role="c:macro"} and `!Py_MATH_El`{.interpreted-text role="c:macro"}.

### Pending removal in future versions

The following APIs are deprecated and will be removed, although there is currently no date scheduled for their removal.

- `Py_TPFLAGS_HAVE_FINALIZE`{.interpreted-text role="c:macro"}: Unneeded since Python 3.8.
- `PyErr_Fetch`{.interpreted-text role="c:func"}: Use `PyErr_GetRaisedException`{.interpreted-text role="c:func"} instead.
- `PyErr_NormalizeException`{.interpreted-text role="c:func"}: Use `PyErr_GetRaisedException`{.interpreted-text role="c:func"} instead.
- `PyErr_Restore`{.interpreted-text role="c:func"}: Use `PyErr_SetRaisedException`{.interpreted-text role="c:func"} instead.
- `PyModule_GetFilename`{.interpreted-text role="c:func"}: Use `PyModule_GetFilenameObject`{.interpreted-text role="c:func"} instead.
- `PyOS_AfterFork`{.interpreted-text role="c:func"}: Use `PyOS_AfterFork_Child`{.interpreted-text role="c:func"} instead.
- `PySlice_GetIndicesEx`{.interpreted-text role="c:func"}: Use `PySlice_Unpack`{.interpreted-text role="c:func"} and `PySlice_AdjustIndices`{.interpreted-text role="c:func"} instead.
- `PyUnicode_READY`{.interpreted-text role="c:func"}: Unneeded since Python 3.12
- `!PyErr_Display`{.interpreted-text role="c:func"}: Use `PyErr_DisplayException`{.interpreted-text role="c:func"} instead.
- `!_PyErr_ChainExceptions`{.interpreted-text role="c:func"}: Use `!_PyErr_ChainExceptions1`{.interpreted-text role="c:func"} instead.
- `!PyBytesObject.ob_shash`{.interpreted-text role="c:member"} member: call `PyObject_Hash`{.interpreted-text role="c:func"} instead.
- Thread Local Storage (TLS) API:
  - `PyThread_create_key`{.interpreted-text role="c:func"}: Use `PyThread_tss_alloc`{.interpreted-text role="c:func"} instead.
  - `PyThread_delete_key`{.interpreted-text role="c:func"}: Use `PyThread_tss_free`{.interpreted-text role="c:func"} instead.
  - `PyThread_set_key_value`{.interpreted-text role="c:func"}: Use `PyThread_tss_set`{.interpreted-text role="c:func"} instead.
  - `PyThread_get_key_value`{.interpreted-text role="c:func"}: Use `PyThread_tss_get`{.interpreted-text role="c:func"} instead.
  - `PyThread_delete_key_value`{.interpreted-text role="c:func"}: Use `PyThread_tss_delete`{.interpreted-text role="c:func"} instead.
  - `PyThread_ReInitTLS`{.interpreted-text role="c:func"}: Unneeded since Python 3.7.
