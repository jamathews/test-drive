#!/usr/bin/env python3

import os
import sys

BLOCK_SIZE = 2 ** 20
DEST = "/volume6/DeadShareTest"

import hashlib


def test_disk():
    test_index = 0
    while True:
        try:
            print(f"{test_index=}")

            test_file = os.path.join(DEST, f"test-{str(test_index).zfill(16)}.dat")
            blocks_written = write_test_data(test_file, test_index)
            sys.stdout.flush()
            print()

            check_test_data(test_file, test_index, blocks_written)
            sys.stdout.flush()
            print()
        except OSError as e:
            if e.errno == 28:  # There is no space left on the device
                break
        test_index += 1


def write_test_data(test_file, test_index):
    block_number = test_index * BLOCK_SIZE
    while True:
        try:
            sha_signature = hashlib.sha512(str(block_number).encode())

            with open(test_file, 'ab') as file:
                file.write(sha_signature.digest())
        except OSError as e:
            if e.errno == 28:  # There is no space left on the device
                break
        finally:
            block_number += 1
            sys.stdout.write(f"\rWritten {block_number}")
            sys.stdout.flush()
        if block_number == (test_index + 1) * BLOCK_SIZE:
            break
    return block_number


def check_test_data(test_file, test_index, blocks_written):
    block_number = test_index * BLOCK_SIZE
    with open(test_file, 'rb') as f:
        while True:
            sha_signature = hashlib.sha512(str(block_number).encode())
            from_disk = f.read(64)
            block_number += 1
            if not from_disk:
                break
            if not from_disk == sha_signature.digest():
                print()
                print(from_disk)
                print(sha_signature.digest())
                raise Exception(f"mismatch at block {block_number}")
            else:
                sys.stdout.write(f"\rChecked {block_number}/{blocks_written}")
                sys.stdout.flush()


if __name__ == '__main__':
    test_disk()
    sys.exit(0)
