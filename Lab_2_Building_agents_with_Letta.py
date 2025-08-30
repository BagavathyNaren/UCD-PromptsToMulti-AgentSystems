#!/usr/bin/env python
# coding: utf-8

# ======================================
# Lab 3: Building Agents with Memory
# ======================================

from letta_client import Letta

# Initialize Letta client
client = Letta(base_url="http://localhost:8283")
# Or use API key if hosted:
#client = Letta(token="LETTA_API_KEY")


# Utility function for printing messages
def print_message(message):
    if message.message_type == "reasoning_message":
        print("🧠 Reasoning: " + message.reasoning)
    elif message.message_type == "assistant_message":
        print("🤖 Agent: " + message.content)
    elif message.message_type == "tool_call_message":
        print("🔧 Tool Call: " + message.tool_call.name + "\n" + message.tool_call.arguments)
    elif message.message_type == "tool_return_message":
        print("🔧 Tool Return: " + message.tool_return)
    elif message.message_type == "user_message":
        print("👤 User Message: " + message.content)


# ================================
# Section 1: Creating the agent
# ================================

agent_state = client.agents.create(
    name="simple_agent",
    memory_blocks=[
        {
            "label": "human",
            "value": "My name is Charles",
            "limit": 10000  # character limit
        },
        {
            "label": "persona",
            "value": "You are a helpful assistant and you always use emojis"
        }
    ],
    model="openai/gpt-4o-mini-2024-07-18",
    embedding="openai/text-embedding-3-small"
)

# ================================
# Send a message to the agent
# ================================

response = client.agents.messages.create(
    agent_id=agent_state.id,
    messages=[
        {
            "role": "user",
            "content": "hows it going????"
        }
    ]
)

for message in response.messages:
    print_message(message)

# Print usage information
print("\n📊 Usage Stats:")
print("Completion Tokens:", response.usage.completion_tokens)
print("Prompt Tokens:", response.usage.prompt_tokens)
print("Step Count:", response.usage.step_count)

# Print agent system prompt
print("\n🧾 Agent System Prompt:")
print(agent_state.system)

# Print agent tools
print("\n🔧 Tools:")
print([t.name for t in agent_state.tools])

# Print memory blocks
print("\n🧠 Memory Blocks:")
print(agent_state.memory)

# Print all messages
print("\n🧾 Conversation History:")
for message in client.agents.messages.list(agent_id=agent_state.id):
    print_message(message)

# List passages (archival memory)
print("\n📚 Archival Memory (Passages):")
passages = client.agents.passages.list(agent_id=agent_state.id)
print(passages)

# ================================
# Update Memory
# ================================

# Correct name
response = client.agents.messages.create(
    agent_id=agent_state.id,
    messages=[
        {
            "role": "user",
            "content": "my name actually Sarah "
        }
    ]
)
print("\n🧠 Name Update:")
for message in response.messages:
    print_message(message)

# Check memory block
updated_human = client.agents.blocks.retrieve(
    agent_id=agent_state.id,
    block_label="human"
)
print("\n📥 Updated 'human' Block Value:", updated_human.value)

# ================================
# Save info to archival memory
# ================================

response = client.agents.messages.create(
    agent_id=agent_state.id,
    messages=[
        {
            "role": "user",
            "content": "Save the information that 'bob loves cats' to archival"
        }
    ]
)
print("\n💾 Save to Archival:")
for message in response.messages:
    print_message(message)

# Confirm new archival passages
passages = client.agents.passages.list(agent_id=agent_state.id)
print("\n📚 Archival Passages After Save:")
print([p.text for p in passages])

# ================================
# Explicitly Create Archival Entry
# ================================

client.agents.passages.create(
    agent_id=agent_state.id,
    text="Bob's loves boston terriers"
)

# Search archival
response = client.agents.messages.create(
    agent_id=agent_state.id,
    messages=[
        {
            "role": "user",
            "content": "What animals do I like? Search archival."
        }
    ]
)
print("\n🔍 Archival Search Response:")
for message in response.messages:
    print_message(message)
