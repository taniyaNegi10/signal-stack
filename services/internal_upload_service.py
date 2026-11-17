
import hashlib
import io
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

from database import get_connection


class InternalUploadService:

    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".pdf", ".txt"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_EXTRACTED_TEXT = 100_000

    def __init__(self):
        self._ensure_table()

    def _ensure_table(self):
        connection = get_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS internal_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                extracted_text TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                extraction_status TEXT DEFAULT 'success',
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(company_id, content_hash),
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        """)

        connection.commit()
        connection.close()

    def _extract_text(self, file_name, file_bytes):
        extension = Path(file_name).suffix.lower()

        if extension == ".txt":
            try:
                return file_bytes.decode("utf-8-sig")
            except UnicodeDecodeError:
                return file_bytes.decode("cp1252")

        if extension == ".pdf":
            reader = PdfReader(io.BytesIO(file_bytes))

            extracted_pages = []

            for page_number, page in enumerate(reader.pages[:100], start=1):
                page_text = page.extract_text() or ""
                extracted_pages.append(
                    f"Page {page_number}\n{page_text}"
                )

            return "\n\n".join(extracted_pages)

        if extension == ".csv":
            dataframe = pd.read_csv(
                io.BytesIO(file_bytes),
                nrows=5000
            )

            return dataframe.to_string(index=False)

        if extension == ".xlsx":
            sheets = pd.read_excel(
                io.BytesIO(file_bytes),
                sheet_name=None,
                nrows=5000,
                engine="openpyxl"
            )

            extracted_sheets = []

            for sheet_name, dataframe in sheets.items():
                extracted_sheets.append(
                    f"Sheet: {sheet_name}\n"
                    f"{dataframe.to_string(index=False)}"
                )

            return "\n\n".join(extracted_sheets)

        raise ValueError("Unsupported file format.")

    def upload_file(self, company_id, uploaded_file):

        file_name = Path(uploaded_file.name).name
        extension = Path(file_name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                "Supported formats: CSV, XLSX, PDF and TXT."
            )

        file_bytes = uploaded_file.getvalue()

        if not file_bytes:
            raise ValueError("The uploaded file is empty.")

        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise ValueError("Maximum file size allowed is 10 MB.")

        content_hash = hashlib.sha256(file_bytes).hexdigest()

        extracted_text = self._extract_text(
            file_name,
            file_bytes
        )

        extracted_text = extracted_text.strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in this file."
            )

        extracted_text = extracted_text[:self.MAX_EXTRACTED_TEXT]

        connection = get_connection()

        try:
            cursor = connection.execute("""
                INSERT INTO internal_documents (
                    company_id,
                    file_name,
                    file_type,
                    file_size,
                    extracted_text,
                    content_hash,
                    extraction_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                company_id,
                file_name,
                extension.replace(".", "").upper(),
                len(file_bytes),
                extracted_text,
                content_hash,
                "success"
            ))

            connection.commit()

            return {
                "success": True,
                "document_id": cursor.lastrowid,
                "file_name": file_name,
                "company_id": company_id,
                "characters_extracted": len(extracted_text)
            }

        except Exception as error:
            connection.rollback()

            if "UNIQUE constraint failed" in str(error):
                raise ValueError(
                    "This file has already been uploaded for this company."
                )

            raise

        finally:
            connection.close()

    def get_documents(self, company_id):

        connection = get_connection()

        try:
            rows = connection.execute("""
                SELECT
                    id,
                    company_id,
                    file_name,
                    file_type,
                    file_size,
                    extraction_status,
                    uploaded_at
                FROM internal_documents
                WHERE company_id = ?
                ORDER BY uploaded_at DESC
            """, (company_id,)).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()

    def get_document_text(self, document_id, company_id):

        connection = get_connection()

        try:
            row = connection.execute("""
                SELECT extracted_text
                FROM internal_documents
                WHERE id = ? AND company_id = ?
            """, (document_id, company_id)).fetchone()

            return row["extracted_text"] if row else None

        finally:
            connection.close()

    def delete_document(self, document_id, company_id):

        connection = get_connection()

        try:
            cursor = connection.execute("""
                DELETE FROM internal_documents
                WHERE id = ? AND company_id = ?
            """, (document_id, company_id))

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()
