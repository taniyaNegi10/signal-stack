
from services.company_service import CompanyService

service = CompanyService()

# Try adding the same company again
company_id = service.add_company(
    "MeetUniversity",
    "https://www.meetuniversity.com",
    "Education Technology"
)

if company_id is None:
    print("Duplicate prevented successfully!")
else:
    print("New company added! ID:", company_id)

# Display all saved companies
companies = service.get_all_companies()

print("\nSaved companies:")

for company in companies:
    print(dict(company))
