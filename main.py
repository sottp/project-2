from logic import *
# something about first numbers stop working

def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()
