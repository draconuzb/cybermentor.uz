import re

body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

COMMON = re.compile(r"\b(the|and|is|of|to|in|it|you|that|was|for|on|are|with|as|this|be|at|have|from|or|one|had|by|word|but|not|what|all|were|we|when|your|can|said|there|use|an|each|which|she|do|how|their|if|will|up|other|about|out|many|then|them|these|so|some|her|would|make|like|him|into|time|has|look|two|more|write|go|see|number|no|way|could|people|my|than|first|water|been|call|who|oil|its|now|find|long|down|day|did|get|come|made|may|part)\b", re.I)

def score(s):
    spaces = s.count(' ')
    words = COMMON.findall(s)
    alnum = sum(1 for c in s if c.isalpha())
    return len(words)*10 + spaces + alnum*0.1

def apply(text, LO, RNG, sign, op, step, start, revin, revout, mod5=False):
    s = text[::-1] if revin else text
    out = []
    for i, ch in enumerate(s):
        code = ord(ch)
        shift = start + (i % 5) if mod5 else start + step * i
        if op == 'add':
            newcode = (code - LO + sign * shift) % RNG + LO
        else:
            newcode = code ^ (shift & 0xFF)
            if not (0 <= newcode <= 0x10FFFF):
                newcode = newcode & 0xFF
        try:
            out.append(chr(newcode))
        except ValueError:
            out.append('?')
    r = "".join(out)
    return r[::-1] if revout else r

results = []
for LO, HI in [(33,126),(32,126),(0,255),(1,255),(32,127)]:
    RNG = HI-LO+1
    for sign in [1,-1]:
        for op in ['add','xor']:
            for mod5 in [False, True]:
                for step in [1,-1]:
                    for revin in [False, True]:
                        for revout in [False, True]:
                            v = apply(body, LO, RNG, sign, op, step, 42, revin, revout, mod5)
                            sc = score(v)
                            results.append((sc, LO, HI, sign, op, step, mod5, revin, revout, v))

results.sort(key=lambda x: -x[0])
for r in results[:10]:
    sc, LO, HI, sign, op, step, mod5, revin, revout, v = r
    print(f"score={sc:.1f} LO={LO} HI={HI} sign={sign} op={op} step={step} mod5={mod5} revin={revin} revout={revout}")
    print(repr(v))
    print()
