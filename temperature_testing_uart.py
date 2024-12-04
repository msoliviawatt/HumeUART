import serial
import time
import argparse
import serial.tools.list_ports


# Define the argument parser and process command line arguments
def formatter(prog): return argparse.HelpFormatter(
    prog, indent_increment=2, max_help_position=60, width=120)


p = argparse.ArgumentParser(formatter_class=formatter, description=__doc__)
p.add_argument('--port', default='COM4')
p.add_argument('--baud', default=115200, type=int, help='baud rate (Hz)')
args = p.parse_args()


def parity_byte(in_command_bytes):
    output_byte = 0
    for byte in in_command_bytes:
        output_byte = int(hex(byte ^ output_byte), 16)
    print(str(output_byte))
    print(hex(output_byte))
    return output_byte

# set_frequency( int new_frequency, float attenuation) and
# would return the message bytes appropriate for this command. Try to implement
# commands for command indices: 0x00, 0x02, 0x05, 0x09, 0x31, 0x35, and 0x80.

# note that there is a resolution of 1 hz in this implementation
def set_frequency_1hz(new_frequency:int, attenuation:int):
    attenuation = attenuation * 10 
    # command index is 0x02
    # data length is 8 bytes 
    # data: 6 bytes frequency, 2 bytes attenuation
    frequency_in_hex = hex(new_frequency)
    attenuation_in_hex = hex(attenuation)
    print(frequency_in_hex + ' ' + attenuation_in_hex)
    frequency_bytes = new_frequency.to_bytes(6, byteorder='big')
    frequency_bytes = bytes_to_byte_array(frequency_bytes)
    attenuation_bytes = attenuation.to_bytes(2, byteorder='big')
    attenuation_bytes = bytes_to_byte_array(frequency_bytes)
    bytes = [0xaa, 0x55, 0x02]
    bytes.append(frequency_bytes)
    bytes.append(attenuation_bytes)
    return (bytes) # return not send

def set_frequency_1hz(new_frequency:int, attenuation:int):
    #command 0x05
    new_frequency = new_frequency * 10
    attenuation = attenuation * 10
    freq_bytes = new_frequency.to_bytes(6, byteorder='big')
    freq_bytes = bytes_to_byte_array(freq_bytes)
    atten_bytes = attenuation.to_bytes(2) 
    atten_bytes = bytes_to_byte_array(atten_bytes)
    print(freq_bytes + atten_bytes )
    return freq_bytes + atten_bytes



# freq = 100000
# print(freq.to_bytes(6, byteorder='big'))

def bytes_to_byte_array(data:str):
    data = str(data) 
    byte_list = data.split("\\x")
    data = data.replace('b', "")
    data = data.replace("'", "")
    data = data.replace("'", "")
    return data

def list_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        print('here1')

# note that this adds the parity bit
def send_data(bytes_to_send: list):
    try:
        with serial.Serial('COM4', args.baud, timeout=1) as ser:
            ser.write(serial.to_bytes(bytes_to_send + parity_byte(bytes_to_send)))
            ser.flush()
    except IOError:
        print("cry")
        ser.close()

def read_response():
    try:
        with serial.Serial('COM4', args.baud, timeout=1) as ser:
            read_line = ser.readline()
            print(f"Received: {read_line}")
            print('received decoded: ' + read_line.hex())
            ser.close()
    except IOError:
        print("cry")
        ser.close()




print(set_frequency_1hz(100, 20))
