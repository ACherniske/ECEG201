import os
import board
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import random
from digitalio import DigitalInOut, Direction, Pull
import analogio
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import audiocore
import audiobusio
import BopItFunc
import wifiFunctions as WifiFunc
import neoPixelFunctions as NeoFunc

ACTION_MAP = {
    0: "NONE",
    1: "BOP",
    2: "PULL",
    3: "FLICK",
    4: "TWIST",  # hall_1
    5: "TWIST"   # hall_2
}

internet = WifiFunc.wifiObject()
THINGSPEAK_CHANNEL = '2945278'
THINGSPEAK_API_KEY = '4NDZLK80SP9ORQ21'
kit = MotorKit()
seed = None
seed_i = 0
num = None
max_index = 0
idle = True
last_input_time = 0
bops = 0
pulls = 0
flicks = 0
twists = 0
spins = 0


def get_voltage(pin): # Specify Analog Pin
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

def detect_Button(analog_read_function, thresholds=(.2, .7, 1.2)): # (0,1,2)
    # ex. detect_Button(get_voltage(analog_in), (1.0, 1.5, 2.0))
    voltage = analog_read_function
    button_pressed = 0  # Initialize button_pressed to None

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
    elif Hall2.value:
        return 5  # Hall sensor 2
    return 0

def wait_for_input(button, Hall1, Hall2):
    while True:
        button_value = detect_Button(get_voltage(button), (.2, .7, 1.2))
        hall_value = detect_hall(Hall1, Hall2)
        if button_value != 0:
            return button_value
        elif hall_value !=0:
            return hall_value
        time.sleep(0.1)

def home_Motor(Hall):
    while Hall.value:
        #neoFun.set_ring_color((255,0,0)) Commented out in Implementation
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    #neoFun.set_ring_color((0,255,0)) Commented out in Implementation
    kit.stepper1.release()

def play_Wav(filename, i2s_tx=board.TX, i2s_clock=board.D10, i2s_word_select=board.D11):
    filename = filename + ".wav"
    a = None
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

def idle_state(button, Hall1, Hall2):
    print("Entering idle state...")
    last_sound_time = time.monotonic()
    global seed_i, seed, max_index
    #print(seed_i, max_index)
    home_Motor(Hall2)
    while True:
        NeoFunc.animate_snake((255,0,0),2,0,24)

        button_value = detect_Button(get_voltage(button), (0.2, 0.7, 1.2))
        hall_value = detect_hall(Hall1, Hall2)
        #print(button_value, hall_value)
        #print(get_voltage(button), hall_value)

        # Play idle sound every 30 seconds
        current_time = time.monotonic()
        # print(current_time, last_sound_time)
        if current_time - last_sound_time >= 60:
            print("Playing idle sound...")
            play_Wav("idle")  # Play the idle sound
            play_Wav("idle")  # Play the idle sound
            play_Wav("idle")  # Play the idle sound
            last_sound_time = current_time  # Reset the timer
        
        # Check for button input to start a game
        if button_value != 0:
            # Ensure we have a valid seed
            if seed is None or max_index is None:
                seed, max_index = generate_seed()
                seed_i = 0  # Reset seed index
            if seed_i >= max_index:
                print("Seed exhausted, generating new seed...")
                seed = None
                seed, max_index = generate_seed()
                seed_i = 0
            play_Wav("Game_Start")
            play_game(button, Hall1, Hall2, seed, max_index)
            return  # If play_game returns, we'll re-enter idle state
        
        time.sleep(0.1)  # Small delay to avoid busy-waiting

def wifiTest():
    print("ESP32-S3 WebClient Test")

    print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

    print("Available WiFi networks:")
    for network in wifi.radio.start_scanning_networks():
        print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                             network.rssi, network.channel))
    wifi.radio.stop_scanning_networks()

    print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
    print(f"My IP address: {wifi.radio.ipv4_address}")

    ping_ip = ipaddress.IPv4Address("8.8.8.8")
    ping = wifi.radio.ping(ip=ping_ip)

    # retry once if timed out
    if ping is None:
        ping = wifi.radio.ping(ip=ping_ip)

    if ping is None:
        print("Couldn't ping 'google.com' successfully")
    else:
        # convert s to ms
        print(f"Pinging 'google.com' took: {ping * 1000} ms")

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    return pool, requests

def generate_seed():
    try :
        response = internet.api_get("http://www.randomnumberapi.com/api/v1.0/random?min=1&max=5&count=100")
    except adafruit_requests.OutOfRetries as e:
        print(f"Error fetching random seed: {e}")
        response = [random.randint(1, 5) for _ in range(100)]
    
    seed = list(response.text.replace(",","").replace("[","").replace("]","").replace("\n",""))
    seed = [v for i, v in enumerate(seed) if i == 0 or v != seed[i-1] or v not in ["4", "5"]]
    max_index = len(seed)
    #print(seed)
    return seed, max_index

def get_random_action(seed):
        global num, seed_i
        num = int(seed[seed_i])
        seed_i += 1
        return ACTION_MAP[num]
    
def play_game(button, Hall1, Hall2, seed, max_index):
    global seed_i
    global last_input_time
    input_received = 0
    bops = 0
    pulls = 0
    flicks = 0
    twists = 0
    spins = 0
    
    print("Starting game...")
    time.sleep(1)
    
    # Initialize game parameters
    score = 0
    
    # Reset the last input time when starting a game
    last_input_time = time.monotonic()
    
    while True:
        input_received = 0
        home_Motor(Hall2)
        time.sleep(1)
        NeoFunc.set_ring_color((255,255,255))    
        action = get_random_action(seed)
        print(f"{action} IT!")
        play_Wav(f"{action}_C")

        while input_received == 0 and time.monotonic() - last_input_time < 3:
            input_received = wait_for_input(button, Hall1, Hall2)
            if input_received != 0:
                print(f"Input received: {input_received}")
        if ACTION_MAP[input_received] == action:
            NeoFunc.set_ring_color((0,255,0))
            print("Correct!")
            score += 1
            if action == "BOP":
                bops += 1
            elif action == "PULL":
                pulls += 1
            elif action == "FLICK":
                flicks += 1
            elif action == "TWIST":
                twists += 1
            elif action == "SPIN":
                spins += 1
            play_Wav(f"{action}_R")
            last_input_time = time.monotonic()  # Reset the last input time
            input_received = 0  # Reset input_received for the next round
            
        else:
            NeoFunc.set_ring_color((255,0,0))
            print(f"Incorrect! You Did {ACTION_MAP[input_received]} instead of {action}")
            play_Wav("LOSE_C")
            time.sleep(0.1)
            play_Wav("LOSE_R2")
            break
            
        time.sleep(1)
    print(f"Your score: {score}")
    print(f"Bops: {bops}, Pulls: {pulls}, Flicks: {flicks}, Twists: {twists}, Spins: {spins}")
    request_msg = "https://api.thingspeak.com/update?api_key={}&field{}={}&field{}={}&field{}={}&field{}={}&field{}={}&field{}={}".format(THINGSPEAK_API_KEY,'1',bops,'2',pulls,'3',flicks,'4',twists,'5',spins,'6',score)
    internet.api_get(request_msg)
    
    # After game ends, return to idle state
    print("Game over! Returning to idle state...")
    idle_state(button, Hall1, Hall2)
