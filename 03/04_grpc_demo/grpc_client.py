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
