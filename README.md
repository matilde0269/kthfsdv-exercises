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

1. **Clone the repository content into your workspace source directory:**
   ```bash
   mkdir -p ~/kthfsdv/src
   cp -r exercise1/* ~/kthfsdv/src/
   cd ~/kthfsdv
