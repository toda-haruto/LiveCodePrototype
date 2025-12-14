#test = "( ( x + 2 ) * 3 + 4 ) * 5"

idx = 0
p = []
variables = {}

def calculate(s):
    global idx
    idx = 0
    tmp = s.split(" ")
    E(tmp)
    stack = []
    for x in range(len(p)):
        if p[x] == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif p[x] == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif p[x] == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif p[x] == "/":
            a = stack.pop()
            b = stack.pop()
            stack.append(b / a)
        else:
            stack.append(p[x])
    return stack.pop()

def E(s):
    global idx
    next = s[idx]
    T(s)
    while idx < len(s):
        next = s[idx]
        if ((next != "+") and (next != "-")):break
        idx += 1
        T(s)
        p.append(next)

def T(s):
    global idx
    next = s[idx]
    F(s)
    while idx < len(s):
        next = s[idx]
        if ((next != "*") and (next != "/")): break
        idx += 1
        T(s)
        p.append(next)

def F(s):
    global idx
    next = s[idx]
    if (next == "("):
        idx += 1
        E(s)
        next = s[idx]
        if (next == ")"):
            idx += 1
    elif (next.isdigit()):
        p.append(int(next))
        idx += 1
    else:
        p.append(int(variables[next]))
        idx += 1

#calculate(test)