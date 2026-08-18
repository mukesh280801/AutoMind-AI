import pytest
import requests


API_URL = "http://127.0.0.1:8000/api/chat"


TEST_QUESTIONS = [
    # Basic factual questions
    "What are Mukesh's skills?",
    "What degree is Mukesh pursuing?",
    "Where did Mukesh complete his bachelor's degree?",

    # Projects
    "What projects has Mukesh worked on?",
    "Tell me about Mukesh's brain tumor segmentation project.",
    "Tell me about Mukesh's lung disease detection project.",

    # Technical details
    "What technologies did Mukesh use for the brain tumor project?",
    "What performance did Mukesh achieve in the brain tumor project?",
    "What model was used for lung disease detection?",

    # Certifications / additional information
    "What certifications does Mukesh have?",
    "What are Mukesh's areas of interest?",

    # Out-of-context question
    "What is Mukesh's favorite programming language?",
]


@pytest.mark.parametrize("question", TEST_QUESTIONS)
def test_question(question):
    response = requests.post(
        API_URL,
        json={
            "question": question
        },
        timeout=120,
    )

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    print("\nSTATUS:")
    print(response.status_code)

    print("\nANSWER:")
    print(response.text)

    print("=" * 70)

    assert response.status_code == 200