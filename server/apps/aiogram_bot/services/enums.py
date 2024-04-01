import enum


class TypeChat(enum.Enum):

    TARGET = 'target'
    PARSER = 'parser'


class SearchType(enum.Enum):

    # Простой поиск по ключевым словам.
    SEARCH_BY_KEYWORDS = 'search_by_keywords'

    # Простой поиск по ключевым словам плюс подбираются синонимы к
    # введенным словам.
    SEARCH_BY_KEYWORDS_AND_SYNONYM = 'SEARCH_BY_KEYWORDS_AND_SYNONYM'

    # Поиск каналов по схожести тематик этих каналов (только 10).
    SEARCH_BY_SIMILAR_TOPIC = 'search_by_similar_topic'
