from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QGridLayout, QMessageBox, QScrollArea, QMenu
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QEvent
from sympy import Matrix, sympify
from PyQt5.QtWidgets import QApplication


class DeterminantesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.matriz_inputs = []

    def initUI(self):
        """Configura la interfaz gráfica del widget."""
        self.setWindowTitle("Método de Determinantes.")
        self.setStyleSheet("background-color: black; color: white;")

        self.layout_principal = QVBoxLayout()

        # Scroll area para la matriz
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)

        titulo = QLabel("Determinantes.")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(titulo)

        layout_tamano = QHBoxLayout()
        layout_tamano.addWidget(QLabel("Tamaño de la matriz (n x n):"))
        self.tamano_input = QLineEdit()
        self.tamano_input.setPlaceholderText("Ingrese 'n'")
        self.tamano_input.setStyleSheet(self.input_style())
        layout_tamano.addWidget(self.tamano_input)

        self.generar_matriz_button = QPushButton("Generar Matriz")
        self.generar_matriz_button.clicked.connect(self.generar_matriz_inputs)
        self.generar_matriz_button.setStyleSheet(self.button_style())
        layout_tamano.addWidget(self.generar_matriz_button)

        self.layout_principal.addLayout(layout_tamano)

        layout_botones = QHBoxLayout()

        self.agregar_button = QPushButton("Agregar")
        self.agregar_button.setStyleSheet(self.button_style())
        menu_agregar = QMenu(self)
        menu_agregar.setStyleSheet("background-color: #222; color: white;")

        accion_agregar_fila = menu_agregar.addAction("Agregar Fila")
        accion_agregar_fila.triggered.connect(self.agregar_fila)

        accion_agregar_columna = menu_agregar.addAction("Agregar Columna")
        accion_agregar_columna.triggered.connect(self.agregar_columna)

        self.agregar_button.setMenu(menu_agregar)
        layout_botones.addWidget(self.agregar_button)

        self.eliminar_button = QPushButton("Eliminar")
        self.eliminar_button.setStyleSheet(self.button_style())
        menu_eliminar = QMenu(self)
        menu_eliminar.setStyleSheet("background-color: #222; color: white;")

        accion_eliminar_fila = menu_eliminar.addAction("Eliminar Fila")
        accion_eliminar_fila.triggered.connect(self.eliminar_fila)

        accion_eliminar_columna = menu_eliminar.addAction("Eliminar Columna")
        accion_eliminar_columna.triggered.connect(self.eliminar_columna)

        self.eliminar_button.setMenu(menu_eliminar)
        layout_botones.addWidget(self.eliminar_button)

        self.calcular_button = QPushButton("Calcular Determinante")
        self.calcular_button.clicked.connect(self.calcular_determinante_gui)
        self.calcular_button.setStyleSheet(self.button_style())
        layout_botones.addWidget(self.calcular_button)

        self.limpiar_button = QPushButton("Limpiar")
        self.limpiar_button.clicked.connect(self.limpiar_campos)
        self.limpiar_button.setStyleSheet(self.button_style())
        layout_botones.addWidget(self.limpiar_button)

        self.layout_principal.addLayout(layout_botones)

        self.matriz_layout = QGridLayout()
        self.scroll_area_layout.addLayout(self.matriz_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.layout_principal.addWidget(self.scroll_area)

        resultado_layout = QVBoxLayout()

        self.resultado_label = QLabel("Resultado:")
        self.resultado_label.setFont(QFont("Arial", 12))
        self.resultado_label.setAlignment(Qt.AlignCenter)
        self.resultado_label.setStyleSheet(self.resultado_label_style())
        resultado_layout.addWidget(self.resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setStyleSheet(self.resultado_text_style())
        resultado_layout.addWidget(self.resultado_text)

        self.layout_principal.addLayout(resultado_layout)

        self.setLayout(self.layout_principal)

    def button_style(self):
        """Estilo para los botones."""
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

    def resultado_label_style(self):
        """Estilo para la etiqueta de resultado."""
        return """
            QLabel {
                border: 2px solid white;
                border-radius: 15px;
                padding: 5px;
                font-size: 14px;
                background-color: black;
                color: white;
            }
        """

    def resultado_text_style(self):
        """Estilo para el cuadro de texto de resultado."""
        return """
            QTextEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def generar_matriz_inputs(self):
        """Genera los campos de Entrada para la matriz segun el tamaño especificado."""
        try:
            n = int(self.tamano_input.text())
            if n <= 0:
                raise ValueError("El tamaño debe ser mayor a 0.")
        except ValueError:
            self.mostrar_error("El tamaño ingresado no es válido. Ingrese un número mayor a 0.")
            return

        self.limpiar_matriz_layout()

        self.matriz_inputs = []
        for i in range(n):
            fila_inputs = []
            for j in range(n):
                input_field = self.crear_campo_entrada(f"({i + 1}, {j + 1})")
                input_field.setMinimumSize(40, 30)
                input_field.setMaximumSize(100,40)
                fila_inputs.append(input_field)
                self.matriz_layout.addWidget(input_field, i, j)
            self.matriz_inputs.append(fila_inputs)

    def crear_campo_entrada(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.input_style())
        input_field.setAlignment(Qt.AlignCenter)
        input_field.installEventFilter(self)
        return input_field

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            row, col = self.get_current_position(obj)
            if key == Qt.Key_Left and col > 0:
                self.matriz_inputs[row][col - 1].setFocus()
            elif key == Qt.Key_Right and col < len(self.matriz_inputs[row]) - 1:
                self.matriz_inputs[row][col + 1].setFocus()
            elif key == Qt.Key_Up and row > 0:
                self.matriz_inputs[row - 1][col].setFocus()
            elif key == Qt.Key_Down and row < len(self.matriz_inputs) - 1:
                self.matriz_inputs[row + 1][col].setFocus()
            return True
        return super().eventFilter(obj, event)

    def get_current_position(self, widget):
        for i, fila in enumerate(self.matriz_inputs):
            if widget in fila:
                return i, fila.index(widget)
        return -1, -1

    def agregar_fila(self):
        if not self.matriz_inputs:
            self.mostrar_error("Primero genere la matriz.")
            return
        nueva_fila = []
        n_columnas = len(self.matriz_inputs[0])
        for j in range(n_columnas):
            input_field = self.crear_campo_entrada("")
            nueva_fila.append(input_field)
            self.matriz_layout.addWidget(input_field, len(self.matriz_inputs), j)
        self.matriz_inputs.append(nueva_fila)

    def agregar_columna(self):
        if not self.matriz_inputs:
            self.mostrar_error("Primero genere la matriz.")
            return
        n_filas = len(self.matriz_inputs)
        for i in range(n_filas):
            input_field = self.crear_campo_entrada("")
            self.matriz_inputs[i].append(input_field)
            self.matriz_layout.addWidget(input_field, i, len(self.matriz_inputs[i]) - 1)

    def eliminar_fila(self):
        if not self.matriz_inputs:
            self.mostrar_error("No hay filas para eliminar.")
            return
        fila_a_eliminar = self.matriz_inputs.pop()
        for widget in fila_a_eliminar:
            widget.deleteLater()

    def eliminar_columna(self):
        if not self.matriz_inputs or not self.matriz_inputs[0]:
            self.mostrar_error("No hay columnas para eliminar.")
            return
        for fila in self.matriz_inputs:
            widget = fila.pop()
            widget.deleteLater()

    def calcular_determinante_gui(self):
        """Calcula el determinante de la matriz ingresada."""
        try:
            if len(self.matriz_inputs) != len(self.matriz_inputs[0]):
                self.mostrar_error("La matriz debe ser cuadrada para calcular el determinante.")
                return

            matriz = []
            for fila_inputs in self.matriz_inputs:
                fila = []
                for input_field in fila_inputs:
                    valor = input_field.text()
                    if not valor:
                        input_field.setStyleSheet(input_field.styleSheet() + "border: 2px solid red;")
                        raise ValueError("Complete todos los campos de la matriz.")
                    fila.append(sympify(valor))
                matriz.append(fila)

            sympy_matrix = Matrix(matriz)
            det = sympy_matrix.det()

            # Verificar propiedades
            propiedades = self.verificar_propiedades(matriz)

            # Mostrar resultados
            self.resultado_label.setText(f"Resultado: Determinante = {det}")
            self.resultado_text.setText(f"El determinante de la matriz es: {det}\n\n" + "\n".join(propiedades))

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def verificar_propiedades(self, matriz):
        """Verifica propiedades específicas de la matriz."""
        mensaje = []
        n = len(matriz)

        # Verificar diagonal
        if all(matriz[i][j] == 0 for i in range(n) for j in range(n) if i != j):
            mensaje.append("La matriz es diagonal. El determinante es el producto de la diagonal.")

        # Verificar triangular superior
        if all(matriz[i][j] == 0 for i in range(1, n) for j in range(i)):
            mensaje.append("La matriz es triangular superior.")

        # Verificar triangular inferior
        if all(matriz[i][j] == 0 for i in range(n) for j in range(i + 1, n)):
            mensaje.append("La matriz es triangular inferior.")

        # Verificar simetría
        if matriz == [list(row) for row in zip(*matriz)]:
            mensaje.append("La matriz es simétrica (A = A^T).")

        return mensaje

    def limpiar_campos(self):
        """Limpia todos los campos de entrada, resultados y reinicia la matriz."""
        self.tamano_input.clear()
        self.limpiar_matriz_layout()
        self.resultado_label.setText("Resultado:")
        self.resultado_text.clear()
        self.matriz_inputs.clear()
        self.tamano_input.setPlaceholderText("Ingrese 'n'")

    def limpiar_matriz_layout(self):
        """Limpia el layout de la matriz."""
        for i in reversed(range(self.matriz_layout.count())):
            widget = self.matriz_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en un cuadro de diálogo."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == "__main__":
    app = QApplication([])
    ventana = DeterminantesWidget()
    ventana.show()
    app.exec_()