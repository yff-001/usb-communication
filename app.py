import usb.core
import usb.util

# Find the CH340 device
dev = usb.core.find(idVendor=0x1A86, idProduct=0x7523)

if dev is None:
    raise ValueError('Device not found')

# Set the active configuration. With no arguments, the first configuration will be the active one
dev.set_configuration()

# Get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

ep_in = usb.util.find_descriptor(
    intf,
    # Match the first IN endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

ep_out = usb.util.find_descriptor(
    intf,
    # Match the first OUT endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

assert ep_in is not None
assert ep_out is not None

# Read data from the endpoint
try:
    while True:
        data = dev.read(ep_in.bEndpointAddress, ep_in.wMaxPacketSize)
        print(f'Received: {data}')
except KeyboardInterrupt:
    print("Exiting")

# Release the device
usb.util.dispose_resources(dev)
