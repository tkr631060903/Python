from datetime import datetime
# from socket import gethostname
from time import sleep
import gevent
from corelib.instrument import DevicesClass
from corelib.config import numberDecode
try:
    from nidaqmx import Task, system
    from nidaqmx.constants import LineGrouping, TerminalConfiguration
except Exception:
    pass


class BriefControl(DevicesClass):
    """对自动化测试平台进行简单控制的方法类
    Arguments:
        object {[type]} -- [description]
    Returns:
        [type] -- [description]
    """
    def __init__(self):
        DevicesClass.__init__(self)
        try:
            sys = system.System.local()
            self.do = None
            self.di = None
            self.dio = None
            self.ai = None
            for dev in sys.devices:
                if len(dev.ai_physical_chans.channel_names) > 0:
                    self.ai = {
                        "addr": dev.name,
                        "chan": len(dev.ai_physical_chans.channel_names)
                    }
                if len(dev.di_lines.channel_names) > 0:
                    if len(dev.do_lines.channel_names) > 0:
                        self.dio = {
                            "addr":
                            dev.name,
                            "chan":
                            len(dev.do_lines.channel_names) +
                            len(dev.di_lines.channel_names)
                        }
                    else:
                        self.di = {
                            "addr": dev.name,
                            "chan": len(dev.di_lines.channel_names)
                        }
                if len(dev.do_lines.channel_names) > 0:
                    if len(dev.di_lines.channel_names) > 0:
                        self.dio = {
                            "addr":
                            dev.name,
                            "chan":
                            len(dev.do_lines.channel_names) +
                            len(dev.di_lines.channel_names)
                        }
                    else:
                        self.do = {
                            "addr": dev.name,
                            "chan": len(dev.do_lines.channel_names)
                        }
        except Exception:
            pass

    # def dut_serial_monitor(self, port='', baudrate=115200, timeout=None, recordfile=''):
    #     with Serial() as ser:
    #         ser.port = port
    #         ser.baudrate = baudrate
    #         ser.timeout = timeout
    #         with open(recordfile, 'a') as fl:
    #             while True:
    #                 msg = ser.read_all()
    #                 serialQueue.put(msg)
    #                 fl.write(msg)

    def getInputVolt(self, devtype=''):
        """获取输入电压
        Keyword Arguments:
            devtype {str} -- {dcpower|dmm} (default: {''})
                dcpower: 直流源
                dmm: 万用表
        Returns:
            {float} -- [description]
        """
        val = 540
        if devtype == 'dcpower':
            val = self.getDCPowerMeasVolt()
        elif devtype == 'dmm':
            val = self.getDmmMeasVal()
        gevent.sleep(0)
        return val

    def getInputCurr(self, devtype=''):
        """获取输入电流
        Keyword Arguments:
            devtype {str} -- {dcpower|dmm} (default: {''})
                dcpower: 直流源
                dmm: 万用表
        Returns:
            {float} -- [description]
        """
        val = 10
        # val = self.getDCPowerMeasCurr()
        gevent.sleep(0)
        return val

    def getOutputVolt(self, devtype=''):
        """获取输出电压
        Keyword Arguments:
            devtype {str} -- {eload|dmm} (default: {''})
                eload: 电子负载
                dmm: 万用表
                daq: 数据采集卡
        Returns:
            {float} -- 返回值
        """
        val = 27
        if devtype == 'dcpower':
            val = self.getEloadMeasVolt()
        elif devtype == 'dmm':
            val = self.getDmmMeasVal()
        gevent.sleep(0)
        return val

    def getOutputCurr(self, devtype=''):
        """获取输出电流
        Keyword Arguments:
            devtype {str} -- {eload|dmm} (default: {''})
                eload: 电子负载
                dmm: 万用表
        Returns:
            {float} -- [description]
        """
        val = 110
        # val = self.getEloadMeasCurr()
        gevent.sleep(0)
        return val

    def measureSelect(self, typ):
        """选择测量的量类型
        Arguments:
            typ {str} -- {Vin|Iin|Vout|Iout}
        Returns:
            {num} -- 返回的是某个类型的测量值
        """
        measVal = 0
        if typ == 'Vout':
            measVal = self.getOutputVolt()
        elif typ == 'Vin':
            measVal = self.getInputVolt()
        elif typ == 'Iout':
            measVal = self.getOutputCurr()
        elif typ == 'Iin':
            measVal = self.getInputCurr()
        return measVal

    def judgeVoltOrCurrRiseToRefVal(self, typ, refval, refcnt, cyclenums,
                                    period):
        """电压或电流上升到给定值的判断
        Arguments:
            typ {str} -- {Vin|Iin|Vout|Iout}
            refval {num} -- 比较用的参考值
            refcnt {int} -- 给定的检测值达到参考值的次数参考值
            cyclenums {int} -- 总的检测循环次数
            period {num} -- 检测时间间隔(s)
        Returns:
            {bool} -- True判断成功；False超时失败
        """
        cnt = 0
        for _ in range(cyclenums):
            measVal = self.measureSelect(typ)
            if measVal >= refval:
                for _ in range(refcnt - 1):
                    measVal = self.measureSelect(typ)
                    if measVal >= refval:
                        cnt += 1
                        sleep(period)
            if cnt >= refcnt:
                return True
            else:
                cnt = 0
            sleep(period)
        else:
            return False

    def judgeVoltOrCurrFallToRefVal(self, typ, refval, refcnt, cyclenums,
                                    period):
        """电压或电流下降到给定值的判断
        Arguments:
            typ {str} -- {Vin|Iin|Vout|Iout}
            refval {num} -- 比较用的参考值
            refcnt {int} -- 检测值达到参考值的次数参考值
            cyclenums {int} -- 总的检测循环次数
            period {num} -- 检测时间间隔(s)
        Returns:
            {bool} -- True判断成功；False超时失败
        """
        cnt = 0
        for _ in range(cyclenums):
            measVal = self.measureSelect(typ)
            if measVal <= refval:
                for _ in range(refcnt - 1):
                    measVal = self.measureSelect(typ)
                    if measVal <= refval:
                        cnt += 1
                        sleep(period)
            if cnt >= refcnt:
                return True
            else:
                cnt = 0
            sleep(period)
        else:
            return False

    def setEloadOnOff(self, onoff):
        """设置电子负载开关
        Arguments:
            onoff onoff {str} -- {OFF|ON}
        """
        self.myEload.set_input(onoff)

    def setEloadCCval(self, curr):
        """设置CC模式下的电流值(A)
        Arguments:
            curr {num} -- 设置CC模式下的电流值(A)
        """
        self.myEload.set_mode('CURR')
        self.myEload.set_current(curr)

    def setEloadCVval(self, volt):
        """设置CV模式下的电压值(V)
        Arguments:
            volt {num} -- 设置CV模式下的电压值(V)
        """
        self.myEload.set_mode('VOLT')
        self.myEload.set_voltage(volt)

    def setEloadCRval(self, res):
        """设置CR模式下的电阻值(Ω)
        Arguments:
            volt {num} -- 设置CR模式下的电阻值(Ω)
        """
        self.myEload.set_mode('RES')
        self.myEload.set_resistance(res)

    def setEloadCPval(self, powe):
        """设置CP模式下的功率值(W)
        Arguments:
            volt {num} -- 设置CP模式下的功率值(W)
        """
        self.myEload.set_mode('POW')
        self.myEload.set_power(powe)

    def setEloadShort(self, onoff):
        """设置CP模式下的功率值(W)
        Arguments:
            volt {num} -- 设置CP模式下的功率值(W)
        """
        self.myEload.set_input_short(onoff)

    def getEloadMeasVolt(self):
        """查询电压平均值(V)
        Returns:
            {float} -- 电压平均值(V)
        """
        val = self.myEload.get_measure_voltage()
        return val

    def getEloadMeasCurr(self):
        """查询电流平均值(A)
        Returns:
            {float} -- 电流平均值(A)
        """
        val = self.myEload.get_measure_current()
        return val

    def setDCPowerOnOff(self, onoff):
        """打开或关闭电源输出
        Arguments:
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.myDCPower.output(onoff)

    def setDCPowerVolt(self, volt):
        """设定电源输出电压(V)
        Arguments:
            volt {num or str} -- 电压值(V)
        """
        self.myDCPower.set_voltage(volt)

    def setDCPowerCurr(self, curr):
        """设定电源输出电流限制(A)
        Arguments:
            curr {num or str} -- 电流值(A)
        """
        self.myDCPower.set_current(curr)

    def getDCPowerMeasVolt(self):
        """检测并返回当前的电压值(V)
        Returns:
            {float} -- [description]
        """
        val = self.myDCPower.get_measure_voltage()
        return val

    def getDCPowerMeasCurr(self):
        """检测并返回当前的电流值(A)
        Returns:
            {float} -- [description]
        """
        val = self.myDCPower.get_measure_current()
        return val

    def setAuxDCPowerOnOff(self, onoff):
        """打开或关闭电源输出
        Arguments:
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.myAuxDCPower.output(onoff)

    def setAuxDCPowerVolt(self, volt):
        """设定电源输出电压(V)
        Arguments:
            volt {num or str} -- 电压值(V)
        """
        self.myAuxDCPower.set_voltage(volt)

    def setAuxDCPowerCurr(self, curr):
        """设定电源输出电流限制(A)
        Arguments:
            curr {num or str} -- 电流值(A)
        """
        self.myAuxDCPower.set_current(curr)

    def getAuxDCPowerMeasVolt(self):
        """检测并返回当前的电压值(V)
        Returns:
            {float} -- [description]
        """
        val = self.myAuxDCPower.get_measure_voltage()
        return val

    def getAuxDCPowerMeasCurr(self):
        """检测并返回当前的电流值(A)
        Returns:
            {float} -- [description]
        """
        val = self.myAuxDCPower.get_measure_current()
        return val

    def setSignalGenOnOff(self, ch, onoff):
        """打开或关闭信号源输出
        Arguments:
            ch {num} -- {0|1}
            onoff {num or str} -- {0|1|OFF|ON}
        """
        self.mySignalGen.set_output(ch, "STAT", onoff)

    def getScopeScreen(self, imgpath, imgname):
        """获取示波器波形
        Arguments:
            imgname {[type]} -- [description]
        """
        imgname = '{0}'.format(datetime.now().strftime('%Y%m%d-%H%M%S') +
                               imgname)
        #########
        imgname = self.myScope.save_image_to_pc(imgpath, imgname)
        #############
        # =HYPERLINK("#"&C3&"!A1",INDIRECT(C3&"!A1"))
        return imgname

    def getAI(self, ch_ranges, nums_per_ch):
        """获取产品板上各电压
        Arguments:
            ch_ranges {int} -- 读取的通道数range(x, xx)
            nums_per_ch {int} -- 每个通道读取的次数
        Returns:
            {list} -- 每个通道读取值的平均值的列表
        """
        if self.ai is not None:
            try:
                with Task() as task:
                    for i in ch_ranges:
                        chnl = '{0}/ai{1}'.format(self.ai["addr"], i)
                        task.ai_channels.add_ai_voltage_chan(
                            chnl, terminal_config=TerminalConfiguration.NRSE)
                    vallist = task.read(nums_per_ch)
                    val_aix = []
                    for i in ch_ranges:
                        val_aix.append(round(sum(vallist[i]) / nums_per_ch, 3))
                # val_aix = [1] * 18
                return val_aix
            except Exception:
                pass

    def setDO(self, line, data):
        """设置数字输出(DO)
        Arguments:
            line {str} -- 板块上的测量的通道范围,最大为0:7
            data {list} -- 数据列表的长度与line的长度相同
        """
        if self.do is not None:
            try:
                with Task() as task:
                    line = '{0}/port0/line{1}'.format(self.do["addr"], line)
                    task.do_channels.add_do_chan(
                        line, line_grouping=LineGrouping.CHAN_PER_LINE)
                    task.write(data)
            except Exception:
                pass

    def uint(self, num, unit='', dot=3):
        rst = ""
        sign = ""
        if num == 0.0:
            return "0.0"
        if num < 0.0:
            sign = "-"
            num = -num
        if num >= 1000000.0:
            rst = str(round(num / 1000000.0, dot)) + "M"
        elif num >= 1000.0:
            rst = str(round(num / 1000.0, dot)) + "k"
        elif num < 0.000000001:
            rst = str(round(num * 1000000000000.0, dot)) + "p"
        elif num < 0.000001:
            rst = str(round(num * 1000000000.0, dot)) + "n"
        elif num < 0.001:
            rst = str(round(num * 1000000.0, dot)) + "u"
        elif num < 1.0:
            rst = str(round(num * 1000.0, dot)) + "m"
        else:
            rst = str(round(num, dot))

        return sign + rst + unit

    def getArgv(self, para, argv):
        try:
            for item in argv[1].split(","):
                try:
                    key = item.split(":")[0]
                    if key in para:
                        if key == "Path":
                            para[key] = item[5:]
                        else:
                            para[key] = eval(numberDecode(item.split(":")[1]))
                except Exception:
                    pass
        except Exception:
            pass


ATS = BriefControl()
