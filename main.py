import sys
from PyQt5.QtWidgets import QApplication
from ui_main import RenamerUI

def main():
    app = QApplication(sys.argv)
    window = RenamerUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
