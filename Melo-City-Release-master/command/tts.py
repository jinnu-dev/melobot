import discord
import requests
import os
import asyncio

from discord.ext import commands
from function import json


def enable(bot: commands.Bot):

    setting = json.get_data("setting.json")
    tts_server = setting["TTS"]["Server"]
    rest_key = setting["TTS"]["REST_KEY"]

    headers = {
        "Content-Type": "application/xml",
        "Authorization": f"KakaoAK {rest_key}"
    }

    voices = {
        "지민": "WOMAN_READ_CALM",
        "아리": "WOMAN_DIALOG_BRIGHT",
        "성민": "MAN_READ_CALM",
        "민수": "MAN_DIALOG_BRIGHT"
    }

    def add_break(message: str) -> str:
        for break_time_word in [".", "!", "?", "\n", "(", ")"]:
            message.replace(break_time_word, f'{break_time_word}<break time="100ms"/>')
        return message

    def make_tts_file(message: str, voice: str, file_name: str):
        print(f"[{os.path.basename(__file__)}] {voice} TTS 요청 : {message}")

        voice = voices[voice]
        text = add_break(message)
        text_data = f'<speak> <audio soundLevel="5dB" speed="110%"/> <voice name="{voice}"> {text} </voice> </speak>'.encode('utf-8').decode('latin1')

        res = requests.post(tts_server, headers=headers, data=text_data)
        file_name = f"{file_name}.mp3"
        with open(file_name, 'wb') as f:
            f.write(res.content)

        print(f"[{os.path.basename(__file__)}] 요청 결과 : {res}")

    async def join_channel(ctx):
        voice_channel = ctx.author.voice.channel
        try:
            voice_client = await voice_channel.move_to()
        except:
            try:
                voice_client = await voice_channel.connect()
            except:
                voice_client = ctx.guild.voice_client

        return voice_client

    async def leave_channel(ctx):
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()

    @bot.command()
    async def 퇴장(ctx):
        try:
            await leave_channel(ctx)
        except:
            await ctx.reply("자비스는 지금 음성 채널에 들어가지 않았어요")

    @bot.command()
    async def 지민(ctx: discord.ext.commands.Context, *, message: str):

        make_tts_file(message, "지민", ctx.message.id)

        voice_client = await join_channel(ctx)
        voice_client.play(discord.FFmpegPCMAudio(options="-loglevel panic",
                                                 source=f"{ctx.message.id}.mp3"))

        while voice_client.is_playing():
            await asyncio.sleep(.1)
        os.remove(f"{ctx.message.id}.mp3")

    @bot.command()
    async def 아리(ctx: discord.ext.commands.Context, *, message: str):

        make_tts_file(message, "아리", ctx.message.id)

        voice_client = await join_channel(ctx)
        voice_client.play(discord.FFmpegPCMAudio(options="-loglevel panic",
                                                 source=f"{ctx.message.id}.mp3"))

        while voice_client.is_playing():
            await asyncio.sleep(.1)
        os.remove(f"{ctx.message.id}.mp3")

    @bot.command()
    async def 성민(ctx: discord.ext.commands.Context, *, message: str):

        make_tts_file(message, "성민", ctx.message.id)

        voice_client = await join_channel(ctx)
        voice_client.play(discord.FFmpegPCMAudio(options="-loglevel panic",
                                                 source=f"{ctx.message.id}.mp3"))

        while voice_client.is_playing():
            await asyncio.sleep(.1)
        os.remove(f"{ctx.message.id}.mp3")

    @bot.command()
    async def 민수(ctx: discord.ext.commands.Context, *, message: str):

        make_tts_file(message, "민수", ctx.message.id)

        voice_client = await join_channel(ctx)
        voice_client.play(discord.FFmpegPCMAudio(options="-loglevel panic",
                                                 source=f"{ctx.message.id}.mp3"))

        while voice_client.is_playing():
            await asyncio.sleep(.1)
        os.remove(f"{ctx.message.id}.mp3")

    print(f"[{os.path.basename(__file__)}] 명령어 활성화됨")
