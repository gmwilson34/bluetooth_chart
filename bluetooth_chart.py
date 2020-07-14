import matplotlib.pyplot as plt
import time
import sys
import argparse
import subprocess
import matplotlib.animation as animation

mac_address = input("Mac_Address: ")
#repeatedly returns the RSSI value of a given device
#you will need to install btmgmt. you can do this by running sudo apt install btmgmt
#this program is linux-only, run it from your raspberry pi.

def rssi_vals(addr):

    #run the btmgmt find command and return the line containing the address specified
    try:
        p = subprocess.Popen('sudo btmgmt find | grep {}'.format(addr), stdout=subprocess.PIPE, shell=True)
        a, b = p.communicate()
        info = str(a)
        #cut out the RSSI value only and return it as an integer
        start = info.index("rssi") + 5
        end = info.index("flags") - 1
        rssi_str = info[start:end]
        reading = int(rssi_str)
        chart_data = open("chart_data","a")
        chart_data.write(f"{reading}")
        return reading

    except ValueError:
        print('Could not find the specified device. Did you enter the correct address? Trying again...')
        time.sleep(1)
def tx_power(addr):
    #find the tx power of the Pi
    p = subprocess.Popen('hcitool tpl {} 0'.format(addr), stdout=subprocess.PIPE, shell=True)
    a, b = p.communicate()
    info = str(a)
    #start = info.index(': ') + 1
    power_str = info[2:-3]
    #reading = int(power_str)
    return power_str

ground_station_addr = f"{mac_address}" #replace with bluetooth address of your computer

while True:
    print('RSSI: ' + str(rssi_vals(ground_station_addr)))
    print(str(tx_power(ground_station_addr)))


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
def animate(i):
    pullData = open("chart_data","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
