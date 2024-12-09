import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class MultiplicacionMatricesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Multiplicación de Matrices.")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Entradas para las matrices
        matrices_layout = QHBoxLayout()
        layout_matriz_a = QVBoxLayout()
        layout_matriz_b = QVBoxLayout()

        matriz_a_label = QLabel("Matriz A:")
        matriz_a_label.setFont(QFont("Arial", 12))
        self.matriz_a_input = QLineEdit()
        self.matriz_a_input.setPlaceholderText("Introduce Matriz A (filas separadas por ';', elementos por ',')")
        self.matriz_a_input.setStyleSheet(self.input_style())
        layout_matriz_a.addWidget(matriz_a_label)
        layout_matriz_a.addWidget(self.matriz_a_input)

        matriz_b_label = QLabel("Matriz B:")
        matriz_b_label.setFont(QFont("Arial", 12))
        self.matriz_b_input = QLineEdit()
        self.matriz_b_input.setPlaceholderText("Introduce Matriz B (filas separadas por ';', elementos por ',')")
        self.matriz_b_input.setStyleSheet(self.input_style())
        layout_matriz_b.addWidget(matriz_b_label)
        layout_matriz_b.addWidget(self.matriz_b_input)

        matrices_layout.addLayout(layout_matriz_a)
        matrices_layout.addLayout(layout_matriz_b)
        self.layout_principal.addLayout(matrices_layout)

        # Botones principales
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_multiplicacion)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(limpiar_button)
        self.layout_principal.addLayout(botones_layout)

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

        # Área de resultados
        resultado_layout = QVBoxLayout()
        resultado_label = QLabel("Resultado:")
        resultado_label.setFont(QFont("Arial", 12))
        resultado_label.setAlignment(Qt.AlignCenter)
        resultado_layout.addWidget(resultado_label)

        resultados_matrices_layout = QHBoxLayout()
        self.resultado_a_text = QTextEdit()
        self.resultado_a_text.setReadOnly(True)
        self.resultado_a_text.setStyleSheet(self.text_edit_style())
        self.resultado_a_text.setPlaceholderText("Matriz A")

        self.resultado_b_text = QTextEdit()
        self.resultado_b_text.setReadOnly(True)
        self.resultado_b_text.setStyleSheet(self.text_edit_style())
        self.resultado_b_text.setPlaceholderText("Matriz B")

        self.resultado_ab_text = QTextEdit()
        self.resultado_ab_text.setReadOnly(True)
        self.resultado_ab_text.setStyleSheet(self.text_edit_style())
        self.resultado_ab_text.setPlaceholderText("Matriz A * B")

        resultados_matrices_layout.addWidget(self.resultado_a_text)
        resultados_matrices_layout.addWidget(self.resultado_b_text)
        resultados_matrices_layout.addWidget(self.resultado_ab_text)
        resultado_layout.addLayout(resultados_matrices_layout)

        self.layout_principal.addLayout(resultado_layout)

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
        """Estilo para los QTextEdit."""
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
        """Inserta el texto en el campo de entrada activo."""
        cursor_pos = self.matriz_a_input.cursorPosition()
        current_text = self.matriz_a_input.text()
        self.matriz_a_input.setText(
            current_text[:cursor_pos] + texto + current_text[cursor_pos:]
        )
        self.matriz_a_input.setCursorPosition(cursor_pos + len(texto))

    def calcular_multiplicacion(self):
        try:
            # Leer las matrices desde las entradas
            matriz_a_str = self.matriz_a_input.text()
            matriz_b_str = self.matriz_b_input.text()

            if not matriz_a_str.strip() or not matriz_b_str.strip():
                raise ValueError("Ambas matrices deben ser ingresadas.")

            # Convertir las matrices de texto a listas de listas
            matriz_a = [self.convertir_fila(fila.split(',')) for fila in matriz_a_str.split(';')]
            matriz_b = [self.convertir_fila(fila.split(',')) for fila in matriz_b_str.split(';')]

            # Verificar compatibilidad
            if len(matriz_a[0]) != len(matriz_b):
                raise ValueError("Columnas de A deben coincidir con filas de B.")

            # Multiplicar matrices
            resultado_ab = self.multiplicar_matrices(matriz_a, matriz_b)

            # Mostrar matrices y resultado
            self.resultado_a_text.setText(self.formatear_matriz(matriz_a))
            self.resultado_b_text.setText(self.formatear_matriz(matriz_b))
            self.resultado_ab_text.setText(self.formatear_matriz(resultado_ab))

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def convertir_fila(self, fila):
        """Convierte los elementos de la fila a float o int."""
        return [float(elemento) if '.' in elemento else int(elemento) for elemento in fila]

    def multiplicar_matrices(self, A, B):
        """Realiza la multiplicación de dos matrices."""
        filas_a = len(A)
        columnas_b = len(B[0])
        columnas_a = len(A[0])

        resultado = [[sum(A[i][k] * B[k][j] for k in range(columnas_a)) for j in range(columnas_b)] for i in range(filas_a)]
        return resultado

    def formatear_matriz(self, matriz):
        """Convierte una matriz en una cadena formateada."""
        return "\n".join(["\t".join(f"{val:.2f}" if isinstance(val, float) else f"{val}" for val in fila) for fila in matriz])

    def limpiar_campos(self):
        """Limpia las entradas y los resultados."""
        self.matriz_a_input.clear()
        self.matriz_b_input.clear()
        self.resultado_a_text.clear()
        self.resultado_b_text.clear()
        self.resultado_ab_text.clear()

    def mostrar_error(self, mensaje):
        """Muestra un cuadro de diálogo con un mensaje de error."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MultiplicacionMatricesApp()
    ventana.show()
    sys.exit(app.exec_())
