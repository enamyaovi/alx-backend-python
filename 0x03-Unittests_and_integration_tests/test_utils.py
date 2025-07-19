#!/usr/bin/env python3

"""
Test suite for the utils module, including nested access,
HTTP JSON fetching, and memoization behavior.
"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Any, Dict, List
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map utility function in utils."""

    @parameterized.expand([
        ("a-level", {"a": 1}, ["a"], 1),
        ("one-nested", {"a": {"b": 2}}, ["a"], {"b": 2}),
        ("two-nested", {"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
        self,
        name: str,
        nested_map: Dict,
        path: List[str],
        result: Any
    ) -> None:
        """
        Test that access_nested_map returns the expected result
        for valid paths in a nested dictionary.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ("empty-dict", {}, ("a",)),
        ("missing-nested", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self,
        name: str,
        nested_map: Dict,
        path: List[str]
    ) -> None:
        """
        Test access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function in utils."""

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        name: str,
        url: str,
        response_data: Dict[str, Any]
    ) -> None:
        """
        Test that get_json returns the expected dictionary
        from a mocked HTTP GET request.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = response_data

        with patch(
            "utils.requests.get",
            return_value=mock_response
        ) as mock_get:
            self.assertEqual(utils.get_json(url), response_data)
            mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator in utils."""

    def test_memoize(self) -> None:
        """
        Test that the memoize decorator caches the result of
        a method after the first call.
        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @utils.memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            instance = TestClass()
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            mock_method.assert_called_once()
