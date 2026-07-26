from ortools.sat.python import cp_model
import json
n = 9
edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
model = cp_model.CpModel()
s = {}
for q in range(7):
    for (u, v) in edges:
        dom = [c for c in range(n) if c not in (u, v)]
        s[(q, u, v)] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(dom), f's{q}_{u}_{v}')
for q in range(7):
    for u in range(n):
        model.AddAllDifferent([s[(q, min(u, v), max(u, v))]
                               for v in range(n) if v != u])
for (u, v) in edges:
    model.AddAllDifferent([s[(q, u, v)] for q in range(7)])
for q in range(6):   # squares interchangeable: sound lex break
    model.Add(s[(q, 0, 1)] < s[(q + 1, 0, 1)])
viol = []
for q in range(7):
    b = model.NewBoolVar(f'noncyc{q}')
    cellb = []
    for (u, v) in edges:
        u2, v2 = sorted(((u + 1) % n, (v + 1) % n))
        c = model.NewBoolVar('')
        d = model.NewIntVar(0, 8, '')
        model.AddModuloEquality(d, s[(q, u, v)] + 1, 9)
        model.Add(s[(q, u2, v2)] != d).OnlyEnforceIf(c)
        model.Add(s[(q, u2, v2)] == d).OnlyEnforceIf(c.Not())
        cellb.append(c)
    model.AddBoolOr(cellb).OnlyEnforceIf(b)
    model.AddBoolAnd([cb.Not() for cb in cellb]).OnlyEnforceIf(b.Not())
    viol.append(b)
model.AddBoolOr(viol)
sv = cp_model.CpSolver()
sv.parameters.max_time_in_seconds = 900
sv.parameters.num_search_workers = 4
st = sv.Solve(model)
print('k8 non-cyclic chart search:', sv.StatusName(st), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [{f'{u},{v}': sv.Value(s[(q, u, v)]) for (u, v) in edges}
           for q in range(7)]
    json.dump(sol, open('k8_noncyclic_chart.json', 'w'))
    print('saved k8_noncyclic_chart.json')
