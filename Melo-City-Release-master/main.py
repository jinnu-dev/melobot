"""
봇이 구동되는 시작 파일
이 파일에서 필요한 명령어 및 이벤트를 불러온다.
"""
import discord
import event
import command

from discord.ext import commands
from discord_components import DiscordComponents
from function import json


setting = json.get_data("setting.json")

prefix = setting["Bot"]["Prefix"]
token = setting["Bot"]["Token"]

# 봇 클래스 생성
bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=prefix,
    status=discord.Status.do_not_disturb  # 기본값은 방해 금지 모드
)

# 컴포넌트를 사용할 수 있는 클라이언트로 변경
DiscordComponents(bot)

event.on_ready.enable(bot)
event.on_command_error.enable(bot)
event.on_member_join.enable(bot)
event.on_message_delete.enable(bot)
event.on_message.enable(bot)
event.on_voice_state_update.enable(bot)
event.on_reaction_add.enable(bot)
event.on_invite_create.enable(bot)

command.activity.enable(bot)
command.anonymous.enable(bot)
command.clean.enable(bot)
command.profile.enable(bot)
command.warning.enable(bot)
command.tts.enable(bot)
command.embed.enable(bot)

# command.debug.enable(bot)
# command.setremote.enable(bot)

bot.run(token)
