import discord
import os
import random

from discord.ext import commands
from discord import Embed

from function import json


def enable(bot: discord.ext.commands.Bot):

    # color 중 랜덤으로 색상을 고르고 임베드에 사용 가능한 색상으로 변환한 값을 반환하는 함수
    def random_embed_color() -> discord.Colour:
        color = json.get_data("color.json")
        color_rgb = color[random.choice(list(color))]
        return discord.Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    @bot.command()
    async def 프사(ctx, mention=None):

        embed_color = random_embed_color()

        if mention is not None:
            user_id = mention
            for s in ["<", "@", "!", ">"]:
                user_id = user_id.replace(s, "")
            user_id = int(user_id)
        else:
            user_id = ctx.author.id

        user = bot.get_user(user_id)

        embed = Embed(color=embed_color)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=f"{user}")

        await ctx.send(embed=embed)

        return

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
