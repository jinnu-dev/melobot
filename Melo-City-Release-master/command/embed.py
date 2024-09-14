import os
import asyncio
import pytz
import datetime

import discord
from discord import Embed
from discord.ext import commands

from function import json


def enable(bot: commands.Bot):

    setting = json.get_data("setting.json")

    def is_message_manager(ctx) -> bool:
        return ctx.author.guild_permissions.manage_messages

    @bot.command()
    async def 임베드생성(ctx):
        if not is_message_manager(ctx):
            return

        current_author = ctx.author

        def check(m):
            return current_author == m.author

        embed_spawner = await ctx.send("임베드 생성을 위해 준비중이에요")

        async def set_embed_color():
            await embed_spawner.edit(
                "생성할 임베드의 색상코드(`#ffffff 형태`)를 입력해주세요. 만일 색상코드가 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                sixteenIntegerHex = int(message.content.replace("#", ""), 16)
                color = int(hex(sixteenIntegerHex), 0)
                embed = Embed(colour=color)
                return embed
            return Embed(colour=0x74b9ff)

        async def set_embed_title():
            await embed_spawner.edit(
                "생성할 임베드의 제목을 입력해주세요. 만일 제목이 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                embed.title = message.content

        async def set_embed_desc():
            await embed_spawner.edit(
                "생성할 임베드의 내용을 입력해주세요. 만일 내용이 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                embed.description = message.content

        async def set_embed_author():
            await embed_spawner.edit(
                "생성할 임베드의 머릿말을 입력해주세요. 만일 머릿말이 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                author = message.content
                await embed_spawner.edit(
                    "생성할 임베드의 머릿말 아이콘으로 사용될 이미지 링크(`https://...`)를 입력해주세요. 만일 아이콘이 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
                message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
                if message.content != "None":
                    icon_url = message.content
                    embed.set_author(name=author, icon_url=icon_url)
                else:
                    embed.set_author(name=author)

        async def set_embed_thumbnail():
            await embed_spawner.edit(
                "생성할 임베드의 썸네일(오른쪽 위 이미지) 이미지 링크를 입력해주세요. 만일 썸네일이 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                embed.set_thumbnail(url=message.content)

        async def set_embed_image():
            await embed_spawner.edit(
                "생성할 임베드의 이미지(배너사진) 링크를 입력해주세요. 만일 이미지가 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                embed.set_image(url=message.content)

        async def add_embed_field():
            desc = ""
            inline = True

            await embed_spawner.edit(
                "생성할 임베드에 추가할 필드 제목을 입력해주세요. 만일 필드가 없다면 `None`을 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                name = message.content
                await embed_spawner.edit(
                    "생성할 임베드에 추가된 필드 내용을 입력해주세요. 필수적으로 입력해주세요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
                message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
                if message.content != "None":
                    desc = message.content
                    await embed_spawner.edit(
                        "생성할 임베드에 추가된 필드 인라인 여부을 입력해주세요. (o / x) 대문자 및 o/x외의 문자를 입력하면 o로 설정돼요\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
                    message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
                    if message.content != "o":
                        inline = True
                    else:
                        inline = False
                embed.add_field(name=name, value=desc, inline=inline)
                await add_embed_field()
            else:
                return

        async def set_embed_footer():
            await embed_spawner.edit(
                "생성할 임베드의 꼬릿말을 입력해주세요. 만일 꼬릿말이 없다면 `None`을 입력해주세요\n꼬릿말에 동적 변수을 사용할 수 있어요\n``{맴버수}, {길드이름}, {연도}, {날짜}, {시간}`\n(8분 동안 입력이 없을 경우 현재 임베드 생성이 취소돼요)")
            message = await bot.wait_for('message', check=check, timeout=480)  # discord.message.Message
            if message.content != "None":
                embed.set_footer(text=message.content)

        try:
            embed = Embed(colour=0x74b9ff)
            embed = await set_embed_color()
            await set_embed_title()
            await set_embed_desc()
            await set_embed_author()
            await set_embed_thumbnail()
            await set_embed_image()
            await add_embed_field()
            await set_embed_footer()

        except asyncio.TimeoutError:
            await ctx.send("8분간 입력이 감지되지 않아 임베드 생성이 취소되었어요")
            return

        message = await ctx.send("성공적으로 임베드를 만들었어요! (임베드 ID = Loading...)")
        await ctx.send(embed=embed)

        embed_collection_channel = bot.get_channel(setting["Server"]["Channel"]["Embed_Collection"])

        summoned_embed = await embed_collection_channel.send(embed=embed)
        await message.edit(
            f"성공적으로 임베드를 만들었어요! (ID = {summoned_embed.id})\n`{bot.command_prefix}임베드전송 <채널> <임베드 ID>`를 입력하여 언제든지 임베드를 채널에 전송할 수 있어요")
        return

    @bot.command()
    async def 임베드전송(ctx, channel: discord.TextChannel, message_id):
        if not is_message_manager(ctx):
            return

        embed_collection_channel = bot.get_channel(setting["Server"]["Channel"]["Embed_Collection"])

        try:
            target_message = await embed_collection_channel.get_partial_message(message_id).fetch()
        except:
            await ctx.send("해당 ID를 가진 임베드를 찾지 못했어요", delete_after=10)
            return

        embed = target_message.embeds[0]

        all_date = datetime.datetime.now(pytz.timezone("Asia/Seoul"))

        if all_date.hour > 12:
            time = f"오전 {all_date.hour-12}시 {all_date.minute}분"
        else:
            time = f"오후 {all_date.hour}시 {all_date.minute}분"

        year = f"{all_date.year}년"
        date = f"{all_date.month}월 {all_date.day}일"

        footer = str(embed.footer)[17:][:-2]
        footer = footer.replace("{맴버수}", str(ctx.guild.member_count))
        footer = footer.replace("{길드이름}", str(ctx.guild.name))
        footer = footer.replace("{연도}", year)
        footer = footer.replace("{날짜}", date)
        footer = footer.replace("{시간}", time)
        embed.set_footer(text=footer)

        await channel.send(embed=embed)
        await ctx.send(f"성공적으로 임베드를 {channel.mention}에 전송했어요", embed=embed)

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
