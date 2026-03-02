"""
Vista Home - Pantalla principal con el listado de mascotas.
Con pestañas, exportación, estadísticas mejoradas y PAGINACIÓN.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QTableView, QHeaderView, QMessageBox,
                               QLineEdit, QHBoxLayout,
                               QGridLayout, QFrame, QScrollArea,
                               QSizePolicy, QTabWidget, QGroupBox,
                               QPushButton, QComboBox)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal


class MascotaTableModel(QAbstractTableModel):
    """
    Modelo de tabla para mostrar mascotas en un QTableView.
    """

    def __init__(self):
        super().__init__()
        self.mascotas = []
        self.headers = ["ID", "Nombre", "Especie", "Peso (kg)"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.mascotas)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.mascotas)):
            return None

        mascota = self.mascotas[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return str(mascota.id)
            elif col == 1:
                return mascota.nombre
            elif col == 2:
                return mascota.especie
            elif col == 3:
                return f"{mascota.peso:.2f}"

        elif role == Qt.TextAlignmentRole:
            if col == 0 or col == 3:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def actualizar_datos(self, mascotas):
        self.beginResetModel()
        self.mascotas = mascotas
        self.endResetModel()


class StatsCard(QFrame):
    """
    Widget para mostrar una tarjeta de estadística con mejor visibilidad.
    """

    def __init__(self, titulo, valor, color="#0078d7", icono="🐾", descripcion="", parent=None):
        super().__init__(parent)
        self.setup_ui(titulo, valor, color, icono, descripcion)

    def setup_ui(self, titulo, valor, color, icono, descripcion):
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumHeight(140)
        self.setMaximumHeight(160)

        self.setStyleSheet(f"""
            StatsCard {{
                background-color: #2d2d2d !important;
                border: 3px solid {color} !important;
                border-radius: 12px !important;
                padding: 15px !important;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icono_container = QFrame()
        icono_container.setFixedSize(45, 45)
        icono_container.setStyleSheet(f"""
            QFrame {{
                background-color: {color} !important;
                border-radius: 22px !important;
                border: none !important;
            }}
        """)

        icono_layout = QVBoxLayout(icono_container)
        icono_layout.setContentsMargins(0, 0, 0, 0)

        icono_label = QLabel(icono)
        icono_label.setAlignment(Qt.AlignCenter)
        icono_label.setStyleSheet(f"""
            QLabel {{
                color: white !important;
                font-size: 22pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }}
        """)
        icono_layout.addWidget(icono_label)

        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("""
            QLabel {
                color: #ffffff !important;
                font-size: 14pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }
        """)

        header_layout.addWidget(icono_container)
        header_layout.addWidget(titulo_label, 1)

        self.valor_label = QLabel(str(valor))
        self.valor_label.setAlignment(Qt.AlignCenter)
        self.valor_label.setStyleSheet(f"""
            QLabel {{
                color: {color} !important;
                font-size: 36pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
                padding: 5px !important;
            }}
        """)

        self.desc_label = QLabel(descripcion)
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setStyleSheet("""
            QLabel {
                color: #cccccc !important;
                font-size: 11pt !important;
                background-color: transparent !important;
            }
        """)

        layout.addLayout(header_layout)
        layout.addWidget(self.valor_label)
        layout.addWidget(self.desc_label)

    def actualizar_valor(self, nuevo_valor):
        self.valor_label.setText(str(nuevo_valor))


class EspecieCard(QFrame):
    """
    Tarjeta para mostrar una especie con mejor visibilidad.
    """

    def __init__(self, especie, cantidad, total, color, icono, parent=None):
        super().__init__(parent)
        self.especie = especie
        self.cantidad = cantidad
        self.total = total
        self.color = color
        self.icono = icono
        self.setup_ui()

    def setup_ui(self):
        porcentaje = (self.cantidad / self.total * 100) if self.total > 0 else 0

        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumHeight(220)
        self.setMaximumHeight(240)
        self.setMinimumWidth(200)
        self.setMaximumWidth(240)

        self.setStyleSheet(f"""
            EspecieCard {{
                background-color: #2d2d2d !important;
                border: 3px solid {self.color} !important;
                border-radius: 15px !important;
                padding: 15px !important;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        icono_container = QFrame()
        icono_container.setFixedSize(70, 70)
        icono_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color} !important;
                border-radius: 35px !important;
                border: none !important;
            }}
        """)

        icono_layout = QVBoxLayout(icono_container)
        icono_layout.setContentsMargins(0, 0, 0, 0)

        icono_label = QLabel(self.icono)
        icono_label.setAlignment(Qt.AlignCenter)
        icono_label.setStyleSheet(f"""
            QLabel {{
                color: white !important;
                font-size: 32pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }}
        """)
        icono_layout.addWidget(icono_label)

        layout.addWidget(icono_container, 0, Qt.AlignCenter)

        nombre_label = QLabel(self.especie)
        nombre_label.setAlignment(Qt.AlignCenter)
        nombre_label.setStyleSheet("""
            QLabel {
                color: #ffffff !important;
                font-size: 18pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }
        """)
        layout.addWidget(nombre_label)

        cantidad_label = QLabel(str(self.cantidad))
        cantidad_label.setAlignment(Qt.AlignCenter)
        cantidad_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color} !important;
                font-size: 32pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }}
        """)
        layout.addWidget(cantidad_label)

        progreso_container = QWidget()
        progreso_layout = QVBoxLayout(progreso_container)
        progreso_layout.setContentsMargins(5, 5, 5, 0)
        progreso_layout.setSpacing(5)

        barra_titulo = QLabel("Progreso:")
        barra_titulo.setAlignment(Qt.AlignLeft)
        barra_titulo.setStyleSheet("""
            QLabel {
                color: #aaaaaa !important;
                font-size: 10pt !important;
                background-color: transparent !important;
            }
        """)
        progreso_layout.addWidget(barra_titulo)

        barra_container = QFrame()
        barra_container.setFixedHeight(15)
        barra_container.setStyleSheet("""
            QFrame {
                background-color: #404040 !important;
                border-radius: 7px !important;
                border: none !important;
            }
        """)

        self.barra = QFrame(barra_container)
        self.barra.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color} !important;
                border-radius: 7px !important;
                border: none !important;
            }}
        """)
        self.barra.setFixedHeight(15)
        self.barra.setFixedWidth(int(170 * (porcentaje / 100)))

        porcentaje_label = QLabel(f"{porcentaje:.1f}%")
        porcentaje_label.setAlignment(Qt.AlignCenter)
        porcentaje_label.setStyleSheet("""
            QLabel {
                color: #ffffff !important;
                font-size: 12pt !important;
                font-weight: bold !important;
                background-color: transparent !important;
            }
        """)

        progreso_layout.addWidget(barra_container)
        progreso_layout.addWidget(porcentaje_label)

        layout.addWidget(progreso_container)


class HomeView(QWidget):
    """
    Vista principal que muestra el listado de mascotas.
    Con pestañas, exportación, estadísticas mejoradas y PAGINACIÓN.
    """

    editar_solicitado = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = None
        self.pagina_actual = 1
        self.items_por_pagina = 20
        self.total_registros = 0
        self.total_paginas = 1
        self.filtro_actual = ""
        self.setup_ui()
        self.conectar_senales()

    def setup_ui(self):
        """Configura la interfaz de usuario de la vista home."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        titulo = QLabel("🐾 Sistema de Adopción de Mascotas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #ffffff;
                background-color: #2b2b2b;
                padding: 15px;
                border-bottom: 2px solid #404040;
            }
        """)
        layout.addWidget(titulo)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #cccccc;
                padding: 10px 25px;
                margin-right: 2px;
                font-size: 11pt;
                font-weight: bold;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #0078d7;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #404040;
            }
        """)

        self.listado_tab = QWidget()
        self.setup_listado_tab()
        self.tabs.addTab(self.listado_tab, "📋 Listado de Mascotas")

        self.estadisticas_tab = QWidget()
        self.setup_estadisticas_tab()
        self.tabs.addTab(self.estadisticas_tab, "📊 Estadísticas")

        layout.addWidget(self.tabs)

    def setup_listado_tab(self):
        """Configura la pestaña de listado con paginación."""
        layout = QVBoxLayout(self.listado_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # ===== BARRA SUPERIOR CON BÚSQUEDA Y EXPORTACIÓN =====
        toolbar_container = QWidget()
        toolbar_container.setMaximumHeight(60)
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)

        # Búsqueda
        label_buscar = QLabel("🔍")
        label_buscar.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14pt;
            }
        """)

        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Filtrar por nombre o especie...")
        self.buscar_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #404040;
                border-radius: 5px;
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)

        toolbar_layout.addWidget(label_buscar)
        toolbar_layout.addWidget(self.buscar_input, 3)

        # Botones de exportación
        toolbar_layout.addSpacing(20)

        self.btn_exportar_csv = QPushButton("📊 CSV")
        self.btn_exportar_csv.setFixedSize(80, 35)
        self.btn_exportar_csv.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34ce57;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.btn_exportar_csv.clicked.connect(self.exportar_csv)

        self.btn_exportar_pdf = QPushButton("📄 PDF")
        self.btn_exportar_pdf.setFixedSize(80, 35)
        self.btn_exportar_pdf.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f14353;
            }
            QPushButton:pressed {
                background-color: #b02a37;
            }
        """)
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)

        toolbar_layout.addWidget(self.btn_exportar_csv)
        toolbar_layout.addWidget(self.btn_exportar_pdf)

        layout.addWidget(toolbar_container)

        # ===== TABLA =====
        self.tabla = QTableView()
        self.tabla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tabla.setSelectionBehavior(QTableView.SelectRows)
        self.tabla.setSelectionMode(QTableView.SingleSelection)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setEditTriggers(QTableView.NoEditTriggers)

        self.tabla.setStyleSheet("""
            QTableView {
                border: 2px solid #404040;
                border-radius: 5px;
                background-color: #2b2b2b;
                alternate-background-color: #353535;
                selection-background-color: #3d3d3d;
                selection-color: #ffffff;
                gridline-color: transparent;
            }
            QTableView::item {
                padding: 8px;
                border: none;
            }
            QTableView::item:selected {
                background-color: #4a4a4a;
            }
            QHeaderView::section {
                background-color: #404040;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #555555;
                font-weight: bold;
                color: #ffffff;
                font-size: 11pt;
            }
        """)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(False)
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        header.setMinimumSectionSize(100)
        header.setDefaultSectionSize(150)

        self.tabla.verticalHeader().setDefaultSectionSize(40)

        self.modelo = MascotaTableModel()
        self.tabla.setModel(self.modelo)

        self.tabla.horizontalHeader().geometriesChanged.connect(self.ajustar_columnas)

        layout.addWidget(self.tabla, 1)

        # ===== BARRA DE PAGINACIÓN =====
        paginacion_container = QWidget()
        paginacion_container.setMaximumHeight(50)
        paginacion_layout = QHBoxLayout(paginacion_container)
        paginacion_layout.setContentsMargins(5, 5, 5, 5)

        # Selector de items por página
        paginacion_layout.addWidget(QLabel("Mostrar:"))

        self.items_por_pagina_combo = QComboBox()
        self.items_por_pagina_combo.addItems(["10", "20", "50", "100"])
        self.items_por_pagina_combo.setCurrentText("20")
        self.items_por_pagina_combo.setStyleSheet("""
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)

        paginacion_layout.addWidget(self.items_por_pagina_combo)
        paginacion_layout.addWidget(QLabel("registros por página"))

        paginacion_layout.addStretch()

        # Información de paginación
        self.info_paginacion = QLabel("Página 1 de 1")
        self.info_paginacion.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 11pt;
                font-weight: bold;
                padding: 5px;
            }
        """)
        paginacion_layout.addWidget(self.info_paginacion)

        paginacion_layout.addSpacing(20)

        # Botones de navegación
        self.btn_primera = QPushButton("⏮️ Primera")
        self.btn_primera.setFixedSize(90, 30)
        self.btn_primera.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
            }
        """)

        self.btn_anterior = QPushButton("◀ Anterior")
        self.btn_anterior.setFixedSize(90, 30)
        self.btn_anterior.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
            }
        """)

        self.btn_siguiente = QPushButton("Siguiente ▶")
        self.btn_siguiente.setFixedSize(90, 30)
        self.btn_siguiente.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
            }
        """)

        self.btn_ultima = QPushButton("Última ⏭️")
        self.btn_ultima.setFixedSize(90, 30)
        self.btn_ultima.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
            }
        """)

        paginacion_layout.addWidget(self.btn_primera)
        paginacion_layout.addWidget(self.btn_anterior)
        paginacion_layout.addWidget(self.btn_siguiente)
        paginacion_layout.addWidget(self.btn_ultima)

        layout.addWidget(paginacion_container)

    def setup_estadisticas_tab(self):
        """Configura la pestaña de estadísticas con mejor visibilidad."""
        layout = QVBoxLayout(self.estadisticas_tab)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)

        # ===== TARJETAS PRINCIPALES =====
        cards_widget = QWidget()
        cards_widget.setStyleSheet("background-color: transparent;")

        cards_layout = QGridLayout(cards_widget)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(20)

        self.total_card = StatsCard("Total Mascotas", 0, "#0078d7", "🐾",
                                   "Registros en el sistema")
        cards_layout.addWidget(self.total_card, 0, 0)

        self.peso_card = StatsCard("Peso Promedio", "0 kg", "#28a745", "⚖️",
                                  "Media de todas las mascotas")
        cards_layout.addWidget(self.peso_card, 0, 1)

        self.especies_card = StatsCard("Especies", 0, "#fd7e14", "🐕",
                                      "Tipos diferentes")
        cards_layout.addWidget(self.especies_card, 0, 2)

        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)
        cards_layout.setColumnStretch(2, 1)

        layout.addWidget(cards_widget)

        # ===== DISTRIBUCIÓN POR ESPECIE =====
        especies_group = QGroupBox("📊 Distribución por Especie")
        especies_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-size: 16pt;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 10px;
                margin-top: 20px;
                padding-top: 20px;
                background-color: #252525;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
                color: #0078d7;
            }
        """)

        especies_layout = QVBoxLayout(especies_group)
        especies_layout.setContentsMargins(15, 15, 15, 15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                height: 12px;
                background: #2b2b2b;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #0078d7;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #0086f0;
            }
        """)

        self.especies_container = QWidget()
        self.especies_container.setStyleSheet("background-color: transparent;")
        self.especies_grid = QGridLayout(self.especies_container)
        self.especies_grid.setContentsMargins(10, 10, 10, 10)
        self.especies_grid.setSpacing(20)
        self.especies_grid.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.especies_container)
        especies_layout.addWidget(scroll_area)

        layout.addWidget(especies_group, 1)

        # ===== DATOS ADICIONALES =====
        datos_group = QGroupBox("📈 Datos Adicionales")
        datos_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-size: 16pt;
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: #252525;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
                color: #28a745;
            }
        """)

        datos_layout = QGridLayout(datos_group)
        datos_layout.setContentsMargins(20, 15, 20, 15)
        datos_layout.setSpacing(15)
        datos_layout.setColumnStretch(0, 1)
        datos_layout.setColumnStretch(1, 2)

        label_style = """
            QLabel {
                color: #cccccc;
                font-size: 12pt;
                padding: 5px;
                background-color: transparent;
            }
        """

        value_style = """
            QLabel {
                color: #0078d7;
                font-size: 12pt;
                font-weight: bold;
                padding: 5px;
                background-color: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 5px;
            }
        """

        self.labels = {}
        info_items = [
            ("🏆 Mascota más pesada:", "peso_max", "—"),
            ("🍃 Mascota más liviana:", "peso_min", "—"),
            ("📊 Promedio por especie:", "promedio_especie", "—"),
            ("🌟 Especie más común:", "especie_comun", "—"),
        ]

        for i, (label, key, valor) in enumerate(info_items):
            lbl = QLabel(label)
            lbl.setStyleSheet(label_style)

            self.labels[key] = QLabel(valor)
            self.labels[key].setStyleSheet(value_style)
            self.labels[key].setWordWrap(True)

            datos_layout.addWidget(lbl, i, 0)
            datos_layout.addWidget(self.labels[key], i, 1)

        layout.addWidget(datos_group)

    def conectar_senales(self):
        """Conecta las señales de la tabla, búsqueda y paginación."""
        self.tabla.doubleClicked.connect(self.on_doble_click)
        self.buscar_input.textChanged.connect(self.on_buscar_text_changed)
        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Señales de paginación
        self.items_por_pagina_combo.currentTextChanged.connect(self.on_items_por_pagina_changed)
        self.btn_primera.clicked.connect(self.ir_a_primera)
        self.btn_anterior.clicked.connect(self.ir_a_anterior)
        self.btn_siguiente.clicked.connect(self.ir_a_siguiente)
        self.btn_ultima.clicked.connect(self.ir_a_ultima)

    # ===== MÉTODOS DE PAGINACIÓN =====

    def on_items_por_pagina_changed(self, texto):
        """Cambia la cantidad de items por página."""
        self.items_por_pagina = int(texto)
        self.pagina_actual = 1
        self.cargar_pagina_actual()

    def ir_a_primera(self):
        """Va a la primera página."""
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.cargar_pagina_actual()

    def ir_a_anterior(self):
        """Va a la página anterior."""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.cargar_pagina_actual()

    def ir_a_siguiente(self):
        """Va a la página siguiente."""
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.cargar_pagina_actual()

    def ir_a_ultima(self):
        """Va a la última página."""
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.cargar_pagina_actual()

    def actualizar_botones_paginacion(self):
        """Habilita/deshabilita botones según la página actual."""
        self.btn_primera.setEnabled(self.pagina_actual > 1)
        self.btn_anterior.setEnabled(self.pagina_actual > 1)
        self.btn_siguiente.setEnabled(self.pagina_actual < self.total_paginas)
        self.btn_ultima.setEnabled(self.pagina_actual < self.total_paginas)

        self.info_paginacion.setText(
            f"Página {self.pagina_actual} de {self.total_paginas} "
            f"({self.total_registros} registros)"
        )

    def cargar_pagina_actual(self):
        """Carga la página actual con el filtro aplicado."""
        if not self.service:
            return

        try:
            with self.service as s:
                offset = (self.pagina_actual - 1) * self.items_por_pagina

                if self.filtro_actual:
                    # Con filtro
                    mascotas = s.obtener_pagina_con_filtro(
                        offset, self.items_por_pagina, self.filtro_actual
                    )
                    self.total_registros = s.contar_con_filtro(self.filtro_actual)
                else:
                    # Sin filtro
                    mascotas = s.obtener_pagina(offset, self.items_por_pagina)
                    self.total_registros = s.contar_total()

                self.total_paginas = max(
                    1, (self.total_registros + self.items_por_pagina - 1) // self.items_por_pagina
                )

                self.modelo.actualizar_datos(mascotas)
                self.actualizar_botones_paginacion()

        except Exception as e:
            print(f"❌ Error al cargar página: {e}")
            self.mostrar_mensaje("Error", f"No se pudo cargar la página: {str(e)}", "error")

    # ===== MÉTODOS DE BÚSQUEDA =====

    def on_buscar_text_changed(self, texto):
        """Maneja el cambio en el texto de búsqueda."""
        self.filtro_actual = texto.strip()
        self.pagina_actual = 1
        self.cargar_pagina_actual()

    # ===== MÉTODOS DE ESTADÍSTICAS =====

    def on_tab_changed(self, index):
        """Cuando se cambia de pestaña, actualizar estadísticas si es necesario."""
        if index == 1:
            self.actualizar_estadisticas()

    def actualizar_estadisticas(self):
        """Obtiene y actualiza las estadísticas desde el servicio."""
        if not self.service:
            return

        try:
            with self.service as s:
                stats = s.obtener_estadisticas()

                self.total_card.actualizar_valor(stats['total'])
                self.especies_card.actualizar_valor(len(stats['por_especie']))

                if stats['peso_promedio'] > 0:
                    self.peso_card.actualizar_valor(f"{stats['peso_promedio']:.2f} kg")
                else:
                    self.peso_card.actualizar_valor("0 kg")

                # Limpiar grid de especies
                for i in reversed(range(self.especies_grid.count())):
                    item = self.especies_grid.itemAt(i)
                    if item.widget():
                        item.widget().deleteLater()

                # Obtener todas las mascotas para datos adicionales
                mascotas = s.obtener_todos()

                colores = ["#dc3545", "#fd7e14", "#ffc107", "#28a745", "#17a2b8", "#6610f2", "#e83e8c"]
                iconos = {
                    "Perro": "🐕", "Gato": "🐈", "Ave": "🐦",
                    "Conejo": "🐇", "Hamster": "🐹", "Pez": "🐠",
                    "Tortuga": "🐢", "Serpiente": "🐍", "Lagarto": "🦎"
                }

                row, col = 0, 0
                max_cols = 3

                for i, (especie, cantidad) in enumerate(stats['por_especie'].items()):
                    color = colores[i % len(colores)]
                    icono = iconos.get(especie, "🐾")

                    card = EspecieCard(especie, cantidad, stats['total'], color, icono)
                    self.especies_grid.addWidget(card, row, col)

                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1

                if mascotas:
                    mascota_pesada = max(mascotas, key=lambda m: m.peso)
                    self.labels['peso_max'].setText(
                        f"{mascota_pesada.nombre} ({mascota_pesada.peso:.2f} kg) - {mascota_pesada.especie}"
                    )

                    mascota_liviana = min(mascotas, key=lambda m: m.peso)
                    self.labels['peso_min'].setText(
                        f"{mascota_liviana.nombre} ({mascota_liviana.peso:.2f} kg) - {mascota_liviana.especie}"
                    )

                    promedios = []
                    for especie in stats['por_especie'].keys():
                        mascotas_especie = [m for m in mascotas if m.especie == especie]
                        if mascotas_especie:
                            promedio = sum(m.peso for m in mascotas_especie) / len(mascotas_especie)
                            promedios.append(f"{especie}: {promedio:.2f} kg")

                    self.labels['promedio_especie'].setText(
                        ", ".join(promedios[:3]) + ("..." if len(promedios) > 3 else "")
                    )

                    especie_comun = max(stats['por_especie'].items(), key=lambda x: x[1])
                    self.labels['especie_comun'].setText(f"{especie_comun[0]} ({especie_comun[1]})")

        except Exception as e:
            print(f"❌ Error al actualizar estadísticas: {e}")

    # ===== MÉTODOS DE SERVICIO =====

    def set_service(self, service):
        """Asigna el servicio y carga los datos iniciales."""
        self.service = service
        self.cargar_pagina_actual()

    def on_doble_click(self, index):
        """Maneja el doble clic en la tabla."""
        id_index = self.modelo.index(index.row(), 0)
        mascota_id = self.modelo.data(id_index, Qt.DisplayRole)

        if mascota_id:
            try:
                self.editar_solicitado.emit(int(mascota_id))
            except ValueError:
                self.mostrar_mensaje("Error", "ID de mascota no válido", "error")

    def ajustar_columnas(self):
        """Ajusta las columnas para que ocupen todo el ancho disponible."""
        header = self.tabla.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def refrescar(self):
        """Refresca los datos después de operaciones CRUD."""
        # Volver a la primera página
        self.pagina_actual = 1
        self.filtro_actual = ""
        self.buscar_input.clear()
        self.cargar_pagina_actual()

        # Actualizar estadísticas si estamos en esa pestaña
        if self.tabs.currentIndex() == 1:
            self.actualizar_estadisticas()

    # ===== MÉTODOS DE EXPORTACIÓN =====

    def exportar_csv(self):
        """Exporta el listado actual a CSV."""
        if not self.service:
            self.mostrar_mensaje("Error", "Servicio no disponible", "error")
            return

        try:
            with self.service as s:
                # Obtener todas las mascotas (sin paginación)
                mascotas = s.obtener_todos()

                from services.export_service import ExportService
                ExportService.exportar_a_csv(mascotas, self)

        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {str(e)}", "error")

    def exportar_pdf(self):
        """Exporta el listado actual a PDF."""
        if not self.service:
            self.mostrar_mensaje("Error", "Servicio no disponible", "error")
            return

        try:
            with self.service as s:
                # Obtener todas las mascotas (sin paginación)
                mascotas = s.obtener_todos()

                from services.export_service import ExportService
                ExportService.exportar_a_pdf(mascotas, self)

        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {str(e)}", "error")

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje al usuario."""
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)

        if tipo == "error":
            msg.setIcon(QMessageBox.Critical)
        elif tipo == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif tipo == "success":
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setIcon(QMessageBox.Information)

        msg.exec()