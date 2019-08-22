import json
from collections import Counter
from datetime import datetime
from json import JSONDecodeError

from django.core.serializers.json import DjangoJSONEncoder
from django.db import DataError
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View

from citizens.models import Imports, Citizens, Relatives


class EncodedJsonResponse(JsonResponse):
    """
    JsonResponse with utf8 encoding.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        if json_dumps_params is None:
            json_dumps_params = {}

        json_dumps_params.update({'ensure_ascii': False})
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)


class CitizenFields:
    """
    Check functions of citizen fields.
    Return True if field value is right.
    """

    @staticmethod
    def is_valid_str_alnum(string):
        """
        Check if string is str, has not zero length, and there is at least 1 letter or digit.
        """
        if not isinstance(string, str):
            return False

        if len(string) <= 0 or len(string) > 256:
            return False

        for char in string:
            if char.isalnum():
                return True

        return False

    @staticmethod
    def is_valid_str(string):
        if not isinstance(string, str):
            return False

        if len(string) <= 0 or len(string) > 256:
            return False

        return True

    @staticmethod
    def is_valid_int(integer):
        if not isinstance(integer, int) or integer < 0:
            return False

        return True

    @staticmethod
    def is_valid_date(date):
        """
        Check if date has valid format or not.
        """
        if not isinstance(date, str):
            return False

        try:
            datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            return False

        return True

    @classmethod
    def check_town(cls, value):
        return cls.is_valid_str_alnum(value)

    @classmethod
    def check_street(cls, value):
        return cls.is_valid_str_alnum(value)

    @classmethod
    def check_building(cls, value):
        return cls.is_valid_str_alnum(value)

    @classmethod
    def check_apartment(cls, value):
        return cls.is_valid_int(value)

    @classmethod
    def check_name(cls, value):
        return cls.is_valid_str(value)

    @classmethod
    def check_birth_date(cls, value):
        return cls.is_valid_date(value)

    @classmethod
    def check_gender(cls, value):
        if value != 'male' or value != 'female':
            return False

        return True

    @classmethod
    def check_relatives(cls, value):
        if not isinstance(value, (list, tuple)):
            return False

        for item in value:
            if not cls.is_valid_int(item):
                return False

        return True


class ImportsView(View):
    def is_valid(self, data):
        """
        Check if passed data corresponds requested rules.
        """
        if not isinstance(data, dict):
            return False

        if 'citizens' not in data:
            return False

        citizens = data['citizens']

        if not isinstance(citizens, list):
            return False

        relatives_dict = {}
        citizens_list = []

        for citizen in citizens:
            if not self.citizen_is_valid(citizen):
                return False

            current_citizen_id = citizen['citizen_id']
            relatives = citizen['relatives']

            if not isinstance(relatives, (list, tuple)):
                return False

            checked_relatives = []
            for citizen_id in citizens_list:
                if current_citizen_id in relatives_dict[citizen_id]:
                    checked_relatives.append(citizen_id)

            for relative in relatives:
                if relative in citizens_list and relative not in checked_relatives:
                    return False

            relatives_dict.update({current_citizen_id: relatives})
            citizens_list.append(current_citizen_id)

        for index, count in Counter(citizens_list).items():
            if count > 1:
                return False

        return True

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return EncodedJsonResponse({}, status=400)

        if not self.is_valid(data):
            return EncodedJsonResponse({}, status=400)

        import_inst = Imports()
        import_inst.save()

        citizens = data['citizens']
        citizens_list = {}

        for citizen in citizens:
            relatives_tmp = citizen.pop('relatives')
            citizen_inst = Citizens(**citizen, import_id=import_inst)

            try:
                citizen_inst.save()
            except DataError:
                return EncodedJsonResponse({}, status=400)  # TODO: do not save to db (import), if error.

            citizens_list.update({citizen['citizen_id']: citizen_inst})
            citizen['relatives'] = relatives_tmp

        relative_pairs = self.get_relative_pairs(citizens, citizens_list)

        for relative_pair in relative_pairs:
            relative_inst = Relatives(citizen_1_id=relative_pair[0], citizen_2_id=relative_pair[1],
                                      import_id=import_inst)
            relative_inst.save()  # TODO: bulk create.

        return EncodedJsonResponse({'data': {'import_id': import_inst.id}}, status=201)

    def get_relative_pairs(self, citizens, citizens_list):
        """
        Get list of relative pairs.
        """
        relative_pairs = []

        for citizen in citizens:
            relatives = citizen['relatives']
            citizen_id = citizen['citizen_id']

            for relative in relatives:
                if relative > citizen_id:
                    relative_pairs.append((citizens_list[citizen_id], citizens_list[relative]))

        return relative_pairs

    def citizen_is_valid(self, citizen):
        """
        Check if citizen dict is valid.
        TODO: optimize this code.
        """
        if not isinstance(citizen, dict):
            return False

        if 'citizen_id' not in citizen:
            return False

        if not self.is_valid_int(citizen['citizen_id']):
            return False

        if 'town' not in citizen:
            return False

        if not self.is_valid_str(citizen['town']):
            return False

        if 'street' not in citizen:
            return False

        if not self.is_valid_str(citizen['street']):
            return False

        if 'building' not in citizen:
            return False

        if not self.is_valid_str(citizen['building']):
            return False

        if 'apartment' not in citizen:
            return False

        if not self.is_valid_int(citizen['apartment']):
            return False

        if 'name' not in citizen:
            return False

        if not self.is_valid_str(citizen['name']):
            return False

        if 'birth_date' not in citizen:
            return False

        if not self.is_valid_date(citizen['birth_date']):
            return False

        if 'gender' not in citizen:
            return False

        if not self.is_valid_str(citizen['gender']) or (citizen['gender'] != 'male' and citizen['gender'] != 'female'):
            return False

        if 'relatives' not in citizen:
            return False

        if len(citizen) != 9:
            return False

        return True

    def is_valid_str(self, string):
        """
        Check if string is instance of str and the length is more than 0.
        """
        if not isinstance(string, str) or len(string) <= 0:
            return False

        return True

    def is_valid_int(self, integer):
        """
        Check if integer is instance of int and the number is not negative.
        """
        if not isinstance(integer, int) or integer < 0:
            return False

        return True

    def is_valid_date(self, date):
        """
        Check if date has valid format or not.
        """
        if not isinstance(date, str):
            return False

        try:
            datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            return False

        return True


class ChangeImports(View):
    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return EncodedJsonResponse({}, status=400)

        if not self.is_valid_citizen(data):
            return EncodedJsonResponse({}, status=400)

        import_id = kwargs['import_id']
        citizen_id = kwargs['citizen_id']

        try:
            citizen = Citizens.objects.get(import_id=import_id, citizen_id=citizen_id)
        except Citizens.DoesNotExist or Citizens.MultipleObjectsReturned:
            return EncodedJsonResponse({}, status=400)

        for field_name, value in data.items():
            if field_name != 'relatives':
                setattr(citizen, field_name, value)

        try:
            citizen.save()
        except DataError:
            return EncodedJsonResponse({}, status=400)

        if 'relatives' in data:
            self.delete_old_relatives(import_id, citizen.id)
            if not self.add_new_relatives(import_id, citizen.id, data['relatives']):
                return EncodedJsonResponse({}, status=400)  # TODO: do not save to database if there is an error

        response_content = model_to_dict(citizen, exclude=('id', 'import_id'))
        response_content.update({'relatives': data['relatives']})

        return EncodedJsonResponse(response_content, status=200)

    @staticmethod
    def is_valid_citizen(citizen):
        """
        Check if passed data of citizen is valid.
        """
        allowed_fields = ('town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives')

        if not isinstance(citizen, dict):
            return False

        for field_name, value in citizen.items():
            if field_name not in allowed_fields:
                return False

            is_valid_field = getattr(CitizenFields, 'check_%s' % field_name)

            if not is_valid_field(value):
                return False

        return True

    @staticmethod
    def delete_old_relatives(import_id, citizen_id):
        """
        Delete from database old relatives of current citizen.
        """
        relatives = Relatives.objects.filter(import_id=import_id, citizen_1_id=citizen_id)
        relatives |= Relatives.objects.filter(import_id=import_id, citizen_2_id=citizen_id)
        relatives.delete()

    @staticmethod
    def add_new_relatives(import_id, citizen_id, relatives_list):
        """
        Add to database new relatives from relatives list.
        """
        relative_instances = []

        import_inst = Imports(pk=import_id)
        citizen_1 = Citizens(pk=citizen_id)

        citizens = list(Citizens.objects.filter(import_id=import_id).values('id', 'citizen_id'))
        for relative in relatives_list:
            citizen_2_id_found = False
            for citizen in citizens:
                if citizen['citizen_id'] == relative:
                    citizen_2_id = citizen['id']
                    citizen_2_id_found = True
                    break

            if not citizen_2_id_found:
                return False

            citizen_2 = Citizens(pk=citizen_2_id)  # TODO: try to optimize here (do not go to database)

            relative_instances.append(
                Relatives(import_id=import_inst, citizen_1_id=citizen_1, citizen_2_id=citizen_2)
            )

        Relatives.objects.bulk_create(relative_instances)

        return True
