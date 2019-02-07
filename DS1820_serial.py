import serial
import serial.tools.list_ports

import time
'''
Global variables
'''

rx_Buff = []
tx_Buff = []
rx_Buff = bytearray
tx_Buff = bytearray

#'A9CBNTXHA'
port_id_s = ['A9CBNTXHA']


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)

        except (OSError, serial.SerialException):
            pass
    return result


def open_id(id_list):  # функция для установки связи с КПА
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            #print(com)
            for serial_number in id_list:
                #print(com.serial_number, serial_number)
                if com.serial_number is not None:
                    if com.serial_number.find(serial_number) >= 0:
                        print(com.device)
                        port = com.device
                        return port
        return None


def Serial_port_read(serial_port, rx_Buff):
    rx_Buff
    data_Buff = []
    #[0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00]
    '''опрос ком порта'''
    if(serial_port.inWaiting()>=8):
        data_Buff = serial_port.read(8)
        rx_Buff.extend(data_Buff)
        if(rx_Buff[5]>0):
            data_Buff = []
            data_Buff = serial_port.read(rx_Buff[5])
            rx_Buff.extend(data_Buff)
        print(rx_Buff)
        #serial_port.write(tx_Buff)
        #rx_Buff = []
    #time.sleep(1000)
    #serial_port.write(tx_Buff)









if __name__ == '__main__':
    port = open_id(port_id_s)
    pass


