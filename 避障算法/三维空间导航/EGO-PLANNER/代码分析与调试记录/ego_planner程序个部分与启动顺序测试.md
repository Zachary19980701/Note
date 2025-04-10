EGO-Planner 是一个基于梯度优化的无人机局部规划器，由浙江大学 FAST 实验室开发，其代码托管在 GitHub 上（ZJU-FAST-Lab/ego-planner）。以下是对其代码结构和执行顺序的分析，基于公开的源码和文档信息。我将从整体框架入手，逐步分解主要模块，并梳理其执行流程。

---

### **代码结构概述**
EGO-Planner 的代码主要基于 ROS (Robot Operating System) 框架，使用 C++ 编写，采用 catkin 构建系统。项目结构分为多个功能模块，主要集中在 `src` 目录下。以下是核心部分的结构：

1. **主要目录和包**
   - **`src/planner/plan_manage`**  
     负责规划的高层管理和状态机控制，是整个系统的核心调度模块。
   - **`src/planner/bspline_opt`**  
     实现 B 样条曲线优化，用于生成平滑且动态可行的轨迹。
   - **`src/planner/plan_env`**  
     处理环境感知和地图构建（如网格地图）。
   - **`src/uav_simulator`**  
     提供仿真环境支持，包括无人机动力学模拟和传感器数据生成。
   - **`src/traj_utils`**  
     提供轨迹相关的工具函数，如可视化和数据处理。
   - **`src/local_sensing`**  
     模拟传感器（如深度相机或点云生成），支持 CPU 和 GPU 两种模式。

2. **配置文件**
   - 位于 `launch` 文件夹中（如 `simple_run.launch`、`run_in_sim.launch`），用于启动 ROS 节点并设置参数。

3. **依赖**
   - 依赖外部库如 Eigen（线性代数）、Armadillo（矩阵计算）、PCL（点云处理）以及 ROS 相关库。

---

### **主要模块详解**
以下是几个核心模块的功能和代码文件：

1. **`plan_manage` - 规划管理**
   - **主要文件**：
     - `ego_replan_fsm.h/cpp`：实现有限状态机 (FSM)，管理规划的不同状态（如初始化、等待目标、生成新轨迹、重新规划等）。
     - `planner_manager.h/cpp`：协调前端路径搜索和后端轨迹优化。
   - **功能**：
     - 通过状态机控制规划流程。
     - 处理外部输入（如目标点、里程计数据）并调用底层优化器。

2. **`bspline_opt` - B 样条优化**
   - **主要文件**：
     - `bspline_optimizer.h/cpp`：基于梯度的 B 样条轨迹优化。
   - **功能**：
     - 使用 L-BFGS 算法优化轨迹，考虑平滑性、碰撞避免和动态可行性。
     - 不依赖 ESDF（欧几里得签名距离场），通过碰撞轨迹与引导路径比较来计算梯度。

3. **`plan_env` - 环境建模**
   - **主要文件**：
     - `grid_map.h/cpp`：构建二维或三维网格地图，用于障碍物检测。
   - **功能**：
     - 从传感器数据（如点云或深度图）生成环境表示，供规划器使用。

4. **`local_sensing` - 传感器模拟**
   - **主要文件**：
     - `pcl_render_node_cuda.cpp`（GPU 版本）和 `pcl_render_node_cpu.cpp`（CPU 版本）：生成模拟的深度图或点云。
   - **功能**：
     - 根据 `ENABLE_CUDA` 参数选择使用 GPU 或 CPU 处理传感器数据。

5. **`uav_simulator` - 仿真支持**
   - **主要文件**：
     - `SO3Control.cpp`：实现无人机姿态控制。
     - `odom_visualization.cpp`：发布里程计数据用于可视化。
   - **功能**：
     - 提供虚拟无人机的动力学模型和状态反馈。

---

### **执行顺序分析**
EGO-Planner 的执行顺序由 ROS 节点和回调函数驱动，整体流程可以分为启动阶段和运行阶段。以下是基于 `simple_run.launch` 或 `run_in_sim.launch` 的典型执行流程：

#### **1. 启动阶段**
- **步骤**：
  1. **ROS 节点初始化**：
     - 执行 `catkin_make` 编译代码后，通过 `roslaunch ego_planner simple_run.launch` 启动。
     - 加载 `launch` 文件中的参数（如规划范围、无人机 ID 等）。
  2. **节点注册**：
     - `ego_replan_fsm.cpp` 中的 `EGOReplanFSM::init` 初始化状态机，订阅话题（如 `/odom` 里程计、`/waypoint` 目标点）。
     - 启动定时器（`exec_timer_` 和 `safety_timer_`），分别用于执行规划和碰撞检测。
  3. **仿真环境准备**：
     - `uav_simulator` 启动，发布初始里程计数据和传感器数据（如点云）。
     - `local_sensing` 根据配置生成深度图或点云，发布到 `/grid_map/cloud` 等话题。

#### **2. 运行阶段**
- **状态机循环**（`execFSMCallback`）：
  1. **INIT（初始化）**：
     - 检查是否收到里程计 (`have_odom_`) 和目标点 (`have_target_`)。
     - 若条件满足，切换到 `WAIT_TARGET`。
  2. **WAIT_TARGET（等待目标）**：
     - 通过 `waypointCallback` 接收用户输入的目标点。
     - 目标点就位后，切换到 `GEN_NEW_TRAJ`。
  3. **GEN_NEW_TRAJ（生成新轨迹）**：
     - 调用 `planFromCurrentTraj` 或 `callReboundReplan`，生成初始轨迹。
     - 前端使用 A* 搜索引导路径，后端通过 `bspline_optimizer` 优化 B 样条轨迹。
     - 发布轨迹到 `/bspline` 话题，进入 `EXEC_TRAJ`。
  4. **EXEC_TRAJ（执行轨迹）**：
     - 将轨迹发送给控制器（如 `uav_simulator` 中的 `SO3Control`）。
     - 定时检查碰撞（`checkCollisionCallback`），若检测到障碍，切换到 `REPLAN_TRAJ`。
  5. **REPLAN_TRAJ（重新规划）**：
     - 根据当前状态和环境更新，重新调用优化器生成新轨迹。
     - 返回 `EXEC_TRAJ` 或在紧急情况进入 `EMERGENCY_STOP`。
  6. **EMERGENCY_STOP（紧急停止）**：
     - 调用 `callEmergencyStop`，停止无人机并等待用户干预。

- **数据流**：
  - **输入**：里程计（`/odom`）、传感器数据（`/grid_map/cloud`）、目标点（`/waypoint`）。
  - **处理**：状态机调度 → 路径搜索 → 轨迹优化。
  - **输出**：优化后的 B 样条轨迹（`/bspline`）、可视化数据（通过 `rviz.launch` 显示）。

---

### **关键执行细节**
1. **回调机制**：
   - `odometryCallback` 更新无人机状态（位置、速度、加速度）。
   - `waypointCallback` 处理目标点输入。
   - `execFSMCallback` 和 `checkCollisionCallback` 以固定频率（如 100Hz）运行，驱动状态切换。

2. **优化流程**：
   - `bspline_optimizer` 的 `optimize` 函数是核心，输入控制点和环境数据，输出平滑轨迹。
   - 不使用 ESDF，而是通过碰撞检测和引导路径动态计算梯度。

3. **并行性**：
   - 传感器数据生成（`local_sensing`）和规划（`plan_manage`）并行运行，通过 ROS 话题通信。

---

### **总结**
EGO-Planner 的代码结构清晰分层，`plan_manage` 作为大脑协调各模块，`bspline_opt` 提供高效优化，`plan_env` 和 `local_sensing` 支撑环境感知，`uav_simulator` 实现仿真。执行顺序由状态机驱动，从初始化到轨迹执行和重新规划形成闭环，高度依赖 ROS 的发布-订阅机制。如果需要更深入分析某个模块（如 `bspline_optimizer` 的具体算法），可以进一步展开。

希望这个解答对你理解 EGO-Planner 的代码结构和执行顺序有所帮助！如果有具体问题，欢迎继续提问。