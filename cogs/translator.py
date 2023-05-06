import discord
import json 
import deepl
import os

from discord.commands import SlashCommandGroup
from discord.ext import commands
from deep_translator import GoogleTranslator

JSON_PATH = "./Translate_Language.json"

users = os.getenv('Authorized_Users').split(',')
authorized_users = [int(value) for value in users]
deepl.api_key = str(os.environ.get("DeepL_API"))
TL_Language = {}

try:
    with open(JSON_PATH, "r") as f:
        selected_lang = json.load(f)
except FileNotFoundError:
    selected_lang = {"default": {"language": "JA", "translator": "DeepL"}}
    with open(JSON_PATH, "w") as f:
        json.dump(selected_lang, f)


class LanguageDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        lang = selected_lang.get(user_id, {}).get(
            "language"
        )  # get user's selected language
        options = [
            discord.SelectOption(
                label="Japanese",
                description="Japanese Language",
                emoji="🇯🇵",
                value="JA",
                default=lang == "JA",
            ),
            discord.SelectOption(
                label="Korean",
                description="Korean Language",
                emoji="🇰🇷",
                value="KO",
                default=lang == "KO",
            ),
            discord.SelectOption(
                label="English",
                description="English Language",
                emoji="🇺🇸",
                value="EN",
                default=lang == "EN",
            ),
            discord.SelectOption(
                label="Chinese (Simplified)",
                description="Chinese Language",
                emoji="🇨🇳",
                value="zh-CN",
                default=lang == "zh-CN",
            ),
            discord.SelectOption(
                label="Chinese (Traditional)",
                description="Chinese(Traditional) Language",
                emoji="🇨🇳",
                value="zh-TW",
                default=lang == "zh-TW",
            ),
        ]
        super().__init__(placeholder="Select language to translate...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_lang:
            selected_lang[user_id] = {"language": "JA", "translator": "DeepL"}
        if isinstance(selected_lang[user_id], dict):
            selected_lang[user_id]["language"] = self.values[0]
            with open(JSON_PATH, "w") as f:
                json.dump(selected_lang, f)
            selected_option = next(
                option for option in self.options if option.value == self.values[0]
            )
            await interaction.response.send_message(
                f"Selected language: {selected_option.label} {selected_option.emoji}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your selected language and translator.",
                ephemeral=True,
            )


class TranslatorDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(JSON_PATH, "r") as f:
            selected_trans = json.load(f)
        trans = selected_trans.get(user_id, {}).get("translator")
        options = [
            discord.SelectOption(
                label="DeepL",
                description="Translate using DeepL",
                emoji="<:DeepL:1092335121081839647> ",
                value="DeepL",
                default=trans == "DeepL",
            ),
            discord.SelectOption(
                label="Google Translate",
                description="Translate using Google Translate",
                emoji="<:Google_Translate:1092335419636584480> ",
                value="Google Translate",
                default=trans == "Google Translate",
            ),
        ]
        super().__init__(placeholder="Select translator...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_lang:
            selected_lang[user_id] = {"language": "JA", "translator": "DeepL"}
        if isinstance(selected_lang[user_id], dict):
            selected_lang[user_id]["translator"] = self.values[0]
            with open(JSON_PATH, "w") as f:
                json.dump(selected_lang, f)
            selected_options = [
                option for option in self.options if option.value in self.values
            ]
            selected_labels = [option.label for option in selected_options]
            selected_emojis = [str(option.emoji) for option in selected_options]
            await interaction.response.send_message(
                f"Selected translator: {', '.join(selected_labels)} {' '.join(selected_emojis)}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your selected language and translator.",
                ephemeral=True,
            )


class DropdownView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__()
        self.add_item(TranslatorDropdown(user_id=user_id))
        self.add_item(LanguageDropdown(user_id=user_id))

class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    translator = SlashCommandGroup("translator", "Various help commands for Gura!")
    
    @translator.command(name="settings", description="Translator Settings")
    async def tlsettings(self, ctx: discord.ApplicationContext):
        """Sends a message with our dropdowns that contain language and translator options."""
        view = DropdownView(str(ctx.author.id))
        embed = discord.Embed(
            title="Translation Options",
            description="Select a language and translator to use for translation:",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Translator:", value="DeepL", inline=False)
        embed.add_field(
            name="Languages:",
            value="Japanese,English,Chinese(Simplified),Chinese(Traditional)",
            inline=False,
        )
        await ctx.respond(embed=embed, view=view, ephemeral=True)


    async def translate_text(self,text: str, target_lang: str, translator: str) -> str:
        if translator == "DeepL":
            auth_key = os.environ.get("DeepL_API")
            if target_lang in ("zh-TW", "zh-CN"):
                target_lang = "ZH"
                result = deepl.Translator(auth_key).translate_text(
                    text, target_lang=target_lang
                )
            elif target_lang == "EN":
                target_lang = "EN-US"
                result = deepl.Translator(auth_key).translate_text(
                    text, target_lang=target_lang
                )
            else:
                result = deepl.Translator(auth_key).translate_text(
                    text, target_lang=target_lang
                )
            return result.text
        if translator == "Google Translate":
            if target_lang == "zh-TW":
                target_lang = "zh-TW"
                result = GoogleTranslator(source="auto", target=target_lang).translate(
                    text=text
                )
            elif target_lang == "zh-CN":
                target_lang = "zh-CN"
                result = GoogleTranslator(source="auto", target=target_lang).translate(
                    text=text
                )
            else:
                result = GoogleTranslator(
                    source="auto", target=target_lang.lower()
                ).translate(text=text)
            return result
        return f"Invalid translator selected: {translator}"


    @commands.slash_command(name="translate", description="Gura helps you to translate messages")
    async def translate(self, ctx: discord.ApplicationContext, message: str):
        """Translates a message to the selected language using the selected translator."""
        # Retrieve the user's selected language and translator from the JSON file using their user id as the key
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        user_language = selected_lang.get(str(ctx.author.id), selected_lang["default"])[
            "language"
        ]
        user_translator = selected_lang.get(str(ctx.author.id), selected_lang["default"])[
            "translator"
        ]
        # Check if the user is authorized to use DeepL
        if user_translator == "DeepL" and ctx.author.id not in authorized_users:
            embed = discord.Embed(title="**Translation**", color=discord.Color.red())
            embed.add_field(name="Error", value="You are not authorized to use DeepL due to API limitations.")
            await ctx.respond(embed=embed)
            return
        # Translate the message to the user's selected language using the selected translator
        translated_text = await self.translate_text(message, user_language, user_translator)

        # Create an embed with the input text and the translated text
        embed = discord.Embed(title="**Translation**", color=discord.Color.nitro_pink())
        embed.add_field(name="**Input Text**", value=f"`{message}\n`", inline=False)
        embed.add_field(
            name="**Translated Text**", value=f"`{translated_text}\n`", inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.interaction.user.name}",
            icon_url=ctx.interaction.user.display_avatar.url,
        )
        # Send the embed as a response to the slash command
        await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Translator(bot))