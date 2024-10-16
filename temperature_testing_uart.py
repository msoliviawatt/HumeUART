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


def set_frequency(new_frequency, attenuation):
    # command index is 0x02
    # data length is 8 bytes 
    # data: 6 bytes frequency, 2 bytes attenuation
    frequency_in_hex = hex(new_frequency)
    attenuation_in_hex = hex(attenuation)
    print(frequency_in_hex + ' ' + attenuation_in_hex)


set_frequency(10000, 10)


def list_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        print('here1')


def send_data(bytes_to_send: list):
    try:
        with serial.Serial('COM4', args.baud, timeout=1) as ser:
            ser.write(serial.to_bytes(bytes_to_send))
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




