# 机械革命安装amd 880m核显驱动艰辛历程

## 软件源问题
不要随便屏蔽安装源，有可能会导致universe源等无法更新，造成dkms库无法安装
如果已经遇到安装源问题，建议使用fishros添加相关的源。
## amdgpu-install问题
```bash
amdgpu-install 
Hit:1 http://mirrors.ustc.edu.cn/ubuntu jammy InRelease
Hit:2 http://mirrors.ustc.edu.cn/ubuntu jammy-updates InRelease
Hit:3 http://mirrors.ustc.edu.cn/ubuntu jammy-backports InRelease
Hit:4 http://mirrors.ustc.edu.cn/ubuntu jammy-security InRelease
Hit:5 http://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu jammy InRelease
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package amdgpu-lib
E: Unable to locate package amdgpu-lib32
E: Unable to locate package rocm-opencl-runtime
E: Unable to locate package rocm-hip-runtime
E: Unable to locate package amdgpu-dkms
```
从你提供的信息来看，你尝试运行 `amdgpu-install` 来安装 AMD GPU 相关的驱动或软件包，但遇到了类似“E: Unable to locate package”的错误。这表明系统中当前配置的软件源中无法找到 `amdgpu-lib`、`amdgpu-lib32`、`rocm-opencl-runtime`、`rocm-hip-runtime` 和 `amdgpu-dkms` 等包。以下是可能的原因和解决方法：

---

### 可能原因
1. **`amdgpu-install` 工具未正确安装**  
   你可能还没有安装 `amdgpu-install` 脚本，或者它没有正确添加到系统的 PATH 中，导致无法识别命令或其依赖。

2. **AMD 官方软件源未添加**  
   默认的 Ubuntu 软件源（如 `mirrors.ustc.edu.cn`）并不包含 AMD 的专有驱动或 ROCm 相关包。你需要手动添加 AMD 的官方软件源（`repo.radeon.com`）。

3. **软件源未更新**  
   如果你添加了 AMD 软件源但没有运行 `sudo apt update`，系统无法获取最新的包信息。

4. **Ubuntu 版本兼容性问题**  
   你使用的是 Ubuntu 22.04（Jammy Jellyfish），但某些 AMD 包可能需要特定版本的 ROCm 或驱动支持。如果使用了不匹配的版本，可能会出现找不到包的情况。

---

### 解决步骤

#### 1. 安装 `amdgpu-install` 工具
首先，你需要从 AMD 官方网站下载并安装 `amdgpu-install` 脚本。以 Ubuntu 22.04 为例：
```bash
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/jammy/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
```
- 这里的 `6.3.3` 是截至 2025 年 4 月的一个较新版本，你可以访问 [AMD ROCm 安装页面](https://repo.radeon.com/amdgpu-install/) 检查最新版本。
- 安装完成后，`amdgpu-install` 命令应该可用。

#### 2. 添加 AMD 软件源
安装 `amdgpu-install` 后，它会自动配置 AMD 的软件源。你可以通过以下命令验证：
```bash
cat /etc/apt/sources.list.d/amdgpu.list
```
输出应类似于：
```
deb [arch=amd64] https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy main
```
如果没有，手动添加：
```bash
echo "deb [arch=amd64] https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/amdgpu.list
sudo apt update
```

#### 3. 运行 `amdgpu-install`
安装并配置好后，运行以下命令安装所需的包：
```bash
sudo amdgpu-install -y
```
- 默认情况下，这会安装 `graphics`、`opencl` 和 `hip` 相关的包（包括 `amdgpu-dkms`、`rocm-opencl-runtime` 等）。
- 如果你只需要特定功能，可以指定 `--usecase`，例如：
  - 只安装内核驱动：`sudo amdgpu-install --usecase=dkms`
  - 安装 ROCm 完整堆栈：`sudo amdgpu-install --usecase=rocm`

#### 4. 检查安装结果
安装完成后，验证是否成功：
```bash
dpkg -l | grep amdgpu
dpkg -l | grep rocm
```
如果看到相关包（如 `amdgpu-dkms`、`rocm-opencl-runtime`），说明安装成功。

#### 5. 解决特定包缺失问题
如果仍然提示找不到某些包（例如 `amdgpu-lib32`），可能是因为：
- 32 位支持需要额外启用。运行：
  ```bash
  sudo dpkg --add-architecture i386
  sudo apt update
  sudo amdgpu-install -y --no-32  # 如果不需要 32 位支持，可以跳过此包
  ```
- 某些包名可能已更改或不适用于你的用例。可以搜索可用包：
  ```bash
  apt search amdgpu
  apt search rocm
  ```

---

### 如果仍然失败
请提供更多信息以便进一步排查：
1. 你运行 `sudo apt update` 后的完整输出。
2. `/etc/apt/sources.list.d/` 目录下的文件内容（特别是 `amdgpu.list` 和 `rocm.list`）。
3. 你希望安装的具体功能（例如仅驱动、ROCm、OpenCL 等）。

通常情况下，按照上述步骤添加 AMD 软件源并安装 `amdgpu-install` 后，问题应该能解决。试试看吧！

E: Unable to locate package rocm-opencl-runtime
E: Unable to locate package rocm-hip-runtime

从你提供的错误信息来看，`E: Unable to locate package rocm-opencl-runtime` 和 `E: Unable to locate package rocm-hip-runtime` 表明在你当前的 Ubuntu 系统中，APT 包管理器无法找到这两个软件包。这通常是因为软件源未正确配置或系统中缺少必要的 AMD ROCm 软件源。结合你之前提到使用 Ubuntu 22.04（Jammy），以下是问题的可能原因和解决方法：

---

### 可能原因
1. **AMD ROCm 软件源未添加**  
   默认的 Ubuntu 软件源（如 `mirrors.ustc.edu.cn`）不包含 ROCm 相关的包（如 `rocm-opencl-runtime` 和 `rocm-hip-runtime`）。你需要添加 AMD 官方的 ROCm 软件源。

2. **软件源未更新**  
   如果你添加了 ROCm 软件源但没有运行 `sudo apt update`，系统无法获取最新的包信息。

3. **`amdgpu-install` 未正确安装或使用**  
   `rocm-opencl-runtime` 和 `rocm-hip-runtime` 是通过 `amdgpu-install` 工具安装的。如果你没有安装这个工具，或者没有正确运行它，会导致这些包不可用。

4. **版本兼容性问题**  
   你可能尝试安装的 ROCm 版本与 Ubuntu 22.04 不完全兼容，或者指定的版本在当前软件源中不可用。

---

### 解决步骤

#### 1. 确保安装 `amdgpu-install`
首先，检查是否已安装 `amdgpu-install` 工具。如果没有，请从 AMD 官方网站下载并安装。以 Ubuntu 22.04 为例：
```bash
sudo apt update
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/jammy/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
```
- `6.3.3` 是截至 2025 年 4 月的一个较新版本，你可以访问 [AMD ROCm 下载页面](https://repo.radeon.com/amdgpu-install/) 检查最新版本。
- 安装后，运行 `amdgpu-install --version` 确认工具可用。

#### 2. 添加 AMD ROCm 软件源
安装 `amdgpu-install` 后，它会自动配置 AMD 的软件源。检查是否已添加：
```bash
cat /etc/apt/sources.list.d/amdgpu.list
cat /etc/apt/sources.list.d/rocm.list
```
- 应该看到类似以下内容：
  ```
  deb [arch=amd64] https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy main
  deb [arch=amd64] https://repo.radeon.com/rocm/apt/6.3.3 jammy main
  ```
- 如果没有，手动添加：
  ```bash
  echo "deb [arch=amd64] https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/amdgpu.list
  echo "deb [arch=amd64] https://repo.radeon.com/rocm/apt/6.3.3 jammy main" | sudo tee /etc/apt/sources.list.d/rocm.list
  sudo apt update
  ```

#### 3. 安装 ROCm 相关包
使用 `amdgpu-install` 安装所需的 ROCm 组件：
```bash
sudo amdgpu-install --usecase=rocm -y
```
- `--usecase=rocm` 会安装完整的 ROCm 堆栈，包括 `rocm-opencl-runtime` 和 `rocm-hip-runtime`。
- 如果你只需要特定组件，可以分别指定：
  - OpenCL：`sudo amdgpu-install --usecase=opencl -y`
  - HIP：`sudo amdgpu-install --usecase=hip -y`

#### 4. 验证安装
安装完成后，检查是否成功：
```bash
dpkg -l | grep rocm
```
- 应该能看到 `rocm-opencl-runtime` 和 `rocm-hip-runtime` 等包。
- 运行以下命令测试：
  ```bash
  /opt/rocm/bin/rocminfo
  /opt/rocm/opencl/bin/clinfo
  ```
  如果输出显示你的 GPU 信息，说明安装成功。

#### 5. 解决可能的依赖冲突
如果仍然报错，可能是依赖冲突。尝试修复：
```bash
sudo apt update
sudo apt install -f
sudo amdgpu-install --usecase=rocm -y
```

---

### 如果仍然失败
请提供以下信息，我可以进一步帮你排查：
1. `sudo apt update` 的完整输出。
2. `/etc/apt/sources.list` 和 `/etc/apt/sources.list.d/` 下所有文件的完整内容。
3. 你运行 `amdgpu-install` 时的完整输出。

通常情况下，按照上述步骤添加 AMD 软件源并使用 `amdgpu-install` 安装 ROCm 后，`rocm-opencl-runtime` 和 `rocm-hip-runtime` 应该能正常安装。试试看吧！

linux-headers-6.8.0-57-generic is already the newest version (6.8.0-57.59~22.04.1).
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 amdgpu-lib32 : Depends: libdrm2-amdgpu:i386 but it is not installable
                Depends: libdrm-amdgpu-amdgpu1:i386 but it is not installable
                Depends: libllvm-amdgpu:i386 but it is not installable
                Depends: libxatracker2-amdgpu:i386 but it is not installable
                Depends: libgbm1-amdgpu:i386 but it is not installable
                Depends: libegl1-amdgpu-mesa:i386 but it is not installable
                Depends: libegl1-amdgpu-mesa-drivers:i386 but it is not installable
                Depends: libglapi-amdgpu-mesa:i386 but it is not installable
                Depends: libgl1-amdgpu-mesa-glx:i386 but it is not installable
                Depends: libgl1-amdgpu-mesa-dri:i386 but it is not installable
E: Unable to correct problems, you have held broken packages.

从你提供的信息来看，你尝试安装 `amdgpu-lib32`（AMD GPU 驱动的 32 位支持库），但遇到了依赖问题。错误提示表明一些依赖包（如 `libdrm2-amdgpu:i386`、`libdrm-amdgpu-amdgpu1:i386` 等）无法安装，导致安装失败。以下是问题的分析和解决步骤：

---

### 问题分析
1. **32 位依赖不可用**  
   错误信息显示 `amdgpu-lib32` 需要一系列 32 位库（`:i386` 表示 32 位架构），但这些包在你的系统中“not installable”（不可安装）。这可能是因为：
   - AMD 的软件源没有提供这些 32 位库的最新版本。
   - 你的系统未启用 32 位架构支持。
   - Ubuntu 22.04（Jammy）对 32 位支持有限，且 AMD 的驱动可能不再完全支持 32 位库。

2. **内核版本与驱动兼容性**  
   你当前使用的是 `linux-headers-6.8.0-57-generic`，这是一个较新的内核版本（可能是通过 HWE 更新获得的）。AMD 的驱动（特别是通过 `amdgpu-install` 安装的版本）可能尚未完全适配这个内核，导致依赖冲突。

3. **破损的包或依赖冲突**  
   错误提示“you have held broken packages”表明系统中可能存在被“hold”（锁定）的包，或者之前的安装尝试导致了依赖关系混乱。

---

### 解决步骤

#### 1. 启用 32 位架构支持
确保你的系统支持 32 位包：
```bash
sudo dpkg --add-architecture i386
sudo apt update
```
如果没有启用 32 位支持，某些 `:i386` 包可能无法找到。

#### 2. 检查 AMD 软件源
确保你已经正确添加了 AMD 的软件源，并且版本与 Ubuntu 22.04 匹配。运行以下命令检查：
```bash
cat /etc/apt/sources.list.d/amdgpu.list
```
输出应类似于：
```
deb [arch=amd64] https://repo.radeon.com/amdgpu/6.3.3/ubuntu jammy main
```
如果没有 32 位支持，可能需要额外添加（但 AMD 通常只提供 64 位为主的源）。更新源：
```bash
sudo apt update
```

#### 3. 安装不带 32 位支持的驱动
由于 32 位支持在较新的 Ubuntu 版本和 AMD 驱动中逐渐减少，如果你不需要 32 位应用，可以跳过 `amdgpu-lib32`，直接安装 64 位驱动：
```bash
sudo amdgpu-install --no-32 -y
```
- `--no-32` 参数会跳过 32 位库的安装，避免依赖问题。

#### 4. 修复破损的包
尝试修复现有的依赖冲突：
```bash
sudo apt update
sudo apt install -f
sudo dpkg --configure -a
```
然后再次尝试安装：
```bash
sudo amdgpu-install --no-32 -y
```

#### 5. 检查内核与驱动兼容性
你的内核版本是 `6.8.0-57`，而 AMD 的驱动可能需要匹配的 DKMS 模块。确保 `amdgpu-dkms` 已正确安装：
```bash
dpkg -l | grep amdgpu-dkms
```
如果没有安装，单独安装：
```bash
sudo apt install amdgpu-dkms
```
如果仍然失败，可能需要回退到较旧的内核版本（例如 5.15 或 6.2），方法如下：
```bash
sudo apt install linux-generic
sudo reboot
```
重启后选择旧内核启动，再次尝试安装。

#### 6. 清理并重装
如果以上方法仍无法解决，清理现有安装并重新开始：
```bash
sudo amdgpu-uninstall
sudo apt purge amdgpu* rocm*
sudo apt autoremove
sudo rm -f /etc/apt/sources.list.d/amdgpu.list
sudo rm -f /etc/apt/sources.list.d/rocm.list
```
然后重新下载并安装最新版本的 `amdgpu-install`：
```bash
wget https://repo.radeon.com/amdgpu-install/6.3.3/ubuntu/jammy/amdgpu-install_6.3.60303-1_all.deb
sudo apt install ./amdgpu-install_6.3.60303-1_all.deb
sudo amdgpu-install --no-32 -y
```

#### 7. 验证安装
安装完成后，检查驱动是否正常工作：
```bash
lsmod | grep amdgpu
/opt/rocm/bin/rocminfo
```
如果输出显示 GPU 信息，说明安装成功。

---

### 如果仍然失败
可能是 AMD 驱动对 Ubuntu 22.04 的 HWE 内核（6.8）或 32 位支持存在问题。请提供以下信息：
1. `sudo apt update` 的完整输出。
2. `uname -r` 的输出（确认当前内核）。
3. 你运行 `amdgpu-install` 时的完整错误日志。

通常情况下，使用 `--no-32` 参数跳过 32 位支持可以解决问题，因为现代系统和应用很少需要 32 位库。试试看吧！
