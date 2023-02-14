import pyvisa
import configparser
from os import path


class VISAInfo(object):
    """
    Arguments:
        addr {str} -- 通讯参数
    """
    def __init__(self, serial=False):
        # 获取当前文件路径
        self.thisfiledir = path.abspath(path.join(path.abspath(path.dirname(__file__))))

        rm = pyvisa.ResourceManager()
        self.rc = {}
        for addr in rm.list_resources():
            if not serial:
                if addr.find("ASRL") == 0:
                    continue
                pass
            self.rc[addr] = self.getInstrument(rm, addr)

    def getInstrument(self, rm, addr):
        # 打开本地设置
        config = self.openConfig()
        addr_s = addr.replace("::", "_")
        if not config.has_option("VISA", addr_s):
            try:
                inst = rm.open_resource(addr)
                inst.timeout = 200
                info = ""
                i = 0
                # 尝试获取设备信息
                while info == "" and i < 3:
                    info = inst.query("*IDN?")
                    i += 1
                config.set("VISA", addr_s, info)
                config.write(open(self.thisfiledir + "\\visa.ini", "w"))
                print("更新本地设备地址列表", addr, info)
            except Exception:
                pass
        # 获取本地设置中设备地址并返回
        if config.has_option("VISA", addr_s):
            return config.get("VISA", addr_s)
        else:
            return None

    def openConfig(self):
        # 打开本地设置
        config = configparser.ConfigParser()
        config.read(self.thisfiledir + "\\visa.ini", encoding="utf-8")
        # 校验是否存在设置项,不存在则添加
        if not config.has_section("VISA"):
            config.add_section("VISA")
        return config


if __name__ == "__main__":
    dev = VISAInfo()
    print(dev.rc)
