from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token= api)
dp = Dispatcher(bot, storage=MemoryStorage())

#создаем клавиатуру с кнопками(размер подстраиваемый
kb1 = ReplyKeyboardMarkup(resize_keyboard=True)

button1_1 = KeyboardButton(text = 'Рассчитать')
button1_2 = KeyboardButton(text = 'Информация')
button1_3 = KeyboardButton(text = 'Купить')
kb1.add(button1_1, button1_2)
kb1.add(button1_3)

#создаем инлайн клавиатуру с двумя кнопками
kb2 = InlineKeyboardMarkup()

button2_1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
button2_2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb2.add(button2_1, button2_2)

# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
kb3 = InlineKeyboardMarkup(resize_keyboard=True)
button3_1 = InlineKeyboardButton(text = 'Product1', callback_data='product_buying')
button3_2 = InlineKeyboardButton(text = 'Product2', callback_data='product_buying')
button3_3 = InlineKeyboardButton(text = 'Product3', callback_data='product_buying')
button3_4 = InlineKeyboardButton(text = 'Product4', callback_data='product_buying')
kb3.row(button3_1, button3_2, button3_3, button3_4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):# start(message) - присылает клавиатуру с кнопками
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb1)

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):# по нажатию кнопки"рассчитать" присылает инлайн клавиатуру
    await message.answer("Выберите опцию:", reply_markup = kb2)

@dp.callback_query_handler(text='formulas')# реагирует на нажатие кнопки
async def get_formulas(call): # присылать сообщение с формулой Миффлина-Сан Жеора.
    await call.message.answer("Упрощенный вариант формулы Миффлина-Сан Жеора "
                              "для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()
@dp.callback_query_handler(text = 'calories')# реагирует на нажатие кнопки
async def set_age(call):
    await call.message.answer("Введите свой возраст:")# функция выводит вTelegram - бот сообщение
    await call.answer()
    await UserState.age.set() # После ожидать ввода возраста в атрибут UserState.age при помощи метода set.


@dp.message_handler(state=UserState.age)#реагирует на переданное состояние UserState.age.
async def set_growth(message, state):
# функция должна обновлять данные в состоянии age на message.text
# Далее должна выводить в Telegram - бот сообщение 'Введите свой рост:'.
# После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)# реагирует  на переданное  состояние   UserState.growth.
async def set_weight(message, state):
# Эта функция должна обновлять данные в состоянии growth на message.text
# Далее должна выводить в Telegram - бот сообщение'Введите свой вес:'.
# После ожидать ввода роста в атрибут UserState.weightпри помощи метода set
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)# реагирует на переданное состояние UserState.weight.
async def send_calories(message, state):
# Эта функция должна обновлять данные в состоянии weight наmessage.text
    await state.update_data(weight=message.text)
    date = await state.get_data()# запомните в переменную data все ранее введённые состояния
# упрощённую формулу Миффлина-Сан Жеора для подсчёта нормы калорий(для женщин)
    kalorii = 10*int(date['weight']) + 6.25*int(date['growth']) - 5*int(date['age']) - 161
    await message.answer(f"Ваша норма калорий: {kalorii}")# Результат вычисления по формуле .
    await state.finish()# Финишируйте машину состояний методомfinish().

# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
@dp.message_handler(text=['Купить'])
async def get_buying_list(message):# выводить надписи. После каждой надписи выводите картинки к продуктам.
    for i in range(1, 5):
        with open(f'Product{i}.jpeg', 'rb') as img:
            await message.answer_photo(img, f"Название: Product {i} | Описание: описание {i} | Цена: {i * 100}")
        if i == 4:# В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
            await message.answer("Выберите продукт для покупки:", reply_markup=kb3)

# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
@dp.callback_query_handler(text='product_buying')# реагирует на нажатие кнопки
async def send_confirm_message(call):# присылает сообщение "Вы успешно приобрели продукт!"
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler()
async def all_massages(message):
    # all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы начать общение.'.
    # Запускается при любом обращении не описанном ранее. (используйте соответствующий декоратор)
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
