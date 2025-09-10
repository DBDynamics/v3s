from libpro import Bee
import time
from libusb485lite import USB485Pro

m = Bee()


mid_motor_left = 1
mid_motor_right = 2
# m.setPowerOn(mid)
# m.setOutputIO(mid, 0)
m.setPWMMode(mid_motor_left)
m.setPWMMode(mid_motor_right)
sensor = USB485Pro()
mid_speed = 1
mid_direction = 0
machine_state = 0
speed_limit = 900
direction_limit = 51200/4/4
# for loop in range(0, 1000):
while True:
    time.sleep(0.01)
    io_state = m.getInputIO(1)
    if io_state == 1:
        enc_speed0 = sensor.getEncoderValue(mid_speed)
        enc_direction0 = sensor.getEncoderValue(mid_direction)
        while io_state == 1:
            time.sleep(0.02)
            enc_speed = sensor.getEncoderValue(mid_speed) - enc_speed0
            enc_direction = sensor.getEncoderValue(mid_direction) - enc_direction0

            if enc_direction > direction_limit:
                enc_direction = direction_limit
            if enc_direction < -direction_limit:
                enc_direction = -direction_limit


            speed_factor = 12
            motor_pwm_left = (-enc_speed / speed_factor) + (enc_direction / 40)
            motor_pwm_right = (-enc_speed / speed_factor) - (enc_direction / 40)
            if motor_pwm_left > speed_limit:
                motor_pwm_left = speed_limit
            if speed_limit < -speed_limit:
                motor_pwm_left = -speed_limit
            if motor_pwm_right > speed_limit:
                motor_pwm_right = speed_limit
            if motor_pwm_right < -speed_limit:
                motor_pwm_right = -speed_limit   
            m.setTargetVelocity(mid_motor_left, -int(motor_pwm_left))
            m.setTargetVelocity(mid_motor_right, int(motor_pwm_right))
            io_state = m.getInputIO(1)
        # print(motor_pwm)
    else:
        m.setTargetVelocity(mid_motor_left, -int(0))
        m.setTargetVelocity(mid_motor_right, int(0))

m.setTargetVelocity(mid_motor_left, -int(0))
m.setTargetVelocity(mid_motor_right, int(0))
time.sleep(1)
m.stop()
sensor.stop()