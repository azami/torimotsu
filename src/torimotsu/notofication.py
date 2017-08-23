# -*- coding: utf-8 -*-
from enum import Enum

from slackclient import SlackClient

from torimotsu import settings


class SendError(Exception):
    def __init__(self, message):
        self.message = message


class MealTimeEmoji(Enum):
    fork_and_knife = 1
    doughnut = 2
    ramen = 3
    ice_cream = 4
    sake = 5
    cookie = 6


class Notifier(SlackClient):
    def __init__(self, log):
        super().__init__(token=settings.slack.token)
        self.log = log
        self.channel = settings.slack.channel

    def post_foods(self):
        lines = ['{}のたべものきろく。'.format(self.log.yesterday.strftime('%Y-%m-%d'))]
        food_log = self.log.fetch_foods()
        for (food_time, foods) in food_log.foods.items():
            lines.append(':{}: *{}*'.format(MealTimeEmoji(food_time.value).name, food_time.name))
            lines.append('```')
            for food in foods:
                lines.append('{calories:>4}㌔㌍ {name:25}: {amount}{unit_}'.format(
                    unit_=food['loggedFood']['unit']['plural'],
                    **food['loggedFood']))
            lines.append('```')
        lines.append('')
        lines.append(':yum: *{}* ㌔㌍摂取したよ。'.format(food_log.summary['calories']))
        diff = food_log.diff
        if diff > 0:
            lines.append(':innocent: *{}* ㌔㌍セーブしたよ。やったね。'.format(diff))
        else:
            lines.append(':imp: *{}* ㌔㌍余分にたべてしまいました。罪深い。'.format(diff * -1))
        self.send_slack('\n'.join(lines))

    def send_slack(self, text):
        response = self.api_call('chat.postMessage', channel=self.channel, text=text)
        if not response['ok']:
            raise SendError(response['message'])

