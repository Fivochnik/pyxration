class ball:

    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return isinstance(other, ball) and self.v == other.v

    def __lt__(self, other):
        if isinstance(other, ball):
            return self.v < other.v
        raise TypeError(f'Сравнивать на "<" можно только "ball" и "ball", а не "ball" и "{other.__class__.__name__}"')

    def __le__(self, other):
        if isinstance(other, ball):
            return self.v <= other.v
        raise TypeError(f'Сравнивать на "<=" можно только "ball" и "ball", а не "ball" и "{other.__class__.__name__}"')

if __name__ == '__main__':
    a = ball(1)
    b = ball(1)
    try:
        print(f'{a == b = }')
    except:
        print(f'a == b - неопределенно.')
    try:
        print(f'{a != b = }')
    except:
        print(f'a != b - неопределенно.')
    try:
        print(f'{a < b = }')
    except:
        print(f'a < b - неопределенно.')
    try:
        print(f'{a > b = }')
    except:
        print(f'a > b - неопределенно.')
    try:
        print(f'{a <= b = }')
    except:
        print(f'a <= b - неопределенно.')
    try:
        print(f'{a >= b = }')
    except:
        print(f'a >= b - неопределенно.')
