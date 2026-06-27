from smolagents import CodeAgent, LiteLLMModel, tool, InferenceClientModel
from huggingface_hub import login
import os
from tool import query_fact_orders

# login()



model = LiteLLMModel(model_id="groq/llama-3.3-70b-versatile",
                     api_key=os.environ.get("GROQ_API_KEY"))  # Uses a default model

instructions = """
You are a friendly business intelligence assistant.

RULES:
1. Always call query_fact_orders tool first to get data
2. Use pandas code to calculate the exact answer
3. Never show code or technical details in your final answer
4. Always respond in simple business language
5. Format numbers nicely e.g. $1,234.56 or 1,234 units
6. End with a clear one line summary
"""

agent = CodeAgent(
    tools = [query_fact_orders],
    model=model,
    additional_authorized_imports=["pandas","json", "io"],
    verbosity_level = 2,
    max_steps = 5
    # system_prompt=instructions
)


if __name__ == "__main__":
    questions = [
        "Who is the customer with highest spending ?"
        "List avergage revenue for all categories "
        ""
    ]

    for each_question in questions:
        print(f"{"-"*50}")
        print(f"{each_question}")
        print(f"{'='*50}")

        try:
            result = agent.run(
                f"{instructions}\n\nQuestion: {each_question}"
            )

            print("result")
        except Exception as e:
            print("fError ....{str(e)}")
    
    print("question answered :)")
