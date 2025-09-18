from libpro import Bee
import time
import sys

def change_device_id(current_id, new_id):
    """修改设备ID"""
    # 初始化Bee对象
    m = Bee()
    
    try:
        print(f"正在将设备ID从 {current_id} 修改为 {new_id}...")
        # 修改设备ID
        m.changeID(current_id, new_id)
        time.sleep(1)
        print(f"设备ID修改成功：{current_id} -> {new_id}")
    except Exception as e:
        print(f"修改失败：{e}")
    finally:
        # 停止操作
        m.stop()

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 3:
        print("使用方法: python3 changeID.py <当前ID> <新ID>")
        print("示例: python3 changeID.py 0 2")
        sys.exit(1)
    
    try:
        current_id = int(sys.argv[1])
        new_id = int(sys.argv[2])
        
        # 验证ID范围（假设有效范围是0-63
        if not (0 <= current_id <= 63) or not (0 <= new_id <= 63):
            print("错误：ID必须在0-63")
            sys.exit(1)
            
        change_device_id(current_id, new_id)
        
    except ValueError:
        print("错误：ID必须是数字")
        sys.exit(1)