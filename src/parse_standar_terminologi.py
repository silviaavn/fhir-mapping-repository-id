import pdfplumber, re, json
pdf=pdfplumber.open('std.pdf')
HEAD=re.compile(r'^(\d+)\.(\d+)\s+([A-Z][A-Za-z]+\.[A-Za-z0-9.:\[\]\-_ ]+?)\s*$')
RES=re.compile(r'^(\d+)\.\s+Resource\s+(\w+)')
secs=[]; cur=None; curres=None; last_map=None
def clean(c): return re.sub(r'\s+',' ',(c or '').replace('-\n','-')).strip()
def csys(c): return re.sub(r'\s+','',(c or ''))
for pi in range(27,len(pdf.pages)):
    pg=pdf.pages[pi]
    words_lines=[]
    tables=pg.find_tables(table_settings={"text_x_tolerance":1.5})
    tb=[t.bbox for t in tables]
    def intable(y): return any(b[1]-1<=y<=b[3]+1 for b in tb)
    lines=pg.extract_text_lines()
    items=[]
    for l in lines:
        if intable(l['top']): continue
        items.append((l['top'],'L',l['text']))
    for t in tables: items.append((t.bbox[1],'T',t.extract(x_tolerance=1.5)))
    items.sort(key=lambda x:x[0])
    for y,k,x in items:
        if k=='L':
            s=x.strip()
            if s.startswith('BUKU PANDUAN') or s.startswith('SATUSEHAT versi') or s.startswith('Halaman') or re.match(r'^\d+ dari \d+$',s): continue
            m=RES.match(s)
            if m: curres=m.group(2); continue
            m=HEAD.match(s)
            if m and curres and s.split()[1].split('.')[0].lower()[:5]==curres.lower()[:5]:
                cur={'no':m.group(1)+'.'+m.group(2),'path':m.group(3).strip(),'res':curres,'page':pi+1,'rows':[],'note':[]}
                secs.append(cur); last_map=None; continue
            if cur: cur['note'].append(s)
        else:
            if not cur: continue
            rows=x
            if not rows: continue
            hdr=[re.sub(r'\s+','',(c or '')).lower() for c in rows[0]]
            ishdr=not any('http' in (c or '') for c in rows[0]) and any(('system' in h or 'code' in h or 'keterangan' in h or 'display' in h) for h in hdr)
            if ishdr:
                n=len(hdr)
                si=next((i for i,h in enumerate(hdr) if 'system' in h),0)
                di=next((i for i,h in enumerate(hdr) if 'display' in h and i!=si),None)
                ki=next((i for i,h in enumerate(hdr) if 'keterangan' in h or 'definisi' in h or 'deskripsi' in h),None)
                rest=[i for i in range(n) if i not in (si,di,ki) and not hdr[i].startswith('lvl') and hdr[i]!='no']
                ci=next((i for i in rest if i>si),rest[0] if rest else None)
                last_map=dict(si=si,ci=ci,di=di,ki=ki,n=n,hdr=hdr); body=rows[1:]
            else:
                body=rows
            if not last_map: 
                cur['note'].append(' | '.join(clean(c) for c in rows[0])); continue
            M=last_map
            for r in body:
                if len(r)!=M['n']:
                    # try pad
                    if len(r)<M['n']: r=list(r)+['']*(M['n']-len(r))
                    else: r=r[:M['n']]
                g=lambda i: clean(r[i]) if i is not None else ''
                sysv=csys(r[M['si']]); code=g(M['ci']).replace(' ','') if M['ci'] is not None else ''
                if re.match(r'^[A-Z][A-Za-z]+\.',sysv) or sysv.lower() in ('codesystem','system'): continue
                if sysv and not code and not g(M['di']) and not g(M['ki']) and cur['rows'] and not re.match(r'^(https?:|urn:)',sysv) and not re.match(r'^(https?:|urn:).*(sct|\.org|loinc)$',cur['rows'][-1]['system']):
                    cur['rows'][-1]['system']+=sysv; continue
                if not sysv and not code:
                    # continuation of previous row
                    if cur['rows']:
                        p=cur['rows'][-1]
                        if g(M['di']): p['display']=(p['display']+' '+g(M['di'])).strip()
                        if g(M['ki']): p['ket']=(p['ket']+' '+g(M['ki'])).strip()
                    continue
                cur['rows'].append({'system':sysv,'code':code,'display':g(M['di']),'ket':g(M['ki'])})
out=[s for s in secs]
for s in out:
    for r in s['rows']:
        i=r['system'].find('http')
        if i>0: r['system']=r['system'][i:]+r['system'][:i]
        r['system']=re.sub(r'^(http://snomed\.info/sct).+$',r'\1',r['system'])
    full=set(r['system'] for r in s['rows'])
    for r in s['rows']:
        c=[f for f in full if f!=r['system'] and f.startswith(r['system']) and r['system']]
        if c: r['system']=max(c,key=len)
    s['rows']=[r for r in s['rows'] if r['code'] or r['display']]
for s in out: s['note']=' '.join(s['note'])[:1500]
json.dump(out,open('std.json','w'),ensure_ascii=False,indent=0)
print(len(out), sum(len(s['rows']) for s in out))
import collections
print(collections.Counter(s['res'] for s in out).most_common(60))
