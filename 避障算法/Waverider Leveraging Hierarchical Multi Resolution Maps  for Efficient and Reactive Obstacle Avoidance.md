# Waverider: Leveraging Hierarchical, Multi-Resolution Maps  for Efficient and Reactive Obstacle Avoidance
反应式的精准避障方法

# introduce
Existing approaches range from simple reactive methods using 1D distance sensors to optimization-based systems requiring complete 3D maps and vary in complexity, reaction time, and obstacle resolution

现有方法的范围从使用 1D 距离传感器的简单反应方法到需要完整 3D 地图的基于优化的系统，并且在复杂性、反应时间和障碍物分辨率方面各不相同。

目前3D空间中的导航策略可以使用体素地图来表示(Volumetric Map), 目前固定分辨率的体素地图占用的空间非常大，可以使用可变分辨率的体素地图来降低空间占用，目前可变分辨率的体素地图有：
- octomap
- UFOmap
- supereight
- wavemap

本文使用Riemannian Motion Policys (RMPs)来在多分辨率的体素地图上进行导航规划，使用RMPs是在加速度阶上进行规划的，因此是一个天然平滑的规划方法。

**基于RMPs和分层的体素地图**是实现了一个**反应式**的避障方法。

# 分层地图 Hierarchical map
本文使用[wavemap](https://github.com/ethz-asl/wavemap)作为分层体素地图的实现方法。