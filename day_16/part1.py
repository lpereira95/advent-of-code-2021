

MAP_HEXA_TO_BIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def get_packet(hexa):
    return ''.join([MAP_HEXA_TO_BIN[val] for val in hexa])


def get_version(packet, pointer=0):
    return int(packet[pointer:pointer + 3], 2)


def get_type(packet, pointer=0):
    pointer += 3
    return int(packet[pointer:pointer + 3], 2)


def _get_subpacket_lims_4(packet, pointer, max_pointer, visited):
    start = pointer
    if start in visited:
        return []
    visited.append(start)

    pointer += 6

    while True:

        val = packet[pointer]
        if val == '0':
            break
        else:
            pointer += 5

    return [(start, pointer + 5)]


def _get_subpacket_lims_other(packet, pointer, max_pointer, visited):
    start = pointer
    if start in visited:
        return []
    visited.append(start)

    pointer += 6

    bin_val = packet[pointer]
    total_length = 15 if bin_val == '0' else 11
    pointer += 1

    size = int(packet[pointer:pointer + total_length], 2)
    pointer += total_length

    if bin_val == '0':
        child_pointer = pointer
        children_lims = []
        while True:
            child_lims = get_lims(packet, child_pointer, pointer + size, visited)
            if child_lims:
                child_pointer = child_lims[-1][1]
                children_lims += child_lims

            else:
                break

        pointer += size

    else:
        child_pointer = pointer
        children_lims = []
        for i in range(size):
            child_lims = get_lims(packet, child_pointer, max_pointer, visited)

            child_pointer = child_lims[0][1]
            children_lims += child_lims

        pointer = max([lim[1] for lim in children_lims])

    lims = [(start, pointer)]
    lims.extend(children_lims)

    return lims


def get_lims(packet, pointer, max_pointer, visited=[]):
    if pointer > max_pointer - 10:
        return []
    type_ = get_type(packet, pointer)

    if type_ == 4:
        return _get_subpacket_lims_4(packet, pointer, max_pointer, visited)
    else:
        return _get_subpacket_lims_other(packet, pointer, max_pointer, visited)


def _get_parent_end(lims, pointer):
    for lims_ in reversed(lims):
        if lims_[0] < pointer < lims_[1]:
            return lims_[1]

    return None


if __name__ == '__main__':

    filename = 'input_example_6.dat'


    with open(filename, 'r') as file:
        hexa_str = file.read().strip()

    packet = get_packet(hexa_str)

    n = len(packet)
    print(f'Packet size: {n}')
    lims = get_lims(packet, 0, len(packet))

    print(lims)

    versions = [get_version(packet, lim[0]) for lim in lims]
    types = [get_type(packet, lim[0]) for lim in lims]
    print(versions)
    print(types)

    print()
    sum_ = sum(versions)
    print(f'What do you get if you add up the version numbers in all packets? {sum_}')
