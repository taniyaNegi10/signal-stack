
import json
from database import get_connection


class ResearchStorageService:

    def save_research(self, company_id, research_data):

        if research_data.get("status") != "success":
            raise ValueError("Cannot save unsuccessful research.")

        url = research_data["url"]
        title = research_data.get("title", "")
        description = research_data.get("description", "")

        headings = json.dumps(
            research_data.get("headings", [])
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            existing = cursor.execute(
                """
                SELECT rowid
                FROM company_research
                WHERE company_id = ? AND url = ?
                ORDER BY researched_at DESC
                LIMIT 1
                """,
                (company_id, url)
            ).fetchone()

            if existing is not None:

                research_row_id = existing[0]

                cursor.execute(
                    """
                    UPDATE company_research
                    SET title = ?,
                        description = ?,
                        headings = ?,
                        researched_at = CURRENT_TIMESTAMP
                    WHERE rowid = ?
                    """,
                    (
                        title,
                        description,
                        headings,
                        research_row_id
                    )
                )

                action = "updated"

            else:

                cursor.execute(
                    """
                    INSERT INTO company_research (
                        company_id,
                        url,
                        title,
                        description,
                        headings,
                        researched_at
                    )
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (
                        company_id,
                        url,
                        title,
                        description,
                        headings
                    )
                )

                action = "inserted"

            connection.commit()
            return action

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def get_research(self, company_id):

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT *
                FROM company_research
                WHERE company_id = ?
                ORDER BY researched_at DESC
                """,
                (company_id,)
            ).fetchall()

            results = []

            for row in rows:
                item = dict(row)

                item["headings"] = json.loads(
                    item["headings"] or "[]"
                )

                results.append(item)

            return results

        finally:
            connection.close()
