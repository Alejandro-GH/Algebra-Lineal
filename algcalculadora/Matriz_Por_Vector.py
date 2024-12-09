from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit, QMessageBox, QMenu, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import re
import sys

class MatrizPorVectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Matriz por Vector")
        self.setStyleSheet("background-color: black; color: white;")

        self.layout_principal = QVBoxLayout()

        # Título
        titulo = QLabel("Matriz por Vector.")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(titulo)

        # Sección de agregar
        agregar_layout = QHBoxLayout()
        self.agregar_button = QPushButton("Agregar ▼")
        self.agregar_button.setStyleSheet(self.button_style())
        menu_agregar = QMenu(self)
        menu_agregar.setStyleSheet("background-color: #222; color: white;")

        accion_agregar_fila = menu_agregar.addAction("Agregar Fila")
        accion_agregar_fila.triggered.connect(self.agregar_fila)

        accion_agregar_columna = menu_agregar.addAction("Agregar Columna")
        accion_agregar_columna.triggered.connect(self.agregar_columna)

        self.agregar_button.setMenu(menu_agregar)
        agregar_layout.addWidget(self.agregar_button)

        self.layout_principal.addLayout(agregar_layout)

        # Entrada de matriz
        matriz_layout = QHBoxLayout()
        matriz_layout.addWidget(QLabel("Matriz:"))
        self.matriz_input = QLineEdit()
        self.matriz_input.setStyleSheet(self.input_style())
        matriz_layout.addWidget(self.matriz_input)
        limpiar_button = QPushButton("Limpiar")
        limpiar_button.clicked.connect(self.limpiar_campos)
        limpiar_button.setStyleSheet(self.button_style())
        matriz_layout.addWidget(limpiar_button)

        self.layout_principal.addLayout(matriz_layout)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular Resultado")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_matriz)
        botones_layout.addWidget(calcular_button)

        self.layout_principal.addLayout(botones_layout)

        # Área de resultados
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

    def agregar_fila(self):
        self.resultado_text.setText("Agregar fila no implementado en este contexto.")

    def agregar_columna(self):
        self.resultado_text.setText("Agregar columna no implementado en este contexto.")

    def calcular_matriz(self):
        try:
            texto_matriz = self.matriz_input.text()
            if not texto_matriz.strip():
                raise ValueError("La matriz no puede estar vacía.")
            matriz = self.convertir_a_matriz(texto_matriz)
            self.resultado_text.setText(f"Resultado: {matriz}")
        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def convertir_a_matriz(self, texto):
        texto = re.sub(r'[^\d,;.-]', '', texto)
        try:
            matriz = [list(map(float, fila.split(','))) for fila in texto.split(';')]
        except ValueError:
            raise ValueError("Formato inválido. Use ';' para separar filas y ',' para separar elementos.")
        return matriz

    def limpiar_campos(self):
        self.matriz_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MatrizPorVectorWidget()
    ventana.show()
    sys.exit(app.exec_())