"""
Servicio de Exportación - Permite exportar listados a diferentes formatos.
Soporta PDF y CSV (Excel).
"""

import csv
import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QTextDocument, QPageLayout, QPageSize
from PySide6.QtCore import QMargins  # [CORREGIDO] QMargins está en QtCore, no en QtGui
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtCore import Qt


class ExportService:
    """
    Servicio para exportar datos a diferentes formatos.
    """

    @staticmethod
    def exportar_a_csv(mascotas, parent=None):
        """
        Exporta la lista de mascotas a un archivo CSV.

        Args:
            mascotas: Lista de objetos Mascota
            parent: Widget padre para el diálogo

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        if not mascotas:
            QMessageBox.warning(parent, "Sin datos", "No hay mascotas para exportar.")
            return False

        # Obtener ruta para guardar
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_default = f"mascotas_{fecha}.csv"

        ruta, _ = QFileDialog.getSaveFileName(
            parent,
            "Guardar archivo CSV",
            os.path.expanduser(f"~/{nombre_default}"),
            "Archivos CSV (*.csv);;Todos los archivos (*.*)"
        )

        if not ruta:
            return False  # Usuario canceló

        try:
            with open(ruta, 'w', newline='', encoding='utf-8-sig') as archivo:
                writer = csv.writer(archivo)

                # Escribir encabezados
                writer.writerow(['ID', 'Nombre', 'Especie', 'Peso (kg)'])

                # Escribir datos
                for mascota in mascotas:
                    writer.writerow([
                        mascota.id,
                        mascota.nombre,
                        mascota.especie,
                        f"{mascota.peso:.2f}"
                    ])

            QMessageBox.information(
                parent,
                "Exportación exitosa",
                f"Datos exportados correctamente a:\n{ruta}"
            )
            return True

        except Exception as e:
            QMessageBox.critical(
                parent,
                "Error de exportación",
                f"No se pudo exportar a CSV:\n{str(e)}"
            )
            return False

    @staticmethod
    def exportar_a_pdf(mascotas, parent=None):
        """
        Exporta la lista de mascotas a un archivo PDF con formato profesional.

        Args:
            mascotas: Lista de objetos Mascota
            parent: Widget padre para el diálogo

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        if not mascotas:
            QMessageBox.warning(parent, "Sin datos", "No hay mascotas para exportar.")
            return False

        # Obtener ruta para guardar
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_default = f"mascotas_{fecha}.pdf"

        ruta, _ = QFileDialog.getSaveFileName(
            parent,
            "Guardar archivo PDF",
            os.path.expanduser(f"~/{nombre_default}"),
            "Archivos PDF (*.pdf);;Todos los archivos (*.*)"
        )

        if not ruta:
            return False  # Usuario canceló

        try:
            # Crear documento HTML
            html = ExportService._generar_html_reporte(mascotas)

            # Configurar impresor/PDF
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(ruta)

            # Establecer márgenes de página correctamente
            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.A4))
            page_layout.setOrientation(QPageLayout.Portrait)
            page_layout.setMargins(QMargins(20, 20, 20, 20))  # Márgenes en mm (20 mm = 2 cm)
            printer.setPageLayout(page_layout)

            # Crear documento y cargar HTML
            doc = QTextDocument()
            doc.setHtml(html)

            # Imprimir a PDF
            doc.print_(printer)

            QMessageBox.information(
                parent,
                "Exportación exitosa",
                f"PDF generado correctamente:\n{ruta}"
            )
            return True

        except Exception as e:
            QMessageBox.critical(
                parent,
                "Error de exportación",
                f"No se pudo exportar a PDF:\n{str(e)}"
            )
            return False

    @staticmethod
    def _generar_html_reporte(mascotas):
        """
        Genera el HTML para el reporte PDF.

        Args:
            mascotas: Lista de objetos Mascota

        Returns:
            str: HTML formateado
        """
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Calcular estadísticas para el resumen
        total = len(mascotas)
        especies = {}
        peso_total = 0

        for m in mascotas:
            especies[m.especie] = especies.get(m.especie, 0) + 1
            peso_total += m.peso

        peso_promedio = peso_total / total if total > 0 else 0

        # Generar filas de la tabla
        filas = ""
        for i, mascota in enumerate(mascotas, 1):
            filas += f"""
            <tr style="background-color: {'#f5f5f5' if i % 2 == 0 else '#ffffff'};">
                <td style="padding: 8px; text-align: center;">{mascota.id}</td>
                <td style="padding: 8px;">{mascota.nombre}</td>
                <td style="padding: 8px;">{mascota.especie}</td>
                <td style="padding: 8px; text-align: right;">{mascota.peso:.2f} kg</td>
            </tr>
            """

        # Generar resumen de especies
        especies_html = ""
        for especie, cantidad in especies.items():
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            especies_html += f"""
            <div style="margin-bottom: 5px;">
                <span style="font-weight: bold;">{especie}:</span> 
                {cantidad} ({porcentaje:.1f}%)
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Mascotas</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    color: #0078d7;
                    text-align: center;
                    border-bottom: 2px solid #0078d7;
                    padding-bottom: 10px;
                }}
                .fecha {{
                    text-align: right;
                    color: #666;
                    font-size: 11pt;
                    margin-bottom: 20px;
                }}
                .resumen {{
                    background-color: #f0f0f0;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .resumen-item {{
                    display: inline-block;
                    margin-right: 30px;
                    font-size: 12pt;
                }}
                .resumen-valor {{
                    font-weight: bold;
                    color: #0078d7;
                    font-size: 14pt;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th {{
                    background-color: #0078d7;
                    color: white;
                    padding: 10px;
                    text-align: left;
                }}
                td {{
                    border-bottom: 1px solid #ddd;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #999;
                    font-size: 10pt;
                }}
            </style>
        </head>
        <body>
            <h1>🐾 Sistema de Adopción de Mascotas</h1>
            <div class="fecha">Generado: {fecha_actual}</div>
            
            <div class="resumen">
                <div class="resumen-item">
                    <span>Total Mascotas:</span>
                    <span class="resumen-valor">{total}</span>
                </div>
                <div class="resumen-item">
                    <span>Peso Promedio:</span>
                    <span class="resumen-valor">{peso_promedio:.2f} kg</span>
                </div>
                <div class="resumen-item">
                    <span>Especies:</span>
                    <span class="resumen-valor">{len(especies)}</span>
                </div>
            </div>
            
            <h3>Distribución por Especie:</h3>
            {especies_html}
            
            <h3>Listado Detallado:</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Especie</th>
                        <th>Peso (kg)</th>
                    </tr>
                </thead>
                <tbody>
                    {filas}
                </tbody>
            </table>
            
            <div class="footer">
                Reporte generado automáticamente por PySide Mascotas
            </div>
        </body>
        </html>
        """

        return html