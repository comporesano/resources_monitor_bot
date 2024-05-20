from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from settings import TOKEN
import psutil
import requests



class MonitorBot(Bot):
    
    def __init__(self, TOKEN) -> None:
        super().__init__(token=TOKEN) 
        
        self.emit_keyboard()
        
    def emit_keyboard(self) -> None:
        cpu_button = InlineKeyboardButton(text='CPU', callback_data='cpu_check')
        ram_button = InlineKeyboardButton(text='RAM', callback_data='ram_check')
        hd_button = InlineKeyboardButton(text='Hard Disk', callback_data='hd_check')
        net_button = InlineKeyboardButton(text='Connection', callback_data='net_check')
        summary_button = InlineKeyboardButton(text='Summary', callback_data='sum_check')
        
        help_command = KeyboardButton('/help')
        get_menu_command = KeyboardButton('/get_menu')
        
        self.reply_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(help_command,
                                                                          get_menu_command)
        self.inline_markup = InlineKeyboardMarkup().add(cpu_button,
                                                ram_button,
                                                hd_button,
                                                net_button,
                                                summary_button)

        
m_bot = MonitorBot(TOKEN=TOKEN)
dp = Dispatcher(m_bot)

@dp.message_handler(commands=['start'])
async def hello_world_message(message: types.Message) -> None:
    await message.reply('Hello!', reply_markup=m_bot.reply_markup)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message) -> None:
    await message.reply('Monitoring Ubuntu server resources bot!\nWrite /get_menu for start utility!')
        
@dp.message_handler(commands=['get_menu'])     
async def get_menu_command(message: types.Message) -> None:
    await message.reply('Choose option:', reply_markup=m_bot.inline_markup)

@dp.callback_query_handler(text=['cpu_check', 'ram_check', 'hd_check', 'net_check', 'sum_check'])
async def handle_button(call: types.CallbackQuery):
    cpu_use = psutil.cpu_percent()
    ram_use = psutil.virtual_memory().percent
    hd_use = psutil.disk_usage('/')
    connection = True
    
    if call.data == 'cpu_check':
        # CPU monitor
        if cpu_use > 95:
            await call.message.answer(f'Critical CPU usage: {cpu_use}%')
        else:
            await call.message.answer(f'CPU usage: {cpu_use}%')
            
    if call.data == 'ram_check':
        # RAM monitor
        if ram_use > 95:
            await call.message.answer(f'Critical RAM usage: {ram_use}%')
        else:
            await call.message.answer(f'RAM usage: {ram_use}%')
    
    if call.data == 'hd_check':
        # HD monitor
        if hd_use.percent > 95:
            await call.message.answer(f'Critical Hard Disk usage: {hd_use.percent}%')
        else:
            await call.message.answer(f'Hard disk usage: {hd_use.percent}%')
    
    if call.data == 'net_check':
        # Check connection
        try:
            requests.head('http://www.google.com/', timeout=1)
            await call.message.answer(f'Server online!')
        except requests.ConnectionError:
            connection = False
            await call.message.answer(f'No connection')
    
    if call.data == 'sum_check':
        # Send statistics
        await call.message.answer(f'* CPU usage: {cpu_use}%\n* RAM usage: {ram_use}%\n* HD usage: {hd_use.percent}%\n* Connection: {connection}')
    
    await call.answer()
    
def main():
    executor.start_polling(dp)   
    
if __name__ == '__main__':
    main()