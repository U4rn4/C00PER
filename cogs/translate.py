import discord 
from discord.ext import commands
import deepl
from apikeys import *

# To use this cog you must have the DEEPLKEY written in the apikeys module

class translate(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="translate", help="example: .translate target_language content")
    async def translate(self, ctx, lang, *, cont):
        try:
            async with ctx.typing():
                translator = deepl.Translator(DEEPLKEY)
                
                match lang:
                    case "german":
                        lang = "DE"
                    case "english":
                        lang = "EN-US"
                    case "spanish":
                        lang = "ES"
                    case "french":
                        lang = "FR"
                    case "italian":
                        lang = "IT"
                    case "dutch":
                        lang = "NL"
                    case "polish":
                        lang = "PL"
                    case "portuguese":
                        lang = "PT"
                    case "russian":
                        lang = "RU"
                    case "japanese":
                        lang = "JA"
                    case "arabic":
                        lang = "AR"
                    case "bulgarian":
                        lang = "BG"
                    case "czech":
                        lang = "CS"
                    case "danish":
                        lang = "DA"
                    case "greek":
                        lang = "EL"
                    case "estonian":
                        lang = "ET"
                    case "finnish":
                        lang = "FI"
                    case "hungarian":
                        lang = "HU"
                    case "lithuanian":
                        lang = "LT"
                    case "latvian":
                        lang = "LV"
                    case "norwegian":
                        lang = "NB"
                    case "dutch":
                        lang = "NL"
                    case "romanian":
                        lang = "RO"
                    case "slovak":
                        lang = "SK"
                    case "slovenian":
                        lang = "SL"
                    case "swedish":
                        lang = "SV"
                    case "turkish":
                        lang = "TR"
                    case "ukrainian":
                        lang = "UK"
                    case "chinese":
                        lang = "ZH"
                    case "korean":
                        lang = "KO"
                    case _:
                        pass

                result = translator.translate_text(cont, target_lang=lang)
                await ctx.reply(result)
        except:
            ctx.reply("The language you entered is not supported or the text is too long")

async def setup(bot):
    await bot.add_cog(translate(bot))
