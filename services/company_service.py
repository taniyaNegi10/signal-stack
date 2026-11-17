
from database import get_connection


class CompanyService:

    def add_company(self, name, website, industry):
        """Add a company only if its website is not already registered."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM companies WHERE website = ?",
            (website,)
        )

        existing_company = cursor.fetchone()

        if existing_company:
            connection.close()
            return None

        cursor.execute(
            """
            INSERT INTO companies (name, website, industry)
            VALUES (?, ?, ?)
            """,
            (name, website, industry)
        )

        connection.commit()
        company_id = cursor.lastrowid
        connection.close()

        return company_id

    def get_all_companies(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM companies")
        companies = cursor.fetchall()

        connection.close()
        return companies

    def get_company(self, company_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM companies WHERE id = ?",
            (company_id,)
        )

        company = cursor.fetchone()
        connection.close()

        return company
