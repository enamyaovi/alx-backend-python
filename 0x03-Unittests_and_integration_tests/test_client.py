#!/usr/bin/env python3
"""Unittest module for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from clients import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("clients.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload."""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )
        self.assertEqual(result, {"payload": True})

    @parameterized.expand([
        ("google",),
    ])
    @patch("clients.get_json")
    def test_public_repos_url(self, org_name, mock_get_json):
        """Test that _public_repos_url returns the expected URL."""
        mock_get_json.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient(org_name)
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/google/repos"
        )

    @patch("clients.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        test_payload = [
            {"name": "Repo1", "license": {"key": "mit"}},
            {"name": "Repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/example/repos"
            client = GithubOrgClient("example")
            repos = client.public_repos()

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/example/repos"
            )
            self.assertEqual(repos, ["Repo1", "Repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns correct boolean based on license key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class using fixtures."""

    org_payload = {}
    repos_payload = []
    expected_repos = []
    apache2_repos = []

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set side_effect for test URLs."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repos."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos)
