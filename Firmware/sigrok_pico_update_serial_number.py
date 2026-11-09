#!/usr/bin/env python3

"""
This script patches a specific line of pico-sdk to allow assigning a unique
serial number (and description) to each CI shield's RP2350 chip.
"""

import re
import pathlib
import sys

THIS_SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()

serno_descriptor_file = THIS_SCRIPT_DIR / pathlib.Path("sigrok-pico") / "build" / "_deps" / "pico_sdk-src" / "src" / "rp2_common" / "pico_stdio_usb" / "stdio_usb_descriptors.c"

SERIAL_DESCRIPTOR_LINE_REGEX = re.compile(r'\[USBD_STR_SERIAL\] = "([^"]+)",')
DESCRIPTION_DESCRIPTOR_LINE_REGEX = re.compile(r'\[USBD_STR_CDC\] = "([^"]+)",')

if len(sys.argv) != 2:
    print(f"Error: Usage: {sys.argv[0]} <serial number of board>")
    sys.exit(1)

try:
    int(sys.argv[1])
except ValueError:
    print("Serial number argument must be an integer")
    sys.exit(1)

descriptor_file_text = serno_descriptor_file.read_text()
search_result = re.search(DESCRIPTOR_LINE_REGEX, descriptor_file_text)
if search_result is None:
    print("Can't fine target line in source file")
    sys.exit(1)
else:
    print("Old serial number: " + search_result.group(1))

# Note: Spaces don't seem to work in this serial number, even though
# they should be allowed. TinyUSB limitation?
# It also seems to be limited to 19 (?) characters.
new_serial_number = "Mbed_SR_Pico_SN" + sys.argv[1]
print("New serial number: " + new_serial_number)

new_serial_descriptor_line = '[USBD_STR_SERIAL] = "' + new_serial_number + '",'
new_description_descriptor_line = '[USBD_STR_CDC] = "CI Shield ' + new_serial_number + ' Sigrok-Pico",'

new_file_text = re.sub(SERIAL_DESCRIPTOR_LINE_REGEX, new_descriptor_line, descriptor_file_text)
new_file_text = re.sub(DESCRIPTION_DESCRIPTOR_LINE_REGEX, new_description_descriptor_line, descriptor_file_text)

serno_descriptor_file.write_text(new_file_text)