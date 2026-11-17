
from database import get_connection

QUESTIONS = [
    "What does your company do?",
    "What products or services does your company offer?",
    "Who are your ideal customers?",
    "Which industries or markets do you serve?",
    "What makes your company different from competitors?",
    "Who are your main competitors?",
    "What are your company's biggest business goals?",
    "What are the biggest challenges your company currently faces?",
    "Which market trends could affect your company?",
    "What important developments should Signal Stack monitor?"
]

ANSWERS = {
    3: [
        "Tata Motors is an Indian commercial vehicle manufacturer. It designs, manufactures and sells trucks, buses, pickups and other mobility solutions for transportation, logistics, infrastructure and public mobility.",
        "Its offerings include heavy, intermediate and light commercial trucks, small commercial vehicles, buses, electric buses, electric trucks, pickups, vehicle parts, maintenance, fleet solutions and connected vehicle services.",
        "Its customers include logistics and transport companies, fleet operators, infrastructure and construction businesses, manufacturers, distributors, small business owners, public transport organisations and government agencies.",
        "It serves road transportation, logistics, e-commerce delivery, construction, infrastructure, mining, agriculture, public transportation, industrial supply chains and last-mile delivery. India is a major market, with international operations as well.",
        "Its differentiators include a broad commercial-vehicle portfolio, established brand recognition, engineering and manufacturing capabilities, extensive distribution and service networks, fleet-support solutions and investments in electric and connected mobility.",
        "Key competitors and market peers include Ashok Leyland, Eicher/VE Commercial Vehicles, Mahindra Truck and Bus, BharatBenz and SML Isuzu. The competitive set varies by vehicle category.",
        "Based on publicly stated strategic priorities, important goals include profitable growth, strengthening commercial-vehicle market leadership, expanding electric and sustainable mobility, improving vehicle technology and connectivity, growing international business and improving operational efficiency.",
        "Potential challenges include intense competition, cyclical demand in the commercial-vehicle market, commodity and component costs, regulatory changes, supply-chain disruptions, electric-vehicle adoption barriers and the need to maintain profitability while investing in new technologies.",
        "Important trends include electric commercial vehicles, alternative fuels, stricter emission and safety standards, fleet digitisation, connected vehicles, logistics growth, infrastructure investment, automation and demand for lower operating costs.",
        "Monitor competitor vehicle launches and pricing, commercial-vehicle sales and market share, electric truck and bus adoption, charging infrastructure, government transport policies, emission regulations, fleet technology developments, commodity prices, supply-chain changes and major partnerships."
    ],
    4: [
        "Infosys is a global IT services and consulting company that helps organisations use technology to improve business operations, modernise systems, develop digital capabilities and transform their businesses.",
        "Its services include IT consulting, application development and maintenance, cloud transformation, artificial intelligence, data analytics, cybersecurity, enterprise solutions, digital transformation, business process management and technology platforms such as Infosys Cobalt and Infosys Topaz.",
        "Its ideal customers are large enterprises, multinational corporations, financial institutions, manufacturers, retailers, healthcare organisations, telecommunications companies and public-sector organisations seeking technology transformation.",
        "Infosys serves financial services and insurance, manufacturing, retail, consumer goods, logistics, communications, telecommunications, energy, utilities, resources, healthcare, life sciences and high technology. Its geographic markets include North America, Europe, India and other international markets.",
        "Its differentiators include global delivery capabilities, long-term enterprise relationships, consulting expertise, industry-specific knowledge, a large technology workforce, strategic technology partnerships and its AI, cloud and digital platforms.",
        "Major competitors and market peers include Tata Consultancy Services (TCS), Accenture, HCLTech, Wipro, Cognizant and Capgemini. Competition also comes from specialised cloud, AI and consulting firms.",
        "Based on public strategy statements, key goals include expanding AI-first services, helping clients achieve measurable business outcomes, growing cloud and digital transformation businesses, strengthening technology partnerships, developing employee capabilities and achieving sustainable profitable growth.",
        "Potential challenges include intense global competition, changing technology, pressure on consulting and IT spending, rapid AI adoption, talent reskilling requirements, cybersecurity risks, data privacy requirements and maintaining margins while investing in new capabilities.",
        "Important trends include generative and agentic AI, cloud adoption, enterprise automation, cybersecurity, data engineering, digital transformation, AI governance, platform modernisation and changing global technology budgets.",
        "Monitor major client wins, contract renewals, quarterly financial results, workforce and hiring trends, AI and cloud partnerships, new technology launches, competitor announcements, acquisitions, global IT spending and regulatory developments affecting technology services."
    ]
}


def save_answers(company_id, answers):
    connection = get_connection()
    inserted = 0
    updated = 0

    try:
        for question, answer in zip(QUESTIONS, answers):
            existing = connection.execute(
                """
                SELECT id
                FROM interview_answers
                WHERE company_id = ? AND question = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (company_id, question)
            ).fetchone()

            if existing:
                connection.execute(
                    """
                    UPDATE interview_answers
                    SET answer = ?
                    WHERE id = ?
                    """,
                    (answer, existing["id"])
                )
                updated += 1
            else:
                connection.execute(
                    """
                    INSERT INTO interview_answers
                    (company_id, question, answer)
                    VALUES (?, ?, ?)
                    """,
                    (company_id, question, answer)
                )
                inserted += 1

        connection.commit()

        print(f"\nCompany ID: {company_id}")
        print("Inserted:", inserted)
        print("Updated:", updated)
        print("Total questions saved:", len(answers))

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    save_answers(3, ANSWERS[3])
    save_answers(4, ANSWERS[4])

    print("\nCOMPANY INTERVIEWS SAVED SUCCESSFULLY!")
