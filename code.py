import time
import board
import analogio
import digitalio
import rotaryio
import pwmio

fan = pwmio.PWMOut(board.GP25)
knob = rotaryio.IncrementalEncoder(board.GP3, board.GP4)

cBtn = digitalio.DigitalInOut(board.GP11)
cBtn.direction = digitalio.Direction.INPUT
cBtn.pull = digitalio.Pull.UP

redLED = digitalio.DigitalInOut(board.GP12)
redLED.direction = digitalio.Direction.OUTPUT
redLED.value = True

greenLED = digitalio.DigitalInOut(board.GP13)
greenLED.direction = digitalio.Direction.OUTPUT
greenLED.value = True

blueLED = digitalio.DigitalInOut(board.GP14)
blueLED.direction = digitalio.Direction.OUTPUT
blueLED.value = True

offset = 10

def noctua(speed):
    if speed > 65535:
        speed = 65535
    fan.duty_cycle = speed

def encoder():
    global offset
    position = knob.position
    step = int(position)+offset
    if step < 1:
        offset = offset + 1
        step = 1
    step = 5000*step-5000
    if step > 70000:
        offset = offset - 1
    return step

step = 0
oldstep = 0
toggle = False
count = 0

while True:
    step = encoder()
    if oldstep is not step:
        print("Fan Speed: " + str(step))
        oldstep = step

    if toggle is False:
        redLED.value = True
        greenLED.value = False
        blueLED.value = True
        noctua(0)
    else:
        greenLED.value = True
        if count < 300:
            redLED.value = False
            blueLED.value = True
        if count > 300:
            redLED.value = True
            blueLED.value = False
        if count > 600:
            count = 1
        count = count+1
        noctua(encoder())

    if cBtn.value is True:
        if toggle is False:
            print("pushed on")
            if encoder() is 0:
                offset = offset+10
            toggle = True
        elif toggle is True:
            print("pushed off")
            toggle = False
        time.sleep(0.4)
    
    time.sleep(0.001)