class Frame:
    pid = [1,1]; rxtx = [1,1]; sensor = [1,1]; micom = [1,1]; gid = [1,2];
    high = [100,1]; low = [1,1]; level = [50,1]; Type = [1,1]; rate = [1,1]
    status = [1,1]; dtime = [1,2]
    cmd = [1,1]; sub = [1,1]; time = [1,2]
    srcPid = [1,1]; dstPid = [1,1]; srcGid = [1,2]; dstGid = [1,2]
    tbd0 = [1,2]; tbd1 = [1,2]; tbd2 = [1,2]; zone = [1,1]; CheckSum = [1,1]
    crc = [1,2]
    frameList = [ pid, rxtx, sensor, micom, gid,
        high, low, level, Type, rate, status, dtime,
        cmd, sub, time,
        srcPid, dstPid, srcGid, dstGid, tbd0, tbd1, tbd2, zone, CheckSum, crc ]
    frame = ''
    # hks
    clearBuff = False

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

    def setFrame(self):
        frame = '{'
        for numList in self.frameList:
            if(numList[1]==2):
                frame += '%04x' % numList[0]
            else:
                frame += '%02x' % numList[0]
        frame += '}'
        print(frame)

    def getClearBuff(self):
        return self.clearBuff

    def parseFrame(self, inFrame):
        first = inFrame.rfind('{')
        last = inFrame.rfind('}')
        if last > 70:
            self.clearBuff = True
        else:
            self.clearBuff = False

        if (last - first -1) == 68:
            result = inFrame[(first+1):last]
            self.clearBuff = True
            count = 0
            temp = list()
            for s in range(1,35):
                ss = result[count:count+2]
                temp.append(int(ss,16))
                # print('count:{},{}'.format(count,ss))
                count += 2

            count = 0
            for i in self.frameList:
                if i[1] == 2:
                    i[0] = temp[count]*256
                    count += 1
                    i[0] += temp[count]
                else:
                    i[0] = temp[count]
                count += 1
            self.setFrame()
            return True
        else:
            print('Fail Parse')
            return False

    def testFrame(self):
        print('----------- testFrame --------------')
        strTest = '{01010101123464013201010100010101000101010001000100010001000101010001}1234'
        print(strTest.find('}'))
        self.parseFrame(strTest)
        if self.getClearBuff():
            print('clear input buff')
            strTest = ''
            

if __name__ == '__main__':
    frame = Frame()
    myFrame = frame.getFrame()

    str_List = '{'
    for numList in myFrame:
        if(numList[1]==2):
            str_List += '%04x' % numList[0]
        else:
            str_List += '%02x' % numList[0]
    str_List += '}'
    print(str_List)

    frame.testFrame()



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
