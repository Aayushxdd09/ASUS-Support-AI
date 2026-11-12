
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Send a test question
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain what a laptop battery does in two sentences."
        }
    ]
)

# Print AI response
print(response.choices[0].message.content)
