from ui.main_window import HomeChefApp

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = HomeChefApp()
    window.show()
    sys.exit(app.exec_())
