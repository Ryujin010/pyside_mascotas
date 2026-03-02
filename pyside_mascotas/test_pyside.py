import sys
from PySide6.QtWidgets import QApplication, QLabel

print("PySide6 cargado correctamente")
app = QApplication(sys.argv)
label = QLabel("¡Funciona!")
label.show()
sys.exit(app.exec())