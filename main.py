import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSlider, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush



def compute_servo_angles(x, y, L1, L2):
    r = math.sqrt(x**2 + y**2)
    
    if r == 0:
        return None, None

    cos_alpha_term = (L1**2 + r**2 - L2**2) / (2 * L1 * r)
    cos_beta_term = (L1**2 + L2**2 - r**2) / (2 * L1 * L2)

    if abs(cos_alpha_term) > 1 or abs(cos_beta_term) > 1:
        return None, None

    alpha = math.atan2(y, x) - math.acos(cos_alpha_term)
    beta = math.pi - math.acos(cos_beta_term)



    return alpha, beta


def map_angle_to_servo(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

def angle_to_pwm(angle):
    print(angle)
    return map_angle_to_servo(angle, 0, 180, 0, 100)



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Servo Control with PyQt'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 600, 700)
        
        layout = QVBoxLayout()

        self.x_slider = QSlider(Qt.Horizontal, self)
        self.y_slider = QSlider(Qt.Horizontal, self)
        self.x_slider.setRange(-14, 14)  # Adjust as needed
        self.y_slider.setRange(-14, 14)

        self.label = QLabel(self)

        # Graphics Scene & View
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 400)  # Adjust as needed
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.arm_line1 = self.scene.addLine(0, 0, 0, 0, QPen(Qt.black, 2))
        self.arm_line2 = self.scene.addLine(0, 0, 0, 0, QPen(Qt.red, 2))
        
        self.x_slider.valueChanged.connect(self.update_display)
        self.y_slider.valueChanged.connect(self.update_display)
        
        layout.addWidget(self.view)
        layout.addWidget(QLabel('X Position'))
        layout.addWidget(self.x_slider)
        layout.addWidget(QLabel('Y Position'))
        layout.addWidget(self.y_slider)
        layout.addWidget(self.label)

        self.alpha_label = QLabel(self)
        self.beta_label = QLabel(self)
        layout.addWidget(self.alpha_label)
        layout.addWidget(self.beta_label)

        self.pwm_alpha_label = QLabel(self)
        self.pwm_beta_label = QLabel(self)

        layout.addWidget(self.pwm_alpha_label)
        layout.addWidget(self.pwm_beta_label)


        self.target_point = self.scene.addEllipse(0, 0, 5, 5, QPen(Qt.green), QBrush(Qt.green))

        self.setLayout(layout)


    def update_display(self):
        x = self.x_slider.value()
        y = self.y_slider.value()
        L1, L2 = 7, 7
        alpha, beta = compute_servo_angles(x, y, L1, L2)
        
        if alpha is None or beta is None:
            self.label.setText("Unreachable position")
            return

        # Compute joint and end effector positions
        joint_x = L1 * math.cos(alpha)
        joint_y = L1 * math.sin(alpha)
        end_x = joint_x + L2 * math.cos(alpha + beta)
        end_y = joint_y + L2 * math.sin(alpha + beta)


        # Update lines
        self.arm_line1.setLine(250, 200, 250 + joint_x*10, 200 - joint_y*10)
        self.arm_line2.setLine(250 + joint_x*10, 200 - joint_y*10, 250 + end_x*10, 200 - end_y*10)

        # Update target point position
        self.target_point.setPos(250 + x*10 - 2.5, 200 - y*10 - 2.5)



        pwm_alpha = angle_to_pwm(alpha)
        pwm_beta = angle_to_pwm(beta)

        #self.pwm_alpha_label.setText(f"PWM Alpha (Joint 1): {pwm_alpha:.0f}")
        #self.pwm_beta_label.setText(f"PWM Beta (Joint 2): {pwm_beta:.0f}")
        self.alpha_label.setText(f"Alpha (Joint 1): {math.degrees(alpha):.2f}°")
        self.beta_label.setText(f"Beta (Joint 2): {math.degrees(beta):.2f}°")

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

