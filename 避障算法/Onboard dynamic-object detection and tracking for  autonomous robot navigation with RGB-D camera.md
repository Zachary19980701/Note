# Onboard dynamic-object detection and tracking for  autonomous robot navigation with RGB-D camera
there three problems of mobile robot obstacle detection and tracking:
- onboard computatioon resources is limited, deeplearning methods are not applicable
- the depth camera's FOV is limited, make obstacle detection difficult
- the noise of depth camera is high

**based the above three problrms, the author presents 3D dynamiv obstacle detection and tracking(DODT) based on RGB-D camera**

to compare with other methods which use **sigle detoctor**, 
the author presents a **multi-detector** to obstain fast and accurate obstracle detection

**The authort presents three novel contributions:**
- efficient ensemble detection by combaining mutli-detectors
- feature-based association and tracking
- Auxiliary Learning-based Detection Module

## related work
**Pointcloud based method**
1. Combain YOLO and PCL for human detection----T. Eppenberger, G. Cesari, M. Dymczyk, R. Siegwart, and R. Dub ́e, “Leveraging stereo-camera data for real-time dynamic obstacle detection and tracking,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2020, pp. 10 528–10 535.
2. clustering-based detection for indoor dynamic obstacle avoidance [Autonomous flights in dynamic environments with onboard vision]
3. point cloud feature vectors and object track points to identify correct object matches and estimate their states
4. KD-Tree map is directly constructed from the LiDAR point cloud for dynamic obstacle avoidance [Avoiding dynamic small obstacles with onboard sensing and computation on aerial robots]
## System Review
![图 2](../images/ecf7845735353bbd25e4ce6fbbb9e278b3f87c20fa4f106f5cf8dae5f0824d7f.png)  
**The system can be disilluted into three parts:**
- Pointcloud and image input
- Mutli-detector for obstacles detection, which  departed into two parts: Non-learning detection and Learning-based detection.
- Obstacle association and tracking
- Dynamic obstacle indentication
- Remove dynamic obstacles from map
- Output dynamic osbtacles
### 3D-osbtacle detector
Three methods obstacle detector are presented:
- **U-depth**
- **DB-SCAN**
- **YOLO-MAD**
And all detectors return axis-aligned bounding box(AABB)
#### U-depth

