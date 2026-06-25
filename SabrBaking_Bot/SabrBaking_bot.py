import asyncio
import logging #все собитие терминала
import sqlite3
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

#--------------------------------------------------
#Удаление товара
class DeleteProduct(StatesGroup):
    id = State()
#--------------------------------------------------
    

TOKEN = "8764204152:AAFlWhoQxXlLVcccbl39wdEwa_sx3Z4yXWo"

#управление ботом 
#--------------------------------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
#--------------------------------------------------

#хранение базу данных
#--------------------------------------------------
connection = sqlite3.connect("my_data_SabrBaking.db")
connection.row_factory = sqlite3.Row   
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS baking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    title TEXT,
    photo TEXT,
    view TEXT,
    recipe TEXT,
    massa TEXT,
    price TEXT
)
""")
connection.commit()
#--------------------------------------------------

# проверка пустой базы
cursor.execute("SELECT COUNT(*) FROM baking")
count = cursor.fetchone()[0]

#показ и добавление данных
#--------------------------------------------------
if count == 0:
    cursor.execute("""
    INSERT INTO baking (category, title, photo, view, recipe, massa, price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Торты",
        "Bento Torte",
        "images/Bento Torte.jpg",
        "Фруктовое изделие",
        "Клубника в шоколаде",
        "Диаметр: 12 см",
        "120с ❌ 80с ✅"
    ))
    connection.commit()
#--------------------------------------------------

#start SabrBaking 
#--------------------------------------------------
@dp.message(Command("start"))
async def start_handler(message: types.Message):

    await message.answer(
    "🍰 <b>SabrBaking</b> 🎂\n\n"
    "Добро пожаловать в наш Telegram-бот!\n\n"
    "🤖 В этом боте находится вся информация о SabrBaking.\n"
    "🍓 Здесь вы сможете ознакомиться с нашими кондитерскими изделиями.\n"
    "📖 Узнать состав, рецепты и особенности продукции.\n"
    "🌐 Посетить другие наши проекты и предложения.\n"
    "ℹ️ Вся необходимая информация доступна в разделах бота.\n\n"
    "❓ Если у вас возникли вопросы, воспользуйтесь  Help.\n\n"
    "👇 Выберите действие ниже:",
        reply_markup=start_inline_menu(),
    parse_mode="HTML"
)
#--------------------------------------------------
    
#заказ через айди
#--------------------------------------------------
def product_keyboard(product_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Заказать",
                    callback_data=f"order_{product_id}"
                )
            ]
        ]
    )
#--------------------------------------------------
    
#меню  после старта
#--------------------------------------------------
def start_inline_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [  
                InlineKeyboardButton(text="❓ Help", callback_data="help"),
                InlineKeyboardButton(text="📋 Меню", callback_data="open_menu")
               
            ]
        ]
    )
    return keyboard
#--------------------------------------------------

#кнопка help в старт  меню
#--------------------------------------------------
@dp.message(F.text == "❓ Помощь")
async def help_message(message: Message):
    await message.answer(
        "❓ Выберите раздел помощи:",
        reply_markup=help_menu()
    )
#--------------------------------------------------

#btn-help  Для чего создан раздел Изделия?
#--------------------------------------------------
@dp.callback_query(F.data == "help_products")
async def help_products(callback: types.CallbackQuery):
    await callback.message.answer(
    "🍰 Для чего создан раздел Изделия?\n\n"
    "Раздел создан для просмотра кондитерских изделий.\n\n"
    "📖 Как использовать?\n"
    "1. Выберите категорию.\n"
    "2. Нажмите на нужное изделие.\n"
    "3. Посмотрите карточку товара."
)
    await callback.answer()
#--------------------------------------------------

#btn-help  ℹ️ О SabrBaking
#--------------------------------------------------
@dp.callback_query(F.data == "help_about")
async def help_about(callback: types.CallbackQuery):
    await callback.message.answer(
    "ℹ️ О SabrBaking\n\n"
    "Этот раздел создан, чтобы познакомить вас с нашей кондитерской.\n\n"
    "Здесь находится информация о нас, наших услугах и сотрудниках."
)

    await callback.answer()
#--------------------------------------------------

#для чего нужен раздел  сылки 
#--------------------------------------------------
@dp.callback_query(F.data == "help_social")
async def help_social(callback: types.CallbackQuery):
    await callback.message.answer(
        "Что можно  сделать в 🌐 социальних сетях SabrBaking ?"
        "через наши соц.сети вы можете найти что то интерестное для себя и для других"
        "инструкция: нажмите на сылку или фото чтобы открыт группу SabrBaking"
        "Если синую кнопку instagram то вы посетите наши пости, рилсы"
        "Если возникли затруднения то  обратитесь к админу этого  бота",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "help_admin")
async def help_admin(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔐 Админ-панель доступна только администратору.\n\n"
        "в этом разделе можно управлять ботом добавить меню или удалить"
        "это  может сделать только админ +992 99 800 31 06"
    )
    await callback.answer()

def help_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🍰 Изделия",
        callback_data="help_products"
    )

    builder.button(
        text="ℹ️ О SabrBaking",
        callback_data="help_about"
    )

    builder.button(
        text="🌐 Социальние сети",
        callback_data="help_social"
    )

    builder.button(
        text="🔐 Админ-панель",
        callback_data="help_admin"
    )

    builder.adjust(2)

    return builder.as_markup()

@dp.callback_query(F.data == "open_menu")
async def open_menu(callback: types.CallbackQuery):

    await callback.message.answer(
    "🍰 Добро пожаловать в меню SabrBaking!",
    reply_markup=main_menu()
)
    await callback.answer()


@dp.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):

    await callback.message.answer(
        "❓ Выберите раздел помощи:",
        reply_markup=help_menu()
    )

    await callback.answer()

#функции Sabrbaking
def main_menu():
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="ℹ️ О SabrBaking"),
        types.KeyboardButton(text="🍰 Изделия")
    )

    builder.row(
        types.KeyboardButton(text="🌐 Соцсети"),
        types.KeyboardButton(text="⚙️ Доп. функции")
    )

    builder.row(
        types.KeyboardButton(text="🔐 Админ-панель"),
        types.KeyboardButton(text="❓ Помощь")
    )

    return builder.as_markup(resize_keyboard=True)
    
    

@dp.message(F.text == "⚙️ Доп. функции")
async def order_handler(message: Message):
    
    await message.answer(
        "                                             <b>SabrBaking</b>                                                 \n\n"
        "в этом разделе скоро мы добавим функции как:\n"
        "калькулятор"
        "игры"
        "корзина",
        parse_mode="HTML"
    )
    
    
#Sabr Baking  ℹ️ О SabrBaking 
@dp.message(F.text == "ℹ️ О SabrBaking")
async def order_handler(message: Message):
    await message.answer(
        "🍰                                            <b>SabrBaking</b>                                                🎂\n\n"
        "✨ Вся информация о SabrBaking собрана в одном месте.\n"
        "✨ Наш бот поможет вам найти всё необходимое.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🍓 Узнайте больше о нашей кондитерской.\n"
        "🎂 Ознакомьтесь с нашей продукцией.\n"
        "👨‍🍳 Познакомьтесь с командой и услугами.\n"
        "📍 Найдите информацию о местоположении.\n\n"
        "👇 Выберите интересующий раздел:",
        parse_mode="HTML",
        reply_markup=food_inline_menu()
    )

#SabrBaking 
@dp.message(F.text == "🍰 Изделия")
async def show_categories(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🎂 Торты",
                callback_data="cat_Торты"
            )],
            [InlineKeyboardButton(
                text="🧁 Капкейки",
                callback_data="cat_Капкейки"
            )],
            [InlineKeyboardButton(
                text="🍮 Пирожные",
                callback_data="cat_Пирожные"
            )]
        ]
    )

    await message.answer(
        "Выберите категорию:",
        reply_markup=keyboard
    )
    
@dp.callback_query(F.data.startswith("cat_"))
async def open_category(callback: types.CallbackQuery):

    category = callback.data.replace("cat_", "")

    cursor.execute(
        "SELECT * FROM baking WHERE category=?",
        (category,)
    )

    products = cursor.fetchall()

    keyboard = InlineKeyboardBuilder()

    for product in products:
        keyboard.button(
            text=product[2],
            callback_data=f"product_{product[0]}"
        )

    keyboard.adjust(1)

    await callback.message.answer(
        f"{category}",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()
    
@dp.callback_query(F.data.startswith("product_"))
async def show_product(callback: types.CallbackQuery):

    product_id = int(callback.data.replace("product_", ""))

    cursor.execute(
        "SELECT * FROM baking WHERE id=?",
        (product_id,)
    )

    item = cursor.fetchone()

    if not item:
        await callback.answer("❌ Товар не найден")
        return

    photo = item[3]

    if not photo:
        await callback.message.answer("❌ Фото отсутствует")
        await callback.answer()
        return

    try:
        await callback.message.answer_photo(
            photo=photo,
            caption=(
                f"🎂 Название: {item[2]}\n\n"
                f"⚖️ Вес: {item[6]}\n"
                f"💰 Цена: {item[7]}\n\n"
                f"📋 Описание: {item[4]}\n"
                f"🍓 Состав: {item[5]}"
            ),
            reply_markup=product_keyboard(product_id)
        )
    except Exception as e:
        await callback.message.answer(
            f"❌ Ошибка отправки фото\n\n{e}"
        )

    await callback.answer()
        
@dp.message(F.text == "🌐 Соцсети")
async def social(message: Message):
    await message.answer(
        "🌐 Наши социальние сети:\n\n"
        "📸 нажмите на кнопку <a href='https://www.instagram.com/sabr.baking'>instagram</a> чтобы посмотрет  наши видео  ролики\n"
        "Telegram где можно легко посмотрет все наши кондитерские изделия: t.me/sabrbaking19\n\n"
        "Скоро  мы добавим наш web-site ждите новостей полная информация к админу",
         parse_mode="HTML"
    )


def food_inline_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Что означает  SabrBaking ?",
        callback_data="SabrBaking_info"
    )
    builder.button(
        text="Что мы готовим ?",
        callback_data="SabrBaking_cooking"
    )
    builder.button(
        text="Какие у нас услуги ?",
        callback_data="SabrBaking_services"
    )
    builder.button(
        text="Где мы находимся ?",
        callback_data="SabrBaking_locate"
    )
    builder.button(
        text="Информация о кондитерше ?",
        callback_data="SabrBaking_working"
    )
    builder.button(
        text="О нашем телеграм боте ?",
        callback_data="SabrBaking_workbot"
    )

    builder.adjust(2)
    return builder.as_markup()

@dp.callback_query(F.data == "SabrBaking_workbot")
async def sabr_info(callback: types.CallbackQuery):

    await callback.message.answer(
        "🍰 <b>О Telegram-боте SabrBaking</b>\n\n"
        "Добро пожаловать в официальный Telegram-бот SabrBaking!\n\n"
        "🤖 Этот бот создан для удобного знакомства с нашей кондитерской и быстрого получения всей необходимой информации.\n\n"     
        "<b>Возможности бота:</b>\n\n"       
        "🍰 Просмотр всех кондитерских изделий\n"
        "📂 Удобное разделение товаров по категориям\n"
        "📖 Подробная информация о каждом изделии\n"
        "🛒 Быстрое оформление заказа\n"
        "🌐 Переход в наши социальные сети\n"
        "ℹ️ Информация о SabrBaking и наших услугах\n"
        "📞 Связь с администратором\n\n"        
        "✨ Мы постоянно развиваем проект и добавляем новые функции для удобства клиентов.\n\n"       
        "<b>Планируется в будущем:</b>\n\n"
        "🧮 Калькулятор заказов\n"
        "🛍 Корзина товаров\n"
        "🎁 Система акций и скидок\n"
        "🎮 Небольшие игры и бонусы для клиентов\n\n"
        "⚠️ Бот находится в стадии развития. Если вы заметили ошибку или хотите предложить улучшение, пожалуйста, свяжитесь с администратором.\n\n"     
        "📞 Администратор:\n"
        "<code>+992 99 800 31 06</code>\n\n"
        "Спасибо, что выбираете <b>SabrBaking</b>! 🍓🎂",
        parse_mode="HTML"
    )

    await callback.answer()

@dp.callback_query(F.data == "SabrBaking_info")
async def sabr_info(callback: types.CallbackQuery):
    await callback.message.answer(
        "🍰 <b>Что означает SabrBaking?</b>\n\n"
        "✨ Название состоит из двух слов:\n\n"
        "🤲 <b>Sabr</b> — терпение.\n"
        "🎂 <b>Baking</b> — выпечка.\n\n"
        "💡 Для нас SabrBaking означает выпечку, созданную с терпением, заботой и любовью к своему делу.\n\n"
        "🍓 Мы стремимся создавать не только красивые, но и вкусные кондитерские изделия для каждого клиента."
        ,
        parse_mode="HTML"
    )
    
@dp.callback_query(F.data == "SabrBaking_cooking")
async def sabr_cooking(callback: types.CallbackQuery):

    await callback.message.answer(
        "🍰 <b>Что мы готовим?</b>\n\n"
        "В SabrBaking мы готовим домашние кондитерские изделия на заказ.\n\n"
        "🎂 Торты\n"
        "🧁 Капкейки\n"
        "🍮 Пирожные\n"
        "🍫 Шоколадные десерты\n"
        "🍓 Бенто-торты\n"
        "🎁 Сладкие наборы\n\n"
        "✨ Каждое изделие готовится из свежих ингредиентов с вниманием к качеству и вкусу.",
        parse_mode="HTML"
    )

    await callback.answer()
    
@dp.callback_query(F.data == "SabrBaking_services")
async def sabr_services(callback: types.CallbackQuery):

    await callback.message.answer(
        "🛎 <b>Наши услуги</b>\n\n"
        "Мы предлагаем:\n\n"
        "🎂 Изготовление тортов на заказ\n"
        "🧁 Капкейки для праздников\n"
        "🍓 Бенто-торты\n"
        "🎁 Сладкие подарочные наборы\n"
        "🎉 Десерты для дней рождения и мероприятий\n"
        "💬 Консультацию по выбору изделия\n\n"
        "✨ Каждый заказ обсуждается индивидуально, чтобы результат соответствовал вашим пожеланиям.",
        parse_mode="HTML"
    )

    await callback.answer()
    
@dp.callback_query(F.data == "SabrBaking_locate")
async def sabr_locate(callback: types.CallbackQuery):

    await callback.message.answer(
        "📍 <b>Где мы находимся?</b>\n\n"
        "🏠 Город: Бустон\n"
        "🇹🇯 Республика Таджикистан\n\n"
        "📞 Для заказа и уточнения информации:\n"
        "<code>+992 99 800 31 06</code>\n\n"
        "💬 Также вы можете связаться с нами через Telegram и Instagram.\n\n"
        "🍰 SabrBaking всегда рада новым клиентам!",
        parse_mode="HTML"
    )

    await callback.answer()
    
@dp.callback_query(F.data == "SabrBaking_working")
async def sabr_working(callback: types.CallbackQuery):

    await callback.message.answer(
        "👩‍🍳 <b>О кондитере SabrBaking</b>\n\n"
        "Здравствуйте!\n\n"
        "Меня зовут <b>Кадырова Сабрина</b>, я домашний кондитер из города Бустон.\n\n"
        "🎂 Уже более <b>3 лет</b> я занимаюсь приготовлением домашних тортов, десертов и сладких наборов на заказ.\n\n"
        "✨ В своей работе я уделяю особое внимание качеству ингредиентов, аккуратному оформлению и вкусу каждого изделия.\n\n"
        "🍓 Для вас доступны:\n"
        "• Торты на заказ\n"
        "• Бенто-торты\n"
        "• Капкейки\n"
        "• Сладкие наборы\n"
        "• Десерты для праздников и особых событий\n\n"
        "💖 Для меня важно, чтобы каждый заказ был не только красивым, но и по-настоящему вкусным, поэтому к каждому изделию я подхожу с любовью, вниманием и ответственностью.\n\n"
        "📞 Связаться со мной можно по номеру:\n"
        "<code>+992 99 800 31 06</code>\n\n"
        "С уважением,\n"
        "<b>Кадырова Сабрина</b>\n"
        "Основатель SabrBaking 🍰",
        parse_mode="HTML"
    )

    await callback.answer()


def back_help_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙 Назад",
        callback_data="back_sabr"
    )

    builder.button(
        text="❓ Помощь",
        callback_data="help_sabr"
    )

    builder.adjust(2)
    return builder.as_markup()


@dp.message(F.text.lower().in_({"id", "мой id", "-id-"}))
async def get_id(message: Message):
    await message.answer(
        f"Ваш Telegram ID:\n<code>{message.from_user.id}</code>",
        parse_mode="HTML"
    )
    
@dp.callback_query(F.data == "back_sabr")
async def back(callback: types.CallbackQuery):

    await callback.message.delete()
    await callback.answer()
    
#admin панел 
ADMIN_ID = 6587899261
@dp.message(F.text == "🔐 Админ-панель")
async def admin_panel(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        await message.answer(

            f"⛔ Нет доступа! {message.from_user.first_name}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Ваш id:<code> {message.from_user.id}</code> не совпадает"
            f"Доступно только админу ",
            parse_mode="HTML",
        )
        
        return
    

    await message.answer(
    f"🔐 Доступ разрешён, Добро пожаловать {message.from_user.first_name } в админ панель !\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    f"👤 Имя: {message.from_user.first_name}\n"
    f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
    f"Какие действия вы предпочитаете?",
    parse_mode="HTML",
    reply_markup=admin_menu()
    
    
)

def admin_menu():
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="➕ Добавить товар"),
        types.KeyboardButton(text="❌ Удалить товар")
    )

    builder.row(
        types.KeyboardButton(text="📋 Все товары"),
        types.KeyboardButton(text="🏠 Главное меню")
    )

    return builder.as_markup(resize_keyboard=True)

@dp.message(lambda m: m.text and "Главное меню" in m.text)
async def back_to_main(message: Message):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu()
    )

class AddProduct(StatesGroup):
    category = State()
    title = State()
    photo = State()
    view = State()
    recipe = State()
    massa = State()
    price = State()
    
@dp.message(F.text == "➕ Добавить товар")
async def add_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.clear()

    await message.answer("📂 Категория:")
    await state.set_state(AddProduct.category)

    
@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено")

@dp.message(AddProduct.category)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("🎂 Название:")
    await state.set_state(AddProduct.title)


@dp.message(AddProduct.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("📷 Отправь фото:")
    await state.set_state(AddProduct.photo)


@dp.message(AddProduct.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):

    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)

    await message.answer("4️⃣ Описание какого вида")
    await state.set_state(AddProduct.view)


@dp.message(AddProduct.photo)
async def photo_required(message: Message):
    await message.answer("❌ Отправьте фотографию товара.")


@dp.message(AddProduct.view)
async def add_view(message: Message, state: FSMContext):
    await state.update_data(view=message.text)
    await message.answer("5️⃣ рецепт содержимого")
    await state.set_state(AddProduct.recipe)


@dp.message(AddProduct.recipe)
async def add_recipe(message: Message, state: FSMContext):
    await state.update_data(recipe=message.text)
    await message.answer("6️⃣ Масса или размер")
    await state.set_state(AddProduct.massa)


@dp.message(AddProduct.massa)
async def add_massa(message: Message, state: FSMContext):

    await state.update_data(massa=message.text)

    await message.answer("7️⃣ Цена  добавьте со скидкой:  150❌ 130✅)")
    await state.set_state(AddProduct.price)

@dp.message(AddProduct.price)
async def add_price(message: Message, state: FSMContext):

    await state.update_data(price=message.text)

    data = await state.get_data()

    cursor.execute("""
        INSERT INTO baking (category, title, photo, view, recipe, massa, price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["category"],
        data["title"],
        data["photo"],
        data["view"],
        data["recipe"],
        data["massa"],
        data["price"],
    ))

    connection.commit()

    await message.answer("✅ Товар добавлен!")
 
    await state.clear()



@dp.message(F.text == "📋 Все товары")
async def all_products(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT * FROM baking")
    items = cursor.fetchall()

    if not items:
        await message.answer("❌ Товаров нет.")
        return

    text = "📋 Список товаров:\n\n"

    for item in items:
        text += (
        f"🆔 {item[0]}\n"
        f"📂 Категория: {item[1]}\n"
        f"🎂 Название: {item[2]}\n"
        f"💰 Цена: {item[7]}с\n\n"
    )
    await message.answer(text)
    
@dp.message(DeleteProduct.id)
async def delete_product(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        product_id = int(message.text)
    except:
        await message.answer("❌ Введите число")
        return

    cursor.execute("DELETE FROM baking WHERE id=?", (product_id,))

    if cursor.rowcount == 0:
        await message.answer("❌ Товар не найден")
    else:
        connection.commit()
        await message.answer("🗑 Товар удалён")

    await state.clear()

  
@dp.message(F.text == "❌ Удалить товар")
async def delete_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT id, title, category FROM baking")
    items = cursor.fetchall()

    if not items:
        await message.answer("❌ Товаров нет.")
        return

    text = "🗑 Список товаров для удаления:\n\n"

    for item in items:
        text += (
            f"🆔 {item[0]}\n"
            f"🎂 {item[1]}\n"
            f"📂 {item[2]}\n\n"
        )

    await message.answer(text)

    await message.answer("✏️ Введите ID товара, который нужно удалить:")
    await state.set_state(DeleteProduct.id)


@dp.callback_query(F.data.startswith("order_"))
async def order_button(callback: types.CallbackQuery):

    product_id = int(callback.data.split("_")[1])

    cursor.execute("SELECT * FROM baking WHERE id=?", (product_id,))
    item = cursor.fetchone()

    if not item:
        return await callback.answer("Товар не найден")

    user_id = callback.from_user.id
    user_name = callback.from_user.username

    if user_name:
        user_text = f"@{user_name}"
    else:
        user_text = callback.from_user.first_name

    order_text = (
        "🛒 НОВЫЙ ЗАКАЗ\n\n"
        f"👤 Пользователь: {user_text}\n"
        f"🆔 ID: {user_id}\n\n"
        f"🎂 Товар: {item[2]}\n"
        f"📂 Категория: {item[1]}\n"
        f"⚖️ Вес: {item[6]}\n"
        f"💰 Цена: {item[7]}\n"
        f"🍓 Состав: {item[5]}"
    )

    buttons = []

    if user_name:
        buttons.append(
        InlineKeyboardButton(
            text="✍️ Написать",
            url=f"https://t.me/{user_name}"
        )
    )

    buttons.append(
    InlineKeyboardButton(
        text="✅ Подтвердить",
        callback_data=f"confirm_{user_id}"
    )
)

    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[buttons]
)
    


    await bot.send_message(ADMIN_ID, order_text, reply_markup=keyboard)

    await callback.answer("Заказ отправлен")
    
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: types.CallbackQuery):

    user_id = int(callback.data.split("_")[1])

    await bot.send_message(
        user_id,
        "✅ Ваш заказ подтверждён!\n\n🍰 Мы уже начали готовить ваш заказ.\n"
        "Мы вам напишем"
    )

    await callback.answer()

async def main():
    await dp.start_polling(bot)

try:
    asyncio.run(main())
finally:
    connection.close()