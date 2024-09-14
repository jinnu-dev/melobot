# 경고 관련 명령어

import discord
import os
import random

from discord.ext import commands
from discord import Embed
from function import json

from plugin import database


def enable(bot: commands.Bot):

    # color 중 랜덤으로 색상을 고르고 임베드에 사용 가능한 색상으로 변환한 값을 반환하는 함수
    def random_embed_color() -> discord.Colour:
        color = json.get_data("color.json")
        color_rgb = color[random.choice(list(color))]
        return discord.Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    def get_embed_color(color_name: str) -> discord.Colour:
        color_list = json.get_data("color.json")
        color_rgb = color_list[color_name]
        return discord.Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    @bot.command()
    async def 경고(ctx: discord.ext.commands.Context, mention, value: int, *, reason: str = "사유 없음"):

        def is_message_manager() -> bool:
            return ctx.author.guild_permissions.manage_messages

        if not is_message_manager():
            return

        user_id = mention

        for s in ["<", "@", "!", ">", " "]:
            user_id = user_id.replace(s, "")

        user = bot.get_user(int(user_id))
        warning_log = bot.get_channel(json.get_data("setting.json")["Server"]["Channel"]["Log"]["Warning"])

        warn = database.warning(user)
        warn.add(value, reason)
        print(f"{user.display_name} >> 경고 지급됨")

        embed_color = get_embed_color("Light_Red")
        total_value = warn.get_value()

        embed = Embed(title="⚠ 경고 안내", description=f"경고 대상자 : {mention}", color=embed_color)
        embed.add_field(name="🅿️ 누적 경고", value=f"({value}) {total_value // 5}회 {total_value % 5}점", inline=True)
        embed.add_field(name="📝 경고 사유", value=reason, inline=True)

        await ctx.send(embed=embed)
        await warning_log.send(embed=embed)

        return 0

    @bot.command()
    async def 경고내역(ctx, mention=None):

        embed_color = random_embed_color()

        if mention is not None:
            user_id = mention
            for s in ["@", "<", ">", "!"]:
                user_id = user_id.replace(s, "")
        else:
            user_id = ctx.author.id

        user = bot.get_user(int(user_id))
        warning = database.warning(user)
        value = warning.get_value()
        last_reason = warning.get_last_reason()

        embed = Embed(title=f"💬 {user}님의 경고 내역",
                      description="더 자세한 경고 사유/기록은 't.경고전체내역'을 사용해주세요", color=embed_color)
        embed.add_field(name="🅿️ 누적 경고", value=f"{value // 5}회 {value % 5}점", inline=True)
        embed.add_field(name="📝 최근 경고 사유", value=last_reason, inline=True)

        await ctx.send(embed=embed)

        return

    @bot.command()
    async def 경고전체내역(ctx, mention=None):

        embed_color = random_embed_color()

        if mention is not None:
            user_id = mention
            for s in ["@", "<", ">", "!"]:
                user_id = user_id.replace(s, "")
        else:
            user_id = ctx.author.id

        user = bot.get_user(int(user_id))
        warning = database.warning(user)
        reasons = "\n".join(warning.get_all_reason())

        embed = Embed(title=f"💬 {user}님의 경고 내역", color=embed_color)

        await ctx.send(embed=embed)
        await ctx.send(f"```(지급된 포인트) 지급 전 포인트 -> 지급 후 포인트 : 사유\n{reasons}```")

        return

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
