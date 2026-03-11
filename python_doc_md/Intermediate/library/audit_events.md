:::: {#audit-events}
::: index
single: audit events
:::
::::

# Audit events table

This table contains all events raised by `sys.audit`{.interpreted-text role="func"} or `PySys_Audit`{.interpreted-text role="c:func"} calls throughout the CPython runtime and the standard library. These calls were added in 3.8 or later (see `578`{.interpreted-text role="pep"}).

See `sys.addaudithook`{.interpreted-text role="func"} and `PySys_AddAuditHook`{.interpreted-text role="c:func"} for information on handling these events.

::: impl-detail
This table is generated from the CPython documentation, and may not represent events raised by other implementations. See your runtime specific documentation for actual events raised.
:::

::: audit-event-table
:::

The following events are raised internally and do not correspond to any public API of CPython:

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  Audit event                                               Arguments
  --------------------------------------------------------- ---------------------------------------------------------------------------------------------
  [winapi.CreateFile]{#winapi.createfile}                   `file_name`, `desired_access`, `share_mode`, `creation_disposition`, `flags_and_attributes`

  [winapi.CreateJunction]{#winapi.createjunction}           `src_path`, `dst_path`

  [winapi.CreateNamedPipe]{#winapi.createnamedpipe}         `name`, `open_mode`, `pipe_mode`

  [winapi.CreatePipe]{#winapi.createpipe}                   

  [winapi.CreateProcess]{#winapi.createprocess}             `application_name`, `command_line`, `current_directory`

  [winapi.OpenProcess]{#winapi.openprocess}                 `process_id`, `desired_access`

  [winapi.TerminateProcess]{#winapi.terminateprocess}       `handle`, `exit_code`

  [posixsubprocess.fork_exec]{#posixsubprocess.fork_exec}   `exec_list`, `args`, `env`

  ctypes.PyObj_FromPtr                                      `obj`
  -------------------------------------------------------------------------------------------------------------------------------------------------------

::: versionadded
3.14 The `_posixsubprocess.fork_exec` internal audit event.
:::
