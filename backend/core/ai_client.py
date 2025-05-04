from groq import Groq
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

client = Groq()

async def check_if_beats(seed: str, guess: str, persona: str) -> str:
    prompt = f"Does '{guess}' beat '{seed}'? Answer YES or NO only."
    models = ["llama3-70b-8192", "mistral-saba-24b", "gemma2-9b-it"]
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a {persona} judge. Decide if guess beats seed. Reply YES or NO."
                    },
                    {
                        "role": "user",
                        "content": f"{guess} vs {seed}"
                    }
                ],
                max_tokens=1,
                temperature=0
            )
            
            # Print Usage Information
            usage = {
                "Model": model,
                "Prompt Tokens": response.usage.prompt_tokens,
                "Completion Tokens": response.usage.completion_tokens,
                "Total Tokens": response.usage.total_tokens,
                "Time": response.usage.total_time,
                "Content": response.choices[0].message.content.strip().upper()
            }
            
            logging.info(f"Usage for model {model}: {usage}")

            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"Error with model {model}: {e}")
            
    return "NO"  # Default to NO if all models fail