
from database import get_connection


class SourceService:

    VALID_CATEGORIES = [
        "Customers",
        "Competitors",
        "Market",
        "Internal Intelligence"
    ]

    def add_source(self, company_id, name, url, category, reason):
        """Add a source as pending approval."""

        if category not in self.VALID_CATEGORIES:
            raise ValueError("Invalid source category.")

        if not name or not url or not reason:
            raise ValueError("Name, URL, and reason are required.")

        url = url.strip().rstrip("/")
        name = name.strip()
        reason = reason.strip()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id FROM sources
                WHERE company_id = ?
                AND RTRIM(url, '/') = ?
                """,
                (company_id, url)
            )

            if cursor.fetchone():
                return None

            cursor.execute(
                """
                INSERT INTO sources (
                    company_id,
                    name,
                    url,
                    category,
                    reason,
                    approved
                )
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (company_id, name, url, category, reason)
            )

            source_id = cursor.lastrowid
            connection.commit()
            return source_id

        finally:
            connection.close()

    def approve_source(self, source_id):
        """Approve a pending source."""

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE sources
                SET approved = 1
                WHERE id = ?
                """,
                (source_id,)
            )

            updated = cursor.rowcount > 0
            connection.commit()
            return updated

        finally:
            connection.close()

    def reject_source(self, source_id):
        """Move a source back to pending approval."""

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE sources
                SET approved = 0
                WHERE id = ?
                """,
                (source_id,)
            )

            updated = cursor.rowcount > 0
            connection.commit()
            return updated

        finally:
            connection.close()

    def delete_source(self, source_id):
        """Permanently delete a source."""

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM sources WHERE id = ?",
                (source_id,)
            )

            deleted = cursor.rowcount > 0
            connection.commit()
            return deleted

        finally:
            connection.close()

    def update_source_category(self, source_id, category, reason):
        """Update the category and reason of an existing source."""

        if category not in self.VALID_CATEGORIES:
            raise ValueError("Invalid source category.")

        if not reason:
            raise ValueError("Reason is required.")

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE sources
                SET category = ?, reason = ?
                WHERE id = ?
                """,
                (category, reason.strip(), source_id)
            )

            updated = cursor.rowcount > 0
            connection.commit()
            return updated

        finally:
            connection.close()

    def get_sources(self, company_id, approved_only=False):
        """Get all sources or only approved sources."""

        connection = get_connection()
        cursor = connection.cursor()

        try:
            if approved_only:
                cursor.execute(
                    """
                    SELECT * FROM sources
                    WHERE company_id = ? AND approved = 1
                    ORDER BY id
                    """,
                    (company_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM sources
                    WHERE company_id = ?
                    ORDER BY id
                    """,
                    (company_id,)
                )

            sources = cursor.fetchall()
            return [dict(source) for source in sources]

        finally:
            connection.close()

    def get_pending_sources(self, company_id):
        """Get sources awaiting approval."""

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM sources
                WHERE company_id = ? AND approved = 0
                ORDER BY id
                """,
                (company_id,)
            )

            sources = cursor.fetchall()
            return [dict(source) for source in sources]

        finally:
            connection.close()

    def get_approved_sources(self, company_id):
        """Get only approved sources."""

        return self.get_sources(
            company_id,
            approved_only=True
        )
