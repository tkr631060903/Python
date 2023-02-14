import requests
import json

import hashlib
import random
from datetime import datetime, timedelta

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import os
from PIL import Image

# ################################腾讯云COS##################################
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
coscfg = CosConfig(
    Region="ap-guangzhou",
    SecretId="AKIDwy64qcovvNfmiSkyRjx6FNZrCOPnCd9E",
    SecretKey="560qlaE7h7LOFxTyRSDnCPSSVW8Xqyvy")
# 文件对象桶
bucket = 'ate-1258162491'


def imgUpload(path):
    # 判断文件是否存在
    if os.path.isfile(path):
        #  获取客户端对象
        client = CosS3Client(coscfg)
        # 获取文件名
        file_name = os.path.basename(path)
        client.upload_file(
            Bucket=bucket,
            LocalFilePath=path,
            Key=file_name,
            PartSize=10,
            MAXThread=10)
        url = client.get_presigned_download_url(
            Bucket=bucket,
            Key=file_name,
        )
        img = Image.open(path)
        result = json.dumps({
            "name": file_name,
            "md5": hashlib.md5(img.tobytes()).hexdigest(),
            "url": url,
            "ext": img.format,
            "w": img.size[0],
            "h": img.size[1],
            "size": os.path.getsize(path)
        })
        return result
    else:
        raise RuntimeError('不存在文件')


# ################################腾讯云COS##################################


# ################################网易云信##################################
class CheckSumHeader(object):
    """
    生成一个用来给requests库用的头，携带网易云信需要的checksum函数
    """
    _Content_Type = "application/x-www-form-urlencoded;charset=utf-8"
    _str_num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, app_key, app_secret):
        self.App_key = app_key
        self.app_secret = app_secret
        self.curtime = self.get_CurTime()
        self.Nonce = self.get_random_num_str(30)

    def check_period(self, curtime):
        """
        检查checksum是否过期
        :return: True or False
        """
        five_min = timedelta(seconds=250)
        now = datetime.utcnow()
        if now - datetime.fromtimestamp(float(curtime)) > five_min:
            return False
        else:
            return True

    def update_curtime(self):
        """
        检查curtime参数是否过期
        :return:curtime
        """
        if not self.check_period(self.curtime):
            self.curtime = self.get_CurTime()
        return self.curtime

    def get_random_num_str(self, num):
        """
        获取一个随机数字符串
        :param num: 字符串长度
        :return: 随机字符串
        """
        nonce = ""
        for x in range(num):
            nonce += self._str_num_list[random.randint(0, 9)]
        self.Nonce = nonce
        return nonce

    @staticmethod
    def str_encrypt(str):
        """
        使用sha1加密算法，返回str加密后的字符串
        """
        sha = hashlib.sha1(str)
        encrypts = sha.hexdigest()
        return encrypts

    @staticmethod
    def get_CurTime():
        """
        获取当前时间戳的字符串形式
        :return:
        """
        return str(int(datetime.now().timestamp()))

    def get_checksum_headers(self):
        """
        获取带checksum，AppKey，Nonce，CurTime的头部字典
        :return:
        """
        CheckSum = self.str_encrypt((self.app_secret + self.Nonce +
                                     self.update_curtime()).encode('utf8'))
        return {
            "AppKey": self.App_key,
            "Nonce": self.Nonce,
            "CurTime": self.curtime,
            "CheckSum": CheckSum,
            "Content-Type": self._Content_Type
        }


# ################################网易云信##################################


class IMMsg():
    def __init__(self, cfg):
        self.cfg = cfg

    def sendMsg(
            self,
            _body,
            _type=0,
            _from='Minieye-HW',
            _to='nxn',
    ):
        self.header_seter = CheckSumHeader("6f1836cf3ee89dc87d643ee5049e2c4e",
                                           "bf63646565c7")
        self.header = self.header_seter.get_checksum_headers()
        url = "https://api.netease.im/nimserver/msg/sendMsg.action"
        data = {
            "from": _from,
            "ope": 0,
            "to": _to,
            "type": _type,
            "body": _body
        }
        try_f = True
        try_cnt = 0
        while try_f:
            resp = requests.post(url=url, headers=self.header, data=data)
            try_cnt += 1
            if resp["status_code"] is 200 or try_cnt is 3:
                try_f = False
            else:
                print("*************************失败了", try_cnt)

        # return resp.json()

    def send(self, message):
        msgbody = []
        if type(message["msg"]) is str:
            msgbody.append(message["msg"])
        else:
            msgbody = message["msg"]
        # 遍历消息通知配置
        for item in self.cfg:
            try:
                # 配置的消息通知类型包含传入的消息类型
                if item["action"].find(message["action"]) >= 0:
                    # 遍历消息
                    for msg in msgbody:
                        try:
                            # 消息数量无限制或未达到最大值
                            if item["max"] == -1 or item["cnt"] < item["max"]:
                                # 消息是否为文件
                                if os.path.isfile(msg):
                                    # 图片消息数量无限制或未达到最大值
                                    if item["max_img"] == -1 or item[
                                            "cnt_img"] < item["max_img"]:
                                        # 指定用户发送消息
                                        self.sendMsg(
                                            imgUpload(msg),
                                            _type=1,
                                            _to=item["usr"])
                                        item["cnt"] += 1
                                        item["cnt_img"] += 1
                                        item["cnt"] += 1
                                        item["cnt_img"] += 1
                                # 非文件消息,消息长度判断
                                elif len(msg) > 1:
                                    # 指定用户发送消息
                                    self.sendMsg(
                                        json.dumps({
                                            "msg": msg
                                        }),
                                        _to=item["usr"])
                                    item["cnt"] += 1
                        except Exception:
                            pass
            except Exception:
                pass


if __name__ == '__main__':
    pass
