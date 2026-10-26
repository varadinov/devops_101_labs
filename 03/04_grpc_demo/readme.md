# Setup

This demo uses [uv](https://docs.astral.sh/uv/) to manage the Python environment and dependencies.

Install uv if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

# Define the gRPC Service
Create a file named demo.proto that defines the service and the messages for the GetTime and EchoMessage methods.

```protobuf
syntax = "proto3";

package demo;

// The demo service definition.
service DemoService {
  // Get current server time
  rpc GetTime (Empty) returns (TimeResponse);
  
  // Echo the message back
  rpc EchoMessage (EchoRequest) returns (EchoResponse);
}

// Empty message (used for GetTime)
message Empty {}

// Response message containing the server time
message TimeResponse {
  string current_time = 1;
}

// Request message for echo
message EchoRequest {
  string message = 1;
}

// Response message for echo
message EchoResponse {
  string message = 1;
}
```

# Generate gRPC Python Code
This will generate two files: demo_pb2.py and demo_pb2_grpc.py, which will contain the necessary classes for implementing the gRPC client and server.

```bash
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. demo.proto
```

# Implement the gRPC Server 
Create file grpc_server.py

```python
from concurrent import futures
from datetime import datetime

import demo_pb2
import demo_pb2_grpc
import grpc

# The implementation of the gRPC service
class DemoServiceServicer(demo_pb2_grpc.DemoServiceServicer):
    def GetTime(self, request, context):
        # Return the current server time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return demo_pb2.TimeResponse(current_time=current_time)

    def EchoMessage(self, request, context):
        # Echo the received message back
        return demo_pb2.EchoResponse(message=request.message)

# Initialize and run the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    demo_pb2_grpc.add_DemoServiceServicer_to_server(DemoServiceServicer(), server)
    
    # Bind the server to port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

```

# Implement the gRPC Client 
Create file grpc_client.py

```python
import demo_pb2
import demo_pb2_grpc
import grpc

# Connect to the gRPC server
def run():
    # Create a channel to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client) for the DemoService
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        
        # Call GetTime RPC
        response = stub.GetTime(demo_pb2.Empty())
        print("Server Time:", response.current_time)

        # Call EchoMessage RPC
        message = "Hello from gRPC Client!"
        response = stub.EchoMessage(demo_pb2.EchoRequest(message=message))
        print("Echoed Message:", response.message)

if __name__ == '__main__':
    run()

```

# Run server

```bash
uv run python grpc_server.py
```

# Run client

```bash
uv run python grpc_client.py
```