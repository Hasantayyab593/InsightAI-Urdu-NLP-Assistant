
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chatbot import detect_intent, get_response


def test_english_greeting():
    assert detect_intent("Hello!") == "greeting"


def test_roman_urdu_greeting():
    assert detect_intent("salam") == "greeting"


def test_urdu_help():
    assert detect_intent("مدد") == "help"


def test_about_assistant():
    assert detect_intent("آپ کون ہیں؟") == "about"


def test_unknown_message_returns_response():
    assert isinstance(get_response("xyzabc"), str)
    assert len(get_response("xyzabc")) > 0
