import sys

def decode_string(input_string):
    # Split the input string into a list of hexadecimal values
    if len(input_string) < 1:
        return ""
    if "p" in input_string:
        hex_list = input_string.split('p')
    elif "o" in input_string:
        hex_list = input_string.split('o')
    else:
        sys.exit("SOMETHING WENT WRONG IN DECIPHERING")

    # Convert the hexadecimal values to ASCII characters
    decoded_str = ''.join([chr(int(hex_val, 16)) for hex_val in hex_list if hex_val])
    return decoded_str
