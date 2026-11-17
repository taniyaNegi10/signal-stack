
from services.source_service import SourceService

source_service = SourceService()


deleted = source_service.delete_source(2)

print("Duplicate deleted:", deleted)

print("\nREMAINING SOURCES\n")

sources = source_service.get_sources(1)

for source in sources:
    print(
        "ID:", source["id"],
        "| Name:", source["name"],
        "| URL:", source["url"]
    )
