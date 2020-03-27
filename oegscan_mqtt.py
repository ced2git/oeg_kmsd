#!/usr/bin/env python3


oeg_dict = {

	39:"T2_Sensor",
	40:"T3_Sensor",
	41:"T4_Sensor",
	42:"T5_Sensor",
	47:"Planning_Bruleur",
	50:"T2_Limit",
	51:"T3_Limit",
	52:"T4_Limit",
	53:"T5_Limit",
	58:"Planning _Chaudiere",
	59:"TD_Retour"
	}

broker_address="192.168.0.101"
mqtt_clientname="oeg controller"

import minimalmodbus
import serial 
import csv
import time
import paho.mqtt.client as mqtt

from minimalmodbus import ModbusException
from minimalmodbus import NoResponseError 



instrument = minimalmodbus.Instrument('/dev/ttyACM0', 128, minimalmodbus.MODE_ASCII) # port name, slave address (in decimal)
instrument.serial.baudrate = 9600 # Baud
instrument.serial.parity = serial.PARITY_EVEN
instrument.serial.bytesize = 7
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.05	# seconds

client = mqtt.Client(mqtt_clientname)
client.connect(broker_address)

#localtime=time.asctime(time.localtime(time.time()))
#file=open('chaudiere.csv', 'a')
#writer= csv.writer(file)
for x in oeg_dict:
	try: 
		#print ("Register %d" %(x), instrument.read_register (x, 1,3))
		#print localtime
		mqtt_topic = "oeg/" + oeg_dict[x]
		#print mqtt_topic
		client.publish(mqtt_topic,instrument.read_register(x,1,3))
		#writer.writerow( (x, instrument.read_register (x,0,3),localtime))
	except NoResponseError:
		a=1

#print ("Register %d" %(x), "TimeOut")
#file.close()
