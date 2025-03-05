from pathlib import Path
import os
from PySide6 import QtWidgets, QtCore

class AssetManagerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Manager")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QtWidgets.QVBoxLayout()
        
        # Directory Selection
        self.dir_label = QtWidgets.QLabel("Select Asset Directory:")
        self.layout.addWidget(self.dir_label)
        
        self.dir_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.dir_input)
        
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        self.layout.addWidget(self.browse_button)
        
        # File List
        self.file_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.file_list)
        
        # Load Files Button
        self.load_button = QtWidgets.QPushButton("Load Files")
        self.load_button.clicked.connect(self.load_files)
        self.layout.addWidget(self.load_button)
        
        # Import & Reference Buttons
        self.import_button = QtWidgets.QPushButton("Import File")
        self.import_button.clicked.connect(self.import_file)
        self.layout.addWidget(self.import_button)
        
        self.reference_button = QtWidgets.QPushButton("Reference File")
        self.reference_button.clicked.connect(self.reference_file)
        self.layout.addWidget(self.reference_button)
        
        self.setLayout(self.layout)
    
    def browse_directory(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.dir_input.setText(dir_path)
    
    def load_files(self):
        directory = self.dir_input.text()
        if not directory:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a directory.")
            return
        
        self.file_list.clear()
        files = list_files(directory, extensions=['.ma', '.mb'])
        self.file_list.addItems(files)
    
    def import_file(self):
        directory = self.dir_input.text()
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file to import.")
            return
        
        filename = selected_items[0].text()
        print(f"Simulating import of file: {filename}")
    
    def reference_file(self):
        directory = self.dir_input.text()
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file to reference.")
            return
        
        filename = selected_items[0].text()
        print(f"Simulating reference of file: {filename}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AssetManagerUI()
    window.show()
    app.exec()