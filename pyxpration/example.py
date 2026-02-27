from stringolist import stringolist
from exprtree import (
    algebra,
    exprtree,
    operation,
    operInfix,
    operGrouping,
    operPrefix,
    operObject,
    str_tree
)
from functree import (
    funcparam,
    functree
)
from transtree import (
    apply,
    operation_sorter,
    expression_replacer,
    neutrals_deleter,
    zero_absorber
)

plus = operInfix('plus', '+')
mult = operInfix('multiply', '*')
main_group = operGrouping('()', '(', ')')
intObj = operObject('integer', lambda x: x.is_str() and x.to_str().isdigit(), lambda x: int(x.to_str()), lambda x: stringolist(list(str(x))))
varObj = operObject('variable', lambda x: x.is_str() and x.to_str().isidentifier(), lambda x: x.to_str(), lambda x: stringolist(list(x)))

simple = algebra(
    'simple',
    [main_group, plus, mult, intObj, varObj],
    [main_group, intObj, varObj, mult, plus],
    main_group
)

sortPlusMult = operation_sorter([plus, mult])
d0 = '%a%*(%b%+%c%)'
d1 = '%a%*%b%+%a%*%c%'
d0st = stringolist(list(d0))
d1st = stringolist(list(d1))
d0func = simple.new_func(d0st, [funcparam('a'), funcparam('b'), funcparam('c')])
d1func = simple.new_func(d1st, [funcparam('a'), funcparam('b'), funcparam('c')])
simple.order_brackets_del(d0func)
simple.order_brackets_del(d1func)
distr = d0func, d1func
distrToSum = expression_replacer(distr)
ZERO = exprtree(intObj, [0])
ONE = exprtree(intObj, [1])
delNeutrals = neutrals_deleter({'plus': [ZERO], 'multiply': [ONE]})
absorbed = zero_absorber({'multiply': [ZERO]})

a = '12+(0+1*k)+9*a+1*0*(a+b*(0+k)*1)+12*b+3+0+a*(b+c)'
b = '12+1*1*1*0+3+9*a+12*b+(k*1+0)+a*(b+c)+1*(a+b*(k+0))*0'
ast = stringolist(list(a))
bst = stringolist(list(b))
aExpr = simple.new_expr(ast)
bExpr = simple.new_expr(bst)
simple.order_brackets_del(aExpr)
simple.order_brackets_del(bExpr)
print('-' * 50)
print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
print('-' * 50)
print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
print('-' * 50)
aExpr = apply(aExpr, sortPlusMult)
bExpr = apply(bExpr, sortPlusMult)
print('\n' * 9)
print('-' * 50)
print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
print('-' * 50)
print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
print('-' * 50)
aExpr = apply(aExpr, absorbed)
bExpr = apply(bExpr, absorbed)
print('\n' * 9)
print('-' * 50)
print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
print('-' * 50)
print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
print('-' * 50)
aExpr = apply(aExpr, delNeutrals)
bExpr = apply(bExpr, delNeutrals)
print('\n' * 9)
print('-' * 50)
print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
print('-' * 50)
print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
print('-' * 50)
aExpr = apply(aExpr, distrToSum)
bExpr = apply(bExpr, distrToSum)
print('\n' * 9)
print('-' * 50)
print(f'A: {a} = {simple.to_str(aExpr)}:\n{str_tree(aExpr, True)}')
print('-' * 50)
print(f'B: {b} = {simple.to_str(bExpr)}:\n{str_tree(bExpr, True)}')
print('-' * 50)

print(aExpr == bExpr)
