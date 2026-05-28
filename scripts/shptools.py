#!/usr/bin/env python3
'''
Westwood LCW (Format80) codec + CPS/SHP helpers, for the classic-mode
TD-sprite palette remap. Ported from Vanilla Conquer common/lcw.cpp.

LCW_Uncompress is an exact port (must be bit-faithful). lcw_compress is a
faithful port of LCW_Comp; the engine decodes either, but matching VC keeps
output sizes sane.

License: GPL v3 (inherited from Vanilla Conquer base).
'''
import struct
import sys


def lcw_decompress(src, length):
    '''Decompress `length` bytes out of LCW stream `src`. Returns bytes.'''
    out = bytearray()
    s = 0
    src = memoryview(src)
    while len(out) < length:
        op = src[s]
        s += 1
        if not (op & 0x80):
            # short copy from dest: count=(op>>4)+3, rel offset 12-bit
            count = (op >> 4) + 3
            rel = src[s] + ((op & 0x0F) << 8)
            s += 1
            start = len(out) - rel
            for i in range(count):
                out.append(out[start + i])
        elif not (op & 0x40):
            if op == 0x80:
                break
            # medium copy from source: count = op & 0x3f
            count = op & 0x3F
            out += bytes(src[s:s + count])
            s += count
        else:
            if op == 0xFE:
                # long run of a single byte
                count = src[s] | (src[s + 1] << 8)
                val = src[s + 2]
                s += 3
                out += bytes([val]) * count
            elif op == 0xFF:
                # long copy from dest (absolute offset)
                count = src[s] | (src[s + 1] << 8)
                pos = src[s + 2] | (src[s + 3] << 8)
                s += 4
                for i in range(count):
                    out.append(out[pos + i])
            else:
                # medium copy from dest (absolute offset): count=(op&0x3f)+3
                count = (op & 0x3F) + 3
                pos = src[s] | (src[s + 1] << 8)
                s += 2
                for i in range(count):
                    out.append(out[pos + i])
    return bytes(out)


def lcw_compress(src):
    '''Faithful port of VC LCW_Comp. Returns compressed bytes.'''
    src = bytes(src)
    n = len(src)
    if n == 0:
        return b''
    out = bytearray()
    getp = 0
    getstart = 0
    getend = n
    # starting cmd1 (medium copy from source, count-in-low-bits)
    cmd_onep = len(out)
    out.append(0x81)
    out.append(src[getp])
    getp += 1
    cmd_one = True

    while getp < getend:
        # RLE run?
        if getend - getp > 64 and src[getp] == src[getp + 64]:
            rlemax = getend if (getend - getp) < 0xFFFF else getp + 0xFFFF
            rlep = getp + 1
            while rlep < rlemax and src[rlep] == src[getp]:
                rlep += 1
            run_length = rlep - getp
            if run_length >= 0x41:
                cmd_one = False
                out.append(0xFE)
                out.append(run_length & 0xFF)
                out.append((run_length >> 8) & 0xFF)
                out.append(src[getp])
                getp = rlep
                continue

        block_size = 0
        offsetp = getp
        offchk = getstart
        while offchk < getp:
            while offchk < getp and src[offchk] != src[getp]:
                offchk += 1
            if offchk >= getp:
                break
            i = 1
            while getp + i < getend and src[offchk + i] == src[getp + i]:
                i += 1
            if i >= block_size:
                block_size = i
                offsetp = offchk
            offchk += 1

        if block_size <= 2:
            if cmd_one and out[cmd_onep] < 0xBF:
                out[cmd_onep] += 1
                out.append(src[getp])
                getp += 1
            else:
                cmd_onep = len(out)
                out.append(0x81)
                out.append(src[getp])
                getp += 1
                cmd_one = True
        else:
            rel_offset = getp - offsetp
            if block_size > 0xA or rel_offset > 0xFFF:
                if block_size > 0x40:
                    out.append(0xFF)
                    out.append(block_size & 0xFF)
                    out.append((block_size >> 8) & 0xFF)
                else:
                    out.append(((block_size - 3) | 0xC0) & 0xFF)
                offset = offsetp - getstart
            else:
                offset = ((rel_offset << 8) | (16 * (block_size - 3) + (rel_offset >> 8))) & 0xFFFF
            out.append(offset & 0xFF)
            out.append((offset >> 8) & 0xFF)
            getp += block_size
            cmd_one = False

    out.append(0x80)
    return bytes(out)


KF_DELTA = 0x20
KF_KEYDELTA = 0x40
KF_KEYFRAME = 0x80
_SHP_HDR = '<HHHHHHh'  # frames,x,y,width,height,largest_frame_size,flags
_SHP_HDR_LEN = 14


def apply_xor_delta(buf, src):
    '''Port of VC common/xordelta.cpp Apply_XOR_Delta. XORs `src` delta
    stream onto `buf` (a bytearray) in place. Self-terminating.'''
    p = 0          # position in buf
    s = 0          # position in src
    src = memoryview(src)
    while True:
        cmd = src[s]
        s += 1
        if not (cmd & 0x80):
            if cmd == 0:
                count = src[s]
                value = src[s + 1]
                s += 2
                for _ in range(count):
                    buf[p] ^= value
                    p += 1
            else:
                # 0b0??????? : XOR next cmd bytes
                count = cmd
                for _ in range(count):
                    buf[p] ^= src[s]
                    p += 1
                    s += 1
        else:
            count = cmd & 0x7F
            if count != 0:
                # skip `count` bytes
                p += count
                continue
            count = src[s] | (src[s + 1] << 8)
            s += 2
            if count == 0:
                return
            if (count & 0x8000) == 0:
                p += count
                continue
            if count & 0x4000:
                count &= 0x3FFF
                value = src[s]
                s += 1
                for _ in range(count):
                    buf[p] ^= value
                    p += 1
            else:
                count &= 0x3FFF
                for _ in range(count):
                    buf[p] ^= src[s]
                    p += 1
                    s += 1


def parse_shp(data):
    '''Return (header_dict, [(data_offset, flags), ...]) for nframes frames.'''
    frames, x, y, width, height, largest, flags = struct.unpack_from(_SHP_HDR, data, 0)
    if flags & 1:
        raise NotImplementedError('SHP with embedded palette (flags&1) not handled')
    entries = []
    for n in range(frames):
        o0, o1 = struct.unpack_from('<II', data, _SHP_HDR_LEN + n * 8)
        entries.append((o0 & 0x00FFFFFF, (o0 >> 24) & 0xFF))
    hdr = dict(frames=frames, width=width, height=height, flags=flags)
    return hdr, entries


def decode_shp(data):
    '''Decode every frame to a flat w*h index bytearray. Returns (hdr, [bitmap,...]).
    Sequential reconstruction handles keyframe / keydelta / delta chains.'''
    hdr, entries = parse_shp(data)
    w, h = hdr['width'], hdr['height']
    size = w * h
    frames = []
    buf = bytearray(size)
    keyframe = bytearray(size)
    for off, flags in entries:
        if flags & KF_KEYFRAME:
            buf = bytearray(lcw_decompress(data[off:], size))
            if len(buf) < size:
                buf += bytes(size - len(buf))
            keyframe = bytearray(buf)
        elif flags & KF_KEYDELTA:
            buf = bytearray(keyframe)
            apply_xor_delta(buf, data[off:])
        elif flags & KF_DELTA:
            apply_xor_delta(buf, data[off:])
        else:
            raise ValueError(f'unknown frame flags {flags:#04x}')
        frames.append(bytearray(buf))
    return hdr, frames


def encode_shp(hdr, frames):
    '''Re-encode frames as a SHP with every frame a standalone Format80
    keyframe. Returns bytes.'''
    w, h = hdr['width'], hdr['height']
    nframes = len(frames)
    comp = [lcw_compress(bytes(f)) for f in frames]
    largest = max((len(c) for c in comp), default=0)

    table_len = (nframes + 2) * 8
    data_start = _SHP_HDR_LEN + table_len
    out = bytearray()
    out += struct.pack(_SHP_HDR, nframes, 0, 0, w, h, min(largest, 0xFFFF), 0)

    offsets = []
    cur = data_start
    for c in comp:
        offsets.append(cur)
        cur += len(c)
    file_end = cur

    for off in offsets:
        out += struct.pack('<II', off | (KF_KEYFRAME << 24), 0)
    # +2 sentinels: end-of-data offset, then zero.
    out += struct.pack('<II', file_end, 0)
    out += struct.pack('<II', 0, 0)
    for c in comp:
        out += c
    return bytes(out)


def read_cps(data):
    '''Decode a Westwood CPS image. Returns (pixels_bytes, embedded_palette_or_None).
    Header: u16 filesize, u16 compression(4=LCW), u32 uncompressed_size,
    u16 palette_flag (0x0300 => 768-byte palette follows).'''
    filesize, comp, uncompressed, palflag = struct.unpack_from('<HHIH', data, 0)
    off = 10
    palette = None
    if palflag == 0x0300:
        palette = data[off:off + 768]
        off += 768
    if comp == 0x0004:
        pixels = lcw_decompress(data[off:], uncompressed)
    elif comp == 0x0000:
        pixels = data[off:off + uncompressed]
    else:
        raise ValueError(f'unsupported CPS compression {comp:#06x}')
    return pixels, palette


# --- TD->RA classic-mode palette remap -------------------------------------
# TD house-color "unity" range is 176..191; RA's is 80..95 (verified against
# TD CONST.CPP / RA PALETTE.CPS). Remapping TD's range onto RA's lets RA's
# engine recolor those pixels per player. Every other index is matched to the
# nearest RA colour by RGB, excluding index 0 (transparent) and 80..95 (so a
# non-house pixel never accidentally becomes house-coloured).
TD_REMAP_LO, TD_REMAP_HI = 176, 191
RA_REMAP_LO, RA_REMAP_HI = 80, 95


def load_pal(path):
    '''Load a 768-byte 6-bit VGA palette into a list of 256 (r,g,b) tuples.'''
    d = open(path, 'rb').read()
    if len(d) < 768:
        raise ValueError(f'{path}: expected 768 bytes, got {len(d)}')
    return [(d[i * 3], d[i * 3 + 1], d[i * 3 + 2]) for i in range(256)]


def build_remap_lut(td_pal, ra_pal):
    '''Return a 256-entry list mapping TD palette index -> RA palette index.'''
    excluded = set(range(RA_REMAP_LO, RA_REMAP_HI + 1)) | {0}
    candidates = [j for j in range(256) if j not in excluded]
    lut = [0] * 256
    for i in range(256):
        if i == 0:
            lut[i] = 0
        elif TD_REMAP_LO <= i <= TD_REMAP_HI:
            lut[i] = RA_REMAP_LO + (i - TD_REMAP_LO)
        else:
            tr, tg, tb = td_pal[i]
            best_j, best_d = candidates[0], 1 << 30
            for j in candidates:
                rr, rg, rb = ra_pal[j]
                d = (tr - rr) ** 2 + (tg - rg) ** 2 + (tb - rb) ** 2
                if d < best_d:
                    best_d, best_j = d, j
            lut[i] = best_j
    return lut


def remap_shp(data, lut):
    '''Decode a SHP, remap every pixel via lut, re-encode as Format80.'''
    hdr, frames = decode_shp(data)
    for f in frames:
        for k in range(len(f)):
            f[k] = lut[f[k]]
    return encode_shp(hdr, frames)


def _cmd_remap(argv):
    if len(argv) < 4:
        print('usage: shptools.py remap <in.shp> <out.shp> <td.pal> <ra.pal>', file=sys.stderr)
        return 2
    inp, outp, tdpal, rapal = argv[:4]
    lut = build_remap_lut(load_pal(tdpal), load_pal(rapal))
    data = open(inp, 'rb').read()
    open(outp, 'wb').write(remap_shp(data, lut))
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'remap':
        sys.exit(_cmd_remap(sys.argv[2:]))
    # Self-test: round-trip lcw on some data.
    import os
    sample = bytes(range(256)) * 10 + b'\x00' * 500 + os.urandom(300)
    comp = lcw_compress(sample)
    back = lcw_decompress(comp, len(sample))
    assert back == sample, 'LCW round-trip FAILED'
    print(f'LCW round-trip OK ({len(sample)} -> {len(comp)} -> {len(back)})')
