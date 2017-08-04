import yaml
from collections import namedtuple


SETTINGS_FILE = '../../settings.yml'
Fitbit = namedtuple('Fitbit', ['client_id', 'client_secret', 'system'])
Slack = namedtuple('Slack', ['token', 'channel'])


def _load():
    with open(SETTINGS_FILE) as f:
        settings = yaml.load(f.read())
    return (Fitbit(**settings['fitbit']), Slack(**settings['slack']))

(fitbit, slack) = _load()

