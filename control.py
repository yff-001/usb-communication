import usb.core
import usb.util

# Find the CH340 device by Vendor ID (VID) and Product ID (PID)
dev = usb.core.find(idVendor=0x1A86, idProduct=0x7523)

if dev is None:
    raise ValueError('Device not found')

# Set the active configuration. With no arguments, the first configuration will be the active one
dev.set_configuration()

# Define control transfer request types and constants
SET_LINE_CODING = 0x20
GET_LINE_CODING = 0x21
SET_CONTROL_LINE_STATE = 0x22

# Line coding structure: [baud rate (4 bytes), stop bits (1 byte), parity (1 byte), data bits (1 byte)]
# Example: 9600 baud, 1 stop bit, no parity, 8 data bits
line_coding = [
    0x80, 0x25, 0x00, 0x00,  # 9600 baud rate
    0x00,  # 1 stop bit
    0x00,  # No parity
    0x08   # 8 data bits
]

# Set line coding (baud rate, stop bits, parity, data bits)
dev.ctrl_transfer(
    bmRequestType=0x21,  # Host to device, Class request, Interface recipient
    bRequest=SET_LINE_CODING,
    wValue=0, wIndex=0,
    data_or_wLength=line_coding
)

# Get line coding (retrieve current UART settings)
response = dev.ctrl_transfer(
    bmRequestType=0xA1,  # Device to host, Class request, Interface recipient
    bRequest=GET_LINE_CODING,
    wValue=0, wIndex=0,
    data_or_wLength=7  # Length of line coding structure
)

# Parse the response
baud_rate = response[0] | (response[1] << 8) | (response[2] << 16) | (response[3] << 24)
stop_bits = response[4]
parity = response[5]
data_bits = response[6]

print(f'Current UART Settings:')
print(f'Baud Rate: {baud_rate}')
print(f'Stop Bits: {stop_bits}')
print(f'Parity: {parity}')
print(f'Data Bits: {data_bits}')
