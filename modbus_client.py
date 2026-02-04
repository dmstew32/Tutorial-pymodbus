"""
Modbus RTU Client
Sends Read Holding Registers (0x03) commands to test the server.
"""

import logging
from pymodbus.client import ModbusSerialClient
import time

# Set up logging to see what's happening
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


def read_registers(client, address, count, unit=0x9D):
    """
    Read holding registers from the server.
    
    Args:
        client: The Modbus client connection
        address: Starting register address (e.g., 0x01F4)
        count: Number of registers to read
        unit: Slave address (default 0x9D = 157)
    """
    print(f"\nReading {count} register(s) starting at address 0x{address:04X} ({address})...")
    
    try:
        # Send Read Holding Registers command (function code 0x03)
        result = client.read_holding_registers(
            address=address,
            count=count,
            device_id=unit
        )
        
        if result.isError():
            print(f"  ERROR: {result}")
        else:
            print(f"  SUCCESS: Read {len(result.registers)} register(s)")
            print(f"  Values: {result.registers}")
            return result.registers
            
    except Exception as e:
        print(f"  EXCEPTION: {e}")
    
    return None


def main():
    """
    Main function - connects to server and reads registers.
    """
    # Serial port settings (must match the server)
    PORT = "COM11"         # Change to your actual port (COM3, COM4, etc.)
    BAUDRATE = 9600
    BYTESIZE = 8
    PARITY = 'N'
    STOPBITS = 1
    TIMEOUT = 1
    
    print("=" * 60)
    print("Modbus RTU Client Starting...")
    print("=" * 60)
    print(f"Port:     {PORT}")
    print(f"Baudrate: {BAUDRATE}")
    print(f"Connecting to Slave Address: 0x9D (157)")
    print("=" * 60)
    
    # Create the client
    client = ModbusSerialClient(
        port=PORT,
        baudrate=BAUDRATE,
        bytesize=BYTESIZE,
        parity=PARITY,
        stopbits=STOPBITS,
        timeout=TIMEOUT
    )
    
    # Connect to the server
    if client.connect():
        print("\n✓ Connected to Modbus server!")
        
        # Give the connection a moment to stabilize
        time.sleep(0.5)
        
        # Test reading the specified registers
        print("\n" + "=" * 60)
        print("Testing Register Reads...")
        print("=" * 60)
        
        # Read register 0x0000
        read_registers(client, 0x0000, 1)
        
        # Read registers 0x0005-0x0008 (4 registers)
        read_registers(client, 0x0005, 4)
        
        # Read registers 0x0010-0x0012 (3 registers)
        read_registers(client, 0x0010, 3)
        
        # Read registers 0x001A-0x001F (6 registers)
        read_registers(client, 0x001A, 6)
        
        # Read registers 0x0020-0x0022 (3 registers)
        read_registers(client, 0x0020, 3)
        
        # Read registers 0x002A-0x002F (6 registers)
        read_registers(client, 0x002A, 6)
        
        # Read registers 0x01F4-0x01F9 (6 registers)
        read_registers(client, 0x01F4, 6)
        
        print("\n" + "=" * 60)
        print("All tests complete!")
        print("=" * 60)
        
        # Close the connection
        client.close()
        print("\n✓ Connection closed.")
        
    else:
        print("\n✗ Failed to connect to Modbus server!")
        print("  Make sure the server is running on COM10")


if __name__ == "__main__":
    main()