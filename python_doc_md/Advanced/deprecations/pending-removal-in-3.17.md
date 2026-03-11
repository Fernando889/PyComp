# Pending removal in Python 3.17

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
