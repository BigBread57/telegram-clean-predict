from PIL import Image, ImageEnhance

# 323x550

# https://ast.ru/news/trekhkartochnye-rasklady-taro-dlya-nachinayushchikh/
# ЛИНЕЙНЫЕ ТРЕХКАРТОЧНЫЕ РАСКЛАДЫ ТАРО
new = Image.new("RGBA", (1023, 550))

img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
one = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/numbers/1.png")
two = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/numbers/2.png")
three = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/numbers/3.png")

new.paste(img, (0, 0))
new.paste(one, (150, 500))
new.paste(img, (350, 0))
new.paste(two, (500, 500))
new.paste(img, (700, 0))
new.paste(three, (850, 500))

new.show()


# СБАЛАНСИРОВАННЫЙ ТРЕХКАРТОЧНЫЙ РАСКЛАД ТАРО
# new = Image.new("RGBA", (1260, 1120))
#
# img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
#
# new.paste(img.rotate(-45, expand=True), (0, 500))
# new.paste(img.transpose(method=Image.FLIP_LEFT_RIGHT).rotate(45, expand=True), (640,500))
# new.paste(img, (466,0))
#
# new.show()


# ПЕРЕКРЕЩЕННЫЕ ТРЕХКАРТОЧНЫЕ РАСКЛАДЫ ТАРО
# new = Image.new("RGBA", (550, 1120))
#
# img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
#
# new.paste(img.rotate(90, expand=True), (0, 112))
# new.paste(img, (112, 0))
# new.paste(img, (112, 570))
#
# new.show()


# ФУНДАМЕНТАЛЬНЫЕ ТРЕХКАРТОЧНЫЕ РАСКЛАДЫ ТАРО
# new = Image.new("RGBA", (1023, 1100))
#
# img = Image.open("/home/gleb/Experience/telegram-clean-prediction/server/cards/inverted/1_the_magician.png")
#
# new.paste(img, (0,550))
# new.paste(img, (350,0))
# new.paste(img, (700,550))
#
# new.show()


