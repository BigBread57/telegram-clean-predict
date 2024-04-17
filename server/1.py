from server.apps.telegram_clean_prediction.models import Card

# for card in Card.objects.all():
#     for type_layout, items in card.description.items():
#         for suit_type, desc in items.items():
#             if len(desc) > 1000:
#                 print(f'{card}: {type_layout}: {suit_type}')