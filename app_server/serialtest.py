#-*- coding: utf-8 -*-
import serial

ser = serial.Serial(port = 'COM7', baudrate = 9600)

class Arduino_master:
    def __init__(self, tcpServer):
        self.andRaspTCP = tcpServer

    def getdht(self):
        #if command == "10\n":
        sensor = [] #**************마지막에 센서 배열 초기화하면 오류나도 다시 가능!!!!!!!********************
        for i in range(16):
            try: #디코딩 실패(예외) 시 except로 넘어가기
                sensor.append(ser.read().decode('utf-8'))
            except:
                pass
                #sensor.clear()#배열 비우기
        print(sensor)
        if sensor[0] == '1' or sensor[0] == '2' or sensor[0] == '3':
            temp = sensor[0:4]
            humi = sensor[4:8]
            dust = sensor[8:14]
            state = sensor[14:]
            #while len(sensor) > 0: sensor.pop() # 배열 비우기
            #sensor.clear()
            send_temp = ''.join(temp)
            send_humi = ''.join(humi)
            send_dust = ''.join(dust)
            send_state = ''.join(state);
            self.andRaspTCP.sendAll(send_temp + send_humi + send_dust + send_state + '\n')
            print("전송 완료")

        else:
            print("전송 실패")
            #sensor.clear()  # 배열 비우기

    def realtimedht(self):
        while True:
            self.getdht()

    def server_sensor(self, command):
        # 서버에서 받아온 값 사용
        # cctv off, on= 100,101
        if command == "100\n":
            pass