import ujson
import dataclasses
from datetime import datetime

from launart import Launart
from graia.saya import Channel
from avilla.core import MessageReceived, Message
from graiax.shortcut.saya import listen, decorate

from .utils import seg_content
from shared.utils.models import get_user
from shared.utils.control import Distribute
from shared.database.tables import ChatRecord
from shared.database.interface import Database

channel = Channel.current()


@listen(MessageReceived)
@decorate(Distribute.distribute())
async def chat_recorder(message: Message):
    db = Launart.current().get_interface(Database)
    user = await get_user(message.sender)
    await db.add(
        ChatRecord(
            uid=user.id, 
            time=datetime.now(), 
            persistent_string=str(message.content),
            seg=await seg_content(message)
        )
    )