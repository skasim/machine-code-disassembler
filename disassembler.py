def main():
    print("Module 4 Assignment: MIPS Disassembler by Samra Kasim\n")

    instr1 = '00000001101011100101100000100100'
    instr2 = '10001101010010010000000000001000'
    instr3 = '00001000000000010010001101000101'
    instr4 = '00000010101010010101100000100010'
    instr5 = '00000011111000000000000000001000'
    instr6 = '00110101111100001011111011101111'
    instr7 = '10101110100011010000000000100000'
    instr8 = '00000010110011010101000000100000'

    instructions: list = [instr1, instr2, instr3, instr4, instr5, instr6, instr7, instr8]

    count: int = 0
    for instruction in instructions:
        count += 1
        print("binary instruction #%i: %s " % (count, instruction))
        l: list = str_to_list(instruction)
        opscode: str = list_to_str(l[0:6])
        funct: str = list_to_str(l[26:])

        if opscode == '000000' and key_exists(funct, func_codes):
            print('machine code instruction: %s \n' % (get_r_type_instruction(l)))
        elif key_exists(opscode, op_codes_i_type):
            print('machine code instruction: %s \n' % (get_i_type_instruction(l)))
        elif key_exists(opscode, op_codes_j_type):
            print('machine code instruction: %s \n' % (get_j_type_instruction(l)))
        else:
            print("error: only following instructions are processed: add, and, or, sub, j, jal, jr, addi, andi, lw"
                  "ori, sw")


def get_r_type_instruction(l: list) -> str:
    """Parses the binary list representation the binary string and returns the assembly language instruction
    for R types"""

    opcode: str = func_codes.get(list_to_str(l[26:]))
    rs: str = get_register_from_decimal(binary_to_decimal_converter(list_to_str(l[6:11])))
    rt: str = get_register_from_decimal(binary_to_decimal_converter(list_to_str(l[11:16])))
    rd: str = get_register_from_decimal(binary_to_decimal_converter(list_to_str(l[16:21])))

    return '%s %s, %s, %s' % (opcode, rd, rs, rt)


def get_i_type_instruction(l: list) -> str:
    """Parses the binary list representation the binary string and returns the assembly language instruction
    for I types"""

    opcode: str = op_codes_i_type.get(list_to_str(l[0:6]))
    rs: str = get_register_from_decimal(binary_to_decimal_converter(list_to_str(l[6:11])))
    rt: str = get_register_from_decimal(binary_to_decimal_converter(list_to_str(l[11:16])))
    imm: str = binary_to_hex_converter(list_to_str(l[16:]))

    if opcode == 'sw' or opcode == 'lw':
        return '%s %s, %s(%s)' % (opcode, rt, imm, rs)

    if opcode == 'jr':
        return '%s %s' % (opcode, rs)

    return '%s %s, %s, %s' % (opcode, rt, rs, imm)


def get_j_type_instruction(l: list) -> str:
    """Parses the binary list representation the binary string and returns the assembly language instruction
    for J types. Since address value is 26 bits, 2 bits are prepended for HEX conversion"""

    opcode: str = op_codes_j_type.get(list_to_str(l[0:6]))
    deepcopy_l = [i for i in list_to_str(l)]
    deepcopy_l = deepcopy_l[6:]

    if deepcopy_l[6] == '0':
        deepcopy_l.insert(0, '0')
        deepcopy_l.insert(1, '0')
    else:
        deepcopy_l.insert(0, '1')
        deepcopy_l.insert(1, '1')

    address: str = binary_to_hex_converter(list_to_str(deepcopy_l))

    return '%s %s' % (opcode, address)


def binary_to_hex_converter(binary: str) -> str:
    """Convert a binary string to HEX"""

    l: list = str_to_list(binary)
    hex_val: str = ''

    for x in range(0, len(l) - 1, 4):
        tot: int = 0
        if int(l[x]) == 1:
            tot += 8
        if int(l[x + 1]) == 1:
            tot += 4
        if int(l[x + 2]) == 1:
            tot += 2
        if int(l[x + 3]) == 1:
            tot += 1
        hex_val += get_hex_value_from_decimal(tot)

    return '0x'+hex_val


def binary_to_decimal_converter(binary: str) -> int:
    """Convert a binary string to decimal"""

    l: list = str_to_list(binary)
    index = len(l) - 1
    tot: int = 0
    for x in range(0, len(l), 1):
        if int(l[x]) == 1:
            tot += 2 ** (index - x)

    return tot


def get_register_from_decimal(decimal: int) -> str:
    """Return the register name for a provided decimal"""

    if decimal == 0:
        return '0'
    elif decimal == 1:
        return '$at'
    elif decimal == 2:
        return '$v0'
    elif decimal == 3:
        return '$v1'
    elif decimal == 4:
        return '$a0'
    elif decimal == 5:
        return '$a1'
    elif decimal == 6:
        return '$a2'
    elif decimal == 7:
        return '$a3'
    elif decimal == 8:
        return '$t0'
    elif decimal == 9:
        return '$t1'
    elif decimal == 10:
        return '$t2'
    elif decimal == 11:
        return '$t3'
    elif decimal == 12:
        return '$t4'
    elif decimal == 13:
        return '$t5'
    elif decimal == 14:
        return '$t6'
    elif decimal == 15:
        return '$t7'
    elif decimal == 16:
        return '$s0'
    elif decimal == 17:
        return '$s1'
    elif decimal == 18:
        return '$s2'
    elif decimal == 19:
        return '$s3'
    elif decimal == 20:
        return '$s4'
    elif decimal == 21:
        return '$s5'
    elif decimal == 22:
        return '$s6'
    elif decimal == 23:
        return '$s7'
    elif decimal == 24:
        return '$t8'
    elif decimal == 25:
        return '$t9'
    elif decimal == 26:
        return '$k0'
    elif decimal == 27:
        return '$k1'
    elif decimal == 28:
        return '$gp'
    elif decimal == 29:
        return '$sp'
    elif decimal == 30:
        return '$fp'
    elif decimal == 31:
        return '$ra'


def get_hex_value_from_decimal(decimal: int) -> str:
    """Return hex values from the provided decimal"""

    if decimal == 10:
        return 'A'
    elif decimal == 11:
        return 'B'
    elif decimal == 12:
        return 'C'
    elif decimal == 13:
        return 'D'
    elif decimal == 14:
        return 'E'
    elif decimal == 15:
        return 'F'
    else:
        return str(decimal)

# Dictionaries for storing key values


func_codes: dict = {
    '100000': 'add',
    '100100': 'and',
    '100101': 'or',
    '100010': 'sub'
}

op_codes_i_type: dict = {
    '001100': 'andi',
    '001000': 'addi',
    '001101': 'ori',
    '100011': 'lw',
    '101011': 'sw',
    '000000': 'jr'

}

op_codes_j_type: dict = {
    '000010': 'j',
    '000011': 'jal',
}

# HELPER METHODS


def key_exists(key: str, dictionary: dict):
    """Check if a key exists in the given dictionary"""

    if key in dictionary.keys():
        return True
    else:
        return False


def str_to_list(binary: str) -> list:
    """Convert string to a list"""

    return [i for i in binary]


def list_to_str(l: list) -> str:
    """Convert a list to a string"""

    binary: str = ''
    for i in l:
        binary += i

    return binary


if __name__ == "__main__":
    main()
