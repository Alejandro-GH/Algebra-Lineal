import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTabWidget, QMessageBox, QLabel
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt
from Determinantes import DeterminantesWidget
from Matriz_Inversa import InversaMatrizApp
from Matriz_Por_Vector import MatrizPorVectorWidget
from Met_Newton_Raphson import NewtonRaphsonWidget
from Metodo_Biseccion import BiseccionWidget
from Metodo_De_Gauss_Jordan import GaussJordanWidget
from Metodo_De_Matrices_Transpuestas import MatricesTranspuestasWidget
from Multiplicacion_De_Matrices import MultiplicacionMatricesApp
from Propiedad_Distributiva import PropiedadDistributivaWidget
from Regla_De_Cramer import ReglaCramerWidget
from Falsa_Posicion import FalsaPosicionApp
from Secante import SecanteApp


class MathCoderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MathCoder")
        self.setGeometry(100, 100, 1200, 800)

        self.menu_expanded = True
        self.menu_buttons = []

        # Ruta del ícono principal
        ruta_icono_calculadora = os.path.join(os.path.dirname(__file__), "iconos/mathcoder.ico")
        if os.path.exists(ruta_icono_calculadora):
            self.setWindowIcon(QIcon(ruta_icono_calculadora))
        else:
            print(f"Advertencia: No se encontró el ícono de la calculadora en {ruta_icono_calculadora}")

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)

        # Menú lateral
        self.menu_layout = QVBoxLayout()
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_widget.setFixedWidth(250)
        self.menu_widget.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #ccc;")
        self.main_layout.addWidget(self.menu_widget)

        # Botón para alternar el menú
        ruta_icono_menu = os.path.join(os.path.dirname(__file__), "iconos/menú.png")
        self.toggle_menu_button = QPushButton()
        if os.path.exists(ruta_icono_menu):
            self.toggle_menu_button.setIcon(QIcon(ruta_icono_menu))
        self.toggle_menu_button.setIconSize(QSize(32, 32))
        self.toggle_menu_button.setToolTip("Ocultar/Desplegar menú")
        self.toggle_menu_button.clicked.connect(self.toggle_menu)
        self.menu_layout.addWidget(self.toggle_menu_button)

        # Tabs principales
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tab_widget)

        # Agregar botones al menú
        self.agregar_botones()

        # Botón para salir
        salir_button = QPushButton("Salir")
        salir_button.setIconSize(QSize(32, 32))
        salir_button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                font-size: 14px;
                background-color: #ffcccc;
            }
            QPushButton:hover {
                background-color: #ff9999;
            }
        """)
        salir_button.clicked.connect(self.confirm_exit)
        self.menu_layout.addWidget(salir_button)

    def agregar_botones(self):
        categorias = [
            ("Resolución de Ecuaciones No Lineales", [
                ("Newton-Raphson", NewtonRaphsonWidget),
                ("Método de Bisección", BiseccionWidget),
                ("Falsa Posición", FalsaPosicionApp),
                ("Método de la Secante", SecanteApp),
            ]),
            ("Álgebra Matricial", [
                ("Determinantes", DeterminantesWidget),
                ("Inversa de Matriz", InversaMatrizApp),
                ("Multiplicación Matriz-Vector", MatrizPorVectorWidget),
                ("Multiplicación de Matrices", MultiplicacionMatricesApp),
            ]),
            ("Propiedades Avanzadas", [
                ("Gauss-Jordan", GaussJordanWidget),
                ("Matriz Transpuesta", MatricesTranspuestasWidget),
                ("Propiedad Distributiva", PropiedadDistributivaWidget),
                ("Regla de Cramer", ReglaCramerWidget),
            ])
        ]

        for categoria, widgets in categorias:
            self.menu_layout.addWidget(QLabel(categoria))
            for nombre, widget_class in widgets:
                button = QPushButton(nombre)
                button.clicked.connect(lambda _, w=widget_class, n=nombre: self.open_tab(w, n))
                self.menu_layout.addWidget(button)

    def toggle_menu(self):
        self.menu_widget.setFixedWidth(60 if self.menu_expanded else 250)
        self.menu_expanded = not self.menu_expanded

    def open_tab(self, widget_class, nombre):
        widget = widget_class()
        index = self.tab_widget.addTab(widget, nombre)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def confirm_exit(self):
        if QMessageBox.question(self, "Confirmar", "¿Salir?") == QMessageBox.Yes:
            QApplication.quit()


def main():
    app = QApplication(sys.argv)
    ventana = MathCoderApp()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()