#!/usr/bin/env python3
"""
recover_queries.py — recover the pre-artefact-floor search-query corpus from the
PROSE of analytics/daily-research/*.md, and compare it with the post-floor
machine-readable corpus in analytics/search-results/*.json.

Run:  LC_ALL=C python3 analytics/recover_queries.py
Measured at a single commit; the commit is printed in the header, not assumed.

THE ARTEFACT FLOOR is 2026-09-20 (first file in analytics/search-results/).
Pre-floor and post-floor corpora are NEVER summed into one number by this script.

CLASSIFIERS ARE PRINTED, NOT IMPLIED.  Every count this script emits names the
rule that produced it; the rules are the constants and functions below.
"""
import re, glob, os, json, subprocess, collections, sys

REPO = '/home/user/isds-watcher'
DR   = os.path.join(REPO, 'analytics/daily-research')
SR   = os.path.join(REPO, 'analytics/search-results')
FLOOR = '2026-09-20'

# ---------------------------------------------------------------- classifier C0
# C0  SPAN: an inline code span = text between two backticks, on one line,
#     OUTSIDE a fenced block (a line whose lstrip starts with ``` toggles fence
#     state).  Fenced blocks are excluded because they hold JSON artefacts, not
#     prose.
FENCE = re.compile(r'^\s*```')
SPAN  = re.compile(r'`([^`\n]+)`')

# ---------------------------------------------------------------- classifier C1
# C1  NOT-A-QUERY: a span is discarded as an identifier, not a query, if it
#     (a) starts with a URL scheme, /, ./, ~, $, > or < ; or
#     (b) begins with a shell/py token from SHELL_HEADS ; or
#     (c) contains a filename extension from EXTS ; or
#     (d) is a bare slash-path with no spaces.
SHELL_HEADS = (r'git|grep|rg|python3?|curl|sed|awk|wc|ls|cat|jq|find|sort|uniq|head|tail|'
               r'diff|sha256sum|md5sum|LC_ALL|export|date|tr|xargs|echo|printf|test|bash|'
               r'sh|npm|pip|gh|os\.path|open\(|def |import |for |if |while |return |'
               r'ALLOWED_HOSTS|EXCERPT_CHARS|GET |POST ')
RE_SHELL = re.compile(r'^(%s)\b' % SHELL_HEADS)
EXTS = re.compile(r'\.(md|py|json|jsonl|ya?ml|txt|csv|html?|pdf|xml|sh|toml|cfg|lock|js|ts|png|jpg)\b')
RE_PATHY = re.compile(r'^[A-Za-z0-9_\-/.]+/[A-Za-z0-9_\-/.?=&%#]+$')

def is_identifier_not_query(s):
    if s.startswith(('http://', 'https://', '/', './', '~', '$', '>', '<', '#')): return True
    if RE_SHELL.match(s): return True
    if EXTS.search(s): return True
    if RE_PATHY.match(s): return True
    if re.match(r'^[a-z0-9_]+\([^)]*\)$', s): return True          # a function call
    if re.match(r'^[0-9a-f]{7,40}$', s): return True               # a commit sha
    return False

# ---------------------------------------------------------------- classifier C2
# C2  QUERY-LABEL ANCHOR: the >=120 characters of the line immediately BEFORE the
#     span (or, when the span opens the line, the whole of the PREVIOUS line)
#     match RE_ANCHOR.  This is the high-precision tier: the record itself is
#     labelling the span as a query that was fired.
RE_ANCHOR = re.compile(
    r'(?i)(quer(y|ies)\b|\bsearch(es|ed)?\b|\bfired\b|\bwebsearch\b|'
    r'\bcall\b|\bS[0-9]\b|\bverbatim\b|\bin order fired\b)')

# ---------------------------------------------------------------- classifier C3
# C3  QUERY SHAPE: a span is query-SHAPED if it has >= 5 whitespace words and at
#     least one of: a double-quote (an exact-phrase operator), " OR ", " AND ".
#     Applied on top of C1.  Tier 2 = C3 without a C2 anchor.
def is_query_shaped(s):
    if len(s.split()) < 5: return False
    return ('"' in s) or (' OR ' in s) or (' AND ' in s)

# ------------------------------------------------- classifier C4: search slots
# C4  DECLARED SEARCH SLOT: a bolded numbered label of the form **Search N ...**
#     or **Query N ...** at the head of a line (allowing -, *, >, | and spaces).
#     These are slots the record declares it fired; in the earliest era they
#     carry a TOPIC label and NO query string.
RE_SLOT = re.compile(r'^[-*>|\s]*\*\*(?:Search|Query|Searches|Queries)\s+(\d+)'
                     r'(?:\s*[–—-]\s*\d+)?', re.M)

# C5  DECLARED SEARCH COUNT: an explicit statement of how many searches were run.
#     Matched on the whole file, deduped by (line, matched text).
RE_COUNT = re.compile(
    r'\*\*Searches conducted:\*\*\s*(\d+)'
    r'|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|'
    r'thirteen|fourteen|fifteen|\d+)\s+(?:targeted\s+|bounded\s+|differently-shaped\s+)?'
    r'(?:web\s+)?(?:searches|queries|websearch calls|search calls)\b', re.I)
WORDNUM = {w: i for i, w in enumerate(
    'zero one two three four five six seven eight nine ten eleven twelve thirteen '
    'fourteen fifteen'.split())}

def load_spans():
    out = []
    for f in sorted(glob.glob(os.path.join(DR, '*.md'))):
        lines = open(f, encoding='utf-8').read().split('\n')
        infence = False
        prev = ''
        for i, l in enumerate(lines, 1):
            if FENCE.match(l):
                infence = not infence; prev = l; continue
            if infence: prev = l; continue
            for m in SPAN.finditer(l):
                pre = l[:m.start()]
                ctx = pre[-120:] if pre.strip() else prev[-200:]
                out.append(dict(file=os.path.basename(f), line=i,
                                span=m.group(1), ctx=ctx))
            prev = l
    return out

def main():
    commit = subprocess.check_output(['git', '-C', REPO, 'rev-parse', 'HEAD']).decode().strip()
    dirty  = subprocess.check_output(['git', '-C', REPO, 'status', '--porcelain']).decode()
    files  = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DR, '*.md')))
    print('# recover_queries.py')
    print('measured_at_commit:', commit)
    print('working_tree_dirty_at_measurement:', bool(dirty.strip()),
          '(entries: %d)' % len([x for x in dirty.split('\n') if x.strip()]))
    print('daily_research_files:', len(files), 'first:', files[0], 'last:', files[-1])
    print('artefact_floor:', FLOOR)
    print()

    spans = load_spans()
    print('C0 inline code spans outside fenced blocks:', len(spans))
    kept = [s for s in spans if not is_identifier_not_query(s['span'])]
    print('C0+C1 after discarding identifiers/paths/commands:', len(kept))

    tier1 = [s for s in kept if len(s['span'].split()) >= 4 and RE_ANCHOR.search(s['ctx'])]
    tier2 = [s for s in kept if is_query_shaped(s['span'])]
    t1keys = {(s['file'], s['line'], s['span']) for s in tier1}
    tier2_only = [s for s in tier2 if (s['file'], s['line'], s['span']) not in t1keys]
    print('TIER 1  (C0+C1+C2, >=4 words, query-label anchored):', len(tier1))
    print('TIER 2  (C0+C1+C3 query-shaped) total:', len(tier2),
          '| of which NOT in tier 1:', len(tier2_only))
    union = {}
    for s in tier1 + tier2_only:
        union.setdefault(s['span'], []).append((s['file'], s['line']))
    print('UNION distinct query STRINGS (exact string equality):', len(union))
    print('UNION occurrences (a string re-quoted later counts once per occurrence):',
          len(tier1) + len(tier2_only))
    print()

    # per-file, split at the floor
    per = collections.Counter()
    for s in tier1 + tier2_only:
        per[s['file']] += 1
    pre  = {f: per.get(f, 0) for f in files if f[:10] <  FLOOR}
    post = {f: per.get(f, 0) for f in files if f[:10] >= FLOOR}
    print('PRE-FLOOR  files: %d, recovered query occurrences: %d, files with >=1: %d'
          % (len(pre), sum(pre.values()), sum(1 for v in pre.values() if v)))
    print('POST-FLOOR files: %d, recovered query occurrences: %d, files with >=1: %d'
          % (len(post), sum(post.values()), sum(1 for v in post.values() if v)))
    print()

    # declared slots and counts -> the recall denominator
    slots, counts = {}, {}
    for f in files:
        txt = open(os.path.join(DR, f), encoding='utf-8').read()
        ss = [int(m.group(1)) for m in RE_SLOT.finditer(txt)]
        slots[f] = (len(set(ss)), max(ss) if ss else 0)
        cs = []
        for m in RE_COUNT.finditer(txt):
            g = m.group(1) or m.group(2)
            if g is None: continue
            g = g.lower()
            n = WORDNUM.get(g, None)
            if n is None:
                try: n = int(g)
                except ValueError: continue
            if 0 < n <= 40: cs.append((n, m.group(0).strip()))
        counts[f] = cs
    print('C4 DECLARED SLOTS / C5 DECLARED COUNTS / recovered, per file')
    print('%-32s %6s %6s %6s %6s' % ('file', 'slots', 'maxN', 'cntMax', 'recov'))
    for f in files:
        ns, mx = slots[f]
        cm = max([n for n, _ in counts[f]], default=0)
        print('%-32s %6d %6d %6d %6d' % (f, ns, mx, cm, per.get(f, 0)))
    print()
    # the recall denominator: per file take max(distinct slots, max declared count)
    den = {f: max(slots[f][0], max([n for n, _ in counts[f]], default=0)) for f in files}
    prefiles  = [f for f in files if f[:10] <  FLOOR]
    postfiles = [f for f in files if f[:10] >= FLOOR]
    print('RECALL DENOMINATOR = per file max(C4 distinct slot numbers, C5 largest declared count)')
    print('  pre-floor  declared >= %d over %d files; recovered %d'
          % (sum(den[f] for f in prefiles), len(prefiles), sum(per.get(f,0) for f in prefiles)))
    print('  post-floor declared >= %d over %d files; recovered %d'
          % (sum(den[f] for f in postfiles), len(postfiles), sum(per.get(f,0) for f in postfiles)))
    print()
    # post-floor JSON ground truth
    print('POST-FLOOR GROUND TRUTH (analytics/search-results/*.json)')
    gt = {}
    for p in sorted(glob.glob(os.path.join(SR, '*.json'))):
        d = json.load(open(p))
        qs = [c.get('query') for c in d.get('calls', []) if c.get('query')]
        gt[os.path.basename(p)[:10]] = qs
        print('  %s  calls=%d' % (os.path.basename(p), len(qs)))
    print('  total JSON-recorded queries:', sum(len(v) for v in gt.values()))
    json.dump(dict(commit=commit, floor=FLOOR,
                   union={k: v for k, v in union.items()},
                   per_file=dict(per), declared=den,
                   ground_truth=gt),
              open('/tmp/claude-0/-home-user-isds-watcher/51aae013-9850-5f6a-ba40-dbb3f1920362/scratchpad/recovered.json', 'w'), indent=1)

if __name__ == '__main__':
    main()

# ---------------------------------------------------------------------------
# VALIDATION (added same session): the post-floor window 2026-09-20..2026-09-26
# is the ONLY part of the corpus with machine-readable ground truth.  Run the
# prose recoverer against those same daily records and measure precision and
# recall of the classifier there.  Matching rule V1: normalise by lowercasing,
# collapsing runs of whitespace, and stripping ASCII double quotes and the
# characters  ` * — – ; two strings MATCH if one normalised form is a substring
# of the other (a record sometimes quotes a query with a trailing gloss).
def _norm(s):
    s = s.lower().replace('"', ' ').replace('`', ' ')
    for ch in '*—–':
        s = s.replace(ch, ' ')
    return ' '.join(s.split())

def validate():
    import glob, json, os
    commit = subprocess.check_output(['git','-C',REPO,'rev-parse','HEAD']).decode().strip()
    print('\n# VALIDATION against post-floor ground truth, at commit', commit)
    spans = load_spans()
    kept = [s for s in spans if not is_identifier_not_query(s['span'])]
    t1 = [s for s in kept if len(s['span'].split()) >= 4 and RE_ANCHOR.search(s['ctx'])]
    t1k = {(s['file'], s['line'], s['span']) for s in t1}
    t2o = [s for s in kept if is_query_shaped(s['span'])
           and (s['file'], s['line'], s['span']) not in t1k]
    TP=FN=0; found=[]; missed=[]
    gtn_all=[]
    for p in sorted(glob.glob(os.path.join(SR, '*.json'))):
        day = os.path.basename(p)[:10]
        d = json.load(open(p))
        prose = [s['span'] for s in t1 + t2o if s['file'].startswith(day)]
        pn = [_norm(x) for x in prose]
        for c in d.get('calls', []):
            q = c.get('query')
            if not q: continue
            n = _norm(q); gtn_all.append((day,n))
            hit = any(n in x or x in n for x in pn)
            if hit: TP+=1; found.append((day,q))
            else: FN+=1; missed.append((day,q))
    print('ground-truth queries in window:', TP+FN)
    print('  recovered from prose by the classifier (TP):', TP)
    print('  present in JSON but NOT recovered from prose (FN):', FN)
    for day,q in missed: print('    MISS %s  %s' % (day, q[:150]))
    # precision: prose hits in the window that do NOT match any ground-truth query
    gts = [n for _,n in gtn_all]
    extra=[]
    for s in t1+t2o:
        day=s['file'][:10]
        if day < FLOOR or day=='2026-09-27': continue
        n=_norm(s['span'])
        if not any(n in g or g in n for g in gts): extra.append((day,s['line'],s['span']))
    print('  prose spans in window flagged as queries with NO ground-truth match (FP):', len(extra))
    for day,ln,sp in extra[:200]: print('    FP %s:%d  %s' % (day,ln,sp[:150]))

if __name__ == '__main__' and '--validate' in sys.argv:
    validate()
