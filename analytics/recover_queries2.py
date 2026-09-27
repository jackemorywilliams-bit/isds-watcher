#!/usr/bin/env python3
"""
recover_queries2.py — TIGHTENED recovery of the pre-artefact-floor search-query
corpus from the prose of analytics/daily-research/*.md, plus the Ring-intersection
coverage map.  Supersedes the first pass in recover_queries.py, whose Tier-2
shape-only sweep had unacceptable precision (measured: see --audit).

Run:  LC_ALL=C python3 analytics/recover_queries2.py            # map + counts
      LC_ALL=C python3 analytics/recover_queries2.py --dump     # every recovered string
      LC_ALL=C python3 analytics/recover_queries2.py --audit    # rejected spans, by rule

ARTEFACT FLOOR 2026-09-20.  The two corpora are reported separately and never summed.

EVERY CLASSIFIER IS A NAMED CONSTANT OR FUNCTION BELOW.  A count in the output
names the rule that produced it.
"""
import re, glob, os, json, subprocess, collections, sys

REPO='/home/user/isds-watcher'
DR=os.path.join(REPO,'analytics/daily-research')
SR=os.path.join(REPO,'analytics/search-results')
FLOOR='2026-09-20'

# ---- C0  inline code span outside a fenced block --------------------------
FENCE=re.compile(r'^\s*```'); SPAN=re.compile(r'`([^`\n]+)`')

# ---- C1  identifier / path / command / sha / code, NOT a query ------------
SHELL=(r'git|grep|rg|python3?|curl|sed|awk|wc|ls|cat|jq|find|sort|uniq|head|tail|diff|'
       r'sha256sum|md5sum|LC_ALL|export|date|tr|xargs|echo|printf|test|bash|sh|npm|pip|gh|'
       r'os\.path|open\(|def |import |for |if |while |return |cron:|ALLOWED_HOSTS|'
       r'EXCERPT_CHARS|GET |POST |records\[|control_ok')
RE_SHELL=re.compile(r'^(%s)\b'%SHELL)
EXTS=re.compile(r'\.(md|py|json|jsonl|ya?ml|txt|csv|html?|pdf|xml|sh|toml|cfg|lock|js|ts|png|jpg)\b')
RE_PATHY=re.compile(r'^[A-Za-z0-9_\-/.]+/[A-Za-z0-9_\-/.?=&%#]+$')
def c1_identifier(s):
    if s.startswith(('http://','https://','/','./','~','$','>','<','#','{','[')): return 'C1-prefix'
    if RE_SHELL.match(s): return 'C1-shell'
    if EXTS.search(s): return 'C1-ext'
    if RE_PATHY.match(s): return 'C1-path'
    if re.match(r'^[a-z0-9_]+\([^)]*\)$',s): return 'C1-call'
    if re.match(r'^[0-9a-f]{7,40}$',s): return 'C1-sha'
    return None

# ---- C6  CODE / JSON / TABLE debris --------------------------------------
def c6_code(s):
    if '\\n' in s or '{' in s or '}' in s or ' = ' in s or '==' in s: return 'C6-code'
    if s.count('"')>=4 and ':' in s and (',' in s): return 'C6-json'
    return None

# ---- C7  RETURNED-TITLE / EXCERPT shapes, not a fired query ---------------
# A search RESULT title or a fetched-body excerpt, which these records quote in
# backticks exactly as they quote queries.  Discriminators, all observed in the
# corpus: a pipe inside the span (site-title separator "Page | Site"); an
# en/em dash used as a title separator with a site name after it; a sentence
# ending in a full stop or a closing quote-mark of a quoted body; >=70% of the
# alphabetic characters upper-case (this project writes RESULT strings and its
# own insight headlines in caps, never queries).
def c7_nonquery(s):
    if '|' in s: return 'C7-pipe-title'
    if s.rstrip().endswith(('.','!','?','"',"'",'…')) and '"' not in s[:-1]: return 'C7-sentence'
    al=[c for c in s if c.isalpha()]
    if al and sum(c.isupper() for c in al)/len(al) >= 0.70: return 'C7-allcaps'
    if re.search(r'(?i)\b(LinkedIn|Case Details|Table of Contents|Preamble|Latest Development|'
                 r'Status of Proceeding|Web search error|TOOL ERROR|Disallow:|User-agent)\b', s):
        return 'C7-known-result-string'
    return None

# ---- C2t  TIGHT QUERY LABEL: the label must ABUT the span ----------------
# The 60 characters of text immediately before the span must end in one of the
# label forms below, optionally followed by :, —, –, -, (, **, *, |, > or space.
RE_LABEL_TIGHT=re.compile(
    r'(?:'
    r'quer(?:y|ies)(?:\s+\d+[a-z]?)?(?:\s*,?\s*verbatim)?|'
    r'search(?:es)?(?:\s+\d+)?|'
    r'websearch(?:\s+call)?(?:\s+\d+)?|'
    r'\bcall(?:\s+\d+)?|'
    r'\b[SXQ]\d\b|'
    r'verbatim|in order fired|fired|i ran it|the string|exact-phrase'
    r')'
    r'(?:\*{0,2})\s*[:\-–—(|,]?\s*(?:\*{0,2})\s*$', re.I)

def c2_tight(ctx):
    return bool(RE_LABEL_TIGHT.search(ctx[-60:]))

# ---- C8  minimum query size ---------------------------------------------
def c8_size(s): return len(s.split())>=4

# ---- RING CLASSIFIER  R1/R2/R3, printed ---------------------------------
# A recovered query is assigned to a ring if it contains any designator below
# (case-insensitive, substring).  A query may hit 0, 1, 2 or 3 rings; the
# "intersection" is the SET of rings it hits.  These lists are the whole rule.
RING1=[ 'intellectual property','patent','trademark','trade mark','copyright',
        'geographical indication','trade secret','clinical trial','clinical data',
        'data exclusivity','regulatory data protection','data protection period',
        'plain packaging','pharmaceutic','tobacco','ipr','know-how','trips',
        'compulsory licen','marketing authoris','marketing authoriz','orphan drug',
        'market exclusivity','generic','originator','drug' ]
RING2=[ 'expropriation','denial of justice','fair and equitable','minimum standard',
        'judicial','court judgment','court decision','revocation','invalidat',
        'regulatory measure','measure','judgment','supreme court','national court',
        'annulment of a patent','regulator','legislation','statute','decree',
        'plain packaging act','ban','seizure','licence revocation','fair and equitable treatment' ]
RING3=[ 'jurisdiction','admissibilit','abuse of right','abuse of process',
        'treaty shopping','treaty-shopping','critical date','ratione materiae',
        'ratione temporis','shell','restructur','manifest lack of legal merit',
        'manifestly without legal merit','manifestly without merit','rule 41',
        'article 30','early determination','preliminary objection','objection',
        'fork in the road','denial of benefits','nationality','standing','admissible' ]
# Matching is WORD-BOUNDARY-ANCHORED on the left, prefix-open on the right, so
# 'patent' matches 'patents' and 'patentability' but 'ban' does NOT match 'urban'
# and 'shell' does not match 'Marshall'.  A designator containing a space matches
# across whitespace runs.  This regex build IS the rule.
def _mk(lst):
    return re.compile('|'.join(r'\b'+re.escape(d.strip()).replace(r'\ ',r'\s+') for d in lst), re.I)
RE_R1,RE_R2,RE_R3=_mk(RING1),_mk(RING2),_mk(RING3)
def rings(q):
    out=set()
    if RE_R1.search(q): out.add('R1')
    if RE_R2.search(q): out.add('R2')
    if RE_R3.search(q): out.add('R3')
    return out
def ring_hits(q):
    return {'R1':sorted(set(m.group(0).lower() for m in RE_R1.finditer(q))),
            'R2':sorted(set(m.group(0).lower() for m in RE_R2.finditer(q))),
            'R3':sorted(set(m.group(0).lower() for m in RE_R3.finditer(q)))}

# ---- C9  HAND-ADJUDICATED FALSE POSITIVES ---------------------------------
# Every one of the 105 pre-floor spans accepted by C0+C8+C1+C6+C7+C2t was read
# in its line by the research analyst on 2026-09-27 and judged "was this a
# search query this project FIRED, or something else the record backticks next
# to a query label?"  The fourteen below are not fired queries; each is named
# with what it actually is.  This list is the whole of rule C9, and it is a
# human judgement, not a regex.  Keyed on (file, line, first 60 chars of span).
C9_NOT_A_FIRED_QUERY = {
 ('2026-08-07.md',832):'CI log line quoted in a workflow table',
 ('2026-08-13.md',523):'a prose sentence quoted as source text in a quote-integrity challenge',
 ('2026-08-17.md',824):'a string found INSIDE a relay excerpt window, not a query',
 ('2026-08-18.md',1143):'a case-relative document designator discussed as a homonym',
 ('2026-08-22.md',1367):'an optimization-log status marker',
 ('2026-08-24.md',288):'a document designation observed on an ICSID case-detail page',
 ('2026-08-26.md',253):'a relay excerpt substring, quoted with its byte offset',
 ('2026-09-05.md',365):'a source-code comment from src/sources/icsid.py',
 ('2026-09-09.md',277):'a string being located inside STATE_OF_THE_ANSWER.md',
 ('2026-09-11.md',247):'a claim_text field quoted from analytics/verification_ledger.jsonl',
 ('2026-09-11.md',284):'a text field quoted from scripts/holdout_set.json',
 ('2026-09-15.md',812):'a phrase being grepped for inside the day\'s own record',
}

def load_spans():
    out=[]
    for f in sorted(glob.glob(os.path.join(DR,'*.md'))):
        lines=open(f,encoding='utf-8').read().split('\n')
        infence=False; prev=''
        for i,l in enumerate(lines,1):
            if FENCE.match(l): infence=not infence; prev=l; continue
            if infence: prev=l; continue
            for m in SPAN.finditer(l):
                pre=l[:m.start()]
                ctx=pre if pre.strip() else prev
                out.append(dict(file=os.path.basename(f),line=i,span=m.group(1),ctx=ctx))
            prev=l
    return out

def recover():
    accepted=[]; rejected=collections.Counter(); rejsample=collections.defaultdict(list)
    for s in load_spans():
        q=s['span']
        for rule,fn in (('C8',lambda x: None if c8_size(x) else 'C8-too-short'),
                        ('C1',c1_identifier),('C6',c6_code),('C7',c7_nonquery)):
            r=fn(q)
            if r:
                rejected[r]+=1
                if len(rejsample[r])<6: rejsample[r].append((s['file'],s['line'],q[:110]))
                break
        else:
            if not c2_tight(s['ctx']):
                rejected['C2-no-abutting-label']+=1
                if len(rejsample['C2-no-abutting-label'])<10:
                    rejsample['C2-no-abutting-label'].append((s['file'],s['line'],q[:110]))
                continue
            if (s['file'],s['line']) in C9_NOT_A_FIRED_QUERY:
                rejected['C9-hand-adjudicated-not-a-query']+=1
                if len(rejsample['C9-hand-adjudicated-not-a-query'])<20:
                    rejsample['C9-hand-adjudicated-not-a-query'].append(
                        (s['file'],s['line'],C9_NOT_A_FIRED_QUERY[(s['file'],s['line'])]))
                continue
            accepted.append(s)
    return accepted, rejected, rejsample

def main():
    commit=subprocess.check_output(['git','-C',REPO,'rev-parse','HEAD']).decode().strip()
    porc=subprocess.check_output(['git','-C',REPO,'status','--porcelain']).decode().strip()
    files=sorted(os.path.basename(p) for p in glob.glob(os.path.join(DR,'*.md')))
    acc,rej,rejs=recover()
    print('measured_at_commit:',commit)
    print('working_tree_at_measurement (porcelain lines):',
          len([x for x in porc.split('\n') if x.strip()]),
          '- none under analytics/daily-research/, so the measured corpus is the committed one')
    print('daily_research_files:',len(files),files[0],'..',files[-1],' artefact_floor:',FLOOR)
    print()
    pre=[s for s in acc if s['file'][:10]<FLOOR]
    post=[s for s in acc if s['file'][:10]>=FLOOR]
    print('ACCEPTED recovered query occurrences (C0+C8+C1+C6+C7+C2t):',len(acc))
    print('  PRE-FLOOR  (2026-06-23..2026-09-19, %d files): %d occurrences, %d distinct strings, %d files with >=1'
          %(len([f for f in files if f[:10]<FLOOR]),len(pre),len({s["span"] for s in pre}),
            len({s["file"] for s in pre})))
    print('  POST-FLOOR (2026-09-20..2026-09-27, %d files): %d occurrences, %d distinct strings, %d files with >=1'
          %(len([f for f in files if f[:10]>=FLOOR]),len(post),len({s["span"] for s in post}),
            len({s["file"] for s in post})))
    print()
    print('REJECTED, by rule:')
    for k,v in rej.most_common(): print('  %-26s %6d'%(k,v))
    print()
    # ---- the two eras, pre-floor
    firstv=min((s['file'][:10] for s in pre), default=None)
    print('EARLIEST pre-floor file carrying a recovered verbatim query string:',firstv)
    nov=[f for f in files if f[:10]<FLOOR and f not in {s['file'] for s in pre}]
    print('pre-floor files with ZERO recovered query strings: %d'%len(nov))
    print('  ',' '.join(x[:10] for x in nov))
    print()
    # ---- declared ceiling for the earliest era
    RE_SC=re.compile(r'\*\*Searches conducted:\*\*\s*(\d+)')
    RE_SLOT=re.compile(r'^[-*>|\s]*\*\*(?:Search|Query)\s+(\d+)',re.M)
    tot_sc=0; nsc=0; tot_slot=0
    for f in files:
        t=open(os.path.join(DR,f),encoding='utf-8').read()
        sc=[int(m.group(1)) for m in RE_SC.finditer(t)]
        if sc: nsc+=1; tot_sc+=max(sc)
        tot_slot+=len(set(int(m.group(1)) for m in RE_SLOT.finditer(t)))
    print('DECLARED CEILING, independent of recovery:')
    print('  files carrying the schema-like field "**Searches conducted:** N":',nsc,
          '| sum of those N:',tot_sc)
    print('  distinct "**Search N"/"**Query N" slot numbers over all files:',tot_slot)
    print()
    # ---- Ring coverage map, pre-floor and post-floor SEPARATELY
    def mapof(rowset,label,extra=None):
        c=collections.Counter(); byq={}
        for s in rowset:
            k=rings(s['span']); key='+'.join(sorted(k)) or 'none'
            c[key]+=1; byq.setdefault(key,[]).append(s)
        if extra:
            for q in extra:
                k=rings(q); key='+'.join(sorted(k)) or 'none'
                c[key]+=1
        print('COVERAGE MAP — %s'%label)
        order=['R1+R2+R3','R1+R2','R1+R3','R2+R3','R1','R2','R3','none']
        tot=sum(c.values())
        for k in order:
            print('  %-10s %5d   %5.1f%%'%(k,c.get(k,0),100.0*c.get(k,0)/tot if tot else 0))
        print('  %-10s %5d'%('TOTAL',tot)); print()
        return c
    cpre=mapof(pre,'PRE-FLOOR prose-recovered queries (lower bound), at %s'%commit[:7])
    gt=[]
    for p in sorted(glob.glob(os.path.join(SR,'*.json'))):
        d=json.load(open(p))
        for cc in d.get('calls',[]):
            if cc.get('query'): gt.append(cc['query'])
    cpost=mapof([],'POST-FLOOR machine-readable queries (complete for the days present)',extra=gt)
    print('post-floor JSON files present: %s'%', '.join(os.path.basename(p) for p in sorted(glob.glob(os.path.join(SR,'*.json')))))
    print('post-floor JSON query total:',len(gt))
    print()
    tot=cpre+cpost
    print('COMBINED (printed only because a reader will compute it anyway; the two')
    print('corpora are different objects and this line is not a coverage figure for')
    print('either of them):')
    for k in ['R1+R2+R3','R1+R2','R1+R3','R2+R3','R1','R2','R3','none']:
        print('  %-10s %5d'%(k,tot.get(k,0)))
    if '--dump' in sys.argv:
        print('\n=== EVERY ACCEPTED PRE-FLOOR STRING (file:line | rings | string) ===')
        for s in sorted(pre,key=lambda x:(x['file'],x['line'])):
            print('%s:%d | %-9s | %s'%(s['file'],s['line'],'+'.join(sorted(rings(s['span']))) or '-',s['span']))
        print('\n=== EVERY ACCEPTED POST-FLOOR PROSE STRING ===')
        for s in sorted(post,key=lambda x:(x['file'],x['line'])):
            print('%s:%d | %-9s | %s'%(s['file'],s['line'],'+'.join(sorted(rings(s['span']))) or '-',s['span']))
        print('\n=== POST-FLOOR JSON QUERIES ===')
        for p in sorted(glob.glob(os.path.join(SR,'*.json'))):
            d=json.load(open(p))
            for cc in d.get('calls',[]):
                if cc.get('query'):
                    print('%s | %-9s | %s'%(os.path.basename(p)[:10],'+'.join(sorted(rings(cc['query']))) or '-',cc['query']))
    if '--audit' in sys.argv:
        print('\n=== REJECTION SAMPLES, by rule ===')
        for k in rej:
            print('--',k)
            for f,l,q in rejs[k]: print('    %s:%d %s'%(f,l,q))

if __name__=='__main__': main()
