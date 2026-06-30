from datetime import datetime

from IPython.display import Image, display
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from utils import show_prompt, stream_agent, format_messages

from src.file_tools import ls, read_file, write_file
from src.prompts import (
    FILE_USAGE_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
)
from src.research_tools import tavily_search, think_tool, get_today_str
from src.state import DeepAgentState
from src.task_tool import _create_task_tool
from src.todo_tools import write_todos, read_todos

# Create agent using unified initialization protocols
model = init_chat_model(model="anthropic:claude-sonnet-4-20250514", temperature=0.0)

# Execution Constraints
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Tools Allocations
sub_agent_tools = [tavily_search, think_tool]
built_in_tools = [ls, read_file, write_file, write_todos, read_todos, think_tool]

# Configure specialized sub-agent metadata profiles
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": ["tavily_search", "think_tool"],
}

# Create task tool to isolate execution blocks within sub-agents
task_tool = _create_task_tool(
    sub_agent_tools, [research_sub_agent], model, DeepAgentState
)

delegation_tools = [task_tool]
all_tools = sub_agent_tools + built_in_tools + delegation_tools  

# Construct System Instruction Profiles
SUBAGENT_INSTRUCTIONS = SUBAGENT_USAGE_INSTRUCTIONS.format(
    max_concurrent_research_units=max_concurrent_research_units,
    max_researcher_iterations=max_researcher_iterations,
    date=datetime.now().strftime("%a %b %-d, %Y"),
)

show_prompt(RESEARCHER_INSTRUCTIONS)

INSTRUCTIONS = (
    "# TODO MANAGEMENT\n"
    + TODO_USAGE_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + "# FILE SYSTEM USAGE\n"
    + FILE_USAGE_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + "# SUB-AGENT DELEGATION\n"
    + SUBAGENT_INSTRUCTIONS
)

show_prompt(INSTRUCTIONS)

# ==============================================================================
# APPROACH 1: STANDARD REACT AGENT RUNTIME
# ==============================================================================
react_agent = create_agent(
    model, 
    tools=all_tools, 
    system_prompt=INSTRUCTIONS, 
    state_schema=DeepAgentState
)

# Visualize runtime graph
display(Image(react_agent.get_graph(xray=True).draw_mermaid_png()))

react_result = react_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Give me an overview of Model Context Protocol (MCP).",
            }
        ],
    }
)
format_messages(react_result["messages"])


# ==============================================================================
# APPROACH 2: HIERARCHICAL DEEP AGENT RUNTIME
# ==============================================================================
from deepagents import create_deep_agent

deep_agent = create_deep_agent(
    sub_agent_tools,
    INSTRUCTIONS,
    subagents=[research_sub_agent],
    model=model,
)

# Visualize runtime graph
display(Image(deep_agent.get_graph(xray=True).draw_mermaid_png()))

deep_result = deep_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Give me a very brief overview of Model Context Protocol (MCP).",
            }
        ],
    }
)
format_messages(deep_result["messages"])
