'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'RUNNER' # change to what you need
#BOT_OWNER_ROLE_ID = "626492799621136396"
  
 

 
oot_channel_id_list = [
    "623823944549662724", #trivia king
	"613735885460209694", #loco galaxy
    "607613349491900436", #loco sudy iq
    "595635734904307742", #loco tf2.0 
	"620140094476517396", #loco ukt
	"569420128794443776",#loco unt
	"613744392968208403", #confetti gala
	"590583414541910018",#confetti study
	"605443517069656084",#confetti tf2.0
  "620140099346104325", #confetti ukt
  "588070986554015764",#confetti unt
	"523359669280833536", #hq tgl 
  "580198028950896640", #hq trivia tribe
	"513818250652680213", #hq trivia worl
  "613746114016968806",#jeetoh galaxy
  "593070663548403743", #jeetoh study
  "595636121124208640", #jeetoh tf2.0
  "620140095181291521",#jeetoh ukt
  "595654063870181386", #jeetoh unt
	"585618493093969923", # swag iq tgl
	"446448437119025154", #sawg iq tgl
    "558136902885048329",
    "588739972354408532",
    "588325679108456468",
    "570257859850272788",
    "588325025040564225",
    "588748255106433045",
	"587984504564482054",
	"587984118059499560",
	"586830578653855744",
	"588739972354408532",
	"587984347496185866",
    "588325341563715589",
	"590182635653824542",
	"590182835948879872",
	"590224806256050196",
	"590228259937976321",
	"590074352607690762",
	"590074693097095168",
	"590109407950667776",
	"590074894738259979",
	"591079879982841856",
	"591067917123190804",
	"591186950057361409",
	"590926548174110730",
"590583414541910018"
	"593460363349983233",
	"593070663548403743",
	"593990638329004032",
	"595654063870181386",
	"595636121124208640",
"619972234081075221"
]


answer_pattern = re.compile(r'(not|n)?([1-4]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 500
nomarkscore = 400
markscore = 300

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("BabluTJ v2.20 Developer Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="Google search", description="**__Searching google results for Confetti.__**")
        self.embed.add_field(name="**__Option 1__**", value="0", inline=False)
        self.embed.add_field(name="**__Option 2__**", value="0", inline=False)
        self.embed.add_field(name="**__Option 3__**", value="0", inline=False)
        self.embed.add_field(name="**__Option 4__**", value="0", inline=False)
        self.embed.set_footer(text=f"Bot made by BabluTJ_v2.20", \
            icon_url="https://cdn.discordapp.com/attachments/600721736098643991/608901532091547668/Screenshot_20190808112708.jpg")
        # await self.bot.add_reaction(embed,':Trivia_King_Official_Logo:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best=":mag:"
         

        if highest > 0:
            if answer == 1:
                one_check = ":one:"
            else:
                one_check=":x:"
            if answer ==1:
                best=":one::white_check_mark: "
            if answer == 2:
                two_check = ":two:"
            else:
                two_check= ":x:"
            if answer == 2:
                best=":two::white_check_mark: "
            if answer == 3:
                three_check = ":three:"
            else:
                three_check= ":x:"
            if answer == 3:
                best=":three::white_check_mark: "
            if answer == 4:
              four_check = ":four:"
            else:
                four_check=":x:"
            if answer == 4:
                best=":four::white_check_mark: "
                
#         if lowest < 0:
#             if answer == 1:
#                 one_check = ":question: "
#             if answer == 2:
#                 two_check = ":question: "
#             if answer == 3:
#                 three_check = ":question: "
#             if answer == 4:
#                 four_check = "question: "
 
        self.embed.set_field_at(0, name="**__Option 1__**", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**__Option 2__**", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**__Option 3__**", value="**{0}**{1}".format(lst_scores[2],three_check))
        self.embed.set_field_at(3, name="**__Option 4__**", value="**{0}**{1}".format(lst_scores[3],four_check))

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("BabluTJ_v2.20 Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name='With BabluTJ_v2.20'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Lol You Not Have permission To Use This cmd!** :Trivia_King_Official_Logo:")
            return

        if message.content.startswith('Game'):
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="Help Commands", description="**How Run Bot**", color=0x00ff00)
           embed.add_field(name="Supported Game", value="**Loco\nBrainbaazi\nPollbaazi\nSwag-iq\nThe-Q\nConfett-India\nCash-Quiz-Live\nHQ Tivia\n\nJeetoh Answer For `+`**", inline=False)
           embed.add_field(name="when Question come put command", value="** `+` is command work for support game**", inline=False)
           await message.channel.send(embed=embed)

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NTU3OTEwODMxMjU0MzM5NTk3.XYu6fw.ZT51LrwilM_ihNnZ6FkK-Uj1T3Y'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NTU4MTIwNjIwNDgzOTM2Mjc3.XUhFSQ.jaohmCL7LGF4cB-ZRyWjfmv2rZo',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
