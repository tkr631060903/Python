"""ZLG USB-CAN drives Module"""
from ctypes import (CDLL, POINTER, Structure, c_byte, c_char, c_char_p, c_int,
                    c_int16, c_int32, c_ubyte, c_uint, c_uint16, c_uint32,
                    c_void_p, cdll, windll)
from threading import RLock

import pyvisa


class VCI_BORD_INFO(Structure):
    """板卡信息结构体"""
    _fields_ = [
        ('hw_Version', c_uint16),  # 硬件版本号
        ('fw_Version', c_uint16),  # 固件版本号
        ('dr_Version', c_uint16),  # 驱动程序版本号
        ('in_Version', c_uint16),  # 接口库版本号
        ('irq_Num', c_uint16),  # 板卡所使用的中断号
        ('can_Num', c_byte),  # 表示有几路CAN通道
        ('str_Serial_Num', c_char * 20),  # 此板卡的序列号，元素20个的字符型数组
        ('str_hw_Type', c_char * 40),  # 硬件类型
        ('Reserved', c_uint16 * 4)
    ]  # 系统保留


class VCI_CAN_OBJ(Structure):
    """CAN帧结构体"""
    _fields_ = [
        ('ID', c_uint),  # 帧ID, 32位变量
        ('TimeStamp', c_uint),  # 设备接收到某一帧的时间标识
        ('TimeFlag', c_byte),  # 是否使用时间标识
        ('SendType', c_byte),  # 发送帧类型。0为正常发送，1为单次发送，2为自发自收，3为单次自发自收
        ('RemoteFlag', c_byte),  # 是否远程帧。0为数据帧，1为远程帧
        ('ExternFlag', c_byte),  # 是否扩展帧。0为标准帧，1为扩展帧
        ('DataLen', c_ubyte),  # 数据长度DLC<=8
        ('Data', c_ubyte * 8),  # CAN帧的数据，最大为8个字节
        ('Reserved', c_byte * 3)
    ]  # 系统保留


class VCI_CAN_STATUS(Structure):
    """CAN状态结构体"""
    _fields_ = [
        ('ErrInterrupt', c_ubyte),  # 中断记录，读操作会清除中断
        ('regMode', c_ubyte),  # CAN控制器模式寄存器值
        ('regStatus', c_ubyte),  # CAN控制器状态寄存器值
        ('regALCapture', c_ubyte),  # CAN控制器仲裁丢失寄存器值
        ('regECCapture', c_ubyte),  # CAN控制器错误寄存器值
        ('regEWLimit', c_ubyte),  # CAN控制器错误警告限制寄存器值。默认为96
        ('regRECounter', c_ubyte),  # CAN控制器接收错误寄存器值。
        ('regTECounter', c_ubyte),  # CAN控制器发送错误寄存器值。
        ('Reserved', c_int32)
    ]  # 系统保留


class VCI_ERR_INFO(Structure):
    """错误信息结构体"""
    _fields_ = [
        ('ErrCode', c_uint),  # 错误码
        # 当产生的错误中有消极错误时表示为消极错误的错误标识数据。
        ('Passive_ErrData', c_byte * 3),
        ('ArLost_ErrData', c_byte)
    ]  # 当产生的错误中有仲裁丢失错误时表示为仲裁丢失错误的错误标识数据。


class VCI_INIT_CONFIG(Structure):
    """板卡初始化结构体"""
    _fields_ = [
        ('AccCode', c_uint),  # 验收码
        ('AccMask', c_uint),  # 屏蔽码。
        ('Reserved', c_uint),  # 保留
        ('Filter', c_ubyte),  # 滤波方式。1表示单滤波，0表示双滤波
        ('Timing0', c_ubyte),  # 波特率定时器0(BTR0)
        ('Timing1', c_ubyte),  # 波特率定时器1(BTR1)
        ('Mode', c_ubyte)
    ]  # 模式。0表示正常模式，1表示只听模式


class CHGDESIPANDPORT(Structure):
    _fields_ = [
        ('szpwd', c_char),  # 更改目标IP和端口所需要的木马，长度小于10
        ('szdesip', c_char),  # 所要更改的目标IP，比如为"192.168.0.111"
        ('desport', c_int),  # 所要更改的目标端口，比如4000
        ('blisten', c_byte)
    ]  # 所要更改的工作模式。0表示正常模式，1表示只听模式


class VCI_FILTER_RECORD(Structure):
    _fields_ = [
        ('ExtFrame', c_int),  # 过滤的帧类型标志，1过滤扩展帧，0过滤标准帧
        ('Start', c_int),  # 滤波范围的起始帧ID
        ('End', c_int)
    ]  # 滤波范围的结束帧ID


class CANX(object):
    """设置设备关键参数
    Keyword Arguments:
        devType {int} -- 设备类型号
            VCI_PCI5121 = 1
            VCI_PCI9810 = 2
            VCI_USBCAN1 = 3
            VCI_USBCAN2A = 4
            VCI_PCI9820 = 5
            VCI_CAN232 = 6
            VCI_PCI5110 = 7
            VCI_CANLITE = 8
            VCI_ISA9620 = 9
            VCI_ISA5420 = 10
            VCI_PCI104CAN = 11
            VCI_CANETUDP = 12
            VCI_CANETE = 12
            VCI_DNP9810 = 13
            VCI_PCI9840 = 14
            VCI_PCI5010U = 15
        devInd {int} -- 设备索引号,比如一个CAN卡时，是0，第二块CAN卡是1，类推
    """

    def __init__(self, devType=0, devInd=0):
        from os import path
        thisfiledir = path.dirname(path.abspath(__file__))
        self.xlock = RLock()
        dllpath = path.join(thisfiledir, '_cdll', 'ControlCAN.dll')
        print(dllpath)
        self.rm = windll.LoadLibrary(dllpath)
        self.devType = devType
        self.devInd = devInd

    def IDN(self):
        if self.openDevice() == 1:
            return 'CANalyst-II\n'
        else:
            return 'ERROR\n'

    def openDevice(self):
        """用以打开设备
        Keyword Arguments:
            devType: 设备类型号
            devInd: 设备索引号,比如一个CAN卡时，是0，第二块CAN卡是1，类推
            reserved: 保留参数，通常为0
        """
        self.xlock.acquire()
        #self.rm.VCI_OpenDevice.argtypes(c_uint32, c_uint32, c_uint32)
        reserved = 0
        ret = self.rm.VCI_OpenDevice(self.devType, self.devInd, reserved)
        self.xlock.release()
        return ret

    def closeDevice(self):
        """用以关闭设备
        Keyword Arguments:
            devType: 设备类型号
            devInd: 设备索引号
        """
        self.xlock.acquire()
        ret = self.rm.VCI_CloseDevice(self.devType, self.devInd)
        self.xlock.release()
        return ret

    def initCAN(self, CANInd=0, baudRate=500):
        """初始化指定的CAN通道
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            baudRate: 波特率，单位Kbps
        """
        ##--------------#--------------#--------------#
        # CAN波特率       定时器0         定时器1
        ##--------------#--------------#--------------#
        # 5Kbps           0xBF           0xFF
        ##--------------#--------------#--------------#
        # 10Kbps          0x31           0x1C
        ##--------------#--------------#--------------#
        # 20Kbps          0x18           0x1C
        ##--------------#--------------#--------------#
        # 40Kbps          0x87           0xFF
        ##--------------#--------------#--------------#
        # 50Kbps          0x09           0x1C
        ##--------------#--------------#--------------#
        # 80Kbps          0x83           0xFF
        ##--------------#--------------#--------------#
        # 100Kbps         0x04           0x1C
        ##--------------#--------------#--------------#
        # 125Kbps         0x03           0x1C
        ##--------------#--------------#--------------#
        # 200Kbps         0x81           0xFA
        ##--------------#--------------#--------------#
        # 250Kbps         0x01           0x1C
        ##--------------#--------------#--------------#
        # 400Kbps         0x80           0xFA
        ##--------------#--------------#--------------#
        # 500Kbps         0x00           0x1C
        ##--------------#--------------#--------------#
        # 666Kbps         0x80           0xB6
        ##--------------#--------------#--------------#
        # 800Kbps         0x00           0x16
        ##--------------#--------------#--------------#
        # 1000Kbps        0x00           0x14
        ##--------------#--------------#--------------#
        self.xlock.acquire()
        self.rm.VCI_InitCAN.argtypes = (c_uint32, c_uint32, c_uint,
                                        POINTER(VCI_INIT_CONFIG))

        pInitConfig = VCI_INIT_CONFIG()
        pInitConfig.AccCode = 0x00000000
        pInitConfig.AccMask = 0xFFFFFFFF
        pInitConfig.Reserved = 0
        pInitConfig.Filter = 0  # 单滤波
        pInitConfig.Mode = 0  # 正常模式
        if baudRate == 500:
            pInitConfig.Timing0 = 0x00
            pInitConfig.Timing1 = 0x1C
        elif baudRate == 250:
            pInitConfig.Timing0 = 0x01
            pInitConfig.Timing1 = 0x1C
        elif baudRate == 200:
            pInitConfig.Timing0 = 0x81
            pInitConfig.Timing1 = 0xFA
        ret = self.rm.VCI_InitCAN(self.devType, self.devInd, c_uint(CANInd),
                                  pInitConfig)
        self.xlock.release()
        return ret

    def readBoardInfo(self, CANInd=0):
        """此函数用以获取设备信息
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            pInfo: 用来存储设备信息的VCI_BOARD_INFO结构指针
        """
        self.xlock.acquire()
        self.rm.VCI_ReadBoardInfo.argtypes(c_uint32, c_uint32, c_uint,
                                           POINTER(VCI_BORD_INFO))
        pInfo = VCI_BORD_INFO()
        ret = self.rm.VCI_ReadBoardInfo(self.devType, self.devInd, CANInd,
                                        pInfo)
        self.xlock.release()
        return ret

    def readErrInfo(self, CANInd=0):
        """用以获取CAN卡发生的最近一次错误信息
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            pErrInfo: 用来存储错误信息的VCI_ERR_INFO结构指针
        """
        self.xlock.acquire()
        self.rm.VCI_ReadErrInfo.argtypes = (c_uint32, c_uint32, c_uint,
                                            POINTER(VCI_ERR_INFO))
        pErrInfo = VCI_ERR_INFO()
        flag = self.rm.VCI_ReadErrInfo(self.devType, self.devInd, CANInd,
                                       pErrInfo)
        if flag == 1:
            info = pErrInfo.ErrCode
        else:
            info = '读取错误信息失败'
        self.xlock.release()
        return info

    def readCANStatus(self, CANInd=0):
        """用以获取CAN状态
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            pCANStatus: 用来存储CAN状态的VCI_CAN_STATUS结构体指针
        """
        self.xlock.acquire()
        self.rm.VCI_ReadCANStatus.argtypes = (c_uint32, c_uint32, c_uint,
                                              POINTER(VCI_CAN_STATUS))
        pCANStatus = VCI_CAN_STATUS()
        flag = self.rm.VCI_ReadCANStatus(self.devType, self.devInd,
                                         c_uint(CANInd), pCANStatus)
        if flag == 1:
            datalist = [0] * 9
            datalist[0] = pCANStatus.ErrInterrupt
            datalist[1] = pCANStatus.regMode
            datalist[2] = pCANStatus.regStatus
            datalist[3] = pCANStatus.regALCapture
            datalist[4] = pCANStatus.regECCapture
            datalist[5] = pCANStatus.regEWLimit
            datalist[6] = pCANStatus.regRECounter
            datalist[7] = pCANStatus.regTECounter
            datalist[8] = pCANStatus.Reserved
            ret = datalist
        else:
            ret = '读取CAN状态失败'
        self.xlock.release()
        return ret

    def getReference(self, CANInd=0, refType=0):
        """用以获取设备的相应参数
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            refType: 参数类型
            pData: 用来存储参数有关数据缓存区地址首指针
        """
        self.xlock.acquire()
        self.rm.VCI_GetReference.argtypes = (c_uint32, c_uint32, c_uint32,
                                             c_uint32, POINTER(c_byte))
        pData = c_byte(0)
        ret = self.rm.VCI_GetReference(self.devType, self.devInd,
                                       c_uint32(CANInd), c_uint32(refType),
                                       pData)
        self.xlock.release()
        return ret

    def setReference(self, CANInd=0, refType=0):
        """设置设备的相应参数
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
            refType: 参数类型
            pData: 用来存储参数有关数据缓存区地址首指针
        """
        self.xlock.acquire()
        self.rm.VCI_SetReference.argtypes = (c_uint32, c_uint32, c_uint32,
                                             c_uint32, POINTER(c_byte))
        pData = c_byte(0)
        ret = self.rm.VCI_SetReference(self.devType, self.devInd,
                                       c_uint32(CANInd), c_uint32(refType),
                                       pData)
        self.xlock.release()
        return ret

    def startCAN(self, CANInd=0):
        """此函数用以启动CAN卡的某一个CAN通道
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
        """
        self.xlock.acquire()
        ret = self.rm.VCI_StartCAN(self.devType, self.devInd, c_uint32(CANInd))
        self.xlock.release()
        return ret

    def resetCAN(self, CANInd=0):
        """此函数用以复位CAN
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
        """
        self.xlock.acquire()
        ret = self.rm.VCI_ResetCAN(self.devType, self.devInd, c_uint32(CANInd))
        self.xlock.release()
        return ret

    def getReceiveNum(self, CANInd=0):
        """用以获取指定CAN通道的接收缓冲区中，接收到但尚未被读取的帧数量
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
        """
        # self.xlock.acquire()
        ret = self.rm.VCI_GetReceiveNum(self.devType, self.devInd,
                                        c_uint32(CANInd))
        # self.xlock.release()
        return ret

    def clearBuffer(self, CANInd=0):
        """用以清空指定CAN通道的缓冲区
        Keyword Arguments:
            CANInd: 第几路CAN。0位第一路，1为第二路
        """
        self.xlock.acquire()
        ret = self.rm.VCI_ClearBuffer(self.devType, self.devInd,
                                      c_uint32(CANInd))
        self.xlock.release()
        return ret

    def transmit(self,
                 CANInd=0,
                 ID=0,
                 sendType=0,
                 remoteFlag=0,
                 externFlag=0,
                 data=[] * 8):
        """发送CAN帧
        Keyword Arguments:
            CANInd {int} -- 第几路CAN。0位第一路，1为第二路 (default: {0})
            ID {int} --  帧ID (default: {0})
            sendType {int} -- 发送帧类型。0为正常发送，1为单次发送，2为自发自收，3为单次自发自收 (default: {0})
            remoteFlag {int} -- 0为数据帧，1为远程帧 (default: {0})
            externFlag {int} -- 0为标准帧，1为扩展帧 (default: {0})
            data {list} -- CAN帧的数据，最大8个字节，不用的字节补0x00, 数据为16进制  (default: {[]*8})
        Returns:
            [type] -- 返回值为实际发送成功的帧数
        """
        self.xlock.acquire()
        self.rm.VCI_Transmit.argtypes = (c_uint32, c_uint32, c_uint32,
                                         POINTER(VCI_CAN_OBJ), c_uint32)

        Len = 1  # Len: 要发送的帧结构体数组的长度(发送的帧数量),默认发送一帧
        pSend = VCI_CAN_OBJ()
        pSend.ID = ID
        pSend.SendType = sendType
        pSend.RemoteFlag = remoteFlag
        pSend.ExternFlag = externFlag
        pSend.DataLen = 8
        for i in range(8):
            pSend.Data[i] = data[i]
            # print('s: ' + str(pSend.Data[i]))

        ret = self.rm.VCI_Transmit(self.devType, self.devInd, c_uint32(CANInd),
                                   pSend, c_uint32(Len))
        self.xlock.release()
        return ret

    def receive2(self, CANInd=0, waitTime=-1):
        """读取CAN帧
        Keyword Arguments:
            CANInd {int} -- 第几路CAN。0位第一路，1为第二路 (default: {0})
            waitTime {int} -- 缓冲区无数据，函数阻塞等待时间。以毫秒为单位。若为-1则表示无超时，一直等待。 (default: {-1})
        Returns:
            {list} -- 返回值为实际接收到的CAN帧字符串列表, 字符串中数字为16进制数
        """
        self.xlock.acquire()
        self.rm.VCI_Receive.argtypes = (c_uint32, c_uint32, c_uint32,
                                        POINTER(VCI_CAN_OBJ), c_uint32, c_int)
        Len = self.getReceiveNum(CANInd)  # Len: 用以接收的帧结构体数组的长度(接收的帧数量)
        # Len = 1
        pReceive = VCI_CAN_OBJ()
        rdatalist = []
        for _ in range(Len):
            self.rm.VCI_Receive(self.devType, self.devInd, c_uint32(CANInd),
                                pReceive, c_uint32(Len), c_int(waitTime))
            rDatas = hex(pReceive.ID) + ' '
            rDatas += ' '.join(
                [hex(pReceive.Data[i])[2:4].zfill(2) for i in range(8)])
            rdatalist.append(rDatas)
        self.clearBuffer(CANInd)
        self.xlock.release()
        return rdatalist

    def receive(self, CANInd=0, waitTime=-1):
        """读取CAN帧
        Keyword Arguments:
            CANInd {int} -- 第几路CAN。0位第一路，1为第二路 (default: {0})
            waitTime {int} -- 缓冲区无数据，函数阻塞等待时间。以毫秒为单位。若为-1则表示无超时，一直等待。 (default: {-1})
        Returns:
            {str} -- 返回值为实际接收到的CAN帧字符串
        """
        self.xlock.acquire()
        self.rm.VCI_Receive.argtypes = (c_uint32, c_uint32, c_uint32,
                                        POINTER(VCI_CAN_OBJ), c_uint32, c_int)
        # Len = self.getReceiveNum(CANInd)  # Len: 用以接收的帧结构体数组的长度(接收的帧数量)
        Len = 1
        pReceive = VCI_CAN_OBJ()
        self.rm.VCI_Receive(self.devType, self.devInd, c_uint32(CANInd),
                            pReceive, c_uint32(Len), c_int(waitTime))
        rDatas = hex(pReceive.ID) + ' '
        rDatas += ' '.join(
            [hex(pReceive.Data[i])[2:4].zfill(2) for i in range(8)])
        # self.clearBuffer(CANInd)
        self.xlock.release()
        return rDatas


if __name__ == "__main__":
    from time import sleep
    myCAN = CANX(4, 0)
    print(myCAN.IDN())
    print(myCAN.openDevice())
    print(myCAN.initCAN(CANInd=0))
    print(myCAN.initCAN(CANInd=1, baudRate=500))
    print(myCAN.startCAN(0))
    print(myCAN.startCAN(1))
    # sleep(2)
    # print(myCAN.readBoardInfo())
    '''
    for _ in range(10):
        myCAN.transmit(CANInd=0,
                       data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x0F])
        sleep(1e-6)
        print(myCAN.receive(CANInd=1))
        sleep(0.5)
    '''
    noframe = '0x0 00 00 00 00 00 00 00 00'
    cnt = 0
    for _ in range(10000):
        framelist = myCAN.receive(CANInd=0)
        if framelist != noframe:
            print(cnt, framelist)
        cnt += 1
        sleep(1)
