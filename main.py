import discord
from discord.ext import commands

# Inicializa los intents
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes

# Inicializa el bot con el prefijo '!' y los intents
bot = commands.Bot(command_prefix='.', intents=intents)

# Archivo donde se almacenará el valor del contador
COUNTER_FILE = 'counter.txt'

# Función para leer el contador del archivo
def read_counter():
    try:
        with open(COUNTER_FILE, 'r') as file:
            return int(file.read())
    except FileNotFoundError: 
        return 0

# Función para escribir el contador en el archivo
def write_counter(counter):
    with open(COUNTER_FILE, 'w') as file:
        file.write(str(counter))

# Comando para incrementar el contador
@bot.command()
async def increment(ctx):
    counter = read_counter() + 1
    write_counter(counter)
    await ctx.send(counter)
@bot.command()
async def decr(ctx):
    counter = read_counter() - 1
    write_counter(counter)
    await ctx.send(counter)

# Evento que indica que el bot está listo
@bot.event
async def on_ready():
    print(f'Bot listo. Conectado como {bot.user}')

# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot
# bot.run()
