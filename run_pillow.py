import serial, string, os
import RPi.GPIO as GPIO
import time
import multiprocessing

threads = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

motor_map = {'1': 0.1,
        '2': 0.2,
        '3': 0.3,
        '4': 0.4}

def motor_start(mode):
  for _ in range(5):
    GPIO.output(18, True)
    time.sleep(mode)
    GPIO.output(18, False)
    time.sleep(mode)

def audio_start(setting):
  print('starting audio:' + str(setting))
  volume = audio_map[setting][1]
  audio = audio_map[setting][0]  
  os.system ('omxplayer -o local --vol ' + str(volume) + ' ' + audio)

def aroma_start():
  GPIO.output(17, True)
  time.sleep(10)
  GPIO.output(17, False)

audio_map = {'1': ['jacobs_siri.mp3', -1200],
        '2': ['relaxation.mp3', -1200],
        '3': ['whitenoise.mp3', -1800],
        '4': ['jacobs_serena.mp3', -1200]}

def run_pillow(setting):
  print('starting setting: ' + str(setting))
  motor_setting = motor_map[setting]
  motor_start(motor_setting)
  audio_start(setting)
  aroma_start()

def kill_threads():
  print('killing threads')
  global threads
  for thread in threads:
    thread.terminate()
  threads = []

output = ' '
ser = serial.Serial('/dev/ttyACM0', 4800, timeout=1)

while True:
  while output != '':
    output = ser.readline()
    try:
      run_pillow(output)
    except KeyError:
      pass
  output = ' '



