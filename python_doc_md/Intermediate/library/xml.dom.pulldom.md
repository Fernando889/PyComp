# `!xml.dom.pulldom`{.interpreted-text role="mod"} \-\-- Support for building partial DOM trees

::: {.module synopsis="Support for building partial DOM trees from SAX events."}
xml.dom.pulldom
:::

**Source code:** `Lib/xml/dom/pulldom.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!xml.dom.pulldom`{.interpreted-text role="mod"} module provides a \"pull parser\" which can also be asked to produce DOM-accessible fragments of the document where necessary. The basic concept involves pulling \"events\" from a stream of incoming XML and processing them. In contrast to SAX which also employs an event-driven processing model together with callbacks, the user of a pull parser is responsible for explicitly pulling events from the stream, looping over those events until either processing is finished or an error condition occurs.

:::: note
::: title
Note
:::

If you need to parse untrusted or unauthenticated data, see `xml-security`{.interpreted-text role="ref"}.
::::

::: versionchanged
3.7.1

The SAX parser no longer processes general external entities by default to increase security by default. To enable processing of external entities, pass a custom parser instance in:

    from xml.dom.pulldom import parse
    from xml.sax import make_parser
    from xml.sax.handler import feature_external_ges

    parser = make_parser()
    parser.setFeature(feature_external_ges, True)
    parse(filename, parser=parser)
:::

Example:

    from xml.dom import pulldom

    doc = pulldom.parse('sales_items.xml')
    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.tagName == 'item':
            if int(node.getAttribute('price')) > 50:
                doc.expandNode(node)
                print(node.toxml())

`event` is a constant and can be one of:

- `START_ELEMENT`{.interpreted-text role="data"}
- `END_ELEMENT`{.interpreted-text role="data"}
- `COMMENT`{.interpreted-text role="data"}
- `START_DOCUMENT`{.interpreted-text role="data"}
- `END_DOCUMENT`{.interpreted-text role="data"}
- `CHARACTERS`{.interpreted-text role="data"}
- `PROCESSING_INSTRUCTION`{.interpreted-text role="data"}
- `IGNORABLE_WHITESPACE`{.interpreted-text role="data"}

`node` is an object of type `xml.dom.minidom.Document`{.interpreted-text role="class"}, `xml.dom.minidom.Element`{.interpreted-text role="class"} or `xml.dom.minidom.Text`{.interpreted-text role="class"}.

Since the document is treated as a \"flat\" stream of events, the document \"tree\" is implicitly traversed and the desired elements are found regardless of their depth in the tree. In other words, one does not need to consider hierarchical issues such as recursive searching of the document nodes, although if the context of elements were important, one would either need to maintain some context-related state (i.e. remembering where one is in the document at any given point) or to make use of the `DOMEventStream.expandNode`{.interpreted-text role="func"} method and switch to DOM-related processing.

::: PullDOM(documentFactory=None)
Subclass of `xml.sax.handler.ContentHandler`{.interpreted-text role="class"}.
:::

::: SAX2DOM(documentFactory=None)
Subclass of `xml.sax.handler.ContentHandler`{.interpreted-text role="class"}.
:::

::: function
parse(stream_or_string, parser=None, bufsize=None)

Return a `DOMEventStream`{.interpreted-text role="class"} from the given input. *stream_or_string* may be either a file name, or a file-like object. *parser*, if given, must be an `~xml.sax.xmlreader.XMLReader`{.interpreted-text role="class"} object. This function will change the document handler of the parser and activate namespace support; other parser configuration (like setting an entity resolver) must have been done in advance.
:::

If you have XML in a string, you can use the `parseString`{.interpreted-text role="func"} function instead:

::: function
parseString(string, parser=None)

Return a `DOMEventStream`{.interpreted-text role="class"} that represents the (Unicode) *string*.
:::

::: data
default_bufsize

Default value for the *bufsize* parameter to `parse`{.interpreted-text role="func"}.

The value of this variable can be changed before calling `parse`{.interpreted-text role="func"} and the new value will take effect.
:::

## DOMEventStream Objects

::::::: {.DOMEventStream(stream, .parser, .bufsize)}
::: versionchanged
3.11 Support for `~object.__getitem__`{.interpreted-text role="meth"} method has been removed.
:::

::: method
getEvent()

Return a tuple containing *event* and the current *node* as `xml.dom.minidom.Document`{.interpreted-text role="class"} if event equals `START_DOCUMENT`{.interpreted-text role="data"}, `xml.dom.minidom.Element`{.interpreted-text role="class"} if event equals `START_ELEMENT`{.interpreted-text role="data"} or `END_ELEMENT`{.interpreted-text role="data"} or `xml.dom.minidom.Text`{.interpreted-text role="class"} if event equals `CHARACTERS`{.interpreted-text role="data"}. The current node does not contain information about its children, unless `expandNode`{.interpreted-text role="func"} is called.
:::

::: method
expandNode(node)

Expands all children of *node* into *node*. Example:

    from xml.dom import pulldom

    xml = '<html><title>Foo</title> <p>Some text <div>and more</div></p> </html>'
    doc = pulldom.parseString(xml)
    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.tagName == 'p':
            # Following statement only prints '<p/>'
            print(node.toxml())
            doc.expandNode(node)
            # Following statement prints node with all its children '<p>Some text <div>and more</div></p>'
            print(node.toxml())
:::

::: method
DOMEventStream.reset()
:::
:::::::
