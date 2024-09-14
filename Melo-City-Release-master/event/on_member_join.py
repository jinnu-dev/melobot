# 유저가 길드에 들어왔을 때 이벤트

import asyncio
import discord
import random
import os

from discord.ext import commands
from function import json


def enable(bot: discord.ext.commands.Bot):

    @bot.event
    async def on_member_join(member: discord.member.Member):

        # color 중 랜덤으로 색상을 고르고 임베드에 사용 가능한 색상으로 변환한 값을 반환하는 함수
        def random_embed_color() -> discord.Colour:
            color = json.get_data("color.json")
            color_rgb = color[random.choice(list(color))]
            return discord.Colour.from_rgb(
                r=color_rgb[0],
                g=color_rgb[1],
                b=color_rgb[2]
            )

        async def give_roles_to_member(roles: list) -> None:
            print(f"[{os.path.basename(__file__)}] {member}에게 기본 역할이 지급되었습니다.")
            for currentRole in roles:
                await member.add_roles(member.guild.get_role(currentRole))
                await asyncio.sleep(0.3)
            return

        mention = member.mention
        avatar = member.avatar_url
        member_count = member.guild.member_count

        embed_color = random_embed_color()

        message_text = f":revolving_hearts: Enjoy with us! {mention}"

        embed_decs = " \n".join([
            ":heart: Announce : <#934724966669238273>",
            ":green_heart: Rule : <#785715135435898900>",
            ":blue_heart: Notice : <#939856339184783421>",
            ":orange_heart: Chat (Korea) : <#728809695753666644>",
            ":yellow_heart: Chat (Global) : <#796951640832868392>\n\n"
            ":white_check_mark: For more :point_right: <#796312409517457438>"
        ])

        message_footer = f"🎁 Boost our Server! {member_count}th resident"

        embed = discord.Embed(description=embed_decs, color=embed_color)
        embed.set_author(name="👋 Welcome to 🎶✨ㆍMelo City!ㆍ✨🎶", icon_url=avatar)
        embed.set_footer(text=message_footer)

        setting = json.get_data("setting.json")

        welcome_channel = bot.get_channel(
            setting["Server"]["Channel"]["Welcome"]
        )

        await welcome_channel.send(
            content=message_text,
            embed=embed
        )

        will_give_role = [
            810763466088513576,  # Bio
            810765447275347968,  # Ping
            810765633310425129,  # Special
            975649748998553600,  # 인증 전
        ]

        await give_roles_to_member(will_give_role)

        return 0

    print(f"[{os.path.basename(__file__)}] 활성화됨")
