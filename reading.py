import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

#Constants
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

#Initialize serial connection
ser = serial.Serial(SERIAL_PORT,BAUD_RATE, timeout=60)

#Initialize empty lists to store data
sensorData = {
    'time':[],
    'soil':[],
    'temp':[],
    'prox':[],
    'noise':[]
}
data_clear = 1
#some user counter
user = 0

#Func to read and process Arduino data
def read_arduino():
    global user, data_clear

    line = ser.readline().decode('utf-8').strip()
    sensorValues = line.split(', ')
    sw = int(sensorValues[0])

    if (sw==0 and data_clear == 0):
        #if the circuit is closed and we didn't clear the data, write data, change user, and clear data
        write_file()
        user+=1
        for key in sensorData:
            sensorData[key] = []
        data_clear = 1
        
    elif (sw == 1):
        #if circuit is open, get the data, mark the data as not clear
        data_clear = 0
        sensorData['time'].append(float(sensorValues[1]))
        sensorData['temp'].append(float(sensorValues[2]))
        sensorData['soil'].append(int(sensorValues[3]))
        sensorData['prox'].append(float(sensorValues[4]))
        sensorData['noise'].append(int(sensorValues[5]))
        #Print received values:
        print(f'Time: {sensorValues[1]}, Temp: {sensorValues[2]}, Soil:{sensorValues[3]}, Proximity:{sensorValues[4]} cm, Noise:{sensorValues[5]}')
    else:
        #in case the circuit is closed but we already cleared the data, we ar ejust waiting
        print("Waiting to start...")

    

#Func to update plot
def update_plot(frame):
    read_arduino()
    plt.cla()
    plt.plot(sensorData['time'],sensorData['temp'], label="temperature")
    plt.plot(sensorData['time'],sensorData['soil'], label="soil")
    plt.plot(sensorData['time'], sensorData['prox'], label="proximity")
    plt.plot(sensorData['time'],sensorData['noise'], label="noise")
    plt.xlabel('Time')
    plt.ylabel("Sensor Values")
    plt.legend()

#Funct to save data to csv
def on_close(event):
    with open('arduino_data_' + str(user) + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time','Soil data'])
        for t,temp,s,p,n in zip(sensorData['time'],sensorData['temp'],sensorData['soil'],sensorData['prox'],sensorData['noise']):
            writer.writerow([t,temp,s,p,n])

def write_file():
    print("Writing file for user "+ str(user)+"...",end='')
    with open('arduino_data_' + str(user) + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time','Soil data'])
        for t,temp,s,p,n in zip(sensorData['time'],sensorData['temp'],sensorData['soil'],sensorData['prox'],sensorData['noise']):
            writer.writerow([t,temp,s,p,n])
    print('Success!')

#Register callback when plot windows is closed
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

#only works for circuit is on
#ani = FuncAnimation(fig, update_plot, interval = 1000, cache_frame_data=False)
#plt.show()

#try this for continuous data
while (True):
    read_arduino()
