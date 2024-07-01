#!/usr/bin/env python3

import hashlib
import os
import sys
from multiprocessing import Pool

BLOCK_SIZE = 2 ** 20
DISK_FULL_ERRNO = 28


def generate_hash_signature(data):
    return hashlib.sha512(str(data).encode())


def print_to_stdout(output, newline=False):
    sys.stdout.write(f"{output}\n" if newline else output)
    sys.stdout.flush()


def perform_disk_test(dest):
    test_index = 0
    os.makedirs(dest, exist_ok=True)
    while True:
        try:
            print_to_stdout(f"{test_index=}", newline=True)
            test_file = os.path.join(dest, f"test-{str(test_index).zfill(16)}.dat")
            blocks_written = write_data_to_disk(test_file, test_index)
            print_to_stdout("\n")
            verify_data_integrity(test_file, test_index, blocks_written)
            print_to_stdout("\n")
        except OSError as e:
            if e.errno == DISK_FULL_ERRNO:
                break
        test_index += 1


def write_data_to_disk(test_file, test_index):
    block_number = test_index * BLOCK_SIZE
    while True:
        try:
            sha_signature = generate_hash_signature(block_number)
            with open(test_file, 'ab') as file:
                file.write(sha_signature.digest())
        except OSError as e:
            if e.errno == DISK_FULL_ERRNO:
                break
        finally:
            block_number += 1
            print_to_stdout(f"\rWritten {block_number}")
        if block_number == (test_index + 1) * BLOCK_SIZE:
            break
    return block_number


def verify_data_integrity(test_file, test_index, blocks_written):
    block_number = test_index * BLOCK_SIZE
    with open(test_file, 'rb') as f:
        while True:
            sha_signature = generate_hash_signature(block_number)
            from_disk = f.read(64)
            block_number += 1
            if not from_disk:
                break
            if from_disk != sha_signature.digest():
                print_to_stdout("\n")
                print_to_stdout(from_disk)
                print_to_stdout(sha_signature.digest())
                raise Exception(f"mismatch at block {block_number}")
            else:
                print_to_stdout(f"\rChecked {block_number}/{blocks_written}")


if __name__ == '__main__':
    # Check if the destination is provided and if not, print a usage message and exit
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <disk_test_dest>")
        sys.exit(1)

    destinations = sys.argv[1:]

    # Create a new Pool of processes
    with Pool(processes=len(destinations)) as process_pool:
        # Use the Pool to map the perform_disk_test function onto each destination
        process_pool.map(perform_disk_test, destinations)
    sys.exit(0)
