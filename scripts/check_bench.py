#!/usr/bin/env python3
"""CI gate for agent-safety-bench-zh. Exit 0 = clean, 1 = problems."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "bench.jsonl")
TOPKEYS = {"id","category","difficulty","context","action","gold","rationale","tags"}
CATS = {"benign","prompt_injection","destructive"}
DIFF = {"easy","medium","hard"}
RISK = {"low","medium","high","critical"}
DIRTY = [re.compile(p, re.I) for p in [
    r"APT\s*\d+", r"(俄罗斯|朝鲜|伊朗|以色列|北约)\s*(黑客|情报|组织|间谍)",
    r"(国家支持|国家赞助|nation[\-\s]state\s+actor)", r"\bLazarus\s*Group\b", r"(地缘政治|geopolit)"]]

def main():
    problems=[]; rows=[]
    for ln,line in enumerate(open(DATA,encoding="utf-8"),1):
        line=line.strip()
        if not line: continue
        try: o=json.loads(line)
        except Exception as e: problems.append(f"L{ln} invalid JSON: {e}"); continue
        rows.append(o)
        if set(o.keys())!=TOPKEYS: problems.append(f"{o.get('id','?')} bad keys {sorted(o.keys())}")
        if o.get("category") not in CATS: problems.append(f"{o.get('id')} bad category")
        if o.get("difficulty") not in DIFF: problems.append(f"{o.get('id')} bad difficulty")
        g=o.get("gold",{})
        if g.get("decision") not in {"allow","block"}: problems.append(f"{o.get('id')} bad decision")
        if g.get("risk") not in RISK: problems.append(f"{o.get('id')} bad risk")
        # constraint: benign<->allow, others<->block
        if o.get("category")=="benign" and g.get("decision")!="allow":
            problems.append(f"{o.get('id')} benign must be allow")
        if o.get("category") in {"prompt_injection","destructive"} and g.get("decision")!="block":
            problems.append(f"{o.get('id')} {o.get('category')} must be block")
        if not str(o.get("rationale","")).strip() or len(o.get("rationale",""))<10:
            problems.append(f"{o.get('id')} rationale too short")
        blob=json.dumps(o,ensure_ascii=False)
        for r in DIRTY:
            m=r.search(blob)
            if m: problems.append(f"{o.get('id')} purity violation: {m.group()!r}")
    # uniqueness
    ids=[r["id"] for r in rows]
    if len(ids)!=len(set(ids)): problems.append("duplicate id(s) present")
    sig=[json.dumps(r["action"],ensure_ascii=False)+r["context"] for r in rows]
    if len(sig)!=len(set(sig)): problems.append("duplicate context+action present")
    # ratio band + difficulty coverage
    n=len(rows) or 1
    from collections import Counter
    c=Counter(r["category"] for r in rows)
    if not (0.30<=c["benign"]/n<=0.50): problems.append(f"benign ratio out of band: {c['benign']/n:.0%}")
    if not (0.20<=c["prompt_injection"]/n<=0.40): problems.append("injection ratio out of band")
    if not (0.20<=c["destructive"]/n<=0.40): problems.append("destructive ratio out of band")
    for cat in CATS:
        diffs={r["difficulty"] for r in rows if r["category"]==cat}
        if "easy" not in diffs and "hard" not in diffs: problems.append(f"{cat} lacks difficulty spread")
    print(f"checked {len(rows)} samples; categories={dict(c)}")
    if problems:
        print(f"\nFAIL — {len(problems)} issue(s):")
        for p in problems[:60]: print("  -",p)
        print("\nFix the real gap. Do NOT pass by deleting samples or labels.")
        return 1
    print("PASS — schema ok, constraints hold, unique, ratios in band, purity clean.")
    return 0
if __name__=="__main__": sys.exit(main())
