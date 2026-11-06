

# THIS CODE WORKS FOR HARDCODE RESPONSE DATA FROM CODE FILE
# import os

# import psycopg
# from dotenv import load_dotenv

# load_dotenv()


# def get_connection():
#     """Connect to the local InsightAI PostgreSQL database."""
#     return psycopg.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         port=int(os.getenv("DB_PORT", "5432")),
#         dbname=os.getenv("DB_NAME", "insightai_db"),
#         user=os.getenv("DB_USER", "insightai_user"),
#         password=os.getenv("DB_PASSWORD"),
#     )


# def initialize_database():
#     """Create the conversation table if it doesn't exist."""
#     with get_connection() as connection:
#         connection.execute("""
#             CREATE TABLE IF NOT EXISTS app.chat_messages (
#                 id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#                 role VARCHAR(20) NOT NULL
#                     CHECK (role IN ('user', 'assistant')),
#                 message TEXT NOT NULL,
#                 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
#             );
#         """)


# def save_message(role: str, message: str):
#     """Save a user or assistant message."""
#     if role not in ("user", "assistant"):
#         raise ValueError("role must be 'user' or 'assistant'")

#     with get_connection() as connection:
#         connection.execute(
#             """
#             INSERT INTO app.chat_messages (role, message)
#             VALUES (%s, %s)
#             """,
#             (role, message),
#         )


# def get_recent_messages(limit: int = 20):
#     """Return recent messages in chronological order."""
#     if limit < 1:
#         raise ValueError("limit must be at least 1")

#     with get_connection() as connection:
#         rows = connection.execute(
#             """
#             SELECT role, message, created_at
#             FROM app.chat_messages
#             ORDER BY id DESC
#             LIMIT %s
#             """,
#             (limit,),
#         ).fetchall()

#     return list(reversed(rows))

#NEW CODE FOR HARDCODE RESPONSE DATA FROM DATABASE



import os
import re

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Connect to the InsightAI PostgreSQL database."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "insightai_db"),
        user=os.getenv("DB_USER", "insightai_user"),
        password=os.getenv("DB_PASSWORD"),
    )


def normalize_question(text: str) -> str:
    """Normalize a question for consistent database lookup."""
    text = text.strip().lower()
    text = re.sub(r"[!?,۔؟.]+", " ", text)
    return " ".join(text.split())


def initialize_database():
    """Create the tables and insert initial answer data."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS app.chat_messages (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                role VARCHAR(20) NOT NULL
                    CHECK (role IN ('user', 'assistant')),
                message TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS app.answers (
                question_key TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
        """)

        sample_answers = [
            (
                "salam",
                "salam",
                "وعلیکم السلام! آپ کیسے ہیں؟",
            ),
            (
                "hello",
                "hello",
                "Hello! Welcome to InsightAI.",
            ),
            (
                "what is your name",
                "what is your name",
                "I am InsightAI, an Urdu NLP assistant.",
            ),
            (
                "help",
                "help",
                "ضرور! بتائیں آپ کو کس چیز میں مدد چاہیے؟",
            ),
            (
                "آپ کون ہو",
                "آپ کون ہو",
                "میں InsightAI ہوں، ایک اردو NLP اسسٹنٹ۔",
            ),
        ]

        with connection.cursor() as cursor:
            cursor.executemany(
            """
            INSERT INTO app.answers (question_key, question, answer)
            VALUES (%s, %s, %s)
            ON CONFLICT (question_key) DO NOTHING;
            """,
            sample_answers,
        )


def get_response(question: str) -> str:
    """Retrieve a saved answer from PostgreSQL."""
    question_key = normalize_question(question)

    with get_connection() as connection:
        result = connection.execute(
            """
            SELECT answer
            FROM app.answers
            WHERE question_key = %s;
            """,
            (question_key,),
        ).fetchone()

    if result:
        return result[0]

    return (
        "معذرت، مجھے اس سوال کا جواب ڈیٹا بیس میں نہیں ملا۔ "
        "براہ کرم دوسرا سوال پوچھیں۔"
    )


def add_answer(question: str, answer: str):
    """Add a new answer or update an existing one."""
    question_key = normalize_question(question)

    if not question_key or not answer.strip():
        raise ValueError("Question and answer cannot be empty.")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO app.answers (question_key, question, answer)
            VALUES (%s, %s, %s)
            ON CONFLICT (question_key)
            DO UPDATE SET
                question = EXCLUDED.question,
                answer = EXCLUDED.answer;
            """,
            (question_key, question.strip(), answer.strip()),
        )


def save_message(role: str, message: str):
    """Save a conversation message separately from answer data."""
    if role not in ("user", "assistant"):
        raise ValueError("role must be 'user' or 'assistant'")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO app.chat_messages (role, message)
            VALUES (%s, %s);
            """,
            (role, message),
        )
