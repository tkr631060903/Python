# coding: utf-8
import sys
from corelib.autolib import ATS
import plotly
import plotly.graph_objs as go
from time import clock
from datetime import datetime


class AutoTest():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.meas_out = [""]

        self.u_wkmode = {
            'Vin': 28,  # 直流电源电压设置
            'Iin': 2,
            'Iout': 0,
            'Path': "E:/Workspace/Software/ExcelATE",
        }
        ATS.getArgv(self.u_wkmode, sys.argv)
        print("[process]" + "@输入电压:" + str(self.u_wkmode['Vin']) + "V 限制电流:" +
              str(self.u_wkmode['Iin']) + "A")

    def U_InitDevices(self):
        """仪器设备初始化
        """
        # @USER: 根据测试方法调用仪器设备控制函数进行初始设置
        try:
            ATS.setDCPowerOnOff('OFF')
            i = 0
            stclk = clock()
            while clock() - stclk < 30:
                if clock() - stclk > i:
                    i += 1
                    print(
                        '\u001b[0K' + "[process]" + "预计" + str(int(30 - i)) +
                        "S后开始测试",
                        end='\r')
            # ATS.setEloadOnOff('ON')
        except Exception as err:
            print("[process] init error:" + str(err))

    def U_SetStatus(self, mode=None):
        """设置其他工作条件
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 设置其他工作条件，如改变设备状态，加入延时等等
        # ATS.setNI9472DO('0:5', [True] + [False]*4 + [True])
        try:
            ATS.setDCPowerVolt(self.u_wkmode['Vin'])
            ATS.setDCPowerCurr(self.u_wkmode['Iin'])

        except Exception as err:
            print("[process] set status error:" + str(err))

    def U_GetDatas(self, mode=None):
        """获取测试数据；主要是从仪器设备里面读取；根据测试用例实际想要检测的量进行
        Arguments:
            i {int} -- 第i种工况
        """
        # @USER: 对想要获取的量进行检测操作(多个函数检测用协程)
        try:
            ATS.setDCPowerOnOff('ON')
            stclk = clock()
            i = 0.0
            j = 0.0
            cur = []
            val = []
            xalias = []
            # while clock()-stclk < 300:
            #     if ATS.getDCPowerMeasVolt() > self.u_wkmode['Vin']*0.9:
            #         break
            # self.meas_out[1] = str(round(clock()-stclk,3))
            while clock() - stclk < 60:
                j += 1
                val.append(ATS.getDCPowerMeasVolt())
                cur.append(ATS.getDCPowerMeasCurr())
                xalias.append(j)
                if clock() - stclk > i:
                    print(
                        '\u001b[0K' + "[process]" + "当前限制电流:" + str(
                            round(self.u_wkmode['Iin'], 3)) + "A 预计" + str(
                                int(60 - i)) + "S后完成",
                        end='\r')
                    i += 1
            for index in range(len(xalias)):
                xalias[index] = round(xalias[index] * (60 / j), 3)
            ATS.setDCPowerOnOff('OFF')
            html_name = datetime.now().strftime('%Y%m%d-%H%M%S') + '-极性反接'
            trace1 = go.Scatter(x=xalias, y=val, mode='lines', name='电压')
            trace2 = go.Scatter(
                x=xalias, y=cur, mode='lines', name='电流', yaxis='y2')
            data = [trace1, trace2]
            layout = go.Layout(
                title=html_name,
                yaxis=dict(title="电压(V)"),
                yaxis2=dict(
                    title="电流(A)",
                    # tickfont=dict(
                    #     color='rgb(148, 103, 189)'
                    # ),
                    overlaying='y',
                    side='right'))
            fig = go.Figure(data=data, layout=layout)

            plotly.offline.plot(
                fig,
                auto_open=False,
                filename=self.u_wkmode['Path'] + '/Html/' + html_name +
                '.html')
            self.meas_out[0] = html_name + '.html'
        except Exception as err:
            print("[process] get data error:" + str(err))


if __name__ == "__main__":
    use_devices = ['直流电源']
    ate = AutoTest()
    ATS.connect_devices(use_devices)
    ate.U_InitDevices()
    ate.U_SetStatus()
    ate.U_GetDatas()
    ATS.delete_devices(use_devices)
    print("meas_out", ate.meas_out)
