import os
import random
import asyncio

import discord_components
import requests

from discord import Embed, Colour
from discord.ext import commands
from discord_components import Button, Select, SelectOption

from function import json


def enable(bot: commands.Bot):
    # color 중 랜덤으로 색상을 고르고 임베드에 사용 가능한 색상으로 변환한 값을 반환하는 함수
    def random_embed_color() -> Colour:
        color = json.get_data("color.json")
        color_rgb = color[random.choice(list(color))]
        return Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    def get_embed_color(color_name: str) -> Colour:
        color_list = json.get_data("color.json")
        color_rgb = color_list[color_name]
        return Colour.from_rgb(
            r=color_rgb[0],
            g=color_rgb[1],
            b=color_rgb[2]
        )

    ask_embed_color = random_embed_color()
    ask_embed = Embed(description="✨ 어떤 액티비티를 활성할까요?", colour=ask_embed_color)

    def error_embed(desc: str):
        embed_color = get_embed_color("Light_Red")
        return Embed(description=f"⛔ {desc}", colour=embed_color)

    def success_embed(desc: str):
        embed_color = get_embed_color("Light_Blue")
        return Embed(description=f"✅  {desc}", colour=embed_color)

    def get_activity_link(ctx, activity_name):
        # activity = json.get_data("activity_app.json")[activity_name]
        token = json.get_data("setting.json")["Bot"]["Token"]
        activities = json.get_data("activity_app.json")

        response = requests.post(f"https://discord.com/api/v8/channels/{ctx.author.voice.channel.id}/invites",
                                 json={
                                     "max_age": 86400,
                                     "max_uses": 0,
                                     "validate": None,
                                     "temporary": False,
                                     "target_application_id": activities[activity_name],
                                     "target_type": 2
                                 },
                                 headers={
                                     "Authorization": f"Bot {token}",
                                     "Content-Type": "application/json"
                                 }
                                 )
        data = response.json()
        print(data)
        party_link = "https://discord.gg/" + data["code"]

        return party_link

    @bot.command()
    async def 액티비티(ctx):
        channel = ctx.author.voice
        if channel is None:
            await ctx.reply(embed=error_embed("먼저 음성 채널에 입장해주세요"), delete_after=5)
            return

        message = await ctx.reply(
            embed=ask_embed,
            components=[
                Select(
                    placeholder="여기를 눌러 액티비티 선택",
                    options=[
                        SelectOption(label="Youtube", value="Youtube"),
                        SelectOption(label="Fishing", value="Fishing"),
                        SelectOption(label="Letter League", value="Letter League"),
                        SelectOption(label="Word Snack", value="Word Snack"),
                        SelectOption(label="SpellCast", value="SpellCast"),
                        SelectOption(label="짭몽어스", value="짭몽어스"),
                        SelectOption(label="Draw it!", value="Draw it"),
                        SelectOption(label="Chess", value="Chess"),
                        SelectOption(label="Checker", value="Checker")
                    ]
                )
            ]
        )

        try:
            interaction = await bot.wait_for("select_option", timeout=15.0)
            activity_link = get_activity_link(ctx, interaction.values[0])
            await interaction.message.delete()
            print(activity_link)
            await interaction.channel.send(
                embed=success_embed(f"{ctx.author.voice.channel.mention}에서 {interaction.values[0]} 액티비티를 활성화할게요!"),
                components=[
                    Button(label=f"{interaction.values[0]} 참가하기",
                           style=discord_components.ButtonStyle.URL,
                           url=activity_link
                           )
                ]
            )
        except asyncio.TimeoutError:
            await message.edit(embed=error_embed("선택 시간이 초과됐어요"), delete_after=5, components=[])

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
