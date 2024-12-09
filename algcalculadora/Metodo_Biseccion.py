import sys
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, sin, cos, tan, log, ln, pi
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QApplication
)
from PyQt5.QtCore import Qt


class BiseccionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Bisección")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Entradas
        layout_entradas = QGridLayout()
        layout_entradas.addWidget(QLabel("Función:"), 0, 0)
        self.funcion_input = QLineEdit()
        self.funcion_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.funcion_input, 0, 1)

        layout_entradas.addWidget(QLabel("a:"), 1, 0)
        self.a_input = QLineEdit()
        self.a_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.a_input, 1, 1)

        layout_entradas.addWidget(QLabel("b:"), 2, 0)
        self.b_input = QLineEdit()
        self.b_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.b_input, 2, 1)

        layout_entradas.addWidget(QLabel("Iteraciones:"), 3, 0)
        self.iteraciones_input = QLineEdit()
        self.iteraciones_input.setStyleSheet(self.input_style())
        layout_entradas.addWidget(self.iteraciones_input, 3, 1)

        self.layout_principal.addLayout(layout_entradas)

        # Botones
        layout_botones = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_biseccion)
        layout_botones.addWidget(calcular_button)

        graficar_button = QPushButton("Graficar")
        graficar_button.setStyleSheet(self.button_style())
        graficar_button.clicked.connect(self.graficar_funcion)
        layout_botones.addWidget(graficar_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar_campos)
        layout_botones.addWidget(limpiar_button)

        self.layout_principal.addLayout(layout_botones)

        # Resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet(self.resultado_text_style())
        self.layout_principal.addWidget(self.resultado_text)

        # Teclado Virtual
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

    def resultado_text_style(self):
        return """
            QTextEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def calcular_biseccion(self):
        try:
            # Leer y validar entradas
            funcion_str = self.funcion_input.text()
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            iteraciones = int(self.iteraciones_input.text())

            if a >= b:
                raise ValueError("El valor de 'a' debe ser menor que el valor de 'b'.")

            # Definir la función con sympy
            x = symbols('x')
            funcion = sympify(funcion_str, locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": ln, "pi": pi})

            # Método de Bisección con proceso detallado
            proceso = self.biseccion(funcion, a, b, iteraciones)

            # Mostrar proceso detallado
            self.resultado_text.setText("\n".join(proceso))
        except ValueError as e:
            self.resultado_text.setText(f"Error: {str(e)}")
        except Exception as e:
            self.resultado_text.setText(f"Error inesperado: {str(e)}")

    def biseccion(self, funcion, a, b, iteraciones):
        x = symbols('x')
        proceso = [f"Iteración inicial: a={a}, b={b}"]
        for i in range(1, iteraciones + 1):
            c = (a + b) / 2
            f_a = funcion.evalf(subs={x: a})
            f_b = funcion.evalf(subs={x: b})
            f_c = funcion.evalf(subs={x: c})

            proceso.append(f"Iteración {i}:")
            proceso.append(f"    a={a}, f(a)={f_a}")
            proceso.append(f"    b={b}, f(b)={f_b}")
            proceso.append(f"    c={c}, f(c)={f_c}")

            if f_c == 0 or abs(b - a) < 1e-6:
                proceso.append(f"Raíz encontrada: c={c}")
                return proceso

            if f_a * f_c < 0:
                b = c
            else:
                a = c

        proceso.append(f"Raíz aproximada después de {iteraciones} iteraciones: c={c}")
        return proceso

    def graficar_funcion(self):
        try:
            # Leer entradas
            funcion_str = self.funcion_input.text()
            a = float(self.a_input.text())
            b = float(self.b_input.text())

            # Validar entradas
            if a >= b:
                raise ValueError("El valor de 'a' debe ser menor que el valor de 'b'.")

            # Procesar función
            x = symbols('x')
            funcion = sympify(funcion_str, locals={"sin": sin, "cos": cos, "tan": tan, "log": log, "ln": ln, "pi": pi})

            # Generar datos para graficar
            x_vals = np.linspace(a, b, 500)
            f = np.vectorize(lambda val: funcion.evalf(subs={x: val}))
            y_vals = f(x_vals)

            # Graficar
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}", color="blue")
            plt.axhline(0, color="red", linestyle="--", linewidth=1)
            plt.title("Gráfica de la función")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.grid(True)
            plt.legend()
            plt.show()
        except Exception as e:
            self.resultado_text.setText(f"Error al graficar: {str(e)}")

    def limpiar_campos(self):
        self.funcion_input.clear()
        self.a_input.clear()
        self.b_input.clear()
        self.iteraciones_input.clear()
        self.resultado_text.clear()


class TecladoWidget(QWidget):
    """Teclado virtual para la entrada de funciones."""
    def __init__(self, input_target):
        super().__init__()
        self.input_target = input_target
        self.teclas = [
            ['(', ')', 'sin', 'cos', 'tan'],
            ['7', '8', '9', 'log', 'ln'],
            ['4', '5', '6', '/', '√'],
            ['1', '2', '3', '*', '^'],
            ['0', '.', 'pi', '+', '-']
        ]
        self.initUI()

    def initUI(self):
        self.layout_teclado = QGridLayout()
        for i, fila in enumerate(self.teclas):
            for j, tecla in enumerate(fila):
                boton = QPushButton(tecla)
                boton.setStyleSheet("""
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
                """)
                boton.clicked.connect(lambda _, t=tecla: self.insertar_tecla(t))
                self.layout_teclado.addWidget(boton, i, j)
        self.setLayout(self.layout_teclado)

    def insertar_tecla(self, tecla):
        """Inserta el valor de la tecla en el campo de entrada."""
        cursor = self.input_target.cursorPosition()
        texto = self.input_target.text()
        nuevo_texto = texto[:cursor] + tecla + texto[cursor:]
        self.input_target.setText(nuevo_texto)
        self.input_target.setCursorPosition(cursor + len(tecla))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BiseccionWidget()
    ventana.show()
    sys.exit(app.exec_())