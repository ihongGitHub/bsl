import serial
import time
from threading import Thread, Lock

# ser = serial.Serial('/dev/cu.SLAB_USBtoUART',115200,timeout=0)
# ser = serial.Serial('/dev/ttyUSB0',115200,timeout=0)
# ser = serial.Serial('/dev/ttyAMA0',115200,timeout=0)
# serialName = 'COM62'
# ser = serial.Serial(serialName, 115200, timeout=0)
# print('serial port is {}'.format(ser.portstr))
class serThread(Thread):
    serFirstFlag = True
    serAlive = False
    writeFlag = False
    readFlag = False
    readStr = ''
    writeStr = ''

    def __init__(self):
        print('Now Start SerialThread')
        Thread.__init__(self)

    def send(self, writeStr):
        self.writeStr = writeStr
        self.writeFlag = True

    def getReadFlag(self):
        return self.readFlag

    def clearReadFlag(self):
        self.readFlag = False

    def getReadStr(self):
        return self.readStr

    def clearWriteFlag(self):
        self.writeFlag = False

    def getWriteFlag(self):
        return self.writeFlag

    def getWriteStr(self):
        return self.writeStr

    def getSerAlive(self):
        return self.serAlive

    def run(self):
        with serial.Serial('COM62', 115200, timeout = 0) as ser:
            self.serDevice = ser
            self.serAlive = True
            count = 0
            while True:
                try:
                    self.readStr=str(ser.readline(),'utf-8')
                    if self.readStr != '':
                        self.readFlag = True
                except:
                    print('Error Data')

                if self.readFlag:
                    print(self.readStr)
                    self.readFlag = False
                    if self.readStr.find('Quit Serial') != -1:
                        break

                if self.writeFlag:
                    # print('writeFlag')
                    ser.write(bytearray(self.writeStr,'ascii'))
                    self.writeFlag = False

                count += 1
                # time.sleep(0.001)
                # # self.send('count:{}'.format(count))
                # if count > 20000:
                #     break
        self.serAlive = False
        self.serFirstFlag = True
        print('End of inThread')


class readThread(Thread):
    readFlag = False
    readStr = ''
    def __init__(self):
        print('Now Start readThread')
        Thread.__init__(self)

    def run(self):
        global ser
        while True:
            try:
                self.readStr=str(ser.readline(),'utf-8')
            except:
                print('Error Data')
            if self.readStr != '':
                strFind = self.readStr.find('QuitSerial')
                if strFind != -1:
                    print('strFind:{}'.format(strFind))
                    break
                self.readFlag = True
                print(self.readStr)
        print('End of inThread')

    def getReadFlag(self):
        return self.readFlag

    def clearReadFlag(self):
        self.readFlag = False

    def getReadStr(self):
        return self.readStr

class writeSer():
    writeStr = ''
    writeFlag = False
    # global ser

    def send(self, writeStr):
        self.writeStr = writeStr
        ser.write(bytearray(self.writeStr,'ascii'))
        self.writeFlag = True

    def clearWriteFlag(self):
        self.writeFlag = False

    def getWriteFlag(self):
        return self.writeFlag

    def getWriteStr(self):
        return self.writeStr

class testThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        outSer = writeSer()
        inSer = readThread()
        inSer.start()

        count=5
        while count:
            count -= 1
            testStr = 'Count = {}\r'.format(count)
            outSer.send(testStr)
            time.sleep(0.5)
            if inSer.getReadFlag():
                print('testSer.getReadFlag')
                inSer.clearReadFlag()
        outSer.send('QuitSerial')
        print('End of testThread')

if __name__ == "__main__":
    # setInSer()

    testSer = testThread()
    testSer.start()
