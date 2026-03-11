# Pending removal in Python 3.15

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
