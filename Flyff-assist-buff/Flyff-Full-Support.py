# Build with pain by Zogby :v
import sys
import time
import random
import threading
import keyboard
import win32gui
import win32con

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QSpinBox, QTabWidget, QPushButton, QHBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QFont


class KeySpammerThread(threading.Thread):
    def __init__(self, get_window_func, get_key_func, get_min_delay, get_max_delay):
        super().__init__(daemon=True)
        self.get_window_func = get_window_func
        self.get_key = get_key_func
        self.get_min_delay = get_min_delay
        self.get_max_delay = get_max_delay
        self.running = False

    def run(self):
        while True:
            if self.running:
                hwnd = self.get_window_func()
                key = self.get_key()
                
                if hwnd:
                    # Kirim input langsung ke window
                    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord(key), 0)
                    time.sleep(0.05)
                    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord(key), 0)
                
                time.sleep(random.uniform(self.get_min_delay(), self.get_max_delay()))
            else:
                time.sleep(0.1)

    def toggle(self):
        self.running = not self.running
        return self.running


class DualBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlyFF Dual Login + Key Spammer")
        self.resize(1024, 720)

        # Variabel untuk menyimpan window handles
        self.window_handles = {"Login 1": None, "Login 2": None}
        
        # Layout utama
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Browser 1
        self.browser1 = QWebEngineView()
        self.browser1.load(QUrl("https://universe.flyff.com"))
        self.tabs.addTab(self.browser1, "Login 1")

        # Browser 2
        self.browser2 = QWebEngineView()
        self.browser2.load(QUrl("https://universe.flyff.com"))
        self.tabs.addTab(self.browser2, "Login 2")

        # Timer untuk update window handles
        self.handle_timer = QTimer()
        self.handle_timer.timeout.connect(self.update_window_handles)
        self.handle_timer.start(1000)  

        # Tab pengaturan
        self.init_key_spammer_tab()

        # Thread spammer
        self.key_spammer = KeySpammerThread(
            self.get_target_window,
            self.get_selected_key,
            self.get_min_delay,
            self.get_max_delay,
        )
        self.key_spammer.start()

        # Hotkey
        keyboard.add_hotkey("F6", self.toggle_spammer_ui)

    def update_window_handles(self):
        """Update window handles secara periodic"""
        if self.browser1.winId():
            self.window_handles["Login 1"] = int(self.browser1.winId())
        if self.browser2.winId():
            self.window_handles["Login 2"] = int(self.browser2.winId())

    def init_key_spammer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Auto Key Spammer")
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)

        # Target browser selection
        layout.addWidget(QLabel("Target browser:"))
        self.target_tab_combo = QComboBox()
        self.target_tab_combo.addItems(["Login 1", "Login 2"])
        layout.addWidget(self.target_tab_combo)

        # Key selection
        layout.addWidget(QLabel("Key yang akan di-spam:"))
        self.key_combo = QComboBox()
        self.key_combo.addItems(["F1", "F2", "1", "2", "Q", "E"])
        layout.addWidget(self.key_combo)

        # Delay settings
        delay_layout = QHBoxLayout()
        min_layout = QVBoxLayout()
        min_layout.addWidget(QLabel("Min delay (s):"))
        self.min_spin = QSpinBox()
        self.min_spin.setRange(1, 30)
        self.min_spin.setValue(2)
        min_layout.addWidget(self.min_spin)
        delay_layout.addLayout(min_layout)
        
        max_layout = QVBoxLayout()
        max_layout.addWidget(QLabel("Max delay (s):"))
        self.max_spin = QSpinBox()
        self.max_spin.setRange(1, 30)
        self.max_spin.setValue(4)
        max_layout.addWidget(self.max_spin)
        delay_layout.addLayout(max_layout)
        layout.addLayout(delay_layout)

        # Toggle button
        self.toggle_button = QPushButton("Aktifkan Auto Spammer (F6)")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_spammer_ui)
        layout.addWidget(self.toggle_button)

        # Status
        self.status_label = QLabel("Status: Tidak Aktif")
        layout.addWidget(self.status_label)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Key Spammer")

    def toggle_spammer_ui(self):
        is_running = self.key_spammer.toggle()
        self.toggle_button.setChecked(is_running)
        if is_running:
            self.toggle_button.setText("Matikan Auto Spammer (F6)")
            self.status_label.setText(f"Status: AKTIF - Spamming {self.get_selected_key()} ke {self.target_tab_combo.currentText()}")
        else:
            self.toggle_button.setText("Aktifkan Auto Spammer (F6)")
            self.status_label.setText("Status: Tidak Aktif")

    def get_target_window(self):
        target = self.target_tab_combo.currentText()
        return self.window_handles.get(target)

    def get_selected_key(self):
        return self.key_combo.currentText()

    def get_min_delay(self):
        return self.min_spin.value()

    def get_max_delay(self):
        return self.max_spin.value()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DualBrowserApp()
    win.show()
    sys.exit(app.exec_())