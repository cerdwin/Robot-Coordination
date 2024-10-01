# Autonomous Multi-Robot Exploration with CoppeliaSim

This project involves developing an exploration strategy for autonomous mobile robots using the CoppeliaSim simulator. The solution connects multiple robots that autonomously navigate through an environment while avoiding collisions and collecting metric maps. The project's success is measured by environment coverage in a given time.

## Project Overview

The main objective is to implement a Python-based strategy for multi-robot exploration, where each robot independently navigates and contributes to a shared occupancy grid map. The following features are part of the project:

- **Environment Mapping**: Robots will build occupancy grid maps as they navigate through unknown environments.
- **Frontier-based Exploration**: Robots will identify frontiers—regions between explored and unexplored areas—and select navigation goals accordingly.
- **Goal Planning**: Robots will select goals based on proximity or utility (mutual information gain) and plan paths using pre-defined algorithms.

### Features

1. **Frontier Detection**: Robots identify frontiers and select new goals to maximize exploration efficiency.
2. **Goal Planning**:
   - Closest Frontier Planning: Robots prioritize the closest frontier.
   - Utility-based Planning: Robots use mutual information to select goals for maximal exploration.
3. **Multi-Robot Coordination**:
   - Robots operate in a fully centralized system with simple task allocation.
   - Exploration tasks can be decentralized for more complex coordination.
4. **Occupancy Grid Mapping**:
   - Static-sized maps.
   - Dynamic-sized maps that grow based on the explored area.

### File Structure

```plaintext
Project/
│
├── Explorer.py                 # Main runnable script
├── hexapod_explorer/
│   ├── HexapodExplorer.py       # Implementation of map building, processing, and planning
│
├── hexapod_robot/
│   ├── HexapodController.py     # Robot locomotion control
│   ├── HexapodRobot.py          # Main interface for the simulated robot
│
├── cpg/                         # Locomotion controlling CPG
├── hexapod_sim/                 # Simulator interface
└── README.md                    # This file
