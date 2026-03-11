# Pending removal in Python 3.20

- The `__version__`, `version` and `VERSION` attributes have been deprecated in these standard library modules and will be removed in Python 3.20. Use `sys.version_info`{.interpreted-text role="py:data"} instead.

  - `argparse`{.interpreted-text role="mod"}
  - `csv`{.interpreted-text role="mod"}
  - `ctypes`{.interpreted-text role="mod"}
  - `!ctypes.macholib`{.interpreted-text role="mod"}
  - `decimal`{.interpreted-text role="mod"} (use `decimal.SPEC_VERSION`{.interpreted-text role="data"} instead)
  - `http.server`{.interpreted-text role="mod"}
  - `imaplib`{.interpreted-text role="mod"}
  - `ipaddress`{.interpreted-text role="mod"}
  - `json`{.interpreted-text role="mod"}
  - `logging`{.interpreted-text role="mod"} (`__date__` also deprecated)
  - `optparse`{.interpreted-text role="mod"}
  - `pickle`{.interpreted-text role="mod"}
  - `platform`{.interpreted-text role="mod"}
  - `re`{.interpreted-text role="mod"}
  - `socketserver`{.interpreted-text role="mod"}
  - `tabnanny`{.interpreted-text role="mod"}
  - `tkinter.font`{.interpreted-text role="mod"}
  - `tkinter.ttk`{.interpreted-text role="mod"}
  - `wsgiref.simple_server`{.interpreted-text role="mod"}
  - `xml.etree.ElementTree`{.interpreted-text role="mod"}
  - `!xml.sax.expatreader`{.interpreted-text role="mod"}
  - `xml.sax.handler`{.interpreted-text role="mod"}
  - `zlib`{.interpreted-text role="mod"}

  (Contributed by Hugo van Kemenade and Stan Ulbrych in `76007`{.interpreted-text role="gh"}.)
