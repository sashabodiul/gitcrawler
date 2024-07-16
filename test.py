import unittest
from crawler import search_github

class TestGithubCrawler(unittest.TestCase):
    def test_crawl_github_search(self):
        input_data = {
            "keywords": ["openstack"],
            "type": "Repositories"
        }
        results = search_github(input_data["keywords"], input_data["type"])
        self.assertGreater(len(results), 0)
        self.assertTrue(all('url' in result for result in results))

if __name__ == '__main__':
    unittest.main()