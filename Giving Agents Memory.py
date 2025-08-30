"""

LLMs Do Not Have Memory

When we are building an Agent, we need it to remember its actions and the result of those actions. 

For example, if it tries to create a calendar event for a meeting and the API call fails due to an incorrect

 parameter value that it provided, we want it to remember that the API call failed and why. 
 
 This way, it can correct the mistake and try again. If we have a complex task that we break down into multiple steps,
  
we need the Agent to remember the results of each step to ensure that it can continue the task from where it left off. 

Memory is crucial for Agents.

LLMs Do Not Have Memory

When interacting with an LLM, the model does not inherently “remember” previous conversations or responses. 

Every time you call the model, it generates a response based solely on the information provided in the messages parameter.

If previous context is not included in the messages, the model will not have any knowledge of it.

This means that to simulate continuity in a conversation, you must explicitly pass all relevant prior 

messages (including system, user, and assistant roles) in the messages list for each request.

"""

from dotenv import load_dotenv
import os
from litellm import completion
from typing import List, Dict
import base64

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Example 1: Missing Context in the Prompt

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4.1-mini",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


# messages = [
#     {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
#     {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
# ]

# response = generate_response(messages)
# print(response)

# # Second query without including the previous response
# messages = [
#     {"role": "user", "content": "Update the function to include documentation."}
# ]

# response = generate_response(messages)
# print(response)

# Example 2: Including Previous Responses for Continuity

messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# We are going to make this verbose so it is clear what
# is going on. In a real application, you would likely
# just append to the messages list.
messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."},
   
   # Here is the assistant's response from the previous step
   # with the code. This gives it "memory" of the previous
   # interaction.
   {"role": "assistant", "content": response},
      # Now, we can ask the assistant to update the function
   {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)


"""

Explanation: By including the assistant’s previous response in the messages, the model can maintain context and provide an appropriate response to the follow-up question.

Key Takeaways

No Inherent Memory: The LLM has no knowledge of past interactions unless explicitly provided in the current prompt (via messages).
Provide Full Context: To simulate continuity in a conversation, include all relevant messages (both user and assistant responses) in the messages parameter.
Role of Assistant Messages: Adding previous responses as assistant messages allows the model to maintain a coherent conversation and build on earlier exchanges. For an agent, this will allow it to remember what actions, such as API calls, it took in the past.
Memory Management: We can control what the LLM remembers or does not remember by managing what messages go into the conversation. Causing the LLM to forget things can be a powerful tool in some circumstances, such as when we need to break a pattern of poor responses from an Agent.
Why This Matters

Understanding the stateless nature of LLMs is crucial for designing agents that rely on multi-turn conversations with their environment. Developers must explicitly manage and provide context to ensure the model generates accurate and relevant responses.

"""