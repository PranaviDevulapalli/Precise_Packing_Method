import sys
import joblib
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Load trained model
model = joblib.load("F:\SaiU\semester 4\Sri\models\packing_model.pkl")

class PackagingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI Packaging Predictor")
        self.setGeometry(100, 100, 300, 300)

        # Labels and Inputs
        self.weight_label = QLabel("Weight (kg):")
        self.weight_input = QLineEdit()

        self.length_label = QLabel("Length (cm):")
        self.length_input = QLineEdit()

        self.width_label = QLabel("Width (cm):")
        self.width_input = QLineEdit()

        self.height_label = QLabel("Height (cm):")
        self.height_input = QLineEdit()

        # Predict Button
        self.predict_button = QPushButton("Predict Packaging")
        self.predict_button.clicked.connect(self.predict_packaging)

        # Result Label
        self.result_label = QLabel("Prediction: ")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_input)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def predict_packaging(self):
        try:
            # Strip spaces and check if any field is empty
            weight_text = self.weight_input.text().strip()
            length_text = self.length_input.text().strip()
            width_text = self.width_input.text().strip()
            height_text = self.height_input.text().strip()

            if not weight_text or not length_text or not width_text or not height_text:
                raise ValueError("All fields must be filled")

            weight = float(weight_text)
            length = float(length_text)
            width = float(width_text)
            height = float(height_text)

            # Compute volume
            volume = length * width * height

            # Create DataFrame with correct column names
            input_data = pd.DataFrame([[weight, length, width, height, volume]],
                                      columns=["Weight (kg)", "Length", "Width", "Height", "Volume"])

            # Predict
            prediction = model.predict(input_data)[0]
            self.result_label.setText(f"Prediction: {prediction}")

        except ValueError:
            self.result_label.setText("Error: Enter valid numbers!")

# Run GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackagingApp()
    window.show()
    sys.exit(app.exec_())
