# 不同dds实现方式对于ros2的最终效果的影响
在点云等数据传输中，ros2的底层通讯协议[dds](https://design.ros2.org/articles/ros_on_dds.html)对于大量数据的吞吐具有明显的影响。ros2默认使用的dds实现方式是fastdds，但是在实际测试中发现fastdds会造成定位数据不更新，因此需要将dds的实现方式更改为cyclonedds。

在autoware的测试结果中，对于大数据量吞吐场景，也建议使用cyclondds作为优选中间件。https://autowarefoundation.github.io/autoware-documentation/main/installation/additional-settings-for-developers/network-configuration/dds-settings/

在领英一个博主的测试中，也推荐汽车的智驾系统使用cyclone作为默认中间件的实现方式 https://www.linkedin.com/pulse/importance-choosing-right-dds-ros2-realtime-vehicle-rajaram-moorthy/


https://www.robotandchisel.com/2020/08/12/cyclonedds/



# 检查ROS2 DDS中间件并配置CycloneDDS

## 检查已安装的DDS中间件

首先，让我们检查系统中已安装的RMW (ROS Middleware) 实现：

```bash
ros2 pkg list | grep -i rmw
```

这将列出所有已安装的RMW包。通常，您可能会看到类似这样的输出：

```
rmw
rmw_connextdds
rmw_cyclonedds_cpp
rmw_fastrtps_cpp
rmw_fastrtps_dynamic_cpp
rmw_implementation
...
```

您也可以检查当前使用的RMW实现：

```bash
echo $RMW_IMPLEMENTATION
```

如果未设置此变量，ROS2将使用默认中间件（通常是FastRTPS/FastDDS）。

## 检查CycloneDDS是否已安装

确认CycloneDDS是否已安装：

```bash
ros2 pkg list | grep -i cyclone
```

如果尚未安装，可以通过以下命令安装：

```bash
sudo apt install ros-$ROS_DISTRO-rmw_cyclonedds_cpp
```

其中`$ROS_DISTRO`是您的ROS2发行版（如humble, foxy等）。

## 配置.bashrc使用CycloneDDS

在您的`.bashrc`文件中添加以下行，将CycloneDDS设置为默认RMW实现：

```bash
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
```

为了进一步优化CycloneDDS用于跨主机通信，您还可以添加以下配置：

```bash
echo 'export CYCLONEDDS_URI=file:///path/to/cyclonedds_config.xml' >> ~/.bashrc
```

然后，创建`cyclonedds_config.xml`文件并包含以下配置（请根据您的网络环境调整）：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain id="any">
    <General>
      <NetworkInterfaceAddress>auto</NetworkInterfaceAddress>
      <AllowMulticast>true</AllowMulticast>
      <MaxMessageSize>65500B</MaxMessageSize>
    </General>
    <Discovery>
      <ParticipantIndex>auto</ParticipantIndex>
      <Peers>
        <!-- 如有需要，可以在此明确定义对等点
        例如：<Peer address="192.168.1.10"/>
        -->
      </Peers>
    </Discovery>
  </Domain>
</CycloneDDS>
```

应用更改：

```bash
source ~/.bashrc
```

## 验证配置

验证DDS中间件设置是否生效：

```bash
echo $RMW_IMPLEMENTATION
```

应该显示：`rmw_cyclonedds_cpp`

## 测试跨主机通信

1. 在两台主机上设置相同的`ROS_DOMAIN_ID`：

```bash
echo 'export ROS_DOMAIN_ID=<一个0-232之间的数字>' >> ~/.bashrc
source ~/.bashrc
```

2. 确保两台主机能够互相访问，并确保防火墙不阻止DDS通信端口（通常是7400-7500范围内的UDP端口）。

3. 在一台主机上运行服务器：

```bash
ros2 run demo_nodes_cpp add_two_ints_server
```

4. 在另一台主机上尝试调用服务：

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

这个配置应该能够解决跨主机ROS2服务通信的问题，特别是当两台主机在同一网络中并且网络允许UDP多播通信时。
