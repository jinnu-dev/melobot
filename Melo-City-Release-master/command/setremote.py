import discord
import os

from discord.ext import commands
from discord import Embed

from function import json


def enable(bot: discord.ext.commands.Bot):

    # color 중 color_name의 색을 임베드에 사용 가능한 변수로 반환
    def get_embed_color(color_name: str) -> discord.Colour:
        color_list = json.get_data("color.json")
        color_rgb = color_list[color_name]
        return discord.Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    @bot.command()
    async def setremote(ctx):
        remote_channel = bot.get_channel(939531297683017788)
        embed_color = get_embed_color("Light_Yellow")

        embed = Embed(title="VoiceChannel 대시보드",
                      description="이 곳에서 음성채널을 관리할 수 었어요",
                      color=embed_color)
        embed.set_image(url="https://cdn.discordapp.com/attachments/939797813250883594/939804741226090496/15e81451c9648c5f36abbe630518b24d.gif")
        embed.add_field(name="⬆", value="인원 제한 +1", inline=True)
        embed.add_field(name="⬇", value="인원 제한 -1", inline=True)
        embed.add_field(name="🆓", value="인원 제한 제거", inline=True)
        embed.add_field(name="2️⃣ 3️⃣ 4️⃣ 5️⃣", value="빠른 인원 제한 (2~5명)", inline=True)
        embed.add_field(name="🔒", value="성인 제한 On / Off", inline=True)

        remote_message = await remote_channel.send(embed=embed)
        remote_reactions = [
            "⬆",  # 인원 제한 한 명 업
            "⬇",  # 인원 제한 한 명 다운
            "🆓",  # 빠르게 인원 제한 제거
            "2️⃣", "3️⃣", "4️⃣", "5️⃣",  # 빠르게 인원 제한 (2~5)
            "🔒"  # 성인 제한 On / Off
        ]

        for reaction in remote_reactions:
            await remote_message.add_reaction(reaction)

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
