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
