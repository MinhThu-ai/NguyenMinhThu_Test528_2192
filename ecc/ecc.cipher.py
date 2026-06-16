import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ecc import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton_3.clicked.connect(self.call_api_gen_keys)
        self.pushButton.clicked.connect(self.call_api_sign)
        self.pushButton_2.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Thông báo", data["message"])
            else:
                QMessageBox.warning(self, "Lỗi", "Không gọi được API tạo khóa")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"

        payload = {
            "message": self.textBrowser.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.textBrowser_2.setPlainText(data["signature"])
                QMessageBox.information(self, "Thông báo", "Signed Successfully")
            else:
                QMessageBox.warning(self, "Lỗi", "Không gọi được API ký")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"

        payload = {
            "message": self.textBrowser.toPlainText(),
            "signature": self.textBrowser_2.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                if data["is_verified"]:
                    QMessageBox.information(self, "Thông báo", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Thông báo", "Verified Fail")
            else:
                QMessageBox.warning(self, "Lỗi", "Không gọi được API xác minh")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi", str(e))


if __name__ == "__main__":
    print("Đang mở giao diện ECC...")

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    sys.exit(app.exec_())