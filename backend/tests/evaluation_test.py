import requests
import json


# =========================================================
# Configuration
# =========================================================

BASE_URL = "http://127.0.0.1:8000"

CHAT_URL = f"{BASE_URL}/api/v2/chat"


# =========================================================
# Evaluation Dataset
# =========================================================

TEST_CASES = [

    # =====================================================
    # AUTOMOTIVE - CAN
    # =====================================================

    {
        "name": "CAN maximum bus length",
        "question": "What is the maximum CAN bus length at 1 Mbit/s?",
        "expected": "40 m",
        "type": "automotive",
    },

    {
        "name": "CAN automotive characteristics",
        "question": "What are the main characteristics of CAN in automotive applications?",
        "expected": "CAN",
        "type": "automotive",
    },

    {
        "name": "CAN bit rate",
        "question": "What bit rate is mentioned for CAN?",
        "expected": "1 Mbit/s",
        "type": "automotive",
    },

    {
        "name": "CAN bus length",
        "question": "How long can the CAN bus be at 1 Mbit/s?",
        "expected": "40 m",
        "type": "automotive",
    },


    # =====================================================
    # AUTOMOTIVE - BLUETOOTH
    # =====================================================

    {
        "name": "Bluetooth automotive applications",
        "question": "What is Bluetooth used for in automotive applications?",
        "expected": "Bluetooth",
        "type": "automotive",
    },

    {
        "name": "Bluetooth document retrieval",
        "question": "What does the document discuss about Bluetooth in automotive applications?",
        "expected": "Bluetooth",
        "type": "automotive",
    },

    {
        "name": "Automotive networking",
        "question": "What wireless technology is discussed in the automotive document?",
        "expected": "Bluetooth",
        "type": "automotive",
    },


    # =====================================================
    # PROJECT KNOWLEDGE
    # =====================================================

    {
        "name": "Lung disease accuracy",
        "question": "What is the accuracy of the Lung Disease Detection project?",
        "expected": "96%",
        "type": "project",
    },

    {
        "name": "Lung disease F1 score",
        "question": "What is the F1-score of the Lung Disease Detection project?",
        "expected": "0.93",
        "type": "project",
    },

    {
        "name": "Attention U-Net Dice score",
        "question": "What is the Dice Score of the Attention U-Net project?",
        "expected": "98.7%",
        "type": "project",
    },

    {
        "name": "Attention U-Net IoU",
        "question": "What is the IoU score of the Attention U-Net project?",
        "expected": "97.9%",
        "type": "project",
    },

    {
        "name": "Project list",
        "question": "What projects are mentioned in the resume?",
        "expected": "AutoMind AI",
        "type": "project",
    },


    # =====================================================
    # GROUNDING / HALLUCINATION
    # =====================================================

    {
        "name": "Unsupported vehicle engine displacement",
        "question": "What is the engine displacement of the vehicle in the ADAS project?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },

    {
        "name": "Unsupported vehicle mileage",
        "question": "What is the fuel mileage of the vehicle in the ADAS project?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },

    {
        "name": "Unsupported battery capacity",
        "question": "What is the battery capacity of the vehicle in the ADAS project?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },

    {
        "name": "Unsupported vehicle price",
        "question": "What is the price of the vehicle used in the ADAS project?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },


    # =====================================================
    # GENERAL DOCUMENT GROUNDING
    # =====================================================

    {
        "name": "Unsupported employee information",
        "question": "What is the employee ID mentioned in the documents?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },

    {
        "name": "Unsupported company revenue",
        "question": "What is the annual revenue of the company mentioned in the documents?",
        "expected": "I couldn't find that information in the uploaded documents.",
        "type": "grounding",
    },


    # =====================================================
    # CROSS-DOMAIN RETRIEVAL
    # =====================================================

    {
        "name": "Automotive and project retrieval",
        "question": "Does the uploaded knowledge base contain automotive information?",
        "expected": "automotive",
        "type": "automotive"
    },

    {
        "name": "Document knowledge retrieval",
        "question": "What topics are covered by the uploaded documents?",
        "expected": "automotive",
        "type": "grounding"
    },
]


# =========================================================
# Run One Test
# =========================================================

def run_test(test_case, index):

    print()
    print("=" * 70)
    print(f"TEST {index}: {test_case['name']}")
    print("=" * 70)

    print(f"Question : {test_case['question']}")

    payload = {
        "question": test_case["question"],
        "thread_id": f"evaluation-test-{index}",
    }

    try:

        response = requests.post(
            CHAT_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "answer",
            "",
        )

        sources = data.get(
            "sources",
            [],
        )

        expected = test_case["expected"]

        # =================================================
        # Evaluation
        # =================================================

        passed = expected.lower() in answer.lower()

        print()
        print(f"Answer   : {answer}")
        print(f"Expected : {expected}")
        print(f"Sources  : {len(sources)}")

        if passed:
            print("Result   : PASS")
        else:
            print("Result   : FAIL")

        return {
            "name": test_case["name"],
            "passed": passed,
            "answer": answer,
            "sources": len(sources),
        }

    except Exception as exc:

        print()
        print(f"Result   : ERROR")
        print(f"Error    : {exc}")

        return {
            "name": test_case["name"],
            "passed": False,
            "answer": "",
            "sources": 0,
        }


# =========================================================
# Main Evaluation
# =========================================================

def main():

    print()
    print("=" * 70)
    print("AUTOMIND AI - V2 EVALUATION")
    print("=" * 70)

    results = []

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        result = run_test(
            test_case,
            index,
        )

        results.append(result)

    # =====================================================
    # Summary
    # =====================================================

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    failed = total - passed

    accuracy = (
        (passed / total) * 100
        if total > 0
        else 0
    )

    print()
    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print(f"Accuracy    : {accuracy:.2f}%")

    print()
    print("Test Results:")

    for result in results:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"- {status}: "
            f"{result['name']} "
            f"(sources={result['sources']})"
        )

    # =====================================================
    # Save JSON Report
    # =====================================================

    report = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "accuracy": accuracy,
        "results": results,
    }

    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print(
        "Report saved: evaluation_results.json"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    main()