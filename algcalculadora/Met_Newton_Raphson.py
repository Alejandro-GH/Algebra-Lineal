from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from sympy import symbols, diff, lambdify, sympify
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication

class TecladoWidget(QWidget):
    """Teclado virtual para la entrada de funciones."""
    def __init__(self, input_target):
        super().__init__()
        self.input_target = input_target
        self.teclas = [
            ['(', ')', 'f(x)', 'x', 'sin', 'cos', 'tan'],
            ['7', '8', '9', 'log', 'ln', 'π'],
            ['4', '5', '6', '/', '√'],
            ['1', '2', '3', '*', '^'],
            ['0', '.', '=', '+', '-']
        ]
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        for i, fila in enumerate(self.teclas):
            for j, tecla in enumerate(fila):
                boton = QPushButton(tecla)
                boton.setStyleSheet(self.boton_style())
                boton.clicked.connect(lambda checked, t=tecla: self.insertar_texto(t))
                layout.addWidget(boton, i, j)
        self.setLayout(layout)

    def insertar_texto(self, texto):
        if self.input_target:
            cursor_position = self.input_target.cursorPosition()
            current_text = self.input_target.text()
            new_text = (
                current_text[:cursor_position]
                + texto
                + current_text[cursor_position:]
            )
            self.input_target.setText(new_text)
            self.input_target.setCursorPosition(cursor_position + len(texto))

    def boton_style(self):
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

class NewtonRaphsonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Newton-Raphson")
        self.setStyleSheet("background-color: black; color: white;")
        layout_principal = QVBoxLayout()

        # Entradas
        layout_entradas = QGridLayout()
        layout_entradas.addWidget(QLabel("Función f(x):"), 0, 0)
        self.funcion_input = QLineEdit()
        self.funcion_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.funcion_input, 0, 1)

        layout_entradas.addWidget(QLabel("x0 (Valor Inicial):"), 1, 0)
        self.x0_input = QLineEdit()
        self.x0_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.x0_input, 1, 1)

        layout_entradas.addWidget(QLabel("Tolerancia:"), 2, 0)
        self.tolerancia_input = QLineEdit()
        self.tolerancia_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.tolerancia_input, 2, 1)

        layout_entradas.addWidget(QLabel("Iteraciones:"), 3, 0)
        self.iteraciones_input = QLineEdit()
        self.iteraciones_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.iteraciones_input, 3, 1)

        layout_principal.addLayout(layout_entradas)

        # Botones
        layout_botones = QHBoxLayout()
        calcular_button = QPushButton("Calcular Resultado")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular)
        layout_botones.addWidget(calcular_button)

        graficar_button = QPushButton("Graficar")
        graficar_button.setStyleSheet(self.button_style())
        graficar_button.clicked.connect(self.graficar)
        layout_botones.addWidget(graficar_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar)
        layout_botones.addWidget(limpiar_button)

        layout_principal.addLayout(layout_botones)

        # Resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet(self.resultado_style())
        layout_principal.addWidget(self.resultado_text)

        # Teclado virtual
        self.teclado = TecladoWidget(self.funcion_input)
        layout_principal.addWidget(self.teclado)

        self.setLayout(layout_principal)

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
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """

    def resultado_style(self):
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
            func = sympify(self.funcion_input.text())
            xi = float(self.x0_input.text())
            tol = float(self.tolerancia_input.text())
            max_iter = int(self.iteraciones_input.text())

            resultado, procedimiento = self.newton_raphson(func, xi, tol, max_iter)
            if resultado is not None:
                self.resultado_text.setText(f"Raíz: {resultado:.6f}\n\n" + "\n".join(procedimiento))
            else:
                self.resultado_text.setText("No se encontró una raíz.\n\n" + "\n".join(procedimiento))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    @staticmethod
    def newton_raphson(func, xi, tol, max_iter):
        x = symbols('x')
        f = lambdify(x, func)
        f_prime = lambdify(x, diff(func, x))
        procedimiento = []

        for i in range(max_iter):
            fx = f(xi)
            f_prime_xi = f_prime(xi)
            if f_prime_xi == 0:
                return None, ["Derivada nula. Proceso detenido."]
            xi1 = xi - fx / f_prime_xi
            ea = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')
            procedimiento.append(f"Iteración {i + 1}: xi={xi:.6f}, xi+1={xi1:.6f}, ea={ea:.6f}%")
            if ea < tol:
                return xi1, procedimiento
            xi = xi1

        return None, ["No se alcanzó la convergencia."]

    def graficar(self):
        try:
            func = sympify(self.funcion_input.text())
            xi = float(self.x0_input.text())

            x = symbols('x')
            f = lambdify(x, func)

            # Generar puntos para la gráfica
            x_vals = np.linspace(xi - 10, xi + 10, 500)
            y_vals = [f(val) for val in x_vals]

            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f"f(x) = {self.funcion_input.text()}")
            plt.axhline(0, color='red', linestyle='--', linewidth=0.8, label="y=0")
            plt.axvline(xi, color='blue', linestyle='--', linewidth=0.8, label=f"x0 = {xi}")
            plt.title("Método de Newton-Raphson - Gráfica de la función")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.grid(True)
            plt.legend()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

    def limpiar(self):
        self.funcion_input.clear()
        self.x0_input.clear()
        self.tolerancia_input.clear()
        self.iteraciones_input.clear()
        self.resultado_text.clear()


if __name__ == "__main__":
    app = QApplication([])
    ventana = NewtonRaphsonWidget()
    ventana.show()
    app.exec_()