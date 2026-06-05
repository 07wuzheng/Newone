"""Capture viewport screenshots (no full page) using Chrome DevTools Protocol."""
import sys, io, base64, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SITE = "https://backend-six-alpha-77.vercel.app"
OUT = "D:/claude-test/docs/screenshots"


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--hide-scrollbars")
    opts.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    return webdriver.Chrome(options=opts)


def emulate(driver, width, height, mobile=False, dpr=1):
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": width, "height": height,
        "deviceScaleFactor": dpr, "mobile": mobile,
    })


def snap(driver, out_path):
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": False,
    })
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(result["data"]))
    print(f"  wrote {out_path}")


def main():
    driver = make_driver()
    try:
        # 1. Desktop home (1440x1200 to show hero + stats + filter + part of editor picks)
        print("[1/4] home-desktop 1440x1200")
        emulate(driver, 1440, 1200, mobile=False)
        driver.get(f"{SITE}/")
        time.sleep(6)
        snap(driver, f"{OUT}/home-desktop.png")

        # 2. Mobile home (iPhone 13/14: 390x844)
        print("[2/4] home-mobile 390x844 mobile")
        emulate(driver, 390, 844, mobile=True, dpr=1)
        driver.get(f"{SITE}/")
        time.sleep(6)
        snap(driver, f"{OUT}/home-mobile.png")

        # 3. Tool detail (1440x1200)
        print("[3/4] tool-detail 1440x1200")
        emulate(driver, 1440, 1200, mobile=False)
        driver.get(f"{SITE}/tool/1")
        time.sleep(6)
        snap(driver, f"{OUT}/tool-detail.png")

        # 4. ChatBot opened with a Q+A
        print("[4/4] chatbot 1440x900 with conversation")
        emulate(driver, 1440, 900, mobile=False)
        driver.get(f"{SITE}/")
        time.sleep(5)
        # Open the chatbot (the trigger button when closed)
        try:
            trigger = driver.find_element(By.CSS_SELECTOR, ".fixed.bottom-5.right-5 button")
            trigger.click()
            time.sleep(1)
        except Exception as e:
            print(f"  WARN: could not click trigger: {e}")
        # Type into input
        try:
            input_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='试']")
            input_box.send_keys("推荐免费的AI绘画工具")
            time.sleep(0.3)
            input_box.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"  WARN: could not send question: {e}")
        # Poll for response done (no loading dots + at least one assistant bubble visible)
        for _ in range(30):
            time.sleep(1)
            try:
                done = driver.execute_script(
                    "return !document.querySelector('.animate-bounce') "
                    "&& document.querySelectorAll('[class*=\"rounded-bl\"]').length > 0;"
                )
                if done:
                    break
            except Exception:
                pass
        time.sleep(1)
        snap(driver, f"{OUT}/chatbot.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
