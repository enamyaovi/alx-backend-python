
#!/bin/usr/env python3

import unittest
from unittest.mock import Mock, patch, PropertyMock
import clients, utils
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
import requests


class TestGithubOrgClient(unittest.TestCase):

    config = {}

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch("clients.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"payload":"data"}
        x = clients.GithubOrgClient(org_name)
        payload = x.org
        mock_get_json.assert_called_once()
        mock_get_json.assert_called_once_with(clients.GithubOrgClient.ORG_URL.format(org=org_name))
        self.assertIsInstance(payload, dict)

    @parameterized.expand([
        ('google',)
    ])
    def test_public_repos_url(self, org_name):
        with patch("clients.get_json", autospec=True) as mock_get_json:
            mock_get_json.return_value = {"payload":"data", "repos_url":"example.com"}
            x = clients.GithubOrgClient(org_name)
            x_url = x._public_repos_url
            self.assertEqual(x_url, "example.com")

    @patch("clients.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = {"1":{"name":"example", "repos_url":"https://api.github.com/orgs/example", "license":{"key":"11"}}}
        with patch.object(clients.GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos:
            mock_public_repos.return_value = "https://api.github.com/orgs/example"
            x = clients.GithubOrgClient('example')
            
            res = x.repos_payload
            mock_public_repos.assert_called_once()
            mock_get_json.assert_called_once()
            mock_get_json.assert_called_once_with(clients.GithubOrgClient.ORG_URL.format(org='example'))

            self.assertEqual(res, mock_get_json('https://api.github.com/orgs/example'))


    @parameterized.expand(
            [
                ({"license": {"key": "my_license"}}, "my_license", True),
                ({"license": {"key": "other_license"}}, "my_license", False),
            ]
    )
    def test_has_license(self, repo, license_key, response):
        self.assertEqual(clients.GithubOrgClient.has_license(repo, license_key), response)


@parameterized_class([
    {'org_payload':TEST_PAYLOAD[0], 'repos_payload':TEST_PAYLOAD[0][1], 'expected_repos':TEST_PAYLOAD[0][2], 'apache2_repos':TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def mock_reponse(cls):
        response = Mock()
        response.return_value = TEST_PAYLOAD[0][1]
        return response

    # @patch("__main__.requests.get")
    @classmethod
    def setUpClass(cls):
        
        cls.get_patcher = patch("requests.get")
        cls.mock_requests = cls.get_patcher.start()
        cls.mock_requests.side_effect = cls.mock_reponse
        pass
    

    @classmethod
    def tearDownClass(cls) -> None:
        cls.get_patcher.stop()
