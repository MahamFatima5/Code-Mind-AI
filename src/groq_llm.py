import os
from groq import Groq


class GroqLLM:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found.")

        self.client = Groq(api_key=api_key)

        # llama-3.3-70b-versatile was decommissioned by Groq on 2026-08-16.
        # Defaulting to the recommended replacement; override via env var
        # if you want a different model.
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    def generate_answer(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        return completion.choices[0].message.content
