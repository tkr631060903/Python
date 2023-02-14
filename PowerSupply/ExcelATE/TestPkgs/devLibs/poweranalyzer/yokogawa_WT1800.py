from math import isnan, isinf
from threading import RLock
pyvisa


class PowerAnalyzer(object):
    """功率分析仪
    Arguments:
        visaAdrr {str} -- 通讯参数
    """

    def __init__(self, visaAdrr):
        self.xlock = RLock()
        rm = visa.ResourceManager(
        )  # this uses pyvisa 'C:\\Windows\\System32\\visa32.dll'
        self.heromix = rm.open_resource(visaAdrr)
        # Set Global Timeout
        self.heromix.timeout = 2000
        # Clear the instrument bus
        self.heromix.clear()
        self.heromix.write('*CLS')

    def IDN(self):
        """获取设备ID"""
        return self.heromix.query('*IDN?')

    def RST(self):
        """复位"""
        self.heromix.write('*RST')

    def CLS(self):
        """清除寄存器的值"""
        self.heromix.write('*CLS')

    def getValue(self, arg=''):
        """读取值
        arg: '1' to '255'
        """
        try:
            rval = float(self.heromix.get_numeric_normal_value(arg))
            if isnan(rval) or isinf(rval):
                rval = 9999
            return rval
        except ValueError as err:
            print('PowerAls getValue failed, ', str(err))
            return 0

    def setPreset(self, arg=''):
        self.heromix.set_numberic_normal_preset(arg)

    def get_Aoutput(self):
        """查询所有D/A输出设置"""
        return self.heromix.query(':AOUT?')

    def get_Aoutput_normal(self):
        """查询所有D/A输出设置"""
        return self.heromix.query(':AOUT:NORM?')

    def set_Aoutput_channel(self, x='0', func='', elem='', order=''):
        """设置一个D/A输出元素(function, element, or harmonic order)
        x: '1' to '20'
        func: 'NONE' or URMS|IRMS|P|S|Q|...
        elem: '1' to '6'|SIGMA|SIGMB|SIGMC
        order:  TOT|DC|'1' to '500'
        """
        self.heromix.write(':AOUTPUT:CHANNEL' + x + ',' + func + ',' + elem +
                           ',' + order)

    def get_Aoutput_channel(self, x='0'):
        """查询一个D/A输出元素(function, element, or harmonic order)
        x: '1' to '20'
        """
        return self.heromix.query(':AOUTPUT:CHANNEL' + x + '?')

    def set_Aoutput_IRtime(self, first='0', second='0', third='0'):
        """设置intergration time that is used in the D/A output of the integrated value
        first: '0' to '10000' (hours)
        second: '0' to '59' (minutes)
        third: '0' to '59' (seconds)
        """
        self.heromix.write(':AOUT:IRT ' + first + ',' + second + ',' + third)

    def get_Aoutput_IRtime(self):
        """查询intergration time that is used in the D/A output of the integrated value
        """
        return self.heromix.query(':AOUT:IRT?')

    def set_Aoutput_mode(self, x='0', mode=''):
        """sets the rated-value setup mode for D/A output items
        x: '1' to '20'
        mode: 'FIX' or 'MAN'
        """
        self.heromix.write(':AOUT:MODE' + x + ',' + mode)

    def get_disp(self):
        """queries all disp setting"""
        return self.heromix.query(':DISP?')

    def get_disp_bar(self):
        """Queries all bar graph disp settings."""
        return self.heromix.query(':DISP:BAR?')

    def set_disp_bar_format(self, argv=''):
        """Sets or queries the bar graph disp format.
        argv: 'SING' or 'DUAL' or 'TRI'
        """
        self.heromix.write(':DISP:BAR:FORM ' + argv)

    def set_disp_bar_item(self, x='0', func='', elem=''):
        """Sets or queries the function and element of the
        specified bar graph item.
        x: '1' to '3'
        func: U|I|P|S|Q|LAMB|PHI|PHIU|Z|RS|XS|RP|XP
        elem: '1' to '6'
        """
        self.heromix.write(':DISP:BAR:ITEM' + x + func + ',' + elem)

    def get_disp_bar_item(self, x='0'):
        """Queries all the disp settings of the specified
        bar graph.
        x: '1' to '3'
        """
        return self.heromix.query(':DISP:BAR:ITEM' + x + '?')

    def get_disp_bar_item_scal(self, x='0'):
        """Queries all scaling settings for the specified bar graph.
        x: '1' to '3'
        """
        return self.heromix.query(':DISP:BAR:ITEM' + x + 'SCAL?')

    def set_disp_bar_item_scalMode(self, x='0', mode=''):
        """Sets or queries the scaling mode of the specified
        bar graph.
        x: '1' to '3'
        mode: 'FIX' or 'MAN'
        """
        self.heromix.write(':DISP:BAR:ITEM' + x + ':SCAL:MODE ' + mode)

    def set_disp_bar_scalVal(self, x='0', argv='0'):
        """Sets or queries the scaling mode of the specified
        bar graph.
        x: '1' to '3'
        argv: number string '<NRf>'
        """
        self.heromix.write(':DISP:BAR:ITEM' + x + ':SCAL:argv ' + argv)

    def set_disp_bar_item_scalVertical(self, x='0', argv=''):
        """Sets or queries the vertical scaling mode of the
        specified bar graph.
        x: '1' to '3'
        argv: 'LIN' or 'LOG'
        """
        self.heromix.write(':DISP:BAR:ITEM' + x + ':SCAL:VERT ' + argv)

    def set_disp_bar_item_scalXaxis(self, x='0', argv=''):
        """Sets or queries the position of the X axis of the
        specified bar graph.
        x: '1' to '3'
        argv: 'BOTT' or 'CENT'
        """
        self.heromix.write(':DISP:BAR:ITEM' + x + ':SCAL:XAX ' + argv)

    def set_disp_bar_order(self, first='0', second='10'):
        """Sets or queries the disped starting and ending
        harmonic orders of the bar graphs.
        first: '0' to '490'
        second: '10' or '500'
        """
        self.heromix.write(':DISP:BAR:ORD ' + first + ',' + second)

    def get_disp_hspeed(self):
        """Queries all high speed data capturing disp
        settings."""
        self.heromix.query(':DISP:HSP?')

    def get_disp_hspeed_col(self):
        """Queries all column settings of the high speed
        data capturing mode."""
        return self.heromix.query(':DISP:HSP:COL?')

    def set_disp_hspeed_col_item(self, x='0', argv=''):
        """Sets or queries the specified column disp item
        of the high speed data capturing mode.
        x: '1' to '6'
        argv: 'NONE' or '<NRf>'|'SIGMA'|'SIGMB'|'SIGMC'
        """
        self.heromix.write(':DISP:HSP:COL:ITEM' + x + ' ' + argv)

    def set_disp_hspeed_col_num(self, argv='0'):
        """Sets or queries the number of columns of the
        high speed data capturing mode.
        argv: '<NRf>'
        """
        self.heromix.write(':DISP:HSP:COL:NUM ' + argv)

    def set_disp_hspeed_col_reset(self):
        """Resets the column disp items to their default
        values on the high speed data capturing mode."""
        self.heromix.write(':DISP:HSP:COL:RES')

    def set_disp_hspeed_frame(self, onoff=''):
        """Sets or queries the on/off status of the high speed
        data capturing mode's data section frame.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:HSP:FRAM ' + onoff)

    def set_disp_hspeed_page(self, argv=''):
        """Sets or queries the disped page of the high
        speed data capturing mode.
        argv: '<NRf>'
        """
        self.heromix.write(':DISP:HSPEED:PAGE ' + argv)

    def set_disp_hspeed_pover(self, onoff=''):
        """Sets or queries the on/off status of the disp of
        peak over-range information in high speed data capturing mode.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:HSPEED:POV ' + onoff)

    def get_disp_info(self):
        """Queries all setup parameter list disp settings."""
        return self.heromix.query(':DISP:INFO?')

    def set_disp_info_page(self, argv=''):
        """Sets or queries the disped page of the setup
        parameter list disp.
        argv: 'POW' or 'RANG' or '<NRf>'
        """
        self.heromix.write(':DISP:INFO:PAGE ' + argv)

    def set_disp_info(self, onoff=''):
        """Sets or queries the on/off status of the setup
        parameter list disp.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:INFO ' + onoff)

    def set_disp_mode(self, mode=''):
        """Sets or queries the disp mode.
        mode: 'NUM'|'WAVE'|'TREN'|'BAR'|'VECT'|'NWAV'|'NTR'|'NBAR'|
        'NVEC'|'WNUM'|'WTR'|'WBAR'|'WVEC'|'TNUM'|'TWAV'|'TBAR'|'TVEC'|'HSP'|
        """
        self.heromix.write('DISP:MODE ' + mode)

    def get_disp_numeric(self):
        """Queries all numeric disp settings."""
        return self.heromix.query(':DISP:NUM?')

    def get_disp_numeric_custom(self):
        """Queries all numeric disp settings in custom
        disp mode."""
        return self.heromix.query(':DISP:NUM:CUST?')

    def set_disp_numeric_custom_file_cdir(self, argv=''):
        """Changes the directory that files are loaded from
        or saved to for the numeric disp in custom
        disp mode.
        argv: dirctory name
        """
        self.heromix.write(':DISP:NUM:CUST:FILE:CDIR ' + argv)

    def set_disp_numeric_custom_file_drive(self, argv=''):
        """Sets the drive that files are loaded from or saved
        to for the numeric disp in custom disp mode.
        argv: 'RAM'|'USB[,<NRf>]|NETW'
        """
        self.heromix.write(':DISP:NUM:CUST:FILE:DRIV ' + argv)

    def get_disp_numeric_custom_file_free(self):
        """Queries the amount of free space (in bytes) on
        the drive that files are loaded from or saved to for
        the numeric disp in custom disp mode."""
        return self.heromix.query(':DISP:NUM:CUST:FILE:FREE?')

    def set_disp_numeric_custom_file_load(self, typ='', argv=''):
        """Aborts a file loading operation for the numeric
        disp in custom disp mode.
        typ: 'ABOR' or 'BMP' or 'BOTH' or 'ITEM'
        argv: string
        """
        self.heromix.write(':DISP:NUM:CUST:FILE:LOAD:' + typ + ' ' + argv)

    def get_disp_numeric_custom_file_path(self):
        """Queries the absolute path of the directory that
        files are loaded from or saved to for the numeric
        disp in custom disp mode."""
        return self.heromix.query(':DISP:NUM:CUST:FILE:PATH?')

    def set_disp_numeric_custom_file_save(self, typ='', argv=''):
        """Sets or queries the automatic file name
        generation feature for saving disp configuration
        files of the numeric disp in custom disp mode.
        typ: 'ANAM' or 'ITEM'
        argv:
            typ='ANM': 'OFF' or 'NUMB' or 'DATE'
            typ='ITEM': <string>
        """
        self.heromix.write(':DISP:NUM:CUST:FILE:SAVE:' + typ + ' ' + argv)

    def get_disp_numeric_custom_item(self, x='0'):
        """Queries all the settings of the specified disp
        item of the numeric disp in custom disp mode.
        x: '1' to '192'
        """
        return self.heromix.query(':DISP:NUM:CUST:ITEM' + x + '?')

    def set_disp_numeric_custom_item_color(self, x='0', argv=''):
        """Sets or queries the font color of the specified
        disp item of the numeric disp in custom
        disp mode.
        x: '1' to '192'
        argv: 'YELL'|'GRE'|'MAG'|'CYAN'|'RED'|'ORAN'|'LBL'|'PURP'|'BLUE'|
        'PINK'|'LGR'|'DBL'|'BGR'|'SPIN'|'MGR'|'GRAY'|'WHITE'|'DGRAY'|'BGRAY'|
        'BLAC'
        """
        self.heromix.write(':DISP:NUM:CUST:ITEM' + x + ':COL ' + argv)

    def set_disp_numeric_custom_item(self, x='0', func='', elem='', order=''):
        """Sets or queries the display item (numeric item or
        string) of the numeric display in custom display mode.
        x: '1' to '192'
        func: 'URMS'|'IRMS'|'P'|'S'|'Q'|...
        elem: '<NRf>'|SIGMA|SIGMB|SIGMC
        order: 'TOT'|'DC'|'<NRf>'
        """
        if elem != '':
            elem = ',' + elem
        if order != '':
            order = ',' + order
        self.heromix.write(':DISP:NUM:CUST:ITEM' + x + ' ' + func + elem +
                           order)

    def set_disp_numeric_custom_item_postion(self, x='0', first='', second=''):
        """Sets or queries the display position of the
        specified display item of the numeric display in
        custom display mode.
        first: '0' to '800'
        second: '0' to '672'
        """
        self.heromix.write(':DISP:NUM:CUST:ITEM' + x + ':POS ' + first + ',' +
                           second)

    def set_disp_numeric_custom_item_size(self, x='0', argv=''):
        """Sets or queries the font size of the specified
        display item of the numeric display in custom
        display mode.
        x: '0' to '192'
        argv: '14', '16', '20', '24', '32', '48', '64', '96', '128'
        """
        self.heromix.write(':DISP:NUM:CUST:ITEM' + x + ':SIZE ' + argv)

    def set_disp_num_custom_page(self, argv=''):
        """Sets or queries the displayed page of the numeric
        display in custom display mode.
        argv: '1' to '12'
        """
        self.heromix.write(':DISP:NUM:CUST:PAGE ' + argv)

    def set_disp_numeric_custom_prepage(self, argv=''):
        """Sets or queries the number of items displayed
        per page of the numeric display in custom display
        mode.
        argv: '1' to the total number of display items
        """
        self.heromix.write(':DISP:NUM:CUST:PERP ' + argv)

    def set_disp_numeric_custom_total(self, argv=''):
        """Sets or queries the total number of display items
        of the numeric display in custom display mode.
        argv: '1' to '192'
        """
        self.heromix.write(':DISP:NUM:CUST:TOT ' + argv)

    def set_disp_numeric_frame(self, onoff=''):
        """Sets or queries the on/off status of the numeric
        display’s data section frame.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:NUM:FRAM ' + onoff)

    def get_disp_numeric_normal(self):
        """Queries all numeric display settings."""
        return self.heromix.query(':DISP:NUM:NORM?')

    def get_disp_numeric_all(self):
        """Queries all settings of the numeric display in All
        Items display mode."""
        return self.heromix.query(':DISP:NUM:ALL?')

    def get_disp_numeric_all_col(self):
        """Queries all column settings of the numeric display
        in All Items display mode."""
        return self.heromix.query(':DISP:NUM:ALL:COL?')

    def set_disp_numeric_all_col_daelem(self, onoff=''):
        """Sets or queries the on/off status of the column
        display all feature of the numeric display in All
        Items display mode.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:NUM:ALL:COL:DAEL ' + onoff)

    def set_disp_numeric_all_col_scroll(self, argv=''):
        """Sets or queries the on/off status of column
        scrolling of the numeric display in All Items
        display mode.
        argv: '0' to '3'
        """
        self.heromix.write(':DISP:NUM:ALL:COL:SCR ' + argv)

    def set_disp_numeric_all_cursor(self, func=''):
        """Sets or queries the cursor position on the numeric
        display in All Items display mode..
        func: 'URMS'|'IRMS'|'P'|'S'|'Q'|...
        """
        self.heromix.write(':DISP:NUM:ALL:COL:CURS ' + func)

    def set_disp_numeric_all_order(self, order=''):
        """Sets or queries the displayed harmonic order on
        the harmonic measurement function display page
        of the numeric display in All Items display mode.
        order: 'TOT'|'DC'|'<NRf>'('1' to '500')
        """
        self.heromix.write(':DISP:NUM:ALL:COL:ORD ' + order)

    def set_disp_numeric_all_page(self, argv=''):
        """Sets or queries the displayed page of the numeric
        display in All Items display mode.
        argv: '1' to '7'
        """
        self.heromix.write(':DISP:NUM:ALL:PAGE ' + argv)

    def set_disp_numeric_format(self, argv=''):
        """Sets or queries the numeric display format.
        argv: 'VAL4'|'VAL8'|'VAL16'|'MATR'|'ALL'|'SING'|'DUAL'|'CUST'
        """
        self.heromix.write(':DISP:NUM:FORM ' + argv)

    def get_disp_numeric_list(self):
        """Queries all numeric display settings in the list
        display modes."""
        return self.heromix.query(':DISP:NUM:LIST?')

    def set_disp_numeric_list_cursor(self, argv=''):
        """Sets or queries the cursor position on the numeric
        display in the list display modes.
        argv: 'HEAD' or 'ORD'
        """
        self.heromix.write(':DISP:NUM:LIST:CURS ' + argv)

    def set_disp_numeric_list_header(self, argv=''):
        """Sets or queries the cursor position of the header
        section on the numeric display in the list display
        modes.
        argv: '1' to '155'
        """
        self.heromix.write(':DISP:NUM:LIST:HEAD ' + argv)

    def set_disp_numeric_list_item(self, x='0', func='', elem=''):
        """Sets or queries the specified display item (function
        and element) on the numeric display in the list
        display modes.
        x: '1' or '2'
        func: 'U'|'I'|'P'|'S'|'Q'|'LAMB'|'PHI'|'PHIU'|'PHII'|'Z'|
        'RS'|'XS'|'RP'|'XP'
        elem: '<NRf>'('1' to '6')|'SIMGa'|'SIMGB'|'SIGMC'
        """
        self.heromix.write(':DISP:NUM:LIST:ITEM' + x + ' ' + func + ',' + elem)

    def set_disp_numeric_list_order(self, argv=''):
        """Sets or queries the harmonic order cursor position
        of the data section on the numeric display in the
        list display modes.
        argv: '1' to '500' (harmonic order)
        """
        self.heromix.write(':DISP:NUM:LIST:ORD ' + argv)

    def get_disp_numeric_matrix(self):
        """Queries all numeric display settings in matrix
        display mode."""
        return self.heromix.query(':DISP:NUM:MATR?')

    def get_disp_numeric_matrix_col(self):
        """Queries all column settings of the numeric display
        in matrix display mode."""
        return self.heromix.query(':DISP:NUM:MATR:COL?')

    def set_disp_numeric_matrix_col_item(self, x='0', elem=''):
        """Sets or queries the specified column display item
        of the numeric display in matrix display mode.
        x: '1' to '6'
        elem: '<NRf>'('1' to '6')|SIMGa|SIMGB|SIMGC
        """
        self.heromix.write(':DISP:NUM:MATR:COL:ITEM' + x + ' ' + elem)

    def set_disp_numeric_matrix_col_num(self, argv=''):
        """Sets or queries the number of columns of the
        numeric display in matrix display mode.
        argv: '4', '6'
        """
        self.heromix.write(':DISP:NUM:MATR:COL:NUM ' + argv)

    def set_disp_numeric_matrix_col_reset(self):
        """Resets the column display items to their default
        values on the numeric display in matrix display
        mode."""
        self.heromix.write(':DISP:NUM:MATR:COL:RES')

    def set_disp_numeric_matrix_cursor(self, argv=''):
        """Sets or queries the cursor position on the numeric
        display in matrix display mode.
        argv: '1' to '81'
        """
        self.heromix.write(':DISP:NUM:MATR:CURS ' + argv)

    def set_disp_numeric_matrix_item(self, x='0', func='', elem='', order=''):
        """Sets or queries the specified display item (function
        harmonic order) on the numeric display in
        matrix display mode.
        x: '1' to '81'
        func: 'URMS'|'IRMS'|'P'|'S'|'Q'|...
        elem: '<NRf>'('1' to '6')|'SIGMA'|'SIGMB'|'SIGMC'
        order: 'TOT'|'DC'|'<NRf>'('1' to '500')
        """
        if elem != '':
            elem = ',' + elem
        if order != '':
            order = ',' + order
        self.heromix.write(':DISP:NUM:MATR:ITEM' + x + func + elem + order)

    def set_disp_numeric_matrix_page(self, argv=''):
        """Sets or queries the displayed page of the numeric
        display in matrix display mode.
        argv: '1' to '9'
        """
        self.heromix.write(':DISP:NUM:MATR:PAGE ' + argv)

    def set_disp_numeric_matrix_preset(self, argv=''):
        """Presets the display order pattern of displayed
        items on the numeric display in matrix display
        mode.
        argv: '<NRf>'('1' to '4')|'EOR'|'FOR'|'CLRP'|'CLRA'
        """
        self.heromix.write(':DISP:NUM:MATR:PRES ' + argv)

    def get_disp_numeric_VAL(self, x=''):
        """Queries all numeric display settings in 4 Items, 8
        Items, or 16 Items display mode.
        argv: '4', '8', '16'
        """
        return self.heromix.query(':DISP:NUM:argv' + x + '?')

    def set_disp_numeric_VAL_cursor(self, x='', argv=''):
        """Sets or queries the cursor position on the numeric
        display in 4 Items, 8 Items, or 16 Items display
        mode.
        x: '4', '8', '16'
        argv:
            if x='4': argv='1' to '48'
            if x='8': argv='1' to '96'
            if x='16': argv='1' to '192'
        """
        self.heromix.write(':DISP:NUM:argv' + x + ':CURS ' + argv)

    def set_disp_numeric_VAL_item(self,
                                  x1='',
                                  x2='',
                                  func='',
                                  elem='',
                                  order=''):
        """Sets or queries the function, element, and
        armonic order of the specified numeric display
        item in 4 Items, 8 Items, or 16 Items display
        mode.
        x1: '4', '8', '16'
        argv:
            if x1='4': x2='1' to '48'
            if x1='8': x2='1' to '96'
            if x1='16': x2='1' to '192'
        func: 'URMS'|'IRMS'|'P'|'S'|'Q'|...
        elem: '<NRf>'('1' to '6')|'SIGMA'|'SIGMB'|'SIGMC'
        order: 'TOT'|'DC'|'<NRf>'('1' to '500')
        """
        if elem != '':
            elem = ',' + elem
        if order != '':
            order = ',' + order
        self.heromix.write(':DISP:NUM:argv' + x1 + ':ITEM' + x2 + ' ' + func +
                           elem + order)

    def set_disp_numeric_VAL_page(self, x='', argv=''):
        """Sets or queries the displayed page of the numeric
        display in 4 Items, 8 Items, or 16 Items display
        mode.
        x: '4', '8', '16'
        argv: '1' to '12'
        """
        self.heromix.write(':DISP:NUM:argv' + x + ':PAGE ' + argv)

    def set_disp_numeric_VAL_preset(self, x='', argv=''):
        """Presets the display order pattern of displayed
        items on the numeric display in 4 Items, 8 Items,
        or 16 Items display mode.
        x: '4','8','16'
        argv: '<NRf>'('1' to '4')|'FOR'|'EOR'|'CLRP'|'CLRA'
        """
        self.heromix.write(':DISP:NUM:argv' + x + ':PRES ' + argv)

    def get_disp_wave(self):
        """Queries all waveform display settings."""
        return self.heromix.query(':DISP:WAVE?')

    def set_disp_wave_all(self, onoff=''):
        """Collectively sets the on/off status of all waveform
        displays.
        onoff: 'OFF' or 'ON'
        """
        self.heromix.write(':DISP:WAVE:ALL ' + onoff)

    def set_disp_wave_format(self, argv=''):
        """Sets or queries the display format of all waveforms.
        argv: 'SING'|'DUAL'|'TRI'|'QUAD'|'HEX'
        """
        self.heromix.write(':DISP:WAVE:FORM ' + argv)

    def set_disp_wave_graticule(self, argv=''):
        """Sets or queries the graticule (grid) type
        argv: 'GRID'|'FRAM'|'CROS'
        """
        self.heromix.write(':DISP:WAVE:GRAT ' + argv)

    def set_disp_wave_interpolate(self, argv=''):
        """Sets or queries the waveform interpolation
        method.
        argv: 'OFF'|'LINE'
        """
        self.heromix.write(':DISP:WAVE:INT ' + argv)

    def get_disp_wave_mapping(self):
        """Queries all split screen waveform mapping
        settings."""
        return self.heromix.query(':DISP:WAVE:MAPP?')

    def set_disp_wave_mapping_mode(self, argv=''):
        """Sets or queries the split screen waveform
        mapping mode.
        argv: 'AUTO'|'FIX'|'USER'
        """
        self.heromix.write(':DISP:WAVE:MAPP:MODE ' + argv)

    def set_disp_wave_mapping_UIAUX(self, typx='', argv=''):
        """Sets or queries the split screen voltage, current,
        rotating speed, torque, or auxiliary signal
        waveform mapping setting.
        typ: 'U<x>'|'I<x>'|'AUX<x>'|SPE|TORQ
        x: '1' to '6' AUX<x>中x取值'1' to '2'; 比如U1, I1, AUX1
        argv= '0' to '5'
        """
        self.heromix.write(':DISP:WAVE:MAPP:' + typx + ' ' + argv)

    def get_disp_wave_position(self):
        """Queries all waveform vertical position (center
        position level) settings."""
        return self.heromix.query(':DISP:WAVE:POS?')

    def set_disp_wave_position(self, typx='', argv=''):
        """Sets or queries the vertical position (center
        position level) of the specified element’s voltage
        or current waveform.
        typx: 'U<x>'|'I<x>'|'<NRf>'('-130.000' to '130.000'(%))|'UALL'|'IALL'
        argv:
        """
        self.heromix.write(':DISP:WAVE:POS:' + typx + ' ' + argv)

    def set_disp_wave_svalue(self, onoff=''):
        """Sets or queries the on/off status of the scale
        value display.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':DISP:WAVE:SVAL ' + onoff)

    def set_disp_wave_tdiv(self, argv=''):
        """Sets or queries the waveform Time/div value.
        argv: '0.05','0.1','0.2','0.5','1','2','5','10','20','50','100','200',
        '500' (ms), '1','2' (s)
        """
        self.heromix.write(':DISP:WAVE:TDIV ' + argv)

    def set_disp_wave_tlabel(self, onoff=''):
        """Sets or queries the on/off status of the waveform
        labels.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':DISP:WAVE:TLAB ' + onoff)

    def get_disp_wave_trigger(self):
        """Queries all trigger settings."""
        self.heromix.write(':DISP:WAVE:TRIG?')

    def set_disp_wave_trigger_level(self, argv=''):
        """Sets or queries the trigger level.
        argv: '-100.0' to '100.0' (%)
        """
        self.heromix.write(':DISP:WAVE:TRIG:LEV ' + argv)

    def set_disp_wave_trigger_mode(self, argv=''):
        """Sets or queries the trigger mode.
        argv: 'AUTO'|'NORM'|'OFF'
        """
        self.heromix.write(':DISP:WAVE:TRIG:MODE ' + argv)

    def set_disp_wave_trigger_slope(self, argv=''):
        """Sets or queries the trigger slope.
        argv: 'RISE'|'FALL'|'BOTH'
        """
        self.heromix.write(':DISP:WAVE:TRIG:SLOP ' + argv)

    def set_disp_wave_trigger_source(self, argv=''):
        """Sets or queries the trigger source.
        argv: 'U<x>'|'I<x>'|'EXT'
        """
        self.heromix.write(':DISP:WAVE:TRIG:SOUR ' + argv)

    def set_disp_wave_UIAUX(self, typx='', onoff=''):
        """Sets or queries the split screen voltage, current,
        rotating speed, torque, or auxiliary signal
        waveform mapping setting.
        typ: 'U<x>'|'I<x>'|'AUX<x>'|SPE|TORQ
        x: '1' to '6' AUX<x>中x取值'1' to '2'; 比如U1, I1, AUX1
        onoff= 'OFF'|'ON'
        """
        self.heromix.write(':DISP:WAVE:' + typx + ' ' + onoff)

    def get_disp_wave_vzoom(self):
        """Queries all waveform vertical zoom factor settings."""
        return self.heromix.query(':DISP:WAVE:VZ?')

    def set_disp_wave_vzoom(self, typx='', argv=''):
        """Sets or queries the vertical zoom factor of the
        specified element’s voltage or current waveform.
        typx: 'U<x>'|'I<x>'|'UALL'|'IALL'
        argv: '0.1' to '100'
        """
        self.heromix.write(':DISP:WAVE:VZ:' + typx + ' ' + argv)

    def get_input(self):
        """Queries all input element settings."""
        return self.heromix.query(':INP?')

    def set_input_cfactor(self, argv=''):
        """Sets or queries the crest factor设置波峰因素.
        argv: '3', '6'"""
        self.heromix.write(':INP:CFAC ' + argv)

    def get_input_curr(self):
        """Queries all electric current measurement settings."""
        return self.heromix.query(':INP:CURR?')

    def get_input_curr_auto(self):
        """Queries the electric current auto range on/off
        statuses of all elements."""
        return self.heromix.query(':INP:CURR:AUTO?')

    def set_input_curr_auto(self, onoff=''):
        """Collectively sets the electric current auto range
        on/off status of all elements.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:CURR:AUTO ' + onoff)

    def set_input_curr_auto_element(self, x='0', onoff=''):
        """Sets or queries the electric current auto range
        on/off status of the specified element.
        x: '1' to '6'
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:CURR:AUTO:ELEM' + x + ' ' + onoff)

    def set_input_curr_auto_sigm(self, typ='', onoff=''):
        """Collectively sets the electric current auto range
        on/off status of all the elements that belong to the
        specified wiring unit (ΣA, ΣB, or ΣC).
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:CURR:AUTO:' + typ + ' ' + onoff)

    def get_input_curr_config(self):
        """Queries the valid electric current ranges of all
        elements."""
        return self.heromix.query(':INP:CURR:CONF?')

    def set_input_curr_config_all(self, val1='', *argv):
        """Collectively sets the valid electric current range of
        all elements.
        val1:
            • 50 A input elements
            • When the crest factor is set to 3:
            1 A, 2 A, 5 A, 10 A, 20 A, 50 A
            • When the crest factor is set to 6:
            500 mA, 1 A, 2.5 A, 5 A, 10 A, 25 A
            • 5 A input elements
            • When the crest factor is set to 3:
            10 mA, 20 mA, 50 mA, 100 mA,
            200 mA, 500 mA, 1 A, 2 A, 5 A
            • When the crest factor is set to 6:
            5 mA, 10 mA, 25 mA, 50 mA,
            100 mA, 250 mA, 500 mA, 1 A, 2.5 A
        """
        if len(argv) != 0:
            for tval in argv:
                val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:CURR:CONF:ALL ' + val1)

    def set_input_curr_config_element(self, x='0', val1='', *argv):
        """Sets or queries the valid electric current range of
        the specified element.
        val1: 'ALL'|<current>
        """
        if val1 != 'ALL':
            if len(argv) != 0:
                for tval in argv:
                    val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:CURR:CONF:ELEM' + x + ' ' + val1)

    def get_input_curr_extsensor(self):
        """Queries all external current sensor range settings."""
        return self.heromix.query(':INP:CURR:EXTS?')

    def get_input_curr_extsensor_config(self):
        """Queries the valid external current sensor ranges
        of all elements."""
        return self.heromix.query(':INP:CURR:EXTS:CONF?')

    def set_input_curr_extsensor_config_all(self, val1='', *argv):
        """Collectively sets the valid external current sensor
        range of all elements.
        val1: 'ALL'|<Voltage>
        • When the crest factor is set to 3:
        <Voltage> = 50 mV, 100 mV, 200 mV, 500 mV,
        1 V, 2 V, 5 V, 10 V
        • When the crest factor is set to 6:
        <Voltage> = 25 mV, 50 mV, 100 mV, 250 mV,
        500 mV, 1 V, 2.5 V, 5 V
        """
        if len(argv) != 0:
            for tval in argv:
                val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:CURR:CONF:EXTS:ALL ' + val1)

    def set_input_curr_extsensor_config_element(self, x='0', val1='', *argv):
        """Sets or queries the valid external current sensor
        ranges of the specified element.
        val1: 'ALL'|<Voltage>
            • When the crest factor is set to 3:
            <Voltage> = 50 mV, 100 mV, 200 mV, 500 mV,
            1 V, 2 V, 5 V, 10 V
            • When the crest factor is set to 6:
            <Voltage> = 25 mV, 50 mV, 100 mV, 250 mV,
            500 mV, 1 V, 2.5 V, 5 V
        """
        if val1 != 'ALL':
            if len(argv) != 0:
                for tval in argv:
                    val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:CURR:EXTS:CONF:ELEM' + x + ' ' + val1)

    def set_input_curr_extsensor_display(self, argv=''):
        """Sets or queries the display mode of the external
        current sensor range.
        argv: 'DIR'|'MEAS'
        """
        self.heromix.write(':INP:CURR:EXTS:DISP ' + argv)

    def get_input_curr_extsensor_pojump(self):
        """Queries the jump destination ranges of all
        elements that are used when a current peak overrange
        occurs."""
        return self.heromix.query(':INP:CURR:EXTS:POJ?')

    def set_input_curr_extsensor_pojump(self, argv=''):
        """Collectively sets the jump destination range of all
        elements that is used when a current peak overrange
        occurs.
        argv: 'OFF'|'<voltage>'
        if crest factor == 3: <voltage> = 50, 100, 200, 500 mV, 1, 2, 5, 10 V
        if crest factor == 6: <voltage> = 25, 50, 100, 250, 500 mV, 1, 2.5, 5 V
        """
        self.heromix.write(':INP:CURR:EXTS:POJ ' + argv)

    def set_input_curr_extsensor_pojump_element(self, x='0', argv=''):
        """Sets or queries the jump destination range of the
        specified element that is used when a current
        peak over-range occurs.
        x: '1' to '6'
        argv: 'OFF'|'<voltage>'
        if crest factor == 3: <voltage> = 50, 100, 200, 500 mV, 1, 2, 5, 10 V
        if crest factor == 6: <voltage> = 25, 50, 100, 250, 500 mV, 1, 2.5, 5 V
        """
        self.heromix.write(':INP:CURR:EXTS:POJ:ELEM' + x + ' ' + argv)

    def get_input_curr_pojump(self):
        """Queries the jump destination ranges of all
        elements that are used when a current peak overrange
        occurs."""
        return self.heromix.query(':INP:CURR:POJ?')

    def set_input_curr_pojump(self, argv=''):
        """Collectively sets the jump destination range of all
        elements that is used when a current peak overrange
        occurs.
        argv: 'OFF'|'<Current>'
        • 50 A input elements
        • When the crest factor is set to 3:
        <Current> = 1 A, 2 A, 5 A, 10 A, 20 A, 50 A
        • When the crest factor is set to 6:
        <Current> = 500 mA, 1 A, 2.5 A, 5 A, 10 A,
        25 A
        • 5 A input elements
        • When the crest factor is set to 3:
        <Current> = 10 mA, 20 mA, 50 mA, 100 mA,
        200 mA, 500 mA, 1 A, 2 A, 5 A
        • When the crest factor is set to 6:
        <Current> = 5 mA, 10 mA, 25 mA, 50 mA,
        100 mA, 250 mA, 500 mA, 1 A, 2.5 A
        """
        self.heromix.write(':IPN:CURR:POJ ' + argv)

    def get_input_curr_range(self):
        """Queries the electric current ranges of all
        elements."""
        return self.heromix.query(':INP:CURR:RANG?')

    def set_input_curr_range(self, flag=0, argv=''):
        """Collectively sets the electric current range of all
        elements.
        flag: 0|1
        argv: '<Current>'|'<Voltage>'
        """
        if flag == 0:
            self.heromix.write(':INP:CURR:RANG ' + argv)
        else:
            self.heromix.write(':INP:CURR:RANG EXT,' + argv)

    def set_input_curr_range_element(self, flag=0, x='0', argv=''):
        """Sets or queries the electric current range of the
        specified element.
        x: '1' to '6'
        argv: '<Current>'|'<Voltage>'
        """
        if flag == 0:
            self.heromix.write(':INP:CURR:RANG:ELEM' + x + ' ' + argv)
        else:
            self.heromix.write(':INP:CURR:RANG:ELEM' + x + ' EXT,' + argv)

    def set_input_curr_range_sigm(self, flag=0, typ='', argv=''):
        """Collectively sets the electric current range of all
        the elements that belong to the specified wiring
        unit (ΣA, ΣB, or ΣC).
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        argv: '<Current>'|'<Voltage>'
        """
        if flag == 0:
            self.heromix.write(':INP:CURR:RANG:' + typ + ' ' + argv)
        else:
            self.heromix.write(':INP:CURR:RANG:ELEM' + typ + ' EXT,' + argv)

    def get_input_curr_sratio(self):
        """Queries the external current sensor conversion
        ratios of all elements."""
        return self.heromix.query(':INP:CURR:SRAT?')

    def set_input_curr_sratio(self, argv=''):
        """Collectively sets the external current sensor
        conversion ratios of all elements.
        argv: '0.0001' to '99999.9999'
        """
        self.heromix.write(':INP:CURR:SRAT ' + argv)

    def set_input_curr_sratio_element(self, x='0', argv=''):
        """Sets or queries the external current sensor
        conversion ratio of the specified element.
        X: '1' to '6'
        argv: '0.0001' to '99999.9999'
        """
        self.heromix.write(':INP:CURR:SRAT:ELEM' + x + ' ' + argv)

    def set_input_curr_sratio_sigm(self, typ='', argv=''):
        """Collectively sets the external current sensor
        conversion ratios of all the elements that belong
        to the specified wiring unit (ΣA, ΣB, or ΣC).
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        argv: '0.0001' to '99999.9999'
        """
        self.heromix.write(':INP:CURR:SRAT:' + typ + ' ' + argv)

    def set_input_eselect(self, argv=''):
        """Sets or queries the element whose measurement
        range will be set.
        argv: '1' to '6'| 'ALL'
        """
        self.heromix.write(':INP:ESEL ' + argv)

    def get_input_filter(self):
        """Queries all input filter settings."""
        return self.heromix.query(':INP:FILT?')

    def get_input_filter_freq(self):
        """Queries the frequency filters of all elements."""
        return self.heromix.query(':INP:FILT:FREQ?')

    def set_input_filter_freq(self, argv=''):
        """Collectively sets the frequency filter of all elements.
        argv: 'OFF'|'<Frequency>'
        <Frequency> = 100， 1000 kHz
        """
        self.heromix.write(':INP:FILT:FREQ ' + argv)

    def set_input_filter_freq_element(self, x='0', argv=''):
        """Sets or queries the frequency filter of the
        specified element.
        x: '1' to '6'
        argv: 'OFF'|'<Frequency>'
        <Frequency> = 100， 1000 kHz
        """
        self.heromix.write(':INP:FILT:FREQ:ELEM' + x + ' ' + argv)

    def get_input_filter_line(self):
        """Queries the line filters of all elements."""
        return self.heromix.query(':INP:FILT:LINE?')

    def set_input_filter_line(self, argv=''):
        """Collectively sets the line filter of all elements.
        argv: 'OFF'|'<Frequency>'
        <Frequency> = 0.1kHz to 100.0kHz,300kHz,1MHz
        """
        self.heromix.write(':INP:FILT:LINE ' + argv)

    def set_input_filter_line_element(self, x='0', argv=''):
        """Sets or queries the line filter of the specified
        element.
        x: '1' to '6'
        argv: 'OFF'|'<Frequency>'
        <Frequency> = 0.1kHz to 100.0kHz,300kHz,1MHz
        """
        self.heromix.write(':INP:FILT:LINE:ELEM' + x + ' ' + argv)

    def get_input_scaling(self):
        """Queries all scaling settings."""
        return self.heromix.query(':INP:SCAL?')

    def get_input_scaling_state(self):
        """Queries the on/off statuses of the scaling of all
        elements."""
        return self.heromix.query(':INP:SCAL:STAT?')

    def set_input_scaling_state(self, onoff=''):
        """Collectively sets the on/off status of the scaling of
        all elements.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:SCAL:STAT ' + onoff)

    def set_input_scaling_state_element(self, x='0', onoff=''):
        """Sets or queries the on/off status of the scaling of
        the specified element.
        x: '1' to '6'
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:SCAL:STAT:ELEM' + x + ' ' + onoff)

    def get_input_scaling_VTCT(self, typ=''):
        """Queries the VT ratios, CT ratios, or power
        coefficients of all elements.
        typ: 'VT'|'CT'|'SFAC'
        """
        return self.heromix.query(':INP:SCAL:' + typ)

    def set_input_scaling_VTCT(self, typ='', argv=''):
        """Collectively sets the VT ratio, CT ratio, or power
        coefficient of all elements.
        typ: 'VT'|'CT'|'SFAC'
        argv: '0.0001' to '99999.9999'
        """
        self.heromix.write(':INP:SCAL:' + typ + ' ' + argv)

    def set_input_scaling_VTCT_element(self, x='0', typ='', argv=''):
        """Sets or queries the VT ratio, CT ratio, or power
        coefficient of the specified element.
        x: '1' to '6'
        typ: 'VT'|'CT'|'SFAC'
        argv: '0.0001' to '99999.9999'
        """
        self.heromix.write(':INP:SCAL:' + typ + ':ELEM' + x + ' ' + argv)

    def get_input_volt(self):
        """Queries all voltage measurement settings."""
        return self.heromix.query(':INP:VOLT?')

    def get_input_volt_auto(self):
        """Queries the voltage auto range on/off statuses of
        all elements."""
        return self.heromix.query('INP:VOLT:AUTO?')

    def set_input_volt_auto(self, onoff=''):
        """Collectively sets the voltage auto range on/off
        status of all elements.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:VOLT:AUTO ' + onoff)

    def set_input_volt_auto_element(self, x='0', onoff=''):
        """Sets or queries the voltage auto range on/off
        status of the specified element.
        x: '1' to '6'
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:VOLT:AUTO:ELEM' + x + ' ' + onoff)

    def set_input_volt_auto_sigm(self, typ='', onoff=''):
        """Collectively sets the voltage auto range on/off
        status of all the elements that belong to the
        specified wiring unit (ΣA, ΣB, or ΣC).
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':INP:VOLT:AUTO:' + typ + ' ' + onoff)

    def get_input_config(self):
        """Queries the valid voltage ranges of all elements."""
        return self.heromix.query(':INP:VOLT:CONF?')

    def set_input_volt_config(self, val1='', *argv):
        """Collectively sets the valid voltage range of all
        elements.
        val1: 'ALL'|'<Voltage>'
            • When the crest factor is set to 3:
            <Voltage> = 1.5 V, 3 V, 6 V, 10 V, 15 V, 30 V,
            60 V, 100 V, 150 V, 300 V, 600 V, 1000 V
            • When the crest factor is set to 6:
            <Voltage> = 0.75 V, 1.5 V, 3 V, 5 V, 7.5 V, 15 V,
            30 V, 50 V, 75 V, 150 V, 300 V, 500 V
        """
        if len(argv) != 0:
            for tval in argv:
                val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:VOL:CONF:ALL ' + val1)

    def set_input_volt_config_element(self, x='0', val1='', *argv):
        """Sets or queries the valid voltage ranges of the
        specified element.
        val1: 'ALL'|<voltage>
        """
        if val1 != 'ALL':
            if len(argv) != 0:
                for tval in argv:
                    val1 = val1 + ',' + str(tval)
        self.heromix.write(':INP:VOLT:CONF:ELEM' + x + ' ' + val1)

    def get_input_volt_pojump(self):
        """Queries the jump destination ranges of all
        elements that are used when a voltage peak overrange
        occurs."""
        return self.heromix.query(':INP:VOLT:POJ?')

    def set_input_volt_pojump(self, argv=''):
        """Collectively sets the jump destination range of all
        elements that is used when a voltage peak overrange
        occurs.
        argv: 'OFF'|'<Current>'
        • When the crest factor is set to 3:
        <Voltage> = 1.5 V, 3 V, 6 V, 10 V, 15 V, 30 V,
        60 V, 100 V, 150 V, 300 V, 600 V, 1000 V
        • When the crest factor is set to 6:
        <Voltage> = 0.75 V, 1.5 V, 3 V, 5 V, 7.5 V, 15 V,
        30 V, 50 V, 75 V, 150 V, 300 V, 500 V
        """
        self.heromix.write(':IPN:VOLT:POJ ' + argv)

    def get_input_volt_range(self):
        """Queries the electric voltage ranges of all
        elements."""
        return self.heromix.query(':INP:VOLT:RANG?')

    def set_input_volt_range(self, argv=''):
        """Collectively sets the electric voltage range of all
        elements.
        flag: 0|1
        argv: '<Voltage>'
        """
        self.heromix.write(':INP:VOLT:RANG ' + argv)

    def set_input_volt_range_element(self, x='0', argv=''):
        """Sets or queries the electric voltage range of the
        specified element.
        x: '1' to '6'
        argv: '<Voltage>'
        """
        self.heromix.write(':INP:VOLT:RANG:ELEM' + x + ' ' + argv)

    def set_input_volt_range_sigm(self, typ='', argv=''):
        """Collectively sets the electric voltage range of all
        the elements that belong to the specified wiring
        unit (ΣA, ΣB, or ΣC).
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        argv: '<Voltage>'
        """
        self.heromix.write(':INP:VOLT:RANG:' + typ + ' ' + argv)

    def get_numeric_normal(self):
        """Queries all numeric data output settings."""
        return self.heromix.query(':NUM:NORM?')

    def set_numeric_normal_clear(self, first='', second=''):
        """Clears numeric data output items (sets the items
        to NONE).
        first: '1' to '255'
        second: '1' to '255'
        """
        self.heromix.write(':NUM:NORM:CLE ' + first + ',' + second)

    def set_numeric_normal_delete(self, first='', second=''):
        """Deletes numeric data output items.
        first: '1' to '255'
        second: '1' to '255'
        """
        self.heromix.write('NUM:NORM:DEL ' + first + ',' + second)

    def set_numeric_normal_item(self, x='0', func='', elem='', order=''):
        """Sets or queries the specified numeric data output
        item (function, element, and harmonic order).
        x: '1' to '255'
        func: 'URMS'|'IRMS'|'P'|'S'|'Q'|...
        elem: '<NRf>'('1' to '6')|'SIGMA'|'SIGMB'|'SIGMC'
        order: 'TOT'|'DC'|'<NRf>'('1' to '500')
        """
        if elem != '':
            elem = ',' + elem
        if order != '':
            order = ',' + order
        self.heromix.write(':NUM:NORM:ITEM' + x + func + elem + order)

    def set_numeric_normal_num(self, argv=''):
        """Sets or queries the number of numeric data items
        that are transmitted by the :NUMeric[:NORMal]:
        VALue? command.
        argv: '<NRf>'|'ALL'  '<NRf>' = '1' to '255'
        """
        self.heromix.write(':NUM:NORM:NUM ' + argv)

    def set_numberic_normal_preset(self, argv=''):
        """Presets the numeric data output item pattern.
        argv: '1' to '4'
        """
        self.heromix.write(':NUM:NORM:PRES ' + argv)

    def get_numeric_normal_value(self, argv=''):
        """Queries the numeric data.
        argv: '1' to '255'
        """
        return self.heromix.query(':NUM:NORM:VAL? ' + argv)

    def get_numeric_list(self):
        """Queries all harmonic measurement numeric list
        data output settings."""
        return self.heromix.query(':NUM:LIST?')

    def set_numeric_list_clear(self, first='', second=''):
        """Clears harmonic measurement numeric list data
        output items (sets the items to NONE).
        first: '1' to '255'
        second: '1' to '255'
        """
        self.heromix.write(':NUM:LIST:CLE ' + first + ',' + second)

    def set_numeric_list_delete(self, first='', second=''):
        """Deletes harmonic measurement numeric list data
        output items.
        first: '1' to '64'
        second: '1' to '64'
        """
        self.heromix.write(':NUM:LIST:DEL ' + first + ',' + second)

    def set_numeric_list_num(self, argv=''):
        """Sets or queries the number of numeric list data
        items that are transmitted by :NUMeric:LIST:
        VALue?.
        argv: '1' to '64'|'ALL'
        """
        self.heromix.write(':NUM:LIST:NUM ' + argv)

    def set_numeric_list_order(self, argv=''):
        """Sets or queries the maximum output harmonic
        order of the harmonic measurement numeric list
        data.
        argv: 'ALL'
        """
        self.heromix.write(':NUM:LIST:ORD ' + argv)

    def set_numeric_list_preset(self, argv=''):
        """Presets the harmonic measurement numeric list
        data output item pattern.
        argv: '1' to '4'
        """
        self.heromix.write(':NUM:LIST:PRES ' + argv)

    def set_numeric_list_select(self, argv=''):
        """Sets or queries the output components of the
        harmonic measurement numeric list data.
        argv: 'EVEN'|'ODD'|'ALL'
        """
        self.heromix.write(':NUM:LIST:SEL ' + argv)

    def get_numeric_list_value(self, argv=''):
        """Queries the harmonic measurement numeric list
        data.
        argv: '1' to '64'
        """
        return self.heromix.write(':NUM:LIST:VAL? ' + argv)

    def get_meas(self):
        """Queries all computation settings."""
        return self.heromix.query(':MEAS?')

    def get_meas_averaging(self):
        """Queries all averaging settings."""
        return self.heromix.qury(':MEAS:AVER?')

    def get_meas_averaging_count(self, argv=''):
        """Sets or queries the averaging coefficient.
        argv:
        '<NRf>' = '2' to '64' (attenuation constant
        when TYPE = EXPonent)
        '<NRf>' = '8' to '64' (moving average
        count when TYPE = LINear)
        """
        self.heromix.write(':MEAS:AVER:COUN ' + argv)

    def set_meas_averaging_state(self, onoff=''):
        """Sets or queries the on/off status of averaging.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':MEAS:AVER:STAT ' + onoff)

    def set_meas_averaging_type(self, argv=''):
        """Sets or queries the averaging type.
        argv: 'EXP'|'LIN'
        """
        self.heromix.write(':MEAS:AVER:TYPE ' + argv)

    def set_meas_dmeas(self):
        """Queries all delta computation settings."""
        return self.heromix.write(':MEAS:DM?')

    def set_meas_dmeas_mode(self, argv=''):
        """Sets or queries the voltage or current mode that
        is used in delta computation.
        argv: 'RMS'|'MEAN'|'DC'|'RMEAN'|'AC'
        """
        self.heromix.write(':MEAS:DM:MODE ' + argv)

    def set_meas_dmeas_sigm(self, typ='', argv=''):
        """Sets or queries the delta computation mode for
        wiring unit ΣA, ΣB, or ΣC.
        typ: 'SIGMA'|'SIGMB'|'SIGMC'
        argv: 'OFF'|'DIFF'|'P3W3_V3A3'|'ST_DT'|'DT_ST'
        """
        self.heromix.write(':MEAS:DM:' + argv)

    def get_meas_efficiency(self):
        """Queries all efficiency computation settings."""
        return self.heromix.query(':MEAS:EFF?')

    def get_image(self):
        """Queries all screen image data output settings."""
        return self.heromix.query(':IMAG?')

    def set_image_abort(self):
        """Aborts a screen image data output operation."""
        self.heromix.write(':IMAG:ABOR')

    def set_image_color(self, argv=''):
        """Sets or queries the color tone of the screen
        image data that will be saved.
        argv: 'OFF'|'COL'|'REV'|'GRAY'
        """
        self.heromix.write(':IMAG:COL ' + argv)

    def set_image_comment(self, comment=''):
        """Sets or queries the comment displayed at the
        bottom of the screen.
        comment: string up to 30 characters
        """
        self.heromix.write(':IMAG:COMM ' + comment)

    def set_image_execute(self):
        """Executes a screen image data output operation."""
        self.heromix.write(':IMAG:EXEC')

    def set_image_format(self, argv=''):
        """Sets or queries the format of the screen image
        data that will be saved.
        argv: 'BMP'|'PNG'|'JPEG'
        """
        self.heromix.write(':IMAG:FORM ' + argv)

    def get_image_save(self):
        """Queries all screen image data save settings."""
        return self.heromix.query(':IMAG:SAVE?')

    def set_image_save_anaming(self, argv=''):
        """Sets or queries the auto naming feature for
        saving files.
        argv: 'OFF'|'NUMB'|'DATE'
        """
        self.heromix.write(':IMAG:SAVE:ANAM ' + argv)

    def set_image_save_cdir(self, name=''):
        """Changes the directory that screen image data is
        saved to.
        name: string
        """
        self.heromix.write(':IMAG:SAVE:CDIR ' + name)

    def set_image_save_drive(self, argv=''):
        """Sets the drive that screen image data is saved to.
        argv: 'RAM'|'USB[,<NRf>|NETW]'
        """
        self.heromix.write(':IMAG:SAVE:DRIV ' + argv)

    def get_image_save_free(self):
        """Queries the free space (in bytes) on the drive that
        the screen image data is saved to."""
        return self.heromix.query(':IMAG:SAVE:FREE?')

    def set_image_save_name(self, name=''):
        """Sets or queries the name of the file that will be
        saved.
        name: string file name
        """
        self.heromix.write(':IMAG:SAVE:NAME ' + name)

    def get_image_save_path(self):
        """Queries the absolute path of the directory that the
        screen image data is saved to."""
        return self.heromix.query(':IMAG:SAVE:PATH?')

    def get_image_send(self):
        """Queries the screen image data."""
        return self.heromix.query(':IMAG:SEND?')

    def get_harmonics(self, x=''):
        """Queries all harmonic measurement settings.
        x: '1' to '2'
        """
        return self.heromix.query(':HARM' + x + '?')

    def get_harmonics_configure(self):
        """Queries the harmonic measurement groups of all
        elements.
        """
        return self.heromix.query(':HARM:CONF?')

    def set_harmonics_configure(self, argv=''):
        """Collectively sets the harmonic measurement
        group of all elements.
        x: no meaning
        argv: '1', '2'
        """
        self.heromix.write(':HARM:CONF ' + argv)

    def set_harmonics_configure_element(self, x='', argv=''):
        """Sets or queries the harmonic measurement group
        of the specified element.
        x: '1' to '6'
        argv: '1', '2'
        """
        self.heromix.write(':HARM:CONF:ELEM' + x + ' ' + argv)

    def set_harminocs_order(self, x='', first='', second=''):
        """Sets or queries the maximum and minimum
        harmonic orders that are analyzed.
        x: '1' or '2'
        first: '0' or '1'
        second: '1' to '500'
        """
        self.heromix.write(':HARM' + x + 'ORD ' + first + ',' + second)

    def set_harmonics_pllsource(self, x='', argv=''):
        """Sets or queries the PLL source.
        x: '1' or '2'
        argv: 'U1'~'U6'|'I1'~'I6'|'EXT'
        """
        self.heromix.write(':HARM' + x + ':PLLS ' + argv)

    def set_harmonics_THD(self, x='0', argv=''):
        """Sets or queries the equation used to compute the
        THD (total harmonic distortion).
        x: '1' or '2'
        argv: 'TOT'|'FUND'
        """
        self.heromix.write(':HARM' + x + ':THD ' + argv)

    def get_harmonics_THD(self, x=''):
        """Sets or queries the equation used to compute the
        THD (total harmonic distortion)."""
        return self.heromix.query(':HARM' + x + ':THD?')

    def get_cursor_wave(self):
        """Queries all waveform display cursor measurement
        settings."""
        return self.heromix.query(':CURS:WAVE?')

    def set_cursor_wave_linkage(self, onoff=''):
        """Sets or queries the on/off status of the cursor
        position linkage on the waveform display.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write('CURS:WAVE:LINK ' + onoff)

    def set_cursor_wave_path(self, argv=''):
        """Sets or queries the cursor path on the waveform
        display.
        argv: 'U1'~'U6'|'I1'~'I6'|'SPE'|'TORQ'|'AUX1'~'AUX2'
        """
        self.heromix.write(':CURS:WAVE:TRAC' + ' ' + argv)

    def set_cursor_wave_position(self, x='', argv=''):
        """Sets or queries the position of the specified
        cursor on the waveform display.
        x: '1', '2'
        argv: '0' to '800'
        """
        self.heromix.write('CURS:WAVE:POS' + x + ' ' + argv)

    def set_cussor_wave_state(self, onoff=''):
        """Sets or queries the on/off status of the cursor
        display on the waveform display.
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':CURS:WAVE:STAT ' + onoff)

    def set_cursor_wave_trace(self, x='', argv=''):
        """Sets or queries the target of the specified cursor
        on the waveform display.
        x: '1', '2'
        argv: 'U1'~'U6'|'I1'~'I6'|'SPE'|'TORQ'|'AUX1'~'AUX2'
        """
        self.heromix.write(':CURS:WAVE:TRAC' + x + ' ' + argv)

    def get_communicate(self):
        """Queries all communication settings."""
        return self.heromix.query(':COMM?')

    def set_communicate_header(self, onoff=''):
        """Sets or queries whether a header is added to the
        response to a query. (Example with header: “:
        DISPLAY:MODE NUMERIC.” Example without
        header: “NUMERIC.”)
        onoff: 'OFF'|'ON'
        """
        self.heromix.write(':COMM:HEAD ' + onoff)

    def set_communicate_lockout(self, onoff=''):
        """Sets or clears local lockout."""
        self.heromix.write(':COMM:LOCK ' + onoff)

    def set_file_drive(self, argv=''):
        self.heromix.write(':FILE:DRIV ' + argv)

    def set_file_save(self, name=''):
        self.heromix.write(':FILE:SAVE:WAVE:EXEC ' + name)


if __name__ == '__main__':
    myPowerAls = PowerAnalyzer('TCPIP0::10.44.90.29::INSTR')
    # print(myPowerAls.IDN())
    # myPowerAls.RST()
    myPowerAls.set_disp_mode('WAVE')
    print(myPowerAls.get_disp())
