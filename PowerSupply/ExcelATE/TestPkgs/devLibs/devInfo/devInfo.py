import configparser
from os import environ


class devInfo(object):
    """
    Arguments:
        addr {str} -- 通讯参数
    """

    def __init__(self):
        # 获取当前文件路径
        self.path = environ['tmp']

    def openConfig(self, instrument):
        # 打开本地设置
        config = configparser.ConfigParser()
        config.read(self.path + "\\dev.ini", encoding="utf-8")
        # 校验是否存在设置项,不存在则添加
        if not config.has_section(instrument):
            config.add_section(instrument)
        if not config.has_option(instrument, 'addr'):
            config.set(instrument, "addr", "")
        return config

    def getAddr(self, instrument):
        # 打开本地设置
        config = self.openConfig(instrument)
        # 获取本地设置中设备地址并返回
        return config.get(instrument, "addr")

    def setAddr(self, instrument, addr):
        # 打开本地设置
        config = self.openConfig(instrument)
        # 获取本地设置中设备地址
        addr_r = config.get(instrument, "addr")
        # 本地设置中设备地址需要更新
        if addr_r != addr:
            # 更新设置
            config.set(instrument, "addr", addr)
            # 写入设置
            config.write(open(self.path + "\\dev.ini", "w", encoding="utf-8"))
            print("更新本地设备地址列表", instrument, addr)


if __name__ == "__main__":
    pass
