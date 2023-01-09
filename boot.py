import usb_cdc
import board
import storage
import rotaryio

knob = rotaryio.IncrementalEncoder(board.GP3, board.GP4)

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

knob = 1
for x in range(250):
    knob = encoder()

# Disable devices only if dah/dit is not pressed.
if knob is 1:
    print(f"boot: button not pressed, disabling drive")
    storage.disable_usb_drive()
    storage.remount("/", readonly=False)

    usb_cdc.enable(console=False, data=True)
else:
    print(f"boot: button pressed, enable console, enabling drive")

    usb_cdc.enable(console=True, data=True)

    new_name = "FumeEXT"
    storage.remount("/", readonly=False)
    m = storage.getmount("/")
    m.label = new_name
    storage.remount("/", readonly=True)