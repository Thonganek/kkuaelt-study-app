import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML = Path(__file__).resolve().parent.parent / 'out' / 'KKU-AELT_42_Day_Study_Plan.html'
old = {'v': 2, 'done': {'5': {'essay': True}, '2': {'vocab': True}}, 'quiz': {'V:1': {'done': True, 'score': 18, 'total': 20, 'ans': {}}, 'V:2': {'done': True, 'score': 15, 'total': 20, 'ans': {}}, 'R:W01': {'done': True, 'score': 7, 'total': 10, 'ans': {}}, 'G:G01': {'done': True, 'score': 12, 'total': 15, 'ans': {}}},
       'essays': {'E:1': {'text': 'baseline paragraph about technology'}, 'E:2': {'text': 'three thesis statements'}, 'E:7': {'text': 'topic sentences day7'}, 'E:5': {'text': 'diagnostic essay R3'}},
       'notes': {'1': 'diag notes', '2': 'fragment notes', '6': 'articles'}, 'vstat': {}, 'resolved': {}, 'retry': {}, 'timers': {'B:1:vocab': {'end': 0}}, 'ui': {}, 'settings': {'font': 'm', 'theme': 'light', 'exam': '2026-11-21'}}
errs = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(HTML.as_uri() + '#/plan'); pg.evaluate("s => localStorage.setItem('kkuaelt45.v2', s)", json.dumps(old))
    pg.reload(); pg.wait_for_timeout(600)
    st = pg.evaluate("JSON.parse(localStorage.getItem('kkuaelt45.v2') || 'null') || S")
    st = pg.evaluate("S")
    print('theme attr:', pg.evaluate("document.documentElement.dataset.theme"), 'settings:', st['settings'])
    print('essays:', {k: v['text'] for k, v in st['essays'].items()})
    print('notes:', st['notes'])
    print('done:', st['done'], 'quiz keys:', sorted(st['quiz']), 'timers:', st['timers'], 'plan42:', st.get('plan42'))
    pg.goto(HTML.as_uri() + '#/day/14/writing'); pg.wait_for_timeout(300)
    print('day14 editor has baseline:', 'baseline paragraph' in pg.input_value('textarea.editor'))
    b.close()
print('errors', errs)
