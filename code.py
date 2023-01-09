import time
import board
import analogio
import rotaryio
import pwmio

sensLevel = analogio.AnalogIn(board.GP26)
fan = pwmio.PWMOut(board.GP25)
knob = rotaryio.IncrementalEncoder(board.GP3, board.GP4)

offset = 2

def sens_voltage():
    return (sensLevel.value / 65535 * sensLevel.reference_voltage)

def sens_pvoltage():
    while True:
        result = 0
        measurements = 500
        for x in range(measurements):
            voltage = sens_voltage()
            result = result + voltage

        result = result/measurements
        return int((round((result*100),0)))

def noctua(speed):
    if speed > 65535:
        speed = 65535
    fan.duty_cycle = speed

def encoder():
    global offset
    position = knob.position
    step = int(position)+offset
    if step < 1:
        step = 1
    step = 5000*step-5000
    if step > 65535:
        step = 65535
    return step


fantimer = 60
counter = 0
smoke = False
trigger = False
oldstep = 0
while True:
    sens = sens_pvoltage();
    if trigger is False and sens > 61:
        print("Trigger Fan Sensor: " + str(sens))
        offset = offset + 10
        smoke = True
        trigger = True
    else:
        counter = counter + 1
        smoke = False

    if smoke is False and trigger is True and counter > (fantimer * 1000):
        print("Disabling Fan Sensor: " + str(sens))
        offset = 2
        counter = 0
        trigger = False

    step = encoder()
    if oldstep is not step:
        print("Fan Speed: " + str(step))
        oldstep = step

    noctua(encoder())

    time.sleep(0.001)