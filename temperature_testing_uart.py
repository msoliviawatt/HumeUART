#!/usr/bin/env python3
import serial
import time
import argparse
import serial.tools.list_ports


# Define the argument parser and process command line arguments
def formatter(prog): return argparse.HelpFormatter(prog, indent_increment=2, max_help_position=60, width=120)
p = argparse.ArgumentParser(formatter_class=formatter, description=__doc__)
p.add_argument('--port', default='COM4')
p.add_argument('--baud', default=115200, type=int, help='baud rate (Hz)')
args = p.parse_args()

def parity_byte( in_command_bytes ):
    output_byte = 0
    for byte in in_command_bytes:
        output_byte = int( hex(byte ^ output_byte),16)
    print(str(output_byte))
    print(hex(output_byte))
    return output_byte

try:
    ports = serial.tools.list_ports.comports()
    for port,desc,hwid in sorted(ports):
        print("{}: {} [{}]".format(port,desc,hwid))
    with serial.Serial('COM4', args.baud, timeout=1) as ser:
        print('here1')
        data_bytes = [0xaa,0x55, 0x00, 0x01, 0x01]
        #data_bytes = [0xaa,0x55, 0x02, 0x08, 0x00,0x02,0xcb,0x41,0x78,0x00,0x00,0x00,0x05]
        data_bytes.append( parity_byte(data_bytes) )
        
        ser.write(serial.to_bytes(data_bytes))
        ser.flush()
        read_line = ser.readline()
        print(f"Received: {read_line}")
        print('received decoded: ' + read_line.hex())
        ser.close()
except IOError:
    print("cry")
    ser.close()