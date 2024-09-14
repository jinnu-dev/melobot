import os

from discord import User, Invite, PartialInviteGuild
from discord import Embed
from discord.ext import commands


def enable(bot: commands.Bot):

    def get_embed(
            link: str,
            time_limit: int,
            create_time,
            max_use: int,
            owner: User,
            channel):
        embed = Embed(
            title=f"{owner}가 초대 링크 생성함", colour=0x74b9ff,
            description=f"Link : {link}")
        embed.add_field(name="⏰ 생성한 시간", value=create_time, inline=True)
        embed.add_field(name="⌛ 지속 시간", value=str(time_limit/3600)+"시간", inline=True)
        if max_use == 0:
            embed.add_field(name="🏷️ 최대 사용 가능 횟수", value="무한", inline=True)
        else:
            embed.add_field(name="🏷️ 최대 사용 가능 횟수", value=str(max_use), inline=True)
        embed.add_field(name="📄 초대 채널", value=channel.mention, inline=True)
        return embed

    @bot.event
    async def on_invite_create(invite: Invite):
        link: str = invite.url
        time_limit: int = invite.max_age
        create_time = invite.created_at
        is_temporary: bool = invite.temporary
        max_use: int = invite.max_uses
        owner: User = invite.inviter
        channel: PartialInviteGuild = invite.channel

        embed = get_embed(
            link=invite.url,
            time_limit=invite.max_age,
            create_time=invite.created_at,
            max_use=invite.max_uses,
            owner=invite.inviter,
            channel=invite.channel
        )

        log_channel = bot.get_channel(961239811811848262)
        await log_channel.send(content="초대 링크 생성됨", embed=embed)

    print(f"[{os.path.basename(__file__)}] 활성화됨")
