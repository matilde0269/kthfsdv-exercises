import sys
import numpy as np
from datetime import datetime
import csv

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QCheckBox, QSlider
)
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph as pg


class BaseFunctionPlotter:
    """
    Base class to handle math logic for h(t).
    Tried to separate calculations from GUI elements following good practice.
    """

    def __init__(self, sample_rate=100.0):
        # Setting loop frequency at 100 Hz (dt = 0.01s) similar to ROS node rate loops
        self.sample_rate = sample_rate  
        self.dt = 1.0 / self.sample_rate

    def compute_h(self, t):
        # Formula: h(t) = 3 * pi * exp(-lambda(t))
        # lambda(t) = 5 * sin(2 * pi * 1 * t) -> frequency is 1 Hz
        lambda_t = 5.0 * np.sin(2.0 * np.pi * 1.0 * t)
        return 3.0 * np.pi * np.exp(-lambda_t)


class LivePlotterGUI(QMainWindow, BaseFunctionPlotter):
    """
    Child class for GUI implementation using PyQt5 and pyqtgraph.
    Inherits math calculations from BaseFunctionPlotter.
    """

    def __init__(self):
        QMainWindow.__init__(self)
        BaseFunctionPlotter.__init__(self, sample_rate=100.0)

        # Buffer arrays to store time-series data
        self.current_t = 0.0
        self.t_data = []
        self.h_data = []
        self.window_size = 5.0  # Default display window in seconds

        # QTimer acts like a ROS timer callback triggering data updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("kthfsdv-plotting: h(t) Real-Time Visualizer")
        self.resize(1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # --- Left Panel: Plot Area ---
        self.plot_widget = pg.PlotWidget(title="h(t) = 3·π·exp(-5·sin(2·π·t))")
        self.plot_widget.setLabel('left', 'h(t)')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.plot_widget.showGrid(x=True, y=True)
        
        # Pen configuration for fast real-time rendering
        self.curve = self.plot_widget.plot(pen=pg.mkPen(color='cyan', width=2))
        main_layout.addWidget(self.plot_widget, stretch=3)

        # --- Right Panel: Controls ---
        controls_layout = QVBoxLayout()
        
        # Input field for experiment name metadata
        controls_layout.addWidget(QLabel("Experiment Name:"))
        self.exp_name_input = QLineEdit("experiment_1")
        controls_layout.addWidget(self.exp_name_input)

        # Control buttons
        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.start_plotting)
        controls_layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop_plotting)
        controls_layout.addWidget(self.btn_stop)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_plotting)
        controls_layout.addWidget(self.btn_reset)

        # Toggle grid overlay
        self.grid_checkbox = QCheckBox("Show Grid")
        self.grid_checkbox.setChecked(True)
        self.grid_checkbox.stateChanged.connect(self.toggle_grid)
        controls_layout.addWidget(self.grid_checkbox)

        # Slider for horizontal axis zoom/windowing
        controls_layout.addWidget(QLabel("X-Axis Window (Zoom in s):"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(1)
        self.zoom_slider.setMaximum(20)
        self.zoom_slider.setValue(int(self.window_size))
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        controls_layout.addWidget(self.zoom_slider)

        # Export features
        self.btn_save = QPushButton("Save CSV")
        self.btn_save.clicked.connect(self.save_to_csv)
        controls_layout.addWidget(self.btn_save)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, stretch=1)

    def update_data(self):
        """Simulates incoming stream data at each clock tick (callback style)."""
        self.current_t += self.dt
        h_val = self.compute_h(self.current_t)

        self.t_data.append(self.current_t)
        self.h_data.append(h_val)

        # Re-render plot curve
        self.curve.setData(self.t_data, self.h_data)

        # Auto-scroll X axis to maintain live streaming window effect
        if self.current_t > self.window_size:
            self.plot_widget.setXRange(self.current_t - self.window_size, self.current_t)

    def start_plotting(self):
        # 10ms interval = 100 Hz execution loop
        if not self.timer.isActive():
            self.timer.start(10)

    def stop_plotting(self):
        self.timer.stop()

    def reset_plotting(self):
        # Clear data structures and reset timestamps
        self.stop_plotting()
        self.current_t = 0.0
        self.t_data.clear()
        self.h_data.clear()
        self.curve.setData([], [])
        self.plot_widget.setXRange(0, self.window_size)

    def toggle_grid(self, state):
        show = (state == Qt.Checked)
        self.plot_widget.showGrid(x=show, y=show)

    def update_zoom(self, value):
        self.window_size = float(value)
        if self.current_t > self.window_size:
            self.plot_widget.setXRange(self.current_t - self.window_size, self.current_t)
        else:
            self.plot_widget.setXRange(0, self.window_size)

    def save_to_csv(self):
        # Export experiment data with timestamp header
        exp_name = self.exp_name_input.text().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{exp_name}_{timestamp}.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Experiment", exp_name])
            writer.writerow(["Date_Time", timestamp])
            writer.writerow(["Timestamp_s", "h_t"])
            for t, h in zip(self.t_data, self.h_data):
                writer.writerow([f"{t:.4f}", f"{h:.6f}"])

        print(f"[INFO] Data exported to: {filename}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LivePlotterGUI()
    window.show()
    sys.exit(app.exec_())
