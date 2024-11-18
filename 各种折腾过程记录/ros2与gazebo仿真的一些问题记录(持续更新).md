# gazebo不发布/gazebo/model_states
由于很多时候我只是想要获取机器人的绝对位置，不想要在额外的启动一套定位程序，可以直接使用/gazebo/model_states来获取机器人的状态。在ros1的版本中，这个状态会随着gazebo的启动而发布，但是ros2需要自己在world文件中添加这个插件来启动这个话题。
```xml
<?xml version="1.0" ?>


<sdf version="1.4">
  <world name="default">

  <!-- 添加下面内容 -->
    <plugin name="gazebo_ros_state" filename="libgazebo_ros_state.so">
      <ros>
        <namespace>/gazebo</namespace>
      </ros>
  <!-- 添加内容结束 -->

      <update_rate>1.0</update_rate>
    </plugin>
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>

  </world>
</sdf>
```
## 参考连接
[1] [/gazebo/get_model_state in ROS2 not present](https://robotics.stackexchange.com/questions/29310/gazebo-get-model-state-in-ros2-not-present)
[2] [ROS2 Dashing service `get_entity_state` is missing](https://answers.ros.org/question/360161/ros2-dashing-service-get_entity_state-is-missing/)
[3] [gazebo_ros_pkgs](https://github.com/ros-simulation/gazebo_ros_pkgs/blob/c071749932a541a5b8aced23c3414724a8cd1949/gazebo_ros/worlds/gazebo_ros_state_demo.world#L41-L49)