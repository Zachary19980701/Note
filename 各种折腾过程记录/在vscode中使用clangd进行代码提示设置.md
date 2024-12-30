# 在Vscode中使用clangd进行代码提示设置
## Vscode及部分插件的安装
相关需要安装的插件与依赖：
1. Vscode
2. C/C++ (Microsoft)
3. clang-format
4. clang

## 在cmakelists中需要修改的部分
在Cmakelists文件开始部分设置编译输出
```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

## 在vscode中本地文件夹中添加设置
```json
{
    "clangd.arguments": [
        "--compile-commands-dir=/home/robot/gap_detour_ws/build/reactive_assistance", //指定到你指定的文件夹
    ],
    "clangd.path": "/usr/bin/clangd",
    "C_Cpp.default.configurationProvider": "llvm-vs-code-extensions.vscode-clangd"
}
```
## 关于远程主机中设置的一些坑
**1. 远程ssh无法进行代码补全**
因为在之前的设置中，没有指定clangd的位置，导致远程时依然要从本地的路径中寻找clangd的解释器，添加一行说明文件：
```json
"clangd.path": "/usr/bin/clangd",
```
这样子就可以从远程主机中寻找clangd的解释器。
