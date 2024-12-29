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
        "--compile-commands-dir=${workspaceFolder}"
    ],
    "C_Cpp.default.configurationProvider": "llvm-vs-code-extensions.vscode-clangd"
}
```
