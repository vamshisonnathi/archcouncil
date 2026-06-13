import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from thenvoi import Agent
from thenvoi.adapters import AnthropicAdapter
from thenvoi.config import load_agent_config
from thenvoi.core.types import AdapterFeatures, Emit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"
SYSTEM_PROMPT = (PROMPTS_DIR / "scalability.md").read_text()


async def main():
    load_dotenv()
    agent_id, api_key = load_agent_config("scalability_agent")

    adapter = AnthropicAdapter(
        model="claude-haiku-4-5-20251001",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=2048,
        features=AdapterFeatures(emit=[Emit.EXECUTION]),
    )

    create_kwargs = dict(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )
    if os.getenv("THENVOI_WS_URL"):
        create_kwargs["ws_url"] = os.getenv("THENVOI_WS_URL")
    if os.getenv("THENVOI_REST_URL"):
        create_kwargs["rest_url"] = os.getenv("THENVOI_REST_URL")

    agent = Agent.create(**create_kwargs)

    logger.info("Scalability Agent running...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
