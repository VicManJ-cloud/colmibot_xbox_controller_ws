import rclpy
from rclpy.node import Node
#Joy es el mensaje que publica joy_node con el estado del control
from sensor_msgs.msg import Joy
#Twist es el mensaje que entiende turtlesim
from geometry_msgs.msg import Twist


#indices de los ejes, confirmados con ros2 topic echo /joy
STICK_IZQ_X = 0     #horizontal, izquierda +1.0 derecha -1.0
STICK_IZQ_Y = 1     #vertical, arriba +1.0 abajo -1.0
STICK_DER_X = 2
STICK_DER_Y = 3
GATILLO_RT = 4      #en reposo 1.0, presionado -1.0
GATILLO_LT = 5
CRUZ_X = 6          #solo da -1.0, 0.0 o 1.0
CRUZ_Y = 7

#indices de los botones, confirmados con ros2 topic echo /joy
BOTON_A = 0
BOTON_B = 1
BOTON_X = 3
BOTON_Y = 4
BOTON_LB = 6
BOTON_RB = 7


class JoyTurtleController(Node):
    def __init__(self):
        super().__init__('joy_turtle_controller')

        #escucha el estado del control que publica joy_node
        self.subscription_ = self.create_subscription(Joy, '/joy', self.joy_callback, 10)

        #publica al topico que mueve la tortuga
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        #velocidades maximas en modo normal
        self.vel_lineal_max = 2.0
        self.vel_angular_max = 2.0

        #multiplicadores de los modos
        self.factor_turbo = 2.0
        self.factor_preciso = 0.4

        self.get_logger().info('Controlador listo, manten RB presionado para mover')

    def joy_callback(self, msg):
        #se ejecuta cada vez que joy_node publica el estado del control
        cmd = Twist()

        #B es el paro de emergencia y va primero para que funcione
        #aunque no se este presionando el boton de hombre muerto
        if msg.buttons[BOTON_B] == 1:
            self.publisher_.publish(cmd)
            self.get_logger().info('PARO DE EMERGENCIA')
            return

        #RB es el hombre muerto: si no esta presionado se manda un Twist
        #vacio, que es velocidad cero, y la tortuga se detiene
        if msg.buttons[BOTON_RB] != 1:
            self.publisher_.publish(cmd)
            return

        #LB sube la velocidad y A la baja, si se presionan los dos gana
        #el modo preciso porque la condicion se evalua primero
        if msg.buttons[BOTON_A] == 1:
            factor = self.factor_preciso
        elif msg.buttons[BOTON_LB] == 1:
            factor = self.factor_turbo
        else:
            factor = 1.0

        #joy_node ya entrega los ejes de -1.0 a 1.0 con zona muerta
        #aplicada, y los signos coinciden con la convencion de ROS:
        #arriba es +1.0 y avanzar es linear.x positivo, izquierda es
        #+1.0 y girar a la izquierda es angular.z positivo
        cmd.linear.x = msg.axes[STICK_IZQ_Y] * self.vel_lineal_max * factor
        cmd.angular.z = msg.axes[STICK_IZQ_X] * self.vel_angular_max * factor

        self.publisher_.publish(cmd)
        self.get_logger().info(f'lineal = {cmd.linear.x:.2f} | angular = {cmd.angular.z:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = JoyTurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
