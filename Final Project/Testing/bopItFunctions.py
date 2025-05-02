from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import audiocore
import audiobusio

Hall = DigitalInOut(board.D16)
Hall.direction = Direction.INPUT
kit = MotorKit()

def get_voltage(pin): # Specify Analog Pin
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

def home_Motor():
    while Hall.value:
        #neoFun.set_ring_color((255,0,0)) Commented out in Implementation
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    #neoFun.set_ring_color((0,255,0)) Commented out in Implementation
    kit.stepper1.release()

def detect_Button(analog_read_function, thresholds=(1.0, 1.5, 2.0)): # (0,1,2)
    # ex. detect_Button(get_voltage(analog_in), (1.0, 1.5, 2.0))
    voltage = analog_read_function()
    button_pressed = None  # Initialize button_pressed to None

    if voltage >= thresholds[2]:
        button_pressed = 1
    elif thresholds[1] <= voltage < thresholds[2]:
        button_pressed = 2
    elif thresholds[0] <= voltage < thresholds[1]:
        button_pressed = 3

    return button_pressed

def detect_hall(Hall1, Hall2):
    if not Hall1.value:  # Hall sensors are often active-low
        return 4  # Hall sensor 1
    elif not Hall2.value:
        return 5  # Hall sensor 2
    return None

def read_input():
    button = detect_Button(get_voltage, (1.0, 1.5, 2.0)) # (0,1,2)
    if button is not None:
        return button
    hall = detect_hall(Hall1, Hall2)
    if hall is not None:
        return hall
    return None



def play_Wav(filename, i2s_tx=board.TX, i2s_clock=board.D10, i2s_word_select=board.D11):
    filename = filename + ".wav"
    try:
        f = open(filename, "rb")
        wav = audiocore.WaveFile(f)

        a = audiobusio.I2SOut(i2s_tx, i2s_clock, i2s_word_select)

        print("playing", filename)
        a.play(wav)
        while a.playing:
            pass # wait until the audio finishes playing
        print("stopped", filename)
        return True # success!
    except OSError as e:
        print(f"Error playing {filename}: {e}")
        return False # failure!
    finally:
        if 'f' in locals() and f is not None : # close the file
            f.close()
        if a is not None: # deinitialize the audio output.
            a.deinit()

def give_command():
    global last_hall_command
    while True:
        command_index = random.randint(0, len(commands) - 1)
        command = commands[command_index]

        if (command_index == 3 or command_index == 4) and command_index == last_hall_command:
            continue

        if command_index == 3 or command_index == 4:
            last_hall_command = command_index

        break

    play_Wav(command)

    return command_index + 1

def read_response(timeout):
    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        input_detected = read_input()
        if input_detected is not None:
            return input_detected
        time.sleep(0.01)
    return None

def play_game_over():
    play_Wav("game_over")
    kit.stepper1.release() # Release the motor
    neoFun.set_ring_color((255, 0, 0)) # Red color for game over
    time.sleep(1)
    neoFun.set_ring_color((0, 0, 0)) # Turn off the ring light
    time.sleep(1)
    neoFun.set_ring_color((255, 0, 0)) # Red color for game over
    time.sleep(1)
    neoFun.set_ring_color((0, 0, 0)) # Turn off the ring light
    time.sleep(1)
    neoFun.set_ring_color((255, 0, 0)) # Red color for game over
    time.sleep(1)
    neoFun.set_ring_color((0, 0, 0)) # Turn off the ring light
    time.sleep(1)

