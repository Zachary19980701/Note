# 不同dds实现方式对于ros2的最终效果的影响
在点云等数据传输中，ros2的底层通讯协议[dds](https://design.ros2.org/articles/ros_on_dds.html)对于大量数据的吞吐具有明显的影响。ros2默认使用的dds实现方式是fastdds，但是在实际测试中发现fastdds会造成定位数据不更新，因此需要将dds的实现方式更改为cyclonedds。

在autoware的测试结果中，对于大数据量吞吐场景，也建议使用cyclondds作为优选中间件。https://autowarefoundation.github.io/autoware-documentation/main/installation/additional-settings-for-developers/network-configuration/dds-settings/

在领英一个博主的测试中，也推荐汽车的智驾系统使用cyclone作为默认中间件的实现方式 https://www.linkedin.com/pulse/importance-choosing-right-dds-ros2-realtime-vehicle-rajaram-moorthy/

