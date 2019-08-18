import json
from collections import Counter
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
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
        data = json.loads(request.body)

        if not self.is_valid(data):
            return EncodedJsonResponse({}, status=400)

        import_inst = Imports()
        import_inst.save()

        citizens = data['citizens']
        citizens_list = {}

        for citizen in citizens:
            relatives_tmp = citizen.pop('relatives')
            citizen_inst = Citizens(**citizen, import_id=import_inst)
            citizen_inst.save()
            citizens_list.update({citizen['citizen_id']: citizen_inst})
            citizen['relatives'] = relatives_tmp

        relative_pairs = self.get_relative_pairs(citizens, citizens_list)

        for relative_pair in relative_pairs:
            relative_inst = Relatives(citizen_1_id=relative_pair[0], citizen_2_id=relative_pair[1],
                                      import_id=import_inst)
            relative_inst.save()

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
        Check if date is valid date or not.
        """
        if not isinstance(date, str):
            return False

        try:
            datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            return False

        return True
