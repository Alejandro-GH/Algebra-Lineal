import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from sympy import Matrix, symbols, Eq, solve
from PyQt5.QtWidgets import QApplication


class AutoCloseLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        """Permite autocompletar ciertos caracteres como paréntesis."""
        super().keyPressEvent(event)
        cursor_pos = self.cursorPosition()
        text = self.text()

        if event.key() == Qt.Key_ParenLeft:
            self.setText(text[:cursor_pos] + ')' + text[cursor_pos:])
            self.setCursorPosition(cursor_pos)
        elif event.key() == Qt.Key_BracketLeft:
            self.setText(text[:cursor_pos] + ']' + text[cursor_pos:])
            self.setCursorPosition(cursor_pos)
        elif event.key() == Qt.Key_BraceLeft:
            self.setText(text[:cursor_pos] + '}' + text[cursor_pos:])
            self.setCursorPosition(cursor_pos)


class GaussJordanWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Configura la interfaz gráfica."""
        self.setWindowTitle("Método de Gauss-Jordan")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Sección de entrada para la matriz aumentada
        layout_matriz = QHBoxLayout()
        matriz_label = QLabel("Matriz Aumentada:")
        matriz_label.setFont(QFont("Arial", 12))
        self.matriz_input = AutoCloseLineEdit()
        self.matriz_input.setPlaceholderText(
            "Introduce la matriz aumentada (filas separadas por ';', elementos por ',')"
        )
        self.matriz_input.setStyleSheet(self.input_style())
        layout_matriz.addWidget(matriz_label)
        layout_matriz.addWidget(self.matriz_input)
        self.layout_principal.addLayout(layout_matriz)

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
        botones_layout = QVBoxLayout()
        calcular_button = QPushButton("Calcular Gauss - Jordan.")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_gauss_jordan)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(limpiar_button)

        self.layout_principal.addLayout(botones_layout)

        # Área de resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier", 12))
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

    def insertar_texto(self, texto):
        """Inserta el texto en el campo de entrada activo."""
        cursor_pos = self.matriz_input.cursorPosition()
        current_text = self.matriz_input.text()
        self.matriz_input.setText(
            current_text[:cursor_pos] + texto + current_text[cursor_pos:]
        )
        self.matriz_input.setCursorPosition(cursor_pos + len(texto))

    def limpiar_campos(self):
        """Limpia las entradas y los resultados."""
        self.matriz_input.clear()
        self.resultado_text.clear()

    def calcular_gauss_jordan(self):
        """Calcula la solución del sistema utilizando Gauss-Jordan."""
        try:
            matriz_aumentada = self.matriz_input.text()
            if not matriz_aumentada.strip():
                raise ValueError("La matriz aumentada no puede estar vacía.")

            # Convertir la entrada en una lista de listas
            matriz_aumentada = [
                list(map(float, fila.split(',')))
                for fila in matriz_aumentada.split(';')
            ]

            # Separar la matriz de coeficientes (A) y el vector independiente (b)
            a = [fila[:-1] for fila in matriz_aumentada]
            b = [fila[-1] for fila in matriz_aumentada]

            # Resolver usando Gauss-Jordan
            pasos, solucion = self.eliminacion_gauss_jordan(a, b)

            # Mostrar los pasos y la solución
            resultado = f"{pasos}\n\nSolución: {solucion}"
            self.resultado_text.setText(resultado)

        except ValueError as ve:
            self.mostrar_error(str(ve))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def eliminacion_gauss_jordan(self, a, b):
        """Realiza el método de Gauss-Jordan para resolver el sistema."""
        n = len(b)
        pasos = ""
        m = Matrix([row + [b[i]] for i, row in enumerate(a)])

        # Realizar eliminación de Gauss-Jordan
        m, pivot_columns = m.rref()

        # Verificar si el sistema es inconsistente (matrices singulares)
        if any(m.row(pivot_columns[-1])[pivot_columns[-1]] == 0):
            return "Sistema sin solución o con infinitas soluciones.", ""

        # Generar el sistema de ecuaciones
        x = symbols(f'x1:{n+1}')
        ecuaciones = [Eq(sum(m[i, j] * x[j] for j in range(n)), m[i, -1]) for i in range(n)]
        solucion = solve(ecuaciones, x)

        # Formatear los pasos y la solución
        if not solucion:
            pasos += "El sistema tiene infinitas soluciones.\n\n"
        else:
            pasos += "Solución única.\n\n"

        pasos += "\nMatriz final:\n"
        pasos += self.formatear_matriz(m.tolist())

        return pasos, solucion

    def formatear_matriz(self, m):
        """Convierte la matriz en una cadena formateada para mostrarla como tabla."""
        filas = []
        for fila in m:
            filas.append(" | ".join(f"{val:.2f}" if isinstance(val, float) else f"{val}" for val in fila))
        return "\n".join(filas)

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en un cuadro de diálogo."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = GaussJordanWidget()
    ventana.show()
    sys.exit(app.exec_())