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