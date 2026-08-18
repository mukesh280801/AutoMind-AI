from services.query_rewrite_service import rewrite_question
from services.graph.state import AutoMindState


def rewrite_node(
    state: AutoMindState,
) -> AutoMindState:

    question = state.get(
        "question",
        "",
    ).strip()

    question_lower = question.lower()

    # =========================================================
    # PROJECT QUESTIONS
    # =========================================================

    project_keywords = [
        "project",
        "projects",
        "developed",
        "develop",
        "built",
        "build",
        "created",
        "implemented",
        "experience",
    ]

    is_project_question = any(
        keyword in question_lower
        for keyword in project_keywords
    )

    if is_project_question:

        rewritten_question = (
            "projects project experience "
            "Attention U-Net based Brain Tumor Segmentation "
            "Explainable AI "
            "Lung Disease Detection and Recommendation System "
            "CNN chest X-ray classification "
            "Disease Classification and Recommendation System "
            "Technologies Used "
            "PyTorch OpenCV "
            "ONNX Grad-CAM"
        )

    else:

        rewritten_question = rewrite_question(
            question
        )

    return {
        **state,
        "rewritten_question": rewritten_question,
        "stage": "rewrite",
    }