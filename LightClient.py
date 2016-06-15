import json
import discord
from LightCafeParser import LightCafeParser
import time
import asyncio
from Notice import NoticeBoard


class LightClient(discord.Client):
    def __init__(self, token_file):
        super().__init__()
        with open(token_file) as f:
            data = json.load(f)
            self.token = data['token']
        self.parser = LightCafeParser
        with open('data/time', 'r') as myfile:
            self.last_change = str(myfile.readline().replace('\n', ''))

    def run(self):
        self.loop.create_task(self.check_news())
        super(LightClient, self).run(self.token)

    @asyncio.coroutine
    async def check_news(self):
        await self.wait_until_ready()
        while not self.is_closed:
            self.parser.get_notices()
            if not str(NoticeBoard.last_modified()) == str(self.last_change):
                channels = []
                for serv in self.servers:
                    for chan in serv.channels:
                        if chan.name == 'announcements':
                            channels.append(chan)
                board = NoticeBoard.get_board()
                nxt = board.get()
                try:
                    while nxt:
                        for ch in channels:
                            await self.send_message(ch, str(nxt)+' @everyone')
                        nxt = board.get()
                finally:
                    NoticeBoard.write_board(board)
                self.last_change = NoticeBoard.last_modified()
                with open('data/time', 'w') as myfile:
                    myfile.write(str(self.last_change))
            print('sleeping')
            time.sleep(10)
            print('slept for days')
