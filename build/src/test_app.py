# -*- coding: utf-8 -*-
"""Smoke-test the built HTML in headless Chromium: every view, every day, quizzes, test runner, essay, backup."""
import sys, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
HTML = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'out' / 'KKU-AELT_42_Day_Study_Plan.html'
SHOTS = HTML.parent / 'shots'
SHOTS.mkdir(exist_ok=True)
FULL = '--full' in sys.argv
errors, net = [], []

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    ctx = b.new_context(viewport={'width': 1366, 'height': 900}, accept_downloads=True)
    ctx.set_offline(True)
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    page.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' and 'fonts.g' not in m.text and 'ERR_INTERNET_DISCONNECTED' not in m.text else None)
    page.on('dialog', lambda d: d.accept())
    page.goto(HTML.as_uri())
    page.wait_for_selector('#main > *')

    def go(h, shot=None, full=False):
        page.evaluate(f"location.hash='{h}'")
        page.wait_for_timeout(120)
        if shot:
            page.screenshot(path=str(SHOTS / shot), full_page=full)

    go('#/plan', 'plan.png')
    rows = page.locator('table.plan tr').count()
    print('plan rows', rows)
    for d in range(1, 43):
        go(f'#/day/{d}')
        txt = page.inner_text('#main')
        if 'แสดงส่วนนี้ไม่ได้' in txt or 'เกิดข้อผิดพลาด' in txt:
            errors.append(f'day {d} render problem: ' + re.findall(r'แสดงส่วนนี้ไม่ได้[^\n]*', txt)[:3].__str__())
    go('#/day/1', 'day1.png', True)
    go('#/day/5', 'day5.png')
    go('#/day/22', 'day22.png')
    # answer W01 quiz: pick option A for all mc, type into shorts, submit
    go('#/day/3')
    page.evaluate("location.hash='#/day/3/reading'"); page.wait_for_timeout(150)
    opts = page.locator('.quizbox[data-key="R:W01"] .opts')
    for i in range(opts.count()):
        opts.nth(i).locator('.opt').first.click()
    for inp in page.locator('.quizbox[data-key="R:W01"] .shortin input').all():
        inp.fill('conversational turns')
    page.locator('.quizbox[data-key="R:W01"] [data-act="submit"]').click()
    page.wait_for_timeout(150)
    print('W01 result:', page.locator('.quizbox[data-key="R:W01"] .result .big').first.inner_text() if page.locator('.quizbox[data-key="R:W01"] .result').count() else 'no result')
    # vocab quiz
    page.evaluate("location.hash='#/day/1/vocab'"); page.wait_for_timeout(150)
    vq = page.locator('.quizbox[data-key="V:1"] .opts')
    for i in range(vq.count()):
        vq.nth(i).locator('.opt').nth(1).click()
    page.locator('.quizbox[data-key="V:1"] [data-act="submit"]').click()
    page.wait_for_timeout(150)
    # essay typing
    page.evaluate("location.hash='#/day/3/writing'"); page.wait_for_timeout(150)
    page.screenshot(path=str(SHOTS / 'day1_writing.png'), full_page=False)
    ed = page.locator('textarea.editor').first
    ed.fill('Technology has made our lives more stressful because people are always connected. ' * 3)
    page.wait_for_timeout(400)
    print('wc:', page.locator('[data-wc]').first.inner_text())
    page.screenshot(path=str(SHOTS / 'day1_after.png'), full_page=False)
    # errors view
    go('#/errors', 'errors.png')
    go('#/vocab', 'vocab.png')
    page.fill('input[type=search]', 'evid')
    page.wait_for_timeout(400)
    print('vocab search cards:', page.locator('#vlist .vcard').count())
    go('#/writing/bank', 'writing.png')
    go('#/writing/models', 'models.png')
    go('#/stats', 'stats.png')
    go('#/guide/exam', 'guide.png')
    go('#/settings', 'settings.png')
    # test runner
    if page.evaluate("!!DATA.tests.T1"):
        go('#/test/T1', 'test_intro.png')
        page.locator('[data-act="startTest"]').click()
        page.wait_for_timeout(200)
        page.screenshot(path=str(SHOTS / 'test_run.png'))
        print('runner visible:', page.locator('.testwrap').count())
        for pi in range(6):
            page.locator(f'.ptab[data-pi="{pi}"]').click(); page.wait_for_timeout(80)
            for o in page.locator('.pane-q .opts').all():
                o.locator('.opt').nth(2).click()
        page.locator('.testtop [data-act="submit"]').click()
        page.wait_for_timeout(300)
        page.screenshot(path=str(SHOTS / 'test_result.png'))
        print('T1 result:', page.locator('.result .big').first.inner_text())
    # persistence: reload
    page.reload(); page.wait_for_selector('#main > *')
    st = page.evaluate("JSON.parse(localStorage.getItem('kkuaelt45.v2'))")
    print('persisted quizzes:', sorted(st['quiz'].keys())[:10], 'essays:', list(st['essays'].keys()))
    # mobile
    m = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
    m.set_offline(True)
    mp = m.new_page(); mp.on('pageerror', lambda e: errors.append('mobile pageerror: ' + str(e)))
    mp.goto(HTML.as_uri() + '#/day/4'); mp.wait_for_selector('#main > *'); mp.screenshot(path=str(SHOTS / 'm_day4.png'))
    mp.evaluate("location.hash='#/plan'"); mp.wait_for_timeout(150); mp.screenshot(path=str(SHOTS / 'm_plan.png'))
    mp.evaluate("location.hash='#/day/12'"); mp.wait_for_timeout(150); mp.screenshot(path=str(SHOTS / 'm_day12.png'))
    sw = mp.evaluate("document.documentElement.scrollWidth"); print('mobile scrollWidth', sw)
    # dark
    d = b.new_context(viewport={'width': 1366, 'height': 900}, color_scheme='dark'); d.set_offline(True)
    dp = d.new_page(); dp.goto(HTML.as_uri() + '#/day/2'); dp.wait_for_selector('#main > *'); dp.screenshot(path=str(SHOTS / 'dark_day2.png'))
    b.close()

print('ERRORS:', len(errors))
for e in errors[:40]:
    print(' ', e)
