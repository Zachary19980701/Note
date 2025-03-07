# RAPTOR: Robust and Perception-aware Trajectory  Replanning for Quadrotor Fast Flight
轨迹重规划能够让四旋翼在未知环境中自主导航，但是在高速环境下轨迹重新规划是一个问题。在时间非常有限的情况下，现有方法对解的可行性或质量没有强有力的保证。此外，大多数方法没有考虑环境感知，而环境感知是快速飞行的关键瓶颈。在本文中，我们提出了RAPTOR，一个鲁棒的和感知感知的重规划框架来支持快速和安全的飞行，系统地解决了这些问题。

**设计了一种融合多条拓扑路径的路径引导优化( PGO )方法，以确保在非常有限的时间内找到可行且高质量的轨迹。**

**我们还引入了感知感知规划策略来主动观察和避开未知障碍物**。

Nonetheless, high-speed flight in unknown and highly cluttered environments still remains one of the biggest challenges toward full autonomy.
高速飞行和高度动态的环境仍然是是一个挑战。

**在高速环境中的运动存在以下几个问题：**
- 有限时间快速进行重规划
- 快速重规划过程中，在限制的拓扑类中不一定存在最优的解
- 现有方法对环境感知不敏感，当飞行速度和障碍物密度较高时，会造成致命的后果。
- 主动观察并避免可能出现的危险，而不是被动地躲避观察到的东西，对于安全的高速飞行是至关重要的

In this paper, we propose a Robust And Perception-aware TrajectOry Replanning framework called RAPTOR to address these issues systematically

为了弥补这一差距，我们将其扩展为感知感知规划策略，从两个方面实现更快、更安全的飞行
perception-aware planning strategy

本文的主要的内容：
- A topological paths-guided gradient-based replanning approach, that is capable of generating high-quality trajectories in limited time. 一个基于梯度的拓扑轨迹引导规划，能够在短时间内快速的生成高质量的路径
- A risk-aware trajectory refinement approach, which enforces visibility and safe reaction distance to unknown obstacles. It improves the predictability and safety of fast flights.一个风险感知的轨迹规划方法，能够在未知区域增强对可见性和安全距离，提高快速安全的飞行
- A two-step yaw angle planning method, to actively explore the unknown environments and gather useful information for the flight. 两步的yaw角规划，为飞行提供足够的FOV信息

## SYSTEM OVERVIEW
![](images/2025-03-05-09-53-02.png)
It takes the outputs of the global planning, dense mapping and state estimation modules, and deforms the global reference trajectory locally to avoid previously unknown obstacles.
获得全局规划的输出，稠密映射和状态估计模块的信息，并且对全局参考系进行变形以避开未知障碍物。

**整个重规划分为两步进行工作**
- Firstly, the robust optimistic replanning generates multiple locally optimal trajectories in parallel through the path-guided optimization (Sect.IV).通过路径引导优化的鲁棒重规划，在可通行区域生成局部的优化路径。The optimization is guided by topologically distinctive paths extracted and carefully selected from the topological path searching, which will be detailed in Sect.优化路线是通过挑选的拓扑路线进行搜索引导的。
- Secondly, the perception-aware planning strategy is utilized.The best trajectory among the locally optimal ones is further polished by a risk-aware trajectory refinement, in which its safety and visibility to the unknown and dangerous space is improved, as presented in Sect.VI.第二步对感知模块进行优化，通过感知信息获得更优的yaw角约束。


## PATH-GUIDED TRAJECTORY OPTIMIZATION 路径引导的轨迹优化
在section 2-A中，GTO方法在局部路径规划中速度非常快，但是存在路径的极小点问题。
针对上述问题，本文提出了PGO算法，使用几何路径规划来提高生成路径的成功率。
### 优化失效分析
GTO会由于初始规划的不合适导致规划的失败，传统在解决这个问题时会添加欧氏距离作为约束，但是添加距离约束之后还是会有局部最优的现象。
### problem formulation 问题界定
使用B样条曲线作为基础的规划曲线，是一个低消耗的曲线规划。
For a trajectory segment in collision, we reparameterize it as a pb degree uniform B-spline with control points {q0, q1, . . . , qN } and knot span ∆t.
对于一段轨迹，将这段轨迹的B样条设置为一个包含（q_0, q_1, ..., q_N）的控制点和knot span ∆t

**PGO包含两种不同的相**
1. **生成一段 intermediate warmip trajectory**
也就是用环境的信息来变形轨迹而不是单独的使用ESDF,本文使用几何路径引导，将初始的轨迹引导到自由空间上。
本文中的工作中，无碰撞的轨迹是哟欧基于采样的拓扑路径搜索实现的。
第一阶段的目标函数为：
![](images/2025-03-07-21-39-28.png)
f_S是平滑项，f_g是平滑代价。平滑代价的计算方式是引导路径点到样条曲线之间的距离。
简化fs的形式，通过B样条的方法来简化fs的计算形式。
每个控制点qi在引导路径上分配一个关联点gi，gi沿引导路径均匀采样。然后将fg定义为这些点对之间的平方欧氏距离之和。
It outputs a smooth trajectory in the vicinity of the guiding path.会生成一条基本上大部分无碰撞的初始轨迹，论文中叫热身轨迹。使用这种方法能够将大部分的轨迹放置到无障碍的空间中，在使用标准的GTO算法来优化提升轨迹。Hence, standard GTO methods can be utilized to improve the trajectory.
2. **轨迹的进一步平滑**
将预热轨迹进一步细化为平滑、安全、动态可行的轨迹
![](images/2025-03-07-22-34-11.png)
