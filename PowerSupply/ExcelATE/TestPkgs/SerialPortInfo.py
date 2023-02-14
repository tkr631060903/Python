import serial.tools.list_ports
# print(serial.tools.list_ports.ListPortInfo())
port_list = list(serial.tools.list_ports.comports())
if len(port_list) == 0:
    print('找不到串口')
else:
    for port in port_list:
        print("1111111111", port.device)
        print(port.hwid)
        # print(port.pid)
        # print(port.serial_number)
        # print(port.manufacturer)