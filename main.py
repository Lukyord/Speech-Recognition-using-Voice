import tensorflow as tf
import paho.mqtt.client as mqtt
import json
import pickle
import numpy as np
from helperFunctions import extract_mfcc, print_output
from pydub import AudioSegment
import os
import time
import base64
from io import BytesIO
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import requests

Topic="Alper"
consecutive_negative = 0
URL = "https://maker.ifttt.com/trigger/Alper/json/with/key/jWv1yPfAMG5UE2bB8W6Cuccibb7AraIMAxyxRh1MjGv"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Topic)

def on_message(client, userdata, msg):
    
    global consecutive_negative

    # ===== STEP: 1 =====
    # Recieve Voice Recording from MQTT Server
    try:
        sound_file = open('temp.wav', 'wb')
        sound_file.write(base64.b64decode(msg.payload.decode()))
        print('\n file saved \n')
        sound_file.close()

        # filename = 'temp.mp3'
        # format = filename[-3:]
        # if (format != 'wav'):
        #   audio_file = AudioSegment.from_file(filename, format=format)
        #   audio_file.export("output.wav", format='wav')
        #   print(f"\n Change file format and export as output.wav. \n")

        # # wait for file export before continue the code
        # while not os.path.exists("output.wav"):
        #   print('waiting')
        #   time.sleep(1)
    except:
        print("Error receiving and loading file")
        pass

    try:
     
      # ===== STEP: 2 =====
      # Load Model
      modelPrediction = tf.keras.models.load_model('model\model3E_mfcc40_rms_zcr_TRCS.h5')

      # ===== STEP: 3 =====
      # Extract Feature from voice recording
      mfcc = extract_mfcc("temp.wav") 
      # print(mfcc.shape)

      # ===== STEP: 4 =====
      # Predict mood, send result, and print the result
      prediction = modelPrediction.predict([mfcc])
      mood = print_output(prediction)
      print("\n================================================================================\n")
      print("Result in Vector Format: ", prediction)
      print("The mood dectected is: ", mood)
      print("\n================================================================================\n")

      # ===== STEP: 5 =====
      # count consecutive sadness
      if (print_output(prediction) == 'Negative'):
        consecutive_negative += 1
        if (consecutive_negative >= 2): 
           r = requests.get(url = URL)
      else:
        consecutive_negative = 0
      # ===== STEP: 6 =====
      # publishing data to MQTT server
      properties = Properties(PacketTypes.PUBLISH)
      properties.MessageExpiryInterval = 30 # in seconds

      outgoing_msg = {"mood": mood, "negative": str(prediction[0][0]), "neutral": str(prediction[0][1]), "positive": str(prediction[0][2]), "consecutive_negative": consecutive_negative}
      print(outgoing_msg)
      res = json.dumps(outgoing_msg)
      client.publish(Topic, res, 0, properties=properties)

    except Exception as e:
        print(e)
        pass
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("212.237.204.54", 1883, 60)
client.loop_forever()



