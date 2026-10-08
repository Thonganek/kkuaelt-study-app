import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
D1 = "significant, evidence, indicate, contribute, consequence, factor, approach, determine, assess, evaluate, demonstrate, prevalence, intervention, outcome, association, approximately, whereas, nevertheless, therefore, estimate"
SL = {}
SL[1]="analyse, area, assume, authority, available, benefit, concept, consist, constitute, context, contract, create, data, define, derive, distribute, economy, environment, establish, export, finance, formula, function, identify, income, individual, interpret, involve, issue, labour, legal, legislate, major, method, occur, percent, period, policy, principle, proceed, process, require, research, respond, role, section, sector, similar, source, specific, structure, theory, vary"
SL[2]="achieve, acquire, administrate, affect, appropriate, aspect, assist, category, commission, community, complex, compute, conclude, conduct, construct, consume, credit, culture, design, distinct, element, equate, feature, final, focus, impact, injure, institute, invest, journal, maintain, normal, obtain, participate, perceive, positive, potential, previous, primary, purchase, range, region, regulate, relevant, reside, resource, restrict, secure, seek, select, site, strategy, survey, tradition, transfer"
SL[3]="alternative, circumstance, comment, compensate, component, consent, considerable, constant, constrain, convene, coordinate, core, corporate, correspond, criteria, deduce, document, dominate, emphasis, ensure, exclude, framework, fund, illustrate, immigrate, imply, initial, instance, interact, justify, layer, link, locate, maximise, minor, negate, partner, philosophy, physical, proportion, publish, react, register, rely, remove, scheme, sequence, shift, specify, sufficient, task, technical, technique, technology, valid, volume"
SL[4]="access, adequate, annual, apparent, attitude, attribute, civil, code, commit, communicate, concentrate, confer, contrast, cycle, debate, despite, dimension, domestic, emerge, error, ethnic, goal, grant, hence, hypothesis, implement, implicate, impose, integrate, internal, investigate, label, mechanism, obvious, occupy, option, output, overall, parallel, parameter, phase, predict, principal, prior, professional, project, promote, regime, resolve, retain, series, statistic, status, stress, subsequent, sum, summary, undertake"
SL[5]="academy, adjust, alter, amend, aware, capacity, challenge, clause, compound, conflict, consult, contact, decline, discrete, draft, enable, energy, enforce, entity, equivalent, evolve, expand, expose, external, facilitate, fundamental, generate, generation, image, liberal, licence, logic, margin, medical, mental, modify, monitor, network, notion, objective, orient, perspective, precise, prime, psychology, pursue, ratio, reject, revenue, stable, style, substitute, sustain, symbol, target, transit, trend, version, welfare"
SL[6]="abstract, accurate, acknowledge, aggregate, allocate, assign, attach, author, bond, brief, capable, cite, cooperate, discriminate, display, diverse, domain, edit, enhance, estate, exceed, expert, explicit, federal, fee, flexible, furthermore, gender, ignorance, incentive, incidence, incorporate, index, inhibit, initiate, input, instruct, intelligence, interval, lecture, migrate, minimum, ministry, motive, neutral, overseas, precede, presume, rational, recover, reveal, scope, subsidy, trace, transform, transport, underlie, utilise"
SL[7]="adapt, advocate, aid, channel, chemical, classic, comprehensive, comprise, confirm, contrary, convert, decade, definite, deny, differentiate, dispose, dynamic, eliminate, empirical, equip, extract, finite, foundation, globe, grade, guarantee, hierarchy, identical, ideology, infer, innovate, insert, intervene, isolate, media, mode, paradigm, phenomenon, priority, prohibit, publication, quote, release, reverse, simulate, sole, somewhat, submit, successor, survive, thesis, transmit, ultimate, unique, visible, voluntary"
SL[8]="abandon, accompany, accumulate, ambiguous, append, appreciate, arbitrary, automate, bias, chart, clarify, commodity, complement, conform, contemporary, contradict, crucial, currency, denote, detect, deviate, displace, eventual, exhibit, exploit, fluctuate, guideline, highlight, implicit, induce, inevitable, infrastructure, inspect, intense, manipulate, minimise, nuclear, offset, practitioner, predominant, prospect, radical, random, reinforce, restore, revise, schedule, tension, terminate, theme, thereby, uniform, vehicle, via, virtual, visual, widespread"
SL[9]="accommodate, analogy, anticipate, assure, attain, behalf, bulk, cease, coherent, coincide, commence, compatible, concurrent, confine, controversy, converse, device, devote, diminish, distort, duration, erode, ethic, format, found, inherent, insight, integral, intermediate, manual, mature, mediate, medium, military, minimal, mutual, norm, overlap, passive, portion, preliminary, protocol, qualitative, refine, relax, restrain, revolution, rigid, route, scenario, sphere, subordinate, supplement, suspend, temporary, trigger, unify, violate, vision"
SL[10]="adjacent, albeit, assemble, collapse, colleague, compile, conceive, convince, depress, encounter, enormous, forthcoming, incline, integrity, intrinsic, invoke, levy, likewise, nonetheless, notwithstanding, ongoing, panel, persist, pose, reluctance, so-called, straightforward, undergo, whereby"

def sp(s):
    return [w.strip() for w in s.split(',')]

awl = []
for k in range(1, 11):
    for w in sp(SL[k]):
        awl.append((w, k))
exp = {1:53, 2:55, 3:56, 4:58, 5:59, 6:58, 7:56, 8:57, 9:59, 10:29}
for k, v in exp.items():
    n = len(sp(SL[k]))
    assert n == v, (k, n, v)
assert len(awl) == 540, len(awl)
assert len(set(w for w, _ in awl)) == 540

THEME = {
2:"curriculum, pedagogy, proficiency, literacy, higher education",
3:"emission, pollutant, particulate matter, respiratory, haze",
4:"obesity, sedentary, diagnose, algorithm, chronic",
6:"telemedicine, consultation, accessibility, underserved, caregiver",
7:"adolescent, deprivation, cognitive, circadian rhythm, impair",
8:"generative AI, chatbot, plagiarism, personalised learning, misconduct",
9:"urbanisation, vegetation, mitigate, absorb, heatwave",
10:"antibiotic, resistance, bacteria, prescription, infection",
11:"sanitation, hygiene, recycle, completion rate, digital divide",
13:"food insecurity, malnutrition, affordable, nutritious, vulnerable",
14:"circular economy, single-use, landfill, biodegradable, contamination",
15:"outbreak, vector-borne, epidemic, surveillance, seasonal",
16:"transparency, accountability, dataset, ethical, disparity",
17:"claim, contend, assert, argue, allege",
18:"mortality, shortage, ecosystem, health literacy, workforce",
20:"hypertension, randomised controlled trial, cohort, baseline, adherence",
21:"productivity, well-being, burnout, work-life balance, trial",
22:"firmly believe, in my view, oppose, it is often argued that, it is widely believed that",
23:"moreover, in addition, for instance, as a result, thus",
24:"ageing population, life expectancy, pension, dependency, retirement",
25:"sodium, renewable, privacy, depression, surveillance camera",
27:"in conclusion, to sum up, undoubtedly, outweigh, on balance",
28:"substantial, compelling, undeniable, paramount, detrimental",
29:"exhaustion, resilience, morale, turnover, stigma",
30:"admittedly, granted that, critics argue, it is true that, on the contrary",
31:"play a crucial role in, have a profound impact on, raise awareness of, take measures to, address the issue of",
32:"biodiversity, deforestation, universal coverage, donor, food waste",
34:"vaccine hesitancy, immunisation, misinformation, herd immunity, side effect",
35:"indispensable, rigorous, meritocracy, standardised test, holistic",
36:"lifelong learning, credential, self-paced, isolation, engagement",
37:"collaboration, synergy, autonomy, interpersonal, delegate",
38:"fulfilment, job satisfaction, remuneration, motivation, career advancement",
39:"genomics, tailor, citizen science, volunteering, fatality",
41:"face-to-face, flexibility, interaction, convenience, distraction",
42:"language acquisition, immersion, interdisciplinary, content-based, bilingual",
43:"automation, critical thinking, academic integrity, digital literacy, over-reliance",
}
vdays = [2,3,4,6,7,8,9,10,11,13,14,15,16,17,18,20,21,22,23,24,25,27,28,29,30,31,32,34,35,36,37,38,39,41,42,43]
assert len(vdays) == 36 and sorted(THEME) == vdays
plan = {1: [{"w": w, "src": "research"} for w in sp(D1)]}
allw = set(sp(D1))
for i, d in enumerate(vdays):
    chunk = awl[i*15:(i+1)*15]
    th = sp(THEME[d])
    assert len(th) == 5, (d, th)
    plan[d] = [{"w": w, "src": f"AWL{k}"} for w, k in chunk] + [{"w": w, "src": "theme"} for w in th]
    for e in plan[d]:
        assert e["w"] not in allw, (d, e["w"])
        allw.add(e["w"])
print('total words', sum(len(v) for v in plan.values()), 'unique', len(allw))
json.dump(plan, open('vocab_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for d, v in plan.items():
    print(d, ', '.join(e['w'] for e in v))
