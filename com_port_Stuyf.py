import serial
import serial.tools.list_ports
import crc16_Stuyf
import time
import graph_main


class OaiDDData:
    def __init__(self):

        self.data = {}
        self.graph_data = None

    def create_table_data(self):
        pass

    def create_graph_data(self):
        pass

    def reset_graph_data(self):
        self.graph_data = {}

    def __str__(self):
        pass


class OaiSerial(serial.Serial):
    def __init__(self, **kw):
        serial.Serial.__init__(self)
        self.serial_numbers = []  # это лист возможных серийников!!! (не строка)
        self.baudrate = 115200
        self.timeout = 0.5
        self.self_id = 0x00
        self.dev_id = 0x00
        self.seq_num = 0
        self.port = "COM0"
        self.row_data = b""
        self.state = 0
        self.data = graph_main.MAINWindow
        for key in sorted(kw):
            if key == "serial_numbers":
                self.serial_numbers = kw.pop(key)
            elif key == "baudrate":
                self.baudrate = kw.pop(key)
            elif key == "timeout":
                self.baudrate = kw.pop(key)
            elif key == "port":
                self.baudrate = kw.pop(key)
            elif key == "self_id":
                self.self_id = kw.pop(key)
            elif key == "dev_id":
                self.dev_id = kw.pop(key)
            elif key == "data":
                self.data = kw.pop(key)
            else:
                pass
        self.error_string = "No error"
        self.temperature_pars_data = {}
        self.sensors_numbers = 0

    def open_id(self):  # функция для установки связи с КПА
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            # print(com)
            for serial_number in self.serial_numbers:
                # print(com.serial_number, serial_number)
                if com.serial_number is not None:
                    if com.serial_number.find(serial_number) >= 0:
                        # print(com.device)
                        self.port = com.device
                        try:
                            self.open()
                        except serial.serialutil.SerialException as error:
                            self.error_string = str(error)
                    self.state = 1
                    self.error_string = "Переподключение успешно"
                    return True
        self.state = 0
        return False
        pass

    def serial_close(self):
        self.close()

    def request(self, req_type="test", data=[]):
        if req_type == "test":
            com = 0x00
            answer_leng = 8
        elif req_type == "get_temperature":
            com = 0x01
            answer_leng = 8
        elif req_type == "set_dac":
            com = 0x02
            answer_leng = 10
        #elif req_type == "connect":

        else:
            com = 0x00
            answer_leng = 8
            pass
        # сборка команды
        leng = len(data)
        com_data = [self.dev_id, self.self_id, self.seq_num, 0x00, com, leng]
        com_data.extend(data)
        crc16 = crc16_Stuyf.calc(com_data, len(com_data))
        com_data.extend([(crc16 >> 8) & 0xFF, (crc16 >> 0) & 0xFF])
        if self.is_open:
            try:
                self.read(self.inWaiting())
                self.write(bytes(com_data))
                self.row_data = self.read(size=answer_leng)

                try:
                    if com == 0x01 and self.row_data[5]>0:
                        self.row_data+=self.read(self.row_data[5])
                except Exception as error:
                    print(error)

            except serial.serialutil.SerialException as error:
                self.error_string = str(error)
                self.close()
                self.state = 0
            self.parcing()
        else:
            self.state = 0
            self.open_id()

    def parcing(self):
        if len(self.row_data) > 5:
            if self.row_data[0] == self.self_id and self.row_data[1] == self.dev_id:
                if self.row_data[3] == 0x00 and self.row_data[4] == 0x00:  # тестовая команда
                    self.state = 0x01

                elif self.row_data[3] == 0x00 and self.row_data[4] == 0x01:  # команда на чтение температуры
                    if (len(self.row_data) == (self.row_data[5]+8)) and self.row_data[5]>0: # проверка длины сырых данных на то, что пакет целый
                        self.sensors_numbers = int(self.row_data[5]/6) # вычисление сколько термодатчиков есть на шине
                        self.sensors_serial_numbers  = [int.from_bytes(self.row_data[6+6*i:6*i+10], byteorder="big")for i in range(self.sensors_numbers)] # формирование списка серийников которые есть на шине
                        self.data.row_temperature_data = [int.from_bytes(self.row_data[10+i*6:12+i*6], byteorder="big") for i in range(self.sensors_numbers)] # формирование сырых данных температуры из тех что есть на шине
                        self.data.temperature_data = [float(self.data.row_temperature_data[i]/16) for i in range(self.sensors_numbers)] # формирование данных в градусах цельсия
                        self.temperature_row_to_data_dict() # создание словаря из данных
                        self.state = 0x01
                    else:
                        self.state = 0x00

                elif self.row_data[3] == 0x00 and self.row_data[4] == 0x02:  # команда на чтение данных из АЦП
                    if len(self.row_data) >= 5+2:
                        self.data.dac_data = int.from_bytes(self.row_data[6:8], byteorder="big")
                        self.state = 0x01
                    else:
                        self.state = 0x00
            else:
                self.state = 0x00
        else:
            self.state = 0x00
        pass

    def temperature_row_to_data_dict(self): # словарь данных температуры
        try:
            if (self.temperature_pars_data == {}): # если попали сюда первый раз
                self.temperature_pars_data.update({'Time' : [0]}) # Время нулевое
                for i in range(self.sensors_numbers): # вписываем первые значения температуры для датчиков
                    self.temperature_pars_data.update({self.sensors_serial_numbers[i]: [self.data.temperature_data[i]]})

            else: # если данные не пустые
                self.temperature_pars_data['Time'].append(time.clock()) # добавляем время
                for i in range(self.sensors_numbers): # в диапазоне серийников проверяем, есть ли такой серийник в словаре, если есть
                    try:
                        self.temperature_pars_data[self.sensors_serial_numbers[i]].append(self.data.temperature_data[i]) # просто добавляем ему значение температуры TODO тоже додпилить проверку длины
                    except KeyError:
                        self.temperature_pars_data.update({self.sensors_serial_numbers[i]: [self.data.temperature_data[i]]}) # если нет, то создаем новую пару ключ словарь ToDO дописать обработку добавленного датчика и проверку длины данных

            #print(self.temperature_pars_data)
            #
            #
            # self.data.plot(self, data = ['time',[1, 2, 3, 54],[2, 4, 6, 1]])

        except Exception as error:
             print(error)







    def bytes_to_string(self, data):
        bytes_str = ""
        for i in range(len(data)):
            bytes_str += '%02x ' % (data[i])
        return bytes_str
