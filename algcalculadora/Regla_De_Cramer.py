import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ReglaCramerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Configura la interfaz gráfica."""
        self.setWindowTitle("Regla de Cramer.")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Sección de entradas
        entrada_layout = QGridLayout()
        entrada_layout.setContentsMargins(10, 10, 10, 10)
        entrada_layout.setSpacing(10)

        matriz_label = QLabel("Matriz:")
        matriz_label.setFont(QFont("Arial", 12))
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz (filas separadas por ';', elementos por ',')")
        self.matriz_input.setStyleSheet(self.input_style())

        vector_label = QLabel("Vector:")
        vector_label.setFont(QFont("Arial", 12))
        self.vector_input = QLineEdit()
        self.vector_input.setPlaceholderText("Introduce vector (elementos separados por ',')")
        self.vector_input.setStyleSheet(self.input_style())

        entrada_layout.addWidget(matriz_label, 0, 0)
        entrada_layout.addWidget(self.matriz_input, 0, 1)
        entrada_layout.addWidget(vector_label, 1, 0)
        entrada_layout.addWidget(self.vector_input, 1, 1)

        self.layout_principal.addLayout(entrada_layout)

        # Teclado virtual
        self.teclado_layout = QGridLayout()
        self.teclas = [
            ['(', ')', 'f(x)', 'x', 'sin', 'cos', 'tan'],
            ['7', '8', '9', 'log', 'ln', 'π'],
            ['4', '5', '6', '/', '√'],
            ['1', '2', '3', '*', '^'],
            ['0', '.', '=', '+', '-']
        ]
        for i, fila in enumerate(self.teclas):
            for j, tecla in enumerate(fila):
                boton = QPushButton(tecla)
                boton.setStyleSheet(self.button_style())
                boton.clicked.connect(lambda checked, t=tecla: self.insertar_texto(t))
                self.teclado_layout.addWidget(boton, i, j)

        self.layout_principal.addLayout(self.teclado_layout)

        # Botones principales
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_cramer)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar_campos)
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
        """Estilo para los campos de entrada."""
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
        """Estilo para los botones."""
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
        """Estilo para el QTextEdit."""
        return """
            QTextEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def insertar_texto(self, texto):
        """Inserta texto en el campo de entrada activo."""
        cursor_pos = self.matriz_input.cursorPosition()
        current_text = self.matriz_input.text()
        self.matriz_input.setText(current_text[:cursor_pos] + texto + current_text[cursor_pos:])
        self.matriz_input.setCursorPosition(cursor_pos + len(texto))

    def calcular_cramer(self):
        """Calcula las soluciones de un sistema de ecuaciones lineales utilizando la regla de Cramer."""
        try:
            matriz = self.leer_matriz(self.matriz_input.text())
            vector = self.leer_vector(self.vector_input.text())

            if len(matriz) != len(vector):
                raise ValueError("El número de filas de la matriz debe coincidir con el tamaño del vector.")

            det_A = self.determinante(matriz)
            if abs(det_A) < 1e-9:
                raise ValueError("La matriz es singular (determinante = 0) y no tiene solución única.")

            soluciones = self.regla_cramer(matriz, vector, det_A)

            resultado = "Soluciones del sistema:\n\n"
            for i, sol in enumerate(soluciones):
                resultado += f"x{i+1} = {sol:.6f}\n"
            resultado += f"\nDeterminante principal |A| = {det_A:.6f}"

            self.resultado_text.setText(resultado)

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def leer_matriz(self, texto):
        return [[float(num) for num in fila.split(',')] for fila in texto.split(';')]

    def leer_vector(self, texto):
        return [float(num) for num in texto.split(',')]

    def regla_cramer(self, matriz, vector, det_A):
        soluciones = []
        for i in range(len(matriz)):
            matriz_reemplazada = [fila[:] for fila in matriz]
            for j in range(len(matriz)):
                matriz_reemplazada[j][i] = vector[j]
            soluciones.append(self.determinante(matriz_reemplazada) / det_A)
        return soluciones

    def determinante(self, matriz):
        if len(matriz) == 1:
            return matriz[0][0]
        if len(matriz) == 2:
            return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        det = 0
        for c in range(len(matriz)):
            sub_matriz = [fila[:c] + fila[c+1:] for fila in matriz[1:]]
            det += ((-1) ** c) * matriz[0][c] * self.determinante(sub_matriz)
        return det

    def limpiar_campos(self):
        self.matriz_input.clear()
        self.vector_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = ReglaCramerWidget()
    ventana.show()
    sys.exit(app.exec_())