
from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    UPDATE sources
    SET category = ?,
        reason = ?
    WHERE id = ?
    """,
    (
        "Internal Intelligence",
        "First-party official company website. "
        "Provides company information and promotional "
        "content; not independent customer evidence.",
        1
    )
)

connection.commit()
connection.close()

print("Source category updated successfully!")
