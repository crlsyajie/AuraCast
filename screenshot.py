from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:3000')
    page.wait_for_timeout(3000) # wait for data to load
    page.screenshot(path='screenshot.png')
    browser.close()
