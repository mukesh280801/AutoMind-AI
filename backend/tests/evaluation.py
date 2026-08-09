import requests
import json
import time


API_URL = "http://127.0.0.1:8000/api/chat"


TEST_CASES = [
    {
        "question": "What programming languages does Mukesh know?",
        "expected_keywords": ["Python", "SQL"],
        "should_find": True,
    },
    {
        "question": "What projects has Mukesh worked on?",
        "expected_keywords": [
            "Brain Tumor",
            "Lung Disease",
        ],
        "should_find": True,
    },
    {
        "question": "Which project used Attention U-Net?",
        "expected_keywords": [
            "Brain Tumor",
            "Attention U-Net",
        ],
        "should_find": True,
    },
    {
        "question": "What is Mukesh's favorite programming language?",
        "expected_keywords": [
            "couldn't find",
        ],
        "should_find": False,
    },
]


def run_test(test_case):

    question = test_case["question"]

    start_time = time.perf_counter()

    response = requests.post(
        API_URL,
        json={
            "question": question
        },
        timeout=120,
    )

    elapsed = (
        time.perf_counter() - start_time
    ) * 1000

    if response.status_code != 200:
        return {
            "question": question,
            "passed": False,
            "status": response.status_code,
            "answer": response.text,
            "time_ms": round(elapsed, 2),
        }

    data = response.json()

    answer = data.get(
        "answer",
        ""
    )

    answer_lower = answer.lower()

    expected_keywords = test_case[
        "expected_keywords"
    ]

    if test_case["should_find"]:

        passed = all(
            keyword.lower() in answer_lower
            for keyword in expected_keywords
        )

    else:

        passed = any(
            keyword.lower() in answer_lower
            for keyword in expected_keywords
        )

    return {
        "question": question,
        "passed": passed,
        "status": response.status_code,
        "answer": answer,
        "time_ms": round(elapsed, 2),
        "cached": data.get("cached", False),
    }


def main():

    print("\n")
    print("=" * 70)
    print("AUTOMIND AI - V1 EVALUATION")
    print("=" * 70)

    results = []

    for index, test_case in enumerate(
        TEST_CASES,
        start=1
    ):

        print(
            f"\nRunning test {index}/{len(TEST_CASES)}..."
        )

        result = run_test(test_case)

        results.append(result)

        print("\nQuestion:")
        print(result["question"])

        print("\nAnswer:")
        print(result["answer"])

        print("\nStatus:")
        print(result["status"])

        print("\nCached:")
        print(result.get("cached", False))

        print("\nTime:")
        print(
            f"{result['time_ms']} ms"
        )

        print("\nResult:")
        print(
            "PASS" if result["passed"]
            else "FAIL"
        )

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    total = len(results)

    accuracy = (
        passed / total * 100
        if total > 0
        else 0
    )

    print("\n")
    print("=" * 70)
    print("V1 EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()