# `!grp`{.interpreted-text role="mod"} \-\-- The group database

::: {.module synopsis="The group database (getgrnam() and friends)."}
grp
:::

------------------------------------------------------------------------

This module provides access to the Unix group database. It is available on all Unix versions.

::: availability
Unix, not WASI, not Android, not iOS.
:::

Group database entries are reported as a tuple-like object, whose attributes correspond to the members of the `group` structure (Attribute field below, see `<grp.h>`):

  -----------------------------------------------------------------
  Index   Attribute   Meaning
  ------- ----------- ---------------------------------------------
  0       gr_name     the name of the group

  1       gr_passwd   the (encrypted) group password; often empty

  2       gr_gid      the numerical group ID

  3       gr_mem      all the group member\'s user names
  -----------------------------------------------------------------

The gid is an integer, name and password are strings, and the member list is a list of strings. (Note that most users are not explicitly listed as members of the group they are in according to the password database. Check both databases to get complete membership information. Also note that a `gr_name` that starts with a `+` or `-` is likely to be a YP/NIS reference and may not be accessible via `getgrnam`{.interpreted-text role="func"} or `getgrgid`{.interpreted-text role="func"}.)

It defines the following items:

:::: function
getgrgid(id)

Return the group database entry for the given numeric group ID. `KeyError`{.interpreted-text role="exc"} is raised if the entry asked for cannot be found.

::: versionchanged
3.10 `TypeError`{.interpreted-text role="exc"} is raised for non-integer arguments like floats or strings.
:::
::::

::: function
getgrnam(name)

Return the group database entry for the given group name. `KeyError`{.interpreted-text role="exc"} is raised if the entry asked for cannot be found.
:::

::: function
getgrall()

Return a list of all available group entries, in arbitrary order.
:::

::: seealso

Module `pwd`{.interpreted-text role="mod"}

:   An interface to the user database, similar to this.
:::
