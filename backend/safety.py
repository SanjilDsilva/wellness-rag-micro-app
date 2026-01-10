def check_safety(query: str) -> bool:
    """
    Returns True if the query is considered unsafe.
    """

    query_lower = query.lower()

    unsafe_keywords = [
        "pregnant",
        "pregnancy",
        "trimester",
        "hernia",
        "glaucoma",
        "high blood pressure",
        "hypertension",
        "recent surgery",
        "heart condition",
        "cardiac",
        "disc problem",
        "slip disc"
    ]

    for keyword in unsafe_keywords:
        if keyword in query_lower:
            return True

    return False
def unsafe_response() -> str:
    return (
        "⚠️ Safety Notice:\n\n"
        "Your question touches on an area that can be risky without personalized guidance.\n\n"
        "Instead of advanced or physically demanding poses, consider gentle practices such as "
        "supine relaxation or mindful breathing.\n\n"
        "Please consult a doctor or a certified yoga therapist before attempting these practices."
    )
