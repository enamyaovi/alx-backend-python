from django.test import TestCase

# Create your tests here.

class SomeTest(TestCase):
    def test_should_fail(self):
        self.assertFalse(True)

    def test_should_pass(self):
        self.assertTrue(True)
