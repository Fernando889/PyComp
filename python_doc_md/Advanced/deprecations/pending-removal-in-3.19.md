# Pending removal in Python 3.19

- `ctypes`{.interpreted-text role="mod"}:
  - Implicitly switching to the MSVC-compatible struct layout by setting `~ctypes.Structure._pack_`{.interpreted-text role="attr"} but not `~ctypes.Structure._layout_`{.interpreted-text role="attr"} on non-Windows platforms.
- `hashlib`{.interpreted-text role="mod"}:
  - In hash function constructors such as `~hashlib.new`{.interpreted-text role="func"} or the direct hash-named constructors such as `~hashlib.md5`{.interpreted-text role="func"} and `~hashlib.sha256`{.interpreted-text role="func"}, their optional initial data parameter could also be passed a keyword argument named `data=` or `string=` in various `!hashlib`{.interpreted-text role="mod"} implementations.

    Support for the `string` keyword argument name is now deprecated and slated for removal in Python 3.19.

    Before Python 3.13, the `string` keyword parameter was not correctly supported depending on the backend implementation of hash functions. Prefer passing the initial data as a positional argument for maximum backwards compatibility.
