import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Int32


class NodeB(Node):

    def __init__(self):
        super().__init__('nodeB')
        
        # Subscreve o tópico do seu sobrenome (mesmo nome usado no nodeA)
        self.subscription = self.create_subscription(
            Int32,
            '/lourenco',
            self.listener_callback,
            10
        )
        
        # Publisher para o tópico final exigido
        self.publisher_ = self.create_publisher(Float32, '/kthfs/result', 10)
        
        # Divisor q = 0.15 conforme especificação do exercício
        self.q = 0.15

    def listener_callback(self, msg):
        # Divide o valor recebido k por q (0.15)
        result_value = float(msg.data) / self.q
        
        # Cria a mensagem de saída
        result_msg = Float32()
        result_msg.data = result_value
        
        # Publica o resultado no tópico /kthfs/result
        self.publisher_.publish(result_msg)
        
        self.get_logger().info(
            f'Recebido: {msg.data} | Publicado em /kthfs/result: {result_value:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node_b = NodeB()
    try:
        rclpy.spin(node_b)
    except KeyboardInterrupt:
        pass
    finally:
        node_b.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
