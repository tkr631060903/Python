import serial
import serial.tools.list_ports
from time import sleep
from ..devInfo.devInfo import devInfo


class SignalGen(object):
    """
    Arguments:
        addr {str} -- 通讯参数
    """

    def tryconnect(self, addr):
        if addr.find("COM") == 0:
            for baud in (9600, 115200):
                try_cnt = 0
                while self._ser is None and try_cnt < 3:
                    try_cnt += 1
                    try:
                        ser = serial.Serial(addr, baud, timeout=1)
                        cmd = "UMO"
                        cmd = cmd.encode("ascii")
                        ser.write(cmd + b"\n")
                        sleep(0.1)
                        str_tmp = str(ser.read_all().decode("ascii"))
                        ser.close()
                        if str_tmp.find("FY") == 0:
                            print(addr)
                            self._ser = serial.Serial(addr, baud, timeout=1)
                            if addr is not self.addr_cfg:
                                self.addrInfo.setAddr("signalgen", addr)
                            return
                    except Exception:
                        try_cnt = 3

    def __init__(self, rc=None, instrument=None, sel=0):
        self.addrInfo = devInfo()
        self._ser = None
        self.addr_cfg = self.addrInfo.getAddr("signalgen")
        self.tryconnect(self.addr_cfg)
        for port in list(serial.tools.list_ports.comports()):
            if self._ser is None:
                self.tryconnect(port[0])
        # addrInfo.setAddr("signalgen", "")
        # print("try connect times:", try_cnt)

    def close(self):
        """关闭设备通讯
        """
        self._ser.close()

    def send(self, command):
        if type(command) == str:
            command = command.encode("ascii")
        self._ser.write(command + b"\n")
        sleep(0.5)
        return self

    def exchange(self, command):
        self.send(command)
        ret = self._ser.readline()
        if ret == b"":
            return ""
            # raise TimeoutError()
        self._ser.flushInput()
        return ret[:-1].decode("ascii")  # Ditch the newline

    def IDN(self):
        """查询设备的身份信息
        Returns:
            {str} -- [description]
        """
        if self._ser is not None:
            return self.exchange("UMO")

    def RST(self):
        """恢复设备到工厂状态
        """
        pass

    def CLS(self):
        """清除寄存器的值"""
        pass

    def set_counter(self, vtype='', val=''):
        """设置频率计
        vtype='AUTO', val=''
            :发送该命令，仪器将根据被测信号的特征自动选择合适的闸门时间
        vtype='COUP', val={AC|DC}
            :设置输入信号的耦合方式为交流（AC）或直流（DC）
        vtype='GATE', val={USER1|USER2...USER6}
            :选择测量系统的闸门时间
        vtype='HF', val={ON|OFF}
            :打开或关闭频率计的高频抑制功能
        vtype='LEVE', val={<num>|MIN|Max}
            :设置频率计的触发电平
        vtype='SENS', val={<num>|MIN|Max}
            :设置频率计的触发灵敏度（单位%）
        vtype='STAT', val={ON|OFF|RUN|STOP|SINGLE}
            :设置频率计的状态

        vtype='STATI:CLEA', val=''
            :清除统计结果
        vtype='STATI:DISP', val={DIGITAL|CURVE}
            :选择频率计测量值统计结果的显示形式为数字（DIGITAL）或动态曲线（CURVE）
        vtype='STATI:STAT', val={ON|OFF}
            :打开或关闭频率计的测量结果统计功能
        """
        pass

    def get_counter_measure(self):
        """查询频率计的测量结果
        Returns:
            float -- [description]
        """
        pass

    def set_coupling_ampl(self, vtype='', val=''):
        """设置幅度耦合
        vtype='DEV', val=<num>
            :设置幅度耦合中的幅度差值
        vtype='MODE', val={OFFS|RAT}
            :选择幅度耦合模式为幅度差值（OFFSet）或幅度比例（RATio）
        vtype='RAT', val={<num>|MIN|MAX}
            :设置幅度耦合中的幅度比例
        vtype='STAT', val={ON|OFF}
            :打开或关闭幅度耦合功能
        """
        pass

    def set_coupling_frequency(self, vtype='', val=''):
        """设置频率耦合
        vtype='DEV', val=<num>
            :设置频率耦合中的频率差值
        vtype='MODE', val={OFFS|RAT}
            :选择频率耦合模式为幅度差值（OFFSet）或幅度比例（RATio）
        vtype='RAT', val={<num>|MIN|MAX}
            :设置频率耦合中的频率比例
        vtype='STAT', val={ON|OFF}
            :打开或关闭频率耦合功能
        """
        pass

    def set_coupling_phase(self, vtype='', val=''):
        """设置相位耦合
        vtype='DEV', val=<num>
            :设置相位耦合中的频率差值
        vtype='MODE', val={OFFS|RAT}
            :选择相位耦合模式为幅度差值（OFFSet）或幅度比例（RATio）
        vtype='RAT', val={<num>|MIN|MAX}
            :设置相位耦合中的相位比例
        vtype='STAT', val={ON|OFF}
            :打开或关闭相位耦合功能
        """
        pass

    def set_display(self, vtype='', val=''):
        """设置显示相关的信息
        vtype='BRIG', val={<num>|MIN|MAX}
            :设置屏幕亮度
        vtype='CONT', val={OFFS|RAT}
            :设置屏幕对比度
        vtype='MODE', val={DPV|DGV|SV}
            :选择显示模式为双通道参数（DPV）、双通道图形（DGV）或单通道显示（SV）模式
        vtype='SAV:IMM', val={ON|OFF}
            :无需等待，立即启用屏保
        vtype='SAV:STAT', val={ON|OFF}
            :打开或关闭屏幕保护功能
        vtype='STAT', val={ON|OFF}
            :打开或关闭屏幕显示
        """
        pass

    def get_display_data(self):
        """查询前面板显示屏图像
        Returns:
            {str} -- 屏幕图像数据
        """
        pass

    def get_screen_image(self, imgpath):
        """保存屏幕图像
        Arguments:
            imgpath {str} -- 图片路径 如 C:\\001.png
        """
        pass

    def get_display_text(self):
        """查询屏幕上当前显示的字符串
        Returns:
            {str} -- 字符串
        """
        pass

    def set_display_text(self, vtype='', val=''):
        """
        vtype='CLE', val=''
            :清除屏幕上当前显示的字符串
        vtype='SET', val=
            :从屏幕指定坐标处开始显示指定字符串
        """
        pass

    def set_output(self, n='', vtype='', val=''):
        """
        n={1|2}, vtype='GAT:POL', val={POS|NEG}
            :选择指定通道在门控输出模式下的门控极性为正极性（POSitive）或负极性（NEGative）
        n={1|2}, vtype='IMP', val={<ohms>|INF|MIN|MAX}
            :设置指定通道输出连接器的输出阻抗值, 1~10kΩ， 默认值50Ω
        n={1|2}, vtype='MODE', val={NORM|GAT}
            :选择指定通道输出连接器的输出模式为常规（NORMal）或者门控（GATed）
        n={1|2}, vtype='POL', val={NORM|INV}
            :设置指定通道的输出极性为常规（NORMal）或反相（INVerted）
        n={1|2}, vtype='STAT', val={ON|OFF}
            :设置指定通道的输出ON/OFF
        n={1|2}, vtype='SYNC:DEL', val={ON|OFF}
            :设置指定通道后面板 [Mod/Trig/FSK/Sync] 连接器上同步信号的输出延迟时间
        n={1|2}, vtype='SYNC:POL', val={POS|NEG}
            :选择指定通道后面板 [Mod/Trig/FSK/Sync] 连接器上同步信号的输出极性为常规（POSitive）或反相（NEGative）
        n={1|2}, vtype='SYNC:STAT', val={ON|OFF}
            :选择指定通道后面板 [Mod/Trig/FSK/Sync] 连接器上同步信号的输出极性为常规（POSitive）或反相（NEGative）
        """
        if self._ser is not None:
            cmd = "W"
            if n == 1:
                cmd += "M"
            elif n == 2:
                cmd += "F"
            if val == "ON":
                cmd += "N1"
            elif val == "OFF":
                cmd += "N0"
            self.send(cmd)

    def get_source_apply(self, n=''):
        """查询指定通道的波形类型及其频率、幅度、偏移和相位值
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
        Returns:
            {list} -- 波形类型及其频率、幅度、偏移和相位值,
        """
        pass

    def set_source_apply_arbitrary(self,
                                   n='',
                                   sample_rate='',
                                   amp='',
                                   offset=''):
        """设置指定通道的波形为具有指定采样率、幅度、 偏移和起始相位的任意波（采样率输出模式）
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            sample_rate {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_dc(self, n=''):
        """设置指定通道的波形为具有指定偏移的直流
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_func(self, ch, func="SIN"):
        """设置指定通道的波形功能
        Keyword Arguments:
            ch {str or num} -- {1|2}
            fun {str} -- {SIN|}
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_freg(self, ch, freq):
        """设置指定通道的频率
        Keyword Arguments:
            ch {str or num} -- {1|2}
            freq {num}
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_volt(self, ch, volt):
        """设置指定通道的峰峰值电压
        Keyword Arguments:
            ch {str or num} -- {1|2}
            volt {num}
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_volt_offset(self, ch, offset):
        """设置指定通道的偏置电压
        Keyword Arguments:
            ch {str or num} -- {1|2}
            offset {num}
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_harmonic(self,
                                  n='',
                                  freq='',
                                  amp='',
                                  offset='',
                                  pahse=''):
        """启用指定通道的谐波功能并设置基波（正弦波） 参数（频率、幅度、偏移和相位）
        设置指定通道的波形为具有指定采样率、幅度、 偏移和起始相位的任意波（采样率输出模式）
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_noise(self, n='', amp='', offset=''):
        """设置指定通道的波形为具有指定幅度和偏移的噪声
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_pulse(self,
                               n='',
                               freq='',
                               amp='',
                               offset='',
                               pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的脉冲
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_ramp(self, n='', freq='', amp='', offset='',
                              pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的锯齿波
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass

    def set_source_apply_sinusoid(self,
                                  n='',
                                  freq='',
                                  amp='',
                                  offset='',
                                  pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的正弦波
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        if self._ser is not None:
            cmd = "W"
            if n == "1" or n == '' or n == 1:
                cmd += "M"
            else:
                cmd += "F"
            self.send(cmd + "W0")
            f_freq = float(freq)
            f_freq *= 1000000
            f_freq = int(f_freq)
            str_freq = "F" + str(f_freq).zfill(14)
            self.send(cmd + str_freq)
            f_amp = float(amp)
            f_amp *= 100
            f_amp = int(f_amp)
            str_amp = "A"+str(f_amp//100).zfill(2)+"." + \
                str(f_amp % 100).zfill(2)
            self.send(cmd + str_amp)
            f_ofs = float(offset)
            f_ofs *= 100
            f_ofs = int(f_ofs)
            str_ofs = "O"+str(f_ofs//100).zfill(2)+"." + \
                str(f_ofs % 100).zfill(2)
            self.send(cmd + str_ofs)

    def set_source_apply_square(self,
                                n='',
                                freq='',
                                amp='',
                                offset='',
                                pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的方波
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        if self._ser is not None:
            cmd = "W"
            if n == "1" or n == '' or n == 1:
                cmd += "M"
            else:
                cmd += "F"
            self.send(cmd + "W1")
            f_freq = float(freq)
            f_freq *= 1000000
            f_freq = int(f_freq)
            str_freq = "F" + str(f_freq).zfill(14)
            self.send(cmd + str_freq)
            f_amp = float(amp)
            f_amp *= 100
            f_amp = int(f_amp)
            str_amp = "A"+str(f_amp//100).zfill(2)+"." + \
                str(f_amp % 100).zfill(2)
            self.send(cmd + str_amp)
            f_ofs = float(offset)
            f_ofs *= 100
            f_ofs = int(f_ofs)
            str_ofs = "O"+str(f_ofs//100).zfill(2)+"." + \
                str(f_ofs % 100).zfill(2)
            self.send(cmd + str_ofs)

    def set_source_apply_triangle(self,
                                  n='',
                                  freq='',
                                  amp='',
                                  offset='',
                                  pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的三角波
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        if self._ser is not None:
            cmd = "W"
            if n == "1" or n == '' or n == 1:
                cmd += "M"
            else:
                cmd += "F"
            self.send(cmd + "W4")
            f_freq = float(freq)
            f_freq *= 1000000
            f_freq = int(f_freq)
            str_freq = "F" + str(f_freq).zfill(14)
            self.send(cmd + str_freq)
            f_amp = float(amp)
            f_amp *= 100
            f_amp = int(f_amp)
            str_amp = "A"+str(f_amp//100).zfill(2)+"." + \
                str(f_amp % 100).zfill(2)
            self.send(cmd + str_amp)
            f_ofs = float(offset)
            f_ofs *= 100
            f_ofs = int(f_ofs)
            str_ofs = "O"+str(f_ofs//100).zfill(2)+"." + \
                str(f_ofs % 100).zfill(2)
            self.send(cmd + str_ofs)

    def set_source_apply_user(self, n='', freq='', amp='', offset='',
                              pahse=''):
        """设置指定通道的波形为具有指定频率、幅度、偏移和相位的任意波（频率输出模式）
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        pass


if __name__ == '__main__':
    mygen = SignalGen()
    # print(mygen.IDN())
    # mygen.set_output(1, None, "ON")
    # mygen.set_output(2, None, "OFF")
    # # mygen.set_source_apply_sinusoid('1', '200.340', '5.2', '2')
    # # mygen.set_source_apply_triangle('2', "20000.89", '2.4', '1.3')

    # mygen.set_source_apply_square(1, 500*1000, 3, 1.5, 0)
    # mygen.set_source_apply_square(2, 500*1000, 3, 1.5, 0)
    # # mygen.set_output(1, "STAT", "ON")
    # # mygen.set_output(2, "STAT", "ON")
