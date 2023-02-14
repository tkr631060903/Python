from serial import Serial


class TSCPrinter:

    def __init__(self, portx='', baudratex=9600):
        self.serx = Serial(
            port=portx,
            baudrate=baudratex,
            timeout=0.2,
            write_timeout=0.1,
            inter_byte_timeout=0.1
        )

    def IDN(self):
        """身份标志
        Returns:
            {str} -- [description]
        """
        if self.serx:
            return str(self.serx) + '\n'
        else:
            return 'ERROR\n'

    def close(self):
        """关闭打印机通讯
        Returns:
            [type] -- [description]
        """
        return self.serx.close()

    def send_data_printer(self, cmdstr):
        """向打印机发送数据命令
        Arguments:
            cmdstr {str} -- 字符串命令
        Returns:
            {bool} -- True or False
        """
        try:
            if type(cmdstr) is bytes:
                res = self.serx.write(cmdstr)
            else:
                res = self.serx.write(cmdstr.encode('GBK'))
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
            res.append(self.send_data_printer('SIZE 58 mm, 10 mm\n'))
            res.append(self.send_data_printer('GAP 2 mm,0\n'))
            res.append(self.send_data_printer('DIRECTION 1\n'))
            res.append(self.send_data_printer('OFFSET 0 mm\n'))
            res.append(self.send_data_printer('DENSITY 3\n'))
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
                ss = 'QRCODE 35,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))
                ss = 'QRCODE 299,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))
                ss = 'QRCODE 557,17,L,3,A,0,M2,S7,"https://p.minieye.cc/i/{0}"\n'.format(
                    label)
                res.append(self.send_data_printer(ss))

                ss = 'TEXT 127,30,"FONT001",0,1,1,1,"{0}"\n'.format(label[0:8])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 127,60,"FONT001",0,1,1,1,"{0}"\n'.format(label[8:16])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 389,30,"FONT001",0,1,1,1,"{0}"\n'.format(label[0:8])
                res.append(self.send_data_printer(ss))
                ss = 'TEXT 389,60,"FONT001",0,1,1,1,"{0}"\n'.format(label[8:16])
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

    def print_label_block(self, index=0, label=''):
        """测试失败时打印的条码
        Keyword Arguments:
            index {int} -- [description] (default: {0})
            label {str} -- [description] (default: {''})
        """
        charPerLine = (16, 16, 8)
        leftMargin = (40, 304, 563)
        if index > 2:
            index = 2
        elif index < 0:
            index = 0

        label_length = (len(label.encode('utf-8'))-len(label))/2+len(label)
        print("label_length:"+str(label_length)+" "+label)
        if label_length <= charPerLine[index] / 2:
            print(label)
            ss = 'TEXT {0},20,"song12",0,4,4,1,"{1}"\n'.format(
                leftMargin[index], label)
            self.send_data_printer(ss)
        else:        
            col = charPerLine[index]        
            label_list = ['','','','','',]
            label_index = 0     
            for uchar in label:
                if label_index >3:
                    break
                else:
                    label_list[label_index] += uchar
                    label_len = (len(label_list[label_index].encode('utf-8'))-len(label_list[label_index]))/2+len(label_list[label_index])
                    if label_len == col:
                        label_index += 1
                    elif label_len > col:
                        label_list[label_index] = label_list[label_index][:-1]
                        label_index += 1
                        label_list[label_index] += uchar         
            self.send_data_printer('DENSITY 10\n')            
            for i in range(4):              
                print(label_list[i])
                ss = 'TEXT {0},{1},"song12",0,2,2,1,"{2}"\n'.format(
                    leftMargin[index], 20+24*i, label_list[i])
                self.send_data_printer(ss)

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
        else:
            self.print_label_block(1, label)
        return self.print_excute()


if __name__ == "__main__":
    myPrinter = TSCPrinter('COM7')
    print('@@@', myPrinter.IDN())
    myPrinter.printer_prepare()
    #print(myPrinter.print_label_block(0, '海贼王'))
    #print(myPrinter.print_label_block(1, 'abcdefghij'))
    #print(myPrinter.print_label_block(2, '海贼王'))
    #myPrinter.print_excute()
    print('海')
