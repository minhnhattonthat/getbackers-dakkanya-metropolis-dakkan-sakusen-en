"""GBA BIOS LZ77 (type 0x10) decompress / compress, plus a scan for pointed-to blocks.

    python -X utf8 tools/lz77.py scan ROM       # list LZ77 blocks some aligned 0x08xxxxxx word points at
"""
import struct
import sys


def decompress(d, off=0, limit=None):
    """Return (data, end_offset). Raises ValueError on a malformed block."""
    if d[off] != 0x10:
        raise ValueError('not LZ77')
    size = d[off + 1] | d[off + 2] << 8 | d[off + 3] << 16
    if limit is not None and size > limit:
        raise ValueError('too big')
    out = bytearray()
    i = off + 4
    while len(out) < size:
        flags = d[i]
        i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                b1, b2 = d[i], d[i + 1]
                i += 2
                n = (b1 >> 4) + 3
                disp = ((b1 & 0xF) << 8 | b2) + 1
                if disp > len(out):
                    raise ValueError('bad backref')
                for _ in range(n):
                    out.append(out[-disp])
            else:
                out.append(d[i])
                i += 1
    return bytes(out[:size]), i


def compress(data):
    """VRAM-safe greedy LZ77 (no displacement 1, so 16-bit VRAM writes work)."""
    out = bytearray(struct.pack('<I', 0x10 | len(data) << 8))
    i = 0
    n = len(data)
    while i < n:
        flag_pos = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if i >= n:
                break
            best_len, best_disp = 0, 0
            for disp in range(2, min(i, 0x1000) + 1):
                l = 0
                while l < 18 and i + l < n and data[i + l] == data[i + l - disp]:
                    l += 1
                if l > best_len:
                    best_len, best_disp = l, disp
                    if l == 18:
                        break
            if best_len >= 3:
                flags |= 0x80 >> bit
                v = (best_len - 3) << 12 | (best_disp - 1)
                out += bytes((v >> 8, v & 0xFF))
                i += best_len
            else:
                out.append(data[i])
                i += 1
        out[flag_pos] = flags
    while len(out) % 4:
        out.append(0)
    return bytes(out)


def scan(d, limit=0x40000):
    """Yield (offset, size, end) for every LZ77 block an aligned ROM pointer reaches."""
    targets = set()
    for p in range(0, len(d) - 3, 4):
        v = struct.unpack_from('<I', d, p)[0]
        if 0x08000000 <= v < 0x08000000 + len(d):
            o = v - 0x08000000
            if d[o] == 0x10:
                targets.add(o)
    for o in sorted(targets):
        try:
            data, end = decompress(d, o, limit)
        except (ValueError, IndexError):
            continue
        if data:
            yield o, len(data), end


if __name__ == '__main__':
    if sys.argv[1] == 'scan':
        rom = open(sys.argv[2], 'rb').read()
        for o, size, end in scan(rom):
            print(f'{o:06X} {size:6X} {end:06X}')
