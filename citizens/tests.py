import json
import os

from django.test import TestCase
from django.urls import reverse

from backend_school import settings
from citizens.models import Citizens, Relatives, Imports


# TODO: TEST!
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

            all_citizens = list(Citizens.objects.all().values())
            self.assertEqual(len(all_citizens), 0, msg='Some data written to citizens database')

            all_imports = list(Imports.objects.all().values())
            self.assertEqual(len(all_imports), 0, msg='Some data written to imports database')

            all_relatives = list(Relatives.objects.all().values())
            self.assertEqual(len(all_relatives), 0, msg='Some data written to relatives database')

    def test_right_data(self):
        response = self.imports_post('test_right_data.json')
        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertIsInstance(content, dict)
        self.assertIn('data', content)
        self.assertIn('import_id', content['data'])

        import_id = content['data']['import_id']

        try:
            Imports.objects.get(import_id=import_id)
        except Imports.DoesNotExist:
            self.fail('DoesNotExist raised')

        try:
            citizens = list(Citizens.objects.filter(import_id=import_id).values())
        except Citizens.DoesNotExist:
            self.fail('DoesNotExist raised')

        self.assertEqual(len(citizens), 6)

        try:
            relatives = list(Relatives.objects.filter(import_id=import_id).values())
        except Relatives.DoesNotExist:
            self.fail('DoesNotExist raised')

        self.assertEqual(len(relatives), 5)


class ChangeCitizensTest(TestCase):
    def setUp(self):
        response = self.client.post(reverse('citizens:imports'),
                                    ImportsTest.get_data_from_file('test_right_data.json'),
                                    content_type='application/json')

        content = json.loads(response.content)
        self.import_id = content['data']['import_id']

    def test_fields(self):
        response = self.client.patch(
            reverse('citizens:change_imports', kwargs={'import_id': self.import_id, 'citizen_id': 2}),
            {'town': 'Керчь', 'apartment': 19}
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', content)

        citizen = content['data']

        self.assertIn('town', citizen)
        self.assertEqual(citizen['town'], 'Керчь')
        self.assertIn('apartment', citizen)
        self.assertEqual(citizen['apartment'], 19)
        self.assertIn('citizen_id', citizen)
        self.assertEqual(citizen['citizen_id'], 2)
        self.assertIn('birth_date', citizen)
        self.assertEqual(citizen['birth_date'], '26.12.1986')

        citizen_instance = Citizens.objects.get(import_id=self.import_id, citizen_id=2)

        self.assertEqual(citizen_instance.town, 'Керчь')
        self.assertEqual(citizen_instance.apartment, 19)
        self.assertEqual(citizen_instance.name, 'Иванов Иван Иванович')

    def test_relatives(self):
        new_relatives = [3, 4]

        response = self.client.patch(
            reverse('citizens:change_imports', kwargs={'import_id': self.import_id, 'citizen_id': 2}),
            {"relatives": new_relatives}
        )

        content = json.loads(response.content)

        self.assertEqual(content['data']['relatives'], new_relatives)

        citizen = Citizens.objects.get(import_id=self.import_id, citizen_id=2)

        relatives = Relatives.objects.filter(import_id=self.import_id, citizen_1_id=citizen.id)
        relatives |= Relatives.objects.filter(import_id=self.import_id, citizen_2_id=citizen.id)

        for relative in relatives:
            citizen_1_id = relative.citizen_1_id
            citizen_2_id = relative.citizen_2_id

            if citizen_1_id == citizen.id:
                relative_id = citizen_2_id
            else:
                relative_id = citizen_1_id

            self.assertIn(relative_id, new_relatives)


class CitizensListTest(TestCase):
    def setUp(self):
        response = self.client.post(
            reverse('citizens:imports'), ImportsTest.get_data_from_file('test_right_data.json'),
            content_type='application/json'
        )

        self.import_id = response.content['data']['import_id']

    def test_wrong_request(self):
        response = self.client.get(reverse('citizens:list', kwargs={'import_id': self.import_id + 1}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_right_request(self):
        response = self.client.get(reverse('citizens:list', kwargs={'import_id': self.import_id}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIn('data', content)
        data = content['data']
        self.assertIsInstance(data, (list, tuple))
        self.assertEqual(len(data), 6)


class CitizensBirthDayStat(TestCase):
    def setUp(self):
        response = self.client.post(reverse('citizens:imports'), ImportsTest.get_data_from_file('test_right_data.json'),
                                    content_type='application/json')

        self.import_id = response['data']['import_id']

    def test_wrong_birthdays(self):
        response = self.client.get(reverse('citizens:birthdays', kwargs={'import_id': self.import_id}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_right_birthdays(self):
        response = self.client.get(reverse('citizens:birthdays', kwargs={'import_id': self.import_id}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('data', data)
        birthdays = data['data']

        empty_birthdays = ('1', '2', '3', '5', '6', '7', '8', '9', '10')

        for birthday in empty_birthdays:
            self.assertEqual(len(birthdays[birthday]), 0)

        april_presents = birthdays['4']
        november_presents = birthdays['11']
        december_presents = birthdays['12']

        self.assertEqual(len(april_presents), 1)
        self.assertEqual(april_presents[0]['citizen_id'], 2)
        self.assertEqual(april_presents[0]['presents'], 1)

        self.assertEqual(len(november_presents), 4)
        self.assertEqual(len(december_presents), 2)
