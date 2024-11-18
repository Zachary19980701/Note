import numpy as np
import matplotlib.pyplot as plt

# 参数定义
k_attr = 1.0  # 吸引力系数
k_rep = 100.0  # 斥力系数
rho_0 = 5.0  # 斥力影响范围

# 预瞄点（目标点）和障碍物的定义
goal = np.array([20, 0])
obstacles = [np.array([10, 2]), np.array([15, -3])]  # 障碍物列表
boundary = [(-5, 5)]  # 边界约束

# 机器人的起始位置
robot_position = np.array([0.0, 0.0])

# 函数定义
def attractive_potential(x, goal): # 引力势场
    return 0.5 * k_attr * np.linalg.norm(x - goal)**2

def repulsive_potential(x, obs): # 斥力势场
    d = np.linalg.norm(x - obs)
    if d < rho_0:
        return 0.5 * k_rep * (1/d - 1/rho_0)**2
    else:
        return 0

def total_potential(x, goal, obstacles):
    U_attr = attractive_potential(x, goal)
    U_rep = sum(repulsive_potential(x, obs) for obs in obstacles)
    return U_attr + U_rep

def compute_force(x, goal, obstacles):
    F_attr = -k_attr * (x - goal)
    F_rep = np.zeros_like(x)
    
    for obs in obstacles:
        d = np.linalg.norm(x - obs)
        if d < rho_0:
            F_rep += k_rep * (1/d - 1/rho_0) * (1/d**2) * (x - obs) / d

    return F_attr + F_rep

def apply_boundary_constraints(x, boundary):
    if not (boundary[0][0] <= x[1] <= boundary[0][1]):
        x[1] = np.clip(x[1], boundary[0][0], boundary[0][1])
    return x

# 仿真参数
dt = 0.1  # 时间步长
max_iter = 1000

# 仿真流程
trajectory = [robot_position.copy()]
for _ in range(max_iter):
    force = compute_force(robot_position, goal, obstacles)
    robot_position += force * dt
    robot_position = apply_boundary_constraints(robot_position, boundary)
    trajectory.append(robot_position.copy())

    if np.linalg.norm(robot_position - goal) < 0.1:
        break

# 绘制轨迹
trajectory = np.array(trajectory)
plt.figure()
plt.plot(trajectory[:, 0], trajectory[:, 1], label='Robot Path')
plt.scatter(*goal, color='red', label='Goal')
for obs in obstacles:
    plt.scatter(*obs, color='blue', label='Obstacle')
plt.axhspan(boundary[0][0], boundary[0][1], color='gray', alpha=0.5, label='Boundary')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Robot Path Planning with Artificial Potential Field')
plt.legend()
plt.grid()
plt.show()
