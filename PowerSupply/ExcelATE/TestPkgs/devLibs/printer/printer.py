import ctypes
from PIL import Image, ImageDraw, ImageFont
import base64
import io
from io import BytesIO
import copy
from os import path
import csv

thisfiledir = path.join(path.abspath(path.dirname(__file__)))


class Draw:
    def __init__(self):
        pass

    def text_center(self, draw, pos, text, font, gap=False, fill=0):
        """居中打印文本框        
        """
        if len(pos) < 4:
            return
        # 最小预留间隙
        if gap:
            width_min = draw.textsize("W", font)[0]            
        else:
            width_min = 0
        for i in range(len(text) + 1):
            width = draw.textsize(text[0:i], font)[0]
            if width > pos[2] - pos[0] - width_min:
                # 截取未超出文本框的打印内容
                text = text[0:i - 1]
                break
        # 获取文本内容的宽度和高度
        width, height = draw.textsize(text, font)
        if width > pos[2] - pos[0]:
            width = pos[2] - pos[0]
        if height > pos[3] - pos[1]:
            height = pos[3] - pos[1]
        # 计算文本居中打印的坐标
        x = (int)(pos[2] + pos[0] - width) // 2
        y = (int)(pos[3] + pos[1] - height) // 2
        # 打印文本内同
        draw.text((x, y), text, fill, font=font)
        # 返回实际打印的内容
        return text

    def text_left(self, draw, pos, text, font, fill=0):
        """靠左打印文本框        
        """
        if len(pos) < 4:
            return
        # 最小预留间隙
        width_min = draw.textsize("W", font)[0]
        # 获取文本内容的宽度和高度
        width, height = draw.textsize(text, font)
        if width > pos[2] - pos[0]:
            width = pos[2] - pos[0]
        if height > pos[3] - pos[1]:
            height = pos[3] - pos[1]
        # 计算文本居中靠左打印的坐标
        x = pos[0] + width_min // 2
        y = (int)(pos[3] + pos[1] - height) // 2
        # 打印文本内同
        draw.text((x, y), text, fill, font=font)
        # 返回实际打印的内容
        return text

    def text_label_center(self,
                          draw,
                          pos,
                          text,
                          font,
                          line=2,
                          fill=0):
        """居中打印文本框        
        """
        if len(pos) < 4:
            return
        # 获取打印宽度
        width = draw.textsize(text, font)[0]
        if width < pos[2] - pos[0]:
            # 直接单行打印
            self.text_center(draw, pos, text, font)
        # 打印行数为2
        elif line == 2:
            width = draw.textsize(text, font)[0]
            width1 = width//2
            if width1 > pos[2] - pos[0]:
                # 第一行长度为总长度减去文本框长度
                width1 = pos[2] - pos[0]
            for i in range(len(text) + 1):
                width = draw.textsize(text[0:i], font)[0]
                if width > width1:
                    # 截取第一行打印的内容
                    text1 = text[0:i - 1]
                    break
            # 打印第一行,并更新为实际打印内容
            text1 = self.text_center(draw, (pos[0], pos[1], pos[2], pos[1] +
                                            (pos[3] - pos[1]) // 2), text1,
                                     font)
            # 打印第二行,内容为除去第一行的内容
            self.text_center(draw, (pos[0], pos[1] +
                                    (pos[3] - pos[1]) // 2, pos[2], pos[3]),
                             text.replace(text1, ""), font)

    def text_multi_center(self,
                          draw,
                          pos,
                          text,
                          font,
                          line=2,
                          gap=True,
                          fill=0):
        """居中打印文本框        
        """
        if len(pos) < 4:
            return
        # 最小预留间隙
        width_min = draw.textsize("W", font)[0]
        # 获取打印宽度
        width = draw.textsize(text, font)[0]
        # 单行可以打印完成
        if gap:
            if width < pos[2] - pos[0] - width_min * 2:
                # 直接单行打印
                self.text_center(draw, pos, text, font)
        elif width < pos[2] - pos[0]:
            # 直接单行打印
            self.text_center(draw, pos, text, font)
        # 打印行数为2
        elif line == 2:
            width = draw.textsize(text, font)[0]
            # 第二行默认为总长度的60%
            width2 = (int)(width * 0.6)
            # 第二行没有超出文本框
            if width2 < pos[2] - pos[0] - width_min:
                width1 = width - width2
            else:
                # 第一行长度为总长度减去文本框长度
                width1 = width - (pos[2] - pos[0] - width_min)
                if width1 > pos[2] - pos[0] - width_min:
                    # 第一行也不能超出文本框
                    width1 = pos[2] - pos[0] - width_min
            for i in range(len(text) + 1):
                width = draw.textsize(text[0:i], font)[0]
                if width > width1:
                    # 截取第一行打印的内容
                    text1 = text[0:i - 1]
                    break
            # 打印第一行,并更新为实际打印内容
            text1 = self.text_center(draw, (pos[0], pos[1], pos[2], pos[1] +
                                            (pos[3] - pos[1]) // 2), text1,
                                     font, gap)
            # 打印第二行,内容为除去第一行的内容
            self.text_center(draw, (pos[0], pos[1] +
                                    (pos[3] - pos[1]) // 2, pos[2], pos[3]),
                             text.replace(text1, ""), font, gap)

    def bmp_center(self, img, pos, bmp):
        """居中图片       
        """
        if len(pos) < 4:
            return
        bmp = Image.open(bmp)
        width, height = bmp.size
        if width > pos[2] - pos[0]:
            width = pos[2] - pos[0]
        if height > pos[3] - pos[1]:
            height = pos[3] - pos[1]
        x = (int)(pos[2] + pos[0] - width) // 2
        y = (int)(pos[3] + pos[1] - height) // 2
        img.paste(bmp, (x, y))

    def rectangle(self, draw, pos, width, fill=0):
        """打印矩形       
        """
        if len(pos) < 4:
            return
        oftx = width / 2 - 1 + pos[0]
        ofty = width / 2 + 1 + pos[1]

        draw.line((oftx, pos[1], oftx, pos[3]), fill=fill, width=width)
        draw.line((pos[2] - ofty, pos[1], pos[2] - ofty, pos[3]),
                  fill=fill,
                  width=width)
        draw.line((pos[0], oftx, pos[2], oftx), fill=fill, width=width)
        draw.line((pos[0], pos[3] - ofty, pos[2], pos[3] - ofty),
                  fill=fill,
                  width=width)


class PrintImage:
    def __init__(self, size, frame=False):
        self.img = Image.new("1", size, "white")
        self.dr = ImageDraw.Draw(self.img)
        self.draw = Draw()
        if frame:
            self.draw.rectangle(self.dr, (0, 0, size[0], size[1]), 4)

    def block_label(self, label):
        font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\MSYH.TTC", 34, index=1)
        try:
            self.draw.text_label_center(self.dr, (0, 0, 130, self.img.height),
                                        label[0], font, 2)
            self.draw.text_label_center(self.dr,
                                        (145, 0, 380, self.img.height),
                                        label[1], font, 2)
            self.draw.text_label_center(self.dr,
                                        (405, 0, 640, self.img.height),
                                        label[2], font, 2)
        except Exception:
            pass
        return self.img

    def materials_lable(self, args, mode=0):
        font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\MSYH.TTC", 34, index=1)
        fontnum = ImageFont.truetype("C:\\WINDOWS\\Fonts\\MSYH.TTC", 28)
        self.draw.rectangle(self.dr, (0, 0, 560, 310), 4)
        if mode == 0:
            for i in range(1, 7):
                if i != 4:
                    self.dr.line((0, 44 * i + 2, 560, 44 * i + 2),
                                 fill=0,
                                 width=2)

            self.dr.line((150, 48, 150, 310), fill=0, width=2)

            self.draw.text_center(self.dr, (0, 2, 560, 44 * 1), "深圳佑驾创新科技有限公司",
                                  font)
            self.draw.text_center(self.dr, (4, 44 * 1, 150, 44 * 2), "料号",
                                  font)
            self.draw.text_center(self.dr, (4, 44 * 2, 150, 44 * 3), "品牌",
                                  font)
            self.draw.text_center(self.dr, (4, 44 * 3, 150, 44 * 5), "物料描述",
                                  font)
            self.draw.text_center(self.dr, (4, 44 * 5, 150, 44 * 6), "数量",
                                  font)
            self.draw.text_center(self.dr, (4, 44 * 6, 150, 44 * 7), "送货日期",
                                  font)
            try:
                # 料号
                self.draw.text_center(self.dr, (150, 44 * 1, 560, 44 * 2),
                                      args[0], fontnum)
                # 品牌
                self.draw.text_center(self.dr, (150, 44 * 2, 560, 44 * 3),
                                      args[1], fontnum)
                # 数量
                self.draw.text_center(self.dr, (150, 44 * 5, 560, 44 * 6),
                                      args[3], fontnum)
                # 送货日期
                self.draw.text_center(self.dr, (150, 44 * 6, 560, 44 * 7),
                                      args[4], fontnum)
                # 物料描述
                self.draw.text_multi_center(self.dr,
                                            (150, 44 * 3, 560, 44 * 5),
                                            args[2], fontnum, 2)
            except Exception:
                pass
        elif mode == 1:
            self.draw.bmp_center(self.img, (82, 44 * 4 + 4, 279, 44 * 5),
                                 path.join(thisfiledir, "sign1.bmp"))
            self.draw.bmp_center(self.img, (82, 44 * 5 + 4, 279, 44 * 6),
                                 path.join(thisfiledir, "sign2.bmp"))
            self.draw.bmp_center(self.img, (281, 44 * 4 + 4, 410, 44 * 5),
                                 path.join(thisfiledir, "ok1.bmp"))
            self.draw.bmp_center(self.img, (281, 44 * 5 + 4, 410, 44 * 6),
                                 path.join(thisfiledir, "ok2.bmp"))
            self.draw.bmp_center(self.img, (442, 44 * 6 + 4, 560, 44 * 7),
                                 path.join(thisfiledir, "sign3.bmp"))
            self.draw.rectangle(self.dr, (0, 0, 560, 310), 4)
            for i in range(1, 7):
                self.dr.line((0, 44 * i + 2, 560, 44 * i + 2), fill=0, width=2)

            self.draw.text_center(self.dr, (0, 2, 560, 44 * 1), "封样标签", font)
            self.dr.text((8, 44), "料号:", 0, font=font)
            self.draw.text_center(self.dr, (288, 44 * 1, 412, 44 * 2), "供应商:",
                                  font)
            self.dr.line((279, 46, 279, 44 * 2 + 2), fill=0, width=2)
            self.dr.text((8, 44 * 2), "名称:", 0, font=font)
            self.dr.line((80, 44 * 3 + 2, 80, 44 * 6 + 2), fill=0, width=2)
            self.dr.line((279, 44 * 3 + 2, 279, 310), fill=0, width=2)
            self.dr.line((410, 44 * 3 + 2, 410, 44 * 6 + 2), fill=0, width=2)
            self.dr.text((8, 44 * 3), "部门", 0, font=font)
            self.draw.text_center(self.dr, (80, 44 * 3, 279, 44 * 4), "签样人",
                                  font)
            self.draw.text_center(self.dr, (279, 44 * 3, 410, 44 * 4), "意见",
                                  font)
            self.draw.text_center(self.dr, (410, 44 * 3, 556, 44 * 4), "日期",
                                  font)
            self.dr.text((8, 44 * 4), "研发", 0, font=font)
            self.dr.text((8, 44 * 5), "项目", 0, font=font)
            self.dr.text((8, 44 * 6), "存放区:", 0, font=font)
            self.dr.text((288, 44 * 6), "品管审核:", 0, font=font)
            try:
                self.draw.text_left(self.dr, (80, 44 * 1, 288, 44 * 2),
                                    args[0], fontnum)
                self.draw.text_left(self.dr, (400, 44 * 1, 556, 44 * 2),
                                    args[1], fontnum)
                self.draw.text_left(self.dr, (80, 44 * 2, 556, 44 * 3),
                                    args[2], fontnum)
                self.draw.text_center(self.dr, (412, 44 * 4, 556, 44 * 5),
                                      args[3], fontnum)
                self.draw.text_center(self.dr, (412, 44 * 5, 556, 44 * 6),
                                      args[3], fontnum)
            except Exception:
                pass
        return self.img


class TSCPrinter:
    def __init__(self, portx='', baudratex=9600):
        from os import path
        self.draw = Draw()
        thisfiledir = path.dirname(path.abspath(__file__))
        dllpath = path.join(thisfiledir, 'libs', 'TSCLIB.dll')
        print(dllpath)
        self.tsc = ctypes.WinDLL(dllpath)
        print(self.tsc.usbprintername())
        print(self.tsc.usbprinterserial())
        print(self.tsc.usbportqueryprinter())
        self.tsc.openport(b'USB')

    def close(self):
        """关闭打印机通讯
        Returns:
            [type] -- [description]
        """
        # return self.tsc.closeport()

    def send_data_printer(self, cmdstr):
        """向打印机发送数据命令
        Arguments:
            cmdstr {str} -- 字符串命令
        Returns:
            {bool} -- True or False
        """
        try:
            if type(cmdstr) is bytes:
                # print(cmdstr)
                res = self.tsc.sendBinaryData(cmdstr, len(cmdstr))
            else:
                # print(cmdstr.encode('GBK'))
                res = self.tsc.sendcommand(cmdstr.encode('GBK'))
            if res == len(cmdstr):
                return True
            else:
                return False
        except Exception as err:
            print('[error]', err)
            return False

    def printer_prepare(self):
        """打印准备
        Returns:
            {bool} -- True or False
        """
        res = []
        try:
            res.append(self.send_data_printer('SIZE 50 mm, 30 mm\n'))
            res.append(self.send_data_printer('GAP 2 mm,0\n'))
            res.append(self.send_data_printer('DIRECTION 1\n'))
            res.append(self.send_data_printer('OFFSET 0 mm\n'))
            res.append(self.send_data_printer('DENSITY 15\n'))
            res.append(self.send_data_printer('CODEPAGE 936\n'))
            res.append(self.send_data_printer('CLS\n'))
            if False not in res:
                return True
            else:
                return False
        except Exception as err:
            print('[error]', err)
            return False

    def print_excute(self):
        """打印执行
        Returns:
            {bool} -- True or False
        """
        res = self.send_data_printer('PRINT 1, 1\n')
        return res

    def print_bmp(self, bmp=''):
        """打印位图
        Keyword Arguments:
            index {int} -- [description] (default: {0})
            label {str} -- [description] (default: {''})
        """
        self.printer_prepare()
        print(type(bmp))
        # print(bmp)
        imgdata = base64.b64decode(bmp)
        # print(bmp)
        img = Image.open(BytesIO(imgdata))
        width = 240
        high = 120
        box = (0, 0, width, high)
        region = img.crop(box)
        data = self.bmp2bytes(region)
        width = int(width // 8)
        ss = 'BITMAP 5,5,{0},{1},0,'.format(width, high)
        self.send_data_printer(ss)
        self.send_data_printer(data)
        self.send_data_printer('\n')
        self.print_excute()

    def print_bmp_file(self, bmp=''):
        """打印位图
        Keyword Arguments:
            index {int} -- [description] (default: {0})
            label {str} -- [description] (default: {''})
        """
        self.printer_prepare()
        self.send_data_printer('DENSITY 15\n')
        img = Image.open(bmp)
        width = 560
        high = 310
        # width = 160
        # high = 160
        box = (0, 0, width, high)
        region = img.crop(box)
        data = self.bmp2bytes(region)
        width = int(width // 8) + 2
        ss = 'BITMAP 0,25,{0},{1},0,'.format(width, high)
        self.send_data_printer(ss)
        self.send_data_printer(data)
        self.send_data_printer('\n')
        self.print_excute()

    def bmp2bytes(self, img, row=0, col=16):
        pix = img.load()
        data = b''
        for j in range(img.height + row):
            byt = 0
            for i in range(img.width + col):
                if i < img.width and j < img.height:
                    if pix[i, j] != 0:
                        byt += 1
                else:
                    byt += 1
                if i % 8 == 7:
                    data += byt.to_bytes(length=1, byteorder='big')
                    byt = 0
                byt *= 2
        return data

    def print_materials_lable(self, filename, mode=0):
        """打印位图
        Keyword Arguments:
            index {int} -- [description] (default: {0})
            label {str} -- [description] (default: {''})
        """
        try:
            self.printer_prepare()
            self.send_data_printer('DENSITY 15\n')
            with open(filename, 'r', encoding="utf-8") as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if row[0] != "":
                        img = PrintImage((560, 310), True)
                        img = img.materials_lable(row, mode)
                        img.show()
                        data = self.bmp2bytes(img)
                        width = int(img.width // 8) + 2
                        ss = 'BITMAP 0,25,{0},{1},0,'.format(width, img.height)
                        self.send_data_printer(ss)
                        self.send_data_printer(data)
                        self.send_data_printer('\n')
                        self.print_excute()

        except Exception as err:
            print(err)
            return

    def print_QRCode(self, label):
        """打印二维码和序列号
        Arguments:
            label {str} -- 字符串标签，字符长度大于等于16
        Returns:
            {bool} -- True or False
        """
        if len(label) == 16:
            res = []
            try:
                ss = 'QRCODE 40,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))
                ss = 'QRCODE 190,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))
                ss = 'QRCODE 450,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))

                ss = 'TEXT 280,30,"FONT001",0,1,1,1,"{0}"\n'.format(label[0:8])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 280,60,"FONT001",0,1,1,1,"{0}"\n'.format(
                    label[8:16])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 540,30,"FONT001",0,1,1,1,"{0}"\n'.format(label[0:8])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 540,60,"FONT001",0,1,1,1,"{0}"\n'.format(
                    label[8:16])
                res.append(self.send_data_printer(ss))
                if False not in res:
                    return True
                else:
                    return False
            except Exception as err:
                print('[error]', err)
                return False
        else:
            print('[fail]', "产品序列号必须为16位字符")
            return False

    def print_label_block(self, label):
        """测试失败时打印的条码
        Keyword Arguments:
            index {int} -- [description] (default: {0})
            label {str} -- [description] (default: {''})
        """
        img = PrintImage((648, 90))
        img = img.block_label(label)
        # img.show()
        data = self.bmp2bytes(img, 10, 16)
        width = int(img.width // 8) + 2
        ss = 'BITMAP 0,15,{0},{1},0,'.format(width, img.height + 10)
        self.send_data_printer(ss)
        self.send_data_printer(data)
        self.send_data_printer('\n')
        self.print_excute()

    def print_label(self, staus, label):
        """打印标签到标签纸
        Arguments:
            staus {[type]} -- 字符串标签，字符长度大于等于16
            label {str} -- [description]
        Returns:
            {bool} -- True or False
        """
        self.printer_prepare()
        if staus:
            self.print_QRCode(label)       
        return self.print_excute()

    def backfeed(self):
        """进纸"""
        self.send_data_printer('BACKFEED 10\n')

    def feed(self):
        """出纸"""
        self.send_data_printer('FEED 10\n')

    def home(self):
        """出纸校正"""
        res = []
        try:
            res.append(self.send_data_printer('SIZE 50 mm, 30 mm\n'))
            res.append(self.send_data_printer('GAP 2 mm,0\n'))
            res.append(self.send_data_printer('HOME\n'))
            res.append(self.send_data_printer('FEED 10\n'))
            if False not in res:
                return True
            else:
                return False
        except Exception as err:
            print('[error]', err)
            return False

    def formfeed(self):
        """下一标签"""
        res = []
        try:
            res.append(self.send_data_printer('SIZE 50 mm, 30 mm\n'))
            res.append(self.send_data_printer('GAP 2 mm,0\n'))
            res.append(self.send_data_printer('FORMFEED\n'))
            if False not in res:
                return True
            else:
                return False
        except Exception as err:
            print('[error]', err)
            return False


if __name__ == "__main__":
    # myPrinter = TSCPrinter()
    # myPrinter.print_materials_lable("C:/Users/ThinkPad/Documents/物料标签.csv", 0)
    # myPrinter.print_label_block(
    #      ("深圳佑驾创新科技有限公司", "深圳佑驾创新科技有限公司", "深圳佑驾创新科技有限公司"))
    # img = PrintImage((650, 90))
    # img.block_label(("深圳佑驾创新科技有限公司", "深圳佑驾创新科技有限公司", "深圳佑驾创新科技有限公司")).show()
    img = PrintImage((560, 310), True)
    img.materials_lable1(("1234567890","Microchip"
        , "IC12345678901234567890","200"
        ,"2019/12/15"
        ),0).show()
    # img.materials_lable(("1234567890", "MICROCHIP", "IC12345678901234567890ABCDEFGHIJKLMN",
    #                       "19/12/15"),1).show()
    # # draw = Draw()
    # # cnt = 25
    # # height = 88
    # # img = PrintImage([560, 88 * cnt],True)
    # # font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\MSYH.TTC", 34, index=1)
    # # fontnum = ImageFont.truetype("C:\\WINDOWS\\Fonts\\MSYH.TTC", 28)
    # # for i in range(cnt):
    # #     img.dr.line((0, 88 * i, 560, 88 * i), fill=0, width=2)
    # # img.dr.line((150, 0, 150, 88 * cnt), fill=0, width=2)
    # # value = "100nF/0603/16V123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # # for i in range(cnt):
    # #     draw.text_multi_center(img.dr, (150, 88 * i, 560, 88 * (i + 1)),
    # #                            value[0:i * 1 + 22], fontnum, 2)
    # # img.img.show()