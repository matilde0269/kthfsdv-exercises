# KTH Formula Student Driverless - Recruitment Exercises

This repository contains the recruitment exercises for KTH Formula Student Driverless.

---

## Exercise 1 - ROS 2 System Development

Implementation of two ROS 2 nodes for data stream creation, processing, and real-time visualization.

### System Overview
- **`package1 / nodeA`**: Publishes an increasing integer sequence at 20 Hz to topic `/lourenco`.
- **`package2 / nodeB`**: Subscribes to `/lourenco`, divides incoming values by $q = 0.15$, and publishes the output to `/kthfs/result`.

### Setup & Requirements
- **OS**: Ubuntu 24.04 (via Docker)
- **ROS 2 Distribution**: Jazzy Jalisco
- **Dependencies**: Standard `std_msgs` package and `PlotJuggler` for plotting.

### How to Build & Run

1. **Setup workspace and build:**
   ```bash
   mkdir -p ~/kthfsdv/src
   cp -r exercise1/* ~/kthfsdv/src/
   cd ~/kthfsdv
   colcon build --symlink-install
   source install/setup.bash

2. **Run Node A (Publisher):**
ros2 run package1 nodeA

3. **Run Node B (Subscriber/Divider):**

# Exercise 2 - Real-time Data Visualisation Tool

A standalone GUI application built with PyQt5 and PyQtGraph to compute and visualize mathematical function trajectories in real-time.

---

## Function Definition

The application continuously evaluates and renders the continuous time function:

$$h(t) = 3\pi \cdot \exp(-5\sin(2\pi t))$$

---

## Features

- **Real-Time Plotting**: Dynamic rendering of $h(t)$ time-series data with configurable refresh intervals.
- **Interactive Controls**: Pause, resume, dynamic grid toggle, and full pan/zoom capabilities.
- **Data Export**: Support for exporting generated trajectory points $(t, h(t))$ into CSV format.

---

## Dependencies

Ensure the following packages are installed in your Python environment:

```bash
pip install PyQt5 pyqtgraph numpy
ros2 run package2 nodeB

4. **Data Visualization:**
ros2 run plotjuggler plotjuggler


