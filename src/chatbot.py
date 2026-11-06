
# import random
# import re


# def normalize_text(text: str) -> str:
#     """Normalize text for basic Urdu and Roman Urdu matching."""
#     text = text.strip().lower()
#     text = re.sub(r"[!?,۔؟.]+", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text


# def detect_intent(text: str) -> str:
#     """Detect a simple conversational intent."""
#     normalized = normalize_text(text)

#     greetings = [
#         "hello", "hi", "hey", "salam", "assalam o alaikum",
#         "assalamu alaikum", "السلام علیکم", "سلام", "ہیلو"
#     ]

#     help_phrases = [
#         "help", "madad", "mujhe madad chahiye",
#         "مدد", "مجھے مدد چاہیے"
#     ]

#     about_phrases = [
#         "who are you", "what are you", "tum kon ho",
#         "aap kon hain", "آپ کون ہیں", "تم کون ہو"
#     ]
#     time_phrases = [
#         "what time is it", "kya waqt hua hai", "abhi kya time hai", "ابھی کیا وقت ہوا ہے", "کیا وقت ہوا ہے"
#     ]
    

#     if any(phrase in normalized for phrase in greetings):
#         return "greeting"

#     if any(phrase in normalized for phrase in help_phrases):
#         return "help"

#     if any(phrase in normalized for phrase in about_phrases):
#         return "about"

#     if any(phrase in normalized for phrase in time_phrases):
#         return "time"

#     return "unknown"


# def get_response(text: str) -> str:
#     """Generate a response based on the detected intent."""
#     intent = detect_intent(text)

#     responses = {
#         # "greeting": [
#         #     "وعلیکم السلام! آپ کیسے ہیں؟",
#         #     "Hello! میں InsightAI ہوں۔ میں آپ کی کیا مدد کر سکتا ہوں؟",
#         #     "سلام! خوش آمدید۔"
#         # ],
#         "help": [
#             "ضرور! بتائیں آپ کو کس چیز میں مدد چاہیے؟",
#             "I am here to help. آپ اپنا سوال اردو یا Roman Urdu میں لکھ سکتے ہیں۔"
#         ],
#         "about": [
#             "میں InsightAI ہوں، ایک ابتدائی اردو NLP conversational assistant۔",
#             "I am InsightAI, a prototype assistant designed to understand simple Urdu and Roman Urdu messages."
#         ],
#         "time": [
#                     "میں InsightAI ہوں، ایک ابتدائی اردو NLP conversational assistant۔",
#                     "6:02 right know, a prototype assistant designed to understand simple Urdu and Roman Urdu messages."
#                 ],
        
#         "unknown": [
#             "معذرت، میں آپ کا سوال سمجھ نہیں سکا۔ براہ کرم اسے دوسرے الفاظ میں لکھیں۔",
#             "میں ابھی سیکھنے کے ابتدائی مرحلے میں ہوں۔ کیا آپ اپنا سوال آسان الفاظ میں پوچھ سکتے ہیں؟"
#         ]
#     }

#     return random.choice(responses[intent])





import os

import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

SYSTEM_PROMPT = """
You are InsightAI, a helpful AI assistant.

Your capabilities:
- Understand English, Urdu, and Roman Urdu.
- Answer in the language used by the user.
- Explain difficult topics in simple language.
- Help with programming, education, and general questions.
- Be friendly, clear, and accurate.
- If you do not know something, say so.
"""


def get_response(text: str) -> str:
    """Generate a response using Qwen through Ollama."""

    if not text or not text.strip():
        return "Please enter a question."

    try:
        result = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return result.message.content.strip()

    except ollama.ResponseError as error:
        return f"AI model error: {error}"

    except Exception as error:
        return (
            "Could not connect to Ollama. "
            "Please check that Ollama is running and "
            f"that {MODEL_NAME} is installed. Details: {error}"
        )
