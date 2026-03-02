"""
Vista Formulario - Pantalla para agregar/editar/eliminar mascotas.
Incluye validación básica y conexión con el servicio.
Ahora con botón Eliminar y confirmación.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QFormLayout, QLineEdit, QPushButton,
                               QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator


class FormView(QWidget):
    """
    Vista de formulario para agregar, editar o eliminar mascotas.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = None
        self.modo_edicion = False
        self.mascota_id = None
        self.callback_actualizar = None  # Función para actualizar el listado
        self.callback_volver = None      # Función para volver al home
        self.setup_ui()
        self.conectar_senales()

    def setup_ui(self):
        """Configura la interfaz de usuario del formulario."""

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)

        # Título del formulario
        self.titulo = QLabel("➕ Agregar Nueva Mascota")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #ffffff;
                padding: 15px;
                background-color: #353535;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.titulo)

        # Contenedor del formulario
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Campos del formulario
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: Luna, Max, Misi...")
        self.nombre_input.setMaxLength(100)
        self.nombre_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #353535;
                color: #ffffff;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
            QLineEdit:invalid {
                border-color: #dc3545;
            }
        """)

        self.especie_input = QLineEdit()
        self.especie_input.setPlaceholderText("Ej: Perro, Gato, Ave...")
        self.especie_input.setMaxLength(50)
        self.especie_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #353535;
                color: #ffffff;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)

        self.peso_input = QLineEdit()
        self.peso_input.setPlaceholderText("Ej: 12.5")
        self.peso_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #555555;
                border-radius: 5px;
                background-color: #353535;
                color: #ffffff;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)

        # Configurar validador para el peso (solo números decimales)
        peso_validator = QDoubleValidator()
        peso_validator.setBottom(0.01)  # Peso mínimo: 0.01 kg
        peso_validator.setTop(999.99)   # Peso máximo: 999.99 kg
        peso_validator.setDecimals(2)    # 2 decimales
        self.peso_input.setValidator(peso_validator)

        # Agregar campos al formulario
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Especie:", self.especie_input)
        form_layout.addRow("Peso (kg):", self.peso_input)

        layout.addWidget(form_container)

        # Contenedor de botones
        botones_container = QWidget()
        botones_layout = QHBoxLayout(botones_container)
        botones_layout.setSpacing(15)

        # [NUEVO] Botón Eliminar (solo visible en modo edición)
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """)
        self.btn_eliminar.setVisible(False)  # Oculto por defecto

        # Botón Guardar
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0086f0;
            }
            QPushButton:pressed {
                background-color: #0060b0;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
            }
        """)

        # Botón Cancelar
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7c858d;
            }
            QPushButton:pressed {
                background-color: #5a6268;
            }
        """)

        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_guardar)
        botones_layout.addWidget(self.btn_cancelar)
        botones_layout.addStretch()

        layout.addWidget(botones_container)
        layout.addStretch()

    def conectar_senales(self):
        """Conecta las señales de los botones."""
        self.btn_guardar.clicked.connect(self.procesar_guardado)
        self.btn_cancelar.clicked.connect(self.cancelar)
        # [NUEVO] Conectar botón eliminar
        self.btn_eliminar.clicked.connect(self.procesar_eliminacion)

    def set_service(self, service):
        """Asigna el servicio para acceso a datos."""
        self.service = service

    def set_callback_actualizar(self, callback):
        """
        Asigna la función que se llamará para actualizar el listado.

        Args:
            callback: Función sin argumentos que actualiza la tabla
        """
        self.callback_actualizar = callback

    def set_callback_volver(self, callback):
        """
        Asigna la función que se llamará para volver al home.

        Args:
            callback: Función sin argumentos que cambia a la vista home
        """
        self.callback_volver = callback

    def cargar_datos(self, mascota_id):
        """
        Carga los datos de una mascota en el formulario para edición.

        Args:
            mascota_id (int): ID de la mascota a editar

        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        if not self.service:
            self.mostrar_mensaje(
                "Error interno",
                "El servicio no está disponible",
                "error"
            )
            return False

        try:
            with self.service as s:
                mascota = s.obtener_por_id(mascota_id)

                # Llenar el formulario con los datos
                self.nombre_input.setText(mascota.nombre)
                self.especie_input.setText(mascota.especie)
                self.peso_input.setText(str(mascota.peso))

                # Guardar el ID para la operación de actualización
                self.mascota_id = mascota_id

                return True

        except ValueError as e:
            self.mostrar_mensaje("Error", str(e), "error")
            return False
        except Exception as e:
            self.mostrar_mensaje(
                "Error",
                f"No se pudo cargar la mascota: {str(e)}",
                "error"
            )
            return False

    def validar_campos(self):
        """
        Valida que los campos obligatorios no estén vacíos.

        Returns:
            tuple: (bool, str) - (válido, mensaje de error)
        """
        # Validar nombre
        nombre = self.nombre_input.text().strip()
        if not nombre:
            return False, "El nombre es obligatorio"
        if len(nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"

        # Validar especie
        especie = self.especie_input.text().strip()
        if not especie:
            return False, "La especie es obligatoria"
        if len(especie) < 2:
            return False, "La especie debe tener al menos 2 caracteres"

        # Validar peso
        peso_texto = self.peso_input.text().strip()
        if not peso_texto:
            return False, "El peso es obligatorio"

        try:
            peso = float(peso_texto)
            if peso <= 0:
                return False, "El peso debe ser mayor a 0"
            if peso > 1000:
                return False, "El peso no puede ser mayor a 1000 kg"
        except ValueError:
            return False, "El peso debe ser un número válido"

        return True, ""

    def procesar_guardado(self):
        """
        Procesa el guardado de una mascota en la base de datos.
        """
        # Validar que el servicio esté disponible
        if not self.service:
            self.mostrar_mensaje(
                "Error interno",
                "El servicio no está disponible",
                "error"
            )
            return

        # Validar campos
        valido, mensaje = self.validar_campos()
        if not valido:
            self.mostrar_mensaje("Error de validación", mensaje, "error")
            return

        # Recoger datos del formulario
        datos = {
            'nombre': self.nombre_input.text().strip(),
            'especie': self.especie_input.text().strip(),
            'peso': float(self.peso_input.text().strip())
        }

        try:
            with self.service as s:
                if self.modo_edicion:
                    # Modo edición - actualizar mascota existente
                    mascota_actualizada = s.actualizar(self.mascota_id, datos)

                    self.mostrar_mensaje(
                        "✅ Éxito",
                        f"Mascota actualizada correctamente:\n"
                        f"ID: {mascota_actualizada.id}\n"
                        f"Nombre: {mascota_actualizada.nombre}\n"
                        f"Especie: {mascota_actualizada.especie}\n"
                        f"Peso: {mascota_actualizada.peso} kg",
                        "success"
                    )
                else:
                    # Modo creación - guardar nueva mascota
                    nueva_mascota = s.crear(datos)

                    self.mostrar_mensaje(
                        "✅ Éxito",
                        f"Mascota '{datos['nombre']}' guardada correctamente.\n"
                        f"ID asignado: {nueva_mascota.id}",
                        "success"
                    )

            # Actualizar el listado si hay callback
            if self.callback_actualizar:
                self.callback_actualizar()

            # Volver al home
            self.cancelar()

        except ValueError as e:
            self.mostrar_mensaje("Error de validación", str(e), "error")
        except Exception as e:
            self.mostrar_mensaje(
                "Error al guardar",
                f"No se pudo guardar la mascota:\n{str(e)}",
                "error"
            )

    # [NUEVO] Procesar eliminación de mascota
    def procesar_eliminacion(self):
        """
        Procesa la eliminación de una mascota con confirmación.
        """
        if not self.mascota_id:
            self.mostrar_mensaje(
                "Error",
                "No hay una mascota seleccionada para eliminar",
                "error"
            )
            return

        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "⚠️ Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la mascota?\n\n"
            f"ID: {self.mascota_id}\n"
            f"Nombre: {self.nombre_input.text().strip()}\n"
            f"Especie: {self.especie_input.text().strip()}\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return  # Usuario canceló

        try:
            with self.service as s:
                s.eliminar(self.mascota_id)

            self.mostrar_mensaje(
                "✅ Eliminado",
                f"La mascota con ID {self.mascota_id} ha sido eliminada correctamente.",
                "success"
            )

            # Actualizar el listado si hay callback
            if self.callback_actualizar:
                self.callback_actualizar()

            # Volver al home
            self.cancelar()

        except ValueError as e:
            self.mostrar_mensaje("Error", str(e), "error")
        except Exception as e:
            self.mostrar_mensaje(
                "Error al eliminar",
                f"No se pudo eliminar la mascota:\n{str(e)}",
                "error"
            )

    def cancelar(self):
        """Vuelve a la vista de inicio sin guardar."""
        self.limpiar_campos()
        if self.callback_volver:
            self.callback_volver()

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """
        Muestra un mensaje al usuario.

        Args:
            titulo: Título del mensaje
            mensaje: Contenido del mensaje
            tipo: "info", "error", "warning", "success"
        """
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

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.nombre_input.clear()
        self.especie_input.clear()
        self.peso_input.clear()

    def configurar_modo_edicion(self, activo):
        """
        Configura el formulario para modo edición o creación.

        Args:
            activo: True para modo edición, False para creación
        """
        self.modo_edicion = activo
        if activo:
            self.titulo.setText("✏️ Editar Mascota")
            self.btn_guardar.setText("💾 Actualizar")
            self.btn_eliminar.setVisible(True)  # [NUEVO] Mostrar botón eliminar
        else:
            self.titulo.setText("➕ Agregar Nueva Mascota")
            self.btn_guardar.setText("💾 Guardar")
            self.btn_eliminar.setVisible(False)  # [NUEVO] Ocultar botón eliminar
            self.mascota_id = None
            self.limpiar_campos()