
from database import get_connection


class CompanyInterviewService:

    QUESTIONS = [
        "What does your company do?",
        "What products or services does your company offer?",
        "Who are your ideal customers?",
        "Which industries or markets do you serve?",
        "What makes your company different from competitors?",
        "Who are your main competitors?",
        "What are your company's biggest business goals?",
        "What are the biggest challenges your company currently faces?",
        "Which market trends could affect your company?",
        "What important developments should Signal Stack monitor?"
    ]

    def get_questions(self):
        return self.QUESTIONS

    def save_answer(self, company_id, question, answer):

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty.")

        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO interview_answers
                (company_id, question, answer)
                VALUES (?, ?, ?)
                """,
                (company_id, question, answer.strip())
            )

            connection.commit()
            return True

        finally:
            connection.close()

    def get_answers(self, company_id):

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT id, question, answer, created_at
                FROM interview_answers
                WHERE company_id = ?
                ORDER BY id ASC
                """,
                (company_id,)
            ).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()

    def get_progress(self, company_id):

        answers = self.get_answers(company_id)

        answered_questions = {
            item["question"]
            for item in answers
            if item["answer"] and item["answer"].strip()
        }

        total_questions = len(self.QUESTIONS)
        answered = sum(
            question in answered_questions
            for question in self.QUESTIONS
        )

        return {
            "answered": answered,
            "total": total_questions,
            "remaining": total_questions - answered
        }

    def update_answer(self, answer_id, new_answer):

        if not new_answer or not new_answer.strip():
            raise ValueError("Answer cannot be empty.")

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE interview_answers
                SET answer = ?
                WHERE id = ?
                """,
                (new_answer.strip(), answer_id)
            )

            connection.commit()
            return cursor.rowcount > 0

        finally:
            connection.close()
