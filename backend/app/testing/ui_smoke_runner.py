from playwright.sync_api import sync_playwright
from app.core.logger import get_logger

logger = get_logger("ui_smoke_runner")


def run_ui_smoke_test(base_url: str) -> dict:
    if not base_url:
        return {"passed": False, "details": "No base URL configured"}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(base_url, timeout=15000)
            title = page.title()
            browser.close()
            return {"passed": True, "details": f"Page loaded, title: {title}"}
    except Exception as e:
        return {"passed": False, "details": str(e)}
