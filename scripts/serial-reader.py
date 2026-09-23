import serial
import struct
import sys

# Configuration
PORT = 'COM5'
BAUD_RATE = 115200

try:
    # The 'with' statement ensures the port is automatically closed when the script ends
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Listening on {PORT} at {BAUD_RATE} baud... (Press Ctrl+C to stop)")
        
        while True:
            # Look for the 0x55 start byte
            if ser.read(1) == b'\x55':
                # Look for the 0xAA second header byte
                if ser.read(1) == b'\xFC':
                    raw_bytes = ser.read(12)
                                            
                    # Ensure we actually received exactly 12 bytes before unpacking
                    if len(raw_bytes) == 12:
                        # Unpack 6 Big-Endian (>) 16-bit unsigned integers (H)
                        channels = struct.unpack('>HHHHHH', raw_bytes)
                                                
                        # channels is now a tuple: (ch1, ch2, ch3, ch4, ch5, ch6)
                        print(f"Ch1: {channels[0]} | Ch2: {channels[1]} | Ch3: {channels[2]} | Ch4: {channels[3]} | Ch5: {channels[4]} | Ch6: {channels[5]}")
                    else:
                        print("Warning: Incomplete packet received.")

except serial.SerialException as e:
    print(f"Serial Port Error: {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nExiting gracefully...")
    sys.exit(0)