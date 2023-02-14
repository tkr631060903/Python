from time import sleep
from corelib.autolib import ATS
from corelib.config import Config


class Capture():
    """电压测试类
    Arguments:
        object {[type]} --
    """

    def __init__(self, scope):
        self.out = [""] * 11
        # 示波器实例
        self.scope = scope
        # 获取示波器捕获配置
        config = Config()
        self.cfg = config.getCfgScope()
        # 清空示波器测量
        self.scope.set_measure_clear()
        # 遍历示波器配置
        for item in self.cfg:
            if item["type"] is not None:
                # 添加示波器测量
                self.scope.add_measure(item["ch"], item["type"])

    def tryCapture(self, path):
        imagename = ""
        action = ""
        try:
            # 停止示波器,方便参数读取
            self.scope.set_stop()
            # 延时,等待示波器测量结果稳定
            sleep(2)
            err = ""
            # 遍历示波器配置
            for item in self.cfg:
                if item["type"] is not None:
                    if item["fun"] is not None:
                        i = 0
                        for fun_t in item["fun"].split(","):
                            try:
                                if str(item["spec"]).split(",")[i] is not None:
                                    # 获取示波器测量结果
                                    float_tmp = self.scope.get_measure_val(
                                        item["ch"], item["type"])
                                    # 拼接测量结果判断函数字符串(结果+方法+规格)
                                    func = "(" + str(float_tmp) + fun_t + str(
                                        item["spec"]).split(",")[i] + ")"
                                    # 执行判断函数字符串
                                    if eval(func):
                                        # 捕获到异常,进行示波器截图
                                        imagename = ATS.getScopeScreen(
                                            path + '/Image', "-异常波形")
                                        # 捕获次数累加
                                        item["err_cnt"] += 1
                                        # 捕获后动作
                                        if item["stop"]:
                                            action = "终止"
                                        elif action is "":
                                            action = "异常"
                                        # 添加本次捕获的错误信息 (备注+捕获到异常+判断函数)
                                        err += (item["note"] + "捕获到异常" + func +
                                                "\n")
                            except Exception as err:
                                print(str(err))
                                pass
                            finally:
                                i += 1

            # 更新错误累计输出
            for i in range(len(self.cfg)):
                if self.cfg[i]["id"] == i:
                    self.out[i + 3] = self.cfg[i]["err_cnt"]
            # 输出捕获后动作
            self.out[0] = action
            # 添加错误信息开头
            str_tmp = ""
            if action is not "":
                str_tmp = "测试" + action + "!\n"
            # 输出错误信息
            self.out[1] = str_tmp + err[:-1]
            # 输出捕获图片名称
            self.out[2] = imagename
        except Exception as err:
            print("[err] get data error:" + str(err))
        return self.out


if __name__ == "__main__":
    pass
