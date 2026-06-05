"""Render OG card HTML to a 1200x630 PNG."""
import sys, io, base64, time
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

template = Path('D:/claude-test/scripts/og_template.html').resolve().as_uri()
out = 'D:/claude-test/frontend/public/og.png'

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--hide-scrollbars')
opts.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
d = webdriver.Chrome(options=opts)
d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
    'width': 1200, 'height': 630, 'deviceScaleFactor': 2, 'mobile': False
})
d.get(template)
time.sleep(1)
r = d.execute_cdp_cmd('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False})
Path(out).parent.mkdir(parents=True, exist_ok=True)
with open(out, 'wb') as f:
    f.write(base64.b64decode(r['data']))
print(f'wrote {out}')
d.quit()
