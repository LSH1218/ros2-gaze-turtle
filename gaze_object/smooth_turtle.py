import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SmoothTurtle(Node):
    def __init__(self):
        super().__init__('smooth_turtle')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.t = 0.0
        self.dt = 0.05  # 20Hz: 1초에 20번 명령
        self.timer = self.create_timer(self.dt, self.tick)
        self.get_logger().info('smooth_turtle 시작')

    def tick(self):
        self.t += self.dt
        msg = Twist()
        # 4초 주기로 0 -> 1 -> 0 (숨 쉬듯 빨라졌다 느려짐)
        breath = 0.5 - 0.5 * math.cos(2 * math.pi * self.t / 4.0)
        msg.linear.x = 0.5 + 1.5 * breath
        # 8초 주기로 좌우 회전 (S자)
        msg.angular.z = 1.2 * math.sin(2 * math.pi * self.t / 8.0)
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = SmoothTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
