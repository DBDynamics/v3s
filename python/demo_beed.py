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