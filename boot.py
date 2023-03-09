import serial
from string_decode import decode_string
from brain_boot_codes import *
import sys
import time


# def decode_p(input_string):
#     # Split the input string into a list of hexadecimal values
#     if len(input_string) < 1:
#         return ""
#     if "p" in input_string:
#         hex_list = input_string.split('p')
#     elif "o" in input_string:
#         hex_list = input_string.split('o')
#     else:
#         sys.exit("SOMETHING WENT WRONG IN DECIPHERING")

#     # Convert the hexadecimal values to ASCII characters
#     decoded_str = ''.join([chr(int(hex_val, 16)) for hex_val in hex_list if hex_val])
#     return decoded_str


# brainFirmware = ""
# dspFirmwareMaster = ""
# dspFirmwareSlave = ""
# dspConfig = ""
# dspAfterConfig = ""

# Set up the com ports used
BRAIN_COM = serial.Serial('COM7', 115200, timeout=1)
DSP_COM = serial.Serial('COM3', 115200, timeout=1)


with open("control.asc", "r") as brainFirmwareFile:
    BRAIN_FW = brainFirmwareFile.read()

with open("master.asc", "r") as dspMasterFile:
    DSP_MASTER_FW = dspMasterFile.read()

with open("slave.asc", "r") as dspSlaveFile:
    DSP_SLAVE_FW = dspSlaveFile.read()

with open("Config.asc", "r") as dspConfigFile:
    DSP_CONFIG = dspConfigFile.read()

with open("dspCmd1.asc", "r") as dspCmd1File:
    DSP_CMD1 = dspCmd1File.read()

with open("dspCmd2.asc", "r") as dspCmd2File:
    DSP_CMD2 = dspCmd2File.read()

with open("dspCmd3.asc", "r") as dspCmd3File:
    DSP_CMD3 = dspCmd3File.read()

with open("brainLast1.asc", "r") as brainLast1File:
    BRAIN_LAST_1 = brainLast1File.read()

with open("brainLast2.asc", "r") as brainLast2File:
    BRAIN_LAST_2 = brainLast2File.read()

with open("brainLast3.asc", "r") as brainLast3File:
    BRAIN_LAST_3 = brainLast3File.read()

# Start by turning on the power to the desk.
# Then run this script.


print("sending R")

# Send an "R" on both port:
DSP_COM.write("R".encode('ascii'))
BRAIN_COM.write("R".encode('ascii'))

# Wait for a response on both, before proceding:
portsReady = set()
if len(portsReady) > 0:
    sys.exit("CRAAAAAP")

while True:
    if "DSP" not in portsReady:
        dspCmd = DSP_COM.read().decode('ascii')
        print("dspCOM received: ", dspCmd)
        if dspCmd == "R":
            portsReady.add("DSP")
    if "BRAIN" not in portsReady:
        brainCmd = BRAIN_COM.read().decode('ascii')
        print("BrainCOM received: ", brainCmd)
        if brainCmd == "R":
            portsReady.add("BRAIN")

    # if the set contains two elements, both DSP and Brain are ready - break out of loop.
    if len(portsReady) == 2:
        break


########################################################################################
print("Clearing display, and showing a welcome.")

BRAIN_COM.write("01u".encode())  # Clear display.
time.sleep(0.02)
BRAIN_COM.write("0Cu".encode())  # wellIdunno....?
time.sleep(0.02)
BRAIN_COM.write(WELCOME_STRING1.encode())
BRAIN_COM.write(WELCOME_STRING2.encode())
BRAIN_COM.write(WELCOME_STRING3.encode())
BRAIN_COM.write(WELCOME_STRING4.encode())

print("Send DSP firmware")
DSP_COM.write(DSP_MASTER_FW.encode('ascii'))  

print("Send Brain firmware")
BRAIN_COM.write(BRAIN_FW.encode('ascii'))

brain_reply = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        brain_reply += char

print("Brain replied: ", brain_reply)
print("This is likely very important info - we should probably figure out how to do something with it.")

# write the TAPE... line... thingie...
print("writing the tape list in the display")
BRAIN_COM.write(TAPE_LIST.encode('ascii'))

# The "80p, 81p...84p" queries the tape slots, and the digital io slot.
# The reply will be a string, showing what the card is. f.ex:
# (C) 2000 Mackie Designs {Mackie Opt-8 24-Bit ADAT Light Pipe I/O}

# TODO
# If no card is installed, the string will be empty. Dont write anything then.

# Query the first IO slot:
BRAIN_COM.write("80p".encode('ascii'))

# FIRST slot reply
slot1 = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        slot1 += char

print("First slot card is: ", decode_string(slot1))

# TODO
# Rewrite this, to reflect the actual cards installed.
BRAIN_COM.write(TAPE_A_OPT8.encode('ascii')) # write text, and request next.


# Query second slot:
BRAIN_COM.write("81p".encode('ascii'))
# Second Slot reply
slot2 = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        slot2 += char

print("Second slot card is: ", decode_string(slot2)) 
BRAIN_COM.write(TAPE_B_OPT8.encode('ascii')) # write second slot, request third.


# Query third slot
BRAIN_COM.write("82p".encode('ascii'))
# Third slot reply
slot3 = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        slot3 += char

print("Third slot card is: ", decode_string(slot3))
BRAIN_COM.write(TAPE_C_OPT8.encode('ascii')) # write third slot, request fourth.

# Query alt IO slot
BRAIN_COM.write("83p".encode('ascii'))
# Fourth slot (ALT IO)
slot4 = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        slot4 += char

print("fourth hex: ", slot4)
print("Fourth slot card is: ", decode_string(slot4))
BRAIN_COM.write(ALT_IO_OPT8.encode('ascii')) # write fourth slot

# Query the Digital IO slot
BRAIN_COM.write("84p".encode('ascii'))
digital_slot = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        digital_slot += char

print("Digital IO slot card is: ", decode_string(digital_slot))


############################################################################################
# Time to return our attention to the DSP board - We should get something like R351Dd
# Check reply:

dspReply = ""
replyLength = 0
while True:
    char = DSP_COM.read().decode('ascii')
    dspReply += char
    if len(dspReply) > replyLength:
        replyLength = len(dspReply)
    else:
        break

print(dspReply) # Probably is something like"R351Dd" or "R3535d"

print("Now uploading the second DSP firmware part (slave)")
# Upload second firmware part to the DSP board:
DSP_COM.write(DSP_SLAVE_FW.encode('ascii'))


###########################################################################################
# Tilbage til brain.

print("Now checking response from Brain")
response = ""
char = BRAIN_COM.read().decode('ascii') 
print(response)
time.sleep(0.2)
print("did we get a response?")
# Seems all it really does here, is heartbeating....

# Write the info for the Digital IO in the display:
BRAIN_COM.write(STEREO_WORD_CLOCK_AES.encode('ascii'))


# Query the clock card - this is done by sending "80o"
print("querying the clock slot")
BRAIN_COM.write("80o".encode('ascii'))

# First we will have some "lklk" responses, before we get the interesting code, so handle that:
char = BRAIN_COM.read().decode('ascii')
while char == "k" or char == "l":
    char = BRAIN_COM.read().decode('ascii')

        
# Now fetch the response - using the "(" that char has from last while loop.
clockslot = char
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        clockslot += char

print("clock hex: ", clockslot)
print("Clock slot card is: ", decode_string(clockslot))

# Write the "Mackie" under the word clock:
BRAIN_COM.write(MACKIE_UNDER_WORDCLOCK.encode('ascii'))

# NOW - a single "s" is sent - unsure what it queries.
BRAIN_COM.write("s".encode('ascii'))

# There will be a response - likely "000001E65288c" - Dunno what it means.
# Is it maybe related to fx cards?
someResponse = ""
while True:
    char = BRAIN_COM.read().decode('ascii') 
    if char == "l" or char == "k":
        break
    else:
        someResponse += char

print(someResponse)


# Now display the "loading DSP plugins..."
BRAIN_COM.write(LOADING_DSP.encode('ascii'))

#after this, some time seems to pass....

##################################################################
# meanwhile - in dsp-land:

# Send config twice:
print("Sending config twice")

time.sleep(0.5)
# Send the config file twice
DSP_COM.write(DSP_CONFIG.encode('ascii'))
DSP_COM.write(DSP_CONFIG.encode('ascii'))


############################################################################
# Back to Brain

print ("\n########### Checking FX cards ###############")
# Write the "FX card" stuff in the display.
BRAIN_COM.write(FX_CARD_LIST.encode('ascii'))

##### Check each FX slot, write the corresponding fx card in the display: #####

# ======================== SLOT A =====================================
# Check for MFX in slot1:
print("Checking slot A")
BRAIN_COM.write(FXA_QUERY_MFX.encode('ascii'))

# weed out "l" and "k"
char = BRAIN_COM.read().decode('ascii')
if char != "l" and char != "k":
    response_code = char
    while True:
        char = BRAIN_COM.read().decode('ascii')
        if char != "l" and char != "k":
            response_code += char
        else:
            break
    # We should now have the response code for an MFX card.
    print(response_code)
    # write in the display
    BRAIN_COM.write(FXA_GOT_MFX.encode('ascii'))
    print("Found MFX")
else:
    print("MFX query turned up empty.")
    # MFX query reply was empty. Check if we got a UFX:
    BRAIN_COM.write(FXA_QUERY_UFX.encode('ascii'))

    char = BRAIN_COM.read().decode('ascii')
    print(char)
    if char =="l" or char =="k":
        # Slot is empty
        print("A IS EMPTYYYYY")
        BRAIN_COM.write(FXA_EMPTY.encode('ascii'))
    else:
        print("GOT UFX")
        response = ""
        while (char != "l" and char != "k"):
            response += char
            char = BRAIN_COM.read().decode('ascii')
        print(response)
        # Write to display, and send the two funky commands:
        BRAIN_COM.write(FXA_GOT_UFX.encode('ascii'))
        BRAIN_COM.write(FXA_UFX_CMD1.encode('ascii'))
        BRAIN_COM.write(FXA_UFX_CMD2.encode('ascii'))


# ======================== SLOT B =====================================
# Check for MFX in slot2:
print("Checking slot B")
BRAIN_COM.write(FXB_QUERY_MFX.encode('ascii'))

# weed out "l" and "k"
char = BRAIN_COM.read().decode('ascii')
if char != "l" and char != "k":
    response_code = char
    while True:
        char = BRAIN_COM.read().decode('ascii')
        if char != "l" and char != "k":
            response_code += char
        else:
            break
    # We should now have the response code for an MFX card.
    print(response_code)
    # write in the display
    BRAIN_COM.write(FXB_GOT_MFX.encode('ascii'))
    print("Found MFX")
else:
    print("MFX query turned up empty.")
    # MFX query reply was empty. Check if we got a UFX:
    BRAIN_COM.write(FXB_QUERY_UFX.encode('ascii'))

    char = BRAIN_COM.read().decode('ascii')
    print(char)
    if char =="l" or char =="k":
        # Slot is empty
        print("B IS EMPTYYYYY")
        BRAIN_COM.write(FXB_EMPTY.encode('ascii'))
    else:
        print("GOT UFX")
        response = ""
        while (char != "l" and char != "k"):
            response += char
            char = BRAIN_COM.read().decode('ascii')
        print(response)
        # Write to display, and send the two funky commands:
        BRAIN_COM.write(FXB_GOT_UFX.encode('ascii'))
        BRAIN_COM.write(FXB_UFX_CMD1.encode('ascii'))
        BRAIN_COM.write(FXB_UFX_CMD2.encode('ascii'))

# ======================== SLOT C =====================================
# Check for MFX in slot3:
print("Checking slot C")
BRAIN_COM.write(FXC_QUERY_MFX.encode('ascii'))

# weed out "l" and "k"
char = BRAIN_COM.read().decode('ascii')
if char != "l" and char != "k":
    response_code = char
    while True:
        char = BRAIN_COM.read().decode('ascii')
        if char != "l" and char != "k":
            response_code += char
        else:
            break
    # We should now have the response code for an MFX card.
    print(response_code)
    # write in the display
    BRAIN_COM.write(FXC_GOT_MFX.encode('ascii'))
    print("Found MFX")
else:
    print("MFX query turned up empty.")
    # MFX query reply was empty. Check if we got a UFX:
    BRAIN_COM.write(FXC_QUERY_UFX.encode('ascii'))

    char = BRAIN_COM.read().decode('ascii')
    print(char)
    if char =="l" or char =="k":
        # Slot is empty
        print("C IS EMPTYYYYY")
        BRAIN_COM.write(FXC_EMPTY.encode('ascii'))
    else:
        print("GOT UFX")
        response = ""
        while (char != "l" and char != "k"):
            response += char
            char = BRAIN_COM.read().decode('ascii')
        print(response)
        # Write to display, and send the two funky commands:
        BRAIN_COM.write(FXC_GOT_UFX.encode('ascii'))
        BRAIN_COM.write(FXC_UFX_CMD1.encode('ascii'))
        BRAIN_COM.write(FXC_UFX_CMD2.encode('ascii'))


# ======================== SLOT D =====================================
# Check for MFX in slot4:
print("Checking slot D")
BRAIN_COM.write(FXD_QUERY_MFX.encode('ascii'))

# weed out "l" and "k"
char = BRAIN_COM.read().decode('ascii')
if char != "l" and char != "k":
    response_code = char
    while True:
        char = BRAIN_COM.read().decode('ascii')
        if char != "l" and char != "k":
            response_code += char
        else:
            break
    # We should now have the response code for an MFX card.
    # write in the display
    BRAIN_COM.write(FXD_GOT_MFX.encode('ascii'))
    print("Found MFX")
else:
    print("MFX query turned up empty.")
    # MFX query reply was empty. Check if we got a UFX:
    BRAIN_COM.write(FXD_QUERY_UFX.encode('ascii'))

    char = BRAIN_COM.read().decode('ascii')
    if char =="l" or char =="k":
        # Slot is empty
        print("D IS EMPTYYYYY")
        BRAIN_COM.write(FXD_EMPTY.encode('ascii'))
    else:
        print("GOT UFX")
        response = ""
        while (char != "l" and char != "k"):
            response += char
            char = BRAIN_COM.read().decode('ascii')
        print(response)
        # Write to display, and send the two funky commands:
        BRAIN_COM.write(FXD_GOT_UFX.encode('ascii'))
        BRAIN_COM.write(FXD_UFX_CMD1.encode('ascii'))
        BRAIN_COM.write(FXD_UFX_CMD2.encode('ascii'))




print("We're done identifying FX cards.")
print("read out some 'lk's: ")

char = ""
char = BRAIN_COM.read().decode('ascii')
print("This should be an 'l': ", char)
if char == "k":
    BRAIN_COM.read().decode('ascii')



print("Write some 7x2$...")
# After that, write some weird commands:
DSP_COM.write(DSP_CMD1.encode('ascii'))

char = ""
response = ""
while True:
    char = DSP_COM.read().decode('ascii')
    response += char
    if char == "d":
        break

print("should be 8000d: ",response)

# printing some lk's
for i in range(6):
    char = BRAIN_COM.read().decode('ascii')
    print("i ", char)


print("writing brain last-1 og 2")
BRAIN_COM.write(BRAIN_LAST_1.encode('ascii'))
BRAIN_COM.write(BRAIN_LAST_2.encode('ascii'))


print("writing last DSP part2")
DSP_COM.write(DSP_CMD2.encode('ascii'))

print("writing last brain(3)")
BRAIN_COM.write(BRAIN_LAST_3.encode('ascii'))

print("writing final dsp")
DSP_COM.write(DSP_CMD3.encode('ascii'))


print("DONE!")

# while True:
#     print("BRAIN: ", BRAIN_COM.read().decode('ascii'))
#     print("DSP: ", DSP_COM.read().decode('ascii'))
#     time.sleep(0.3)

# waitasecond
time.sleep(1)

# Open for some sound
# Set channel 9 pan to left
DSP_COM.write("0AdFEFFX0OFDFFXP".encode('ascii'))

# Set channel 10 to right
DSP_COM.write("22dFEFFXFEOFDFFXP".encode('ascii'))  

# Turn channel 9 up to unity
DSP_COM.write("0AcXC1Q".encode('ascii'))

# Turn channel 10 up to unity
DSP_COM.write("22cXC1Q".encode('ascii'))    # Min: 22cX0Q    Max: 22cXFFQ

# Set master to about -10
DSP_COM.write("4Cc9X83QAX83Q".encode('ascii'))  # unity about: 4Cc9XC1QAXC1Q

# Set speaker level to something moderate
BRAIN_COM.write("BA0w".encode('ascii'))
# The command to change the volume is B??w, where the ?? is a value between 00 and BF (case is imporant)


# After these lines, there should be sound coming out of headphone 1 jack. (though mostly so if you connect headphones....)

# Enable the Mains out
BRAIN_COM.write("5Fd".encode('ascii'))


