
#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Any
import utils
import requests



class TestAccessNestedMap(unittest.TestCase):
    """
    A class for testing the utils script
    has methods

    """

    @parameterized.expand(
            [
                # (None, None, None),
                ({"a":1}, ["a"], 1),
                ({"a":{"b":2}}, ["a"], {"b":2}),
                ({"a":{"b":2}}, ["a","b"], 2)
            ]
    )
    def test_access_nested_map(self, nested_map:dict,path:list,result:Any) ->None:
        """
        a test to check that the accesss nested map fxn works as intended
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), result)

    @parameterized.expand(
            [
                ({}, ("a",)),
                ({"a": 1}, ("a", "b"))
            ]
    )
    def test_access_nested_map_exception(self, nested_map, path) -> None:
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)
            

class TestGetJson(unittest.TestCase):
    @parameterized.expand(
            [
                ("http://example.com", {"payload": True}),
                ("http://holberton.io", {"payload": False})            
            ]
    )
    def dummy(self, result):
        response = Mock()
        response.status_code = 200
        response.json.return_value = result
        return response

    @parameterized.expand(
            [
                ("http://example.com", {"payload": True}),
                ("http://holberton.io", {"payload": False})
            ]
    )
    def test_get_json(self, url, response):
        with patch("utils.requests", autospec=True) as mock_request:

            mock_request.get(url).json.return_value = response
            mock_request.get.assert_called_once_with(url)

            self.assertEqual(utils.get_json(url), response) #type:ignore


class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42
            
            @utils.memoize
            def a_property(self):
                return self.a_method()
            
        with patch.object(TestClass, 'a_method') as mock_method:

            mock_method.return_value = 42
            object = TestClass()
            some_property = object.a_property
            self.assertEqual(object.a_property, 42)
            mock_method.assert_called_once()
            