"""DART 공시정보 스크래핑"""
from typing import Dict, Optional

from playwright.sync_api import sync_playwright


class DartScrap:
    def __init__(self, headless: bool = True) -> None:
        self.playwright_context = sync_playwright().start()
        self.browser = self.playwright_context.chromium.launch(
            headless=headless
        )

        page = self.browser.new_page()
        page.goto("https://dart.fss.or.kr/main.do")
        self.cookies = page.context.cookies()
        page.close()

    def __del__(self):
        self.browser.close()
        self.playwright_context.stop()

    @property
    def headers_for_request(self) -> Dict[str, str]:
        jsession = [
            cookie for cookie in self.cookies if cookie["name"] == "JSESSIONID"
        ][0]
        wmonid = [
            cookie for cookie in self.cookies if cookie["name"] == "WMONID"
        ][0]
        return {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "dart.fss.or.kr",
            "Origin": "https://dart.fss.or.kr",
            "Referer": "https://dart.fss.or.kr/dsac001/mainY.do",
            "Cookie": f"{wmonid['name']}={wmonid['value']}; {jsession['name']}={jsession['value']}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        }

    def get_html_content_no_side_menu(self, url: str) -> str | None:
        """dart.fss.or.kr의 사이드 메뉴가 없는 페이지의 html을 가져온다."""
        context = self.browser.new_context()
        page = context.new_page()
        page.goto(url)

        page.locator("iframe").wait_for(state="attached")
        mf = page.frame("ifrm")

        contents: Optional[str] = mf.content() if mf is not None else None

        page.close()
        context.close()
        return contents

    @property
    def dividend_parser(self):
        from stock_clue.dartscrap.dividend_parser import DividendParser

        return DividendParser(self)
