import time
import board
import analogio
import rotaryio
import pwmio

sensLevel = analogio.AnalogIn(board.GP26)
fan = pwmio.PWMOut(board.GP25)
knob = rotaryio.IncrementalEncoder(board.GP3, board.GP4)

offset = 2
measurements = 750
sensortrigger = 67
maxspeed = 40000
fantimer = 1 # Minutes

def sens_voltage():
    return (sensLevel.value / 65536 * sensLevel.reference_voltage)

def sens_pvoltage():
    global measurements
    while True:
        result = 0
        for x in range(measurements):
            voltage = sens_voltage()
            result = result + voltage

        result = result/measurements
        return int((round((result*100),0)))

def noctua(speed):
    if speed > maxspeed:
        speed = maxspeed
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


counter = 0
smoke = False
trigger = False
oldstep = 0
oldsens = 0
while True:
    sens = sens_pvoltage();

    if sens is not oldsens:
        oldsens = sens
        print("Sensor Value: " + str(sens))

    if trigger is False and sens > 64:
        print("Trigger Fan Sensor: " + str(sens))
        offset = offset + 10
        smoke = True
        trigger = True
    else:
        counter = counter + 1
        smoke = False

    if smoke is False and trigger is True and counter > ((fantimer*60) * (1000-measurements)):
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