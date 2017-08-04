from torimotsu.log import Log
from torimotsu.notofication import Notifier


if __name__ == '__main__':
    notifier = Notifier(Log())
    notifier.post_foods()
