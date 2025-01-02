import usb.core
import usb.util

# Find the CH340 device by Vendor ID (VID) and Product ID (PID)
VID = 0x1A86
PID = 0x7523

dev = usb.core.find(idVendor=VID, idProduct=PID)

if dev is None:
    raise ValueError("Device not found")

# Set the active configuration. With no arguments, the first configuration will be the active one
dev.set_configuration()

# Get the active configuration
cfg = dev.get_active_configuration()

# Iterate over the interfaces and their endpoints
for intf in cfg:
    print(f'Interface Number: {intf.bInterfaceNumber}, Alternate Setting: {intf.bAlternateSetting}')
    for ep in intf:
        print(f'  Endpoint Address: {ep.bEndpointAddress}')
        print(f'    Attributes: {ep.bmAttributes}')
        print(f'    Max Packet Size: {ep.wMaxPacketSize}')
        print(f'    Interval: {ep.bInterval}')
