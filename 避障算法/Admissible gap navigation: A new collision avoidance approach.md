# Admissible gap navigation: A new collision avoidance approach
相比于搜索式算法，基于gap的反应式算法能够在未知的稠密复杂环境中高效导航。可接受的gap是由两部分组成的：1. 机器人能够避免碰撞 2. 符合机器人的运动约束。
本文相对于传统的基于gap的导航方法不同，考虑精确的形状形状和运动学，而不是直接对方向进行规划。反应式的基本原则是，一旦穿越过gap，就直接向目标移动。
## Introduction
基于规划的避障方法在狭窄或者复杂的环境中，会出现局部最小值、转向失败、原地振荡（打转）等问题。针对这种问题，提出了一种gap-based methods。但是目前的gap-based method只是将机器人考虑位一个圆形的外形，并且没有考虑机器人的运动学约束，可能会导致某些不符合机器人运动约束的运动规划。针对上述问题：
1. Local incremental planning for a carlike robot navigating among obstacles, 使用最小二乘法将gap的方向解与机器人航向角进行对齐。
2. Robot navigation in very complex, dense, and cluttered indoor/outdoor evironments, 将问题分解为运动学、动力学等子问题进行分析。
本文提出了一个admissible gap（AG）可接受的gap方法。这个方法直接考虑形状和动力学的约束。
基本的思想是搜索车辆周围的一组gap，使用迭代的方法构建虚拟的允许gap，并在这个gap中进行路径规划。
## Related Work
pass
## Preliminary definitions
- 机器人采用差速驱动，在平坦地面上进行导航，并且假定轮子纯滚动
- $p_g$ 机器人目标位置
- $p_r$ 机器人当前位置
- R 机器人的虚拟圆半径
- $P_e, e = 1,..., m, m = 机器人拟合的多边形边数$ 使用m条边拟合机器人
- 传感器使用激光雷达scan
- $S = {p^S_1,...,p^S_n}$ 激光雷达点的集合