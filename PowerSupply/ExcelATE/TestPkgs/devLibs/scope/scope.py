from math import isinf, isnan
import os
from threading import RLock
from time import sleep
import pyvisa
from ..common.common import Dev

scale_enum = (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50)


class ScopeX():
    """
    Arguments:
        rc {str} -- VISA资源列表
        instrument {str} -- 指定型号
    """

    def __init__(self, rc, instrument=None, sel=0):
        """
        Arguments:
            rc {str} -- VISA资源列表
            instrument {str} -- 指定型号
        """

        cfg = {
            "rc":
            rc,
            "instrument":
            instrument,
            "sel":
            sel,
            "key": [{
                "manufacturer": "KEYSIGHT",
                "model": ["EDU-X"]
            }, {
                "manufacturer": "TEKTRONIX",
                "model": None
            }]
        }
        dev = Dev(cfg)
        # info = dev.get_info()
        rm = pyvisa.ResourceManager()
        print(dev.addr)
        self.heromix = rm.open_resource(dev.addr)
        # Set Global Timeout
        self.heromix.timeout = 5000
        # Clear the instrument bus
        self.heromix.clear()
        self.xlock = RLock()

        # for tektronix
        self.tek_meas_index = 0
        self.idn = self.heromix.query("*IDN?")
        self.manuf = self.idn.split(" ")[0].upper()
        self.tek_meas_ch = [
            {
                "ch": 1,
                "type": ""
            },
            {
                "ch": 1,
                "type": ""
            },
            {
                "ch": 1,
                "type": ""
            },
            {
                "ch": 1,
                "type": ""
            },
        ]

    def close(self):
        self.heromix.close()

    def IDN(self):
        """获取示波器的身份标示IDN"""
        IDN = self.heromix.query("*IDN?")
        # Check whether scope is an older InfiniiVision or a newer X-Series InfiniiVision.
        # This is done by parsing the scope's identification string and looking for the 'X'.
        # IDN parts are separated by commas, so parse on the commas
        IDN = IDN.split(',')
        # mfg = IDN[0] # Python indices start at 0
        model = IDN[1]
        # SN = IDN[2]
        # FW = IDN[3]
        scopeTypeCheck = list(model)
        if scopeTypeCheck[3] == "-" or scopeTypeCheck[1] == "9":
            self.generation = "X_Series"
        else:
            self.generation = "Older_Series"
        del scopeTypeCheck, model
        return IDN

    def CLS(self):
        """清除寄存器的值"""
        self.heromix.write('*CLS')

    def RST(self):
        """复位"""
        self.heromix.query('*RST')

    def set_autoScale(self):
        """自动调整"""
        if self.manuf == "KEYSIGHT":
            self.heromix.write('AUTO:ENA')
        else:
            self.heromix.write('AUTOSet EXECute')

    def set_run(self):
        """设置示波器RUN模式"""
        if self.manuf == "KEYSIGHT":
            self.heromix.write('RUN')
        else:
            self.heromix.write('ACQ:STATE ON')
            # self.heromix.write('ACQuire:STATE RUN')

    def set_stop(self):
        """设置示波器STOP模式"""
        if self.manuf == "KEYSIGHT":
            self.heromix.write('STOP')
        else:
            self.heromix.write('ACQuire:STATE OFF')
            # self.heromix.write('ACQuire:STATE STOP')

    def set_single(self):
        """设置示波器SINGLE模式"""
        if self.manuf == "KEYSIGHT":
            self.heromix.write('SING')
        else:
            self.heromix.write("ACQE:STOPA SEQ")
            self.heromix.write('ACQ:STATE 1')

    def get_state(self):
        """设置示波器SINGLE模式"""
        self.xlock.acquire()
        if self.manuf == "KEYSIGHT":
            val = (int(self.heromix.query(':OPER:COND?')) & 8) >> 3
        else:
            val = self.heromix.query('ACQuire:STATE?')
        self.xlock.release()
        return val

    def set_measure_clear(self):
        """清除所有测量显示"""
        if self.manuf == "KEYSIGHT":
            self.heromix.write('MEAS:CLE')
        else:
            for i in range(4):
                self.heromix.write('MEASU:MEAS{0}:STATE OFF'.format(i + 1))
            self.tek_meas_index = 0

    def add_measure(self, source, vtype, args=None):
        """测量电压显示
        Arguments:
            ch {num} -- 通道
            vtype {str} -- {MAXI|MINI|NOV|POV|VPP|AMP|VAV|VBAS|VTOP|RMS|DELAY}
        """
        if self.manuf == "KEYSIGHT":
            if vtype == "POV" or vtype == "NOV":
                vtype = "OVER"
            if vtype == "AMP" or vtype == "MAX" or vtype == "RMS":
                vtype = "V" + vtype
            if vtype == "MINI":
                vtype = "VMIN"
            if type(source) is not str:
                ch = "CHAN" + str(source)
            else:
                ch = source
            self.heromix.write(':MARK:MODE {0}'.format("MEAS"))
            self.heromix.write(':MEAS:{0} {1}'.format(vtype, ch))
        else:
            if type(source) is not str:
                ch = "CH" + str(source)
            else:
                ch = source
            if vtype == "VPP":
                vtype = "PK2P"
            self.heromix.write(
                'MEASU:MEAS{0}:STATE ON'.format(self.tek_meas_index % 4 + 1))
            self.heromix.write('MEASU:MEAS{0}:SOU {1}'.format(
                self.tek_meas_index % 4 + 1, ch))
            self.heromix.write('MEASU:MEAS{0}:TYP {1}'.format(
                self.tek_meas_index % 4 + 1, vtype))
            self.tek_meas_ch[self.tek_meas_index % 4]["ch"] = ch
            self.tek_meas_ch[self.tek_meas_index % 4]["type"] = vtype
            self.tek_meas_index += 1

    def get_measure_val(self, source, vtype):
        """获取测量电压值(V)
        Arguments:
            ch {num} -- 通道
            vtype {str} -- {AMP|ARE|BUR|CAR|CME|CRM|DEL|FALL|FREQ|HIGH|LOW|
                            MAXI|MEAN|MINI|NDU|NEDGEC|NOV|NPULSEC|NWI|PEDGEC|
                            PDU|PERI|PHA|PK2PK|POV|PPULSEC|PWI|RIS|RMS}
                AMP: 幅值
                ARE:
                BUR: 脉冲
        Returns:
            {float} --
        """
        if self.manuf == "KEYSIGHT":
            if vtype == "POV" or vtype == "NOV":
                vtype = "OVER"
            if vtype == "AMP" or vtype == "MAX":
                vtype = "V" + vtype
            if vtype == "MINI":
                vtype = "VMIN"
            if type(source) is not str:
                source = "CHAN" + str(source)
            val = float(
                self.heromix.query(':MEAS:{0}? {1}'.format(vtype, source)))
            if isnan(val) or isinf(val):
                val = 996699
            return val
        else:
            if type(source) is not str:
                source = "CH" + str(source)
            # self.heromix.write('MEASU:IMM:SOU {0}'.format(source))
            # self.heromix.write('MEASU:IMM:TYP {0}'.format(vtype))
            # val = float(self.heromix.query('MEASU:IMM:VAL?'))
            # if isnan(val) or isinf(val):
            #     val = 996699
            # return float(val)
            if vtype == "VPP":
                vtype = "PK2P"
            ch = 0
            for i in range(len(self.tek_meas_ch)):
                if self.tek_meas_ch[i]["ch"] == source:
                    if self.tek_meas_ch[i]["type"] == vtype:
                        ch = i + 1
                        break
            if ch > 0:
                val = float(self.heromix.query(
                    'MEASU:MEAS{0}:VAL?'.format(ch)))
                if isnan(val) or isinf(val):
                    val = 996699
                return float(val)
            return 996699

    def save_image_to_pc(self, imgPath, imgName):
        """将示波器波形截图保存到本地
        imgPath: 波形路径
        imgName: 波形命名
        """
        self.xlock.acquire()
        imgFmt = ".png"
        if self.manuf == "KEYSIGHT":
            self.IDN()
            # Turns off previously displayed (non-error) messages
            self.heromix.query(':SYSTEM:DSP "";*OPC?')
            # The following command defines whether the image background will be black or white.
            # If you want to save ink, turn on this 'inksaver' setting.
            self.heromix.write(":HARDCOPY:INKSAVER OFF")
            # Ask scope for screenshot in png format
            if self.generation == "Older_Series":
                # The older InfiniiVisions have 3 parameters
                self.heromix.write(":DISPlAY:DATA? PNG, SCREEN, COLOR")
            elif self.generation == "X_Series":
                # The newer InfiniiVision-Xs do not have the middle parameter above
                self.heromix.write(":DISPlAY:DATA? PNG, COLOR")

            imgData = self.heromix.read_raw()
            # print("Image has been read.\n")
            # Returns image data as a List of floating values
            imgData = binblock_raw(imgData)

        else:
            IDN = self.heromix.query("*IDN?")
            if IDN.find("TDS 2024C") > 0:
                imgFmt = ".bmp"
                self.heromix.write("SAVe:IMAGe:FILEFormat BMP")
            else:
                imgFmt = ".png"
                self.heromix.write("SAVe:IMAGe:FILEFormat PNG")
            self.heromix.write("SAVe:IMAGe:INKSaver OFF")
            self.heromix.write("HARDCopy STARt")
            imgData = self.heromix.read_raw()
            # print("Image has been read.\n")

        imgName += imgFmt
        if not os.path.exists(imgPath):
            os.makedirs(imgPath)
        filename = os.path.join(imgPath, imgName)
        imgFile = open(filename, "wb")
        imgFile.write(imgData)
        imgFile.close()
        self.xlock.release()
        return imgName

    def set_channel_autoscale(self,
                              ch,
                              display="ON",
                              coupling="DC",
                              vin=24,
                              offset=1,
                              probe=10,
                              units="V"):
        """设置通道单位
        Arguments:
            ch {num or str}--{1|2 or CH1+CH2|CH1-CH2|CH3+CH4|CH3-CH4|CH1*CH2|CH3*CH4}
            display {str} -- {ON|OFF}
            coupling {num or str} -- {AC|DC|GND}
            scale {num} -- 通道每格宽度
            probe {num} -- 探头比例
            offset {num} -- 偏移值
            display {num or str} -- {ON|OFF}
            units {str} -- {V|A}
        """
        scale = 1
        for sca in scale_enum:
            if (4 - offset) * sca > vin:
                scale = sca
                break
        self.set_channel(ch, display, coupling, scale, offset, probe, units)

    def set_channel(self,
                    ch,
                    display="ON",
                    coupling="DC",
                    scale=1,
                    offset=1,
                    probe=10,
                    units="V"):
        """设置通道单位
        Arguments:
            ch {num or str}--{1|2 or CH1+CH2|CH1-CH2|CH3+CH4|CH3-CH4|CH1*CH2|CH3*CH4}
            display {str} -- {ON|OFF}
            coupling {num or str} -- {AC|DC|GND}
            scale {num} -- 通道每格宽度
            probe {num} -- 探头比例
            offset {num} -- 偏移值
            display {num or str} -- {ON|OFF}
            units {str} -- {V|A}
        """
        if type(ch) is str and len(ch) == 7:
            if self.manuf == "KEYSIGHT":
                if ch[3] == "+":
                    func = "ADD"
                elif ch[3] == "-":
                    func = "SUBT"
                elif ch[3] == "*":
                    func = "MULT"
                self.heromix.write('FUNC:OPER {0}'.format(func))
                self.heromix.write('FUNC:DISP {0}'.format(display))
                self.heromix.write('FUNC:SCAL {0}'.format(scale))
                self.heromix.write('FUNC:OFFS {0}'.format(-offset * scale))
            else:
                self.heromix.write('MATH:DEFINE "{0}"'.format(ch))
                self.heromix.write('SEL:MATH {0}'.format(display))
                self.heromix.write('MATH:VERT:SCA {0}'.format(scale))
                self.heromix.write('MATH:VERT:POS {0}'.format(offset))
        else:
            if self.manuf == "KEYSIGHT":
                self.heromix.write(':CHAN{0}:DISP {1}'.format(ch, display))
                self.heromix.write(':CHAN{0}:COUP {1}'.format(ch, coupling))
                self.heromix.write(':CHAN{0}:SCAL {1}'.format(ch, scale))
                self.heromix.write(':CHAN{0}:PROB {1}'.format(ch, probe))
                self.heromix.write('CHAN{0}:OFFS {1}'.format(
                    ch, -offset * scale))
                if units == "V":
                    units = "VOLT"
                elif units == "A":
                    units = "AMP"
                self.heromix.write(':CHAN{0}:UNIT {1}'.format(ch, units))
            else:
                self.heromix.write('SEL:CH{0} {1}'.format(ch, display))
                self.heromix.write('CH{0}:COUP {1}'.format(ch, coupling))
                self.heromix.write('CH{0}:SCA {1}'.format(ch, scale))
                self.heromix.write('CH{0}:PRO:GAIN {1}'.format(ch, 1 / probe))
                self.heromix.write('CH{0}:OFFS {1}'.format(ch, 0))
                self.heromix.write('CH{0}:POS {1}'.format(ch, offset))
                self.heromix.write('CH{0}:YUN "{1}"'.format(ch, units))

    def set_trigger(self,
                    source=1,
                    mode="NORM",
                    slope="RIS",
                    level=0,
                    coupling="DC"):
        """设置通道单位
        Arguments:
            source {str} -- {CH1|CH2|CH3|CH4|LINE}
            mode {str} -- {AUTO|NORM}
            slope {str} -- {RISe|FALL}
            level {ECL|TTL|<NR3>}
                <NR3> specifies the trigger level in user units (usually volts)
                ECL specifies a preset ECL high level of -1.3V
                TTL specifies a preset TTL high level of 1.4V
        """
        if self.manuf == "KEYSIGHT":
            if type(source) is not str:
                source = "CHAN" + str(source)
            self.heromix.write('TRIG:SOUR {0}'.format(source))
            self.heromix.write('TRIG:SWE {0}'.format(mode))
            self.heromix.write('TRIG:SLOP {0}'.format(slope))
            self.heromix.write('TRIG:MODE {0}'.format("EDGE"))
            self.heromix.write('TRIG:LEV {0}'.format(level))
            self.heromix.write('TRIG:COUP {0}'.format("DC"))
        else:
            if type(source) is not str:
                source = "CH" + str(source)
            if source == "EXT":
                if self.idn.find("DPO") > 0 or self.idn.find("MDO") > 0:
                    source = "AUX"
            self.heromix.write('TRIG:A:MOD {0}'.format(mode))
            self.heromix.write('TRIG:A:EDGE:SLO {0}'.format(slope))
            self.heromix.write('TRIG:A:EDGE:SOU {0}'.format(source))
            if source == "AUX":
                self.heromix.write('AUX:PROb:GAIN {0}'.format(1))
                self.heromix.write('TRIG:A:LEV:AUX {0}'.format(level))
            else:
                self.heromix.write('TRIG:A:LEV {0}'.format(level))

    def set_timebase(self, scale, pos=0, mode="MAIN"):
        """设置时间窗口单格宽度(s)
        Arguments:
            scale {num} -- float or int number
            pos {num} -- float or int number
            mode {str} -- {MAIN|WIND|XY|ROLL}
        """
        if self.manuf == "KEYSIGHT":
            self.heromix.write(':TIM:MODE {0}'.format(mode))
            self.heromix.write('TIM:SCAL {0}'.format(scale))
            self.heromix.write('TIM:POS {0}'.format(scale * (50 - pos) / 10))
        else:
            self.heromix.write('HOR:DEL:STAT {0}'.format("OFF"))
            self.heromix.write('HOR:SCAL {0}'.format(scale))
            self.heromix.write('HOR:TRIG:POS {0}'.format(pos))

    def set_flash(self):
        self.xlock.acquire()
        if self.manuf == "KEYSIGHT":
            pass
        else:
            if self.idn.find("TBS 1") > 0:
                val = float(self.heromix.query('DIS:BACKL?'))
                self.heromix.write('DIS:BACKL 0')
                sleep(0.5)
                self.heromix.write('DIS:BACKL {0}'.format(val))
            else:
                try:
                    val = float(self.heromix.query('DIS:INTENSIT:BACKL?'))
                    self.heromix.write('DIS:INTENSIT:BACKL 0')
                    sleep(0.5)
                    self.heromix.write('DIS:INTENSIT:BACKL {0}'.format(val))
                except Exception:
                    self.heromix.write('DIS:INTENSIT:BACKL LOW')
                    sleep(1)
                    self.heromix.write('DIS:INTENSIT:BACKL HIGH')
        self.xlock.release()

    def set_resolution(self, num):
        """采样点数
        Arguments:
            num {num} -- int number
        """
        if self.manuf == "KEYSIGHT":
            pass
        else:
            self.heromix.write('HOR:RESO {0}'.format(num))

    def get_cursor_y(self, source=[
            1,
    ], pos1=0, pos2=0, units="SEC"):
        result = []
        if self.manuf == "KEYSIGHT":
            self.heromix.write('MARK:MODE {0}'.format("WAV"))
            self.heromix.write('MARK:X1P {0}'.format(pos1))
            self.heromix.write('MARK:X2P {0}'.format(pos2))
            self.heromix.write('MARK:XUN {0}'.format(units))
            for ch in source:
                if type(ch) is not str:
                    ch = "CHAN" + str(ch)
                self.heromix.write('MARK:X1Y1 {0}'.format(ch))
                self.heromix.write('MARK:X2Y2 {0}'.format(ch))
                sleep(1)
                result.append([
                    round(float(self.heromix.query('MARK:Y1P?')), 3),
                    round(float(self.heromix.query('MARK:Y2P?')), 3)
                ])
        else:
            self.heromix.write('CURS:FUNC {0}'.format("WAVE"))
            self.heromix.write('CURS:VBA:POSITION1 {0}'.format(pos1))
            self.heromix.write('CURS:VBA:POSITION2 {0}'.format(pos2))
            self.heromix.write('CURS:VBA:UNI {0}'.format(units))
            for ch in source:
                if type(ch) is not str:
                    ch = "CH" + str(ch)
                self.heromix.write('SEL:CONTROl {0}'.format(ch))
                sleep(2)
                result.append([
                    round(float(self.heromix.query('CURS:VBA:HPOS1?')), 3),
                    round(float(self.heromix.query('CURS:VBA:HPOS2?')), 3)
                ])
        return result


def binblock_raw(data_in):

    # Grab the beginning section of the image file, which will contain the header.
    Header = str(data_in[0:12])
    # print("Header is " + str(Header))
    # Find the start position of the IEEE header, which starts with a '#'.
    startpos = Header.find("#")
    # print("Start Position reported as " + str(startpos))
    # Check for problem with start position.
    if startpos < 0:
        raise IOError("No start of block found")
    # Find the number that follows '#' symbol.  This is the number of digits in the block length.
    Size_of_Length = int(Header[startpos + 1])
    # print("Size of Length reported as " + str(Size_of_Length))
    # Now that we know how many digits are in the size value, get the size of the image file.
    Image_Size = int(Header[startpos + 2:startpos + 2 + Size_of_Length])
    # print("Number of bytes in image file are: " + str(Image_Size))
    # Get the length from the header
    offset = startpos + Size_of_Length
    # Extract the data out into a list.
    return data_in[offset:offset + Image_Size]


if __name__ == "__main__":
    # print(myscope.write('SAV:IMGE 001.png'))
    # myscopeK = ScopeX("KEYSIGHT")
    myscopeT = ScopeX("TEKTRONIX")

    # myscopeK.set_channel(1, "ON","AC",5,1,1,"V")
    # myscopeK.set_channel(2, "ON","DC",10,10,2,"A")

    # myscopeT.set_channel(1, "ON","AC",5,1,1,"A")
    # myscopeT.set_channel(2, "ON","DC",10,10,2,"A")

    myscopeT.set_trigger(2, "NORM", "FALL", 1)
    # myscopeT.set_trigger(2, "NORM", "RIS",1)

    # myscopeK.set_timebase(0.1, 60)
    # myscopeT.set_timebase(0.001, 50)
    # myscope = ScopeX("TEKTRONIX")
    # myscope.set_timebase_position(20)

    # myscope.set_single()
    # print(myscope.get_state())
    # print(myscope.get_measure_type_val(1, "RMS"), myscope.get_measure_type_val(2, "RMS"),
    #       myscope.get_measure_type_val(3, "RMS"), myscope.get_measure_type_val(4, "RMS"))
    # myscope.set_timebase_position(60)
    # myscope.set_trigger_force()

    # print(myscope.IDN())
    # myscope.save_image_to_pc('E:\\', '0001.png')
    # myscope.heromix.write(':SAVE:WAVEFORM:FILEFORMAT SPREADSHEET')
    # print(myscope.heromix.write(':SAVE:WAVEFORM ALL,"F:\\ZG\\test1_all.csv"'))
    # print(myscope.save_image_to_pc("E:\\","testpng.png"))
