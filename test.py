import pyxpration as pyx

power = pyx.operInfix('power', '^')

variable = pyx.operObject(
    'variable',
    lambda x: x.is_str() and x.to_str().isidentifier(),
    lambda x: x.to_str(),
    lambda x: pyx.stringolist(list(x))
)

alg = pyx.algebra(
    'one',
    [power, variable],
    [variable, power]
)

exp1 = alg.new_func('e^%x%')
exp2 = power(variable('e'), pyx.funcparam('x'))
print(
    'exp1 = ' + alg.to_str(exp1),
    pyx.str_tree(exp1, True),
    '=' * 50,
    'exp2 = ' + alg.to_str(exp2),
    pyx.str_tree(exp2, True),
    '=' * 50,
    f'{exp1 == exp2 = }',
    sep = '\n')
