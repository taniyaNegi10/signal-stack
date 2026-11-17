# SIGNAL STACK — TEST EVIDENCE

## 1. Testing Overview

Individual Python test scripts were created to validate company management, source discovery, source approval, signal collection, analysis, competitor research, internal document processing, and report generation.

The following results were observed during development.

## 2. Test Results

| Test Area | Observed Result |
|---|---|
| Company management | Company profiles created and managed |
| Company interviews | Tata Motors and Infosys: 10 answers each |
| MeetUniversity source approval | 20 approved sources |
| MeetUniversity collection | 20 sources checked |
| Signal collection | 13 signals saved |
| Duplicate detection | 7 duplicates skipped |
| Collection failures | 0 in the recorded run |
| Competitor research | 6 competitor profiles used |
| Internal document processing | Sample feedback document processed |
| Tata Motors collection | 1 approved source and 1 signal |
| Infosys source access | Tested URLs blocked by robots.txt |
| Report generation | Reports generated for all 3 companies |

## 3. Report Evidence

Three generated reports were exported from the SQLite database:

1. MeetUniversity — Report ID 17
2. Tata Motors — Report ID 18
3. Infosys — Report ID 19

The reports are available in the reports directory.

## 4. Source Access and Responsible Collection

- Public source accessibility was checked before collection.
- Sources blocked by robots.txt were not bypassed.
- Inaccessible Infosys sources remained unapproved.
- Source accessibility was not treated as proof of credibility.
- Generated interpretations require human verification.

## 5. Known Limitations

- The interview uses a fixed question set rather than adaptive questioning.
- Signal analysis is preliminary and rule-based.
- Evidence coverage differs between companies.
- Infosys currently has no collected signals.
- Automated weekly scheduling has not been verified as operational.
- Individual test scripts were created, but this document does not claim that every test script passed.

## 6. Conclusion

The observed results demonstrate that the core company management, source workflow, signal collection, internal document processing, and report generation workflows were exercised during development.

Further testing and validation are required before production deployment.
