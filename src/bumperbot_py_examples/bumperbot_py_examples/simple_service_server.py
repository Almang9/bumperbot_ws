import rclpy
from rclpy.node import Node

from bumperbot_msgs.srv import AddTwoInts


class SimpleServiceServer(Node):
    def __init__(self):
        super().__init__("simple_service_server")
        self.service = self.create_service(
            AddTwoInts, "add_two_ints", self.serviceCallback
        )
        self.get_logger().info("Service 'simple_service' is ready.")

    def serviceCallback(self, request, response):
        self.get_logger().info(
            "New Request received a: %d, b: %d" % (request.a, request.b)
        )
        response.sum = request.a + request.b
        self.get_logger().info("Returning sum: %d" % response.sum)
        return response


def main() -> None:
    rclpy.init()
    simple_service_server = SimpleServiceServer()
    rclpy.spin(simple_service_server)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
