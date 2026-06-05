"""Diagnose overflow at viewport=390 with mobile emulation."""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--disable-gpu")
opts.add_argument("--hide-scrollbars")
opts.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

driver = webdriver.Chrome(options=opts)

# Force exact viewport via CDP
driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
    "width": 390,
    "height": 1600,
    "deviceScaleFactor": 1,
    "mobile": True,
})

driver.get("https://backend-six-alpha-77.vercel.app/")
time.sleep(6)

result = driver.execute_script("""
const vw = window.innerWidth;
const overflowing = [];
document.querySelectorAll('*').forEach(el => {
  const rect = el.getBoundingClientRect();
  if (rect.right > vw + 1 && rect.width <= vw * 3) {
    overflowing.push({
      tag: el.tagName,
      cls: (el.className?.toString?.() || '').slice(0, 100),
      w: Math.round(rect.width),
      l: Math.round(rect.left),
      r: Math.round(rect.right),
    });
  }
});
return {
  innerWidth: vw,
  bodyScroll: document.body.scrollWidth,
  docElScroll: document.documentElement.scrollWidth,
  overflowing: overflowing.slice(0, 20),
};
""")
print(json.dumps(result, ensure_ascii=False, indent=2))
driver.quit()
