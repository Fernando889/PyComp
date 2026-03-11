# Pending removal in future versions

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
