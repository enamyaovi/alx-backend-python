#!/usr/bin/env python3

"""
Unit tests for the utils module.
"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Any
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function in utils.
    """

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(
        self, nested_map: dict, path: list, result: Any) -> None:
        """
        Test that access_nested_map returns the correct result
        for valid nested keys.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path) -> None:
        """
        Test that access_nested_map raises a KeyError
        when given invalid keys.
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function in utils.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def dummy(self, result):
        """
        Return a mock response object for use in tests.
        """
        response = Mock()
        response.status_code = 200
        response.json.return_value = result
        return response

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, response):
        """
        Test that get_json makes a GET request to the correct URL
        and returns the expected JSON payload.
        """
        with patch("utils.requests", autospec=True) as mock_request:
            mock_request.get(url).json.return_value = response
            mock_request.get.assert_called_once_with(url)
            self.assertEqual(utils.get_json(url), response)  # type: ignore


class TestMemoize(unittest.TestCase):
    """
    Tests for the memoize decorator in utils.
    """

    def test_memoize(self):
        """
        Test that memoize caches the result of a method after the first call.
        """
        class TestClass:
            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            obj = TestClass()
            _ = obj.a_property
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()
