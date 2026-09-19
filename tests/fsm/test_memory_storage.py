import pytest
from peyk.fsm.storage.memory import MemoryStorage

@pytest.mark.asyncio
async def test_memory_state_and_data_are_isolated():
    storage = MemoryStorage()
    await storage.set_state("a", "StateA")
    await storage.update_data("a", x=1)
    await storage.set_state("b", "StateB")
    assert await storage.get_state("a") == "StateA"
    assert await storage.get_state("b") == "StateB"
    assert await storage.get_data("a") == {"x": 1}
    assert await storage.get_data("b") == {}
