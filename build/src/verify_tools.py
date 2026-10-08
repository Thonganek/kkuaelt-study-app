# -*- coding: utf-8 -*-
"""Blind answer-key verification.
  python verify_tools.py export NAME src1.json [src2.json ...]   -> verify/blind_NAME.json (no keys)
  python verify_tools.py compare NAME                            -> compares verify/answers_NAME.json with keys
Answers file format: {"<qid>": <0-3 or "short text">, ...} where qid = "<passageId>.<n>" or "<gramId>.<n>".
"""
import json, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
SCR = Path(__file__).resolve().parent.parent
C = SCR / 'content'; V = SCR / 'verify'; V.mkdir(exist_ok=True)


def items_from(path):
    d = json.loads((C / path).read_text(encoding='utf-8'))
    if 'passages' in d:
        for p in d['passages']:
            yield 'p', p
    if 'sets' in d:
        for g in d['sets']:
            yield 'g', g


def export(name, srcs):
    out = {'passages': [], 'grammar': []}
    for s in srcs:
        for kind, x in items_from(s):
            if kind == 'p':
                out['passages'].append({'id': x['id'], 'title': x['title'], 'paragraphs': x['paragraphs'],
                    'questions': [{'qid': f"{x['id']}.{i+1}", 'type': q['type'], 'q': q['q'], **({'options': q['options']} if q['type'] == 'mc' else {})} for i, q in enumerate(x['questions'])]})
            else:
                out['grammar'].append({'id': x['id'], 'title': x['title_en'], 'questions': [{'qid': f"{x['id']}.{i+1}", 'q': q['q'], 'options': q['options']} for i, q in enumerate(x['quiz'])]})
    (V / f'blind_{name}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    n = sum(len(p['questions']) for p in out['passages']) + sum(len(g['questions']) for g in out['grammar'])
    print(f'blind_{name}.json: {len(out["passages"])} passages, {len(out["grammar"])} grammar sets, {n} questions')


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'\b(the|a|an)\b', ' ', str(s).lower())).strip(' .')


def compare(name, srcs=None):
    ans = json.loads((V / f'answers_{name}.json').read_text(encoding='utf-8'))
    blind = json.loads((V / f'blind_{name}.json').read_text(encoding='utf-8'))
    keys = {}
    for f in C.glob('*.json'):
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        for p in d.get('passages', []) if isinstance(d, dict) else []:
            for i, q in enumerate(p['questions']):
                keys[f"{p['id']}.{i+1}"] = (q, f.name)
        for g in d.get('sets', []) if isinstance(d, dict) else []:
            for i, q in enumerate(g['quiz']):
                keys[f"{g['id']}.{i+1}"] = (q, f.name)
    qids = [q['qid'] for p in blind['passages'] for q in p['questions']] + [q['qid'] for g in blind['grammar'] for q in g['questions']]
    bad = []
    for qid in qids:
        q, fn = keys[qid]
        a = ans.get(qid)
        if q['type'] == 'mc' if 'type' in q else True:
            ok = a is not None and int(a) == q['answer']
        else:
            ok = a is not None and norm(a) in [norm(x) for x in q['answers']]
        if not ok:
            bad.append((qid, fn, q, a))
    print(f'{name}: {len(qids)} questions, {len(bad)} disagreements ({len(qids)-len(bad)} agree)')
    rep = []
    for qid, fn, q, a in bad:
        line = {'qid': qid, 'file': fn, 'q': q['q'], 'key': q.get('answer', q.get('answers')), 'verifier': a,
                'options': q.get('options'), 'explain': q.get('explain')}
        rep.append(line)
        print('-', qid, '| key:', line['key'], '| verifier:', a, '|', q['q'][:90])
    (V / f'disagree_{name}.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == 'export':
        export(name, sys.argv[3:])
    else:
        compare(name)
