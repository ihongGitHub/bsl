# eMst: 64, eGw: 32,
class Frame:
    pidOrg = [1,1]; rxtxOrg = [64,1]; gidOrg = [2,2];
    pid = [1,1]; rxtx = [64,1]; sensor = [1,1]; micom = [1,1]; gid = [2,2];
    high = [100,1]; low = [1,1]; level = [50,1]; Type = [1,1]; rate = [1,1]
    status = [1,1]; dtime = [0x1234,2]
    cmd = [100,1]; sub = [1,1]; time = [1,2]
    dstPid = [1,1]; dstRxTx = [1,1]; dstGid = [1,2]; srcGid = [1,2]
    tbd0 = [1,2]; tbd1 = [1,2]; tbd2 = [1,2]; zone = [1,1]; CheckSum = [1,1]
    crc = [1,2]
    frameList = [ pidOrg, rxtxOrg, sensor, micom, gidOrg,
        high, low, level, Type, rate, status, dtime,
        cmd, sub, time,
        pid, rxtx, gid, srcGid, tbd0, tbd1, tbd2, zone, CheckSum, crc ]

    frame = ''
    byteList = []
    # input buffer clear
    clearBuffFlag = False
    newFrameFlag = False

    def getPid(self):
        return self.pid[0]
    def setPid(self, vaule):
        self.pid[0] = vaule

    def getRxTx(self):
        return self.rxtx[0]
    def setRxTx(self, vaule):
        self.rxtx[0] = vaule

    def getGid(self):
        return self.gid[0]
    def setGid(self, vaule):
        self.gid[0] = vaule

    def getHigh(self):
        return self.high[0]
    def setHigh(self, vaule):
        self.high[0] = vaule

    def getLow(self):
        return self.low[0]
    def setLow(self, vaule):
        self.low[0] = vaule

    def getLevel(self):
        return self.level[0]
    def setLevel(self, vaule):
        self.level[0] = vaule

    def getCmd(self):
        return self.cmd[0]
    def setCmd(self, vaule):
        self.cmd[0] = vaule

    def getSub(self):
        return self.sub[0]
    def setSub(self, vaule):
        self.sub[0] = vaule

    def getFrame(self):
        return self.frame

    def setCrcFrame(self):
        tempList = []

        for numList in self.frameList:
            if(numList[1]==2):
                tempList.append(numList[0]%256)
                tempList.append(int(numList[0]/256))
            else:
                tempList.append(numList[0])
        tempList = tempList[0:(len(tempList)-2)]
        crcIn = bytearray(tempList)
        crcResult = self.getCrc(crcIn)
        self.crc[0] = crcResult

    def setFrame(self):
        self.setCrcFrame()
        self.frame = '{'
        for numList in self.frameList:
            if(numList[1]==2):
                self.frame += '%02x' % (numList[0]%256)
                self.frame += '%02x' % int(numList[0]/256)
            else:
                self.frame += '%02x' % numList[0]
        self.frame += '}'
        with open('outHex.txt','w') as fp:
            print(self.frame, file = fp)
        print(self.frame)

    def getClearBuff(self):
        return self.clearBuff

    def getCrc(self, data):
        from crc import CRC
        crc16 = CRC()
        return crc16.update(data)

    def getNewFrameFlag(self):
        return self.newFrameFlag

    def clearNewFrameFalg(self):
        self.newFrameFlag

    def parseFrame(self, inFrame):
        first = inFrame.rfind('{')
        last = inFrame.rfind('}')
        if last > 70:
            self.clearBuffFlag = True
        else:
            self.clearBuffFlag = False

        if (last - first -1) == 68:
            self.clearBuffFlag = True
            result = inFrame[(first+1):last]

            count = 0
            temp = list(); self.byteList;
            for s in range(1,35):
                ss = result[count:count+2]
                temp.append(int(ss,16))
                self.byteList.append(int(ss,16))
                count += 2

            print(self.byteList)
            temp = temp[0:(len(temp)-2)]
            print(self.byteList)
            crcIn = bytearray(temp)
            crcResult = self.getCrc(crcIn)
            print(temp)

            count = 0
            for i in self.frameList:
                if i[1] == 2:
                    i[0] = self.byteList[count]
                    count += 1
                    i[0] += self.byteList[count]*256
                else:
                    i[0] = self.byteList[count]
                count += 1

            if crcResult == self.crc[0]:
                print('Crc check Ok')
                newFrameFlag = True
                self.setFrame()
            else:
                print('Crc error')
            return True

        else:
            print('Fail Parse')
            return False

    def testFrame(self):
        print('----------- testFrame --------------')
        strTest = '{000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1fc36a}1234'
        # strTest = '{01010101123464013201010100010101000101010001000100010001000101010001}1234'
        print(strTest.find('}'))
        self.parseFrame(strTest)
        if self.getClearBuff():
            print('clear input buff')
            strTest = ''


if __name__ == '__main__':
    frame = Frame()
    myFrame = frame.getFrame()

    frame.setFrame()
    a = frame.getFrame()
    aa = bytearray(a, 'ascii')
    print(aa)

    # str_List = '{'
    # for numList in myFrame:
    #     if(numList[1]==2):
    #         str_List += '%04x' % numList[0]
    #     else:
    #         str_List += '%02x' % numList[0]
    # str_List += '}'
    # print(str_List)
    #
    # frame.testFrame()



# with open("dict.txt","w") as f:
#     print(str_List, file = f)
#
# import crc16
# print(crc16.crc16xmodem(b'123456789'))
# import numpy as np
#
# def crc16(data: bytes):
#     '''
#     CRC-16-CCITT Algorithm
#     '''
#     data = bytearray(data)
#     poly = 0x8408
#     crc = 0xFFFF
#     for b in data:
#         cur_byte = 0xFF & b
#         for _ in range(0, 8):
#             if (crc & 0x0001) ^ (cur_byte & 0x0001):
#                 crc = (crc >> 1) ^ poly
#             else:
#                 crc >>= 1
#
#             cur_byte >>= 1
#
#     crc = (~crc & 0xFFFF)
#     crc = (crc << 8) | ((crc >> 8) & 0xFF)
#
#     return np.uint16(crc)
#
# values = [0x81, 0x12, 0xC0, 0x00, 0x01, 0x05]
# string = "".join(chr(i) for i in values)
# print (crc16(string))
