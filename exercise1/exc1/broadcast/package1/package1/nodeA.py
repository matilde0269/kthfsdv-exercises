import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class NodeA(Node):

    def __init__(self):
        super().__init__('nodeA')
        self.publisher_ = self.create_publisher(Int32, '/lourenco', 10)
        
        # 20 Hz = período de 0.05 segundos (1.0 / 20.0)
        self.timer_period = 0.05
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.k = 4  # Valor inicial k > 0
        self.n = 4  # Incremento n = 4

    def timer_callback(self):
        msg = Int32()
        msg.data = self.k
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando em /lourenco: {msg.data}')
        self.k += self.n


def main(args=None):
    rclpy.init(args=args)
    node_a = NodeA()
    try:
        rclpy.spin(node_a)
    except KeyboardInterrupt:
        pass
    finally:
        node_a.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
