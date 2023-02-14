from os import path
import os
import json
import re
import serial

thisfiledir = path.join(path.abspath(path.dirname(__file__)))
# 示波器可测量类型
type_dict = {
    "频率": "FREQ",
    "周期": "PERI",
    "上升时间": "RIS",
    "下降时间": "FALL",
    "峰峰值": 'VPP',
    "幅值": "AMP",
    "最大值": "MAX",
    "最小值": "MINI",
    "": None
}


# 单位转换
def numberDecode(num):
    # 千
    str_temp = num.replace("k", "*1000")
    str_temp = str_temp.replace("K", "*1000")
    # 毫
    str_temp = str_temp.replace("m", "/1000")
    # 微
    str_temp = str_temp.replace("u", "/1000000")
    # 兆
    str_temp = str_temp.replace("M", "*1000000")
    # 删除所有英文字符
    str_temp = re.sub(r'[A-Za-z]+', "", str_temp)
    return str_temp


class Config():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self):
        self.scope = []
        self.msg = []
        self.serial = []
        cfg = None
        try:
            # 打开配置文件
            with open(path.join(os.environ['tmp'], 'suite.json'),
                      'r',
                      encoding='UTF-8') as f:
                # 加载配置
                cfg = json.loads(f.read())
        except Exception:
            pass
        if cfg is not None:
            try:
                suite = cfg["波形捕获"]
                for i in range(len(suite)):
                    # print(suite[i]["通道"], suite[i]["测量类型"], suite[i]["捕获方法"],
                    #       suite[i]["捕获规格"], suite[i]["备注"])
                    if suite[i]["通道"] is not None:
                        if suite[i]["测量类型"] is not None:
                            if suite[i]["通道"].find("CH") == 0:
                                try:
                                    stop = False
                                    if suite[i]["捕获后动作"] is not None:
                                        if suite[i]["捕获后动作"] == "终止":
                                            stop = True
                                    self.scope.append({
                                        "id":
                                        i,
                                        "ch":
                                        int(suite[i]["通道"].split("CH")[1]),
                                        "type":
                                        type_dict[str(suite[i]["测量类型"])],
                                        "fun":
                                        suite[i]["捕获方法"],
                                        "stop":
                                        stop,
                                        "spec":
                                        eval(numberDecode(suite[i]["捕获规格"])),
                                        "note":
                                        suite[i]["备注"],
                                        "err_cnt":
                                        0
                                    })
                                except Exception as err:
                                    print("[process] get config error:" +
                                          str(err))
            except Exception:
                pass
            try:
                suite = cfg["消息通知"]
                for i in range(len(suite)):
                    # print(suite[i]["用户"], suite[i]["最大图片数量"],
                    #       suite[i]["最大消息数量"])
                    if suite[i]["用户"] is not None:
                        if suite[i]["最大消息数量"] is None:
                            max_all = -1
                        else:
                            max_all = suite[i]["最大消息数量"]
                        if suite[i]["最大图片数量"] is None:
                            max_img = -1
                        else:
                            max_img = suite[i]["最大图片数量"]
                        try:
                            self.msg.append({
                                "id": i,
                                "usr": suite[i]["用户"],
                                "max": max_all,
                                "cnt": 0,
                                "action": suite[i]["消息通知类型"],
                                "max_img": max_img,
                                "cnt_img": 0
                            })
                        except Exception as err:
                            print("[process] get config error:" + str(err))
            except Exception:
                pass
            try:
                suite = cfg["串口监控"]
                for i in range(len(suite)):
                    # print(suite[i]["COM"], suite[i]["关键字"], suite[i]["错误关键字"],
                    #       suite[i]["备注"])
                    if suite[i]["COM"] is not None:
                        if suite[i]["COM"].find("COM") == 0:
                            try:
                                ser = serial.Serial(suite[i]["COM"],
                                                    115200,
                                                    timeout=1)
                                ser_aux = None
                                try:
                                    if suite[i]["辅助串口"].find("COM") == 0:
                                        ser_aux = serial.Serial(
                                            suite[i]["辅助串口"],
                                            115200,
                                            timeout=1)
                                except Exception:
                                    pass

                                if ser is not None:
                                    self.serial.append({
                                        "id":
                                        i,
                                        "ser":
                                        ser,
                                        "key":
                                        suite[i]["关键字"],
                                        "key_err":
                                        suite[i]["错误关键字"],
                                        "ser_aux":
                                        ser_aux,
                                        "note":
                                        suite[i]["备注"],
                                        "log":
                                        "",
                                        "log_aux":
                                        "",
                                        "result":
                                        "",
                                        "err_cnt":
                                        0
                                    })
                            except Exception as err:
                                print("[process] get config error:" + str(err))
                                os._exit(0)
            except Exception:
                pass

    def getCfgSerial(self):
        return self.serial

    def getCfgMsg(self):
        return self.msg

    def getCfgScope(self):
        return self.scope


if __name__ == "__main__":
    cfg = Config()
    print(cfg.getCfgSerial())
    print(cfg.getCfgMsg())
    print(cfg.getCfgScope())
