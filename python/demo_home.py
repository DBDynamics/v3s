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