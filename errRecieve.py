"""
Client's side at error detection process
The receiver receives the encoded data string from the sender.
with the help of the key receiver decodes the data and finds out the remainder.
If the remainder is --> there is no error in data sent by the sender.
If the remainder comes out to be non-zero --> there was an error, a Negative Acknowledgement is sent to the sender.
The sender then resends the data until the receiver receives the correct data.
"""


def xor(a, b):
    result = []

    # Traverse all bits, if bits are same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def mod2div(dividend, divisor):
    # Number of bits to be XORed at a time.
    pick = len(divisor)

    # Slicing the dividend to appropriate
    # length for particular step
    tmp = dividend[0: pick]

    while pick < len(dividend):

        if tmp[0] == '1':

            # replace the dividend by the result of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + dividend[pick]

        else:  # If leftmost bit is '0'
            # If the leftmost bit of the dividend (or the part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an all-0s divisor.
            tmp = xor('0' * pick, tmp) + dividend[pick]

        # increment pick to move further
        pick += 1

    # For the last n bits, we have to carry it out normally as increased value of pick will cause Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword


# Function used at the receiver side to decode data received by sender
def decodeData(data, key):
    l_key = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data.decode() + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)

    return remainder

