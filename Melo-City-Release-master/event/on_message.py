import discord
import os

from discord import Embed
from discord.ext.commands import Bot
from function import json

from plugin import chatting
from plugin import database


def enable(bot: Bot):

    setting = json.get_data("setting.json")

    def get_embed_color(color_name: str) -> discord.Colour:
        color_list = json.get_data("color.json")
        color_rgb = color_list[color_name]
        return discord.Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    async def get_message_history(message: discord.Message, limit: int):
        return await message.channel.history(limit=limit).flatten()

    @bot.event
    async def on_message(message: discord.Message):

        def is_bot() -> bool:
            return message.author.bot or message.is_system()

        def is_command() -> bool:
            return message.content.startswith("t.")

        def is_message_manager() -> bool:
            return message.author.guild_permissions.manage_messages

        if is_bot():
            return

        if is_command():
            await bot.process_commands(message)
            return 0

        detect_channel = [
            936234304692957224,  # 쉼터
            728809695753666644,  # kr
            796951640832868392,  # global
            939529587560435722,  # 음챗 채팅
            810724608541851689   # 개발
        ]

        badword = chatting.badword(message.content)
        if badword.used:
            if message.channel.id not in detect_channel:
                return
            if is_message_manager():
                return
            await message.delete()

            warning = database.warning(message.author)
            warning.add(1, "[Auto] 욕설 사용")

            warn_value = warning.get_value()

            warning_log_channel = bot.get_channel(setting["Server"]["Channel"]["Log"]["Warning"])

            embed_color = get_embed_color("Light_Red")

            # 경고 로그, DM, 채널용 경고 임베드
            embed = Embed(title="⚠ 경고 안내", description=f"경고 대상자 : {message.author.mention}", color=embed_color)
            embed.add_field(name="🅿️ 누적 경고", value=f"(1) {warn_value // 5}회 {warn_value % 5}점", inline=True)
            embed.add_field(name="📝 경고 사유", value="[Auto] 욕설 사용", inline=True)
            embed.add_field(name="⚠ 감지된 욕설", value=f"[{badword.detect_type}] {badword.detect_word}", inline=True)
            embed.add_field(name="💬 메시지", value=message.content, inline=True)
            await message.channel.send(embed=embed, delete_after=5)  # 채널에 경고 메시지 전송
            await warning_log_channel.send(embed=embed)  # 로그 채널에 경고 메시지 전송
            await message.author.send(embed=embed)  # dm 전송

            msg_history = await get_message_history(message, 10)
            previous_msgs = []
            for msg in msg_history:
                previous_msgs.append(f"{msg.author.display_name} ({msg.author}) : {msg.content}")
            previous_msgs.append(f"{message.author.display_name} ({message.author}) : {message.content}")
            previous_msgs = "\n".join(previous_msgs)

            # 욕설 채널 로그용 임베드
            embed = Embed(description=f"채널 : {message.channel.mention}", color=embed_color)
            embed.set_author(name=f"{message.author.nick}({message.author})이/가 욕설 사용",
                             icon_url=message.author.avatar_url)
            embed.add_field(name="⚠ 감지된 욕설", value=f"[{badword.detect_type}] {badword.detect_word}", inline=True)
            embed.add_field(name="💬 메시지", value=message.content, inline=True)
            badword_log_channel = bot.get_channel(setting["Server"]["Channel"]["Log"]["Badword"])
            await badword_log_channel.send(embed=embed)
            await badword_log_channel.send(
                f"욕설이 사용되기 전 상황 메시지들```{previous_msgs}```\n해당 메시지로 이동하기 : [{msg_history[0].jump_url}]")

            return

        message_without_emoji = message.content

        for emoji in message.guild.emojis:  # 이모티콘을 한글자로 변경
            message_without_emoji = message_without_emoji.replace(f"{str(emoji)}", ":emoji:")

        longer = chatting.long_sentence(message_without_emoji)
        if longer.longer:
            if message.channel.id not in detect_channel:
                return
            if is_message_manager():
                return
            await message.delete()

            embed_color = get_embed_color("Yellow")

            # 채널용 임베드
            embed = Embed(description=f"채널 : {message.channel.mention}", color=embed_color)
            embed.set_author(name=f"채팅이 너무 길어요!", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=5)

            # 로그용 임베드
            embed = Embed(description=f"채널 : {message.channel.mention}", color=embed_color)
            embed.set_author(name=f"{message.author}({message.author.nick})이/가 도배성 채팅 전송",
                             icon_url=message.author.avatar_url)
            embed.add_field(name="💬 메시지", value=message.content, inline=True)
            longer_log_channel = bot.get_channel(setting["Server"]["Channel"]["Log"]["Long"])
            await longer_log_channel.send(embed=embed)

            return

    print(f"[{os.path.basename(__file__)}] 활성화됨")
