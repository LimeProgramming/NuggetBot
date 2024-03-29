import discord
import datetime
import random
import asyncio
import colorsys

### Embed generater for when a member joins
### to be posted in archive
async def getMemJoinStaff(member, invite):

    embed = discord.Embed(  description="Mention: <@{0.id}> | Username: {0.name}#{0.discriminator}\n"
                                        "Created (UTC): {1}".format(member,
                                                                    member.created_at.strftime('%b %d, %Y %H:%M:%S')
                                                                    ),
                            colour=     0x51B5CC,
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow()
                        )

    embed.set_author(       name=       "Member Joined",
                            icon_url=   AVATAR_URL_AS(member)
                    )

    #===== If user is a bot account
    if member.bot:
        embed.add_field(    name=       "Bot Account",
                            value=      "This user account is a bot.",
                            inline=     False
                        )

    #===== if account is less than 7 days old
    diff = (datetime.datetime.utcnow() - member.created_at)
    if diff.days < 7:
        
        #=== days
        if diff.days:
            ago = "{} days".format(diff.days)
        #=== hours
        if int(diff.seconds/3600):
            ago = "{} hours".format(round(diff.seconds/3600))
        #=== minutes
        elif int(diff.seconds/60):
            ago = "{} minutes".format(round(diff.seconds/60))
        #=== seconds
        else:
            ago = "{} seconds".format(diff.seconds)

        embed.add_field(    name=       "New Account",
                            value=      "Account made {} ago. "
                                        "Be cautious of possible troll.".format(ago),
                            inline=     False
                        )

    #===== Invite info
    if invite is not None:
        if invite["max_uses"] == 0:
            embed.add_field(name=       "Invite",
                            inline=     False,
                            value=      "User: {} / {}#{} | Code: {}".format( invite["inviter"]["mention"],
                                                                                invite["inviter"]["name"],
                                                                                invite["inviter"]["discriminator"],
                                                                                invite["code"]
                                                                            )
                            )
        else:
            embed.add_field(name=       "Invite",
                            inline=     False,
                            value=      "User: {} / {}#{} | Code: {} | Uses: {}/{}".format( invite["inviter"]["mention"],
                                                                                            invite["inviter"]["name"],
                                                                                            invite["inviter"]["discriminator"],
                                                                                            invite["code"],
                                                                                            invite["uses"],
                                                                                            invite["max_uses"]
                                                                                            )
                            )

    else:
        embed.add_field(    name=       "Invite",
                            value=      "Invite not found",
                            inline=     False
                        )

    #===== Footer
    embed.set_footer(       text=f"User ID: {member.id}"
                    )

    return embed

async def getMemLeaveStaff(member, memberBanned):
    embed = discord.Embed(  description="Mention: <@{0.id}> | Username: {0.name}#{0.discriminator}\n"
                                        "Join Date: {1}".format( member,
                                                                member.joined_at.strftime('%b %d, %Y %H:%M:%S')
                                                                ),
                            colour=     0xCC1234,
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow()
                        )

    embed.set_author(       name=       ("Member Left" if not memberBanned else "Member Banned"),
                            icon_url=   AVATAR_URL_AS(member)
                    )

    embed.set_footer(       text=       f"User ID: {member.id}"
                    )
    
    return embed

async def getMemJoinLeaveUser(member, joining):

    embed = discord.Embed(  description="Mention: <@{0.id}> | Username: {0.name}#{0.discriminator}\n"
                                        "{1}".format(   member, 
                                                        f"Created (UTC): {member.created_at.strftime('%b %d, %Y %H:%M:%S')}" 
                                                        if joining else 
                                                        f"Join Date: {member.joined_at.strftime('%b %d, %Y %H:%M:%S')}"
                                                    ),

                            colour=     0x51B5CC if joining else 0xCC1234,
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow()
                        )

    embed.set_author(       name=       ("Member Banned" if joining == "banned" else ("Member Joined" if joining else "Member Left")),
                            icon_url=   AVATAR_URL_AS(member)
                    )
                    
    embed.set_footer(       icon_url=   GUILD_URL_AS(member.guild),
                            text=       member.guild.name
                    )
    
    return embed

async def getScheduleRemNewRole(member, daysUntilRemove):
    #==== log event
    embed = discord.Embed(  title=      'Event Scheduled', 
                            description="{0.mention} | {0.name}#{0.discriminator} will have the Fresh role removed in {1} days.".format(member,
                                                                                                                                        daysUntilRemove
                                                                                                                                        ),
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            color=      0x0091E0)
    return embed

async def genRemNewRole(member):
    embed = discord.Embed(  title=      'Scheduled Event', 
                            description='{0.mention} | {0.name}#{0.discriminator} has had their Fresh role removed.'.format(member), 
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            color=      0xB20828
                        )
    
    return embed

async def getScheduleKick(member, daysUntilKick, kickDate):
    #==== log event
    embed = discord.Embed(  title=      'Event Scheduled', 
                            description="{} | {}#{} will be kicked in {} days ({} CE), unless verified.".format(   member.mention,
                                                                                                                member.name,
                                                                                                                member.discriminator,
                                                                                                                daysUntilKick,
                                                                                                                kickDate.strftime('%H:%M:%S, %b %d, %Y')),
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            color=      0x0091E0)
    return embed

async def genKickEntrance(member, entrance_gate_channel_id):
    embed = discord.Embed(  title=      'Scheduled Event', 
                            description='<@{0.id}> | {0.name}#{0.discriminator} has been kicked from <#{1}>.'.format(member, entrance_gate_channel_id), 
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            color=      0xB20828
                        )
    
    return embed

#==================== Massive perms embeds
async def getUserPermsOwner(member, msg):
    embed = discord.Embed(  title=      "Server Owner",
                            description="User: <@{0.id}> | {0.name}#{0.discriminator} is owner of {1.name}, behave yourself with them around.".format(  member,
                                                                                                                                                        msg.guild
                                                                                                                                                        ),
                            colour=     0x51B5CC,
                            timestamp=  datetime.datetime.utcnow(),
                            type=       "rich"
                            )

    embed.set_thumbnail(    url=        AVATAR_URL_AS(member)
                        )

    embed.set_author(       name=       "{0.name}#{0.discriminator}".format(member),
                            icon_url=   AVATAR_URL_AS(member)
                    )

    embed.set_footer(       icon_url=   GUILD_URL_AS(msg.guild), 
                            text=       "{0.guild.name} | ID: {1.id}".format(msg, member)
                    )

    embed.add_field(        name=       "Roles[{}]".format( len(member.roles) - 1),
                            value=      (" ".join([role.mention for role in member.roles if not role.is_everyone])) 
                                        if len(member.roles) > 1 else 
                                        ("Member has no roles.")
                    )

    return embed

async def getUserPermsAdmin(member, msg):
    embed = discord.Embed(   title=      "Administrator",
                            description="User: {0.mention} | {0.name}#{0.discriminator} has Admin permission and can do everything.\n"
                                        "Hierarchy: {1}".format( member,
                                                                (len(msg.guild.roles) - member.top_role.position)
                                                                ),
                            colour=     0x51B5CC,
                            timestamp=  datetime.datetime.utcnow(),
                            type=       "rich"
                        )

    embed.set_thumbnail(    url=        AVATAR_URL_AS(member)
                        )
    embed.set_author(       name=       "{0.name}#{0.discriminator}".format(member),
                            icon_url=   AVATAR_URL_AS(member)
                    )
    embed.set_footer(       icon_url=   GUILD_URL_AS(msg.guild), 
                            text=       "{0.guild.name} | ID: {1.id}".format(msg, member)
                    )
    embed.add_field(        name=       "Roles[{}]".format( len(member.roles) - 1),
                            
                            value=      (" ".join([role.mention for role in member.roles if not role.is_everyone])) 
                                        if len(member.roles) > 1 else 
                                        ("Member has no roles.")
                    )

    return embed

async def getUserPerms(member, msg):
    #===== Variable setup
    server_wide_perms = list()
    channel_specific_perms = list()
    embeds = list()
    perms = ["Create Instant Invite", "Kick Members", "Ban Members", "Administrator", "Manage Channels",
            "Manage Server","Add Reactions", "View Audit Logs", "Nothing", "Nothing", "Read Messages", "Send Messages",
            "Send TTS Messages", "Manage Messages", "Embed Links", "Attach Files", "Read Message History",
            "Mention Everyone", "External Emojis", "Nothing", "Connect", "Speak", "Mute Members", "Deafen Members",
            "Move Members", "Use Voice Activation", "Change Nickname", "Manage Nicknames", "Manage Roles",
            "Manage Webhooks", "Manage Emojis"]

    raw_perms = ["create_instant_invite", "kick_members", "ban_members", "administrator", "manage_channels",
            "manage_server","add_reactions", "view_audit_logs", "", "", "read_messages", "send_messages",
            "send_tts_messages", "manage_messages", "embed_links", "attach_files", "read_message_history",
            "mention_everyone", "external_emojis", "", "connect", "speak", "mute_members", "deafen_members",
            "move_members", "use_voice_activation", "change_nickname", "manage_nicknames", "manage_roles",
            "manage_webhooks", "manage_emojis"]
    

    #===== server wide
    """
        This is how discord permissions work, 
        27 possible options all rolled into a 10 digit int that you have to adjust and do a Bitwise And function on.
        I don't really know how it works but at least it can be shortened down into a loop.
        4 values are unused (place 31 unlisted here) with the possibility of 21 more. 
        So discord can easily add 25 more perms.
        """
    for role in member.roles:
        for i in range(31):
            if bool((role.permissions.value >> i) & 1):
                server_wide_perms.append(perms[i])

    #===== one entry for each item
    server_wide_perms = list(set(server_wide_perms))

    #===== channel
    """
        Getting the channel perms for the role sorted.
        The channels are sorted by position for readability of results. 
        Normally they are sorted by position anyway but sometimes they come back in a mess of an order.
        """
    for channel in sorted(msg.guild.channels, key=lambda x: x.position):
        temp = list()
        cleanedTemp = list()

        for role in ([member] + member.roles):
            channelPerms = channel.overwrites_for(role)

            for i in range(31):
                if not raw_perms[i] == "":
                    #Making sure voice channels are not checked for buggy text channel perms
                    if (channel.type == discord.ChannelType.voice) and (raw_perms[i] in ["read_messages", "send_messages"]):
                        continue

                    #Making sure text channels are not checked for voice channel perms
                    if (channel.type == discord.ChannelType.text) and (raw_perms[i] in ["speak", "connect", "mute_members", "deafen_members", "move_members", "use_voice_activation"]):
                        continue

                    result = channelPerms._values.get(raw_perms[i])

                    if isinstance(role, discord.Member):
                        if result == True:
                            temp.append("**[User]** {}".format(perms[i]))

                        elif result == False:
                            temp.append("**[User]** Not {}".format(perms[i]))

                    else:
                        if result == True:
                            temp.append(perms[i])

                        elif result == False:
                            temp.append("Not {}".format(perms[i]))

        """
            Because discord will take a yes over a no when it comes to perms,
            we remove the Not {perm} is the perm is there as a yes
            """
        for item in temp:
            if item.startswith("Not"):
                if not any([i for i in temp if i == item[4:]]):
                    cleanedTemp.append(item)

            else: 
                cleanedTemp.append(item)

        #=== If at end of loop no perms where found, log nothing.
        if len(cleanedTemp) > 0:
            channel_specific_perms.append(dict(channelName=channel.name,
                                                perms=cleanedTemp,
                                                channelType=channel.type.__str__()))


    #===== results, processing them into an actual reply
    #You can only have 25 fields in a discord embed. So I'm breaking up my list of possible fields into a 2d array.
    channel_specific_perms = await split_list(channel_specific_perms, size=24)
    firstLoop = True

    for channelSpecificPerms in channel_specific_perms:
        
        #=== Set up the first embed
        if firstLoop:
            text = " | ".join(server_wide_perms)
            if text == "":
                text = "None"

            embed = discord.Embed(  title=      "Server Wide:",
                                    description="{}\n"
                                                "**Hierarchy: {}**".format(text,
                                                                            (len(msg.guild.roles) - member.top_role.position)
                                                                            ),
                                    colour=     0x51B5CC,
                                    timestamp=  datetime.datetime.utcnow(),
                                    type=       "rich"
                                    )

            embed.set_author(       name=       "{0.name}#{0.discriminator}".format( member,
                                                                                    ),
                                    icon_url=   member.avatar_url.__str__()
                            )

            embed.add_field(        name=       "Roles[{}]".format(len(member.roles) - 1),

                                    value=      (" ".join([role.mention for role in member.roles if not role.is_everyone])) 
                                                if len(member.roles) > 1 else 
                                                ("Member has no roles.")
                            )

        #=== Set up additional embeds
        else:
            embed = discord.Embed(  description="",
                                    colour=     0x51B5CC,
                                    timestamp=  datetime.datetime.utcnow(),
                                    type=       "rich"
                                    )

            embed.set_author(       name=       "{0.name}#{0.discriminator} | Information Continued".format( member,
                                                                                                            ),
                                    icon_url=   member.avatar_url.__str__()
                            )

        for i in channelSpecificPerms:
            #= The category channel type does not have a name, instead it's called "4"
            embed.add_field(        name=       i["channelName"] + (":" if not i["channelType"] == "4" else " - Category:"),
                                    value=      " | ".join(i["perms"]),
                                    inline=     False
                            )


        #=== since these are always going to be the same
        embed.set_thumbnail(        url=        member.avatar_url.__str__()
                            )
        embed.set_footer(           icon_url=   GUILD_URL_AS(msg.guild), 
                                    text="{0.guild.name} | ID: {1.id}".format(msg, member)
                        )

        embeds.append(embed)
        firstLoop = False

    return embeds

async def getRolePerms(msg, role, bot_avatar_url):

    #===== Variable setup
    server_wide_perms = list()
    channel_specific_perms = list()
    embeds = list()
    perms = ["Create Instant Invite", "Kick Members", "Ban Members", "Administrator", "Manage Channels",
            "Manage Server","Add Reactions", "View Audit Logs", "Nothing", "Nothing", "Read Messages", "Send Messages",
            "Send TTS Messages", "Manage Messages", "Embed Links", "Attach Files", "Read Message History",
            "Mention Everyone", "External Emojis", "Nothing", "Connect", "Speak", "Mute Members", "Deafen Members",
            "Move Members", "Use Voice Activation", "Change Nickname", "Manage Nicknames", "Manage Roles",
            "Manage Webhooks", "Manage Emojis"]

    raw_perms = ["create_instant_invite", "kick_members", "ban_members", "administrator", "manage_channels",
            "manage_server","add_reactions", "view_audit_logs", "", "", "read_messages", "send_messages",
            "send_tts_messages", "manage_messages", "embed_links", "attach_files", "read_message_history",
            "mention_everyone", "external_emojis", "", "connect", "speak", "mute_members", "deafen_members",
            "move_members", "use_voice_activation", "change_nickname", "manage_nicknames", "manage_roles",
            "manage_webhooks", "manage_emojis"]
    

    #===== server wide
    """
        This is how discord permissions work, 
        27 possible options all rolled into a 10 digit int that you have to adjust and do a Bitwise And function on.
        I don't really know how it works but at least it can be shortened down into a loop.
        4 values are unused (place 31 unlisted here) with the possibility of 21 more. 
        So discord can easily add 25 more perms.
        """
    for i in range(31):
        if bool((role.permissions.value >> i) & 1):
            server_wide_perms.append(perms[i])

    #===== channel
    """
        Getting the channel perms for the role sorted.
        The channels are sorted by position for readability of results. 
        Normally they are sorted by position anyway but sometimes they come back in a mess of an order.
        """
    for channel in sorted(msg.guild.channels, key=lambda x: x.position):
        temp = list()
        channelPerms = channel.overwrites_for(role)

        for i in range(31):
            if not raw_perms[i] == "":
                #Making sure voice channels are not checked for buggy text channel perms
                if (channel.type == discord.ChannelType.voice) and (raw_perms[i] in ["read_messages", "send_messages"]):
                    continue

                #Making sure text channels are not checked for voice channel perms
                if (channel.type == discord.ChannelType.text) and (raw_perms[i] in ["speak", "connect", "mute_members", "deafen_members", "move_members", "use_voice_activation"]):
                    continue

                """
                    Channel overwrite perms do not have a value unlike regular permissions.
                    So it's easier to feed the "_values.get()" function a perm you're looking for than to try and retrive a value you can use yourself.
                    Technically I could have looped through 27*2 if statements but this is cleaner. 
                    """
                result = channelPerms._values.get(raw_perms[i])

                if result == True:
                    temp.append(perms[i])

                elif result == False:
                    temp.append(("Not {}".format(perms[i])))
        
        #=== If at end of loop no perms where found, log nothing.
        if len(temp) > 0:
            channel_specific_perms.append(dict(channelName=channel.name,
                                                perms=temp,
                                                channelType=channel.type.__str__()))


    #===== results, processing them into an actual reply
    #You can only have 25 fields in a discord embed. So I'm breaking up my list of possible fields into a 2d array.
    channel_specific_perms = await split_list(channel_specific_perms, size=25)
    firstLoop = True

    for channelSpecificPerms in channel_specific_perms:
        
        #=== Set up the first embed
        if firstLoop:
            text = " | ".join(server_wide_perms)
            if text == "":
                text = "None"

            embed = discord.Embed(  title=      "Server Wide:",
                                    description="{}\n".format(text),
                                    colour=     0x51B5CC,
                                    timestamp=  datetime.datetime.utcnow(),
                                    type=       "rich"
                                    )

            embed.set_author(       name=       "{} Information".format(role.name),
                                    icon_url=   bot_avatar_url
                            )

        #=== Set up additional embeds
        else:
            embed = discord.Embed(  description="",
                                    colour=     0x51B5CC,
                                    timestamp=  datetime.datetime.utcnow(),
                                    type=       "rich"
                                    )

            embed.set_author(       name=       "{} information continued".format(role.name),
                                    icon_url=   bot_avatar_url
                            )

        for i in channelSpecificPerms:
            #= The category channel type does not have a name, instead it's called "4"
            embed.add_field(        name=       i["channelName"] + (":" if not i["channelType"] == "4" else " - Category:"),
                                    value=      " | ".join(i["perms"]),
                                    inline=     False
                            )

        embed.set_footer(           icon_url=   GUILD_URL_AS(msg.guild), 
                                    text=       f"{msg.guild.name}"
                        )

        embeds.append(embed)
        firstLoop = False
    
    return embeds

async def getRolePermsAdmin(role, msg):
    embed = discord.Embed(  title=      "Administrator",
                            description="{} role has Admin permission and can do everything.".format(role.name),
                            colour=     0x51B5CC,
                            timestamp=  datetime.datetime.utcnow(),
                            type=       "rich"
                            )

    embed.set_author(       name=       "{} Information".format(role.name),
                            icon_url=   GUILD_URL_AS(msg.guild)
                    )

    embed.set_footer(       icon_url=   GUILD_URL_AS(msg.guild), 
                            text=       "{}".format(msg.guild.name)
                    )

    return embed





async def getNuggetHelp(msg, avatar_url, command_prefix, reception_channel_id, self_mention):
    embed = discord.Embed(  title=      "Self Assignable Roles:",
                            description="**SFW Roles:**\n"
                                        "" + command_prefix + "NotifyMe:\tA role that we use to ping people about goings on.\n"
                                        "" + command_prefix + "Book_Wyrm:\tUsed to access <#304365533619421184> text and voice channels.\n"
                                        "" + command_prefix + "RP:\tUsed to access the SFW RP channels.\n"
                                        "" + command_prefix + "Artist:\tArtists who are open to commissions. Plus gain write permissions in <#382167213521633280>\n"
                                        "\n"
                                        "**NSFW Roles (NSFW Role required):**\n"
                                        "" + command_prefix + "RP_Lewd:\tUsed to access the NSFW RP channels.\n"
                                        "\n",
                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            colour=     0x51B5CC
                        )

    embed.set_author(   name=   "Nugget Help",
                        icon_url=avatar_url)

    embed.add_field(    name=   "NSFW Access",
                        value=  "To get access to the NSFW channels just ping staff in <#{}> with your age.".format(reception_channel_id),
                        inline= False)

    embed.add_field(    name=   "Private Feedback:",
                        value=  "You can always DM me {} with feedback for the staff.\nFeedback can be submitted anonymously this way.".format(self_mention),
                        inline= False)
    
    embed.add_field(    name=   "Fun Commands:",
                        value=  f"{command_prefix}RPS <rock/paper/scissors>:\tPlay rock paper scissors with me.\n"
                                f"{command_prefix}8ball <question>:\tAsk your question and I shall consult the ball of knowledge.\n"
                                f"{command_prefix}Roll <number>:\tRole a dice, you tell me how high I can go.\n"
                                f"{command_prefix}Leaderboard:\tTop 10 most popular, I hope I'm on that list.\n",
                        inline= False
                    )
    
    embed.add_field(    name=   "Art and Commissions:",
                        value=  
                                f"{command_prefix}Commissioner:\tAdds commissioner role, meant for people looking for commissions.\n"
                                f"{command_prefix}FindArtists:\tDMs you info about any artist who have registered with us.\n"
                                f"{command_prefix}OpenCommissions:\tAdds OpenCommissions role to artists, to show you have slots open.\n"
                                f"{command_prefix}ArtistRegister <info>: For artists registering their info with us.\n"
                                f"{command_prefix}PingCommissioners: Artists can ping people with the Commissioner role.\n"
                                "[Note: expect more info on this subject soon]",
                        inline= False)

    embed.add_field(    name=   "Need a break?:",
                        value=  "If you want to hide the server from yourself for a while; "
                                f"you can post {command_prefix}HideServer <xDxHxMxS/seconds> and "
                                "I'll try hide the server from you for a bit. You can re-show the server anytime. \n"
                                "If you're stressed, don't worry: https://www.youtube.com/watch?v=L3HQMbQAWRc,",
                        inline= False)

    embed.set_footer(   text=    msg.guild.name,
                        icon_url=GUILD_URL_AS(msg.guild)
    )
    
    return embed 


async def getMemberLeveledUP(msg, level, reward, total):
    embed = discord.Embed(      description=    f"Level: {level} | Reward: {reward} :gem:\n"
                                                f"Total Gems: {total}",
                                colour =        0xbe95c6,
                                timestamp=      datetime.datetime.utcnow(),
                                type=           "rich"
                    )
    embed.set_author(           name=       "Level Up!",
                                icon_url=   AVATAR_URL_AS(user=msg.author)
                    )
    embed.set_thumbnail(        url=        AVATAR_URL_AS(user=msg.author))

    embed.set_footer(           icon_url=   GUILD_URL_AS(msg.guild),
                                text=       "{0.name}#{0.discriminator}".format(msg.author)
                    )
    return embed


async def getUserProfile(msg, info):
    embed = discord.Embed(      description=    f"Level: {info['level']}\n"
                                                f"Gems: {info['gems']} :gem:\n",
                                colour =        random_embed_color(), #0xbe95c6,
                                timestamp=      datetime.datetime.utcnow(),
                                type=           "rich"
    )
    embed.set_author(           name=           "{0.name}#{0.discriminator}".format(msg.author),
                                icon_url=       AVATAR_URL_AS(user=msg.author)
    )
    embed.set_thumbnail(        url=            AVATAR_URL_AS(user=msg.author))

    embed.set_footer(           icon_url=       GUILD_URL_AS(msg.guild), 
                                text=           "{0.guild.name} | ID: {0.author.id}".format(msg)
    )
    
    return embed 
    
async def getCancelHideServer(member):
    embed = discord.Embed(  description="{} has been made available to you again.\n"
                                        "Welcome back.".format(member.guild.name),
                            type=       'rich',
                            timestamp=  datetime.datetime.utcnow(),
                            color=      0x6953B2,
                        )

    embed.set_footer(       icon_url=   GUILD_URL_AS(member.guild),
                            text=       member.guild.name
                    )
        
    embed.set_author(       name=       'Server Available',
                            icon_url=   AVATAR_URL_AS(user=member)
                    )
    
    return embed


#==================== Owner commands
async def ownerRestart(msg):

    embed = discord.Embed(  description="Restarting 👋",
                            colour=     0x6BB281,
                            timestamp=  datetime.datetime.utcnow(),
                            type=       "rich"
                            )
    embed.set_footer(       icon_url=   GUILD_URL_AS(msg.guild), 
                            text=       msg.guild.name
                    )
    embed.set_author(       name=       "Owner Command",
                            icon_url=   AVATAR_URL_AS(user=msg.author)
                    )

    return embed 

async def ownerShutdown(msg):
    embed = discord.Embed(  description="Shutting Down 👋",
                            colour=     0x6BB281,
                            timestamp=  datetime.datetime.utcnow(),
                            type=       "rich"
                            )

    embed.set_footer(       icon_url=   GUILD_URL_AS(msg.guild), 
                            text=       msg.guild.name
                    )

    embed.set_author(       name=       "Owner Command",
                            icon_url=   AVATAR_URL_AS(user=msg.author)
                    )

    return embed

@asyncio.coroutine
async def genFeedbackSnooping(user_id, msg_id, chl_id, srv_id, present, senddate, guild):
    embed = discord.Embed(  title=      'Anon Feedback',
                            description=f'User: <@{user_id}> | Still on guild: {present}\n'
                                        f"On {senddate.strftime('%b %d, %Y %H:%M:%S')} (UTC), posted:\n https://discordapp.com/channels/{srv_id}/{chl_id}/{msg_id}",

                            type=       "rich",
                            timestamp=  datetime.datetime.utcnow(),
                            color=      random_embed_color()
                                    
                            )

    embed.set_footer(       icon_url=   GUILD_URL_AS(guild),
                            text=       guild.name
                    )
    return embed




#==================== Functions
def AVATAR_URL_AS(user, format=None, static_format='webp', size=256):
    if not isinstance(user, discord.abc.User):
        return 'https://cdn.discordapp.com/embed/avatars/0.png'

    if user.avatar is None:
        # Default is always blurple apparently
        #return user.default_avatar_url
        return 'https://cdn.discordapp.com/embed/avatars/{}.png'.format(user.default_avatar.value)

    format = format or 'png'

    return 'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.{1}?size={2}'.format(user, format, size)


def GUILD_URL_AS(guild, format=None, static_format='webp', size=256):
    if not isinstance(guild, discord.Guild):
        return 'https://cdn.discordapp.com/embed/avatars/0.png'
    
    if format is None:
        format = 'gif' if guild.is_icon_animated() else static_format

    return 'https://cdn.discordapp.com/icons/{0.id}/{0.icon}.{1}?size={2}'.format(guild, format, size)

def random_embed_color():
    choice = random.choice([1]*10 + [2]*20 + [3]*20)

    if choice == 1:
        values = [int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1)]
    elif choice == 2: 
        values = [int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), random.random(), 1)]
    else:
        values = [int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), random.random(), random.random())]

    color = discord.Color.from_rgb(*values)

    return color

async def split_list(arr, size=100):
    """Custom function to break a list or string into an array of a certain size"""

    arrs = []

    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]

    arrs.append(arr)
    return arrs


