import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from thenvoi import Agent
from thenvoi.adapters import AnthropicAdapter
from thenvoi.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"
SYSTEM_PROMPT = (PROMPTS_DIR / "cost.md").read_text()


async def main():
    load_dotenv()
    agent_id, api_key = load_agent_config("cost_agent")

    adapter = AnthropicAdapter(
        model="claude-haiku-4-5",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=2048,
        enable_execution_reporting=True,
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
        ws_url=os.getenv("THENVOI_WS_URL"),
        rest_url=os.getenv("THENVOI_REST_URL"),
    )

    logger.info("Cost Agent running...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
