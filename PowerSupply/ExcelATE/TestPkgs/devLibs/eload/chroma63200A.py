from threading import RLock

import pyvisa


class EloadX(object):
    """Chrome 电子负载63200A
    Arguments:
        visaAdrr {str} -- 通讯参数
    """

    #rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
    def __init__(self, visaAdrr):
        rm = visa.ResourceManager(
        )  # this uses pyvisa C:\\Windows\\System32\\visa32.dll
        self.heromix = rm.open_resource(visaAdrr)
        ## Set Global Timeout
        self.heromix.timeout = 10000
        ## Clear the instrument bus
        self.heromix.clear()
        self.xlock = RLock()

    def close(self):
        """关闭设备通讯
        """
        self.heromix.close()

    # IEEE-488命令

    def close(self):
        self.heromix.close()

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
        self.heromix.write('*RST')
        self.xlock.release()

    def CLS(self):
        """清除寄存器的值"""
        self.xlock.acquire()
        self.heromix.write('*CLS')
        self.xlock.release()

    def set_mode(self, mode=''):
        """设置电子负载的操作模式
        mode: 'CCL'|'CCM'|'CCH'|'CVL'|'CVM'|'CVH'|'CRL'|'CRM'|'CRH'|\
        'CPL'|'CPM'|'CPH'|'CCDL'|'CCDM'|'CCDH'|'CRDL'|'CRDM'|'CRDH'|\
        'BATL'|'BATM'|'BATH'
        """
        self.xlock.acquire()
        self.heromix.write('MODE ' + mode)
        self.xlock.release()

    def set_load_state(self, onoff=''):
        """电子负载load on or off
        onoff: '0'|'OFF'|'1'|'ON'
        """
        self.xlock.acquire()
        self.heromix.write('LOAD ' + onoff)
        self.xlock.release()

    def set_load_short_state(self, onoff=''):
        """设置电子负载的短路模拟功能
        onoff: '0'|'OFF'|'1'|'ON'
        """
        self.xlock.acquire()
        self.heromix.write('LOAD:SHOR ' + onoff)
        self.xlock.release()

    def set_load_short_key(self, val=''):
        """设置电子负载的短路健模式
        val: '0'|Hold, '1'|'TOGGLE', '2'|'DISABLE'
        """
        self.xlock.acquire()
        self.heromix.write('LOAD:SHOR:KEY ' + val)
        self.xlock.release()

    def get_load_id(self):
        """查询电子负载身份"""
        self.xlock.acquire()
        ID = self.heromix.query('LOAD:ID?')
        self.xlock.release()
        return ID

    def set_config_voltRange(self, val=''):
        """设置拉载电流的电压为ON
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('CONF:VOLT:RANG ' + val)
        self.xlock.release()

    def set_config_voltOnOff(self, typ='', val=''):
        """设置拉载电流的电压为OFF
        typ: 'ON'|'OFF'
        val: 'MAX'|'MIN'|其他值
        """
        self.xlock.acquire()
        self.heromix.write('CONF:VOLT:' + typ + ' ' + val)
        self.xlock.release()

    def set_config_voltLatch(self, onoff=''):
        """设定Von的动作类别
        onoff: '0'|'ON', '1'|'OFF'
        """
        self.xlock.acquire()
        self.heromix.write('CONF:VOLY:LATC ' + onoff)
        self.xlock.release()

    def set_config_voltLatch_reset(self):
        """重新设定Von信号"""
        self.xlock.acquire()
        self.heromix.write('CONF:VOLT:LATC:RES')
        self.xlock.release()

    def set_current_static(self, ch='', val=''):
        """设定定电流静态模式下的静态负载电流
        ch: '1'|'2'
        val: 具体电流值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:STAT:L' + ch + ' ' + val)
        self.xlock.release()

    def set_current_static_slew(self, typ='', val=''):
        """设定定电流静态模式下的电流上升或下降斜率
        typ: 'RISE'|'FALL'
        val: 具体值(A/us)|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:STAT:' + typ + ' ' + val)
        self.xlock.release()

    def set_current_static_vrng(self, val=''):
        """设定CC模式下的电压量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:STAT:VRNG ' + val)
        self.xlock.release()

    def set_current_dynamic_L(self, chl='', val=''):
        """设定定电流动态模式下T1或T2期间的负载电流
        chl: '1'|'2'
        val: 具体电流值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:DYN:L' + chl + ' ' + val)
        self.xlock.release()

    def set_current_dynamic_T(self, cht='', val=''):
        """设定定电流动态模式的期间参数T1
        cht: '1'|'2'
        val: 具体时间值(单位s)|'MAX'|'MIN'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:DYN:T' + cht + ' ' + val)
        self.xlock.release()

    def set_current_dynamic_repeat(self, val=''):
        """设定定电流动态模式的重复次数
        val: '0'~'65535'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:DYN:REP ' + val)
        self.xlock.release()

    def set_current_dynamic_slew(self, typ='', val=''):
        """设定定电流动态模式下的电流上升或下降斜率
        typ: 'RISE'|'FALL'
        val: 具体值(A/us)|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:DYN:' + typ + ' ' + val)
        self.xlock.release()

    def set_current_dynamic_Irng(self, val=''):
        """设定CCD模式下的电流量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('CURR:DYN:VRNG ' + val)
        self.xlock.release()

    def set_resistance_static(self, ch='', val=''):
        """设定定电阻模式下的静态电阻位
        ch: '1'|'2'
        val: 具体电流值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('RES:STAT:L' + ch + ' ' + val)
        self.xlock.release()

    def set_resistance_static_slew(self, typ='', val=''):
        """设定定电阻静态模式下的电流上升或下降斜率
        typ: 'RISE'|'FALL'
        val: 具体值(A/us)|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('RES:STAT:' + typ + ' ' + val)
        self.xlock.release()

    def set_resistance_static_vrng(self, val=''):
        """设定CC模式下的电压量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('RES:STAT:IRNG ' + val)
        self.xlock.release()

    def set_resistance_dynamic_L(self, chl='', val=''):
        """设定定电阻动态模式下T1或T2期间的负载电阻
        chl: '1'|'2'
        val: 具体电阻值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('RES:DYN:L' + chl + ' ' + val)
        self.xlock.release()

    def set_resistance_dynamic_T(self, cht='', val=''):
        """设定定电阻动态模式的期间参数T1
        cht: '1'|'2'
        val: 具体时间值(单位s)|'MAX'|'MIN'
        """
        self.xlock.acquire()
        self.heromix.write('RES:DYN:T' + cht + ' ' + val)
        self.xlock.release()

    def set_resistance_dynaminc_repeat(self, val=''):
        """设定定电阻动态模式的重复次数
        val: '0'~'65535'
        """
        self.xlock.acquire()
        self.heromix.write('RES:DYN:REP ' + val)
        self.xlock.release()

    def set_resistance_dynamic_slew(self, typ='', val=''):
        """设定定电阻动态模式下的电流上升或下降斜率
        typ: 'RISE'|'FALL'
        val: 具体值(A/us)|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('RES:DYN:' + typ + ' ' + val)
        self.xlock.release()

    def set_resistance_dynamic_Irng(self, val=''):
        """设定CCD模式下的电流量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('RES:DYN:IRNG ' + val)
        self.xlock.release()

    def set_voltage_static(self, ch='', val=''):
        """设定定电压静态模式下的静态负载电压
        ch: '1'|'2'
        val: 具体电压值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('VOLT:STAT:L' + ch + ' ' + val)
        self.xlock.release()

    def set_voltage_static_Ilimit(self, val=''):
        """在定电压模式设定限电流
        val: 具体电流值|'MAX'|'MIN'
        """
        self.xlock.acquire()
        self.heromix.write('VOLT:STAT:ILIM ' + val)
        self.xlock.release()

    def set_voltage_static_response(self, val=''):
        """在定电压模式设定回复速度
        val: '0'|'SLOW', '1'|'NORMAL', '2'|'FAST'
        """
        self.xlock.acquire()
        self.heromix.write('VOLT:STAT:RES ' + val)
        self.xlock.release()

    def set_voltge_static_Irng(self, val=''):
        """设定定电压模式下的电流量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('VOLT:STAT:IRNG ' + val)
        self.xlock.release()

    def set_power_static(self, ch='', val=''):
        """设定定功率模式的静态负载功率
        ch: '1'|'2'
        val: 具体功率值|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('POW:STAT:L' + ch + ' ' + val)
        self.xlock.release()

    def set_power_static_slew(self, typ='', val=''):
        """设定定功率模式的电流上升或下降斜率
        typ: 'RISE'|'FALL'
        val: 具体值(A/us)|'MIN'|'MAX'
        """
        self.xlock.acquire()
        self.heromix.write('POW:STAT:' + typ + ' ' + val)
        self.xlock.release()

    def set_power_static_vrng(self, val=''):
        """设定定功率模式的电压量测档位
        val: '0'|'LOW'|'L', '1'|'MIDDLE'|'M', '2'|'HIGH'|'H'
        """
        self.xlock.acquire()
        self.heromix.write('POW:STAT:VRNG ' + val)
        self.xlock.release()

    def get_measure_current(self):
        """查询电流的量测值"""
        self.xlock.acquire()
        val = self.heromix.query('MEAS:CURR?')
        self.xlock.release()
        return float(val)

    def get_measure_power(self):
        """查询功率的量测值"""
        self.xlock.release()
        val = self.heromix.query('MEAS:POW?')
        self.xlock.release()
        return float(val)

    def get_measure_voltage(self):
        """查询电压的量测值"""
        self.xlock.acquire()
        val = self.heromix.query('MEAS:VOLT?')
        self.xlock.release()
        return float(val)
