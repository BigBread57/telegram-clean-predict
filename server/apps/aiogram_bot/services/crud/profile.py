from typing import List, Tuple

import asyncstdlib

from server.apps.telegram_clean_prediction.models import Client
from server.apps.telegram_clean_prediction.models.profile import Profile


async def get_client_topic_names_and_keys(
    profile: Profile,
) -> Tuple[str, List[str]]:
    """Получение списка тема, в которых клиент может помочь."""
    client_topic_names = ''
    client_topic_keys = []
    # topics = [
    #     topic
    #     async for topic in Topic.objects.filter(profiles__client=client)
    # ]
    async for index, topic in asyncstdlib.enumerate(profile.topics.all()):
        client_topic_names += f'{index + 1}) {topic.name}.\n'
        client_topic_keys.append(topic.key)

    return (
        '\n' + client_topic_names if client_topic_names else 'не указаны\n',
        client_topic_keys,
    )
