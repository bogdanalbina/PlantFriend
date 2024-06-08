import serial

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
    'touch':[],
    'electric':[],
    'volt':[],
    'noise':[]
}
data_clear = 1

#Func to read and process Arduino data
def read_arduino():
    global data_clear

    line = ser.readline().decode('utf-8').strip()
    sensorValues = line.split('; ')
    sw = int(sensorValues[0])

    if (sw==0 and data_clear == 0):
        #if the circuit is closed and we didn't clear the data, write data, change user, and clear data
        clear_file()
        for key in sensorData:
            sensorData[key] = []
        data_clear = 1
        
    elif (sw == 1):
        #if circuit is open, get the data, mark the data as not clear
        data_clear = 0
        time = float(sensorValues[1])
        temp = float(sensorValues[2])
        soil = int(sensorValues[3])
        prox = float(sensorValues[4])
        touch = int(sensorValues[5])
        elec = sensorValues[6].split(",")
        volt = int(sensorValues[7])
        noise = int(sensorValues[8])
        sensorData['time'].append(time)
        sensorData['temp'].append(temp)
        sensorData['soil'].append(soil)
        sensorData['prox'].append(prox)
        sensorData['touch'].append(touch)
        sensorData['electric'].append(elec)
        sensorData['volt'].append(volt)
        sensorData['noise'].append(noise)
        #Print received values:
        #print(f'Time: {sensorValues[1]}, Temp: {sensorValues[2]}, Soil:{sensorValues[3]}, Proximity:{sensorValues[4]} cm, Touch: {int(sensorValues[5])}, Noise:{sensorValues[6]}')
        with open("recordings.txt", "a") as fp:
            fp.write(f'Time: {int(time/2000)}, Temperature: {temp}, Soil Moisture:{soil}, Proximity:{prox} cm, Touch: {touch}, Electric Signal: {elec}, Voltage:{volt}, Noise:{noise}\n')
    else:
        #in case the circuit is closed but we already cleared the data, we ar ejust waiting
        #print("Waiting to start...")
        clear_file()

def clear_file():
    with open("recordings.txt", "w") as fp:
        fp.write("0 Waiting to start...\n")

#try this for continuous data
print ("Running",end='')
while (True):
    for i in range(10):
        try:
            print(".",end='')
            read_arduino()
        except ValueError:
            print("e",end='')
            continue