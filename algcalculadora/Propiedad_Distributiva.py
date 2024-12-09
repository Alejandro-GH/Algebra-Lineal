import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class PropiedadDistributivaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Configura la interfaz gráfica."""
        self.setWindowTitle("Propiedad Distributiva.")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Entradas para las matrices y vectores
        entrada_layout = QGridLayout()
        entrada_layout.setContentsMargins(10, 10, 10, 10)
        entrada_layout.setSpacing(10)

        matriz_a_label = QLabel("Matriz A:")
        matriz_a_label.setFont(QFont("Arial", 12))
        self.matriz_a_input = QLineEdit()
        self.matriz_a_input.setPlaceholderText("Introduce Matriz A (filas separadas por ';', elementos por ',')")
        self.matriz_a_input.setStyleSheet(self.input_style())

        matriz_b_label = QLabel("Matriz B:")
        matriz_b_label.setFont(QFont("Arial", 12))
        self.matriz_b_input = QLineEdit()
        self.matriz_b_input.setPlaceholderText("Introduce Matriz B (filas separadas por ';', elementos por ',')")
        self.matriz_b_input.setStyleSheet(self.input_style())

        vector_u_label = QLabel("Vector u:")
        vector_u_label.setFont(QFont("Arial", 12))
        self.vector_u_input = QLineEdit()
        self.vector_u_input.setPlaceholderText("Introduce Vector u (elementos separados por ',')")
        self.vector_u_input.setStyleSheet(self.input_style())

        vector_v_label = QLabel("Vector v:")
        vector_v_label.setFont(QFont("Arial", 12))
        self.vector_v_input = QLineEdit()
        self.vector_v_input.setPlaceholderText("Introduce Vector v (elementos separados por ',')")
        self.vector_v_input.setStyleSheet(self.input_style())

        entrada_layout.addWidget(matriz_a_label, 0, 0)
        entrada_layout.addWidget(self.matriz_a_input, 0, 1)
        entrada_layout.addWidget(matriz_b_label, 1, 0)
        entrada_layout.addWidget(self.matriz_b_input, 1, 1)
        entrada_layout.addWidget(vector_u_label, 2, 0)
        entrada_layout.addWidget(self.vector_u_input, 2, 1)
        entrada_layout.addWidget(vector_v_label, 3, 0)
        entrada_layout.addWidget(self.vector_v_input, 3, 1)

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
        calcular_button.clicked.connect(self.calcular_distributiva)
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
        cursor_pos = self.matriz_a_input.cursorPosition()
        current_text = self.matriz_a_input.text()
        self.matriz_a_input.setText(current_text[:cursor_pos] + texto + current_text[cursor_pos:])
        self.matriz_a_input.setCursorPosition(cursor_pos + len(texto))

    def calcular_distributiva(self):
        """Calcula la propiedad distributiva."""
        try:
            matriz_str = self.matriz_a_input.text()
            vector_u_str = self.vector_u_input.text()
            vector_v_str = self.vector_v_input.text()

            if not matriz_str.strip() or not vector_u_str.strip() or not vector_v_str.strip():
                raise ValueError("Todos los campos deben estar completos.")

            matriz = [[float(num) for num in fila.split(',')] for fila in matriz_str.split(';')]
            u = [float(num) for num in vector_u_str.split(',')]
            v = [float(num) for num in vector_v_str.split(',')]

            if len(matriz[0]) != len(u) or len(u) != len(v):
                raise ValueError("Dimensiones incompatibles entre matriz y vectores.")

            suma_uv = self.sumar_vectores(u, v)
            resultado_a_uv = self.multiplicar_matriz_vector(matriz, suma_uv)

            resultado_au = self.multiplicar_matriz_vector(matriz, u)
            resultado_av = self.multiplicar_matriz_vector(matriz, v)
            resultado_au_av = self.sumar_vectores(resultado_au, resultado_av)

            es_distributivo = self.comparar_vectores(resultado_a_uv, resultado_au_av)

            resultados = (
                f"A(u + v): {resultado_a_uv}\n"
                f"Au + Av: {resultado_au_av}\n"
                f"Propiedad distributiva: {'Cumple' if es_distributivo else 'No cumple'}"
            )
            self.resultado_text.setText(resultados)
        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def limpiar_campos(self):
        self.matriz_a_input.clear()
        self.vector_u_input.clear()
        self.vector_v_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def sumar_vectores(self, u, v):
        return [u[i] + v[i] for i in range(len(u))]

    def comparar_vectores(self, vec1, vec2, tolerancia=1e-9):
        return all(abs(a - b) < tolerancia for a, b in zip(vec1, vec2))

    def multiplicar_matriz_vector(self, matriz, vector):
        return [sum(fila[j] * vector[j] for j in range(len(vector))) for fila in matriz]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PropiedadDistributivaWidget()
    ventana.show()
    sys.exit(app.exec_())