# Superseded modules {#superseded}

The modules described in this chapter have been superseded by other modules for most use cases, and are retained primarily to preserve backwards compatibility.

Modules may appear in this chapter because they only cover a limited subset of a problem space, and a more generally applicable solution is available elsewhere in the standard library (for example, `getopt`{.interpreted-text role="mod"} covers the very specific task of \"mimic the C `!getopt`{.interpreted-text role="c:func"} API in Python\", rather than the broader command line option parsing and argument parsing capabilities offered by `optparse`{.interpreted-text role="mod"} and `argparse`{.interpreted-text role="mod"}).

Alternatively, modules may appear in this chapter because they are deprecated outright, and awaiting removal in a future release, or they are `soft deprecated`{.interpreted-text role="term"} and their use is actively discouraged in new projects. With the removal of various obsolete modules through `594`{.interpreted-text role="pep"}, there are currently no modules in this latter category.

::: {.toctree maxdepth="1"}
getopt.rst profile.rst
:::
