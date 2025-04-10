# 代码功能说明
 **`plan_manage` - 规划管理**
   - **主要文件**：
     - `ego_replan_fsm.h/cpp`：实现有限状态机 (FSM)，管理规划的不同状态（如初始化、等待目标、生成新轨迹、重新规划等）。
     - `planner_manager.h/cpp`：协调前端路径搜索和后端轨迹优化。
   - **功能**：
     - 通过状态机控制规划流程。
     - 处理外部输入（如目标点、里程计数据）并调用底层优化器。


# planner_manager
实现了一个名为 EGOPlannerManager 的轨迹规划管理器，主要用于无人机或其他移动机器人在三维空间中的运动规划。
1. 参数的初始化
2. 全局的轨迹规划
3. 局部的轨迹重规划
4. 紧急停止
5. 轨迹优化和参数化
6. 轨迹可视化
7. 异常处理

# 全局轨迹规划
```cpp
  bool EGOPlannerManager::planGlobalTraj(const Eigen::Vector3d &start_pos, const Eigen::Vector3d &start_vel, const Eigen::Vector3d &start_acc,
                                         const Eigen::Vector3d &end_pos, const Eigen::Vector3d &end_vel, const Eigen::Vector3d &end_acc)
  {
    // 全局轨迹规划
    // generate global reference trajectory

    vector<Eigen::Vector3d> points; // 初始化一个point向量
    // 将开始点和结束点放入向量中
    points.push_back(start_pos);
    points.push_back(end_pos);

    // insert intermediate points if too far 插入中间点
    vector<Eigen::Vector3d> inter_points; //中间点向量
    const double dist_thresh = 4.0; // 设置中间点间隔

    for (size_t i = 0; i < points.size() - 1; ++i)
    {
      inter_points.push_back(points.at(i)); // at()对数组的边界进行检查，会有轻微的性能损耗
      double dist = (points.at(i + 1) - points.at(i)).norm(); // 计算两点之间的距离

      if (dist > dist_thresh) // 如果两点之间的距离大于阈值，则插入中间点
      {
        int id_num = floor(dist / dist_thresh) + 1; // 计算需要插入多少中间点

        for (int j = 1; j < id_num; ++j)
        {
          Eigen::Vector3d inter_pt =
              points.at(i) * (1.0 - double(j) / id_num) + points.at(i + 1) * double(j) / id_num; // 对每一个中间点之间的路径按照线性插值求出中间点的坐标
          inter_points.push_back(inter_pt);
        }
      }
    }

    inter_points.push_back(points.back()); // 获得所有中间点的坐标数组

    // write position matrix 组合数组矩阵
    int pt_num = inter_points.size();
    Eigen::MatrixXd pos(3, pt_num);
    for (int i = 0; i < pt_num; ++i)
      pos.col(i) = inter_points[i];

    Eigen::Vector3d zero(0, 0, 0);
    Eigen::VectorXd time(pt_num - 1);
    for (int i = 0; i < pt_num - 1; ++i)
    {
      time(i) = (pos.col(i + 1) - pos.col(i)).norm() / (pp_.max_vel_); // 计算每一个点到下一个点之间的时间，由两个点之间的距离除以最大的速度计算
    }

    //第一段路线的时间和最后一段的时间设置为2倍
    time(0) *= 2.0;
    time(time.rows() - 1) *= 2.0;

    PolynomialTraj gl_traj;
    if (pos.cols() >= 3) // 如果一段轨迹中有多个点，采用多项式进行生成平滑轨迹
      gl_traj = PolynomialTraj::minSnapTraj(pos, start_vel, end_vel, start_acc, end_acc, time);
    else if (pos.cols() == 2) // 如果只有两个点，则只有开始点和结束点两段轨迹
      gl_traj = PolynomialTraj::one_segment_traj_gen(start_pos, start_vel, start_acc, end_pos, end_vel, end_acc, time(0));
    else
      return false;

    auto time_now = ros::Time::now();
    global_data_.setGlobalTraj(gl_traj, time_now);

    return true;
  }
```
上面的代码是实现了全局的轨迹规划的代码，主要流程是将首尾点中插入中间点，然后根据中间点数量不同进行不同的规划方法，当中间点数量大于2时，使用多项式规划，当数量小于=2时，使用单段轨迹规划。
**单段轨迹规划代码分析**
单段轨迹中的轨迹规划使用五次多项式进行轨迹规划
```cpp
PolynomialTraj PolynomialTraj::one_segment_traj_gen(const Eigen::Vector3d &start_pt, const Eigen::Vector3d &start_vel, const Eigen::Vector3d &start_acc,
                                                    const Eigen::Vector3d &end_pt, const Eigen::Vector3d &end_vel, const Eigen::Vector3d &end_acc,
                                                    double t)
{
  // 只有一段轨迹的情况下进行多项式的规划
  Eigen::MatrixXd C = Eigen::MatrixXd::Zero(6, 6), Crow(1, 6);
  Eigen::VectorXd Bx(6), By(6), Bz(6);

  C(0, 5) = 1;
  C(1, 4) = 1;
  C(2, 3) = 2;
  Crow << pow(t, 5), pow(t, 4), pow(t, 3), pow(t, 2), t, 1;
  C.row(3) = Crow;
  Crow << 5 * pow(t, 4), 4 * pow(t, 3), 3 * pow(t, 2), 2 * t, 1, 0;
  C.row(4) = Crow;
  Crow << 20 * pow(t, 3), 12 * pow(t, 2), 6 * t, 2, 0, 0;
  C.row(5) = Crow;

  Bx << start_pt(0), start_vel(0), start_acc(0), end_pt(0), end_vel(0), end_acc(0);
  By << start_pt(1), start_vel(1), start_acc(1), end_pt(1), end_vel(1), end_acc(1);
  Bz << start_pt(2), start_vel(2), start_acc(2), end_pt(2), end_vel(2), end_acc(2);

  Eigen::VectorXd Cofx = C.colPivHouseholderQr().solve(Bx);
  Eigen::VectorXd Cofy = C.colPivHouseholderQr().solve(By);
  Eigen::VectorXd Cofz = C.colPivHouseholderQr().solve(Bz);

  vector<double> cx(6), cy(6), cz(6);
  for (int i = 0; i < 6; i++)
  {
    cx[i] = Cofx(i);
    cy[i] = Cofy(i);
    cz[i] = Cofz(i);
  }

  PolynomialTraj poly_traj;
  poly_traj.addSegment(cx, cy, cz, t);

  return poly_traj;
}
```
为什么要在轨迹规划中采用五次多项式，因为五次多项式在二阶导数和三阶导数上都是连续的，可以保障轨迹的平滑性。
