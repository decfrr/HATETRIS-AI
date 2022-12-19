import re

import numpy as np
import typing


BITS_PER_CHAR = 11
BITS_PER_BYTE = 8

pair_strings = [
  '89AZazÆÆÐÐØØÞßææððøøþþĐđĦħııĸĸŁłŊŋŒœŦŧƀƟƢƮƱǃǝǝǤǥǶǷȜȝȠȥȴʯͰͳͶͷͻͽͿͿΑΡΣΩαωϏϏϗϯϳϳϷϸϺϿЂЂЄІЈЋЏИКикяђђєіјћџѵѸҁҊӀӃӏӔӕӘәӠӡӨөӶӷӺԯԱՖաֆאתװײؠءاؿفي٠٩ٮٯٱٴٹڿہہۃےەەۮۼۿۿܐܐܒܯݍޥޱޱ߀ߪࠀࠕࡀࡘࡠࡪࢠࢴࢶࢽऄनपरलळवहऽऽॐॐॠॡ०९ॲঀঅঌএঐওনপরললশহঽঽৎৎৠৡ০ৱ৴৹ৼৼਅਊਏਐਓਨਪਰਲਲਵਵਸਹੜੜ੦੯ੲੴઅઍએઑઓનપરલળવહઽઽૐૐૠૡ૦૯ૹૹଅଌଏଐଓନପରଲଳଵହଽଽୟୡ୦୯ୱ୷ஃஃஅஊஎஐஒஓககஙசஜஜஞடணதநபமஹௐௐ௦௲అఌఎఐఒనపహఽఽౘౚౠౡ౦౯౸౾ಀಀಅಌಎಐಒನಪಳವಹಽಽೞೞೠೡ೦೯ೱೲഅഌഎഐഒഺഽഽൎൎൔൖ൘ൡ൦൸ൺൿඅඖකනඳරලලවෆ෦෯กะาาเๅ๐๙ກຂຄຄງຈຊຊຍຍດທນຟມຣລລວວສຫອະາາຽຽເໄ໐໙ໞໟༀༀ༠༳ཀགངཇཉཌཎདནབམཛཝཨཪཬྈྌကဥဧဪဿ၉ၐၕ',
  '07'
]


lookup_e = {}
lookup_d = {}
for r, pair_string in enumerate(pair_strings):
    # Decompression
    encode_repertoire = []
    for pair in re.findall(r'..', pair_string):
        first = ord(pair[0])
        last = ord(pair[1])
        for code_point in range(first, last+1):
            encode_repertoire.append(chr(code_point))

    num_z_bits = BITS_PER_CHAR - BITS_PER_BYTE * r  # 0 -> 11, 1 -> 3
    lookup_e[num_z_bits] = encode_repertoire
    for z, char in enumerate(encode_repertoire):
        lookup_d[char] = [num_z_bits, z]


def encode(uint8array: np.array) -> str:
    length = len(uint8array)

    result = ""
    z = 0
    num_z_bits = 0

    for i in range(length):
        uint8 = uint8array[i]
        # Take most significant bit first
        for j in range(BITS_PER_BYTE - 1, -1, -1):
            bit = (uint8 >> j) & 1

            z = (z << 1) + bit
            num_z_bits += 1

            if num_z_bits == BITS_PER_CHAR:
                result += lookup_e[num_z_bits][z]
                z = 0
                num_z_bits = 0

    if num_z_bits != 0:
        while num_z_bits not in lookup_e:
            z = (z << 1) + 1
            num_z_bits += 1
        z = z & (2 ** num_z_bits - 1)
        result += lookup_e[num_z_bits][z]

    return result


def decode(string: str) -> np.array:
    length = len(string)

    # This length is a guess. There's a chance we allocate one more byte here
    # than we actually need. But we can count and slice it off later
    uint8_array = np.zeros(length * BITS_PER_CHAR // BITS_PER_BYTE, dtype=np.uint8)
    num_uint8s = 0
    uint8 = 0
    num_uint8_bits = 0

    for i in range(length):
        chr = string[i]

        if chr not in lookup_d:
            raise ValueError(f"Unrecognised Base2048 character: {chr}")

        num_z_bits, z = lookup_d[chr]

        if num_z_bits != BITS_PER_CHAR and i != length - 1:
            raise ValueError("Secondary character found before end of input at position {}".format(i))

        # Take most significant bit first
        for j in range(num_z_bits - 1, -1, -1):
            bit = (z >> j) & 1

            uint8 = (uint8 << 1) + bit
            num_uint8_bits += 1

            if num_uint8_bits == BITS_PER_BYTE:
                uint8_array[num_uint8s] = uint8
                num_uint8s += 1
                uint8 = 0
                num_uint8_bits = 0

    # Final padding bits! Requires special consideration!
    # Remember how we always pad with 1s?
    # Note: there could be 0 such bits, check still works though
    if uint8 != (1 << num_uint8_bits) - 1:
        raise ValueError("Padding mismatch")

    return uint8_array[:num_uint8s]
