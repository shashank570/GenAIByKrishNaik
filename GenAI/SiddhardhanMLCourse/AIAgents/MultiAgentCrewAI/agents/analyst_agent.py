from crewai import Agent, LLM
from tools.stock_research_tool import get_stock_price


llm = LLM(
    model = "groq/llama-3.3-70b-versatile",
    temperature=0.0
)

analyst_agent = Agent(
    role = "Financial Market Analyst", # Defines who the agent is
    goal = ("Perform in-depth evaluations of publicly traded stocks using real-time data, "
           "identifying trends, performance insights, and key financial "
           "signals to support decision-making."), # Defines what the agent should achieve
    backstory = ("You are a veteran financial analyst with deep expertise in interpreting stock market data, "
                 "technical trends, and fundamentals. You specialize in producing well-structured reports that evaluate "
                 "stock performance using live market indicators."), # This shapes how the agent thinks
    llm = llm,
    tools = [get_stock_price],
    verbose = True
)