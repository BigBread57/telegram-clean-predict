from typing import Any, Dict, Optional


async def get_page(
    state_data: Dict[str, Any],
    callback_data: str,
) -> str:
    """Получить информацию о номере страницы."""
    # Если нажата кнопка со стрелками, то получаем номер страницы,
    # Если кнопка не нажата, то получаем информацию из хранилища или
    # возвращаем 1 страницу.
    if callback_data.find('pagination') != -1:
        return callback_data.split(' ')[1]
    if page := state_data.get('page'):
        return page
    return '1'


async def check_topic_key(
    callback_data: str,
    state_data: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """Получить информацию о выбранной теме."""
    # Если нажата кнопка с информацией о теме (не стрелки), то сверяем
    # полученный ключ, с теми ключами, которые у нас есть в хранилище.
    # Если ключ уже был, то удаляем его, если не было, то добавляем.
    if callback_data.find('key') != -1:
        if state_data and callback_data in state_data['client_topic_keys']:
            state_data['client_topic_keys'].remove(callback_data)
            return None
        return callback_data
    return None
