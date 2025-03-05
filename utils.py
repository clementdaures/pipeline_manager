from pathlib import Path
import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore

class AssetManagerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maya Asset Manager")
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
        import_file(directory, filename)
    
    def reference_file(self):
        directory = self.dir_input.text()
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file to reference.")
            return
        
        filename = selected_items[0].text()
        import_file_as_reference(directory, filename)

# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AssetManagerUI()
    window.show()
    app.exec()

def list_files(directory: str, extensions=None):
    """
    Lists all files in the given directory, optionally filtering by extensions.
    
    :param directory: Path to the directory
    :param extensions: List of file extensions to filter (e.g., ['.ma', '.mb'])
    :return: List of file names (List[str])
    """
    try:
        path = Path(directory)
        if not path.exists():
            print("Error: Directory not found.")
            return []
        
        files = [f.name for f in path.iterdir() if f.is_file()]
        if extensions:
            files = [f for f in files if Path(f).suffix in extensions]
        return files
    except PermissionError:
        print("Error: Permission denied.")
        return []

def import_file_as_reference(directory: str, filename: str) -> None:
    """
    Imports a specified file as a reference into Maya.
    
    :param directory: Path to the directory containing the file
    :param filename: Name of the file to import as a reference
    :return: None
    """
    file_path = Path(directory) / filename
    if not file_path.exists():
        print(f"Error: File '{filename}' not found in '{directory}'.")
        return
    
    try:
        cmds.file(str(file_path), reference=True, ignoreVersion=True, namespace=filename.split('.')[0])
        print(f"Successfully referenced: {file_path}")
    except Exception as e:
        print(f"Error importing file: {e}")

def import_file(directory: str, filename: str) -> None:
    """
    Imports a file into Maya (not as a reference).
    
    :param directory: Path to the directory containing the file
    :param filename: Name of the file to import
    :return: None
    """
    file_path = Path(directory) / filename
    if not file_path.exists():
        print(f"Error: File '{filename}' not found in '{directory}'.")
        return
    try:
        cmds.file(str(file_path), i=True, ignoreVersion=True)
        print(f"Successfully imported: {file_path}")
    except Exception as e:
        print(f"Error importing file: {e}")
