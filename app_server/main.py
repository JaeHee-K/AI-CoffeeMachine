import tcpServer
from multiprocessing import Queue
import time
#import serial
import dbModule
from datetime import date, datetime

# make public queue
commandQueue = Queue()

# init Arduino
#ser = serial.Serial(port = 'COM7', baudrate = 9600)

# init module
andRaspTCP = tcpServer.TCPServer(commandQueue,"172.30.1.44", 8888)
andRaspTCP.start()
print("서버 연결 중")

# set module to executer
#commandArduino = serialtest.Arduino_master(andRaspTCP)

coffee_out = [0 for i in range(7)]
coffee_out_count = 0

# Coffee output chart test
coffee_out[0] = 2
coffee_out[1] = 5
coffee_out[2] = 1
#coffee_out[3] = 0
coffee_out[4] = 2
coffee_out[5] = 6
coffee_out[6] = 4

timedata = [0 for i in range(2)]
timecount = 0

# set MySQL module
db_class = dbModule.Database()

while True:
    try:
        # Current Time get
        # now.hour, now.minute, now.year, now.month, now.day
        # date(2020, 9, 3).weekday()
        now = datetime.now()
        date_count = date(now.year, now.month, now.day).weekday()

        # Coffee output count reset
        if date_count == 6 and now.hour == 23 and now.minute == 59:
            for i in range(7):
                coffee_out[i] = 0

        command = commandQueue.get(True,1)

        # Coffee reservation (with continue exception)
        if command[0] == "@":
            timedata = command[1:].split('#')
            timecount = 1
            continue

        # Coffee type
        if command[0] == "1":
            coffee_out[date_count] += 1
            es = int(command[3]) + 5
            target = 2
            sql = "INSERT INTO ISIADB.coffee(density, target) \
                   VALUES('%d', '%d')" % (es, target)
            db_class.execute(sql)
            db_class.commit()
        elif command[0] == "2":
            coffee_out[date_count] += 1
            es = int(command[3])
            target = 1
            sql = "INSERT INTO ISIADB.coffee(density, target) \
                   VALUES('%d', '%d')" % (es, target)
            db_class.execute(sql)
            db_class.commit()

        # Coffee temp
        """if command[1] == "0":
            ser.write('a'.encode())
        elif command[1] == "1":
            ser.write('b'.encode())
        elif command[1] == "2":
            ser.write('c'.encode())

        # Coffee grind
        if command[2] == "0":
            ser.write('d'.encode())
        elif command[2] == "1":
            ser.write('e'.encode())
        elif command[2] == "2":
            ser.write('f'.encode())

        # Coffee thick
        # espresso
        if command[0] == "1":
            if command[3] == "1":
                ser.write('6'.encode())
            elif command[3] == "2":
                ser.write('7'.encode())
            elif command[3] == "3":
                ser.write('8'.encode())
            elif command[3] == "4":
                ser.write('9'.encode())
            elif command[3] == "5":
                ser.write('0'.encode())
        # americano
        if command[0] == "2":
            if command[3] == "1":
                ser.write('1'.encode())
            elif command[3] == "2":
                ser.write('2'.encode())
            elif command[3] == "3":
                ser.write('3'.encode())
            elif command[3] == "4":
                ser.write('4'.encode())
            elif command[3] == "5":
                ser.write('5'.encode())"""

    except:
        # Coffee reservation
        if int(timedata[0]) == int(now.hour) and int(timedata[1]) == int(now.minute) and timecount == 1:
            print("커피 추출!")
            timecount = 0

        sql = "SELECT centroid_1, centroid_2 \
               FROM ISIADB.centroid"
        row = db_class.CustomexecuteOne(sql)
        centroid_1 = int(row['centroid_1'])
        centroid_2 = int(row['centroid_2'])
        send_data = str(centroid_1) + str(centroid_2) + str(coffee_out[0]) + str(coffee_out[1]) + str(coffee_out[2]) + str(coffee_out[3]) + str(coffee_out[4]) + str(coffee_out[5]) + str(coffee_out[6]) +'\n'
        #print(send_data)
        andRaspTCP.sendAll(send_data)
