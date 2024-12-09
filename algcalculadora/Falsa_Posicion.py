from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit, QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from sympy import symbols, lambdify, sympify
import numpy as np
import matplotlib.pyplot as plt

class TecladoWidget(QWidget):
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
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
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
                border-radius: 15px;
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

class FalsaPosicionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Falsa Posición")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Entradas
        layout_entradas = QGridLayout()
        layout_entradas.addWidget(QLabel("Función f(x):"), 0, 0, alignment=Qt.AlignRight)
        self.funcion_input = QLineEdit()
        self.funcion_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.funcion_input, 0, 1)

        layout_entradas.addWidget(QLabel("a (Extremo Izquierdo):"), 1, 0, alignment=Qt.AlignRight)
        self.a_input = QLineEdit()
        self.a_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.a_input, 1, 1)

        layout_entradas.addWidget(QLabel("b (Extremo Derecho):"), 2, 0, alignment=Qt.AlignRight)
        self.b_input = QLineEdit()
        self.b_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.b_input, 2, 1)

        layout_entradas.addWidget(QLabel("Tolerancia:"), 3, 0, alignment=Qt.AlignRight)
        self.tolerancia_input = QLineEdit()
        self.tolerancia_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.tolerancia_input, 3, 1)

        layout_entradas.addWidget(QLabel("Iteraciones:"), 4, 0, alignment=Qt.AlignRight)
        self.iteraciones_input = QLineEdit()
        self.iteraciones_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.iteraciones_input, 4, 1)

        self.layout_principal.addLayout(layout_entradas)

        # Botones
        layout_botones = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
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

        self.layout_principal.addLayout(layout_botones)

        # Resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet("""
            QTextEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.layout_principal.addWidget(self.resultado_text)

        # Teclado
        self.teclado = TecladoWidget(self.funcion_input)
        self.layout_principal.addWidget(self.teclado)

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
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """

    def calcular(self):
        try:
            funcion = sympify(self.funcion_input.text())
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            tol = float(self.tolerancia_input.text())
            max_iter = int(self.iteraciones_input.text())

            x = symbols('x')
            f = lambdify(x, funcion)

            if f(a) * f(b) > 0:
                raise ValueError("No hay cambio de signo en el intervalo dado.")

            resultado, pasos = self.falsa_posicion(funcion, a, b, tol, max_iter)
            self.resultado_text.setText(f"Raíz: {resultado}\n\n" + "\n".join(pasos))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    @staticmethod
    def falsa_posicion(funcion, a, b, tol, max_iter):
        x = symbols('x')
        f = lambdify(x, funcion)
        pasos = []

        for i in range(max_iter):
            c = (a * f(b) - b * f(a)) / (f(b) - f(a))
            pasos.append(f"Iteración {i + 1}: a={a:.6f}, b={b:.6f}, c={c:.6f}, f(c)={f(c):.6f}")

            if abs(f(c)) < tol:
                return c, pasos

            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

        raise ValueError("No se encontró raíz en el número máximo de iteraciones.")

    def graficar(self):
        try:
            funcion = sympify(self.funcion_input.text())
            a = float(self.a_input.text())
            b = float(self.b_input.text())

            x = symbols('x')
            f = lambdify(x, funcion)

            x_vals = np.linspace(a - 2, b + 2, 500)
            y_vals = [f(val) for val in x_vals]

            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f"f(x) = {self.funcion_input.text()}")
            plt.axhline(0, color='red', linestyle='--', linewidth=0.8, label="y=0")
            plt.axvline(a, color='green', linestyle='--', linewidth=0.8, label=f"a = {a}")
            plt.axvline(b, color='blue', linestyle='--', linewidth=0.8, label=f"b = {b}")
            plt.title("Método de Falsa Posición - Gráfica de la función")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.grid(True)
            plt.legend()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

    def limpiar(self):
        self.funcion_input.clear()
        self.a_input.clear()
        self.b_input.clear()
        self.tolerancia_input.clear()
        self.iteraciones_input.clear()
        self.resultado_text.clear()


if __name__ == "__main__":
    app = QApplication([])
    ventana = FalsaPosicionApp()
    ventana.show()
    app.exec_()