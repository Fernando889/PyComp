# `!xml.dom`{.interpreted-text role="mod"} \-\-- The Document Object Model API

::: {.module synopsis="Document Object Model API for Python."}
xml.dom
:::

**Source code:** `Lib/xml/dom/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The Document Object Model, or \"DOM,\" is a cross-language API from the World Wide Web Consortium (W3C) for accessing and modifying XML documents. A DOM implementation presents an XML document as a tree structure, or allows client code to build such a structure from scratch. It then gives access to the structure through a set of objects which provided well-known interfaces.

The DOM is extremely useful for random-access applications. SAX only allows you a view of one bit of the document at a time. If you are looking at one SAX element, you have no access to another. If you are looking at a text node, you have no access to a containing element. When you write a SAX application, you need to keep track of your program\'s position in the document somewhere in your own code. SAX does not do it for you. Also, if you need to look ahead in the XML document, you are just out of luck.

Some applications are simply impossible in an event driven model with no access to a tree. Of course you could build some sort of tree yourself in SAX events, but the DOM allows you to avoid writing that code. The DOM is a standard tree representation for XML data.

The Document Object Model is being defined by the W3C in stages, or \"levels\" in their terminology. The Python mapping of the API is substantially based on the DOM Level 2 recommendation.

DOM applications typically start by parsing some XML into a DOM. How this is accomplished is not covered at all by DOM Level 1, and Level 2 provides only limited improvements: There is a `DOMImplementation`{.interpreted-text role="class"} object class which provides access to `Document`{.interpreted-text role="class"} creation methods, but no way to access an XML reader/parser/Document builder in an implementation-independent way. There is also no well-defined way to access these methods without an existing `Document`{.interpreted-text role="class"} object. In Python, each DOM implementation will provide a function `getDOMImplementation`{.interpreted-text role="func"}. DOM Level 3 adds a Load/Store specification, which defines an interface to the reader, but this is not yet available in the Python standard library.

Once you have a DOM document object, you can access the parts of your XML document through its properties and methods. These properties are defined in the DOM specification; this portion of the reference manual describes the interpretation of the specification in Python.

The specification provided by the W3C defines the DOM API for Java, ECMAScript, and OMG IDL. The Python mapping defined here is based in large part on the IDL version of the specification, but strict compliance is not required (though implementations are free to support the strict mapping from IDL). See section `dom-conformance`{.interpreted-text role="ref"} for a detailed discussion of mapping requirements.

::: seealso

[Document Object Model (DOM) Level 2 Specification](https://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/)

:   The W3C recommendation upon which the Python DOM API is based.

[Document Object Model (DOM) Level 1 Specification](https://www.w3.org/TR/REC-DOM-Level-1/)

:   The W3C recommendation for the DOM supported by `xml.dom.minidom`{.interpreted-text role="mod"}.

[Python Language Mapping Specification](https://www.omg.org/spec/PYTH/1.2/PDF)

:   This specifies the mapping from OMG IDL to Python.
:::

## Module Contents

The `!xml.dom`{.interpreted-text role="mod"} contains the following functions:

::: function
registerDOMImplementation(name, factory)

Register the *factory* function with the name *name*. The factory function should return an object which implements the `DOMImplementation`{.interpreted-text role="class"} interface. The factory function can return the same object every time, or a new one for each call, as appropriate for the specific implementation (e.g. if that implementation supports some customization).
:::

::: function
getDOMImplementation(name=None, features=())

Return a suitable DOM implementation. The *name* is either well-known, the module name of a DOM implementation, or `None`. If it is not `None`, imports the corresponding module and returns a `DOMImplementation`{.interpreted-text role="class"} object if the import succeeds. If no name is given, and if the environment variable `PYTHON_DOM`{.interpreted-text role="envvar"} is set, this variable is used to find the implementation.

If name is not given, this examines the available implementations to find one with the required feature set. If no implementation can be found, raise an `ImportError`{.interpreted-text role="exc"}. The features list must be a sequence of `(feature, version)` pairs which are passed to the `hasFeature`{.interpreted-text role="meth"} method on available `DOMImplementation`{.interpreted-text role="class"} objects.
:::

Some convenience constants are also provided:

::: data
EMPTY_NAMESPACE

The value used to indicate that no namespace is associated with a node in the DOM. This is typically found as the `namespaceURI`{.interpreted-text role="attr"} of a node, or used as the *namespaceURI* parameter to a namespaces-specific method.
:::

::: data
XML_NAMESPACE

The namespace URI associated with the reserved prefix `xml`, as defined by [Namespaces in XML](https://www.w3.org/TR/REC-xml-names/) (section 4).
:::

::: data
XMLNS_NAMESPACE

The namespace URI for namespace declarations, as defined by [Document Object Model (DOM) Level 2 Core Specification](https://www.w3.org/TR/DOM-Level-2-Core/core.html) (section 1.1.8).
:::

::: data
XHTML_NAMESPACE

The URI of the XHTML namespace as defined by [XHTML 1.0: The Extensible HyperText Markup Language](https://www.w3.org/TR/xhtml1/) (section 3.1.1).
:::

In addition, `!xml.dom`{.interpreted-text role="mod"} contains a base `Node`{.interpreted-text role="class"} class and the DOM exception classes. The `Node`{.interpreted-text role="class"} class provided by this module does not implement any of the methods or attributes defined by the DOM specification; concrete DOM implementations must provide those. The `Node`{.interpreted-text role="class"} class provided as part of this module does provide the constants used for the `nodeType`{.interpreted-text role="attr"} attribute on concrete `Node`{.interpreted-text role="class"} objects; they are located within the class rather than at the module level to conform with the DOM specifications.

## Objects in the DOM {#dom-objects}

The definitive documentation for the DOM is the DOM specification from the W3C.

Note that DOM attributes may also be manipulated as nodes instead of as simple strings. It is fairly rare that you must do this, however, so this usage is not yet documented.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Interface                                                 Section                                                      Purpose
  --------------------------------------------------------- ------------------------------------------------------------ ------------------------------------------------------------------
  `DOMImplementation`{.interpreted-text role="class"}       `dom-implementation-objects`{.interpreted-text role="ref"}   Interface to the underlying implementation.

  `Node`{.interpreted-text role="class"}                    `dom-node-objects`{.interpreted-text role="ref"}             Base interface for most objects in a document.

  `NodeList`{.interpreted-text role="class"}                `dom-nodelist-objects`{.interpreted-text role="ref"}         Interface for a sequence of nodes.

  `DocumentType`{.interpreted-text role="class"}            `dom-documenttype-objects`{.interpreted-text role="ref"}     Information about the declarations needed to process a document.

  `Document`{.interpreted-text role="class"}                `dom-document-objects`{.interpreted-text role="ref"}         Object which represents an entire document.

  `Element`{.interpreted-text role="class"}                 `dom-element-objects`{.interpreted-text role="ref"}          Element nodes in the document hierarchy.

  `Attr`{.interpreted-text role="class"}                    `dom-attr-objects`{.interpreted-text role="ref"}             Attribute value nodes on element nodes.

  `Comment`{.interpreted-text role="class"}                 `dom-comment-objects`{.interpreted-text role="ref"}          Representation of comments in the source document.

  `Text`{.interpreted-text role="class"}                    `dom-text-objects`{.interpreted-text role="ref"}             Nodes containing textual content from the document.

  `ProcessingInstruction`{.interpreted-text role="class"}   `dom-pi-objects`{.interpreted-text role="ref"}               Processing instruction representation.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

An additional section describes the exceptions defined for working with the DOM in Python.

### DOMImplementation Objects {#dom-implementation-objects}

The `DOMImplementation`{.interpreted-text role="class"} interface provides a way for applications to determine the availability of particular features in the DOM they are using. DOM Level 2 added the ability to create new `Document`{.interpreted-text role="class"} and `DocumentType`{.interpreted-text role="class"} objects using the `DOMImplementation`{.interpreted-text role="class"} as well.

::: method
DOMImplementation.hasFeature(feature, version)

Return `True` if the feature identified by the pair of strings *feature* and *version* is implemented.
:::

::: method
DOMImplementation.createDocument(namespaceUri, qualifiedName, doctype)

Return a new `Document`{.interpreted-text role="class"} object (the root of the DOM), with a child `Element`{.interpreted-text role="class"} object having the given *namespaceUri* and *qualifiedName*. The *doctype* must be a `DocumentType`{.interpreted-text role="class"} object created by `createDocumentType`{.interpreted-text role="meth"}, or `None`. In the Python DOM API, the first two arguments can also be `None` in order to indicate that no `Element`{.interpreted-text role="class"} child is to be created.
:::

::: method
DOMImplementation.createDocumentType(qualifiedName, publicId, systemId)

Return a new `DocumentType`{.interpreted-text role="class"} object that encapsulates the given *qualifiedName*, *publicId*, and *systemId* strings, representing the information contained in an XML document type declaration.
:::

### Node Objects {#dom-node-objects}

All of the components of an XML document are subclasses of `Node`{.interpreted-text role="class"}.

::: attribute
Node.nodeType

An integer representing the node type. Symbolic constants for the types are on the `Node`{.interpreted-text role="class"} object: `ELEMENT_NODE`{.interpreted-text role="const"}, `ATTRIBUTE_NODE`{.interpreted-text role="const"}, `TEXT_NODE`{.interpreted-text role="const"}, `CDATA_SECTION_NODE`{.interpreted-text role="const"}, `ENTITY_NODE`{.interpreted-text role="const"}, `PROCESSING_INSTRUCTION_NODE`{.interpreted-text role="const"}, `COMMENT_NODE`{.interpreted-text role="const"}, `DOCUMENT_NODE`{.interpreted-text role="const"}, `DOCUMENT_TYPE_NODE`{.interpreted-text role="const"}, `NOTATION_NODE`{.interpreted-text role="const"}. This is a read-only attribute.
:::

::: attribute
Node.parentNode

The parent of the current node, or `None` for the document node. The value is always a `Node`{.interpreted-text role="class"} object or `None`. For `Element`{.interpreted-text role="class"} nodes, this will be the parent element, except for the root element, in which case it will be the `Document`{.interpreted-text role="class"} object. For `Attr`{.interpreted-text role="class"} nodes, this is always `None`. This is a read-only attribute.
:::

::: attribute
Node.attributes

A `NamedNodeMap`{.interpreted-text role="class"} of attribute objects. Only elements have actual values for this; others provide `None` for this attribute. This is a read-only attribute.
:::

::: attribute
Node.previousSibling

The node that immediately precedes this one with the same parent. For instance the element with an end-tag that comes just before the *self* element\'s start-tag. Of course, XML documents are made up of more than just elements so the previous sibling could be text, a comment, or something else. If this node is the first child of the parent, this attribute will be `None`. This is a read-only attribute.
:::

::: attribute
Node.nextSibling

The node that immediately follows this one with the same parent. See also `previousSibling`{.interpreted-text role="attr"}. If this is the last child of the parent, this attribute will be `None`. This is a read-only attribute.
:::

::: attribute
Node.childNodes

A list of nodes contained within this node. This is a read-only attribute.
:::

::: attribute
Node.firstChild

The first child of the node, if there are any, or `None`. This is a read-only attribute.
:::

::: attribute
Node.lastChild

The last child of the node, if there are any, or `None`. This is a read-only attribute.
:::

::: attribute
Node.localName

The part of the `tagName`{.interpreted-text role="attr"} following the colon if there is one, else the entire `tagName`{.interpreted-text role="attr"}. The value is a string.
:::

::: attribute
Node.prefix

The part of the `tagName`{.interpreted-text role="attr"} preceding the colon if there is one, else the empty string. The value is a string, or `None`.
:::

::: attribute
Node.namespaceURI

The namespace associated with the element name. This will be a string or `None`. This is a read-only attribute.
:::

::: attribute
Node.nodeName

This has a different meaning for each node type; see the DOM specification for details. You can always get the information you would get here from another property such as the `tagName`{.interpreted-text role="attr"} property for elements or the `name`{.interpreted-text role="attr"} property for attributes. For all node types, the value of this attribute will be either a string or `None`. This is a read-only attribute.
:::

::: attribute
Node.nodeValue

This has a different meaning for each node type; see the DOM specification for details. The situation is similar to that with `nodeName`{.interpreted-text role="attr"}. The value is a string or `None`.
:::

::: method
Node.hasAttributes()

Return `True` if the node has any attributes.
:::

::: method
Node.hasChildNodes()

Return `True` if the node has any child nodes.
:::

::::: method
Node.isSameNode(other)

Return `True` if *other* refers to the same node as this node. This is especially useful for DOM implementations which use any sort of proxy architecture (because more than one object can refer to the same node).

:::: note
::: title
Note
:::

This is based on a proposed DOM Level 3 API which is still in the \"working draft\" stage, but this particular interface appears uncontroversial. Changes from the W3C will not necessarily affect this method in the Python DOM interface (though any new W3C API for this would also be supported).
::::
:::::

::: method
Node.appendChild(newChild)

Add a new child node to this node at the end of the list of children, returning *newChild*. If the node was already in the tree, it is removed first.
:::

::: method
Node.insertBefore(newChild, refChild)

Insert a new child node before an existing child. It must be the case that *refChild* is a child of this node; if not, `ValueError`{.interpreted-text role="exc"} is raised. *newChild* is returned. If *refChild* is `None`, it inserts *newChild* at the end of the children\'s list.
:::

::: method
Node.removeChild(oldChild)

Remove a child node. *oldChild* must be a child of this node; if not, `ValueError`{.interpreted-text role="exc"} is raised. *oldChild* is returned on success. If *oldChild* will not be used further, its `unlink`{.interpreted-text role="meth"} method should be called.
:::

::: method
Node.replaceChild(newChild, oldChild)

Replace an existing node with a new node. It must be the case that *oldChild* is a child of this node; if not, `ValueError`{.interpreted-text role="exc"} is raised.
:::

::: method
Node.normalize()

Join adjacent text nodes so that all stretches of text are stored as single `Text`{.interpreted-text role="class"} instances. This simplifies processing text from a DOM tree for many applications.
:::

::: method
Node.cloneNode(deep)

Clone this node. Setting *deep* means to clone all child nodes as well. This returns the clone.
:::

### NodeList Objects {#dom-nodelist-objects}

A `NodeList`{.interpreted-text role="class"} represents a sequence of nodes. These objects are used in two ways in the DOM Core recommendation: an `Element`{.interpreted-text role="class"} object provides one as its list of child nodes, and the `getElementsByTagName`{.interpreted-text role="meth"} and `getElementsByTagNameNS`{.interpreted-text role="meth"} methods of `Node`{.interpreted-text role="class"} return objects with this interface to represent query results.

The DOM Level 2 recommendation defines one method and one attribute for these objects:

::: method
NodeList.item(i)

Return the *i*\'th item from the sequence, if there is one, or `None`. The index *i* is not allowed to be less than zero or greater than or equal to the length of the sequence.
:::

::: attribute
NodeList.length

The number of nodes in the sequence.
:::

In addition, the Python DOM interface requires that some additional support is provided to allow `NodeList`{.interpreted-text role="class"} objects to be used as Python sequences. All `NodeList`{.interpreted-text role="class"} implementations must include support for `~object.__len__`{.interpreted-text role="meth"} and `~object.__getitem__`{.interpreted-text role="meth"}; this allows iteration over the `NodeList`{.interpreted-text role="class"} in `for`{.interpreted-text role="keyword"} statements and proper support for the `len`{.interpreted-text role="func"} built-in function.

If a DOM implementation supports modification of the document, the `NodeList`{.interpreted-text role="class"} implementation must also support the `~object.__setitem__`{.interpreted-text role="meth"} and `~object.__delitem__`{.interpreted-text role="meth"} methods.

### DocumentType Objects {#dom-documenttype-objects}

Information about the notations and entities declared by a document (including the external subset if the parser uses it and can provide the information) is available from a `DocumentType`{.interpreted-text role="class"} object. The `DocumentType`{.interpreted-text role="class"} for a document is available from the `Document`{.interpreted-text role="class"} object\'s `doctype`{.interpreted-text role="attr"} attribute; if there is no `DOCTYPE` declaration for the document, the document\'s `doctype`{.interpreted-text role="attr"} attribute will be set to `None` instead of an instance of this interface.

`DocumentType`{.interpreted-text role="class"} is a specialization of `Node`{.interpreted-text role="class"}, and adds the following attributes:

::: attribute
DocumentType.publicId

The public identifier for the external subset of the document type definition. This will be a string or `None`.
:::

::: attribute
DocumentType.systemId

The system identifier for the external subset of the document type definition. This will be a URI as a string, or `None`.
:::

::: attribute
DocumentType.internalSubset

A string giving the complete internal subset from the document. This does not include the brackets which enclose the subset. If the document has no internal subset, this should be `None`.
:::

::: attribute
DocumentType.name

The name of the root element as given in the `DOCTYPE` declaration, if present.
:::

::: attribute
DocumentType.entities

This is a `NamedNodeMap`{.interpreted-text role="class"} giving the definitions of external entities. For entity names defined more than once, only the first definition is provided (others are ignored as required by the XML recommendation). This may be `None` if the information is not provided by the parser, or if no entities are defined.
:::

::: attribute
DocumentType.notations

This is a `NamedNodeMap`{.interpreted-text role="class"} giving the definitions of notations. For notation names defined more than once, only the first definition is provided (others are ignored as required by the XML recommendation). This may be `None` if the information is not provided by the parser, or if no notations are defined.
:::

### Document Objects {#dom-document-objects}

A `Document`{.interpreted-text role="class"} represents an entire XML document, including its constituent elements, attributes, processing instructions, comments etc. Remember that it inherits properties from `Node`{.interpreted-text role="class"}.

::: attribute
Document.documentElement

The one and only root element of the document.
:::

::: method
Document.createElement(tagName)

Create and return a new element node. The element is not inserted into the document when it is created. You need to explicitly insert it with one of the other methods such as `insertBefore`{.interpreted-text role="meth"} or `appendChild`{.interpreted-text role="meth"}.
:::

::: method
Document.createElementNS(namespaceURI, tagName)

Create and return a new element with a namespace. The *tagName* may have a prefix. The element is not inserted into the document when it is created. You need to explicitly insert it with one of the other methods such as `insertBefore`{.interpreted-text role="meth"} or `appendChild`{.interpreted-text role="meth"}.
:::

::: method
Document.createTextNode(data)

Create and return a text node containing the data passed as a parameter. As with the other creation methods, this one does not insert the node into the tree.
:::

::: method
Document.createComment(data)

Create and return a comment node containing the data passed as a parameter. As with the other creation methods, this one does not insert the node into the tree.
:::

::: method
Document.createProcessingInstruction(target, data)

Create and return a processing instruction node containing the *target* and *data* passed as parameters. As with the other creation methods, this one does not insert the node into the tree.
:::

::: method
Document.createAttribute(name)

Create and return an attribute node. This method does not associate the attribute node with any particular element. You must use `setAttributeNode`{.interpreted-text role="meth"} on the appropriate `Element`{.interpreted-text role="class"} object to use the newly created attribute instance.
:::

::: method
Document.createAttributeNS(namespaceURI, qualifiedName)

Create and return an attribute node with a namespace. The *tagName* may have a prefix. This method does not associate the attribute node with any particular element. You must use `setAttributeNode`{.interpreted-text role="meth"} on the appropriate `Element`{.interpreted-text role="class"} object to use the newly created attribute instance.
:::

::: method
Document.getElementsByTagName(tagName)

Search for all descendants (direct children, children\'s children, etc.) with a particular element type name.
:::

::: method
Document.getElementsByTagNameNS(namespaceURI, localName)

Search for all descendants (direct children, children\'s children, etc.) with a particular namespace URI and localname. The localname is the part of the namespace after the prefix.
:::

### Element Objects {#dom-element-objects}

`Element`{.interpreted-text role="class"} is a subclass of `Node`{.interpreted-text role="class"}, so inherits all the attributes of that class.

::: attribute
Element.tagName

The element type name. In a namespace-using document it may have colons in it. The value is a string.
:::

::: method
Element.getElementsByTagName(tagName)

Same as equivalent method in the `Document`{.interpreted-text role="class"} class.
:::

::: method
Element.getElementsByTagNameNS(namespaceURI, localName)

Same as equivalent method in the `Document`{.interpreted-text role="class"} class.
:::

::: method
Element.hasAttribute(name)

Return `True` if the element has an attribute named by *name*.
:::

::: method
Element.hasAttributeNS(namespaceURI, localName)

Return `True` if the element has an attribute named by *namespaceURI* and *localName*.
:::

::: method
Element.getAttribute(name)

Return the value of the attribute named by *name* as a string. If no such attribute exists, an empty string is returned, as if the attribute had no value.
:::

::: method
Element.getAttributeNode(attrname)

Return the `Attr`{.interpreted-text role="class"} node for the attribute named by *attrname*.
:::

::: method
Element.getAttributeNS(namespaceURI, localName)

Return the value of the attribute named by *namespaceURI* and *localName* as a string. If no such attribute exists, an empty string is returned, as if the attribute had no value.
:::

::: method
Element.getAttributeNodeNS(namespaceURI, localName)

Return an attribute value as a node, given a *namespaceURI* and *localName*.
:::

::: method
Element.removeAttribute(name)

Remove an attribute by name. If there is no matching attribute, a `NotFoundErr`{.interpreted-text role="exc"} is raised.
:::

::: method
Element.removeAttributeNode(oldAttr)

Remove and return *oldAttr* from the attribute list, if present. If *oldAttr* is not present, `NotFoundErr`{.interpreted-text role="exc"} is raised.
:::

::: method
Element.removeAttributeNS(namespaceURI, localName)

Remove an attribute by name. Note that it uses a localName, not a qname. No exception is raised if there is no matching attribute.
:::

::: method
Element.setAttribute(name, value)

Set an attribute value from a string.
:::

::: method
Element.setAttributeNode(newAttr)

Add a new attribute node to the element, replacing an existing attribute if necessary if the `name`{.interpreted-text role="attr"} attribute matches. If a replacement occurs, the old attribute node will be returned. If *newAttr* is already in use, `InuseAttributeErr`{.interpreted-text role="exc"} will be raised.
:::

::: method
Element.setAttributeNodeNS(newAttr)

Add a new attribute node to the element, replacing an existing attribute if necessary if the `namespaceURI`{.interpreted-text role="attr"} and `localName`{.interpreted-text role="attr"} attributes match. If a replacement occurs, the old attribute node will be returned. If *newAttr* is already in use, `InuseAttributeErr`{.interpreted-text role="exc"} will be raised.
:::

::: method
Element.setAttributeNS(namespaceURI, qname, value)

Set an attribute value from a string, given a *namespaceURI* and a *qname*. Note that a qname is the whole attribute name. This is different than above.
:::

### Attr Objects {#dom-attr-objects}

`Attr`{.interpreted-text role="class"} inherits from `Node`{.interpreted-text role="class"}, so inherits all its attributes.

::: attribute
Attr.name

The attribute name. In a namespace-using document it may include a colon.
:::

::: attribute
Attr.localName

The part of the name following the colon if there is one, else the entire name. This is a read-only attribute.
:::

::: attribute
Attr.prefix

The part of the name preceding the colon if there is one, else the empty string.
:::

::: attribute
Attr.value

The text value of the attribute. This is a synonym for the `nodeValue`{.interpreted-text role="attr"} attribute.
:::

### NamedNodeMap Objects {#dom-attributelist-objects}

`NamedNodeMap`{.interpreted-text role="class"} does *not* inherit from `Node`{.interpreted-text role="class"}.

::: attribute
NamedNodeMap.length

The length of the attribute list.
:::

::: method
NamedNodeMap.item(index)

Return an attribute with a particular index. The order you get the attributes in is arbitrary but will be consistent for the life of a DOM. Each item is an attribute node. Get its value with the `value`{.interpreted-text role="attr"} attribute.
:::

There are also experimental methods that give this class more mapping behavior. You can use them or you can use the standardized `!getAttribute\*`{.interpreted-text role="meth"} family of methods on the `Element`{.interpreted-text role="class"} objects.

### Comment Objects {#dom-comment-objects}

`Comment`{.interpreted-text role="class"} represents a comment in the XML document. It is a subclass of `Node`{.interpreted-text role="class"}, but cannot have child nodes.

::: attribute
Comment.data

The content of the comment as a string. The attribute contains all characters between the leading `<!-``-` and trailing `-``->`, but does not include them.
:::

### Text and CDATASection Objects {#dom-text-objects}

The `Text`{.interpreted-text role="class"} interface represents text in the XML document. If the parser and DOM implementation support the DOM\'s XML extension, portions of the text enclosed in CDATA marked sections are stored in `CDATASection`{.interpreted-text role="class"} objects. These two interfaces are identical, but provide different values for the `nodeType`{.interpreted-text role="attr"} attribute.

These interfaces extend the `Node`{.interpreted-text role="class"} interface. They cannot have child nodes.

::: attribute
Text.data

The content of the text node as a string.
:::

:::: note
::: title
Note
:::

The use of a `CDATASection`{.interpreted-text role="class"} node does not indicate that the node represents a complete CDATA marked section, only that the content of the node was part of a CDATA section. A single CDATA section may be represented by more than one node in the document tree. There is no way to determine whether two adjacent `CDATASection`{.interpreted-text role="class"} nodes represent different CDATA marked sections.
::::

### ProcessingInstruction Objects {#dom-pi-objects}

Represents a processing instruction in the XML document; this inherits from the `Node`{.interpreted-text role="class"} interface and cannot have child nodes.

::: attribute
ProcessingInstruction.target

The content of the processing instruction up to the first whitespace character. This is a read-only attribute.
:::

::: attribute
ProcessingInstruction.data

The content of the processing instruction following the first whitespace character.
:::

### Exceptions {#dom-exceptions}

The DOM Level 2 recommendation defines a single exception, `DOMException`{.interpreted-text role="exc"}, and a number of constants that allow applications to determine what sort of error occurred. `DOMException`{.interpreted-text role="exc"} instances carry a `code`{.interpreted-text role="attr"} attribute that provides the appropriate value for the specific exception.

The Python DOM interface provides the constants, but also expands the set of exceptions so that a specific exception exists for each of the exception codes defined by the DOM. The implementations must raise the appropriate specific exception, each of which carries the appropriate value for the `code`{.interpreted-text role="attr"} attribute.

::: exception
DOMException

Base exception class used for all specific DOM exceptions. This exception class cannot be directly instantiated.
:::

::: exception
DomstringSizeErr

Raised when a specified range of text does not fit into a string. This is not known to be used in the Python DOM implementations, but may be received from DOM implementations not written in Python.
:::

::: exception
HierarchyRequestErr

Raised when an attempt is made to insert a node where the node type is not allowed.
:::

::: exception
IndexSizeErr

Raised when an index or size parameter to a method is negative or exceeds the allowed values.
:::

::: exception
InuseAttributeErr

Raised when an attempt is made to insert an `Attr`{.interpreted-text role="class"} node that is already present elsewhere in the document.
:::

::: exception
InvalidAccessErr

Raised if a parameter or an operation is not supported on the underlying object.
:::

::: exception
InvalidCharacterErr

This exception is raised when a string parameter contains a character that is not permitted in the context it\'s being used in by the XML 1.0 recommendation. For example, attempting to create an `Element`{.interpreted-text role="class"} node with a space in the element type name will cause this error to be raised.
:::

::: exception
InvalidModificationErr

Raised when an attempt is made to modify the type of a node.
:::

::: exception
InvalidStateErr

Raised when an attempt is made to use an object that is not defined or is no longer usable.
:::

::: exception
NamespaceErr

If an attempt is made to change any object in a way that is not permitted with regard to the [Namespaces in XML](https://www.w3.org/TR/REC-xml-names/) recommendation, this exception is raised.
:::

::: exception
NotFoundErr

Exception when a node does not exist in the referenced context. For example, `NamedNodeMap.removeNamedItem`{.interpreted-text role="meth"} will raise this if the node passed in does not exist in the map.
:::

::: exception
NotSupportedErr

Raised when the implementation does not support the requested type of object or operation.
:::

::: exception
NoDataAllowedErr

This is raised if data is specified for a node which does not support data.
:::

::: exception
NoModificationAllowedErr

Raised on attempts to modify an object where modifications are not allowed (such as for read-only nodes).
:::

::: exception
SyntaxErr

Raised when an invalid or illegal string is specified.
:::

::: exception
WrongDocumentErr

Raised when a node is inserted in a different document than it currently belongs to, and the implementation does not support migrating the node from one document to the other.
:::

The exception codes defined in the DOM recommendation map to the exceptions described above according to this table:

  --------------------------------------------------------------------------------------------------------------------------
  Constant                                                        Exception
  --------------------------------------------------------------- ----------------------------------------------------------
  `DOMSTRING_SIZE_ERR`{.interpreted-text role="const"}            `DomstringSizeErr`{.interpreted-text role="exc"}

  `HIERARCHY_REQUEST_ERR`{.interpreted-text role="const"}         `HierarchyRequestErr`{.interpreted-text role="exc"}

  `INDEX_SIZE_ERR`{.interpreted-text role="const"}                `IndexSizeErr`{.interpreted-text role="exc"}

  `INUSE_ATTRIBUTE_ERR`{.interpreted-text role="const"}           `InuseAttributeErr`{.interpreted-text role="exc"}

  `INVALID_ACCESS_ERR`{.interpreted-text role="const"}            `InvalidAccessErr`{.interpreted-text role="exc"}

  `INVALID_CHARACTER_ERR`{.interpreted-text role="const"}         `InvalidCharacterErr`{.interpreted-text role="exc"}

  `INVALID_MODIFICATION_ERR`{.interpreted-text role="const"}      `InvalidModificationErr`{.interpreted-text role="exc"}

  `INVALID_STATE_ERR`{.interpreted-text role="const"}             `InvalidStateErr`{.interpreted-text role="exc"}

  `NAMESPACE_ERR`{.interpreted-text role="const"}                 `NamespaceErr`{.interpreted-text role="exc"}

  `NOT_FOUND_ERR`{.interpreted-text role="const"}                 `NotFoundErr`{.interpreted-text role="exc"}

  `NOT_SUPPORTED_ERR`{.interpreted-text role="const"}             `NotSupportedErr`{.interpreted-text role="exc"}

  `NO_DATA_ALLOWED_ERR`{.interpreted-text role="const"}           `NoDataAllowedErr`{.interpreted-text role="exc"}

  `NO_MODIFICATION_ALLOWED_ERR`{.interpreted-text role="const"}   `NoModificationAllowedErr`{.interpreted-text role="exc"}

  `SYNTAX_ERR`{.interpreted-text role="const"}                    `SyntaxErr`{.interpreted-text role="exc"}

  `WRONG_DOCUMENT_ERR`{.interpreted-text role="const"}            `WrongDocumentErr`{.interpreted-text role="exc"}
  --------------------------------------------------------------------------------------------------------------------------

## Conformance {#dom-conformance}

This section describes the conformance requirements and relationships between the Python DOM API, the W3C DOM recommendations, and the OMG IDL mapping for Python.

### Type Mapping {#dom-type-mapping}

The IDL types used in the DOM specification are mapped to Python types according to the following table.

  --------------------------------------------------------------
  IDL Type           Python Type
  ------------------ -------------------------------------------
  `boolean`          `bool` or `int`

  `int`              `int`

  `long int`         `int`

  `unsigned int`     `int`

  `DOMString`        `str` or `bytes`

  `null`             `None`
  --------------------------------------------------------------

### Accessor Methods {#dom-accessor-methods}

The mapping from OMG IDL to Python defines accessor functions for IDL `attribute` declarations in much the way the Java mapping does. Mapping the IDL declarations :

    readonly attribute string someValue;
             attribute string anotherValue;

yields three accessor functions: a \"get\" method for `someValue`{.interpreted-text role="attr"} (`_get_someValue`{.interpreted-text role="meth"}), and \"get\" and \"set\" methods for `anotherValue`{.interpreted-text role="attr"} (`_get_anotherValue`{.interpreted-text role="meth"} and `_set_anotherValue`{.interpreted-text role="meth"}). The mapping, in particular, does not require that the IDL attributes are accessible as normal Python attributes: `object.someValue` is *not* required to work, and may raise an `AttributeError`{.interpreted-text role="exc"}.

The Python DOM API, however, *does* require that normal attribute access work. This means that the typical surrogates generated by Python IDL compilers are not likely to work, and wrapper objects may be needed on the client if the DOM objects are accessed via CORBA. While this does require some additional consideration for CORBA DOM clients, the implementers with experience using DOM over CORBA from Python do not consider this a problem. Attributes that are declared `readonly` may not restrict write access in all DOM implementations.

In the Python DOM API, accessor functions are not required. If provided, they should take the form defined by the Python IDL mapping, but these methods are considered unnecessary since the attributes are accessible directly from Python. \"Set\" accessors should never be provided for `readonly` attributes.

The IDL definitions do not fully embody the requirements of the W3C DOM API, such as the notion of certain objects, such as the return value of `getElementsByTagName`{.interpreted-text role="meth"}, being \"live\". The Python DOM API does not require implementations to enforce such requirements.
