import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def wrap(a):
    # 각도를 -pi ~ pi 범위로 맞춤
    return math.atan2(math.sin(a), math.cos(a))


class GazeTurtle(Node):
    def __init__(self):
        super().__init__('gaze_turtle')
        self.declare_parameter('gain', 3.0)       # 얼마나 세게 돌아볼지
        self.declare_parameter('max_speed', 3.0)  # 최대 회전 속도
        self.declare_parameter('smooth', 0.15)    # 0~1, 작을수록 느긋하게 반응
        self.me = None
        self.target = None
        self.w = 0.0  # 현재 회전 속도 (부드럽게 바뀜)
        self.create_subscription(Pose, '/turtle1/pose', self.on_me, 10)
        self.create_subscription(Pose, '/turtle2/pose', self.on_target, 10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_timer(0.05, self.tick)
        self.get_logger().info('gaze_turtle 시작: turtle2를 바라봅니다')

    def on_me(self, msg):
        self.me = msg

    def on_target(self, msg):
        self.target = msg

    def approach_speed(self, dist):
        if dist < 1.0:
            return 0.0                  # 도착: 멈춤
        elif dist < 2.0:
            return (dist - 1.0) * 2.0   # 가까워짐: 서서히 감속
        else:
            return 2.0                  # 멂: 평소 속도

    def tick(self):
        if self.me is None or self.target is None:
            return
        gain = self.get_parameter('gain').value
        max_speed = self.get_parameter('max_speed').value
        smooth = self.get_parameter('smooth').value

        # 1) 목표 방향 계산
        want = math.atan2(self.target.y - self.me.y, self.target.x - self.me.x)
        err = wrap(want - self.me.theta)
        # 2) 오차에 비례한 회전 명령 (최대값 제한)
        w_cmd = max(-max_speed, min(max_speed, gain * err))
        # 3) 바로 바꾸지 않고 조금씩 따라감 -> 부드러운 가속/감속
        self.w += smooth * (w_cmd - self.w)
        # 4) 거리 계산 -> 가까울수록 감속, 가까우면 정지
        dist = math.hypot(self.target.x - self.me.x, self.target.y - self.me.y)

        msg = Twist()
        msg.angular.z = self.w
        msg.linear.x = self.approach_speed(dist)
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = GazeTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
