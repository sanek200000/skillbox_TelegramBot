from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='help',
                           url='https://www.youtube.com/watch?v=5_EHfHbzUCo&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=11')
ib2 = InlineKeyboardButton(text='url',
                           url='https://www.youtube.com/watch?v=5_EHfHbzUCo&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=11')
ikb.add(ib1).insert(ib2).insert(ib2).add(ib1)   # readme p.5
