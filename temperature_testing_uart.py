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

# for adding to set of bytes
def addBytes(data_bytes, command):
    for i in range (0, len(command), 2):
        bytes_add = command[i : i + 2]
        set_of_bytes = int(bytes_add, 16)
        data_bytes.append(set_of_bytes)
    
    return data_bytes

# set_frequency( int new_frequency, float attenuation) and 
# would return the message bytes appropriate for this command. Try to implement 
# commands for command indices: 0x00, 0x02, 0x05, 0x09, 0x31, 0x35, and 0x80.
def set_frequency1 (new_frequency, attenuation):
    # command index is 0x02
    # data length is 8 bytes
    # data: 6 bytes frequency, 2 bytes attenuation

    # Attenuation, step 0.1 dBm, and add up 1500
    attenuation = int(attenuation) * 10 + 1500

    frequency_in_hex = hex(new_frequency)[2:].zfill(12)  # padding to 12 digits for 6 bytes
    attenuation_in_hex = hex(attenuation)[2:].zfill(4)   # padding to 4 digits for 2 bytes

    full_command_hex = frequency_in_hex + attenuation_in_hex
    print(f"full command: {full_command_hex}")

    data_bytes = [0xaa,0x55, 0x02]

    data_bytes = addBytes(data_bytes, full_command_hex)
    
    print(f"Frequency in hex (6 bytes): {frequency_in_hex}")
    print(f"Attenuation in hex (2 bytes): {attenuation_in_hex}")
    print(f"Command in integer bytes: {data_bytes}")

    return data_bytes


# 0x05
# 6 bytes (Frequency, step 0.1 Hz) 
# 2 bytes (Attenuation, step 0.1 dBm, and add up 1500) 
def set_frequency2 (new_frequency, attenuation):
    new_frequency = int(new_frequency) * 10
    attenuation = int(attenuation) * 10

    frequency_in_hex = hex(new_frequency)[2:].zfill(12)
    attenuation_in_hex = hex(attenuation)[2:].zfill(4)

    command_in_hex = frequency_in_hex + attenuation_in_hex
    print(f"full command: {command_in_hex}")

    data_bytes = [0xaa,0x55, 0x05]

    # for i in range(0, len(command_in_hex), 2):
    #     bytes1 = command_in_hex[i:i + 2]
    #     set_of_bytes = int(bytes1, 16)
    #     data_bytes.append(set_of_bytes)

    data_bytes = addBytes(data_bytes, command_in_hex)
    
    print(f"Frequency in hex (6 bytes): {frequency_in_hex}")
    print(f"Attenuation in hex (2 bytes): {attenuation_in_hex}")
    print(f"Command in integer bytes: {data_bytes}")

    return data_bytes


# 0x08
# 0x01 Use Internal Reference
# 0x00 Use External Reference
# enter reference parameter as 'internal' or 'external'(?)
# 1 byte
# with string
def setReferenceClockWithString(reference):
    if (reference.lower() != 'internal' and reference.lower() != 'external'):
        return 'invalid input'
    
    if (reference.lower() == 'internal'):
        reference = 1
    elif (reference.lower() == 'external'):
        reference = 0

    reference_in_hex = hex(reference)[2:].zfill(2)

    data_bytes = [0xaa,0x55, 0x08]
    data_bytes = addBytes(data_bytes, reference_in_hex)

    # for testing purposes
    print(f"Reference parameter in hex (1 byte): {reference_in_hex}")
    print(f"Added command in bytes: {data_bytes}")

    return 

# when input is int
# 0x01 Use Internal Reference
# 0x00 Use External Reference
def setReferenceClockWithInt(reference):

    reference_in_hex = hex(reference)[2:].zfill(2)

    data_bytes = [0xaa,0x55, 0x08]
    data_bytes = addBytes(data_bytes, reference_in_hex)

    # for testing purposes
    print(f"Reference parameter in hex (1 byte): {reference_in_hex}")
    print(f"Added command in bytes: {data_bytes}")

    return data_bytes

# output switch
# 0x01 output ON
# 0x00 output OFF
def setOutputSwitchWithString(output):
    if (output.lower() != 'on' or output.lower() != 'off'):
        return 'invalid input'
    
    if (output.lower() == 'on'):
        output = 1
    elif (output.lower() == 'off'):
        output = 0

    # 1 byte, 2 hex digits
    output_in_hex = hex(output)[2:].zfill(2)

    data_bytes = [0xaa, 0x55, 0x09]
    data_bytes = addBytes(data_bytes, output_in_hex)

    # testing
    print(f"Output value in hex (1 byte): {output_in_hex}")
    print(f"Output switch command bytes: {data_bytes}")

    return data_bytes

# set output with int
# 0x01 output ON
# 0x00 output OFF

def setOutputSwitchWithInt(output):
    if (output != 0 and output != 1):
        return 'invalid input. please use 0 or 1'
    
    output_in_hex = hex(output)[2:].zfill(2)

    data_bytes = [0xaa, 0x55, 0x09]
    data_bytes = addBytes(data_bytes, output_in_hex)

    # testing
    print(f"Output value in hex (1 byte): {output_in_hex}")
    print(f"Output switch command bytes: {data_bytes}")

    return data_bytes

# 0x11
# 9 bytes

# type 1
# 1 byte (0x00, CW) 
# 8 bytes RESERVED; 

# type 2
# 1 byte (0x01, Internal Pulse) 
# 4 bytes (Pulse Period, unit ns) 
# 4 bytes (Pulse Width, unit ns) 

# type 3
# 1 byte (0x02, External Pulse) 
# 4 bytes (Pulse Period, unit ns, INVALID) 
# 4 bytes (Pulse Width, unit ns, INVALID)
# def configureModulation(config):

##################################
# testing 
##################################
print("----------------------------------------------")
print("testing")
print("----------------------------------------------")

print("set frequency to 10000 with attenuation 1")
print("----------------------------------------------")
set_frequency1(10000, 1)

print("set frequency to 1000 with attenuation 0.5")
print("----------------------------------------------")
set_frequency2(1000, 0.5)

print("set reference clock to external using string")
print("----------------------------------------------")
setReferenceClockWithString('external')

print("set reference clock to external using int")
print("----------------------------------------------")
setReferenceClockWithInt(0)

print("set output to on using int")
print("----------------------------------------------")
setOutputSwitchWithInt(1)

print("set output to on using string")
print("----------------------------------------------")
setOutputSwitchWithString('on')



# try:
#     ports = serial.tools.list_ports.comports()
#     for port,desc,hwid in sorted(ports):
#         print("{}: {} [{}]".format(port,desc,hwid))
#     with serial.Serial('COM4', args.baud, timeout=1) as ser:
#         print('here1')
#         data_bytes = [0xaa,0x55, 0x00, 0x01, 0x01]
#         #data_bytes = [0xaa,0x55, 0x02, 0x08, 0x00,0x02,0xcb,0x41,0x78,0x00,0x00,0x00,0x05]
#         data_bytes.append( parity_byte(data_bytes) )
        
#         ser.write(serial.to_bytes(data_bytes))
#         ser.flush()
#         read_line = ser.readline()
#         print(f"Received: {read_line}")
#         print('received decoded: ' + read_line.hex())
#         ser.close()
# except IOError:
#     print("cry")
#     # ser.close()
