# `!syslog`{.interpreted-text role="mod"} \-\-- Unix syslog library routines

::: {.module synopsis="An interface to the Unix syslog library routines."}
syslog
:::

------------------------------------------------------------------------

This module provides an interface to the Unix `syslog` library routines. Refer to the Unix manual pages for a detailed description of the `syslog` facility.

::: availability
Unix, not WASI, not iOS.
:::

This module wraps the system `syslog` family of routines. A pure Python library that can speak to a syslog server is available in the `logging.handlers`{.interpreted-text role="mod"} module as `~logging.handlers.SysLogHandler`{.interpreted-text role="class"}.

The module defines the following functions:

:::::: function
syslog(message) syslog(priority, message)

Send the string *message* to the system logger. A trailing newline is added if necessary. Each message is tagged with a priority composed of a *facility* and a *level*. The optional *priority* argument, which defaults to `LOG_INFO`{.interpreted-text role="const"}, determines the message priority. If the facility is not encoded in *priority* using logical-or (`LOG_INFO | LOG_USER`), the value given in the `openlog`{.interpreted-text role="func"} call is used.

If `openlog`{.interpreted-text role="func"} has not been called prior to the call to `syslog`{.interpreted-text role="func"}, `openlog`{.interpreted-text role="func"} will be called with no arguments.

::: audit-event
syslog.syslog priority,message syslog.syslog
:::

::: versionchanged
3.2 In previous versions, `openlog`{.interpreted-text role="func"} would not be called automatically if it wasn\'t called prior to the call to `syslog`{.interpreted-text role="func"}, deferring to the syslog implementation to call `openlog()`.
:::

::: versionchanged
3.12 This function is restricted in subinterpreters. (Only code that runs in multiple interpreters is affected and the restriction is not relevant for most users.) `openlog`{.interpreted-text role="func"} must be called in the main interpreter before `syslog`{.interpreted-text role="func"} may be used in a subinterpreter. Otherwise it will raise `RuntimeError`{.interpreted-text role="exc"}.
:::
::::::

:::::: function
openlog(\[ident\[, logoption\[, facility\]\]\])

Logging options of subsequent `syslog`{.interpreted-text role="func"} calls can be set by calling `openlog`{.interpreted-text role="func"}. `syslog`{.interpreted-text role="func"} will call `openlog`{.interpreted-text role="func"} with no arguments if the log is not currently open.

The optional *ident* keyword argument is a string which is prepended to every message, and defaults to `sys.argv[0]` with leading path components stripped. The optional *logoption* keyword argument (default is 0) is a bit field \-- see below for possible values to combine. The optional *facility* keyword argument (default is `LOG_USER`{.interpreted-text role="const"}) sets the default facility for messages which do not have a facility explicitly encoded.

::: audit-event
syslog.openlog ident,logoption,facility syslog.openlog
:::

::: versionchanged
3.2 In previous versions, keyword arguments were not allowed, and *ident* was required.
:::

::: versionchanged
3.12 This function is restricted in subinterpreters. (Only code that runs in multiple interpreters is affected and the restriction is not relevant for most users.) This may only be called in the main interpreter. It will raise `RuntimeError`{.interpreted-text role="exc"} if called in a subinterpreter.
:::
::::::

::::: function
closelog()

Reset the syslog module values and call the system library `closelog()`.

This causes the module to behave as it does when initially imported. For example, `openlog`{.interpreted-text role="func"} will be called on the first `syslog`{.interpreted-text role="func"} call (if `openlog`{.interpreted-text role="func"} hasn\'t already been called), and *ident* and other `openlog`{.interpreted-text role="func"} parameters are reset to defaults.

::: audit-event
syslog.closelog \"\" syslog.closelog
:::

::: versionchanged
3.12 This function is restricted in subinterpreters. (Only code that runs in multiple interpreters is affected and the restriction is not relevant for most users.) This may only be called in the main interpreter. It will raise `RuntimeError`{.interpreted-text role="exc"} if called in a subinterpreter.
:::
:::::

:::: function
setlogmask(maskpri)

Set the priority mask to *maskpri* and return the previous mask value. Calls to `syslog`{.interpreted-text role="func"} with a priority level not set in *maskpri* are ignored. The default is to log all priorities. The function `LOG_MASK(pri)` calculates the mask for the individual priority *pri*. The function `LOG_UPTO(pri)` calculates the mask for all priorities up to and including *pri*.

::: audit-event
syslog.setlogmask maskpri syslog.setlogmask
:::
::::

The module defines the following constants:

::: data
LOG_EMERG LOG_ALERT LOG_CRIT LOG_ERR LOG_WARNING LOG_NOTICE LOG_INFO LOG_DEBUG

Priority levels (high to low).
:::

:::: data
LOG_AUTH LOG_AUTHPRIV LOG_CRON LOG_DAEMON LOG_FTP LOG_INSTALL LOG_KERN LOG_LAUNCHD LOG_LPR LOG_MAIL LOG_NETINFO LOG_NEWS LOG_RAS LOG_REMOTEAUTH LOG_SYSLOG LOG_USER LOG_UUCP LOG_LOCAL0 LOG_LOCAL1 LOG_LOCAL2 LOG_LOCAL3 LOG_LOCAL4 LOG_LOCAL5 LOG_LOCAL6 LOG_LOCAL7

Facilities, depending on availability in `<syslog.h>` for `LOG_AUTHPRIV`{.interpreted-text role="const"}, `LOG_FTP`{.interpreted-text role="const"}, `LOG_NETINFO`{.interpreted-text role="const"}, `LOG_REMOTEAUTH`{.interpreted-text role="const"}, `LOG_INSTALL`{.interpreted-text role="const"} and `LOG_RAS`{.interpreted-text role="const"}.

::: versionchanged
3.13 Added `LOG_FTP`{.interpreted-text role="const"}, `LOG_NETINFO`{.interpreted-text role="const"}, `LOG_REMOTEAUTH`{.interpreted-text role="const"}, `LOG_INSTALL`{.interpreted-text role="const"}, `LOG_RAS`{.interpreted-text role="const"}, and `LOG_LAUNCHD`{.interpreted-text role="const"}.
:::
::::

::: data
LOG_PID LOG_CONS LOG_NDELAY LOG_ODELAY LOG_NOWAIT LOG_PERROR

Log options, depending on availability in `<syslog.h>` for `LOG_ODELAY`{.interpreted-text role="const"}, `LOG_NOWAIT`{.interpreted-text role="const"} and `LOG_PERROR`{.interpreted-text role="const"}.
:::

## Examples

### Simple example

A simple set of examples:

    import syslog

    syslog.syslog('Processing started')
    if error:
        syslog.syslog(syslog.LOG_ERR, 'Processing started')

An example of setting some log options, these would include the process ID in logged messages, and write the messages to the destination facility used for mail logging:

    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
    syslog.syslog('E-mail processing initiated...')
