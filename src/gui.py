import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)

class VolumePredictorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📦 AI Volume Predictor")
        self.setGeometry(100, 100, 300, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.length_input = self.create_input(layout, "Length (inches):")
        self.width_input = self.create_input(layout, "Width (inches):")
        self.height_input = self.create_input(layout, "Height (inches):")
        self.weight_input = self.create_input(layout, "Weight (kg):")

        self.predict_button = QPushButton("Predict Volume")
        self.predict_button.clicked.connect(self.predict_volume)
        layout.addWidget(self.predict_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def create_input(self, layout, label_text):
        label = QLabel(label_text)
        layout.addWidget(label)
        input_field = QLineEdit()
        layout.addWidget(input_field)
        return input_field

    def predict_volume(self):
        try:
            # Gather input values
            data = {
                "length_inc": float(self.length_input.text()),
                "width_inc": float(self.width_input.text()),
                "height_inc": float(self.height_input.text()),
                "weight_kg": float(self.weight_input.text())
            }

            # Send request to Flask API
            response = requests.post("http://127.0.0.1:5000/predict", json=data)

            if response.status_code == 200:
                result = response.json()
                volume = result['predicted_volume_cm3']
                self.result_label.setText(f"📦 Predicted Volume: {volume} cm³")
            else:
                error = response.json().get('error', 'Unknown error')
                self.show_error(f"API Error: {error}")

        except ValueError:
            self.show_error("❌ Please enter valid numbers in all fields.")
        except Exception as e:
            self.show_error(f"❌ Unexpected error: {str(e)}")

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VolumePredictorApp()
    window.show()
    sys.exit(app.exec_())
