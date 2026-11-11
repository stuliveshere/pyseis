#!/usr/bin/env python
"""
walk_seismic.py - Walk a directory tree and report SEG-Y / SEG-D files found.

For each directory containing seismic files, picks one random file per format
and prints its type, revision, endianness, and (for SEG-D) manufacturer code.

Usage:
    python walk_seismic.py /path/to/data
    python walk_seismic.py .
"""

import os
import sys
import random
from pathlib import Path
from collections import defaultdict

SEGY_EXTENSIONS = {'.sgy', '.segy'}
SEGD_EXTENSIONS = {'.sgd', '.segd'}


def probe_segy(filepath):
    """Probe a SEG-Y file and return a summary dict, or None on failure."""
    try:
        from pyseis.segy.reader import SEGYReader
        with SEGYReader(filepath) as reader:
            info = reader.probe()
            return {
                'type': 'SEG-Y',
                'revision': info['revision'],
                'endian': 'big' if info['endian'] == '>' else 'little',
                'format_code': info['format_code'],
                'traces': info['num_traces'],
                'samples': info['samples_per_trace'],
                'sample_interval_us': info['sample_interval_us'],
            }
    except Exception as e:
        return {'type': 'SEG-Y', 'error': str(e)}


def probe_segd(filepath):
    """Probe a SEG-D file and return a summary dict, or None on failure."""
    try:
        from pyseis.segd.reader import SEGDReader
        with SEGDReader(filepath) as reader:
            info = reader.probe()
            return {
                'type': 'SEG-D',
                'revision': info['revision'],
                'manufacturer': info.get('manufacturer', 'unknown'),
                'format_code': info['format_code'],
                'traces': info['num_traces'],
                'samples': info['samples_per_trace'],
                'sample_interval_us': info['sample_interval_us'],
                'channel_sets': info['num_channel_sets'],
                'gather_type': info.get('gather_type', '?'),
            }
    except Exception as e:
        return {'type': 'SEG-D', 'error': str(e)}


FORMAT_CODE_NAMES = {
    1: '4-byte IBM float',
    2: '4-byte integer',
    3: '2-byte integer',
    5: '4-byte IEEE float',
    6: '8-byte IEEE float',
    8: '1-byte integer',
    0x8058: '32-bit IEEE demux',
    0x8048: '16-bit integer demux',
    0x8036: '24-bit integer demux',
}


def format_code_label(code):
    return FORMAT_CODE_NAMES.get(code, f'0x{code:04X}' if code > 255 else str(code))


def print_result(filepath, result):
    """Pretty-print a probe result."""
    relpath = filepath
    size_kb = os.path.getsize(filepath) / 1024

    if 'error' in result:
        print(f"  {result['type']:5s}  {relpath}  ({size_kb:.0f} KB)")
        print(f"         ERROR: {result['error']}")
        return

    line = f"  {result['type']:5s}  {relpath}  ({size_kb:.0f} KB)"
    print(line)

    if result['type'] == 'SEG-Y':
        print(f"         Revision: {result['revision']}"
              f"  |  Endian: {result['endian']}"
              f"  |  Format: {format_code_label(result['format_code'])}")
        print(f"         Traces: {result['traces']}"
              f"  |  Samples: {result['samples']}"
              f"  |  dt: {result['sample_interval_us']} µs")

    elif result['type'] == 'SEG-D':
        print(f"         Revision: {result['revision']}"
              f"  |  Manufacturer: {result['manufacturer']}"
              f"  |  Format: {format_code_label(result['format_code'])}")
        print(f"         Traces: {result['traces']}"
              f"  |  Samples: {result['samples']}"
              f"  |  dt: {result['sample_interval_us']} µs"
              f"  |  Ch Sets: {result['channel_sets']}"
              f"  |  Gather: {result['gather_type']}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <directory>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Walking: {root}\n")

    dirs_scanned = 0
    files_found = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Group files by format
        segy_files = [f for f in filenames if Path(f).suffix.lower() in SEGY_EXTENSIONS]
        segd_files = [f for f in filenames if Path(f).suffix.lower() in SEGD_EXTENSIONS]

        if not segy_files and not segd_files:
            continue

        dirs_scanned += 1
        print(f"[{dirpath}]")

        if segy_files:
            pick = random.choice(segy_files)
            fullpath = os.path.join(dirpath, pick)
            files_found += 1
            label = f"(1 of {len(segy_files)})" if len(segy_files) > 1 else ""
            if label:
                print(f"  -- {len(segy_files)} SEG-Y files, sampling 1 random --")
            result = probe_segy(fullpath)
            print_result(fullpath, result)

        if segd_files:
            pick = random.choice(segd_files)
            fullpath = os.path.join(dirpath, pick)
            files_found += 1
            if len(segd_files) > 1:
                print(f"  -- {len(segd_files)} SEG-D files, sampling 1 random --")
            result = probe_segd(fullpath)
            print_result(fullpath, result)

        print()

    print(f"Done. Scanned {dirs_scanned} directories, probed {files_found} files.")


if __name__ == "__main__":
    main()
