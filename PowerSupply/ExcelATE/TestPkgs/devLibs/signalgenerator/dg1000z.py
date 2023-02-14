from threading import RLock

import pyvisa


class SignalGen(object):
    """
    Arguments:
        addr {str} -- 通讯参数
    """

    def __init__(self, addr):
        # 'C:\\Windows\\System32\\visa32.dll'
        ###############
        rm = visa.ResourceManager()
        self.heromix = rm.open_resource(addr)
        # Set Global Timeout
        self.heromix.timeout = 1000
        # Clear the instrument bus
        self.heromix.clear()
        rstatus = self.heromix.write('*CLS')
        self.xlock = RLock()

    def close(self):
        """关闭设备通讯
        """
        self.heromix.close()

    # IEEE-488命令

    def IDN(self):
        """查询设备的身份信息
        Returns:
            {str} -- [description]
        """
        self.xlock.acquire()
        info = self.heromix.query('*IDN?')
        self.xlock.release()
        return info

    def RST(self):
        """恢复设备到工厂状态
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('*RST')
        self.xlock.release()
        return rstatus

    def CLS(self):
        """清除寄存器的值"""
        self.xlock.acquire()
        rstatus = self.heromix.write('*CLS')
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write('COUN:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

    def get_counter_measure(self):
        """查询频率计的测量结果     
        Returns:
            float -- [description]
        """
        self.xlock.acquire()
        try:
            res = self.heromix.query('COUN:MEAS?')
        except Exception as err:
            res = 999999999
            print(err)
        self.xlock.release()
        return float(res)

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
        self.xlock.acquire()
        rstatus = self.heromix.write('COUP:AMPL:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write('COUP:FREQ:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write('COUP:PHAS:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write('DISP:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

    def get_display_data(self):
        """查询前面板显示屏图像
        Returns:
            {str} -- 屏幕图像数据
        """
        self.xlock.acquire()
        res = self.heromix.write('DISP:DATA?')
        self.xlock.release()
        return res

    def get_screen_image(self, imgpath):
        """保存屏幕图像
        Arguments:
            imgpath {str} -- 图片路径 如 C:\\001.png
        """
        self.heromix.write(':HCOP:SDUM:DATA:FORM PNG')
        res = self.get_display_data()
        with open(imgpath, 'wb') as f:
            f.write(res[13:])
        return imgpath

    def get_display_text(self):
        """查询屏幕上当前显示的字符串
        Returns:
            {str} -- 字符串
        """
        self.xlock.acquire()
        res = self.heromix.write('DISP:TEXT?')
        self.xlock.release()
        return res

    def set_display_text(self, vtype='', val=''):
        """      
        vtype='CLE', val=''
            :清除屏幕上当前显示的字符串
        vtype='SET', val=
            :从屏幕指定坐标处开始显示指定字符串
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('DISP:TEXT:{0} {1}'.format(vtype, val))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write('OUTP{0}:{1} {2}'.format(n, vtype, val))
        self.xlock.release()
        return rstatus

    def get_source_apply(self, n=''):
        """查询指定通道的波形类型及其频率、幅度、偏移和相位值
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
        Returns:
            {list} -- 波形类型及其频率、幅度、偏移和相位值, 
        """
        self.xlock.acquire()
        res = self.heromix.write('SOUR{0}:APPLY?')
        self.xlock.release()
        resnew = res.split(',')
        for i in range(1, len(resnew)):
            resnew[i] = float(resnew[i])
        return resnew

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
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:APPL:ARB{1} {2} {3}'.format(
            n, sample_rate, amp, offset))
        self.xlock.release()
        return rstatus

    def set_source_apply_dc(self, n=''):
        """设置指定通道的波形为具有指定偏移的直流
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:APPL:DC'.format(n))
        self.xlock.release()
        return rstatus

    def set_source_func(self, ch, func="SIN"):
        """设置指定通道的波形功能
        Keyword Arguments:
            ch {str or num} -- {1|2} 
            fun {str} -- {SIN|}
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:FUNC {1}'.format(ch, func))
        self.xlock.release()
        return rstatus

    def set_source_freg(self, ch, freq):
        """设置指定通道的频率
        Keyword Arguments:
            ch {str or num} -- {1|2} 
            freq {num} 
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:FREQ {1}'.format(ch, freq))
        self.xlock.release()
        return rstatus

    def set_source_volt(self, ch, volt):
        """设置指定通道的峰峰值电压
        Keyword Arguments:
            ch {str or num} -- {1|2} 
            volt {num} 
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:VOLT {1}'.format(ch, volt))
        self.xlock.release()
        return rstatus

    def set_source_volt_offset(self, ch, offset):
        """设置指定通道的偏置电压
        Keyword Arguments:
            ch {str or num} -- {1|2} 
            offset {num} 
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:VOLT:OFFS {1}'.format(
            ch, offset))
        self.xlock.release()
        return rstatus

    def set_source_apply_harmonic(self,
                                  n='',
                                  freq='',
                                  amp='',
                                  offset='',
                                  pahse=''):
        """启用指定通道的谐波功能并设置基波（正弦波） 参数（频率、幅度、偏移和相位）设置指定通道的波形为具有指定采样率、幅度、 偏移和起始相位的任意波（采样率输出模式） 
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            freq {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            pahse {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write(
            'SOUR{0}:APPL:HARM:{1} {2} {3} {4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

    def set_source_apply_noise(self, n='', amp='', offset=''):
        """设置指定通道的波形为具有指定幅度和偏移的噪声 
        Keyword Arguments:
            n {str or num} -- {1|2} (default: {''})
            amp {str} -- {<num>|DEF|MIN|MAX} (default: {''})
            offset {str} -- {<num>|DEF|MIN|MAX} (default: {''})
        Returns:
            [type] -- [description]
        """
        self.xlock.acquire()
        rstatus = self.heromix.write('SOUR{0}:APPL:NOIS:{1} {2}'.format(
            n, amp, offset))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            'SOUR{0}:APPL:PULS:{1} {2} {3} {4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            'SOUR{0}:APPL:RAMP:{1} {2} {3} {4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            ':SOUR{0}:APPL:SIN {1},{2},{3},{4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            ':SOUR{0}:APPL:SQU {1},{2},{3},{4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            ':SOUR{0}:APPL:TRI {1},{2},{3},{4}'.format(n, freq, amp, offset,
                                                       pahse))
        self.xlock.release()
        return rstatus

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
        self.xlock.acquire()
        rstatus = self.heromix.write(
            ':SOUR{0}:APPL:USER {1},{2},{3},{4}'.format(
                n, freq, amp, offset, pahse))
        self.xlock.release()
        return rstatus


def main():
    mygen = SignalGen('USB0::0x1AB1::0x0642::DG1ZA200100204::INSTR')
    print(mygen.IDN())
    mygen.set_source_apply_square(1, 500 * 1000, 3, 1.5, 0)
    mygen.set_source_apply_square(2, 500 * 1000, 3, 1.5, 0)
    mygen.set_output(1, "STAT", "ON")
    mygen.set_output(2, "STAT", "ON")


if __name__ == '__main__':
    main()
