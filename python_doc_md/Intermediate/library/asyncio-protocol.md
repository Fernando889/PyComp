::: currentmodule
asyncio
:::

# Transports and Protocols {#asyncio-transports-protocols}

**Preface**

Transports and Protocols are used by the **low-level** event loop APIs such as `loop.create_connection`{.interpreted-text role="meth"}. They use callback-based programming style and enable high-performance implementations of network or IPC protocols (e.g. HTTP).

Essentially, transports and protocols should only be used in libraries and frameworks and never in high-level asyncio applications.

This documentation page covers both [Transports](#transports) and [Protocols](#protocols).

**Introduction**

At the highest level, the transport is concerned with *how* bytes are transmitted, while the protocol determines *which* bytes to transmit (and to some extent when).

A different way of saying the same thing: a transport is an abstraction for a socket (or similar I/O endpoint) while a protocol is an abstraction for an application, from the transport\'s point of view.

Yet another view is the transport and protocol interfaces together define an abstract interface for using network I/O and interprocess I/O.

There is always a 1:1 relationship between transport and protocol objects: the protocol calls transport methods to send data, while the transport calls protocol methods to pass it data that has been received.

Most of connection oriented event loop methods (such as `loop.create_connection`{.interpreted-text role="meth"}) usually accept a *protocol_factory* argument used to create a *Protocol* object for an accepted connection, represented by a *Transport* object. Such methods usually return a tuple of `(transport, protocol)`.

**Contents**

This documentation page contains the following sections:

- The [Transports](#transports) section documents asyncio `BaseTransport`{.interpreted-text role="class"}, `ReadTransport`{.interpreted-text role="class"}, `WriteTransport`{.interpreted-text role="class"}, `Transport`{.interpreted-text role="class"}, `DatagramTransport`{.interpreted-text role="class"}, and `SubprocessTransport`{.interpreted-text role="class"} classes.
- The [Protocols](#protocols) section documents asyncio `BaseProtocol`{.interpreted-text role="class"}, `Protocol`{.interpreted-text role="class"}, `BufferedProtocol`{.interpreted-text role="class"}, `DatagramProtocol`{.interpreted-text role="class"}, and `SubprocessProtocol`{.interpreted-text role="class"} classes.
- The [Examples](#examples) section showcases how to work with transports, protocols, and low-level event loop APIs.

## Transports {#asyncio-transport}

**Source code:** `Lib/asyncio/transports.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

Transports are classes provided by `asyncio`{.interpreted-text role="mod"} in order to abstract various kinds of communication channels.

Transport objects are always instantiated by an `asyncio event loop <asyncio-event-loop>`{.interpreted-text role="ref"}.

asyncio implements transports for TCP, UDP, SSL, and subprocess pipes. The methods available on a transport depend on the transport\'s kind.

The transport classes are `not thread safe <asyncio-multithreading>`{.interpreted-text role="ref"}.

### Transports Hierarchy

::: BaseTransport
Base class for all transports. Contains methods that all asyncio transports share.
:::

::: WriteTransport(BaseTransport)
A base transport for write-only connections.

Instances of the *WriteTransport* class are returned from the `loop.connect_write_pipe`{.interpreted-text role="meth"} event loop method and are also used by subprocess-related methods like `loop.subprocess_exec`{.interpreted-text role="meth"}.
:::

::: ReadTransport(BaseTransport)
A base transport for read-only connections.

Instances of the *ReadTransport* class are returned from the `loop.connect_read_pipe`{.interpreted-text role="meth"} event loop method and are also used by subprocess-related methods like `loop.subprocess_exec`{.interpreted-text role="meth"}.
:::

::: {.Transport(WriteTransport, .ReadTransport)}
Interface representing a bidirectional transport, such as a TCP connection.

The user does not instantiate a transport directly; they call a utility function, passing it a protocol factory and other information necessary to create the transport and protocol.

Instances of the *Transport* class are returned from or used by event loop methods like `loop.create_connection`{.interpreted-text role="meth"}, `loop.create_unix_connection`{.interpreted-text role="meth"}, `loop.create_server`{.interpreted-text role="meth"}, `loop.sendfile`{.interpreted-text role="meth"}, etc.
:::

::: DatagramTransport(BaseTransport)
A transport for datagram (UDP) connections.

Instances of the *DatagramTransport* class are returned from the `loop.create_datagram_endpoint`{.interpreted-text role="meth"} event loop method.
:::

::: SubprocessTransport(BaseTransport)
An abstraction to represent a connection between a parent and its child OS process.

Instances of the *SubprocessTransport* class are returned from event loop methods `loop.subprocess_shell`{.interpreted-text role="meth"} and `loop.subprocess_exec`{.interpreted-text role="meth"}.
:::

### Base Transport

::: method
BaseTransport.close()

Close the transport.

If the transport has a buffer for outgoing data, buffered data will be flushed asynchronously. No more data will be received. After all buffered data is flushed, the protocol\'s `protocol.connection_lost()
<BaseProtocol.connection_lost>`{.interpreted-text role="meth"} method will be called with `None`{.interpreted-text role="const"} as its argument. The transport should not be used once it is closed.
:::

::: method
BaseTransport.is_closing()

Return `True` if the transport is closing or is closed.
:::

::: method
BaseTransport.get_extra_info(name, default=None)

Return information about the transport or underlying resources it uses.

*name* is a string representing the piece of transport-specific information to get.

*default* is the value to return if the information is not available, or if the transport does not support querying it with the given third-party event loop implementation or on the current platform.

For example, the following code attempts to get the underlying socket object of the transport:

    sock = transport.get_extra_info('socket')
    if sock is not None:
        print(sock.getsockopt(...))

Categories of information that can be queried on some transports:

- socket:
  - `'peername'`: the remote address to which the socket is connected, result of `socket.socket.getpeername`{.interpreted-text role="meth"} (`None` on error)
  - `'socket'`: `socket.socket`{.interpreted-text role="class"} instance
  - `'sockname'`: the socket\'s own address, result of `socket.socket.getsockname`{.interpreted-text role="meth"}
- SSL socket:
  - `'compression'`: the compression algorithm being used as a string, or `None` if the connection isn\'t compressed; result of `ssl.SSLSocket.compression`{.interpreted-text role="meth"}
  - `'cipher'`: a three-value tuple containing the name of the cipher being used, the version of the SSL protocol that defines its use, and the number of secret bits being used; result of `ssl.SSLSocket.cipher`{.interpreted-text role="meth"}
  - `'peercert'`: peer certificate; result of `ssl.SSLSocket.getpeercert`{.interpreted-text role="meth"}
  - `'sslcontext'`: `ssl.SSLContext`{.interpreted-text role="class"} instance
  - `'ssl_object'`: `ssl.SSLObject`{.interpreted-text role="class"} or `ssl.SSLSocket`{.interpreted-text role="class"} instance
- pipe:
  - `'pipe'`: pipe object
- subprocess:
  - `'subprocess'`: `subprocess.Popen`{.interpreted-text role="class"} instance
:::

::: method
BaseTransport.set_protocol(protocol)

Set a new protocol.

Switching protocol should only be done when both protocols are documented to support the switch.
:::

::: method
BaseTransport.get_protocol()

Return the current protocol.
:::

### Read-only Transports

:::: method
ReadTransport.is_reading()

Return `True` if the transport is receiving new data.

::: versionadded
3.7
:::
::::

:::: method
ReadTransport.pause_reading()

Pause the receiving end of the transport. No data will be passed to the protocol\'s `protocol.data_received() <Protocol.data_received>`{.interpreted-text role="meth"} method until `resume_reading`{.interpreted-text role="meth"} is called.

::: versionchanged
3.7 The method is idempotent, i.e. it can be called when the transport is already paused or closed.
:::
::::

:::: method
ReadTransport.resume_reading()

Resume the receiving end. The protocol\'s `protocol.data_received() <Protocol.data_received>`{.interpreted-text role="meth"} method will be called once again if some data is available for reading.

::: versionchanged
3.7 The method is idempotent, i.e. it can be called when the transport is already reading.
:::
::::

### Write-only Transports

::: method
WriteTransport.abort()

Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol\'s `protocol.connection_lost()
<BaseProtocol.connection_lost>`{.interpreted-text role="meth"} method will eventually be called with `None`{.interpreted-text role="const"} as its argument.
:::

::: method
WriteTransport.can_write_eof()

Return `True`{.interpreted-text role="const"} if the transport supports `~WriteTransport.write_eof`{.interpreted-text role="meth"}, `False`{.interpreted-text role="const"} if not.
:::

::: method
WriteTransport.get_write_buffer_size()

Return the current size of the output buffer used by the transport.
:::

:::: method
WriteTransport.get_write_buffer_limits()

Get the *high* and *low* watermarks for write flow control. Return a tuple `(low, high)` where *low* and *high* are positive number of bytes.

Use `set_write_buffer_limits`{.interpreted-text role="meth"} to set the limits.

::: versionadded
3.4.2
:::
::::

::: method
WriteTransport.set_write_buffer_limits(high=None, low=None)

Set the *high* and *low* watermarks for write flow control.

These two values (measured in number of bytes) control when the protocol\'s `protocol.pause_writing() <BaseProtocol.pause_writing>`{.interpreted-text role="meth"} and `protocol.resume_writing() <BaseProtocol.resume_writing>`{.interpreted-text role="meth"} methods are called. If specified, the low watermark must be less than or equal to the high watermark. Neither *high* nor *low* can be negative.

`~BaseProtocol.pause_writing`{.interpreted-text role="meth"} is called when the buffer size becomes greater than or equal to the *high* value. If writing has been paused, `~BaseProtocol.resume_writing`{.interpreted-text role="meth"} is called when the buffer size becomes less than or equal to the *low* value.

The defaults are implementation-specific. If only the high watermark is given, the low watermark defaults to an implementation-specific value less than or equal to the high watermark. Setting *high* to zero forces *low* to zero as well, and causes `~BaseProtocol.pause_writing`{.interpreted-text role="meth"} to be called whenever the buffer becomes non-empty. Setting *low* to zero causes `~BaseProtocol.resume_writing`{.interpreted-text role="meth"} to be called only once the buffer is empty. Use of zero for either limit is generally sub-optimal as it reduces opportunities for doing I/O and computation concurrently.

Use `~WriteTransport.get_write_buffer_limits`{.interpreted-text role="meth"} to get the limits.
:::

::: method
WriteTransport.write(data)

Write some *data* bytes to the transport.

This method does not block; it buffers the data and arranges for it to be sent out asynchronously.
:::

::: method
WriteTransport.writelines(list_of_data)

Write a list (or any iterable) of data bytes to the transport. This is functionally equivalent to calling `write`{.interpreted-text role="meth"} on each element yielded by the iterable, but may be implemented more efficiently.
:::

::: method
WriteTransport.write_eof()

Close the write end of the transport after flushing all buffered data. Data may still be received.

This method can raise `NotImplementedError`{.interpreted-text role="exc"} if the transport (e.g. SSL) doesn\'t support half-closed connections.
:::

### Datagram Transports

:::: method
DatagramTransport.sendto(data, addr=None)

Send the *data* bytes to the remote peer given by *addr* (a transport-dependent target address). If *addr* is `None`{.interpreted-text role="const"}, the data is sent to the target address given on transport creation.

This method does not block; it buffers the data and arranges for it to be sent out asynchronously.

::: versionchanged
3.13 This method can be called with an empty bytes object to send a zero-length datagram. The buffer size calculation used for flow control is also updated to account for the datagram header.
:::
::::

::: method
DatagramTransport.abort()

Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol\'s `protocol.connection_lost() <BaseProtocol.connection_lost>`{.interpreted-text role="meth"} method will eventually be called with `None`{.interpreted-text role="const"} as its argument.
:::

### Subprocess Transports {#asyncio-subprocess-transports}

::: method
SubprocessTransport.get_pid()

Return the subprocess process id as an integer.
:::

::: method
SubprocessTransport.get_pipe_transport(fd)

Return the transport for the communication pipe corresponding to the integer file descriptor *fd*:

- `0`: writable streaming transport of the standard input (*stdin*), or `None`{.interpreted-text role="const"} if the subprocess was not created with `stdin=PIPE`
- `1`: readable streaming transport of the standard output (*stdout*), or `None`{.interpreted-text role="const"} if the subprocess was not created with `stdout=PIPE`
- `2`: readable streaming transport of the standard error (*stderr*), or `None`{.interpreted-text role="const"} if the subprocess was not created with `stderr=PIPE`
- other *fd*: `None`{.interpreted-text role="const"}
:::

::: method
SubprocessTransport.get_returncode()

Return the subprocess return code as an integer or `None`{.interpreted-text role="const"} if it hasn\'t returned, which is similar to the `subprocess.Popen.returncode`{.interpreted-text role="attr"} attribute.
:::

::: method
SubprocessTransport.kill()

Kill the subprocess.

On POSIX systems, the function sends SIGKILL to the subprocess. On Windows, this method is an alias for `terminate`{.interpreted-text role="meth"}.

See also `subprocess.Popen.kill`{.interpreted-text role="meth"}.
:::

::: method
SubprocessTransport.send_signal(signal)

Send the *signal* number to the subprocess, as in `subprocess.Popen.send_signal`{.interpreted-text role="meth"}.
:::

::: method
SubprocessTransport.terminate()

Stop the subprocess.

On POSIX systems, this method sends `~signal.SIGTERM`{.interpreted-text role="py:const"} to the subprocess. On Windows, the Windows API function `!TerminateProcess`{.interpreted-text role="c:func"} is called to stop the subprocess.

See also `subprocess.Popen.terminate`{.interpreted-text role="meth"}.
:::

::: method
SubprocessTransport.close()

Kill the subprocess by calling the `kill`{.interpreted-text role="meth"} method.

If the subprocess hasn\'t returned yet, and close transports of *stdin*, *stdout*, and *stderr* pipes.
:::

## Protocols {#asyncio-protocol}

**Source code:** `Lib/asyncio/protocols.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

asyncio provides a set of abstract base classes that should be used to implement network protocols. Those classes are meant to be used together with `transports <asyncio-transport>`{.interpreted-text role="ref"}.

Subclasses of abstract base protocol classes may implement some or all methods. All these methods are callbacks: they are called by transports on certain events, for example when some data is received. A base protocol method should be called by the corresponding transport.

### Base Protocols

::: BaseProtocol
Base protocol with methods that all protocols share.
:::

::: Protocol(BaseProtocol)
The base class for implementing streaming protocols (TCP, Unix sockets, etc).
:::

::: BufferedProtocol(BaseProtocol)
A base class for implementing streaming protocols with manual control of the receive buffer.
:::

::: DatagramProtocol(BaseProtocol)
The base class for implementing datagram (UDP) protocols.
:::

::: SubprocessProtocol(BaseProtocol)
The base class for implementing protocols communicating with child processes (unidirectional pipes).
:::

### Base Protocol

All asyncio protocols can implement Base Protocol callbacks.

**Connection Callbacks**

Connection callbacks are called on all protocols, exactly once per a successful connection. All other protocol callbacks can only be called between those two methods.

::: method
BaseProtocol.connection_made(transport)

Called when a connection is made.

The *transport* argument is the transport representing the connection. The protocol is responsible for storing the reference to its transport.
:::

::: method
BaseProtocol.connection_lost(exc)

Called when the connection is lost or closed.

The argument is either an exception object or `None`{.interpreted-text role="const"}. The latter means a regular EOF is received, or the connection was aborted or closed by this side of the connection.
:::

**Flow Control Callbacks**

Flow control callbacks can be called by transports to pause or resume writing performed by the protocol.

See the documentation of the `~WriteTransport.set_write_buffer_limits`{.interpreted-text role="meth"} method for more details.

::: method
BaseProtocol.pause_writing()

Called when the transport\'s buffer goes over the high watermark.
:::

::: method
BaseProtocol.resume_writing()

Called when the transport\'s buffer drains below the low watermark.
:::

If the buffer size equals the high watermark, `~BaseProtocol.pause_writing`{.interpreted-text role="meth"} is not called: the buffer size must go strictly over.

Conversely, `~BaseProtocol.resume_writing`{.interpreted-text role="meth"} is called when the buffer size is equal or lower than the low watermark. These end conditions are important to ensure that things go as expected when either mark is zero.

### Streaming Protocols

Event methods, such as `loop.create_server`{.interpreted-text role="meth"}, `loop.create_unix_server`{.interpreted-text role="meth"}, `loop.create_connection`{.interpreted-text role="meth"}, `loop.create_unix_connection`{.interpreted-text role="meth"}, `loop.connect_accepted_socket`{.interpreted-text role="meth"}, `loop.connect_read_pipe`{.interpreted-text role="meth"}, and `loop.connect_write_pipe`{.interpreted-text role="meth"} accept factories that return streaming protocols.

::: method
Protocol.data_received(data)

Called when some data is received. *data* is a non-empty bytes object containing the incoming data.

Whether the data is buffered, chunked or reassembled depends on the transport. In general, you shouldn\'t rely on specific semantics and instead make your parsing generic and flexible. However, data is always received in the correct order.

The method can be called an arbitrary number of times while a connection is open.

However, `protocol.eof_received() <Protocol.eof_received>`{.interpreted-text role="meth"} is called at most once. Once `eof_received()` is called, `data_received()` is not called anymore.
:::

::: method
Protocol.eof_received()

Called when the other end signals it won\'t send any more data (for example by calling `transport.write_eof()
<WriteTransport.write_eof>`{.interpreted-text role="meth"}, if the other end also uses asyncio).

This method may return a false value (including `None`), in which case the transport will close itself. Conversely, if this method returns a true value, the protocol used determines whether to close the transport. Since the default implementation returns `None`, it implicitly closes the connection.

Some transports, including SSL, don\'t support half-closed connections, in which case returning true from this method will result in the connection being closed.
:::

State machine:

``` none
start -> connection_made
    [-> data_received]*
    [-> eof_received]?
-> connection_lost -> end
```

### Buffered Streaming Protocols

::: versionadded
3.7
:::

Buffered Protocols can be used with any event loop method that supports [Streaming Protocols](#streaming-protocols).

`BufferedProtocol` implementations allow explicit manual allocation and control of the receive buffer. Event loops can then use the buffer provided by the protocol to avoid unnecessary data copies. This can result in noticeable performance improvement for protocols that receive big amounts of data. Sophisticated protocol implementations can significantly reduce the number of buffer allocations.

The following callbacks are called on `BufferedProtocol`{.interpreted-text role="class"} instances:

::: method
BufferedProtocol.get_buffer(sizehint)

Called to allocate a new receive buffer.

*sizehint* is the recommended minimum size for the returned buffer. It is acceptable to return smaller or larger buffers than what *sizehint* suggests. When set to -1, the buffer size can be arbitrary. It is an error to return a buffer with a zero size.

`get_buffer()` must return an object implementing the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}.
:::

::: method
BufferedProtocol.buffer_updated(nbytes)

Called when the buffer was updated with the received data.

*nbytes* is the total number of bytes that were written to the buffer.
:::

::: method
BufferedProtocol.eof_received()

See the documentation of the `protocol.eof_received()
<Protocol.eof_received>`{.interpreted-text role="meth"} method.
:::

`~BufferedProtocol.get_buffer`{.interpreted-text role="meth"} can be called an arbitrary number of times during a connection. However, `protocol.eof_received()
<Protocol.eof_received>`{.interpreted-text role="meth"} is called at most once and, if called, `~BufferedProtocol.get_buffer`{.interpreted-text role="meth"} and `~BufferedProtocol.buffer_updated`{.interpreted-text role="meth"} won\'t be called after it.

State machine:

``` none
start -> connection_made
    [-> get_buffer
        [-> buffer_updated]?
    ]*
    [-> eof_received]?
-> connection_lost -> end
```

### Datagram Protocols

Datagram Protocol instances should be constructed by protocol factories passed to the `loop.create_datagram_endpoint`{.interpreted-text role="meth"} method.

::: method
DatagramProtocol.datagram_received(data, addr)

Called when a datagram is received. *data* is a bytes object containing the incoming data. *addr* is the address of the peer sending the data; the exact format depends on the transport.
:::

::: method
DatagramProtocol.error_received(exc)

Called when a previous send or receive operation raises an `OSError`{.interpreted-text role="class"}. *exc* is the `OSError`{.interpreted-text role="class"} instance.

This method is called in rare conditions, when the transport (e.g. UDP) detects that a datagram could not be delivered to its recipient. In many conditions though, undeliverable datagrams will be silently dropped.
:::

:::: note
::: title
Note
:::

On BSD systems (macOS, FreeBSD, etc.) flow control is not supported for datagram protocols, because there is no reliable way to detect send failures caused by writing too many packets.

The socket always appears \'ready\' and excess packets are dropped. An `OSError`{.interpreted-text role="class"} with `errno` set to `errno.ENOBUFS`{.interpreted-text role="const"} may or may not be raised; if it is raised, it will be reported to `DatagramProtocol.error_received`{.interpreted-text role="meth"} but otherwise ignored.
::::

### Subprocess Protocols {#asyncio-subprocess-protocols}

Subprocess Protocol instances should be constructed by protocol factories passed to the `loop.subprocess_exec`{.interpreted-text role="meth"} and `loop.subprocess_shell`{.interpreted-text role="meth"} methods.

::: method
SubprocessProtocol.pipe_data_received(fd, data)

Called when the child process writes data into its stdout or stderr pipe.

*fd* is the integer file descriptor of the pipe.

*data* is a non-empty bytes object containing the received data.
:::

::: method
SubprocessProtocol.pipe_connection_lost(fd, exc)

Called when one of the pipes communicating with the child process is closed.

*fd* is the integer file descriptor that was closed.
:::

::: method
SubprocessProtocol.process_exited()

Called when the child process has exited.

It can be called before `~SubprocessProtocol.pipe_data_received`{.interpreted-text role="meth"} and `~SubprocessProtocol.pipe_connection_lost`{.interpreted-text role="meth"} methods.
:::

## Examples

### TCP Echo Server {#asyncio_example_tcp_echo_server_protocol}

Create a TCP echo server using the `loop.create_server`{.interpreted-text role="meth"} method, send back received data, and close the connection:

    import asyncio


    class EchoServerProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            peername = transport.get_extra_info('peername')
            print('Connection from {}'.format(peername))
            self.transport = transport

        def data_received(self, data):
            message = data.decode()
            print('Data received: {!r}'.format(message))

            print('Send: {!r}'.format(message))
            self.transport.write(data)

            print('Close the client socket')
            self.transport.close()


    async def main():
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()

        server = await loop.create_server(
            EchoServerProtocol,
            '127.0.0.1', 8888)

        async with server:
            await server.serve_forever()


    asyncio.run(main())

::: seealso
The `TCP echo server using streams <asyncio-tcp-echo-server-streams>`{.interpreted-text role="ref"} example uses the high-level `asyncio.start_server`{.interpreted-text role="func"} function.
:::

### TCP Echo Client {#asyncio_example_tcp_echo_client_protocol}

A TCP echo client using the `loop.create_connection`{.interpreted-text role="meth"} method, sends data, and waits until the connection is closed:

    import asyncio


    class EchoClientProtocol(asyncio.Protocol):
        def __init__(self, message, on_con_lost):
            self.message = message
            self.on_con_lost = on_con_lost

        def connection_made(self, transport):
            transport.write(self.message.encode())
            print('Data sent: {!r}'.format(self.message))

        def data_received(self, data):
            print('Data received: {!r}'.format(data.decode()))

        def connection_lost(self, exc):
            print('The server closed the connection')
            self.on_con_lost.set_result(True)


    async def main():
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()
        message = 'Hello World!'

        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost),
            '127.0.0.1', 8888)

        # Wait until the protocol signals that the connection
        # is lost and close the transport.
        try:
            await on_con_lost
        finally:
            transport.close()


    asyncio.run(main())

::: seealso
The `TCP echo client using streams <asyncio-tcp-echo-client-streams>`{.interpreted-text role="ref"} example uses the high-level `asyncio.open_connection`{.interpreted-text role="func"} function.
:::

### UDP Echo Server {#asyncio-udp-echo-server-protocol}

A UDP echo server, using the `loop.create_datagram_endpoint`{.interpreted-text role="meth"} method, sends back received data:

    import asyncio


    class EchoServerProtocol:
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            message = data.decode()
            print('Received %r from %s' % (message, addr))
            print('Send %r to %s' % (message, addr))
            self.transport.sendto(data, addr)


    async def main():
        print("Starting UDP server")

        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()

        # One protocol instance will be created to serve all
        # client requests.
        transport, protocol = await loop.create_datagram_endpoint(
            EchoServerProtocol,
            local_addr=('127.0.0.1', 9999))

        try:
            await asyncio.sleep(3600)  # Serve for 1 hour.
        finally:
            transport.close()


    asyncio.run(main())

### UDP Echo Client {#asyncio-udp-echo-client-protocol}

A UDP echo client, using the `loop.create_datagram_endpoint`{.interpreted-text role="meth"} method, sends data and closes the transport when it receives the answer:

    import asyncio


    class EchoClientProtocol:
        def __init__(self, message, on_con_lost):
            self.message = message
            self.on_con_lost = on_con_lost
            self.transport = None

        def connection_made(self, transport):
            self.transport = transport
            print('Send:', self.message)
            self.transport.sendto(self.message.encode())

        def datagram_received(self, data, addr):
            print("Received:", data.decode())

            print("Close the socket")
            self.transport.close()

        def error_received(self, exc):
            print('Error received:', exc)

        def connection_lost(self, exc):
            print("Connection closed")
            self.on_con_lost.set_result(True)


    async def main():
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()
        message = "Hello World!"

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: EchoClientProtocol(message, on_con_lost),
            remote_addr=('127.0.0.1', 9999))

        try:
            await on_con_lost
        finally:
            transport.close()


    asyncio.run(main())

### Connecting Existing Sockets {#asyncio_example_create_connection}

Wait until a socket receives data using the `loop.create_connection`{.interpreted-text role="meth"} method with a protocol:

    import asyncio
    import socket


    class MyProtocol(asyncio.Protocol):

        def __init__(self, on_con_lost):
            self.transport = None
            self.on_con_lost = on_con_lost

        def connection_made(self, transport):
            self.transport = transport

        def data_received(self, data):
            print("Received:", data.decode())

            # We are done: close the transport;
            # connection_lost() will be called automatically.
            self.transport.close()

        def connection_lost(self, exc):
            # The socket has been closed
            self.on_con_lost.set_result(True)


    async def main():
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        # Create a pair of connected sockets
        rsock, wsock = socket.socketpair()

        # Register the socket to wait for data.
        transport, protocol = await loop.create_connection(
            lambda: MyProtocol(on_con_lost), sock=rsock)

        # Simulate the reception of data from the network.
        loop.call_soon(wsock.send, 'abc'.encode())

        try:
            await protocol.on_con_lost
        finally:
            transport.close()
            wsock.close()

    asyncio.run(main())

::: seealso
The `watch a file descriptor for read events
<asyncio_example_watch_fd>`{.interpreted-text role="ref"} example uses the low-level `loop.add_reader`{.interpreted-text role="meth"} method to register an FD.

The `register an open socket to wait for data using streams
<asyncio_example_create_connection-streams>`{.interpreted-text role="ref"} example uses high-level streams created by the `open_connection`{.interpreted-text role="func"} function in a coroutine.
:::

### loop.subprocess_exec() and SubprocessProtocol {#asyncio_example_subprocess_proto}

An example of a subprocess protocol used to get the output of a subprocess and to wait for the subprocess exit.

The subprocess is created by the `loop.subprocess_exec`{.interpreted-text role="meth"} method:

    import asyncio
    import sys

    class DateProtocol(asyncio.SubprocessProtocol):
        def __init__(self, exit_future):
            self.exit_future = exit_future
            self.output = bytearray()
            self.pipe_closed = False
            self.exited = False

        def pipe_connection_lost(self, fd, exc):
            self.pipe_closed = True
            self.check_for_exit()

        def pipe_data_received(self, fd, data):
            self.output.extend(data)

        def process_exited(self):
            self.exited = True
            # process_exited() method can be called before
            # pipe_connection_lost() method: wait until both methods are
            # called.
            self.check_for_exit()

        def check_for_exit(self):
            if self.pipe_closed and self.exited:
                self.exit_future.set_result(True)

    async def get_date():
        # Get a reference to the event loop as we plan to use
        # low-level APIs.
        loop = asyncio.get_running_loop()

        code = 'import datetime; print(datetime.datetime.now())'
        exit_future = asyncio.Future(loop=loop)

        # Create the subprocess controlled by DateProtocol;
        # redirect the standard output into a pipe.
        transport, protocol = await loop.subprocess_exec(
            lambda: DateProtocol(exit_future),
            sys.executable, '-c', code,
            stdin=None, stderr=None)

        # Wait for the subprocess exit using the process_exited()
        # method of the protocol.
        await exit_future

        # Close the stdout pipe.
        transport.close()

        # Read the output which was collected by the
        # pipe_data_received() method of the protocol.
        data = bytes(protocol.output)
        return data.decode('ascii').rstrip()

    date = asyncio.run(get_date())
    print(f"Current date: {date}")

See also the `same example <asyncio_example_create_subprocess_exec>`{.interpreted-text role="ref"} written using high-level APIs.
