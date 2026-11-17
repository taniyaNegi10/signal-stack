
from services.company_interview_service import CompanyInterviewService
from services.company_service import CompanyService

interview_service = CompanyInterviewService()
company_service = CompanyService()

COMPANY_ID = 1

print("\nCOMPANY INTERVIEW VERIFICATION")
print("=" * 60)

# 1. Get company details
company = company_service.get_company(COMPANY_ID)

if company:
    print("\nCOMPANY DETAILS")
    print("-" * 60)
    print("Company:", company["name"])
    print("Website:", company["website"])
else:
    print("Company not found.")
    raise SystemExit

# 2. Retrieve saved interview answers
answers = interview_service.get_answers(COMPANY_ID)

print("\nSAVED INTERVIEW ANSWERS")
print("-" * 60)

for index, answer in enumerate(answers, start=1):
    print(f"\nQuestion {index}: {answer['question']}")
    print("Answer:", answer["answer"])

# 3. Verify progress
progress = interview_service.get_progress(COMPANY_ID)

print("\nINTERVIEW PROGRESS")
print("-" * 60)
print("Answered:", progress["answered"])
print("Total:", progress["total"])
print("Remaining:", progress["remaining"])

# 4. Final verification
print("\nVERIFICATION RESULT")
print("-" * 60)

if progress["answered"] == 10 and progress["remaining"] == 0:
    print("SUCCESS: All 10 interview answers are saved.")
else:
    print("INCOMPLETE: Some interview answers are missing.")

print("=" * 60)
