import discord
import asyncio
import re
import sys
import time
import multiprocessing
import threading
import concurrent

oot_channel_id_list = [
    "595635734904307742", #trivia fire 2.0 loco
	"620842231229841421", #galaxy loco
    "626992737018970112", #galaxy loco confetti
    "626458458064945164", #study iq loco 
	"620140094476517396", #ukt loco
	"569420128794443776", #unt loco
	"523359669280833536", #tgl hq
	"459842150323060736", #tdimension hq
	"580198028950896640", #ttribe hq
    "599522378736861194",
    "557047819832393739"

]

# getting number of answers
try:
    N = int(sys.argv[1])
except:
    N = 3

answer_pattern = \
    re.compile(r'(not|n)?([1-{0}]{{1}})(\?)?(apg)?(\?)?$'.format(N),
               re.IGNORECASE)

apgscore = 1000
nomarkscore = 20
markscore = 10


async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2]) - 1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else:  # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else:  # 1? ...
            answer_scores[ind] += markscore

    else:  # contains not or n
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
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        def is_scores_updated(message):
            if message.guild == None or \
                    str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2]) - 1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else:  # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else:  # 1? ...
                    self.answer_scores[ind] += markscore

            else:  # contains not or n
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
        global N
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed = discord.Embed(title="MADE BY nhocsuhot ", description="**Connecting .**", color=0x000440)
        for fnum in range(N):
            self.embed.add_field(name=chr(65 + fnum), value="0", inline=False)
            self.embed.set_footer(text=f"© MADE BY .",
                                  icon_url="")

    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i] = 0

    async def update_embeds(self):
        global N
        check = [''] * N

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)

        if lst_scores.count(highest) < N:
            check[lst_scores.index(highest)] = ":white_check_mark:"
            check[lst_scores.index(lowest)] = ":x:"

        for fnum in range(N):
            self.embed.set_field_at(fnum, name=chr(65 + fnum),
                                    value="{0}{1}".format(lst_scores[fnum], check[fnum]))

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name=''))

    async def send_embed(self, channel, embed):
        return await channel.send('', embed=embed)

    async def edit_embed(self, old_embed, new_embed):
        return await old_embed.edit(embed=new_embed)

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return
        if message.content.lower() == "":
            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await self.send_embed(message.channel, self.embed)
            self.embed_channel_id = message.channel.id
            return

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
            time.sleep(0.2)
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            # res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NTgwMjc5MjM1ODk4MjQ1MTMx.XY5c7w.EdAen5LzqBYIfNRxEabIosU14_8'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):
    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NDg5MTM4MDQ4ODc0MDUzNjQ0.XY4D5A.RpgBuCsSkwT5yQhL6daYXYNb1Qo',
                                   bot=False))
    loop.run_forever()


if __name__ == '__main__':
    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=N)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
