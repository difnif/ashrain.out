import sys, json; sys.path.insert(0,'/root/esc'); import mathir
zn = sys.argv[1]
n=0
for f in [f'out/{zn}.final.json', f'out/{zn}.final_qamismatch.json', f'out/{zn}.final_figrelax.json', f'out/{zn}.review.json']:
    d = json.load(open('/root/esc/'+f, encoding='utf-8'))
    for x in d:
        o = x.get('final') or x.get('draft'); n+=1
        segs,_,errs = mathir.parse_text(o['question']); assert not errs, (x['id'], errs)
        for c in o['choices'] or []:
            _,_,e = mathir.parse_text(c); assert not e, (x['id'], e)
        if o['answer'] is not None: mathir.parse_answer(o['answer'])
        assert mathir.check_figure(o['figure'] or []) == []
        if o['qtype']=='choice': assert o['choices'] and len(o['choices'])==5, (x['id'], 'choices')
        else: assert o['choices'] is None
        assert o['has_figure'] == bool(o['figure'])
print(zn, "re-verified OK:", n)
