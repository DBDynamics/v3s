# PyV3s 控制器文档

## 目录
- [简介](#简介)
- [资源特性](#资源特性)
- [产品细节](#产品细节)
- [配件介绍](#配件介绍)
- [机械尺寸](#机械尺寸)
- [接口布局](#接口布局)
- [开发指南](#开发指南)
- [参考示例](#参考示例)
- [相关视频](#相关视频)

## 简介

![](images/v3s_0.png)

PyV3s是DBD团队开发的一款超小型Python控制器，具有以下特点：

### 核心特性
- **超小尺寸**：仅50mm × 60mm
- **高性能处理器**：全志科技V3s (ARM Cortex-A7)，主频1GHz
- **内存配置**：64M内存，512M存储空间
- **操作系统**：基于buildroot的主线Linux系统
- **协处理器**：ARM Cortex-M0，负责实时通信和编码器数据处理

### 接口配置
- 百兆以太网接口 × 1
- USB2.0接口 × 1
- TTL串口 × 2路
- AB增量编码器接口 × 1路
- 数字输入 × 4路
- 数字输出 × 4路
- RS485通信 × 2路
- 主电源/备用电源接口
- **编程语言**：支持Python编程

* * *

## 资源特性

| 参数 | 规格 |
|------|------|
| **重量** | 7.2g |
| **适配设备** | 全系列Bee电机驱动器/IO板/灯光控制器/编码器 |
| **工作电压** | DC 12V/24V |
| **最大持续输出电流** | 200mA |
| **状态指示灯** | 蓝色 |
| **USB总线速度** | 480Mbps |
| **以太网速度** | 100Mbps |
| **RS485总线速度** | 250Kbps/500Kbps |
| **运行温度** | -10°C ~ +60°C |  
  
## 产品细节

![](images/v3s_001.png) ![](images/v3s_002.png) ![](images/v3s_003.png)

## 配件介绍

### 标准配件清单
- **电源线**：用于12V/24V直流供电
- **网口线**：用于以太网通信连接
- **TTL串口线**：用于串口通信和调试
- **USB线**：用于USB通信和数据传输
- **IO输入线**：用于连接输入传感器
- **IO输出线**：用于连接输出设备
- **编码器线**：用于连接增量编码器

## 机械尺寸

> 详细尺寸图纸请参考产品规格书

## 接口布局

![](images/v3s.png)

### 供电接口

| 参数 | 规格 |
|------|------|
| **供电电压** | 12V/24V DC |
| **接插件** | XH2.54-2P |
| **最大电流** | <3A |
| **备用电源** | 12V/24V DC |  
  
### RS485通信接口

| 参数 | 规格 |
|------|------|
| **对外供电电压** | 5V DC |
| **接插件** | XH2.54-4P |
| **通道数** | 2 |
| **波特率** | 250Kbps |

### 以太网通信接口

| 参数 | 规格 |
|------|------|
| **通信速率** | 100Mbps |
| **IP地址(静态)** | 192.168.10.22 |
| **接插件** | PHB2.0-2x2 |

### USB通信接口

| 参数 | 规格 |
|------|------|
| **通信速率** | 480Mbps |
| **接插件** | PHB2.0-2x2 |  
  
### UART0通信接口

| 参数 | 规格 |
|------|------|
| **通信速率** | 115200bps |
| **接插件** | PHB2.0-2x2 |
| **功能** | 串口调试终端，可用putty连接 |

### UART1通信接口

| 参数 | 规格 |
|------|------|
| **通信速率** | 自定义 |
| **接插件** | PHB2.0-2x2 |
| **功能** | 自定义 |
| **端口** | /dev/ttyS1 |

### UART2通信接口

| 参数 | 规格 |
|------|------|
| **通信速率** | 自定义 |
| **接插件** | PHB2.0-2x2 |
| **功能** | 自定义 |
| **端口** | /dev/ttyS2 |  
  
### IO输出接口

| 参数 | 规格 |
|------|------|
| **通道数** | 4 |
| **接插件** | PHB2.0-2x2 |
| **功能** | 自定义 |
| **输出类型** | 开漏输出（低电平有效） |

### IO输入接口

| 参数 | 规格 |
|------|------|
| **通道数** | 4 |
| **接插件** | PHB2.0-2x3 |
| **功能** | 自定义 |
| **输入类型** | 内部上拉（低电平有效，配合NPN类型接近开关） |  
  
## 开发指南

### 常用开发工具

| 工具 | 用途 |
|------|------|
| **VsCode** | 代码编辑和开发环境 |
| **WinScp** | 文件传输工具 |
| **MobaXterm** | SSH终端和X11服务器 |
| **Putty** | SSH终端连接工具 |

### 最新库文件下载

- [libpro.py](python/libpro.py) - 主要功能库
- [libio.py](python/libio.py) - IO控制库

### 连接方式

#### USB串口终端登录
> [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

#### 网口登录控制器
> 默认IP地址：192.168.10.22

#### VsCode开发环境配置
> [vscode](https://code.visualstudio.com/)

#### WinSCP文件传输
> 用于上传/下载代码文件
> [winscp](https://winscp.net/eng/download.php)

#### MobaXTerm使用
> 集成SSH和文件传输功能
> [mobaxterm](https://mobaxterm.mobatek.net/download.html)

### Python代码运行

登录系统后，使用以下命令运行Python代码：

```bash
python3 your_script.py
```

将 `your_script.py` 替换为您要运行的文件名。

### 开机自动运行设置

要设置开机自动运行Python代码，需要修改文件 `/etc/init.d/S60motion`：

1. 找到以下行并去掉注释符号 `#`：
   ```bash
   #nohup /usr/bin/python3 /root/motion.py &
   ```

2. 将 `motion.py` 替换为您要启动的文件名

3. **注意**：程序中所有涉及到路径的地方都需要使用绝对路径

**完整的S60motion脚本示例：**

```bash
#!/bin/sh
#
# Starts DBD Motion
#

# Allow a few customizations from a config file

start() {
    /sbin/insmod /root/hello.ko
    # printf "start motion..."
    # sleep 1
    nohup /usr/bin/python3 /root/your_script.py &
    # printf "start demo..."
}

stop() {
    printf "Stopping motion"
}

restart() {
    stop
    start
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart|reload)
    restart
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

exit $?
```

### IO接口使用示例

#### 输入IO使用

PyV3s控制器拥有4个IO输入端口，硬件连接注意事项：
- 传感器选用NPN类型
- 支持常开或常闭触点
- 内部已配置上拉电阻

**代码示例：**

```python
from libio import GPIO
import time

io = GPIO()

for loop in range(0, 100):
    ret = io.getInput()
    if ret & 0x1:
        print("Button 0 pressed")
    if ret & 0x2:
        print("Button 1 pressed")
    if ret & 0x4:
        print("Button 2 pressed")
    if ret & 0x8:
        print("Button 3 pressed")
    time.sleep(0.1)
```

#### 输出IO使用

> 输出IO为开漏输出，低电平有效，可用于控制继电器、LED等设备

#### TTL串口使用 (ttyS1/ttyS2)

**代码示例：**

```python
import serial
import time

portName = '/dev/ttyS2'

# 初始化串口
port = serial.Serial(portName, 9600, timeout=0.1)

# 构建消息数据
message = bytearray(8)
message[0] = 0x01  # 设备地址
message[1] = 0x03  # 功能码
message[2] = 0x00  # 起始地址高位
message[3] = 0x00  # 起始地址低位
message[4] = 0x00  # 寄存器数量高位
message[5] = 0x03  # 寄存器数量低位
message[6] = 0x05  # CRC校验低位
message[7] = 0xCB  # CRC校验高位

# 循环发送和接收数据
for loop in range(0, 100):
    port.write(message)
    time.sleep(1)
    ret = port.read(11)
    print(f"Received: {ret}")

# 关闭串口
port.close()
```
### RS485总线的使用
#### 扫描在线设备
```bash
# python3 scan.py
Searching Online Devices...
Online Devices:
[0, 1]
# 
```
注意: 出厂默认编号为0或者0,1 需要单独连接每一个设备进行修改保存 保证编号不重复再进行总线级联
### 如何修改ID
- [最新changeID.py](python/changeID.py)
例子: 把ID为0的设备修改为ID为2
```bash
# python3 changeID.py 0 2
正在将设备ID从 0 修改为 2
设备ID修改成功：0 -> 2
```
例子: 把ID为0的设备修改为ID为4
```bash
# python3 changeID.py 0 4
正在将设备ID从 0 修改为 4
设备ID修改成功：0 -> 4
```
注意: 一拖二双轴驱动器只需要修改第一个编号 比如 0,1 只需要修改0->N 1会自动修改为N+1 

### 如果使用位置模式
> 位置模式的核心参数及意义
- 目标位置: 想要到达的位置
- 运行速度: 在运行过程中能达到的最大运行速度
- 加速时间: 加速到最大运行速度需要的时间
- 实际位置: 当前时间电机的位置

> 位置模式的运行原理:
- 进入位置模式后, 当目标位置与实际位置不同时,开始运动.
- 运动时有加速过程和减速过程, 由加速时间与运行速度决定

> 示例代码 [demo_beed.py](python/demo_beed.py)
``` python
# 导入libpro库中的Bee类，用于控制步进电机
from libpro import Bee

# 创建Bee对象实例，用于电机控制
m = Bee()

# 设置目标速度为1000
m.setTargetVelocity(1000)

# 设置加速时间为500毫秒
m.setAccTime(500)

# 定义轴ID为0，表示控制第0号轴
axis_id = 0

# 循环执行3次往返运动
for loop in range(3):
    # 设置目标位置为51200*3=153600脉冲（正向运动）
    m.setTargetPosition(axis_id, 51200*3)
    # 等待电机到达目标位置
    m.waitTargetPositionReached(axis_id)

    # 设置目标位置为0（返回原点）
    m.setTargetPosition(axis_id, 0)
    # 等待电机到达原点位置
    m.waitTargetPositionReached(axis_id)

# 停止电机运行并释放资源
m.stop()
```

### 如何使用回零模式
> 回零模式的核心参数及意义
- 回零方向: 回零运动的方向, 可以是正方向或负方向
- 回零触发电平: 触发回零运动的电平, 通常是低电平或高电平
- 回零过程中的目标速度: 回零过程中电机的运行速度, 可以根据需要调整
> 回零模式的运行原理:
- 回零模式下, 电机根据设置的回零方向和触发电平, 开始向回零方向运动.
- 当触发电平触发时, 电机停止运动, 并将当前位置作为新的原点.
- 回零模式通常用于将电机定位到一个已知的参考点, 例如零点或参考线.

> 回零模式的示例代码 [demo_home.py](python/demo_home.py)
``` python
# 导入libpro库中的Bee类，用于控制步进电机
from libpro import Bee
# 从demo_beed模块导入axis_id（虽然下面重新定义了）
from python.demo_beed import axis_id

# 创建Bee对象实例，用于电机控制
m = Bee()

# 定义轴ID为0，表示控制第0号轴
axis_id = 0

# 设置回零方向为1（正方向回零）
# 参数说明：1=正方向，-1=负方向
m.setHomingDirection(axis_id, 1)

# 设置回零触发电平为0（低电平触发）
# 参数说明：0=低电平触发，1=高电平触发
m.setHomingLevel(axis_id, 0)

# 设置回零过程中的目标速度为200（脉冲/秒）
m.setTargetVelocity(axis_id, 200)

# 启动回零模式，电机开始寻找原点位置
m.setHomingMode(axis_id)

# 等待回零完成，直到电机到达原点位置
m.waitTargetPositionReached(axis_id)

# 停止电机运行并释放资源
m.stop()
```
### 如何使用同步插补模式
> 同步插补模式的核心参数及意义
- 关键帧信息:包含关键帧时间和每一个轴的关键位置信息
> 同步插补模式的工作原理
- 进入同步规划插补模式后, 控制器会周期性的把规划缓存里的目标位置同步给电机驱动器或灯光驱动器进行执行
- 调用插入关键帧API可以插入关键时间和关键位置等信息, 
- 关键帧数据准备好后调用处理插补API进行多轴轨迹同步插补
- 插补的数据自动压入发送缓存, 调用等待数据发送完成API可以判断轨迹是否运动完成
> 同步插补模式的示例代码 [demo_isp.py](python/demo_isp.py)
``` python
# 导入libpro库中的Bee类，用于控制步进电机
from libpro import Bee

# 创建Bee对象实例，用于多轴电机控制
m = Bee()


def homeAll():
    """
    回零函数：将所有电机轴回到原点位置
    在同步插补模式前必须执行此操作
    """
    print("homeAll")

# 注意: 进入同步插补模式前 要保证驱动的当前位置和我们规划数据的起始位置一致
# 如果不一致 会导致目标位置与当前位置差值过大 不符合运动学定律 
# 一般会采用先回零 再进入同步插补模式 这样所有电机轴的位置都是从0开始 

# 执行所有轴的回零操作，确保起始位置一致
homeAll()

# 设置0-7号轴为同步插补位置模式
# 同步插补模式允许多个轴协调运动，实现复杂的轨迹控制
for axis in range(0, 8):
    m.setInterpolationPositionMode(axis)

# 为每个轴设置关键帧数据，定义运动轨迹
for axis in range(0, 8):
    # 设置关键帧：(轴号, 时间点, 位置值)
    m.setKeyFrame(axis, 0, 0)      # 第0帧：位置0（起始点）
    m.setKeyFrame(axis, 1, 0)      # 第1帧：位置0（保持静止）
    m.setKeyFrame(axis, 100, 51200) # 第100帧：位置51200（运动到目标位置）
    m.setKeyFrame(axis, 199, 0)     # 第199帧：位置0（返回原点）
    m.setKeyFrame(axis, 200, 0)     # 第200帧：位置0（结束点）

# 开始处理插补运算，根据关键帧数据生成平滑的运动轨迹
m.processInterpolation()

# 等待插补运动完成，监控第0轴的运动状态
# 由于是同步插补，所有轴会同时完成运动
m.waitISP(0)

# 停止所有电机运行并释放资源
m.stop()
```
## libpro.Bee 类库详解

### 🔧 **核心功能**
`libpro.Bee` 是一个用于控制步进电机和无刷直流电机的Python库，主要用于工业自动化和运动控制系统。

### 📋 **主要特性**

#### 1. **设备类型支持**
```python
# 支持的设备类型
_BOARD_TYPE_STEPPER_ANT = 0x10      # 步进电机 ANT
_BOARD_TYPE_STEPPER_BEE = 0x11      # 步进电机 BEE  
_BOARD_TYPE_STEPPER_ELEPHANT = 0x12 # 步进电机 ELEPHANT
_BOARD_TYPE_BDCS_BEE = 0x13         # 有刷直流电机 BEE
_BOARD_TYPE_BDC_BEE = 0x14          # 直流电机 BEE
_BOARD_TYPE_BLDCS_BEE = 0x15        # 无刷直流电机 BEE
```

#### 2. **运行模式**
```python
# 操作模式
_OPERATION_MODE_PWM = 0                    # PWM模式
_OPERATION_MODE_PROFILE_VELOCITY = 21     # 速度模式
_OPERATION_MODE_PROFILE_POSITION = 31     # 位置模式
_OPERATION_MODE_HOMING = 40               # 回零模式
_OPERATION_MODE_ESTOP = 61                # 急停模式
_OPERATION_SYNC_INTERPOLATION_POSITION = 34 # 同步插补位置模式
```

### 🚀 **常用方法分类**

#### **电源控制**
```python
m = Bee()
m.setPowerOn(id)           # 上电
m.setPowerOff(id)          # 断电
m.setPowerLimit(id, value) # 设置功率限制
```

#### **运动控制**
```python
# 设置运行模式
m.setVelocityMode(id)      # 速度模式
m.setPositionMode(id)      # 位置模式
m.setHomingMode(id)        # 回零模式
m.setPWMMode(id)           # PWM模式

# 运动参数设置
m.setTargetVelocity(id, velocity)  # 设置目标速度
m.setTargetPosition(id, position)  # 设置目标位置
m.setAccTime(id, time)             # 设置加速时间
```

#### **状态读取**
```python
# 获取实时状态
position = m.getActualPosition(id)  # 获取当前位置
velocity = m.getActualVelocity(id)  # 获取当前速度
status = m.getStatus(id)            # 获取设备状态
io_input = m.getInputIO(id)         # 获取IO输入状态
```

#### **参数配置**
```python
# PID参数调节
m.setKPP(id, value)        # 设置位置比例增益
m.setKPI(id, value)        # 设置位置积分增益
m.setKVF(id, value)        # 设置速度前馈增益
m.setKFF(id, value)        # 设置前馈增益

# 电流控制
m.setRunningCurrent(id, current)   # 设置运行电流
m.setKeepingCurrent(id, current)   # 设置保持电流
m.setCurrentMax(id, current)       # 设置最大电流
```

#### **设备管理**
```python
# 设备扫描和ID管理
devices = m.scanDevices()          # 扫描在线设备
m.changeID(old_id, new_id)         # 修改设备ID
board_type = m.getBoardType(id)    # 获取设备类型
```

### 💡 **典型使用示例**

```python
from libpro import Bee
import time

# 初始化
m = Bee()

# 设备ID
device_id = 0

try:
    # 1. 上电
    m.setPowerOn(device_id)
    time.sleep(0.5)
    
    # 2. 设置位置模式
    m.setPositionMode(device_id)
    
    # 3. 设置运动参数
    m.setAccTime(device_id, 1000)      # 加速时间1秒
    m.setTargetPosition(device_id, 10000)  # 目标位置
    
    # 4. 等待运动完成
    m.waitTargetPositionReached(device_id)
    
    # 5. 获取当前状态
    current_pos = m.getActualPosition(device_id)
    print(f"当前位置: {current_pos}")
    
finally:
    # 6. 断电并停止
    m.setPowerOff(device_id)
    m.stop()
```

### 🔍 **技术特点**

1. **底层通信**：基于共享内存和DMA缓冲区实现高效通信
2. **多轴支持**：支持最多32轴同时控制
3. **实时性**：通过独立线程处理通信，保证实时性
4. **插补功能**：支持多轴同步插补运动
5. **安全机制**：包含急停、限位、过流保护等安全功能

这个库是PyV3s控制器的核心运动控制库，为工业自动化应用提供了完整的电机控制解决方案。
        
## 参考示例
### 项目案例

## 相关视频
### 教程视频
- [pyv3s 控制器运行自定义轨迹](https://www.bilibili.com/video/BV1Re4de3Exe/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [如何使用板载 io 输出](https://www.bilibili.com/video/BV18oHkenEic/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [写一段代码 让电机运行起来](https://www.bilibili.com/video/BV12eH5eaEeC/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [修改一下代码 让两个电机跑起来](https://www.bilibili.com/video/BV12YH5eAE2V/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [如何连接两台电机](https://www.bilibili.com/video/BV1q1HgeBEcH/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [如何扫描和修改 ID](https://www.bilibili.com/video/BV1BkHge6Ev9/)
- [如何使用 winscp 工具进行上传和下载文件](https://www.bilibili.com/video/BV1hMsVeGEYU/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [如何使用 vscode 编写上传运行代码](https://www.bilibili.com/video/BV1kAsGedEMx/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)
- [如何使用以太网接口登录控制器](https://www.bilibili.com/video/BV11ds3ehEmq/)
- [如何使用 TTL 串口线登录 PyV3s 控制器](https://www.bilibili.com/video/BV1ZEsNeYEW2/?vd_source=1bf81de6c7b29ab112e8d99bca0303d8)