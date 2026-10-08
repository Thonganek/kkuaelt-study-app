# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
HTML = Path(__file__).resolve().parent.parent / 'out' / 'KKU-AELT_42_Day_Study_Plan.html'
errs = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(viewport={'width': 1280, 'height': 900}, accept_downloads=True); ctx.set_offline(True)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: d.accept())
    pg.goto(HTML.as_uri()); pg.wait_for_selector('#main .pagehead')
    counts = {}
    for d in range(1, 43):
        pg.evaluate(f"location.hash='#/day/{d}'"); pg.wait_for_timeout(40)
        hrefs = pg.eval_on_selector_all('.steps-list .srow', 'els => els.map(e => e.getAttribute("href"))'); n = len(hrefs); counts[d] = n
        if pg.locator('.hero-cta').count() != 1 or pg.locator('.hero-stats .hs').count() != 4: errs.append(f'day {d}: hero incomplete')
        ov = pg.inner_text('#main')
        for bad in ('เกิดข้อผิดพลาด', 'NaN'):
            if bad in ov: errs.append(f'day {d} overview: {bad}')
        for i, hr in enumerate(hrefs):
            pg.evaluate(f"location.hash='{hr}'"); pg.wait_for_timeout(25)
            if pg.locator('.blockhead').count() != 1 or pg.locator('.stepper a.on').count() != 1: errs.append(f'day {d} step {i}: block view missing')
            t = pg.inner_text('#main')
            for bad in ('แสดงส่วนนี้ไม่ได้', 'ไม่พบชุดคำถาม', 'ยังไม่มีบทอ่าน', 'ยังไม่มีบทเรียน', 'ยังไม่มีข้อสอบ', 'undefined', 'NaN'):
                if bad in t:
                    errs.append(f'day {d} step {i}: {bad}')
    print('steps per day:', counts)
    # quick: answer all quizzes on day 2 wrong, then Sunday weekly retry lists them
    pg.evaluate("location.hash='#/day/4'"); pg.wait_for_timeout(60)
    for k in ('vocab', 'reading', 'writing'):
        pg.evaluate(f"location.hash='#/day/4/{k}'"); pg.wait_for_timeout(40)
        for box in pg.locator('.quizbox').all():
            for o in box.locator('.opts').all():
                o.locator('.opt').nth(3).click()
            sub = box.locator('[data-act=submit]')
            if sub.count(): sub.first.click(); pg.wait_for_timeout(60)
    pg.evaluate("location.hash='#/day/9/weekly'"); pg.wait_for_timeout(60)
    print('weekly retry items:', pg.locator('.q').count())
    pg.locator('.q .opt').first.click(); pg.wait_for_timeout(60)
    print('after retry explain shown:', pg.locator('.explain').count())
    # each test intro
    for t in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'M1', 'M2', 'M3']:
        pg.evaluate(f"location.hash='#/test/{t}'"); pg.wait_for_timeout(40)
        if 'ไม่พบข้อสอบ' in pg.inner_text('#main'): errs.append('missing test ' + t)
    # backup
    pg.evaluate("location.hash='#/settings'"); pg.wait_for_timeout(60)
    with pg.expect_download() as dl:
        pg.locator('[data-act=backup]').click()
    print('backup file:', dl.value.suggested_filename)
    pg.evaluate("location.hash='#/plan'"); pg.wait_for_timeout(60)
    with pg.expect_download() as dl:
        pg.locator('[data-act=csv]').click()
    print('csv file:', dl.value.suggested_filename)
    st = pg.evaluate("JSON.stringify(JSON.parse(localStorage.getItem('kkuaelt45.v2'))).length")
    print('state bytes', st)
    b.close()
print('ERRORS', len(errs)); [print(' ', e) for e in errs[:30]]
