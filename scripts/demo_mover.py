import math, time, rclpy
from geometry_msgs.msg import Twist

# turtle2를 일정한 S자 경로로 움직여 gaze_turtle이 따라가게 하는 데모용 스크립트
rclpy.init()
n = rclpy.create_node('demo_mover')
pub = n.create_publisher(Twist, '/turtle2/cmd_vel', 10)
t0 = time.time()
while time.time() - t0 < 16:
    t = time.time() - t0
    m = Twist()
    m.linear.x = 1.7
    m.angular.z = 0.85 + 0.15 * math.sin(t * 0.8)
    pub.publish(m)
    time.sleep(0.05)
pub.publish(Twist())
n.destroy_node()
rclpy.shutdown()
