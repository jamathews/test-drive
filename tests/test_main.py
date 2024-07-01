import hashlib
import unittest

from main import generate_hash_signature


class TestHashGeneration(unittest.TestCase):

    def test_generate_hash_signature_content(self):
        data = "Test Data"
        hash_signature = generate_hash_signature(data)
        expected_output = hashlib.sha512(str(data).encode())
        self.assertEqual(hash_signature.hexdigest(), expected_output.hexdigest())

    def test_generate_hash_signature_different_data(self):
        data1 = "Test Data"
        data2 = "Test Different Data"
        hash_signature1 = generate_hash_signature(data1)
        hash_signature2 = generate_hash_signature(data2)
        self.assertNotEqual(hash_signature1.hexdigest(), hash_signature2.hexdigest())

    def test_generate_hash_signature_same_data(self):
        data1 = "Test Data"
        hash_signature1 = generate_hash_signature(data1)
        hash_signature2 = generate_hash_signature(data1)
        self.assertEqual(hash_signature1.hexdigest(), hash_signature2.hexdigest())

    def test_generate_hash_signature_case_sensitive(self):
        data1 = "Test Data"
        data2 = "test data"
        hash_signature1 = generate_hash_signature(data1)
        hash_signature2 = generate_hash_signature(data2)
        self.assertNotEqual(hash_signature1.hexdigest(), hash_signature2.hexdigest())


if __name__ == '__main__':
    unittest.main()
