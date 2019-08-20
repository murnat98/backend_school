import json
import os

from django.test import TestCase
from django.urls import reverse

from backend_school import settings


class ImportsTest(TestCase):
    @staticmethod
    def get_data_from_file(filename):
        """
        Get json data from test_data directory file.
        """
        with open(os.path.join(settings.BASE_DIR, 'citizens', 'test_data', filename), 'r') as file:
            content = file.read()

        return content

    def imports_post(self, test_filename):
        """
        POST request to /imports/
        :param test_filename: filename of test data
        :return: response
        """
        return self.client.post(reverse('citizens:imports'),
                                self.get_data_from_file(test_filename),
                                content_type='application/json')

    @staticmethod
    def get_wrong_files_list():
        """
        Get wrong test data list.
        """
        return os.listdir(os.path.join(settings.BASE_DIR, 'citizens', 'test_data', 'wrong_data'))

    def test_wrong_data(self):
        test_files = self.get_wrong_files_list()

        for test_file in test_files:
            response = self.imports_post('wrong_data/%s' % test_file)
            self.assertEqual(response.status_code, 400, msg=test_file)

    def test_right_data(self):
        response = self.imports_post('test_right_data.json')
        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertIsInstance(content, dict)
        self.assertIn('data', content)
        self.assertIn('import_id', content['data'])
