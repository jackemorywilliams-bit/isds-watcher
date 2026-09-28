#!/usr/bin/env python3
"""
designator_census.py — which RING DESIGNATORS have ever fired on the canonical
post-floor query census, and which have NEVER fired.

WHY A THIRD .py UNDER analytics/.  `analytics/` is a records directory and a .py
file here is the acknowledged category error already escalated to Emory
(2026-09-27 ruling 7.3(6)).  This file is the third.  It is here and not under
scripts/ because scripts/ is outside this session's write scope; and it exists
at all rather than as a heredoc because the 2026-09-27 close-out (§7.7 item 6)
directs that a rule which lives in an ephemeral script must be declared as such
in the same sentence as its number, and a committed program writing a committed
artefact is preferred.

IT RE-IMPLEMENTS NOTHING.  RING1/RING2/RING3, the regex builder `_mk` and the
matcher `rings` are IMPORTED from analytics/recover_queries2.py, which is
tracked at HEAD.  This is deliberate: `0927-C1` was sustained because a printed
classifier was not the classifier that ran.  Here there is only one classifier
and it is the committed one.

THE CENSUS POPULATION, stated so it cannot be widened by accident:
  every  calls[].query  string in every  analytics/search-results/*.json ,
  i.e. the POST-FLOOR machine-readable corpus only.  The prose of a daily
  record is NOT a census (adopted binding 2026-09-27 §7.3(2)) and is not read
  by this program.  Era 1 (before 2026-08-01) is unrecorded as to content; Era 2
  (2026-08-01..2026-09-19) survives only as a prose LOWER BOUND and is likewise
  not read here.

Run:  LC_ALL=C python3 analytics/designator_census.py
      LC_ALL=C python3 analytics/designator_census.py --json
"""
import os, sys, glob, json, re, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recover_queries2 as RQ          # the committed classifier, imported not retyped

REPO = RQ.REPO
SR   = RQ.SR

RINGS = {'R1': RQ.RING1, 'R2': RQ.RING2, 'R3': RQ.RING3}

def census_queries():
    """The population. One rule, printed in the docstring, executed here."""
    rows = []
    for p in sorted(glob.glob(os.path.join(SR, '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        for c in d.get('calls', []):
            q = c.get('query')
            if q:
                rows.append((os.path.basename(p)[:10], c.get('id'), q))
    return rows

def main():
    commit = subprocess.check_output(['git','-C',REPO,'rev-parse','HEAD']).decode().strip()
    porc   = subprocess.check_output(['git','-C',REPO,'status','--porcelain']).decode()
    porc   = [l for l in porc.split('\n') if l.strip()]
    rows   = census_queries()
    files  = sorted(os.path.basename(p) for p in glob.glob(os.path.join(SR,'*.json')))

    out = {
      'measured_at_commit': commit,
      'porcelain_lines_at_measurement': len(porc),
      'porcelain_at_measurement': porc,
      'census_files': files,
      'census_size_queries': len(rows),
      'census_date_window': [files[0][:10], files[-1][:10]] if files else None,
      'population_rule': 'every calls[].query in every analytics/search-results/*.json; prose not read',
      'classifier_source': 'analytics/recover_queries2.py RING1/RING2/RING3 + _mk(), imported',
      'rings': {},
    }

    for rname, lst in RINGS.items():
        fired, never = [], []
        for d in lst:
            rx = RQ._mk([d])
            hits = [(dt, cid, m.group(0)) for dt, cid, q in rows for m in [rx.search(q)] if m]
            if hits:
                fired.append({'designator': d, 'n_queries': len(hits),
                              'last_fired': max(h[0] for h in hits),
                              'matched_tokens': sorted({h[2].lower() for h in hits})})
            else:
                never.append(d)
        out['rings'][rname] = {
          'n_designators': len(lst),
          'n_fired': len(fired),
          'n_never_fired': len(never),
          'never_fired': never,
          'fired': sorted(fired, key=lambda x: -x['n_queries']),
        }

    tot  = sum(v['n_designators'] for v in out['rings'].values())
    nev  = sum(v['n_never_fired'] for v in out['rings'].values())
    out['total_designators'] = tot
    out['total_never_fired'] = nev

    # ---- SECONDARY POPULATION, EXPRESSLY NOT A CENSUS ---------------------
    # The pre-floor prose-recovered strings.  This is a LOWER BOUND recovered
    # by recover_queries2.recover() and the 2026-09-27 ruling forbids counting
    # the prose of a daily record as a census of anything.  It is computed here
    # for ONE purpose only: to reconcile today's census figure against the
    # 2026-09-27 figure, which was taken over the UNION of this lower bound and
    # the census.  A designator "never fired" over the union is a STRONGER
    # statement than "never fired" over the census alone.
    acc, _, _ = RQ.recover()
    pre = [s['span'] for s in acc if s['file'][:10] < RQ.FLOOR]
    union = pre + [q for _, _, q in rows]
    out['secondary_population_prefloor_prose_lower_bound'] = {
        'WARNING': 'NOT A CENSUS. Prose lower bound, per 2026-09-27 ruling 7.3(2).',
        'n_strings': len(pre),
        'n_union_with_census': len(union),
        'rings': {},
    }
    for rname, lst in RINGS.items():
        nev_pre, nev_union = [], []
        for d in lst:
            rx = RQ._mk([d])
            if not any(rx.search(q) for q in pre):   nev_pre.append(d)
            if not any(rx.search(q) for q in union): nev_union.append(d)
        out['secondary_population_prefloor_prose_lower_bound']['rings'][rname] = {
            'never_fired_prefloor_prose_only': nev_pre,
            'never_fired_over_union': nev_union,
            'n_never_fired_over_union': len(nev_union),
        }
    out['secondary_population_prefloor_prose_lower_bound']['total_never_fired_over_union'] = sum(
        v['n_never_fired_over_union']
        for v in out['secondary_population_prefloor_prose_lower_bound']['rings'].values())

    if '--json' in sys.argv:
        print(json.dumps(out, indent=1)); return

    print('measured_at_commit:', commit)
    print('porcelain lines at measurement:', len(porc))
    for l in porc: print('   ', l)
    print('census files (%d): %s' % (len(files), ', '.join(f[:10] for f in files)))
    print('census size: %d query strings  window %s..%s'
          % (len(rows), out['census_date_window'][0], out['census_date_window'][1]))
    print('POPULATION RULE:', out['population_rule'])
    print('CLASSIFIER:', out['classifier_source'])
    print()
    for rname in ('R1','R2','R3'):
        v = out['rings'][rname]
        print('%s: %d designators, %d fired, %d NEVER fired'
              % (rname, v['n_designators'], v['n_fired'], v['n_never_fired']))
        print('   NEVER: ' + ', '.join(repr(d) for d in v['never_fired']))
        for f in v['fired']:
            print('   fired  %-28s n=%-3d last=%s  tokens=%s'
                  % (repr(f['designator']), f['n_queries'], f['last_fired'],
                     ','.join(f['matched_tokens'])))
        print()
    print('TOTAL: %d designators, %d never fired on the post-floor census' % (tot, nev))
    sec = out['secondary_population_prefloor_prose_lower_bound']
    print()
    print('--- SECONDARY POPULATION (%s) ---' % sec['WARNING'])
    print('pre-floor prose-recovered strings: %d ; union with census: %d'
          % (sec['n_strings'], sec['n_union_with_census']))
    for rname in ('R1','R2','R3'):
        v = sec['rings'][rname]
        print('%s never-fired OVER THE UNION: %d -> %s'
              % (rname, v['n_never_fired_over_union'],
                 ', '.join(repr(d) for d in v['never_fired_over_union'])))
    print('TOTAL never fired over the union: %d of %d'
          % (sec['total_never_fired_over_union'], tot))

if __name__ == '__main__':
    main()
