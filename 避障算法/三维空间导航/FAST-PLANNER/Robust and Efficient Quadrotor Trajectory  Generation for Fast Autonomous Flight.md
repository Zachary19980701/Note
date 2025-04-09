# Robust and Efficient Quadrotor Trajectory  Generation for Fast Autonomous Flight
我们采用一种动力学路径搜索方法，以在离散的控制空间中找到安全，动力学可行性和最小时间初始轨迹。我们通过B-Spline优化提高了轨迹的平滑度和清除率，该优化结合了来自欧几里得距离场（EDF）的梯度信息，并有效地利用了B-Spline的凸形属性的动态约束。最后，通过将最终轨迹表示为不均匀的B型频道，采用了一种迭代时间调整方法来保证动态可行和非保守的轨迹。我们在各种复杂的模拟环境中验证我们提出的方法。该方法的能力在挑战现实世界任务中也得到了验证。我们将代码作为开源软件包

轨迹产生的效率和鲁棒性至关重要。在许多情况下，例如在未知环境中高速飞行的四型飞机，应在很短的时间内不断再生轨迹，以避免出现紧急威胁。

其次，为了确保生成动作的动力学可行性，对速度和加速度的限制通常会保守地执行。结果，通常很难调谐生成的轨迹的侵略性，以满足优选高速飞行速度的应用。

采用了基于启发式搜索和线性二次最低时间控制的运动动力路径搜索。

将初始路径精制成精心设计的B-Spline优化，该路径利用B-Spline的凸赫尔属性包含梯度信息和动态约束。它改善了初始路径，并迅速收敛到光滑，安全且动态可行的轨迹。最后，该轨迹表示为不均匀的B型频道，为此，我们研究了衍生物的控制点与时间分配之间的关系。

首先初始一条不在乎碰撞的轨迹，然后在碰撞点中添加控制点，将控制点连接成一条无碰撞的轨迹。

本文的创新点在于：
We propose a robust and efficient systematic method, incorporating kinodynamic path searching, B-spline optimization and time adjustment, where safety, dynamic feasibility and aggressiveness are built from bottom-up.
提出了一种结合动力学搜索与B样条优化的方法

We present an optimization formulation based on the convex hull property of B-splines that delicately incorporates gradient information and dynamic constraints, which converges quickly to generate smooth, safe and dynamically feasible trajectories.
提出了一种B样条的优化公式，包含多种信息素

## 动力学搜索
动力学搜索是基于混合A\*首先提出的自动驾驶汽车搜索，hybird-A\*
It searches for a safe and kinodynamic feasible trajectory that is minimal with respect to time duration and control cost in a voxel grid map.
It searches for a safe and kinodynamic feasible trajectory that is minimal with respect to time duration and control cost in a voxel grid map.
在体素地图中寻找动力学可行的轨迹，并且能够较快的进行搜索。

### Primitives Generation 原始轨迹的生成
