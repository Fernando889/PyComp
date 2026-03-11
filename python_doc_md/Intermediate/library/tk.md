# Graphical user interfaces with Tk {#tkinter}

::: index
single: GUI single: Graphical User Interface single: Tkinter single: Tk
:::

Tk/Tcl has long been an integral part of Python. It provides a robust and platform independent windowing toolkit, that is available to Python programmers using the `tkinter`{.interpreted-text role="mod"} package, and its extension, the `tkinter.ttk`{.interpreted-text role="mod"} module.

The `tkinter`{.interpreted-text role="mod"} package is a thin object-oriented layer on top of Tcl/Tk. To use `tkinter`{.interpreted-text role="mod"}, you don\'t need to write Tcl code, but you will need to consult the Tk documentation, and occasionally the Tcl documentation. `tkinter`{.interpreted-text role="mod"} is a set of wrappers that implement the Tk widgets as Python classes.

`tkinter`{.interpreted-text role="mod"}\'s chief virtues are that it is fast, and that it usually comes bundled with Python. Although its standard documentation is weak, good material is available, which includes: references, tutorials, a book and others. `tkinter`{.interpreted-text role="mod"} is also famous for having an outdated look and feel, which has been vastly improved in Tk 8.5. Nevertheless, there are many other GUI libraries that you could be interested in. The Python wiki lists several alternative [GUI frameworks and tools](https://wiki.python.org/moin/GuiProgramming).

::: toctree
tkinter.rst tkinter.colorchooser.rst tkinter.font.rst dialog.rst tkinter.messagebox.rst tkinter.scrolledtext.rst tkinter.dnd.rst tkinter.ttk.rst idle.rst turtle.rst
:::
