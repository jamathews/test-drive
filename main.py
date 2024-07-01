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


def is_disk_full_error(e):
    return e.errno == DISK_FULL_ERRNO


def calculate_test_file_path(disk_test_destination, test_index):
    test_file_name = f"test-{str(test_index).zfill(16)}.dat"
    return os.path.join(disk_test_destination, test_file_name)


def perform_disk_test(disk_test_destination):
    test_index = 0
    os.makedirs(disk_test_destination, exist_ok=True)
    while True:
        try:
            print_to_stdout(f"{test_index=}", newline=True)
            test_file_path = calculate_test_file_path(disk_test_destination, test_index)
            blocks_written = write_data_to_disk(test_file_path, test_index)
            print_to_stdout("\n")
            verify_data_integrity(test_file_path, test_index, blocks_written)
            print_to_stdout("\n")
        except OSError as e:
            if is_disk_full_error(e):
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
            if is_disk_full_error(e):
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
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <disk_test_dest>")
        sys.exit(1)
    disk_test_destinations = sys.argv[1:]
    with Pool(processes=len(disk_test_destinations)) as process_pool:
        process_pool.map(perform_disk_test, disk_test_destinations)
    sys.exit(0)
