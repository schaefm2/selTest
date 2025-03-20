from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton, QSlider, QFormLayout, QLabel
import forceLogin
import searchQuery
import EndpointFuzzer
import LatencyFuzzer
import SelViewOtherBasket
import AdditionalItemInBasket
import sys
from PyQt6.QtCore import Qt


def add_button(text, fun, vis):
	out = QPushButton(text)
	out.setFixedSize(160, 90)
	out.setVisible(vis)
	out.pressed.connect(fun)
	return out


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.buttons = []
		self.login_buttons = []
		self.html_buttons = []
		self.buttons.append(add_button("Forced Login Methods", self.show_login, True))
		self.buttons.append(add_button("HTML Manipulation", self.show_html, True))
		self.buttons.append(add_button("SQL Injection", self.search_query, True))
		self.buttons.append(add_button("API Endpoint Scanner", self.endpoint_fuzz, True))
		self.buttons.append(add_button("Latency Tester", self.latency_fuzz, True))
		self.buttons.append(add_button("Login: Dictionary Attack", self.start_dict, False))
		self.login_buttons.append(self.buttons[-1])

		self.threads = 1
		self.threadSlider = QSlider(Qt.Orientation.Horizontal, self)
		self.threadSlider.setRange(1,8)
		self.threadSlider.setSingleStep(1)
		self.threadSlider.setFixedSize(160, 20)
		self.threadSlider.valueChanged.connect(self.update_threads)
		self.threadSlider.setVisible(False)
		self.buttons.append(self.threadSlider)
		self.login_buttons.append(self.buttons[-1])

		self.threadLabel = QLabel(f'Brute Force Thread Count: {self.threads}', self)
		self.threadLabel.setFixedSize(160, 20)
		self.threadLabel.setVisible(False)
		self.buttons.append(self.threadLabel)
		self.login_buttons.append(self.buttons[-1])

		self.buttons.append("Login: Brute Force Attack", self.start_brute, False)
		self.login_buttons.append(self.buttons[-1])

		self.buttons.append(add_button("HTML: Add Items", additional, False))
		self.html_buttons.append(self.buttons[-1])
		self.buttons.append(add_button("HTML: View Another's Basket", view_basket, False))
		self.html_buttons.append(self.buttons[-1])

		for button in self.buttons:
			self.layout.addWidget(button)
		
		self.setLayout(self.layout)

	def show_login(self):
		state = not self.login_buttons[0].isVisible()
		for button in self.login_buttons:
			button.setVisible(state)
	def show_html(self):
		state = not self.html_buttons[0].isVisible()
		for button in self.html_buttons:
			button.setVisible(state)

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
	def view_basket(self):
		SelViewOtherBasket.main()
	def additional(self):
		AdditionalItemInBasket.main()

def main():
	app = QApplication(sys.argv)
	w = MainWindow()
	w.show()
	app.exec()

main()
