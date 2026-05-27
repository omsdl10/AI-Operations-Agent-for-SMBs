from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import SessionLocal
from app.services.automation_service import AutomationService
from app.services.summary_service import SummaryService
from app.models.business import Business
from sqlalchemy import select

logger = get_logger(__name__)
scheduler = None


def run_automation_cycle() -> None:
    db = SessionLocal()
    try:
        result = AutomationService(db).run_due_automations()
        logger.info("Automation cycle completed: %s", result.model_dump())
    except Exception:
        logger.exception("Automation cycle failed")
    finally:
        db.close()


def run_daily_summary_cycle() -> None:
    db = SessionLocal()
    try:
        business_ids = list(db.scalars(select(Business.id)).all())
        for business_id in business_ids:
            SummaryService(db).generate(business_id)
        logger.info("Daily summary cycle completed for %s businesses", len(business_ids))
    except Exception:
        logger.exception("Daily summary cycle failed")
    finally:
        db.close()


def start_scheduler() -> None:
    global scheduler
    if not settings.automation_scheduler_enabled:
        logger.info("Automation scheduler disabled")
        return
    if scheduler:
        return

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except ImportError:
        logger.warning("APScheduler is not installed; automation scheduler did not start")
        return

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        run_automation_cycle,
        trigger="interval",
        minutes=settings.automation_interval_minutes,
        id="automation_cycle",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        run_daily_summary_cycle,
        trigger="cron",
        hour=23,
        minute=55,
        id="daily_summary_cycle",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logger.info("Automation scheduler started")


def stop_scheduler() -> None:
    global scheduler
    if scheduler:
        scheduler.shutdown(wait=False)
        scheduler = None
        logger.info("Automation scheduler stopped")
