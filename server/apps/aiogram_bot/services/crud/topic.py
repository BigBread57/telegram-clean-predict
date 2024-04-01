from server.apps.telegram_clean_prediction.models import Topic


class TopicStorage(object):
    """Класс-singleton для хранения информации о темах из БД."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Логика для singleton."""
        if cls._instance is None:
            cls._instance = super(TopicStorage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Инициализация переменных для работы."""
        self.topics = None
        self.amount = None
        self.set_values()

    def set_values(self):
        """Установка переменных."""
        self.topics = list(Topic.objects.all())
        self.amount = len(self.topics)


topic_storage = TopicStorage()
