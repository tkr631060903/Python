# from nidaqmx.system import System
# from devLibs.can.zlgcan import CANX
import sys
import os

sys.path.append(os.path.realpath("."))
from corelib.VISAInfo import VISAInfo
from devLibs.dcpower.itech6700 import DCPowerX
from devLibs.eload.itechframe import EloadX
from devLibs.scope.scope import ScopeX
from devLibs.lcr.lcr import LCRX
from devLibs.dmm.dmm import DMMX
# from devLibs.signalgenerator.dg1000z import SignalGen
from devLibs.signalgenerator.FeelTech import SignalGen
from devLibs.Craft.Craft import CRAFT
from time import sleep


class DevicesClass(object):
    def __init__(self):
        self.dev_update()
        self.dev_dict = {
            "辅助电源": {
                "hand": None,
                "func": DCPowerX
            },
            "直流电源": {
                "hand": None,
                "func": DCPowerX
            },
            "示波器": {
                "hand": None,
                "func": ScopeX
            },
            "万用表": {
                "hand": None,
                "func": DMMX
            },
            "LCR": {
                "hand": None,
                "func": LCRX
            },
            "电子负载": {
                "hand": None,
                "func": EloadX
            },
            "信号源": {
                "hand": None,
                "func": SignalGen
            },
            "CRAFT": {
                "hand": None,
                "func": CRAFT
            },
        }

    def dev_Create(self, device):
        inst = None
        sel = 0
        dev_name = device.split(":")[0]
        try:
            try:
                inst = device.split(":")[1]
                try:
                    inst = eval(inst)
                except Exception:
                    pass
                try:
                    sel = device.split(":")[2]
                except Exception:
                    pass
            except Exception:
                pass
            if self.dev_dict[dev_name]["hand"] is not None:
                self.dev_dict[dev_name]["hand"].close()
            for i in range(3):
                try:
                    self.dev_dict[dev_name]["hand"] = self.dev_dict[dev_name][
                        "func"](self.rc, inst, sel)
                    print(dev_name + '实例创建')
                    break
                except Exception as err:
                    print(dev_name + '连接错误' + str(err))
            if self.dev_dict[dev_name]["hand"] is None:
                print(dev_name + '连接错误')
                raise RuntimeError(dev_name + '连接错误')

        except Exception as err:
            print(dev_name + '连接错误', err)
            raise RuntimeError(dev_name + '连接错误')

    def dev_update(self):
        dev = VISAInfo()
        self.rc = {}
        for item in dev.rc:
            if dev.rc[item] is not None:
                self.rc[item] = dev.rc[item]

    def connect_devices(self, use_devices):
        """连接设备
        """
        try:
            for item in use_devices:
                self.dev_Create(item)
            self.myAuxDCPower = self.dev_dict["辅助电源"]["hand"]
            self.myDCPower = self.dev_dict["直流电源"]["hand"]
            self.myScope = self.dev_dict["示波器"]["hand"]
            self.myDMM = self.dev_dict["万用表"]["hand"]
            self.myLCR = self.dev_dict["LCR"]["hand"]
            self.myEload = self.dev_dict["电子负载"]["hand"]
            self.mySignalGen = self.dev_dict["信号源"]["hand"]
            self.myCraft = self.dev_dict["CRAFT"]["hand"]

        except Exception as err:
            print("[process]" + str(err))
            raise RuntimeError(err)
            # os._exit(0)

    def delete_devices(self, use_devices):
        """关闭并删除硬件设备实例
        """
        for item in use_devices:
            dev = item.split(":")[0]
            try:
                del self.dev_dict[dev]["hand"]
                print(dev, '实例删除')
            except Exception as err:
                print("[process]", dev, err)
