import sys
import os
import pandas as pd
import dbf
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QFileDialog, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt

class ExcelToDbfApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.excel_path = None

    def initUI(self):
        self.setWindowTitle('Conversor de Excel a DBF')
        self.resize(450, 200)

        # Layout principal
        layout = QVBoxLayout()

        self.label = QLabel('Selecciona un archivo Excel (.xlsx o .xls)')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(self.label)

        self.btn_select = QPushButton('Seleccionar Archivo')
        self.btn_select.setMinimumHeight(40)
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)

        self.btn_convert = QPushButton('Convertir a DBF')
        self.btn_convert.setMinimumHeight(40)
        self.btn_convert.clicked.connect(self.convert_file)
        self.btn_convert.setEnabled(False)
        layout.addWidget(self.btn_convert)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Excel", "", "Archivos Excel (*.xlsx *.xls)"
        )
        if file_name:
            self.excel_path = file_name
            self.label.setText(f'Archivo: {os.path.basename(file_name)}')
            self.btn_convert.setEnabled(True)
            self.progress.setValue(0)

    def convert_file(self):
        if not self.excel_path:
            return

        try:
            self.btn_convert.setEnabled(False)
            self.progress.setValue(10)
            
            # 1. Leer el Excel
            df = pd.read_excel(self.excel_path)
            self.progress.setValue(40)

            output_path = os.path.splitext(self.excel_path)[0] + '.dbf'

            # 2. Construir el esquema para el archivo DBF
            # DBF solo permite nombres de columna de hasta 10 caracteres
            schema = []
            for col in df.columns:
                clean_name = str(col).replace(' ', '_').replace('-', '_')[:10]
                dtype = df[col].dtype

                if pd.api.types.is_integer_dtype(dtype):
                    schema.append(f"{clean_name} N(18,0)")
                elif pd.api.types.is_float_dtype(dtype):
                    schema.append(f"{clean_name} N(18,5)")
                elif pd.api.types.is_datetime64_any_dtype(dtype):
                    schema.append(f"{clean_name} D")
                elif pd.api.types.is_bool_dtype(dtype):
                    schema.append(f"{clean_name} L")
                else:
                    schema.append(f"{clean_name} C(250)")

            schema_str = "; ".join(schema)
            self.progress.setValue(60)

            # 3. Crear la tabla DBF (cp1252 asegura tildes y eñes)
            table = dbf.Table(output_path, schema_str, codepage='cp1252')
            table.open(mode=dbf.READ_WRITE)

            # 4. Procesar y limpiar los datos para insertar
            for _, row in df.iterrows():
                record = []
                for val in row:
                    if pd.isna(val):
                        record.append(None)
                    elif isinstance(val, str):
                        # Truncar textos para evitar que rompan el límite del esquema DBF
                        record.append(val[:250])
                    else:
                        record.append(val)
                table.append(tuple(record))

            table.close()
            self.progress.setValue(100)
            QMessageBox.information(self, "Éxito", f"Conversión completada.\nGuardado en:\n{output_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al convertir:\n{str(e)}")
            self.progress.setValue(0)
        finally:
            self.btn_convert.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Aplicar el estilo nativo 'Fusion' de PyQt para que se vea bien en Mac y Windows
    app.setStyle('Fusion') 
    ex = ExcelToDbfApp()
    ex.show()
    sys.exit(app.exec())