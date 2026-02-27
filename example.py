import pyxpration as pyx
from pyxpration import transtree as pyxt

#Константы:
strlstFalse = pyx.stringolist('0')
strlstTrue = pyx.stringolist('1')

#Операции и объекты:
Brackets = pyx.operGrouping('brackets', '(', ')')
OpAnd = pyx.operInfix('and', '&')
OpOr = pyx.operInfix('or', '|')
OpImp = pyx.operInfix('implication', '->')
OpNot = pyx.operPrefix('not', '~')
ObjBool = pyx.operObject('boolean',
                         lambda x: x.is_str() and x.to_str().isdigit(),
                         lambda x: x == strlstTrue,
                         lambda x: strlstTrue if x else strlstFalse)
ObjVar = pyx.operObject('variable',
                        lambda x: x.is_str() and x.to_str().isidentifier(),
                        lambda x: x.to_str(),
                        lambda x: pyx.stringolist(list(x)))

#Алгебра:
classicLogics = pyx.algebra('classic logics',
                            [Brackets, OpImp, OpOr, OpAnd, OpNot, ObjBool, ObjVar],
                            [Brackets, ObjBool, ObjVar, OpNot, OpAnd, OpOr, OpImp],
                            Brackets)

#Константные выражения:
exprFalse = classicLogics.new_expr('0')
exprTrue = classicLogics.new_expr('1')

#Функции преобразования:
delNeutrals = pyxt.neutrals_deleter(
    {
        'and': [exprTrue],
        'or': [exprFalse]
    }
)
absorbe = pyxt.zero_absorber(
    {
        'and': [exprFalse],
        'or': [exprTrue]
    }
)

if __name__ == '__main__':
    aExpr = classicLogics.new_expr('(A|B|0)&(C|1|D)->A&B&0|C&1&D')
    print(classicLogics.to_str(aExpr) + ':')
    print(pyx.str_tree(aExpr, True))
    
    aExpr = pyxt.apply(aExpr, absorbe)
    print(classicLogics.to_str(aExpr) + ':')
    print(pyx.str_tree(aExpr, True))
    
    aExpr = pyxt.apply(aExpr, delNeutrals)
    print(classicLogics.to_str(aExpr) + ':')
    print(pyx.str_tree(aExpr, True))
