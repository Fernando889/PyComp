::: currentmodule
asyncio
:::

# Low-level API Index

This page lists all low-level asyncio APIs.

## Obtaining the Event Loop

  ----------------------------------------------------------- -------------------------------------------------------------------------
  `asyncio.get_running_loop`{.interpreted-text role="func"}   The **preferred** function to get the running event loop.

  `asyncio.get_event_loop`{.interpreted-text role="func"}     Get an event loop instance (running or current via the current policy).

  `asyncio.set_event_loop`{.interpreted-text role="func"}     Set the event loop as current via the current policy.

  `asyncio.new_event_loop`{.interpreted-text role="func"}     Create a new event loop.
  ----------------------------------------------------------- -------------------------------------------------------------------------

**Examples**

- `Using asyncio.get_running_loop() <asyncio_example_future>`{.interpreted-text role="ref"}.

## Event Loop Methods

See also the main documentation section about the `asyncio-event-loop-methods`{.interpreted-text role="ref"}.

**Lifecycle**

  ------------------------------------------------------------------ ---------------------------------------------
  `loop.run_until_complete`{.interpreted-text role="meth"}           Run a Future/Task/awaitable until complete.

  `loop.run_forever`{.interpreted-text role="meth"}                  Run the event loop forever.

  `loop.stop`{.interpreted-text role="meth"}                         Stop the event loop.

  `loop.close`{.interpreted-text role="meth"}                        Close the event loop.

  `loop.is_running`{.interpreted-text role="meth"}                   Return `True` if the event loop is running.

  `loop.is_closed`{.interpreted-text role="meth"}                    Return `True` if the event loop is closed.

  `await` `loop.shutdown_asyncgens`{.interpreted-text role="meth"}   Close asynchronous generators.
  ------------------------------------------------------------------ ---------------------------------------------

**Debugging**

  ------------------------------------------------- -----------------------------------
  `loop.set_debug`{.interpreted-text role="meth"}   Enable or disable the debug mode.

  `loop.get_debug`{.interpreted-text role="meth"}   Get the current debug mode.
  ------------------------------------------------- -----------------------------------

**Scheduling Callbacks**

  ------------------------------------------------------------ ---------------------------------------------------------------------------
  `loop.call_soon`{.interpreted-text role="meth"}              Invoke a callback soon.

  `loop.call_soon_threadsafe`{.interpreted-text role="meth"}   A thread-safe variant of `loop.call_soon`{.interpreted-text role="meth"}.

  `loop.call_later`{.interpreted-text role="meth"}             Invoke a callback *after* the given time.

  `loop.call_at`{.interpreted-text role="meth"}                Invoke a callback *at* the given time.
  ------------------------------------------------------------ ---------------------------------------------------------------------------

**Thread/Interpreter/Process Pool**

  --------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------
  `await` `loop.run_in_executor`{.interpreted-text role="meth"}   Run a CPU-bound or other blocking function in a `concurrent.futures`{.interpreted-text role="mod"} executor.

  `loop.set_default_executor`{.interpreted-text role="meth"}      Set the default executor for `loop.run_in_executor`{.interpreted-text role="meth"}.
  --------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------

**Tasks and Futures**

  -------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------
  `loop.create_future`{.interpreted-text role="meth"}      Create a `Future`{.interpreted-text role="class"} object.

  `loop.create_task`{.interpreted-text role="meth"}        Schedule coroutine as a `Task`{.interpreted-text role="class"}.

  `loop.set_task_factory`{.interpreted-text role="meth"}   Set a factory used by `loop.create_task`{.interpreted-text role="meth"} to create `Tasks <Task>`{.interpreted-text role="class"}.

  `loop.get_task_factory`{.interpreted-text role="meth"}   Get the factory `loop.create_task`{.interpreted-text role="meth"} uses to create `Tasks <Task>`{.interpreted-text role="class"}.
  -------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------

**DNS**

  ----------------------------------------------------------- ------------------------------------------------------------------------------
  `await` `loop.getaddrinfo`{.interpreted-text role="meth"}   Asynchronous version of `socket.getaddrinfo`{.interpreted-text role="meth"}.

  `await` `loop.getnameinfo`{.interpreted-text role="meth"}   Asynchronous version of `socket.getnameinfo`{.interpreted-text role="meth"}.
  ----------------------------------------------------------- ------------------------------------------------------------------------------

**Networking and IPC**

  ------------------------------------------------------------------------ ----------------------------------------------------------------------------------------------
  `await` `loop.create_connection`{.interpreted-text role="meth"}          Open a TCP connection.

  `await` `loop.create_server`{.interpreted-text role="meth"}              Create a TCP server.

  `await` `loop.create_unix_connection`{.interpreted-text role="meth"}     Open a Unix socket connection.

  `await` `loop.create_unix_server`{.interpreted-text role="meth"}         Create a Unix socket server.

  `await` `loop.connect_accepted_socket`{.interpreted-text role="meth"}    Wrap a `~socket.socket`{.interpreted-text role="class"} into a `(transport, protocol)` pair.

  `await` `loop.create_datagram_endpoint`{.interpreted-text role="meth"}   Open a datagram (UDP) connection.

  `await` `loop.sendfile`{.interpreted-text role="meth"}                   Send a file over a transport.

  `await` `loop.start_tls`{.interpreted-text role="meth"}                  Upgrade an existing connection to TLS.

  `await` `loop.connect_read_pipe`{.interpreted-text role="meth"}          Wrap a read end of a pipe into a `(transport, protocol)` pair.

  `await` `loop.connect_write_pipe`{.interpreted-text role="meth"}         Wrap a write end of a pipe into a `(transport, protocol)` pair.
  ------------------------------------------------------------------------ ----------------------------------------------------------------------------------------------

**Sockets**

  ------------------------------------------------------------------ ------------------------------------------------------------------------------------------------
  `await` `loop.sock_recv`{.interpreted-text role="meth"}            Receive data from the `~socket.socket`{.interpreted-text role="class"}.

  `await` `loop.sock_recv_into`{.interpreted-text role="meth"}       Receive data from the `~socket.socket`{.interpreted-text role="class"} into a buffer.

  `await` `loop.sock_recvfrom`{.interpreted-text role="meth"}        Receive a datagram from the `~socket.socket`{.interpreted-text role="class"}.

  `await` `loop.sock_recvfrom_into`{.interpreted-text role="meth"}   Receive a datagram from the `~socket.socket`{.interpreted-text role="class"} into a buffer.

  `await` `loop.sock_sendall`{.interpreted-text role="meth"}         Send data to the `~socket.socket`{.interpreted-text role="class"}.

  `await` `loop.sock_sendto`{.interpreted-text role="meth"}          Send a datagram via the `~socket.socket`{.interpreted-text role="class"} to the given address.

  `await` `loop.sock_connect`{.interpreted-text role="meth"}         Connect the `~socket.socket`{.interpreted-text role="class"}.

  `await` `loop.sock_accept`{.interpreted-text role="meth"}          Accept a `~socket.socket`{.interpreted-text role="class"} connection.

  `await` `loop.sock_sendfile`{.interpreted-text role="meth"}        Send a file over the `~socket.socket`{.interpreted-text role="class"}.

  `loop.add_reader`{.interpreted-text role="meth"}                   Start watching a file descriptor for read availability.

  `loop.remove_reader`{.interpreted-text role="meth"}                Stop watching a file descriptor for read availability.

  `loop.add_writer`{.interpreted-text role="meth"}                   Start watching a file descriptor for write availability.

  `loop.remove_writer`{.interpreted-text role="meth"}                Stop watching a file descriptor for write availability.
  ------------------------------------------------------------------ ------------------------------------------------------------------------------------------------

**Unix Signals**

  ------------------------------------------------------------- ----------------------------------------------------------------
  `loop.add_signal_handler`{.interpreted-text role="meth"}      Add a handler for a `signal`{.interpreted-text role="mod"}.

  `loop.remove_signal_handler`{.interpreted-text role="meth"}   Remove a handler for a `signal`{.interpreted-text role="mod"}.
  ------------------------------------------------------------- ----------------------------------------------------------------

**Subprocesses**

  -------------------------------------------------------- ------------------------------------------
  `loop.subprocess_exec`{.interpreted-text role="meth"}    Spawn a subprocess.

  `loop.subprocess_shell`{.interpreted-text role="meth"}   Spawn a subprocess from a shell command.
  -------------------------------------------------------- ------------------------------------------

**Error Handling**

  ----------------------------------------------------------------- -----------------------------------------------
  `loop.call_exception_handler`{.interpreted-text role="meth"}      Call the exception handler.

  `loop.set_exception_handler`{.interpreted-text role="meth"}       Set a new exception handler.

  `loop.get_exception_handler`{.interpreted-text role="meth"}       Get the current exception handler.

  `loop.default_exception_handler`{.interpreted-text role="meth"}   The default exception handler implementation.
  ----------------------------------------------------------------- -----------------------------------------------

**Examples**

- `Using asyncio.new_event_loop() and loop.run_forever()
  <asyncio_example_lowlevel_helloworld>`{.interpreted-text role="ref"}.
- `Using loop.call_later() <asyncio_example_call_later>`{.interpreted-text role="ref"}.
- Using `loop.create_connection()` to implement `an echo-client <asyncio_example_tcp_echo_client_protocol>`{.interpreted-text role="ref"}.
- Using `loop.create_connection()` to `connect a socket <asyncio_example_create_connection>`{.interpreted-text role="ref"}.
- `Using add_reader() to watch an FD for read events
  <asyncio_example_watch_fd>`{.interpreted-text role="ref"}.
- `Using loop.add_signal_handler() <asyncio_example_unix_signals>`{.interpreted-text role="ref"}.
- `Using loop.subprocess_exec() <asyncio_example_subprocess_proto>`{.interpreted-text role="ref"}.

## Transports

All transports implement the following methods:

  -------------------------------------------------------------------------------------------- ---------------------------------------------------------
  `transport.close() <BaseTransport.close>`{.interpreted-text role="meth"}                     Close the transport.

  `transport.is_closing() <BaseTransport.is_closing>`{.interpreted-text role="meth"}           Return `True` if the transport is closing or is closed.

  `transport.get_extra_info() <BaseTransport.get_extra_info>`{.interpreted-text role="meth"}   Request for information about the transport.

  `transport.set_protocol() <BaseTransport.set_protocol>`{.interpreted-text role="meth"}       Set a new protocol.

  `transport.get_protocol() <BaseTransport.get_protocol>`{.interpreted-text role="meth"}       Return the current protocol.
  -------------------------------------------------------------------------------------------- ---------------------------------------------------------

Transports that can receive data (TCP and Unix connections, pipes, etc). Returned from methods like `loop.create_connection`{.interpreted-text role="meth"}, `loop.create_unix_connection`{.interpreted-text role="meth"}, `loop.connect_read_pipe`{.interpreted-text role="meth"}, etc:

**Read Transports**

  -------------------------------------------------------------------------------------------- ----------------------------------------------
  `transport.is_reading() <ReadTransport.is_reading>`{.interpreted-text role="meth"}           Return `True` if the transport is receiving.

  `transport.pause_reading() <ReadTransport.pause_reading>`{.interpreted-text role="meth"}     Pause receiving.

  `transport.resume_reading() <ReadTransport.resume_reading>`{.interpreted-text role="meth"}   Resume receiving.
  -------------------------------------------------------------------------------------------- ----------------------------------------------

Transports that can Send data (TCP and Unix connections, pipes, etc). Returned from methods like `loop.create_connection`{.interpreted-text role="meth"}, `loop.create_unix_connection`{.interpreted-text role="meth"}, `loop.connect_write_pipe`{.interpreted-text role="meth"}, etc:

**Write Transports**

  ------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------
  `transport.write() <WriteTransport.write>`{.interpreted-text role="meth"}                   Write data to the transport.

  `transport.writelines() <WriteTransport.writelines>`{.interpreted-text role="meth"}         Write buffers to the transport.

  `transport.can_write_eof() <WriteTransport.can_write_eof>`{.interpreted-text role="meth"}   Return `True`{.interpreted-text role="const"} if the transport supports sending EOF.

  `transport.write_eof() <WriteTransport.write_eof>`{.interpreted-text role="meth"}           Close and send EOF after flushing buffered data.

  `transport.abort() <WriteTransport.abort>`{.interpreted-text role="meth"}                   Close the transport immediately.

  `transport.get_write_buffer_size()                                                          Return the current size of the output buffer.
  <WriteTransport.get_write_buffer_size>`{.interpreted-text role="meth"}                      

  `transport.get_write_buffer_limits()                                                        Return high and low water marks for write flow control.
  <WriteTransport.get_write_buffer_limits>`{.interpreted-text role="meth"}                    

  `transport.set_write_buffer_limits()                                                        Set new high and low water marks for write flow control.
  <WriteTransport.set_write_buffer_limits>`{.interpreted-text role="meth"}                    
  ------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------

Transports returned by `loop.create_datagram_endpoint`{.interpreted-text role="meth"}:

**Datagram Transports**

  -------------------------------------------------------------------------------- -----------------------------------
  `transport.sendto() <DatagramTransport.sendto>`{.interpreted-text role="meth"}   Send data to the remote peer.

  `transport.abort() <DatagramTransport.abort>`{.interpreted-text role="meth"}     Close the transport immediately.
  -------------------------------------------------------------------------------- -----------------------------------

Low-level transport abstraction over subprocesses. Returned by `loop.subprocess_exec`{.interpreted-text role="meth"} and `loop.subprocess_shell`{.interpreted-text role="meth"}:

**Subprocess Transports**

  -------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------
  `transport.get_pid() <SubprocessTransport.get_pid>`{.interpreted-text role="meth"}                 Return the subprocess process id.

  `transport.get_pipe_transport()                                                                    Return the transport for the requested communication pipe (*stdin*, *stdout*, or *stderr*).
  <SubprocessTransport.get_pipe_transport>`{.interpreted-text role="meth"}                           

  `transport.get_returncode() <SubprocessTransport.get_returncode>`{.interpreted-text role="meth"}   Return the subprocess return code.

  `transport.kill() <SubprocessTransport.kill>`{.interpreted-text role="meth"}                       Kill the subprocess.

  `transport.send_signal() <SubprocessTransport.send_signal>`{.interpreted-text role="meth"}         Send a signal to the subprocess.

  `transport.terminate() <SubprocessTransport.terminate>`{.interpreted-text role="meth"}             Stop the subprocess.

  `transport.close() <SubprocessTransport.close>`{.interpreted-text role="meth"}                     Kill the subprocess and close all pipes.
  -------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------

## Protocols

Protocol classes can implement the following **callback methods**:

  ---------------------------------------------------------------------------------------------- ----------------------------------------------------------------------
  `callback` `connection_made() <BaseProtocol.connection_made>`{.interpreted-text role="meth"}   Called when a connection is made.

  `callback` `connection_lost() <BaseProtocol.connection_lost>`{.interpreted-text role="meth"}   Called when the connection is lost or closed.

  `callback` `pause_writing() <BaseProtocol.pause_writing>`{.interpreted-text role="meth"}       Called when the transport\'s buffer goes over the high water mark.

  `callback` `resume_writing() <BaseProtocol.resume_writing>`{.interpreted-text role="meth"}     Called when the transport\'s buffer drains below the low water mark.
  ---------------------------------------------------------------------------------------------- ----------------------------------------------------------------------

**Streaming Protocols (TCP, Unix Sockets, Pipes)**

  -------------------------------------------------------------------------------------- ------------------------------------
  `callback` `data_received() <Protocol.data_received>`{.interpreted-text role="meth"}   Called when some data is received.

  `callback` `eof_received() <Protocol.eof_received>`{.interpreted-text role="meth"}     Called when an EOF is received.
  -------------------------------------------------------------------------------------- ------------------------------------

**Buffered Streaming Protocols**

  ------------------------------------------------------------------------------------------------ ------------------------------------------------------------
  `callback` `get_buffer() <BufferedProtocol.get_buffer>`{.interpreted-text role="meth"}           Called to allocate a new receive buffer.

  `callback` `buffer_updated() <BufferedProtocol.buffer_updated>`{.interpreted-text role="meth"}   Called when the buffer was updated with the received data.

  `callback` `eof_received() <BufferedProtocol.eof_received>`{.interpreted-text role="meth"}       Called when an EOF is received.
  ------------------------------------------------------------------------------------------------ ------------------------------------------------------------

**Datagram Protocols**

  ------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------------
  `callback` `datagram_received()                                                                  Called when a datagram is received.
  <DatagramProtocol.datagram_received>`{.interpreted-text role="meth"}                             

  `callback` `error_received() <DatagramProtocol.error_received>`{.interpreted-text role="meth"}   Called when a previous send or receive operation raises an `OSError`{.interpreted-text role="class"}.
  ------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------------

**Subprocess Protocols**

  -------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `callback` `~SubprocessProtocol.pipe_data_received`{.interpreted-text role="meth"}     Called when the child process writes data into its *stdout* or *stderr* pipe.

  `callback` `~SubprocessProtocol.pipe_connection_lost`{.interpreted-text role="meth"}   Called when one of the pipes communicating with the child process is closed.

  `callback` `process_exited()                                                           Called when the child process has exited. It can be called before `~SubprocessProtocol.pipe_data_received`{.interpreted-text role="meth"} and `~SubprocessProtocol.pipe_connection_lost`{.interpreted-text role="meth"} methods.
  <SubprocessProtocol.process_exited>`{.interpreted-text role="meth"}                    
  -------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Event Loop Policies

Policies is a low-level mechanism to alter the behavior of functions like `asyncio.get_event_loop`{.interpreted-text role="func"}. See also the main `policies section <asyncio-policies>`{.interpreted-text role="ref"} for more details.

**Accessing Policies**

  ---------------------------------------------------------------- -----------------------------------------
  `asyncio.get_event_loop_policy`{.interpreted-text role="meth"}   Return the current process-wide policy.

  `asyncio.set_event_loop_policy`{.interpreted-text role="meth"}   Set a new process-wide policy.

  `AbstractEventLoopPolicy`{.interpreted-text role="class"}        Base class for policy objects.
  ---------------------------------------------------------------- -----------------------------------------
