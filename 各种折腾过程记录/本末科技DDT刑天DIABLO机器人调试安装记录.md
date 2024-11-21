# 官方引导网页
[本末科技sdk-docs](https://diablo-sdk-docs.readthedocs.io/en/latest/)

# 更改网络从静态网络到动态网络
由于切换镜像之后没有wifi配置了，需要将lan口的网络从静态改为动态网络，还是推荐使用设置中的部署方法，其他方法会造成网络初始化的失败。

# 安装与配置ROS1驱动包
 1. 安装ROS1驱动包
 2. 将ros1的驱动包的端口的ttyAMA0改为ttyS3

# 本末科技轮足驱动编写
将机器人的控制分为两个部分，一个是速度控制，使用/cmd_vel话题，一个是运动姿态控制，采用/sport_mode话题。下述是ros2的控制指令列表。
```
w：控制机器人向前移动。 （-1.0~+1.0米/秒）; （-1.6~+1.6米/秒Low-speed mode::High-speed mode::
s：控制机器人向后移动。 （-1.0~+1.0米/秒）; （-1.6~+1.6米/秒Low-speed mode::High-speed mode::
a：控制机器人左转。 （-5.0~+5.0 弧度/秒）Arbitrarily mode::
d：控制机器人右转。 （-5.0~+5.0 弧度/秒）Arbitrarily mode::

q：控制机器人向左倾斜。 （-0.2~+0.2弧度/秒）Standing mode::
e：控制机器人向右倾斜。 （-0.2~+0.2弧度/秒）Standing mode::
r：将机身倾斜角度调整为水平。Standing mode:

z：将机器人切换到站立模式。
x：将机器人切换到爬行模式。

v：用于提升机器人的控制模式。 （0 ~ 1）Position mode 0:
b：用于提升机器人的控制模式。 （-0.25 ~ +0.25 米/秒）Position mode 1:
n：用于机器人头部俯仰的控制模式。 （0 ~ 1）Position mode 0:
m：用于机器人头部俯仰的控制模式。 （-0.3~ +0.3 弧度/秒）Position mode 

h：站立模式下的最小高度。Position mode
k：站立模式下的中等高度。Position mode
j：站立模式下的最大高度。Position mode


u：控制机器人上仰。Position mode
i：将机身调整为水平。Position mode
o：控制机器人下仰。Position mode


f：太空步。dance mode
g：太空步结束。dance mode
c：跳跃模式。Jump mode
`：退出虚拟遥控器。
```
上述的指令列表可以分为两个部分即cmd_vel和sport_mode消息i
cmd_vel消息替代wasd四个键盘位置。
运动控制可以分为下面的几个模式：
1. roll角的变化 -1 0 1（仅在站立模式可用）
2. 站立爬行模式切换 0 1 包含状态切换
3. 站立模式高度调节 -1 0 1
4. 机器人的前仰后仰 -1 0 1
5. 跳跃模式 0 1 包含状态切换

状态位的顺序为：
1. 站立爬行模式切换 0 1
2. 跳跃模式切换 0 1
3. 站立模式高度调节 -1 0 1
4. roll角的变化 -1 0 1
5. 机器人的前仰后仰 -1 0 1

## 目前存在问题
机器人不能执行cmd vel命令，返回的执行result为0.
### todo
1. 机器人的状态切换
2. 机器人的延迟控制