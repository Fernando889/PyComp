:::: {#security-warnings}
::: index
single: security considerations
:::
::::

# Security Considerations

The following modules have specific security considerations:

- `base64`{.interpreted-text role="mod"}: `base64 security considerations <base64-security>`{.interpreted-text role="ref"} in `4648`{.interpreted-text role="rfc"}
- `hashlib`{.interpreted-text role="mod"}: `all constructors take a "usedforsecurity" keyword-only
  argument disabling known insecure and blocked algorithms
  <hashlib-usedforsecurity>`{.interpreted-text role="ref"}
- `http.server`{.interpreted-text role="mod"} is not suitable for production use, only implementing basic security checks. See the `security considerations <http.server-security>`{.interpreted-text role="ref"}.
- `logging`{.interpreted-text role="mod"}: `Logging configuration uses eval()
  <logging-eval-security>`{.interpreted-text role="ref"}
- `multiprocessing`{.interpreted-text role="mod"}: `Connection.recv() uses pickle
  <multiprocessing-recv-pickle-security>`{.interpreted-text role="ref"}
- `pickle`{.interpreted-text role="mod"}: `Restricting globals in pickle <pickle-restrict>`{.interpreted-text role="ref"}
- `random`{.interpreted-text role="mod"} shouldn\'t be used for security purposes, use `secrets`{.interpreted-text role="mod"} instead
- `shelve`{.interpreted-text role="mod"}: `shelve is based on pickle and thus unsuitable for
  dealing with untrusted sources <shelve-security>`{.interpreted-text role="ref"}
- `ssl`{.interpreted-text role="mod"}: `SSL/TLS security considerations <ssl-security>`{.interpreted-text role="ref"}
- `subprocess`{.interpreted-text role="mod"}: `Subprocess security considerations
  <subprocess-security>`{.interpreted-text role="ref"}
- `tempfile`{.interpreted-text role="mod"}: `mktemp is deprecated due to vulnerability to race
  conditions <tempfile-mktemp-deprecated>`{.interpreted-text role="ref"}
- `xml`{.interpreted-text role="mod"}: `XML security <xml-security>`{.interpreted-text role="ref"}
- `zipfile`{.interpreted-text role="mod"}: `maliciously prepared .zip files can cause disk volume
  exhaustion <zipfile-resources-limitations>`{.interpreted-text role="ref"}

The `-I`{.interpreted-text role="option"} command line option can be used to run Python in isolated mode. When it cannot be used, the `-P`{.interpreted-text role="option"} option or the `PYTHONSAFEPATH`{.interpreted-text role="envvar"} environment variable can be used to not prepend a potentially unsafe path to `sys.path`{.interpreted-text role="data"} such as the current directory, the script\'s directory or an empty string.
