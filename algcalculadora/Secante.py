import sympy as sp
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np
import sys


class SecanteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Secante")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Sección de entradas
        entrada_layout = QGridLayout()
        entrada_layout.setContentsMargins(10, 10, 10, 10)
        entrada_layout.setSpacing(10)

        self.funcion_label = QLabel("Función f(x):")
        self.funcion_input = QLineEdit()
        self.funcion_input.setStyleSheet(self.input_style())
        self.funcion_input.setPlaceholderText("Ej: x**3 - 2*x + 1")

        self.x0_label = QLabel("x0 (Punto Inicial):")
        self.x0_input = QLineEdit()
        self.x0_input.setStyleSheet(self.input_style())
        self.x0_input.setPlaceholderText("Ej: 0.5")

        self.x1_label = QLabel("x1 (Punto Inicial):")
        self.x1_input = QLineEdit()
        self.x1_input.setStyleSheet(self.input_style())
        self.x1_input.setPlaceholderText("Ej: 1.0")

        self.tolerancia_label = QLabel("Tolerancia:")
        self.tolerancia_input = QLineEdit()
        self.tolerancia_input.setStyleSheet(self.input_style())
        self.tolerancia_input.setText("0.0001")

        self.iteraciones_label = QLabel("Iteraciones:")
        self.iteraciones_input = QLineEdit()
        self.iteraciones_input.setStyleSheet(self.input_style())
        self.iteraciones_input.setText("100")

        entrada_layout.addWidget(self.funcion_label, 0, 0)
        entrada_layout.addWidget(self.funcion_input, 0, 1)
        entrada_layout.addWidget(self.x0_label, 1, 0)
        entrada_layout.addWidget(self.x0_input, 1, 1)
        entrada_layout.addWidget(self.x1_label, 2, 0)
        entrada_layout.addWidget(self.x1_input, 2, 1)
        entrada_layout.addWidget(self.tolerancia_label, 3, 0)
        entrada_layout.addWidget(self.tolerancia_input, 3, 1)
        entrada_layout.addWidget(self.iteraciones_label, 4, 0)
        entrada_layout.addWidget(self.iteraciones_input, 4, 1)

        self.layout_principal.addLayout(entrada_layout)

        # Botones principales
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular)
        botones_layout.addWidget(calcular_button)

        graficar_button = QPushButton("Graficar")
        graficar_button.setStyleSheet(self.button_style())
        graficar_button.clicked.connect(self.graficar)
        botones_layout.addWidget(graficar_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar)
        botones_layout.addWidget(limpiar_button)

        self.layout_principal.addLayout(botones_layout)

        # Área de resultados
        resultado_label = QLabel("Resultado:")
        resultado_label.setFont(QFont("Arial", 12))
        resultado_label.setAlignment(Qt.AlignLeft)
        self.layout_principal.addWidget(resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet(self.text_edit_style())
        self.layout_principal.addWidget(self.resultado_text)

        self.setLayout(self.layout_principal)

    def input_style(self):
        return """
            QLineEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #00bfff;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #444;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """

    def text_edit_style(self):
        return """
            QTextEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def calcular(self):
        try:
            funcion = self.funcion_input.text().strip()
            x0 = float(self.x0_input.text())
            x1 = float(self.x1_input.text())
            tol = float(self.tolerancia_input.text())
            max_iter = int(self.iteraciones_input.text())

            x = sp.symbols('x')
            f = sp.lambdify(x, sp.sympify(funcion), 'math')

            raiz, pasos = self.metodo_secante(f, x0, x1, tol, max_iter)
            resultado = f"Raíz encontrada: {raiz:.6f}\n\nPasos del cálculo:\n"
            resultado += "\n".join(pasos)
            self.resultado_text.setText(resultado)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en el cálculo: {str(e)}")

    def metodo_secante(self, f, x0, x1, tol, max_iter):
        pasos = []
        for i in range(1, max_iter + 1):
            f_x0 = f(x0)
            f_x1 = f(x1)
            if abs(f_x1 - f_x0) < 1e-12:
                raise ValueError("División por cero en el cálculo de la secante.")

            x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
            pasos.append(f"Iter {i}: x0={x0:.6f}, x1={x1:.6f}, x2={x2:.6f}")

            if abs(x2 - x1) < tol:
                return x2, pasos

            x0, x1 = x1, x2

        raise ValueError("No se encontró raíz dentro del número máximo de iteraciones.")

    def graficar(self):
        try:
            funcion = self.funcion_input.text().strip()
            x0 = float(self.x0_input.text())
            x1 = float(self.x1_input.text())

            x = sp.symbols('x')
            expr_funcion = sp.sympify(funcion)
            f = sp.lambdify(x, expr_funcion, 'math')

            x_vals = np.linspace(x0 - 2, x1 + 2, 1000)
            y_vals = [f(val) for val in x_vals]

            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f"f(x) = {funcion}")
            plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
            plt.scatter([x0, x1], [f(x0), f(x1)], color='blue', label="Puntos iniciales")
            plt.title("Método de la Secante")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

    def limpiar(self):
        self.funcion_input.clear()
        self.x0_input.clear()
        self.x1_input.clear()
        self.tolerancia_input.setText("0.0001")
        self.iteraciones_input.setText("100")
        self.resultado_text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = SecanteApp()
    ventana.show()
    sys.exit(app.exec_())
