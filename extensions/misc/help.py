import discord
from discord.ext import commands


class Help:
    """Help command."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["commands"])
    @commands.cooldown(1, 2)
    async def help(self, ctx, *, cmds: str=None):
        """help command for the bot"""
        if not cmds:
            commands_list = []
            for command in ctx.bot.commands:
                if command.hidden:
                    continue
                try:
                    can_run = await command.can_run(ctx)
                except Exception:
                    continue
                if can_run:
                    commands_list.append(command.name)
            commands_list.sort()
            help_text = f'{", ".join(f"`{cmd}`" for cmd in commands_list)}'

            embed = discord.Embed(title="Commands <:emalove:421669288190017538>:",
                                  description=f"{help_text}", color=0xB388FF)
            embed.set_footer(
                text=f"Use `{ctx.prefix}help <command>` for more info on a command.", icon_url=ctx.author.avatar_url_as(format="png"))

            embed.add_field(name="For more help join the support server.",
                            value="https://discord.gg/2YcPwgt")

            await ctx.send(embed=embed)

        else:
            try:
                embed = discord.Embed(color=0xB388FF)
                embed.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
                try:
                    sub = self.bot.get_command(cmds).commands
                    if not sub:
                        return await ctx.send("Command not found")
                    else:
                        for cmd in sub:
                            embed.add_field(
                                name=f"**{ctx.prefix}{cmd.signature}**", value=cmd.help.replace("%prefix%", ctx.prefix))
                except Exception:
                    command = self.bot.get_command(cmds)
                    if command.help:
                        helptxt = command.help
                    else:
                        helptxt = "Help not given."

                    embed.add_field(
                        name=f"**{ctx.prefix}{command.signature}**", value=helptxt.replace("%prefix%", ctx.prefix))
                await ctx.send(embed=embed)
            except Exception:
                await ctx.send("Command not found.")


def setup(bot):
    """Set up the extension."""
    try:
        help_command = bot.all_commands["help"]
        help_command.hidden = True
        help_command.name = "old_help"
        bot.remove_command("help")
        bot.add_command(help_command)
    except KeyError:  # This means the setup already did its thing.
        pass
    bot.add_cog(Help(bot))

