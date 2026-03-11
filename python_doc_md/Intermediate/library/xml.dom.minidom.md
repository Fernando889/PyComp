# `!xml.dom.minidom`{.interpreted-text role="mod"} \-\-- Minimal DOM implementation

::: {.module synopsis="Minimal Document Object Model (DOM) implementation."}
xml.dom.minidom
:::

**Source code:** `Lib/xml/dom/minidom.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

`!xml.dom.minidom`{.interpreted-text role="mod"} is a minimal implementation of the Document Object Model interface, with an API similar to that in other languages. It is intended to be simpler than the full DOM and also significantly smaller. Users who are not already proficient with the DOM should consider using the `xml.etree.ElementTree`{.interpreted-text role="mod"} module for their XML processing instead.

:::: note
::: title
Note
:::

If you need to parse untrusted or unauthenticated data, see `xml-security`{.interpreted-text role="ref"}.
::::

DOM applications typically start by parsing some XML into a DOM. With `!xml.dom.minidom`{.interpreted-text role="mod"}, this is done through the parse functions:

    from xml.dom.minidom import parse, parseString

    dom1 = parse('c:\\temp\\mydata.xml')  # parse an XML file by name

    datasource = open('c:\\temp\\mydata.xml')
    dom2 = parse(datasource)  # parse an open file

    dom3 = parseString('<myxml>Some data<empty/> some more data</myxml>')

The `parse`{.interpreted-text role="func"} function can take either a filename or an open file object.

::: function
parse(filename_or_file, parser=None, bufsize=None)

Return a `Document`{.interpreted-text role="class"} from the given input. *filename_or_file* may be either a file name, or a file-like object. *parser*, if given, must be a SAX2 parser object. This function will change the document handler of the parser and activate namespace support; other parser configuration (like setting an entity resolver) must have been done in advance.
:::

If you have XML in a string, you can use the `parseString`{.interpreted-text role="func"} function instead:

::: function
parseString(string, parser=None)

Return a `Document`{.interpreted-text role="class"} that represents the *string*. This method creates an `io.StringIO`{.interpreted-text role="class"} object for the string and passes that on to `parse`{.interpreted-text role="func"}.
:::

Both functions return a `Document`{.interpreted-text role="class"} object representing the content of the document.

What the `parse`{.interpreted-text role="func"} and `parseString`{.interpreted-text role="func"} functions do is connect an XML parser with a \"DOM builder\" that can accept parse events from any SAX parser and convert them into a DOM tree. The names of the functions are perhaps misleading, but are easy to grasp when learning the interfaces. The parsing of the document will be completed before these functions return; it\'s simply that these functions do not provide a parser implementation themselves.

You can also create a `Document`{.interpreted-text role="class"} by calling a method on a \"DOM Implementation\" object. You can get this object either by calling the `getDOMImplementation`{.interpreted-text role="func"} function in the `xml.dom`{.interpreted-text role="mod"} package or the `!xml.dom.minidom`{.interpreted-text role="mod"} module. Once you have a `Document`{.interpreted-text role="class"}, you can add child nodes to it to populate the DOM:

    from xml.dom.minidom import getDOMImplementation

    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "some_tag", None)
    top_element = newdoc.documentElement
    text = newdoc.createTextNode('Some textual content.')
    top_element.appendChild(text)

Once you have a DOM document object, you can access the parts of your XML document through its properties and methods. These properties are defined in the DOM specification. The main property of the document object is the `documentElement`{.interpreted-text role="attr"} property. It gives you the main element in the XML document: the one that holds all others. Here is an example program:

    dom3 = parseString("<myxml>Some data</myxml>")
    assert dom3.documentElement.tagName == "myxml"

When you are finished with a DOM tree, you may optionally call the `unlink`{.interpreted-text role="meth"} method to encourage early cleanup of the now-unneeded objects. `unlink`{.interpreted-text role="meth"} is an `!xml.dom.minidom`{.interpreted-text role="mod"}-specific extension to the DOM API that renders the node and its descendants essentially useless. Otherwise, Python\'s garbage collector will eventually take care of the objects in the tree.

::: seealso

[Document Object Model (DOM) Level 1 Specification](https://www.w3.org/TR/REC-DOM-Level-1/)

:   The W3C recommendation for the DOM supported by `!xml.dom.minidom`{.interpreted-text role="mod"}.
:::

## DOM Objects {#minidom-objects}

The definition of the DOM API for Python is given as part of the `xml.dom`{.interpreted-text role="mod"} module documentation. This section lists the differences between the API and `!xml.dom.minidom`{.interpreted-text role="mod"}.

::: method
Node.unlink()

Break internal references within the DOM so that it will be garbage collected on versions of Python without cyclic GC. Even when cyclic GC is available, using this can make large amounts of memory available sooner, so calling this on DOM objects as soon as they are no longer needed is good practice. This only needs to be called on the `Document`{.interpreted-text role="class"} object, but may be called on child nodes to discard children of that node.

You can avoid calling this method explicitly by using the `with`{.interpreted-text role="keyword"} statement. The following code will automatically unlink *dom* when the `!with`{.interpreted-text role="keyword"} block is exited:

    with xml.dom.minidom.parse(datasource) as dom:
        ... # Work with dom.
:::

::::: method
Node.writexml(writer, indent=\"\", addindent=\"\", newl=\"\", encoding=None, standalone=None)

Write XML to the writer object. The writer receives texts but not bytes as input, it should have a `write`{.interpreted-text role="meth"} method which matches that of the file object interface. The *indent* parameter is the indentation of the current node. The *addindent* parameter is the incremental indentation to use for subnodes of the current one. The *newl* parameter specifies the string to use to terminate newlines.

For the `Document`{.interpreted-text role="class"} node, an additional keyword argument *encoding* can be used to specify the encoding field of the XML header.

Similarly, explicitly stating the *standalone* argument causes the standalone document declarations to be added to the prologue of the XML document. If the value is set to `True`, `standalone="yes"` is added, otherwise it is set to `"no"`. Not stating the argument will omit the declaration from the document.

::: versionchanged
3.8 The `writexml`{.interpreted-text role="meth"} method now preserves the attribute order specified by the user.
:::

::: versionchanged
3.9 The *standalone* parameter was added.
:::
:::::

::::: method
Node.toxml(encoding=None, standalone=None)

Return a string or byte string containing the XML represented by the DOM node.

With an explicit *encoding*[^1] argument, the result is a byte string in the specified encoding. With no *encoding* argument, the result is a Unicode string, and the XML declaration in the resulting string does not specify an encoding. Encoding this string in an encoding other than UTF-8 is likely incorrect, since UTF-8 is the default encoding of XML.

The *standalone* argument behaves exactly as in `writexml`{.interpreted-text role="meth"}.

::: versionchanged
3.8 The `toxml`{.interpreted-text role="meth"} method now preserves the attribute order specified by the user.
:::

::: versionchanged
3.9 The *standalone* parameter was added.
:::
:::::

::::: method
Node.toprettyxml(indent=\"t\", newl=\"n\", encoding=None, standalone=None)

Return a pretty-printed version of the document. *indent* specifies the indentation string and defaults to a tabulator; *newl* specifies the string emitted at the end of each line and defaults to `\n`.

The *encoding* argument behaves like the corresponding argument of `toxml`{.interpreted-text role="meth"}.

The *standalone* argument behaves exactly as in `writexml`{.interpreted-text role="meth"}.

::: versionchanged
3.8 The `toprettyxml`{.interpreted-text role="meth"} method now preserves the attribute order specified by the user.
:::

::: versionchanged
3.9 The *standalone* parameter was added.
:::
:::::

## DOM Example

This example program is a fairly realistic example of a simple program. In this particular case, we do not take much advantage of the flexibility of the DOM.

::: literalinclude
../includes/minidom-example.py
:::

## minidom and the DOM standard {#minidom-and-dom}

The `!xml.dom.minidom`{.interpreted-text role="mod"} module is essentially a DOM 1.0-compatible DOM with some DOM 2 features (primarily namespace features).

Usage of the DOM interface in Python is straight-forward. The following mapping rules apply:

- Interfaces are accessed through instance objects. Applications should not instantiate the classes themselves; they should use the creator functions available on the `Document`{.interpreted-text role="class"} object. Derived interfaces support all operations (and attributes) from the base interfaces, plus any new operations.
- Operations are used as methods. Since the DOM uses only `in`{.interpreted-text role="keyword"} parameters, the arguments are passed in normal order (from left to right). There are no optional arguments. `void` operations return `None`.
- IDL attributes map to instance attributes. For compatibility with the OMG IDL language mapping for Python, an attribute `foo` can also be accessed through accessor methods `_get_foo`{.interpreted-text role="meth"} and `_set_foo`{.interpreted-text role="meth"}. `readonly` attributes must not be changed; this is not enforced at runtime.
- The types `short int`, `unsigned int`, `unsigned long long`, and `boolean` all map to Python integer objects.
- The type `DOMString` maps to Python strings. `!xml.dom.minidom`{.interpreted-text role="mod"} supports either bytes or strings, but will normally produce strings. Values of type `DOMString` may also be `None` where allowed to have the IDL `null` value by the DOM specification from the W3C.
- `const` declarations map to variables in their respective scope (e.g. `xml.dom.minidom.Node.PROCESSING_INSTRUCTION_NODE`); they must not be changed.
- `DOMException` is currently not supported in `!xml.dom.minidom`{.interpreted-text role="mod"}. Instead, `!xml.dom.minidom`{.interpreted-text role="mod"} uses standard Python exceptions such as `TypeError`{.interpreted-text role="exc"} and `AttributeError`{.interpreted-text role="exc"}.
- `NodeList`{.interpreted-text role="class"} objects are implemented using Python\'s built-in list type. These objects provide the interface defined in the DOM specification, but with earlier versions of Python they do not support the official API. They are, however, much more \"Pythonic\" than the interface defined in the W3C recommendations.

The following interfaces have no implementation in `!xml.dom.minidom`{.interpreted-text role="mod"}:

- `DOMTimeStamp`{.interpreted-text role="class"}
- `EntityReference`{.interpreted-text role="class"}

Most of these reflect information in the XML document that is not of general utility to most DOM users.

**Footnotes**

[^1]: The encoding name included in the XML output should conform to the appropriate standards. For example, \"UTF-8\" is valid, but \"UTF8\" is not valid in an XML document\'s declaration, even though Python accepts it as an encoding name. See <https://www.w3.org/TR/2006/REC-xml11-20060816/#NT-EncodingDecl> and <https://www.iana.org/assignments/character-sets/character-sets.xhtml>.
