
import json

from database import get_connection


class SourceQualityStorageService:

    def save_evaluation(self, source_id, company_id, evaluation):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO source_quality (
                source_id,
                company_id,
                score,
                accessibility_score,
                relevance_score,
                credibility_score,
                category_fit_score,
                quality,
                recommendation,
                reasons
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(source_id)
            DO UPDATE SET
                company_id = excluded.company_id,
                score = excluded.score,
                accessibility_score = excluded.accessibility_score,
                relevance_score = excluded.relevance_score,
                credibility_score = excluded.credibility_score,
                category_fit_score = excluded.category_fit_score,
                quality = excluded.quality,
                recommendation = excluded.recommendation,
                reasons = excluded.reasons,
                evaluated_at = CURRENT_TIMESTAMP
        """, (
            source_id,
            company_id,
            evaluation["score"],
            evaluation["accessibility_score"],
            evaluation["relevance_score"],
            evaluation["credibility_score"],
            evaluation["category_fit_score"],
            evaluation["quality"],
            evaluation["recommendation"],
            json.dumps(evaluation["reasons"])
        ))

        connection.commit()
        connection.close()

        return True

    def get_evaluation(self, source_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM source_quality
            WHERE source_id = ?
        """, (source_id,))

        result = cursor.fetchone()
        connection.close()

        if result is None:
            return None

        evaluation = dict(result)
        evaluation["reasons"] = json.loads(
            evaluation["reasons"] or "[]"
        )

        return evaluation

    def get_company_evaluations(self, company_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT sq.*, s.name AS source_name, s.url, s.category
            FROM source_quality sq
            JOIN sources s ON sq.source_id = s.id
            WHERE sq.company_id = ?
            ORDER BY sq.score DESC
        """, (company_id,))

        results = cursor.fetchall()
        connection.close()

        evaluations = []

        for result in results:
            evaluation = dict(result)

            evaluation["reasons"] = json.loads(
                evaluation["reasons"] or "[]"
            )

            evaluations.append(evaluation)

        return evaluations
