# Pending removal in Python 3.18

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
