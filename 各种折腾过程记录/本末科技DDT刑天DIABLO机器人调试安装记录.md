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
机器人的执行频率不能过高，过高会导致机器人不能移动。
### todo
1. 机器人的状态切换
2. 机器人的延迟控制

本末科技轮足驱动代码
```cpp
#include "main.hpp"

namespace info_update_and_ctrl
{
    int InfoUpdateAndCtrl::SubscribeAndPublish()
    {
        DIABLO::OSDK::HAL_Pi Hal;
        if (Hal.init())
            return -1;

        vehicle = new DIABLO::OSDK::Vehicle(&Hal); // Initialize Onboard SDK
        if (vehicle->init())
            return -1;

        vehicle->telemetry->activate();

        vehicle->telemetry->configTopic(DIABLO::OSDK::TOPIC_POWER, OSDK_PUSH_DATA_10Hz);
        vehicle->telemetry->configTopic(DIABLO::OSDK::TOPIC_QUATERNION, OSDK_PUSH_DATA_50Hz);
        vehicle->telemetry->configTopic(DIABLO::OSDK::TOPIC_ACCL, OSDK_PUSH_DATA_50Hz);
        vehicle->telemetry->configTopic(DIABLO::OSDK::TOPIC_GYRO, OSDK_PUSH_DATA_50Hz);
        vehicle->telemetry->configTopic(DIABLO::OSDK::TOPIC_MOTOR, OSDK_PUSH_DATA_10Hz);

        vehicle->telemetry->configUpdate();

        movement_ctrl_ = vehicle->movement_ctrl;

        // Topic you want to publish
        ACCLPublisher = n_.advertise<diablo_sdk::OSDK_ACCL>("diablo_ros_ACCL_b", 10);
        GYROPublisher = n_.advertise<diablo_sdk::OSDK_GYRO>("diablo_ros_GYRO_b", 10);
        LEGMOTORSPublisher = n_.advertise<diablo_sdk::OSDK_LEGMOTORS>("diablo_ros_LEGMOTORS_b", 10);
        POWERPublisher = n_.advertise<diablo_sdk::OSDK_POWER>("diablo_ros_POWER_b", 10);
        QUATERNIONPublisher = n_.advertise<diablo_sdk::OSDK_QUATERNION>("diablo_ros_QUATERNION_b", 10);
        STATUSPublisher = n_.advertise<diablo_sdk::OSDK_STATUS>("diablo_ros_STATUS_b", 10);

        // Topic you want to subscribe
        cmd_vel_sub_ = n_.subscribe("/cmd_vel", 10, &InfoUpdateAndCtrl::cmdVelCallBack, this);
        // sport_mode_sub_ = n_.subscribe("/sport_mode", 1, &InfoUpdateAndCtrl::sportModeCallBack, this);
        ros::spin();

    return 0;
    }

    void InfoUpdateAndCtrl::cmdVelCallBack(const geometry_msgs::Twist::ConstPtr& msg){
        //订阅速度话题，发送机器人速度。
        //sport_mode 向量说明：sport_mode总共5位
        if (!movement_ctrl_->in_control())
        {
            printf("Try to get the control of robot movement!.\n");
            uint8_t result = movement_ctrl_->obtain_control();
            return;
        }
        movement_ctrl_->ctrl_data.forward = 0.0f;
        movement_ctrl_->ctrl_data.left = 0.0f;
        movement_ctrl_->ctrl_data.forward = msg->linear.x;
        movement_ctrl_->ctrl_data.left = msg->angular.z;
        // ROS_WARN("now x is %f", msg->linear.x);
        uint8_t result = movement_ctrl_->SendMovementCtrlCmd();
        InfoUpdateAndCtrl::publishDataProcess(vehicle);
    }

    void InfoUpdateAndCtrl::sportModeCallBack(const std_msgs::Int32MultiArray::ConstPtr &msg){
        //订阅运动模式话题，根据不同运动话题控制机器人姿态[站立/爬行 跳跃 z轴高度 roll角  pitch角]
        ROS_WARN("get new data");
        if (!movement_ctrl_->in_control())
        {
            printf("Try to get the control of robot movement!.\n");
            uint8_t result = movement_ctrl_->obtain_control();
            return;
        }
        static std_msgs::Int32MultiArray last_msg;
        last_msg.data.resize(5);
        //检查接受到的向量长度
        if(msg->data.size() != 5){
            ROS_WARN("SPORT MODE MASSAGE IS INVAILED!");
            return;
        }
        


        switch(msg->data[0]){
            case 1:
                if(last_msg.data[0] != 1){
                    ROS_WARN("robot UP");
                    // movement_ctrl_->ctrl_mode_cmd = true;
                    movement_ctrl_->SendTransformUpCmd();
                    movement_ctrl_->ctrl_data.up = 1.0f;
                }
                else
                    movement_ctrl_->ctrl_data.up = 1.0f;
                break;
            case 0:
                ROS_WARN("robot DOWN");
                movement_ctrl_->ctrl_mode_cmd = true;
                movement_ctrl_->SendTransformDownCmd();
                break;
        }


        if(msg->data[1] == 1){ //机器人跳跃切换
            ROS_WARN("JUMP!!!!");
            movement_ctrl_->ctrl_mode_cmd = true;
            movement_ctrl_->SendJumpCmd(true);
            sleep(1); // wait for jump charge!
        }

        // switch(msg->data[1]){
        //     case 0:
        //         movement_ctrl_->ctrl_mode_cmd = false;
        //         movement_ctrl_->SendJumpCmd(false);
        //     case 1:
        //         ROS_WARN("JUMP!!!!");
        //         movement_ctrl_->ctrl_mode_cmd = true;
        //         movement_ctrl_->SendJumpCmd(true);
        //         sleep(1); // wait for jump charge!
        // }

        switch(msg->data[2]){
            case 0:
                movement_ctrl_->ctrl_data.up = -0.5f;
                break;
            case 1:
                movement_ctrl_->ctrl_data.up = 1.0f;
                break;
            case 2:
                movement_ctrl_->ctrl_data.up = 0.5f;
                break;
        }


        switch(msg->data[3]){
            case 0:
                movement_ctrl_->ctrl_data.roll = -0.1f; // pos ctrl
                break;
            case 1:
                movement_ctrl_->ctrl_data.roll = 0.0f; // pos ctrl
                break;
            case 2:
                movement_ctrl_->ctrl_data.roll = 0.1f; // pos ctrl
                break;
        }


        switch(msg->data[4]){
            case 0:
                movement_ctrl_->ctrl_data.pitch = 0.5f;
                break;
            case 1:
                movement_ctrl_->ctrl_data.pitch = 0.0f;
                break;
            case 2:
                movement_ctrl_->ctrl_data.pitch = -0.5f;
                break;
        }

        if (movement_ctrl_->ctrl_mode_cmd)
        {
            uint8_t result = movement_ctrl_->SendMovementModeCtrlCmd();
        }
        else
        {
            uint8_t result = movement_ctrl_->SendMovementCtrlCmd();
        }
        last_msg = *msg;
        InfoUpdateAndCtrl::publishDataProcess(vehicle);
    }

    void InfoUpdateAndCtrl::publishDataProcess(DIABLO::OSDK::Vehicle *vehicle_)
    {
        ros::Rate loop_rate(100);
        while (ros::ok())
        {
            if (vehicle_->telemetry->newcome & 0x40)
            {
                diablo_sdk::OSDK_STATUS msg;
                msg.ctrl_mode = vehicle_->telemetry->status.ctrl_mode;
                msg.robot_mode = vehicle_->telemetry->status.robot_mode;
                msg.error = vehicle_->telemetry->status.error;
                msg.warning = vehicle_->telemetry->status.warning;
                STATUSPublisher.publish(msg);
                vehicle_->telemetry->eraseNewcomeFlag(0xBF);
            }
            if (vehicle_->telemetry->newcome & 0x20)
            {
                diablo_sdk::OSDK_QUATERNION msg;
                msg.w = vehicle_->telemetry->quaternion.w;
                msg.x = vehicle_->telemetry->quaternion.x;
                msg.y = vehicle_->telemetry->quaternion.y;
                msg.z = vehicle_->telemetry->quaternion.z;
                QUATERNIONPublisher.publish(msg);
                // printf("Quaternion_w:\t%f\nQuaternion_x:\t%f\nQuaternion_y:\t%f\nQuaternion_z:\t%f\n", msg.w, msg.x, msg.y, msg.z);
                vehicle_->telemetry->eraseNewcomeFlag(0xDF);
            }
            if (vehicle_->telemetry->newcome & 0x10)
            {
                diablo_sdk::OSDK_ACCL msg;
                msg.x = vehicle_->telemetry->accl.x;
                msg.y = vehicle_->telemetry->accl.y;
                msg.z = vehicle_->telemetry->accl.z;
                ACCLPublisher.publish(msg);
                // printf("ACCL_X:\t%f\nACCL_Y:\t%f\nACCL_Z:\t%f\n", msg.x, msg.y, msg.z);
                vehicle_->telemetry->eraseNewcomeFlag(0xEF);
            }
            if (vehicle_->telemetry->newcome & 0x08)
            {
                diablo_sdk::OSDK_GYRO msg;
                msg.x = vehicle_->telemetry->gyro.x;
                msg.y = vehicle_->telemetry->gyro.y;
                msg.z = vehicle_->telemetry->gyro.z;
                GYROPublisher.publish(msg);
                // printf("GYRO_X:\t%f\nGYRO_Y:\t%f\nGYRO_Z:\t%f\n", msg.x, msg.y, msg.z);
                vehicle_->telemetry->eraseNewcomeFlag(0xF7);
            }
            if (vehicle_->telemetry->newcome & 0x02)
            {
                diablo_sdk::OSDK_POWER msg;
                msg.battery_voltage = vehicle_->telemetry->power.voltage;
                msg.battery_current = vehicle_->telemetry->power.current;
                msg.battery_capacitor_energy = vehicle_->telemetry->power.capacitor_energy;
                msg.battery_power_percent = vehicle_->telemetry->power.power_percent;
                POWERPublisher.publish(msg);
                // printf("Power:\nVoltage:\t%f\nCurrent:\t%f\nCap_EN:\t%f\nPercent:\t%u\n", msg.battery_voltage, msg.battery_current, msg.battery_current, msg.battery_power_percent);
                vehicle_->telemetry->eraseNewcomeFlag(0xFD);
            }
            if (vehicle_->telemetry->newcome & 0x01)
            {
                diablo_sdk::OSDK_LEGMOTORS msg;
                msg.left_hip_enc_rev = vehicle_->telemetry->motors.left_hip.rev;
                msg.left_hip_pos = vehicle_->telemetry->motors.left_hip.pos;
                msg.left_hip_vel = vehicle_->telemetry->motors.left_hip.vel;
                msg.left_hip_iq = vehicle_->telemetry->motors.left_hip.iq;

                msg.left_knee_enc_rev = vehicle_->telemetry->motors.left_knee.rev;
                msg.left_knee_pos = vehicle_->telemetry->motors.left_knee.pos;
                msg.left_knee_vel = vehicle_->telemetry->motors.left_knee.vel;
                msg.left_knee_iq = vehicle_->telemetry->motors.left_knee.iq;

                msg.left_wheel_enc_rev = vehicle_->telemetry->motors.left_wheel.rev;
                msg.left_wheel_pos = vehicle_->telemetry->motors.left_wheel.pos;
                msg.left_wheel_vel = vehicle_->telemetry->motors.left_wheel.vel;
                msg.left_wheel_iq = vehicle_->telemetry->motors.left_wheel.iq;

                msg.right_hip_enc_rev = vehicle_->telemetry->motors.right_hip.rev;
                msg.right_hip_pos = vehicle_->telemetry->motors.right_hip.pos;
                msg.right_hip_vel = vehicle_->telemetry->motors.right_hip.vel;
                msg.right_hip_iq = vehicle_->telemetry->motors.right_hip.iq;

                msg.right_knee_enc_rev = vehicle_->telemetry->motors.right_knee.rev;
                msg.right_knee_pos = vehicle_->telemetry->motors.right_knee.pos;
                msg.right_knee_vel = vehicle_->telemetry->motors.right_knee.vel;
                msg.right_knee_iq = vehicle_->telemetry->motors.right_knee.iq;

                msg.right_wheel_enc_rev = vehicle_->telemetry->motors.right_wheel.rev;
                msg.right_wheel_pos = vehicle_->telemetry->motors.right_wheel.pos;
                msg.right_wheel_vel = vehicle_->telemetry->motors.right_wheel.vel;
                msg.right_wheel_iq = vehicle_->telemetry->motors.right_wheel.iq;

                LEGMOTORSPublisher.publish(msg);
                vehicle_->telemetry->eraseNewcomeFlag(0xFE);
            }
            ros::spinOnce();
            loop_rate.sleep();
        }
    }
} // namespace info_update_and_ctrl

int main(int argc, char **argv)
{
    // Initiate ROS
    ros::init(argc, argv, "status_update_and_ctrl_example");

    info_update_and_ctrl::InfoUpdateAndCtrl test;
    test.SubscribeAndPublish();

    return 0;
}




```