from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton, QSlider, QFormLayout, QLabel
import forceLogin
import searchQuery
import EndpointFuzzer
import LatencyFuzzer
import SelViewOtherBasket
import AdditionalItemInBasket
import sys
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		loginButton = QPushButton("Forced Login Methods")
		loginButton.setFixedSize(160,90)
		loginButton.clicked.connect(self.show_login)
		
		htmlButton = QPushButton("HTML Manipulation")
		htmlButton.setFixedSize(160,90)

		sqlButton = QPushButton("SQL Injection")
		sqlButton.setFixedSize(160,90)	
		sqlButton.pressed.connect(self.search_query)
		
		apiButton = QPushButton("API Endpoint Scanner")
		apiButton.setFixedSize(160,90)		
		apiButton.pressed.connect(self.endpoint_fuzz)

		latencyButton = QPushButton("Latency Tester")
		latencyButton.setFixedSize(160,90)
		latencyButton.pressed.connect(self.latency_fuzz)

		self.DictButton = QPushButton("Dictionary Attack")
		self.DictButton.pressed.connect(self.start_dict)
		self.DictButton.setFixedSize(160, 90)
		self.DictButton.setVisible(False)		

		self.threads = 1
		self.threadSlider = QSlider(Qt.Orientation.Horizontal, self)
		self.threadSlider.setRange(1,8)
		self.threadSlider.setSingleStep(1)
		self.threadSlider.setFixedSize(160, 20)
		self.threadSlider.valueChanged.connect(self.update_threads)
		self.threadSlider.setVisible(False)

		self.threadLabel = QLabel('Brute Force Thread Count: 1', self)
		self.threadLabel.setFixedSize(160, 20)
		self.threadLabel.setVisible(False)

		self.BruteButton = QPushButton("Brute Force Attack")
		self.BruteButton.setFixedSize(160, 90)
		self.BruteButton.pressed.connect(self.start_brute)
		self.BruteButton.setVisible(False)	

		self.layout = QVBoxLayout()
		self.layout.addWidget(loginButton)
		self.layout.addWidget(htmlButton)
		self.layout.addWidget(sqlButton)
		self.layout.addWidget(apiButton)
		self.layout.addWidget(latencyButton)

		self.layout.addWidget(self.DictButton)
		self.layout.addWidget(self.BruteButton)
		self.layout.addWidget(self.threadSlider)
		self.layout.addWidget(self.threadLabel)

		self.setLayout(self.layout)

	def show_login(self):
		self.DictButton.setVisible(not self.DictButton.isVisible())
		self.BruteButton.setVisible(self.DictButton.isVisible())
		self.threadSlider.setVisible(self.DictButton.isVisible())
		self.threadLabel.setVisible(self.DictButton.isVisible())

	def start_brute(self):
		#print("Starting Brute Force Tester")
		forceLogin.begin("brute", "admin@juice-sh.op", self.threads)
	def start_dict(self):
		#print("Starting Dictionary Attack")
		forceLogin.begin("dict", "admin@juice-sh.op", 1)	
	def update_threads(self, value):
		self.threads = value
		self.threadLabel.setText(f"Brute Force Thread Count: {value}")
	def search_query(self):
		searchQuery.main()
	def endpoint_fuzz(self):
		EndpointFuzzer.main()
	def latency_fuzz(self):
		LatencyFuzzer.main()

def main():
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	app.exec()

main()
