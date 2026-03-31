import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:3000")
        await page.wait_for_selector("text=Batangas", timeout=10000)
        await page.screenshot(path="screenshot.png")
        await browser.close()

asyncio.run(run())
