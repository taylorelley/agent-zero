from python.helpers.extension import Extension
from agent import LoopData
from python.helpers import memory
import asyncio


class MemoryInit(Extension):

    async def execute(self, loop_data: LoopData | None = None, **kwargs):
        if loop_data is None:
            loop_data = LoopData()
        db = await memory.Memory.get(self.agent)
        

   