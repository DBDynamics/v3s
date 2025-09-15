import socket
import struct
import time

NTP_SERVERS = [
    '202.112.29.82',      # 中国国家授时中心
    'ntp.aliyun.com',     # 阿里云
    'cn.pool.ntp.org',    # 中国NTP池
    'time.windows.com',   # 微软
    'pool.ntp.org',       # 全球NTP池
]


def request_time_from_ntp(addr):
    REF_TIME_1970 = 2208988800
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    try:
        client.sendto(data, (addr, 123))
        client.settimeout(2)
        data, address = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= REF_TIME_1970
            time.clock_settime(time.CLOCK_REALTIME, t + 8 * 60 * 60)
        return True
    except Exception as e:
        return False
    finally:
        client.close()


def sync_time():
    while True:
        for server in NTP_SERVERS:
            if request_time_from_ntp(server):
                print(f"Time sync success: {server}")
                return 0
        print("All NTP servers failed. Retrying in 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    sync_time()
