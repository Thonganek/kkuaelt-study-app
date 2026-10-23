# -*- coding: utf-8 -*-
"""Test progress-based days: tick days done / not done, "today" = first unfinished day, the to-do page,
the catch-up split, calendar mode, and the mobile layout. Usage: python test_progress.py [HTML] [--shots]"""
import sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
HTML = Path(args[0]) if args else Path(__file__).resolve().parent.parent / 'out' / 'KKU-AELT_42_Day_Study_Plan.html'
SHOTS = HTML.parent / 'shots'
errs = []


def check(cond, msg):
    if not cond:
        errs.append(msg)


with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1366, 'height': 900}); ctx.set_offline(True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pg.on('dialog', lambda d: d.accept())
    pg.goto(HTML.as_uri()); pg.wait_for_selector('#main .pagehead')

    def go(h, wait=80):
        pg.evaluate(f"location.hash='{h}'"); pg.wait_for_timeout(wait)

    def today():
        go('#/todo'); go('#/today')
        return int(re.search(r'Day (\d+)/42', pg.inner_text('#main .pagehead .eyebrow')).group(1))

    check(today() == 1, 'fresh state should start at Day 1')
    go('#/todo')
    check(pg.locator('.dgrid .dg').count() == 42, 'status grid should have 42 days')
    pg.locator('.dgrid .dg').nth(0).locator('.chkbtn').click(); pg.wait_for_timeout(80)
    check(today() == 2, 'after ticking Day 1, today should be Day 2')

    go('#/todo'); pg.select_option('#upto', '5'); pg.locator('[data-act=markUpTo]').click(); pg.wait_for_timeout(80)
    check(today() == 6, 'after ticking Day 1-5, today should be Day 6')

    go('#/todo'); pg.locator('.dgrid .dg').nth(2).locator('.chkbtn').click(); pg.wait_for_timeout(80)  # undo Day 3
    check(today() == 3, 'after un-ticking Day 3, today should be Day 3')
    check('ยังไม่เริ่ม' in pg.inner_text('#main .pagehead .eyebrow'), 'un-ticked Day 3 should read as not started')

    go('#/day/3'); pg.locator('.pagehead [data-act=dayDone]').click(); pg.wait_for_timeout(80)
    check(pg.locator('.pagehead .daytog.good').count() == 1, 'Day 3 toggle should show done')
    check(today() == 6, 'after ticking Day 3 in its own page, today should be Day 6 again')

    # a step done in the app (vocab quiz submitted) makes Day 6 "partly done"
    go('#/day/6/vocab', 150)
    box = pg.locator('.quizbox[data-key="V:6"]')
    for o in box.locator('.opts').all():
        o.locator('.opt').first.click()
    box.locator('[data-act=submit]').click(); pg.wait_for_timeout(120)
    go('#/todo')
    check('part' in (pg.locator('.dgrid .dg').nth(5).get_attribute('class') or ''), 'Day 6 should be partly done')
    first = pg.locator('.todo-day').first
    check('Day 6' in first.inner_text() and first.locator('.chip.ok').count() == 1, 'to-do list should start with Day 6 and show its finished step')

    # catch-up split: every unfinished day appears exactly once, Light Review last
    rows = pg.locator('table.plan tr').all()[1:]
    listed = [int(x) for r in rows for x in re.findall(r'Day (\d+)', r.locator('td').nth(1).inner_text())]
    left = [d for d in range(1, 43) if d not in (1, 2, 3, 4, 5)]
    check(sorted(listed) == left, f'catch-up split should list every unfinished day once: {listed}')
    n = pg.evaluate('daysToExam()')
    check(len(rows) <= n, f'catch-up split uses {len(rows)} days but only {n} are left')
    if rows:
        check('Day 42' in rows[-1].inner_text(), 'Light Review should be the last day')
    print('days to exam', n, '· split rows', len(rows), '· first row:', rows[0].inner_text().replace('\n', ' ') if rows else '-')

    # plan table + grid both carry tick buttons; CSV has a status column
    go('#/plan')
    check(pg.locator('table.plan .chkbtn').count() == 42, 'plan table should have 42 tick buttons')
    check(pg.locator('.dgrid .dg').count() == 42, 'plan view should show the status grid')

    # calendar mode keeps the original behaviour
    go('#/settings'); pg.locator('[data-act=setDayMode][data-v=calendar]').click(); pg.wait_for_timeout(80)
    raw = pg.evaluate('calRawNum()')
    go('#/today')
    eb = pg.inner_text('#main .pagehead .eyebrow')
    check('Day ' not in eb and ('ต.ค.' in eb or 'พ.ย.' in eb), 'calendar mode eyebrow should show the date: ' + eb)
    check(pg.evaluate('todayNum()') == min(42, max(1, raw)), 'calendar mode today should follow the date')
    go('#/plan'); check(pg.locator('.cal .cell').count() > 0, 'calendar mode shows the calendar')
    go('#/settings'); pg.locator('[data-act=setDayMode][data-v=progress]').click(); pg.wait_for_timeout(80)
    check(pg.evaluate('todayNum()') == 6, 'back in progress mode today should be Day 6')

    # every page still renders without leaks
    for h in ('#/today', '#/todo', '#/plan', '#/vocab', '#/errors', '#/writing', '#/stats', '#/guide', '#/settings', '#/more'):
        go(h)
        t = pg.inner_text('#main').replace('undefined (adj.)', '')
        for bad in ('เกิดข้อผิดพลาด', 'NaN', 'undefined'):
            check(bad not in t, f'{h}: {bad}')

    if '--shots' in sys.argv:
        SHOTS.mkdir(exist_ok=True)
        go('#/today', 300); pg.screenshot(path=str(SHOTS / 'p_today.png'))
        go('#/todo', 300); pg.screenshot(path=str(SHOTS / 'p_todo.png'), full_page=True)
        go('#/plan', 300); pg.screenshot(path=str(SHOTS / 'p_plan.png'))
        pg.evaluate("S.settings.theme='dark';applySettings()"); go('#/todo', 300); pg.screenshot(path=str(SHOTS / 'p_todo_dark.png'))
        pg.evaluate("S.settings.theme='light';applySettings()")

    # phone width: no sideways scroll on the new page, tab bar fits
    m = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); m.set_offline(True)
    mp = m.new_page(); mp.on('pageerror', lambda e: errs.append('mobile pageerror: ' + str(e))); mp.on('dialog', lambda d: d.accept())
    mp.goto(HTML.as_uri() + '#/todo'); mp.wait_for_selector('.dgrid'); mp.wait_for_timeout(200)
    sw = mp.evaluate('document.documentElement.scrollWidth')
    check(sw <= 390, f'mobile to-do page scrolls sideways ({sw}px)')
    check(mp.locator('.tabbar a').count() == 6, 'mobile tab bar should have 6 items')
    tb = mp.evaluate("[...document.querySelectorAll('.tabbar a')].map(a => a.getBoundingClientRect().right)")
    check(max(tb) <= 390, f'tab bar overflows: {tb}')
    mp.locator('.dgrid .dg').nth(0).locator('.chkbtn').click(); mp.wait_for_timeout(80)
    check('done' in (mp.locator('.dgrid .dg').nth(0).get_attribute('class') or ''), 'mobile tick should work')
    for h in ('#/today', '#/day/3'):
        mp.evaluate(f"location.hash='{h}'"); mp.wait_for_timeout(150)
        sw = mp.evaluate('document.documentElement.scrollWidth')
        check(sw <= 390, f'mobile {h} scrolls sideways ({sw}px)')
    if '--shots' in sys.argv:
        mp.evaluate("location.hash='#/todo'"); mp.wait_for_timeout(300); mp.screenshot(path=str(SHOTS / 'p_todo_mobile.png'), full_page=True)
        mp.evaluate("location.hash='#/today'"); mp.wait_for_timeout(300); mp.screenshot(path=str(SHOTS / 'p_today_mobile.png'))
    b.close()

print('ERRORS', len(errs))
for e in errs:
    print(' ', e)
sys.exit(1 if errs else 0)
