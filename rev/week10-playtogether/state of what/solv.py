def read_shuffled_flag(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# tabel FSA
transition = {
    0: {0: 1, 1: 2},
    1: {0: 2, 1: 3},
    2: {0: 3, 1: 0},
    3: {0: 0, 1: 1}
}

# inverse
inverse_transition = {
    0: {1: 0, 3: 1},
    1: {0: 0, 2: 3},
    2: {0: 1, 3: 2},
    3: {1: 1, 2: 2}
}

def unshuffle_flag(shuffled_flag):
    current_state = 0
    original_flag = []
    for char in shuffled_flag:
        bit = int(char)
        for original_bit in (0, 1):
            if transition[current_state][original_bit] == bit:
                original_flag.append(str(original_bit))
                current_state = bit
                break
    return ''.join(original_flag)

def binary_to_ascii(binary_string):
    n = int(binary_string, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

if __name__ == "__main__":
    shuffled_flag = read_shuffled_flag('flag.txt')
    original_flag_binary = unshuffle_flag(shuffled_flag)
    original_flag_ascii = binary_to_ascii(original_flag_binary)
    print(f"Flag: {original_flag_binary}")
    print(f"Flag: {original_flag_ascii}")
