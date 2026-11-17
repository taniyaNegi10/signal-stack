
import argparse
import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from database import get_connection, initialize_database
from services.report_generation_service import ReportGenerationService
from services.source_quality_batch_service import SourceQualityBatchService


TIMEZONE = ZoneInfo("Asia/Kolkata")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("SignalStackScheduler")


def ensure_scheduler_table():
    """Create scheduler run-history storage."""

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS scheduler_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT NOT NULL,
            companies_processed INTEGER DEFAULT 0,
            details TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_companies():
    """Return one record per unique company website."""

    conn = get_connection()

    rows = conn.execute("""
        SELECT id, name, website, industry
        FROM companies AS c
        WHERE id = (
            SELECT MIN(c2.id)
            FROM companies AS c2
            WHERE c2.website = c.website
        )
        ORDER BY id
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def save_run_history(
    job_name,
    started_at,
    status,
    processed,
    details
):
    """Store the outcome of a scheduled task."""

    conn = get_connection()

    conn.execute("""
        INSERT INTO scheduler_runs (
            job_name,
            started_at,
            finished_at,
            status,
            companies_processed,
            details
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_name,
        started_at,
        datetime.now(TIMEZONE).isoformat(),
        status,
        processed,
        json.dumps(details, indent=2)
    ))

    conn.commit()
    conn.close()


def run_weekly_briefs():
    """Generate a Monday Morning Brief for each company."""

    started_at = datetime.now(TIMEZONE).isoformat()

    logger.info("Starting weekly report generation.")

    companies = get_companies()

    if not companies:
        save_run_history(
            "weekly_monday_briefs",
            started_at,
            "failed",
            0,
            [{"error": "No companies found."}]
        )
        return False

    report_service = ReportGenerationService()

    processed = 0
    failures = 0
    details = []

    for company in companies:
        try:
            logger.info(
                "Generating report for %s (ID: %s)",
                company["name"],
                company["id"]
            )

            result = report_service.generate_report(company["id"])

            processed += 1

            details.append({
                "company_id": company["id"],
                "company_name": company["name"],
                "status": "success",
                "report_id": result["report_id"],
                "generated_at": result["generated_at"]
            })

            logger.info(
                "Report generated. ID: %s",
                result["report_id"]
            )

        except Exception as error:
            failures += 1

            details.append({
                "company_id": company["id"],
                "company_name": company["name"],
                "status": "failed",
                "error": str(error)
            })

            logger.exception(
                "Report generation failed for %s",
                company["name"]
            )

    status = (
        "success" if failures == 0
        else "partial_failure" if processed > 0
        else "failed"
    )

    save_run_history(
        "weekly_monday_briefs",
        started_at,
        status,
        processed,
        details
    )

    logger.info(
        "Weekly report run finished. Successful: %s, Failed: %s",
        processed,
        failures
    )

    return failures == 0


def run_monthly_source_audit():
    """Evaluate and save source quality for every company."""

    started_at = datetime.now(TIMEZONE).isoformat()

    logger.info("Starting monthly source health audit.")

    companies = get_companies()

    if not companies:
        save_run_history(
            "monthly_source_health_audit",
            started_at,
            "failed",
            0,
            [{"error": "No companies found."}]
        )
        return False

    batch_service = SourceQualityBatchService()

    processed = 0
    total_sources = 0
    total_successful = 0
    total_failed = 0
    details = []

    for company in companies:
        try:
            logger.info(
                "Auditing sources for %s (ID: %s)",
                company["name"],
                company["id"]
            )

            result = batch_service.evaluate_all_sources(
                company["id"]
            )

            processed += 1

            total_sources += result["total_sources"]
            total_successful += result["successful"]
            total_failed += result["failed"]

            details.append({
                "company_id": company["id"],
                "company_name": company["name"],
                "status": (
                    "success"
                    if result["failed"] == 0
                    else "partial_failure"
                ),
                "total_sources": result["total_sources"],
                "successful": result["successful"],
                "failed": result["failed"],
                "evaluations": result["evaluations"],
                "errors": result["errors"]
            })

            logger.info(
                "%s: %s sources evaluated, %s failed.",
                company["name"],
                result["successful"],
                result["failed"]
            )

        except Exception as error:
            total_failed += 1

            details.append({
                "company_id": company["id"],
                "company_name": company["name"],
                "status": "failed",
                "error": str(error)
            })

            logger.exception(
                "Source audit failed for %s",
                company["name"]
            )

    if total_failed == 0:
        status = "success"
    elif total_successful > 0:
        status = "partial_failure"
    else:
        status = "failed"

    save_run_history(
        "monthly_source_health_audit",
        started_at,
        status,
        processed,
        details
    )

    logger.info(
        "Monthly audit finished. Companies: %s, "
        "Sources: %s, Successful: %s, Failed: %s",
        processed,
        total_sources,
        total_successful,
        total_failed
    )

    return total_failed == 0


def start_scheduler():
    """Start weekly reports and monthly source audits."""

    scheduler = BlockingScheduler(timezone=TIMEZONE)

    scheduler.add_job(
        run_weekly_briefs,
        trigger=CronTrigger(
            day_of_week="mon",
            hour=8,
            minute=0,
            timezone=TIMEZONE
        ),
        id="weekly_monday_briefs",
        name="Weekly Monday Morning Briefs",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600
    )

    scheduler.add_job(
        run_monthly_source_audit,
        trigger=CronTrigger(
            day=1,
            hour=9,
            minute=0,
            timezone=TIMEZONE
        ),
        id="monthly_source_health_audit",
        name="Monthly Source Health Audit",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600
    )

    logger.info("Signal Stack scheduler started.")
    logger.info("Weekly reports: Every Monday at 8:00 AM IST.")
    logger.info("Monthly source audit: 1st day at 9:00 AM IST.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="Signal Stack scheduler"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--run-now",
        action="store_true",
        help="Generate weekly reports immediately."
    )

    group.add_argument(
        "--audit-now",
        action="store_true",
        help="Run monthly source audit immediately."
    )

    args = parser.parse_args()

    initialize_database()
    ensure_scheduler_table()

    if args.run_now:
        success = run_weekly_briefs()
        raise SystemExit(0 if success else 1)

    if args.audit_now:
        success = run_monthly_source_audit()
        raise SystemExit(0 if success else 1)

    start_scheduler()


if __name__ == "__main__":
    main()
