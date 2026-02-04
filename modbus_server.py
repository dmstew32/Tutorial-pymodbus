"""
Modbus RTU Server
Listens on a serial port and responds to Read Holding Registers (0x03) commands.
"""

import logging
from pymodbus.server import StartSerialServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusDeviceContext
)

# Set up logging to see what's happening
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# ============================================================
# SERIAL PORT CONFIGURATION
# TODO: Change these settings to match your hardware
# ============================================================
PORT = "COM10"         # COM port (server port - must be different from client)
BAUDRATE = 9600        # Communication speed
BYTESIZE = 8           # Data bits
PARITY = 'N'           # Parity: 'N'=None, 'E'=Even, 'O'=Odd
STOPBITS = 1           # Stop bits

def create_datastore():
    """
    Create the datastore with holding registers.
    
    This creates a simple sequential block that covers all the addresses
    that the client will request:
    - 0x0000
    - 0x0005-0x0008
    - 0x0010-0x0012
    - 0x001A-0x001F
    - 0x0020-0x0022
    - 0x002A-0x002F
    - 0x01F4-0x01F9
    """
    # Create a block of 1000 registers (addresses 0-999) intialized to 0
    holding_registers = ModbusSequentialDataBlock(0, [0] * 1000)
    
    # Optional: Set some registers to specific values for testing
    # Note: setValues uses 1-based addressing, so we add 1 to the address
    holding_registers.setValues(0x01F4 + 1, [42, 43, 44, 45, 46, 47])
    
    return holding_registers


def run_server():
    """
    Configure and start the Modbus RTU server.
    """
    # Create the register blocks
    hr_block = create_datastore()
    
    # Create blocks for other register types (not used)
    unused_block = ModbusSequentialDataBlock(0, [0] * 100)
    
    # Create the slave context
    # This defines what data is available for a specific slave ID
    store = ModbusDeviceContext(
        di=unused_block,    # Discrete Inputs (not used)
        co=unused_block,    # Coils (not used)
        hr=hr_block,        # Holding Registers
        ir=unused_block     # Input Registers (not used)
    )
    
    # Create the server context
    # single=True means the server responds to ANY slave address from client
    context = ModbusServerContext(devices=store, single=True)
    
    return context


if __name__ == "__main__":
    """
    Main entry point - runs when you execute this script.
    """
    
    print("=" * 60)
    print("Modbus RTU Server Starting...")
    print("=" * 60)
    print(f"Port:     {PORT}")
    print(f"Baudrate: {BAUDRATE}")
    print(f"Parity:   {PARITY}")
    print(f"Stop bits: {STOPBITS}")
    print("Accepts requests from any slave address")
    print("Listening for Read Holding Registers (0x03) commands...")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Get the server context
    context = run_server()
    
    # Start the server
    # This function blocks (runs forever) until you press Ctrl+C
    StartSerialServer(
        context=context,
        port=PORT,
        baudrate=BAUDRATE,
        bytesize=BYTESIZE,
        parity=PARITY,
        stopbits=STOPBITS,
        timeout=1
    )