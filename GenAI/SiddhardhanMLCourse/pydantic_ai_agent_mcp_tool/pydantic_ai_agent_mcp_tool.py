import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()

# update the path with your machine details
# same command as we added in claude_desktop_config.json
server = MCPServerStdio(
    command="/Users/shashankshukla/.local/bin/uv",
    args=[
        "--directory",
        "/Users/shashankshukla/Downloads/GenAIByKrishNaik/GenAI/SiddhardhanMLCourse/mcp_server_basics_with_uv",
        "run",
        "weather.py",
    ],
)

agent = Agent(
    model="groq:llama-3.1-8b-instant",
    toolsets=[server],
)

async def main():
    async with agent:
        result = await agent.run("What is the current weather in Chennai?")
        # result = await agent.run(
        #     "What is the current stock price of Tesla?")  # this won't be answered with the weather tool
    print(result)


if __name__ == "__main__":
    asyncio.run(main())