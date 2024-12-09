from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMenu,
    QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fractions import Fraction

def matriz_identidad(n):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]

def formatear_matriz(matriz):
    """Convierte una matriz en una cadena formateada para mostrarla."""
    return "\n".join(["\t".join(f"{el!s:>8}" for el in fila) for fila in matriz])

def gauss_jordan(matriz, resultado_text):
    n = len(matriz)
    identidad = matriz_identidad(n)
    resultado_text.append("Proceso de eliminación Gauss-Jordan:")
    for i in range(n):
        if matriz[i][i] == 0:
            raise ValueError("La matriz es singular y no tiene inversa.")
        pivote = matriz[i][i]
        for j in range(n):
            matriz[i][j] /= pivote
            identidad[i][j] /= pivote
        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(n):
                    matriz[k][j] -= factor * matriz[i][j]
                    identidad[k][j] -= factor * identidad[i][j]
    return identidad

class CasillaMatriz(QLineEdit):
    """Clase personalizada para manejar eventos en las celdas de la matriz."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        row, col = self.parent.pos_in_grid(self)
        if event.key() == Qt.Key_Left and col > 0:
            self.parent.matriz_inputs[row][col - 1].setFocus()
        elif event.key() == Qt.Key_Right and col < len(self.parent.matriz_inputs[row]) - 1:
            self.parent.matriz_inputs[row][col + 1].setFocus()
        elif event.key() == Qt.Key_Up and row > 0:
            self.parent.matriz_inputs[row - 1][col].setFocus()
        elif event.key() == Qt.Key_Down and row < len(self.parent.matriz_inputs) - 1:
            self.parent.matriz_inputs[row + 1][col].setFocus()
        else:
            super().keyPressEvent(event)

class InversaMatrizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Matriz Inversa.")
        self.setStyleSheet("background-color: black; color: white;")
        self.layout_principal = QVBoxLayout()

        # Título
        titulo = QLabel("Matriz Inversa.")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(titulo)

        # Entrada para el tamaño de la matriz
        layout_tamano = QHBoxLayout()
        layout_tamano.addWidget(QLabel("Tamaño de la matriz (n x n):"))
        self.tamano_input = QLineEdit()
        self.tamano_input.setStyleSheet(self.input_style())
        layout_tamano.addWidget(self.tamano_input)

        self.generar_matriz_button = QPushButton("Generar Matriz")
        self.generar_matriz_button.setStyleSheet(self.button_style())
        self.generar_matriz_button.clicked.connect(self.generar_matriz_inputs)
        layout_tamano.addWidget(self.generar_matriz_button)
        self.layout_principal.addLayout(layout_tamano)

        # Área de la matriz
        self.matriz_layout = QGridLayout()
        self.layout_principal.addLayout(self.matriz_layout)

        # Botones para agregar fila/columna
        layout_botones = QHBoxLayout()
        self.agregar_button = QPushButton("Agregar ▼")
        self.agregar_button.setStyleSheet(self.button_style())
        menu_agregar = QMenu(self)
        menu_agregar.setStyleSheet("background-color: #222; color: white;")

        accion_agregar_fila = menu_agregar.addAction("Agregar Fila")
        accion_agregar_fila.triggered.connect(self.agregar_fila)

        accion_agregar_columna = menu_agregar.addAction("Agregar Columna")
        accion_agregar_columna.triggered.connect(self.agregar_columna)

        self.agregar_button.setMenu(menu_agregar)
        layout_botones.addWidget(self.agregar_button)

        calcular_button = QPushButton("Calcular Inversa")
        calcular_button.setStyleSheet(self.button_style())
        calcular_button.clicked.connect(self.calcular_inversa)
        layout_botones.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.setStyleSheet(self.button_style())
        limpiar_button.clicked.connect(self.limpiar_campos)
        layout_botones.addWidget(limpiar_button)
        self.layout_principal.addLayout(layout_botones)

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

        # Botón de volver
        volver_layout = QHBoxLayout()
        self.volver_button = QPushButton("← Volver")
        self.volver_button.setStyleSheet(self.button_style())
        volver_layout.addWidget(self.volver_button, alignment=Qt.AlignLeft)
        self.layout_principal.addLayout(volver_layout)

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

    def generar_matriz_inputs(self):
        try:
            n = int(self.tamano_input.text())
            if n <= 0:
                raise ValueError("El tamaño debe ser mayor a 0.")
        except ValueError:
            self.mostrar_error("Error: Ingrese un número entero positivo para el tamaño de la matriz.")
            return

        for i in reversed(range(self.matriz_layout.count())):
            widget = self.matriz_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.matriz_inputs = []
        for i in range(n):
            fila_inputs = []
            for j in range(n):
                input_field = CasillaMatriz(self)
                input_field.setStyleSheet(self.input_style())
                fila_inputs.append(input_field)
                self.matriz_layout.addWidget(input_field, i, j)
            self.matriz_inputs.append(fila_inputs)

    def agregar_fila(self):
        if not hasattr(self, 'matriz_inputs') or not self.matriz_inputs:
            self.mostrar_error("Primero genere la matriz.")
            return

        nueva_fila = []
        n_columnas = len(self.matriz_inputs[0])
        fila_actual = len(self.matriz_inputs)

        for j in range(n_columnas):
            input_field = CasillaMatriz(self)
            input_field.setStyleSheet(self.input_style())
            nueva_fila.append(input_field)
            self.matriz_layout.addWidget(input_field, fila_actual, j)

        self.matriz_inputs.append(nueva_fila)

    def agregar_columna(self):
        if not hasattr(self, 'matriz_inputs') or not self.matriz_inputs:
            self.mostrar_error("Primero genere la matriz.")
            return

        n_filas = len(self.matriz_inputs)
        columna_actual = len(self.matriz_inputs[0])

        for i in range(n_filas):
            input_field = CasillaMatriz(self)
            input_field.setStyleSheet(self.input_style())
            self.matriz_inputs[i].append(input_field)
            self.matriz_layout.addWidget(input_field, i, columna_actual)

    def calcular_inversa(self):
        try:
            matriz = []
            for fila_inputs in self.matriz_inputs:
                fila = []
                for input_field in fila_inputs:
                    valor = input_field.text()
                    if not valor:
                        raise ValueError("Complete todos los campos de la matriz.")
                    fila.append(Fraction(valor))
                matriz.append(fila)

            inversa = gauss_jordan(matriz, self.resultado_text)
            self.resultado_text.append(f"\nInversa de la matriz:\n{formatear_matriz(inversa)}")
        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def limpiar_campos(self):
        self.tamano_input.clear()
        for i in reversed(range(self.matriz_layout.count())):
            widget = self.matriz_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.resultado_text.clear()

    def pos_in_grid(self, widget):
        for row_idx, row in enumerate(self.matriz_inputs):
            if widget in row:
                col_idx = row.index(widget)
                return row_idx, col_idx
        return None, None

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = InversaMatrizApp()
    ventana.show()
    sys.exit(app.exec_())