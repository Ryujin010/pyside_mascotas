import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QLabel, QSizePolicy,
                               QMenuBar, QMenu, QStatusBar,
                               QStackedWidget, QToolBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
import qdarkstyle

# Importar nuestros módulos
from services.mascota_service import MascotaService
from services.export_service import ExportService  # [NUEVO]
from views.home_view import HomeView
from views.form_view import FormView


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación de adopción de mascotas.
    """

    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("🐾 PySide Mascotas")
        self.resize(1280, 720)

        # Inicializar servicio
        self.service = MascotaService()

        # Crear el stacked widget para navegación
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Crear las vistas
        self.home_view = HomeView()
        self.form_view = FormView()

        # Configurar vistas
        self.home_view.set_service(self.service)
        self.form_view.set_service(self.service)

        # Configurar callbacks
        self.form_view.set_callback_actualizar(self.home_view.refrescar)
        self.form_view.set_callback_volver(self.mostrar_home)

        # Conectar señal de edición desde HomeView
        self.home_view.editar_solicitado.connect(self.mostrar_formulario_edicion)

        # Agregar vistas al stacked widget
        self.stacked_widget.addWidget(self.home_view)  # Índice 0
        self.stacked_widget.addWidget(self.form_view)  # Índice 1

        # Crear menú y barra de herramientas
        self.crear_menu()
        self.crear_toolbar()

        # Crear barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")

        # Mostrar vista inicial (Home)
        self.mostrar_home()

    def crear_menu(self):
        """Crea la barra de menú de la aplicación."""
        menubar = self.menuBar()

        # Menú Archivo
        menu_archivo = menubar.addMenu("📁 Archivo")

        # [NUEVO] Submenú de Exportar
        menu_exportar = menu_archivo.addMenu("📤 Exportar")

        accion_exportar_csv = QAction("📊 Exportar a CSV", self)
        accion_exportar_csv.setStatusTip("Exportar listado a archivo CSV")
        accion_exportar_csv.triggered.connect(self.exportar_csv)
        menu_exportar.addAction(accion_exportar_csv)

        accion_exportar_pdf = QAction("📄 Exportar a PDF", self)
        accion_exportar_pdf.setStatusTip("Exportar listado a archivo PDF")
        accion_exportar_pdf.triggered.connect(self.exportar_pdf)
        menu_exportar.addAction(accion_exportar_pdf)

        menu_exportar.addSeparator()

        menu_archivo.addSeparator()

        accion_salir = QAction("🚪 Salir", self)
        accion_salir.setShortcut("Ctrl+Q")
        accion_salir.setStatusTip("Salir de la aplicación")
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)

        # Menú Navegación
        menu_navegacion = menubar.addMenu("🧭 Navegación")

        accion_inicio = QAction("🏠 Inicio", self)
        accion_inicio.setShortcut("Ctrl+H")
        accion_inicio.setStatusTip("Ver listado de mascotas")
        accion_inicio.triggered.connect(self.mostrar_home)
        menu_navegacion.addAction(accion_inicio)

        accion_agregar = QAction("➕ Agregar Mascota", self)
        accion_agregar.setShortcut("Ctrl+N")
        accion_agregar.setStatusTip("Agregar una nueva mascota")
        accion_agregar.triggered.connect(self.mostrar_formulario)
        menu_navegacion.addAction(accion_agregar)

        # Menú Ayuda
        menu_ayuda = menubar.addMenu("❓ Ayuda")

        accion_acerca = QAction("ℹ️ Acerca de", self)
        accion_acerca.setStatusTip("Información de la aplicación")
        accion_acerca.triggered.connect(self.mostrar_acerca)
        menu_ayuda.addAction(accion_acerca)

    def crear_toolbar(self):
        """Crea la barra de herramientas de la aplicación."""
        toolbar = QToolBar("Barra de herramientas")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Botón Inicio
        btn_inicio = QAction("🏠 Inicio", self)
        btn_inicio.setStatusTip("Ir al listado de mascotas")
        btn_inicio.triggered.connect(self.mostrar_home)
        toolbar.addAction(btn_inicio)

        toolbar.addSeparator()

        # Botón Agregar
        btn_agregar = QAction("➕ Agregar", self)
        btn_agregar.setStatusTip("Agregar nueva mascota")
        btn_agregar.triggered.connect(self.mostrar_formulario)
        toolbar.addAction(btn_agregar)

        toolbar.addSeparator()

        # [NUEVO] Botones de exportación en toolbar
        btn_exportar_csv = QAction("📊 CSV", self)
        btn_exportar_csv.setStatusTip("Exportar a CSV")
        btn_exportar_csv.triggered.connect(self.exportar_csv)
        toolbar.addAction(btn_exportar_csv)

        btn_exportar_pdf = QAction("📄 PDF", self)
        btn_exportar_pdf.setStatusTip("Exportar a PDF")
        btn_exportar_pdf.triggered.connect(self.exportar_pdf)
        toolbar.addAction(btn_exportar_pdf)

    # [NUEVO] Métodos de exportación
    def exportar_csv(self):
        """Exporta el listado a CSV."""
        try:
            with self.service as s:
                mascotas = s.obtener_todos()
                ExportService.exportar_a_csv(mascotas, self)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar: {str(e)}")

    def exportar_pdf(self):
        """Exporta el listado a PDF."""
        try:
            with self.service as s:
                mascotas = s.obtener_todos()
                ExportService.exportar_a_pdf(mascotas, self)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar: {str(e)}")

    def mostrar_home(self):
        """Muestra la vista de inicio (listado de mascotas)."""
        self.stacked_widget.setCurrentIndex(0)  # HomeView
        self.form_view.configurar_modo_edicion(False)
        self.form_view.limpiar_campos()
        self.home_view.refrescar()  # Actualizar datos
        self.status_bar.showMessage("Mostrando listado de mascotas")

    def mostrar_formulario(self):
        """Muestra el formulario para agregar una nueva mascota."""
        self.stacked_widget.setCurrentIndex(1)  # FormView
        self.form_view.configurar_modo_edicion(False)
        self.form_view.limpiar_campos()
        self.status_bar.showMessage("Agregando nueva mascota")

    def mostrar_formulario_edicion(self, mascota_id):
        """
        Muestra el formulario cargado con los datos de la mascota a editar.

        Args:
            mascota_id (int): ID de la mascota a editar
        """
        self.stacked_widget.setCurrentIndex(1)
        self.form_view.configurar_modo_edicion(True)

        if self.form_view.cargar_datos(mascota_id):
            self.status_bar.showMessage(f"Editando mascota ID: {mascota_id}")
        else:
            self.mostrar_home()

    def mostrar_acerca(self):
        """Muestra información acerca de la aplicación."""
        QMessageBox.about(
            self,
            "Acerca de PySide Mascotas",
            "<h2>🐾 PySide Mascotas</h2>"
            "<p>Versión 2.0</p>"
            "<p>Sistema de Adopción de Mascotas</p>"
            "<p>Características:</p>"
            "<ul>"
            "<li>CRUD completo de mascotas</li>"
            "<li>Modo oscuro con QDarkStyle</li>"
            "<li>Estadísticas en tiempo real</li>"
            "<li>Exportación a CSV y PDF</li>"
            "</ul>"
            "<p>© 2026 - Refugio Digital</p>"
        )


def main():
    """
    Función principal que inicializa la aplicación con tema oscuro.
    """
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()