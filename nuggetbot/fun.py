import discord

from .utils import Response
from .util.chat_formatting import AVATAR_URL_AS, GUILD_URL_AS, RANDOM_DISCORD_COLOR
from random import randint
from random import choice
from enum import Enum
import datetime

class RPS(Enum):
    rock     = "\N{MOYAI}"
    paper    = "\N{PAGE FACING UP}"
    scissors = "\N{BLACK SCISSORS}"


class Fun():
    ball = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely", "Outlook good",
            "Signs point to yes", "Without a doubt", "Yes", "Yes – definitely", "You may rely on it", "Reply hazy, try again",
            "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    @classmethod
    async def roll(cls, author, number : int = 100):
        """Rolls random number (between 1 and user choice)
        Defaults to 100.
        """
        if number > 1:
            n = randint(1, number)
            return Response(content=f"{author.mention} :game_die: {n} :game_die:", reply=True)

        return Response(content=f"{author.mention} Maybe higher than 1?", reply=True)

    @classmethod
    async def rps(cls, author, your_choice):
        """Play rock paper scissors"""

        your_choice = your_choice.lower()

        if your_choice == "rock":
            player_choice = RPS.rock
        elif your_choice == "paper":
            player_choice = RPS.paper
        elif your_choice == "scissors":
            player_choice = RPS.scissors
        else:
            player_choice = None

        bot_choice = choice((RPS.rock, RPS.paper, RPS.scissors))

        cond = {
                (RPS.rock,     RPS.paper)    : False,
                (RPS.rock,     RPS.scissors) : True,
                (RPS.paper,    RPS.rock)     : True,
                (RPS.paper,    RPS.scissors) : False,
                (RPS.scissors, RPS.rock)     : False,
                (RPS.scissors, RPS.paper)    : True
               }

        if player_choice == None:
            return Response(content="Error", reply=True)

        if bot_choice == player_choice:
            outcome = None # Tie
        else:
            outcome = cond[(player_choice, bot_choice)]

        if outcome is True:
            return Response(content="{} You win {}!"
                                    "".format(bot_choice.value, author.mention),
                                    reply=True)
        elif outcome is False:
            return Response(content="{} You lose {}!"
                                    "".format(bot_choice.value, author.mention),
                                    reply=True)
        else:
            return Response(content="{} We're square {}!"
                                    "".format(bot_choice.value, author.mention),
                                    reply=True)

    @classmethod
    async def _8ball(cls, question : str, guild, author):
        """Ask 8 ball a question
        Question must end with a question mark.
        """

        if question.endswith("?") and question != "?":
            e = discord.Embed(
                            title=          "Question",
                            type=           "rich",
                            color=          RANDOM_DISCORD_COLOR(),
                            description=    question,
                            timestamp=      datetime.datetime.utcnow()
                            )
            e.add_field(    name=       "Answer",
                            value=      choice(cls.ball),
                            inline=     False
                        )
            e.set_author(   name=       "8Ball | {0.name}#{0.discriminator}".format(author),
                            icon_url=   AVATAR_URL_AS(user=author)
                        )
            e.set_footer(   icon_url=   GUILD_URL_AS(guild), 
                            text=       f"{guild.name}"
                        )

            return Response(embed=e, reply=True)

        else:
            return Response(content="That doesn't look like a question.", reply=True)
