# The `!compression`{.interpreted-text role="mod"} package

::: module
compression
:::

::: versionadded
3.14
:::

The `!compression`{.interpreted-text role="mod"} package contains the canonical compression modules containing interfaces to several different compression algorithms. Some of these modules have historically been available as separate modules; those will continue to be available under their original names for compatibility reasons, and will not be removed without a deprecation cycle. The use of modules in `!compression`{.interpreted-text role="mod"} is encouraged where practical.

- `!compression.bz2`{.interpreted-text role="mod"} \-- Re-exports `bz2`{.interpreted-text role="mod"}
- `!compression.gzip`{.interpreted-text role="mod"} \-- Re-exports `gzip`{.interpreted-text role="mod"}
- `!compression.lzma`{.interpreted-text role="mod"} \-- Re-exports `lzma`{.interpreted-text role="mod"}
- `!compression.zlib`{.interpreted-text role="mod"} \-- Re-exports `zlib`{.interpreted-text role="mod"}
- `compression.zstd`{.interpreted-text role="mod"} \-- Wrapper for the Zstandard compression library
