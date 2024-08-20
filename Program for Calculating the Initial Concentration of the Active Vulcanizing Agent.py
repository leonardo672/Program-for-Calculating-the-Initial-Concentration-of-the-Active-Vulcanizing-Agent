import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import matplotlib.pyplot as plt
import numpy as np
def calculate_initial_DAV_concentration(xi, S8, Ac, Ak_theta, R_eta, k_constants):
    """
    Функция для расчета начальной концентрации ДАВ.
    Аргументы:
    xi: константа
    S8: начальная концентрация серы (моль/кг)
    Ac: начальная концентрация ускорителя (моль/кг)
    Ak_theta: начальная концентрация активатора (оксида цинка) (моль/кг)
    R_eta: начальная концентрация макрорадикала каучука (моль/кг)
    k_constants: список констант скоростей реакций
    Возвращает:
    Начальная концентрация ДАВ
    """
    # Размерности констант скоростей реакций
    k_dimensions = [1, 1, 1, 1, 1, 1, 1, 1, 1]  # [c-1, c-1, c-1, c-1, c-1, c-1, c-1, c-1, c-1]
    # Проверка соответствия размерностей
    if len(k_constants) != len(k_dimensions):
        raise ValueError("Количество констант скоростей реакций не совпадает с количеством размерностей")
    # Расчет произведения
    product = xi * S8 * Ac * Ak_theta * R_eta
    # Умножение на константы скоростей реакций
    for i in range(len(k_constants)):
        product *= k_constants[i] ** k_dimensions[i]
    return product
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчет начальной концентрации ДАВ")
        self.layout = QVBoxLayout()
        self.xi_edit = QLineEdit()
        self.S8_edit = QLineEdit()
        self.Ac_edit = QLineEdit()
        self.Ak_theta_edit = QLineEdit()
        self.R_eta_edit = QLineEdit()
        self.k_constants_edits = [QLineEdit() for _ in range(9)]
        self.layout.addWidget(QLabel("Введите значение константы xi:"))
        self.layout.addWidget(self.xi_edit)
        self.layout.addWidget(QLabel("Введите начальную концентрацию серы (моль/кг):"))
        self.layout.addWidget(self.S8_edit)
        self.layout.addWidget(QLabel("Введите начальную концентрацию ускорителя (моль/кг):"))
        self.layout.addWidget(self.Ac_edit)
        self.layout.addWidget(QLabel("Введите начальную концентрацию активатора (оксида цинка) (моль/кг):"))
        self.layout.addWidget(self.Ak_theta_edit)
        self.layout.addWidget(QLabel("Введите начальную концентрацию макрорадикала каучука (моль/кг):"))
        self.layout.addWidget(self.R_eta_edit)
        self.layout.addWidget(QLabel("Введите значения констант скоростей реакций (k1-k9):"))
        for i in range(9):
            self.layout.addWidget(self.k_constants_edits[i])
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)
    def calculate(self):
        xi = float(self.xi_edit.text())
        S8 = float(self.S8_edit.text())
        Ac = float(self.Ac_edit.text())
        Ak_theta = float(self.Ak_theta_edit.text())
        R_eta = float(self.R_eta_edit.text())
        k_constants = [float(edit.text()) for edit in self.k_constants_edits]
        try:
            initial_DAV_concentration = calculate_initial_DAV_concentration(xi, S8, Ac, Ak_theta, R_eta, k_constants)
            self.result_label.setText(f"Начальная концентрация ДАВ составляет: {initial_DAV_concentration} моль/кг")
            # Визуализация данных
            k_indices = np.arange(1, 10)
            plt.bar(k_indices, k_constants)
            plt.xlabel('Константы скоростей реакций (k1-k9)')
            plt.ylabel('Значения')
            plt.title('Значения констант скоростей реакций')
            plt.show()
        except ValueError as e:
            self.result_label.setText(str(e))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
