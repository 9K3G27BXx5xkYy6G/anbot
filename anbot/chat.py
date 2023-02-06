import asyncio, logging

import emoji

from opsdroid.core import OpsDroid

from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_event
from opsdroid.events import OpsdroidStarted, JoinRoom, LeaveRoom

logger = logging.getLogger()

class MySkill(Skill):
    def __init__(self, opsdroid, config):
        super().__init__(opsdroid, config)

    @match_event(OpsdroidStarted)
    async def join_and_leave_test_room(self, event):
        matrix = self.opsdroid.get_connector('matrix')
        logger.info('Joining ...')
        await self.opsdroid.send(JoinRoom(
                target = '#test-bot:matrix.org',
                connector = matrix,
            ))
        logger.info('waiting ...')
        await asyncio.sleep(10)
        logger.info('leaving ...')
        await self.opsdroid.send(LeaveRoom(
                target = '#test-bot:matrix.org',
                connector = matrix,
            ))
        logger.info('stopping ...')
        await self.opsdroid.stop()

    @match_regex('how are you?')
    async def how_are_you(self, message):
        await message.respond('Good thanks! My load average is 0.2, 0.1, 0.1.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # it looks like opsdroid modules can be loaded either by providing a path, even to this file, in a config, or
    #  possibly by adding entries to the opsdroid.modules dictionary after loading.
    import gettext, inspect
    __file__ = inspect.stack()[0][1] # file path of this script

    gettext.install('opsdroid') # opsdroid needs gettext installed

    # configs can be objects or files.
        # config files can be reloaded at runtime with opsdroid.reload(); config objects would need to be
        # manually reloaded per the content of that function (await .stop(), .unload(), .config=, .load(), .start())
    opsdroid_config = dict(
        skills = dict(
            my_skill = dict(path = __file__)
        ),
        connectors = dict(
            matrix = dict(
                mxid = '@test_matrix_bot:matrix.org',
                password = 'test_matrix_bot',
                rooms = {
                    'main': '#test-bot:matrix.org'
                },
                nick = 'test-matrix-bot-B',
                #room_specific_nicks = False,  # Look up room specific nicknames of senders (expensive in large rooms)
                #device_name = 'opsdroid',
                #enable_encryption = False,
                #device_id = 'opsdroid', # A unique string to use as an ID for a persistent opsdroid device
                #store_path = 'path/to/store/', # Path to the directory where the matrix store will be saved
            )
        ),
    )
    with OpsDroid(config=opsdroid_config) as opsdroid:
        # opsdroid can launch its own eventloop with .run, or the user can .load/.sync_load and then await for .start()
        opsdroid.run()
    import time
    class Bot(Services):
        pass
    bot = Bot()
    print(f'Logging in ...')
    matrix_service = bot.add_matrix(username='test_matrix_bot', password='test_matrix_bot', homeserver='https://matrix.org')
    room_name = '#test-bot:matrix.org'
    print(f'Joining {room_name} ...')
    test_room = matrix_service.join(room_name)
    print(f'Waiting a bit ...')
    time.sleep(10)
    print(f'Parting {room_name} ...')
    matrix_service.part(test_room)
