from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5888375175:AAF1T-7xe32IipbD8e-K_m0VOvLnJJ0f2BA'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class tg_players:
   def __init__(self, spisok):
      self.spisok = spisok


players = []
chats = []
h = 0


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Супер, теперь я тебя знаю)")
    global players
    chat_id = message.from_user.id
    user_name = message.from_user.username
    pl = [user_name, chat_id]
    # if pl not in players:
    players.append(pl)
    print("Инфа сохранена:", players)


def get_chats_info():
    return players


# photo = InputFile("files/test.png")
# await bot.send_photo(chat_id=player.id, photo=photo)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
