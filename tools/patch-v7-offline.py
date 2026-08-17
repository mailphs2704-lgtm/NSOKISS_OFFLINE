#!/usr/bin/env python3
"""Patch the supplied V7 J2ME client for the NSOKISS offline runtime.

Changes:
  * S.al() no longer downloads the online server list.
  * bQ.H() ignores the supplied endpoint and uses socket://127.0.0.1:14444.

Input/output are local JAR files. The script intentionally works at the class-file
level so the original obfuscated client does not need to be decompiled/recompiled.
"""
from pathlib import Path
import shutil
import struct
import zipfile
import sys


def rebuild_cp(data, transform=lambda i, x: x, additions=()):
    cp_count = struct.unpack('>H', data[8:10])[0]
    p = 10
    entries = []
    i = 1
    while i < cp_count:
        tag = data[p]
        p += 1
        if tag == 1:
            n = struct.unpack('>H', data[p:p+2])[0]
            p += 2
            value = data[p:p+n]
            p += n
            entries.append((tag, value))
        elif tag in (3, 4):
            entries.append((tag, data[p:p+4])); p += 4
        elif tag in (5, 6):
            entries.append((tag, data[p:p+8])); p += 8; i += 1
        elif tag in (7, 8, 16, 19, 20):
            entries.append((tag, data[p:p+2])); p += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            entries.append((tag, data[p:p+4])); p += 4
        elif tag == 15:
            entries.append((tag, data[p:p+3])); p += 3
        else:
            raise ValueError(f'unknown constant-pool tag {tag}')
        i += 1
    cp_end = p
    out = bytearray(data[:8])
    out += struct.pack('>H', cp_count + len(additions))
    for idx, (tag, value) in enumerate(entries, 1):
        if tag == 1:
            value = transform(idx, value)
            out.append(tag); out += struct.pack('>H', len(value)); out += value
        else:
            out.append(tag); out += value
    for tag, value in additions:
        out.append(tag)
        if tag == 1:
            out += struct.pack('>H', len(value)) + value
        else:
            out += value
    out += data[cp_end:]
    return bytes(out), cp_count


def patch_bq(data):
    data, _ = rebuild_cp(data, lambda i, x: b'socket://127.0.0.1:14444' if i == 53 else x)
    old = bytes([0x2b, 0xb6, 0x00, 0xca])
    new = bytes([0x2a, 0xb4, 0x00, 0x38])
    pos = data.find(old)
    if pos < 0:
        raise RuntimeError('bQ.H() patch pattern not found')
    return data[:pos] + new + data[pos+4:]


def patch_s(data):
    fixed = b'Offline:127.0.0.1:14444:0'
    old_cp = struct.unpack('>H', data[8:10])[0]
    new_utf = old_cp + 1
    new_string = new_utf + 1
    data, _ = rebuild_cp(
        data,
        additions=((1, fixed), (8, struct.pack('>H', new_utf))),
    )
    pattern = bytes.fromhex('bb006359b20040b700664cbb006859bb006a592b')
    pos = data.find(pattern)
    if pos < 0:
        raise RuntimeError('S.al() patch pattern not found')
    replacement = bytes([
        0x13, (new_string >> 8) & 0xff, new_string & 0xff,
        0x4b, 0xa7, 0x00, 0x47,
    ]) + bytes(63)
    if len(replacement) != 70:
        raise AssertionError
    return data[:pos] + replacement + data[pos+70:]


def patch_jar(source, target):
    source = Path(source); target = Path(target)
    with zipfile.ZipFile(source, 'r') as zin, zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            payload = zin.read(info.filename)
            if info.filename == 'bQ.class':
                payload = patch_bq(payload)
            elif info.filename == 'S.class':
                payload = patch_s(payload)
            zout.writestr(info, payload)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: patch-v7-offline.py INPUT.jar OUTPUT.jar')
        raise SystemExit(2)
    patch_jar(sys.argv[1], sys.argv[2])
    print(sys.argv[2])
