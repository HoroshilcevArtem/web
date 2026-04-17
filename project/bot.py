import random
import os
import asyncio
import sqlite3
import re
import datetime
from io import BytesIO

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def path(*args):
    return os.path.join(BASE_DIR, *args)

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❗️Как играть❓")],
        [KeyboardButton(text="📰Новости👮‍♂️")],
        [KeyboardButton(text="👤Профиль💼")]
    ],
    resize_keyboard=True
)

# === КОНФИГУРАЦИЯ ===
API_TOKEN = "8498090368:AAEaa2asEpTwWHZK7yVDGGpiieHPz6Sls5A"
WIDTH, HEIGHT = 350, 200
CELL = 100 
REEL_WIDTH, REEL_HEIGHT = 110, 110
REEL_Y = HEIGHT // 2 - REEL_HEIGHT // 2
REEL_X = [0, 120, 240]

FPS = 10
TOTAL_SECONDS = 12  # Увеличили до 12 секунд
TOTAL_FRAMES = FPS * TOTAL_SECONDS
STOP_TIMES = [7, 8, 9] # Тайминги остановки по ТЗ

NAMES_FRUITS = ["🍒 Вишня", "🍋 Лимон", "🍊 Апельсин", "🔔 Колокольчик", "💎 Алмаз", "🎰 BAR"]
NAMES_ROBBERY = ["🤖 Робот-1", "👤 Робот-2", "🚁 Дрон", "💵 Пачка денег", "🗄 Сейф", "💰 Мешок", "🔫 Винтовка", "🏆 Слитки", "👜 Сумка"]

BONUSES = [
    10000, 25000, 50000, 75000,
    100000, 150000, 200000,
    300000, 400000, 500000
]

user_locks = {}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", ".")

def get_user_lock(user_id: int) -> asyncio.Lock:
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]

# === БД ===
def init_db():
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 1000,
        wins INTEGER DEFAULT 0,
        last_bonus INTEGER DEFAULT 0
    )
    """)

    try:
        cur.execute("ALTER TABLE users ADD COLUMN wins INTEGER DEFAULT 0")
        cur.execute("ALTER TABLE users ADD COLUMN last_bonus INTEGER DEFAULT 0")
    except:
        pass

    conn.commit()
    conn.close()

def get_user(user_id, username):
    username = (username or "Игрок")[:10]  # ограничение 10 символов

    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()

    if res is None:
        cur.execute(
            "INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)",
            (user_id, username, 1000)
        )
        conn.commit()
        conn.close()
        return 1000
    else:
        # обновляем ник если изменился
        cur.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
        conn.commit()

    conn.close()
    return res[0]

def update_balance(user_id, amount):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def add_win(user_id):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET wins = wins + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute("SELECT username, balance, wins FROM users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()
    conn.close()
    return res

BONUS_COOLDOWN = 3 * 60 * 60  # 3 часа


def get_last_bonus(user_id):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute("SELECT last_bonus FROM users WHERE user_id = ?", (user_id,))
    res = cur.fetchone()
    conn.close()
    return res[0] if res else 0


def update_last_bonus(user_id):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET last_bonus = ? WHERE user_id = ?",
        (int(datetime.datetime.now().timestamp()), user_id)
    )
    conn.commit()
    conn.close()

def get_rank(wins):
    if wins >= 60:
        return "🪖 Майор"
    elif wins >= 40:
        return "🎖 Лейтенант"
    elif wins >= 10:
        return "🔰 Младший лейтенант"
    else:
        return "🐣 Новобранец"

def split_goose_sprites():
    # Путь к папке
    folder = r"D:\program\Python\goose\гуси"
    input_path = os.path.join(folder, "гуси.jpg")
    
    if not os.path.exists(input_path):
        print(f"❌ Файл не найден: {input_path}")
        return

    # Открываем оригинал
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    # Определяем четверти
    half_w = w // 2
    half_h = h // 2

    # Координаты: (left, top, right, bottom)
    parts = [
        ("recruit.png", (0, 0, half_w, half_h)),      # Верхний левый
        ("junior.png", (half_w, 0, w, half_h)),       # Верхний правый
        ("lieutenant.png", (0, half_h, half_w, h)),   # Нижний левый
        ("major.png", (half_w, half_h, w, h)),        # Нижний правый
    ]

    for name, box in parts:
        # Режем
        part = img.crop(box)
        
        # Сохраняем в PNG
        save_path = os.path.join(folder, name)
        part.save(save_path, "PNG")
        print(f"✅ Сохранено: {name}")

    print("\n🚀 Все гуси нарезаны и конвертированы в PNG")

def generate_goose_profile(wins):
    # 1. Пути к нарезанным PNG (которые мы получили из JPG)
    if wins >= 60:
        img_path = path("goose", "lieutenant.png")
    elif wins >= 40:
        img_path = path("goose", "junior.png")
    elif wins >= 10:
        img_path = path("goose", "recruit.png")
    else:
        img_path = path("goose", "major.png")

    goose = Image.open(img_path).convert("RGBA")

    # --- ХАК: Делаем ЗЕЛЕНЫЙ фон прозрачным ---
    datas = goose.getdata()
    newData = []
    for item in datas:
        r, g, b, a = item
        # Условие для хромакея: если зеленого много, а красного и синего мало
        # Значения 150 и 100 можно немного подкрутить для идеального результата
        if g > 100 and g > r * 1.3 and g > b * 1.3:
            newData.append((0, 0, 0, 0))  # Полная прозрачность
        else:
            newData.append(item)
    goose.putdata(newData)
    # ------------------------------------------

    # 3. Открываем фон
    bg = Image.open(path("assets", "фон 2.jpg")).convert("RGBA")
    
    # Масштабируем фон под гуся
    bg = bg.resize(goose.size, Image.Resampling.LANCZOS)

    # 4. Наложение (теперь маска 'goose' сработает, так как мы сделали прозрачность)
    bg.paste(goose, (0, 0), goose)
    
    # 5. Сохранение
    final_img = bg.convert("RGB")
    buffer = BytesIO()
    final_img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

# === ОБРАБОТКА ИЗОБРАЖЕНИЙ ===
def load_symbols_from_sprite(path, names_list):
    try:
        sprite = Image.open(path).convert("RGBA")
        symbols_dict = {}
        w, h = sprite.size
        cols, rows = 3, (len(names_list) + 2) // 3
        cell_w, cell_h = w // cols, h // rows
        index = 0
        for row in range(rows):
            for col in range(cols):
                if index >= len(names_list): break
                sym = sprite.crop((col * cell_w, row * cell_h, (col+1) * cell_w, (row+1) * cell_h))
                pixels = sym.load()
                for py in range(sym.height):
                    for px in range(sym.width):
                        r, g, b, a = pixels[px, py]
                        if r < 45 and g < 45 and b < 45: pixels[px, py] = (0, 0, 0, 0)
                bbox = sym.getbbox()
                if bbox: sym = sym.crop(bbox)
                final = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
                sym.thumbnail((80, 80), Image.Resampling.LANCZOS)
                final.paste(sym, ((CELL-sym.width)//2, (CELL-sym.height)//2), sym)
                symbols_dict[names_list[index]] = final
                index += 1
        return symbols_dict
    except: return {}

SET_1 = load_symbols_from_sprite(
    path("assets", "fruits.png"),
    NAMES_FRUITS
)

SET_2 = load_symbols_from_sprite(
    path("assets", "robbery.png"),
    NAMES_ROBBERY
)
# === ГЕНЕРАЦИЯ АНИМАЦИИ ===
def generate_slot_gif():
    current_set = SET_1 if random.random() < 0.5 else SET_2
    keys = list(current_set.keys())
    if random.random() < 0.6:
        # ВЫИГРЫШ (60%)
        sym = random.choice(keys)
        result = [sym, sym, sym]
    else:
        # ПРОИГРЫШ (40%)
        result = [random.choice(keys) for _ in range(3)]
        
        # гарантируем, что не все одинаковые
        while result[0] == result[1] == result[2]:
            result = [random.choice(keys) for _ in range(3)]
    
    frames = []
    offsets = [0, 0, 0]
    stop_frames = [t * FPS for t in STOP_TIMES]

    for frame in range(TOTAL_FRAMES):
        img = Image.new("RGBA", (WIDTH, HEIGHT), "#111111")
        draw = ImageDraw.Draw(img)
        
        for i in range(3):
            rx = REEL_X[i]
            sf = stop_frames[i]
            
            # Если время не вышло - крутим
            if frame < sf:
                speed = 30 # Скорость падения
                offsets[i] = (frame * speed) % CELL
            else:
                offsets[i] = 0 # Стоп

            center_y = REEL_Y + REEL_HEIGHT // 2 - CELL // 2
            
            for j in range(-2, 3):
                # Логика: если барабан стоит, в центре (j=0) всегда результат
                if frame >= sf and j == 0:
                    sym = result[i]
                else:
                    # Рандомные символы для эффекта кручения
                    # Используем frame+j для детерминированного, но меняющегося вида
                    seed = (frame + j + (i * 100)) % len(keys)
                    sym = keys[seed]

                # Отрисовка со смещением (падение вниз)
                yy = center_y + (j * CELL) + offsets[i]
                img.paste(current_set[sym], (rx + 5, int(yy)), current_set[sym])

            # Рамки
            draw.rectangle([rx, REEL_Y, rx + REEL_WIDTH, REEL_Y + REEL_HEIGHT], outline="white", width=3)
        
        # Линии
        for rx in REEL_X:
            draw.rectangle([rx + 5, HEIGHT // 2 - 2, rx + REEL_WIDTH - 5, HEIGHT // 2 + 2], fill="#ffd700aa")

        frames.append(img.convert("RGB"))

    # Сжатие
    frames = [f.convert("P", palette=Image.ADAPTIVE, colors=64) for f in frames]
    buffer = BytesIO()
    frames[0].save(buffer, format="GIF", save_all=True, append_images=frames[1:], duration=100, loop=0)
    buffer.seek(0)
    return buffer, result

# === ХЕНДЛЕРЫ ===
async def spin(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.full_name
    balance = get_user(user_id, username)

    match = re.search(r"(\d+)(%?)", message.text)
    if not match:
        return await message.answer("❌ Формат: Слот [ставка]", reply_to_message_id=message.message_id)
    
    val, is_percent = int(match.group(1)), match.group(2) == "%"
    bet = int(balance * val / 100) if is_percent else val

    if bet <= 0 or bet > balance:
        return await message.answer(f"❌ Недостаточно средств ({balance})", reply_to_message_id=message.message_id)

    update_balance(user_id, -bet)

    try:
        use_gif = random.random() < 0.5
        res = None

        if use_gif:
            gif, res = generate_slot_gif()
            file = BufferedInputFile(gif.read(), filename="slot.gif")
            sent = await message.answer_animation(
                file,
                caption=f"🎰 Ставка: {bet}\nУдачи!",
                reply_to_message_id=message.message_id
            )
            await asyncio.sleep(10)
        else:
            current_set = SET_1 if random.random() < 0.5 else SET_2
            keys = list(current_set.keys())

            if random.random() < 0.6:
                sym = random.choice(keys)
                res = [sym, sym, sym]
            else:
                res = [random.choice(keys) for _ in range(3)]
                while res[0] == res[1] == res[2]:
                    res = [random.choice(keys) for _ in range(3)]

            sent = await text_slot_animation(message, res, bet)

        # === ОСНОВНОЙ РЕЗУЛЬТАТ ===
        win = res[0] == res[1] == res[2]

        if win:
            reward = bet * 3
            update_balance(user_id, reward)
            add_win(user_id)
            status = f"🎉 ВЫИГРАЛ: {format_money(reward)}!"
        else:
            reward = 0
            status = "😢 ПРОИГРАЛ"

        new_bal = get_user(user_id, username)

        final_text = f"🎰СЛОТ-МАШИНА🎰\n{' | '.join(res)}\n{status}\n💰 Баланс: {format_money(new_bal)}"

        if use_gif:
            await sent.edit_caption(caption=final_text)
        else:
            await sent.edit_text(final_text)

        # === БОНУСНЫЙ РОЗЫГРЫШ ===
        today = datetime.datetime.now().weekday()  # 4 = пятница
        if today == 4 and random.random() < 0.10:

            await asyncio.sleep(1)

            bonus_msg = await message.answer(
                "⚠️ ВНИМАНИЕ! БОНУСНЫЙ РОЗЫГРЫШ!",
                reply_to_message_id=message.message_id
            )

            await asyncio.sleep(2)

            # повторный прокрут
            current_set = SET_1 if random.random() < 0.5 else SET_2
            keys = list(current_set.keys())

            if random.random() < 0.6:
                sym = random.choice(keys)
                bonus_res = [sym, sym, sym]
            else:
                bonus_res = [random.choice(keys) for _ in range(3)]
                while bonus_res[0] == bonus_res[1] == bonus_res[2]:
                    bonus_res = [random.choice(keys) for _ in range(3)]

            # можно сделать анимацию, но пока просто текст
            await asyncio.sleep(2)

            bonus_win = bonus_res[0] == bonus_res[1] == bonus_res[2]

            if bonus_win:
                bonus_reward = 5_000_000
                update_balance(user_id, bonus_reward)
                bonus_text = f"💥 ДЖЕКПОТ! +{format_money(bonus_reward)}"
            else:
                bonus_text = "😢 Бонус не сыграл"

            new_bal = get_user(user_id, username)

            await message.answer(
                f"🎰 БОНУСНЫЙ СЛОТ\n{' | '.join(bonus_res)}\n{bonus_text}\n💰 Баланс: {format_money(new_bal)}",
                reply_to_message_id=message.message_id
            )

    except Exception as e:
        update_balance(user_id, bet)
        await message.answer(
            "⚠️ Ошибка сервера. Ставка возвращена.",
            reply_to_message_id=message.message_id
        )

def draw_text_pro(draw, position, text, font, fill, stroke_fill="black", stroke_width=2):
    x, y = position

    # обводка
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)

    # основной текст
    draw.text((x, y), text, font=font, fill=fill)

def generate_bonus_gif():
    WIDTH, HEIGHT = 420, 220

    FPS = 7
    SPIN_TIME = 13
    HOLD_TIME = 2

    SPIN_FRAMES = FPS * SPIN_TIME
    HOLD_FRAMES = FPS * HOLD_TIME
    TOTAL_FRAMES = SPIN_FRAMES + HOLD_FRAMES

    CELL_W = 120
    center_x = WIDTH // 2

    # ШРИФТЫ
    font_big = ImageFont.truetype(
    path("fronts", "BebasNeue-Regular.ttf"), 48
    )

    font_mid = ImageFont.truetype(
        path("fronts", "BebasNeue-Regular.ttf"), 28
    )

    # 🎯 выигрыш
    win_bonus = random.choice(BONUSES)

    # длинная лента
    tape = []
    for _ in range(60):
        tape.extend(BONUSES)

    win_index = random.randint(25, 45)
    tape[win_index] = win_bonus

    final_offset = win_index * CELL_W - center_x + CELL_W // 2

    frames = []

    for frame in range(TOTAL_FRAMES):

        # --- ФОН ПУСТЫНИ ---
        img = Image.new("RGB", (WIDTH, HEIGHT), "#e6b566")
        draw = ImageDraw.Draw(img)

        draw.rectangle([0, 0, WIDTH, 90], fill="#f4d29c")
        draw.ellipse([-100, 120, 250, 260], fill="#d89c4a")
        draw.ellipse([150, 130, 500, 280], fill="#c98b3f")

        # --- ДВИЖЕНИЕ ---
        if frame < SPIN_FRAMES:
            t = frame / SPIN_FRAMES
            ease = 1 - (1 - t) ** 3
            current_offset = int(final_offset * ease)
        else:
            current_offset = final_offset

        # --- ЛЕНТА ---
        for i, val in enumerate(tape):
            x = i * CELL_W - current_offset

            if -CELL_W < x < WIDTH:

                if abs(x + CELL_W // 2 - center_x) < 5:
                    color = "#ffcc66"
                else:
                    color = "#b7792b"

                # карточка
                draw.rectangle([x, 80, x + CELL_W, 170], fill=color)

                # свет сверху
                draw.rectangle([x, 80, x + CELL_W, 100], fill="#ffffff22")

                # тень снизу
                draw.rectangle([x, 150, x + CELL_W, 170], fill="#00000033")

                # рамка
                draw.rectangle(
                    [x, 80, x + CELL_W, 170],
                    outline="#5a3b12",
                    width=3
                )

                # --- ТЕКСТ ПО ЦЕНТРУ ---
                text = format_money(val)
                bbox = font_mid.getbbox(text)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]

                tx = x + (CELL_W - tw) // 2
                ty = 115 - th // 2

                draw_text_pro(
                    draw,
                    (tx, ty),
                    text,
                    font_mid,
                    fill="#fff8dc",
                    stroke_fill="#2b1600",
                    stroke_width=2
                )

        # --- ЦЕНТР ЛИНИЯ ---
        draw.line(
            [(center_x, 80), (center_x, 170)],
            fill="#ffdf00",
            width=3
        )

        # --- GLOW (АНИМАЦИЯ) ---
        pulse = abs((frame % 20) - 10)
        for glow in range(4):
            size = glow * 3 + pulse
            draw.ellipse(
                [
                    center_x - 40 - size,
                    100 - size,
                    center_x + 40 + size,
                    140 + size
                ],
                outline="#ffd700"
            )

        # --- PEDRO ---
        text = "🌵PEDRO🌵"
        bbox = font_big.getbbox(text)
        tw = bbox[2] - bbox[0]

        draw_text_pro(
            draw,
            (WIDTH // 2 - tw // 2, 10),
            text,
            font_big,
            fill="#ffcc33",
            stroke_fill="#5a2e00",
            stroke_width=3
        )

        # --- ЭФФЕКТ ЖАРЫ ---
        if frame % 2 == 0:
            img = img.transform(
                img.size,
                Image.AFFINE,
                (1, 0.002, 0, 0.002, 1, 0),
                resample=Image.BICUBIC
            )

        frames.append(img)

    # --- СОХРАНЕНИЕ ---
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    buffer.seek(0)

    return buffer, win_bonus

async def text_slot_animation(message, result, bet):
    msg = await message.reply(f"🎰СЛОТ-МАШИНА🎰\n{result[0]} 🔓 🔒")
    # второй символ (ещё через 4 сек)
    await asyncio.sleep(4)
    await msg.edit_text(f"🎰СЛОТ-МАШИНА🎰\n{result[0]} {result[1]} 🔓")

    # третий символ (ещё через 4 сек)
    await asyncio.sleep(5)
    await msg.edit_text(f"🎰СЛОТ-МАШИНА🎰\n{' | '.join(result)}")
    

    return msg

def get_top_players():
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT username, balance 
        FROM users 
        ORDER BY balance DESC 
        LIMIT 10
    """)

    top = cur.fetchall()
    conn.close()
    return top

async def bonus(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name

    get_user(user_id, username)

    now = int(datetime.datetime.now().timestamp())
    last_bonus = get_last_bonus(user_id)

    # ⛔ Проверка кулдауна
    if now - last_bonus < BONUS_COOLDOWN:
        remaining = BONUS_COOLDOWN - (now - last_bonus)

        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        return await message.answer(
            f"⏳ Бонус будет доступен через {hours}ч {minutes}м"
        )

    try:
        gif, amount = generate_bonus_gif()

        file = BufferedInputFile(gif.read(), filename="bonus.gif")
        msg = await message.answer_animation(file, caption="🎁 Крутим бонус...")

        await asyncio.sleep(10)

        update_balance(user_id, amount)
        update_last_bonus(user_id)

        new_bal = get_user(user_id, username)

        await msg.edit_caption(
            caption=f"🎯 Бонус: {format_money(amount)}\n💰 Баланс: {format_money(new_bal)}"
        )

    except Exception as e:
        await message.answer("⚠️ Ошибка бонуса")

async def transfer_money(from_id, to_id, amount):
    conn = sqlite3.connect("casino.db")
    cur = conn.cursor()

    cur.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, from_id))

    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (to_id,))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)",
            (to_id, "Игрок", amount)
        )
    else:
        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, to_id))

    conn.commit()
    conn.close()
    
@dp.message(F.text.regexp(r"^\+\d+"))
async def transfer_handler(message: types.Message):
    # проверка reply
    if not message.reply_to_message:
        return await message.answer(
            "❌ Ответь на сообщение игрока",
            reply_to_message_id=message.message_id
        )

    amount = int(message.text[1:])
    if amount <= 0:
        return await message.answer("❌ Сумма должна быть больше 0")

    from_id = message.from_user.id
    to_id = message.reply_to_message.from_user.id

    if from_id == to_id:
        return await message.answer("❌ Нельзя перевести самому себе")

    # 🔒 ВАЖНО: правильный порядок lock (чтобы не было deadlock)
    first_id, second_id = sorted([from_id, to_id])

    lock1 = get_user_lock(first_id)
    lock2 = get_user_lock(second_id)

    # если кто-то уже занят
    if lock1.locked() or lock2.locked():
        return await message.answer(
            "⏳ Один из игроков занят, попробуй позже",
            reply_to_message_id=message.message_id
        )

    async with lock1:
        async with lock2:
            # баланс
            from_balance = get_user(from_id, message.from_user.full_name)
            get_user(to_id, message.reply_to_message.from_user.full_name)

            if amount > from_balance:
                return await message.answer(
                    f"❌ Недостаточно средств ({format_money(from_balance)})"
                )

            # перевод
            await transfer_money(from_id, to_id, amount)

            new_balance = get_user(from_id, message.from_user.full_name)

    await message.answer(
        f"💸 Перевод выполнен\n"
        f"👤 Кому: {message.reply_to_message.from_user.full_name}\n"
        f"💰 Сумма: {format_money(amount)}\n"
        f"💳 Баланс: {format_money(new_balance)}",
        reply_to_message_id=message.message_id
    )

@dp.message()
async def router(message: types.Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    user_id = message.from_user.id
    lock = get_user_lock(user_id)

    # если уже выполняется действие — не даём запускать новое
    if lock.locked():
        return
    
    async with lock:
        if re.match(r"(?i)^слот", text):
            await spin(message)

        elif re.match(r"(?i)^(баланс|б|/balance@huila_pedro_bot|/balance)$", text):
            b = get_user(message.from_user.id, message.from_user.full_name) 
            await message.reply(f"💰 Баланс: {format_money(b)}")

        elif text in ["топ", "рейтинг","!топ","/top@huila_pedro_bot","/top"]:
            top = get_top_players()

            if not top:
                return await message.answer("❌ Пока нет игроков")

            text = "🏆 ТОП-10 игроков:\n\n"
            for i, (name, bal) in enumerate(top, 1):
                text += f"{i}. {name} — 💰 {format_money(bal)}\n"

            await message.answer(text, reply_markup=kb)

        elif re.match(r"(?i)^(профиль|/profile|/profile@huila_pedro_bot|👤Профиль💼)$", text):
            username, balance, wins = get_profile(message.from_user.id)
            last_bonus = get_last_bonus(message.from_user.id)
            now = int(datetime.datetime.now().timestamp())
            remaining = BONUS_COOLDOWN - (now - last_bonus)

            if remaining <= 0:
                bonus_text = "🎁 Бонус: доступен"
            else:
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                bonus_text = f"⏳ Бонус через: {hours}ч {minutes}м"

            rank = get_rank(wins)
            img = generate_goose_profile(wins)

            caption = (
                f"👤 {username}\n"
                f"{rank}\n\n"
                f"🏆 Победы: {wins}\n"
                f"💰 Баланс: {format_money(balance)}\n"
                f"{bonus_text}"
            )

            file = BufferedInputFile(img.read(), filename="profile.png")
            await message.answer_photo(file, caption=caption)

        elif text in ["бонус", "/bonus"]:
            await bonus(message)

        elif re.match(r"(?i)^(как играть|инструкция|❗️Как играть❓)$", text):
            await message.answer(
                "🎰 *ПРАВИЛА ИГРЫ* 🎰\n\n"
                "1️⃣ Введите команду `Слот [ставка]` для игры. Ставку можно указать в процентах от баланса (например, `Слот 10%`) или конкретной суммой (например, `Слот 500`).\n"
                "2️⃣ После запуска начнется анимация вращения барабанов. Подождите, пока она закончится.\n"
                "3️⃣ Если на всех трех барабанах выпадут одинаковые символы, вы выиграете в 3 раза больше вашей ставки! Если символы разные — ставка проигрывается.\n"
                "4️⃣ Вы можете проверять свой баланс командой `Баланс` и просматривать свой профиль с достижениями командой `Профиль`.\n"
                "5️⃣ Удачи в игре! 🍀"
            )

        elif re.match(r"(?i)^(новости|📰Новости👮‍♂️)$", text):
            await message.answer(
                "📰@pedro_botlog📰\n\n"
                "💎 Мы добавили систему званий для игроков: от Новобранца до Майора. Чем больше побед — тем выше звание!\n\n"
                "🔥 Не пропустите бонусные розыгрыши по пятницам с шансом выиграть до 5,000,000 монет!"
            )

if __name__ == "__main__":
    init_db()
    asyncio.run(dp.start_polling(bot))
