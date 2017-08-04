import datetime
import json
from enum import Enum
from collections import defaultdict

import fitbit

from torimotsu import settings

FITBIT_TOKEN = '../../.token.json'


class MealType(Enum):
    """
    @see: https://dev.fitbit.com/docs/food-logging/#get-food-logs
    """
    breakfast = 1
    morning_snack = 2
    lunch = 3
    afternoon_snack = 4
    dinner = 5
    anytime = 6


class FoodLog(object):
    def __init__(self, log):
        self.summary = log['summary']
        self.goals = log['goals']
        logged = defaultdict(list)
        for food in log['foods']:
            logged[MealType(food['loggedFood']['mealTypeId'])].append(food)
        self.foods = logged

    @property
    def diff(self):
        return self.goals['calories'] - self.summary['calories']


def _read_credentials():
    with open(FITBIT_TOKEN) as f:
        return json.load(f)


def save_new_token(**kwargs):
    with open(FITBIT_TOKEN, 'w') as f:
        json.dump(kwargs, f)


class Log(object):
    def __init__(self):
        credentials = _read_credentials()
        access_token = credentials['access_token']
        refresh_token = credentials['refresh_token']
        self.client = fitbit.Fitbit(
            settings.fitbit.client_id,
            settings.fitbit.client_secret,
            access_token=access_token, refresh_token=refresh_token,
            refresh_cb=save_new_token,
            system='ja_JP')
        self.today = datetime.datetime.today()
        self.yesterday = self.today - datetime.timedelta(days=1)

    def fetch_foods(self) -> FoodLog:
        return FoodLog(self.client.foods_log(date=self.yesterday))

    @property
    def weight(self):
        weight = self.client.get_bodyweight(base_date=self.today)
        return weight
