from services.llm import llm


def rewrite_question(
    history_text: str,
    question: str
):

    prompt = f"""
You are a query rewriting assistant.

Your task is ONLY to make references explicit.

Examples:

What is C++?
Explain it briefly.
→ Explain C++ briefly.

Tell me about usage guidelines.
Summarize them.
→ Summarize the usage guidelines.

Rules:

1. Keep original wording whenever possible.
2. Resolve pronouns like:
    it, this, that, they, them, these, those.
3. Do NOT expand definitions.
4. Do NOT add new information.
5. Do NOT answer the question.
6. Return only the rewritten question.

Conversation:
{history_text}

Question:
{question}
"""

    result = llm.invoke(prompt)

    return result.content.strip()