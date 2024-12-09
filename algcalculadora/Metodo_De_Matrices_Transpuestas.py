import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class MatricesTranspuestasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Matriz Transpuesta.")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Sección de entrada para la matriz
        layout_matriz = QHBoxLayout()
        matriz_label = QLabel("Tamaño de la matriz (n x n):")
        matriz_label.setFont(QFont("Arial", 12))
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText(
            "Introduce la matriz (filas separadas por ';', elementos por ',')"
        )
        self.matriz_input.setStyleSheet(self.input_style())
        layout_matriz.addWidget(matriz_label)
        layout_matriz.addWidget(self.matriz_input)
        self.layout_principal.addLayout(layout_matriz)

        # Botones principales
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular Transpuesta")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_transpuesta)
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
        resultado_label = QLabel("Resultado:")
        resultado_label.setFont(QFont("Arial", 12))
        resultado_label.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(resultado_label)

        resultado_layout = QHBoxLayout()

        self.resultado_original = QTextEdit()
        self.resultado_original.setReadOnly(True)
        self.resultado_original.setFont(QFont("Courier", 10))
        self.resultado_original.setStyleSheet(self.text_edit_style())
        resultado_layout.addWidget(QLabel("Matriz Original:"))
        resultado_layout.addWidget(self.resultado_original)

        self.resultado_transpuesta = QTextEdit()
        self.resultado_transpuesta.setReadOnly(True)
        self.resultado_transpuesta.setFont(QFont("Courier", 10))
        self.resultado_transpuesta.setStyleSheet(self.text_edit_style())
        resultado_layout.addWidget(QLabel("Matriz Transpuesta:"))
        resultado_layout.addWidget(self.resultado_transpuesta)

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
        cursor_pos = self.matriz_input.cursorPosition()
        current_text = self.matriz_input.text()
        self.matriz_input.setText(
            current_text[:cursor_pos] + texto + current_text[cursor_pos:]
        )
        self.matriz_input.setCursorPosition(cursor_pos + len(texto))

    def calcular_transpuesta(self):
        try:
            # Leer la matriz desde la entrada y convertirla a una lista de listas
            texto_matriz = self.matriz_input.text()
            if not texto_matriz.strip():
                raise ValueError("La entrada está vacía. Por favor, introduce una matriz.")

            matriz = [list(map(float, fila.split(','))) for fila in texto_matriz.split(';')]

            # Verificar que todas las filas tengan el mismo número de columnas
            num_columnas = len(matriz[0])
            if not all(len(fila) == num_columnas for fila in matriz):
                raise ValueError("Todas las filas de la matriz deben tener el mismo número de columnas.")

            # Calcular la transpuesta
            matriz_transpuesta = self.transponer_matriz(matriz)

            # Mostrar la matriz original y su transpuesta
            self.resultado_original.setText(self.formatear_matriz(matriz))
            self.resultado_transpuesta.setText(self.formatear_matriz(matriz_transpuesta))

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def transponer_matriz(self, matriz):
        """Devuelve la transpuesta de la matriz dada."""
        return [list(fila) for fila in zip(*matriz)]

    def formatear_matriz(self, matriz):
        """Convierte una matriz en una cadena formateada para mostrarla."""
        return "\n".join(["\t".join(f"{valor:.2f}" for valor in fila) for fila in matriz])

    def limpiar_campos(self):
        """Limpia la entrada de matriz y los resultados."""
        self.matriz_input.clear()
        self.resultado_original.clear()
        self.resultado_transpuesta.clear()

    def mostrar_error(self, mensaje):
        """Muestra un cuadro de diálogo con un mensaje de error."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MatricesTranspuestasWidget()
    ventana.show()
    sys.exit(app.exec_())