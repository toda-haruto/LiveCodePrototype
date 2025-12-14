import tkinter as tk
from calc_module import variables,calculate
from tutorial import execute,turtle_reset,code,codes,pc

code = ""
codes = []
evaled_code = ""
evaled_codes= []

def run():
    global code,codes,pc
    pc = 0
    code = tf.get("1.0","end").rstrip()
    codes = code.split("\n")
    code_end = len(codes)
    turtle_reset()
    while pc < code_end:
        execute(codes[pc])
        pc += 1

def convert_parentheses(arg):
    converted_arg = ""
    tmp = ""
    n = len(arg)
    count = 0
    for x in range(n):
        ch = arg[x]
        if (count == 0) and (ch == "("):
            count += 1
        elif (count == 1) and (ch == ")"):
            count = 0
            ans = str(calculate(tmp))
            converted_arg += ans
            tmp = ""
        elif (count != 0):
            tmp += ch
            if (ch == "("):
                count += 1
            elif (ch == ")"):
                count -= 1
        else:
            converted_arg += ch
    return converted_arg

def convert_int(arg):
    arg = arg.split("\n")[0]
    if (arg in variables):
        tmp = variables[arg]
        return tmp
    try:
        tmp = float(arg)
        tmp = int(tmp)
        return tmp
    except ValueError:
        return arg
    
def do_LOOP(arg):
    global pc
    count = 0
    loop = arg
    index = pc + 2
    pc1 = index
    pc2 = 0
    while True:
        line = codes[index]
        if (line == "["):
            count += 1
        if (line == "]") and (count == 0):
            pc2 = index - 1
            break
        if (line == "]") and (count != 0):
            count -= 1
        index += 1
    for x in range(loop):
        pc = pc1
        while pc <= pc2:
            eval_line(codes[pc])
            pc += 1
    pc = index

root = tk.Tk()
root.title("LiveCode_prototype")

menu_frame = tk.Frame(root, height=30, bg="#dddddd")
tf = tk.Text(root, width = 40, height = 20)
ta = tk.Text(root, width = 40, height = 20)
Terminal = tk.Text(root, width = 80, height = 5)
btn_run = tk.Button(menu_frame, text="Run", command=run)
btn_run.pack(side="left", padx=5, pady=5)

menu_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
tf.grid(row=1, column=0, sticky="nsew")
ta.grid(row=1, column=1, sticky="nsew")
Terminal.grid(row=2, column=0, columnspan=2, sticky="nsew")

def eval(event):
    global code,codes,evaled_code,evaled_codes,pc
    pc = 0
    evaled_code = ""
    code =  tf.get("1.0","end").rstrip()
    ta.delete("1.0","end")
    codes = code.split("\n")
    code_end = len(codes)
    evaled_codes = [""]*code_end
    while pc < code_end:
        try:
            eval_line(codes[pc])
        except Exception as e:
            pass
        pc += 1
    for x in evaled_codes:
        evaled_code += x + "\n"
    ta.insert(tk.END, evaled_code)

def eval_line(line):
    global pc,evaled_codes
    converted_stm = convert_parentheses(line)
    tokens =  converted_stm.split(" ")
    func = tokens[0]
    args = tokens[1:]
    if func == "FD":
        evaled_codes[pc] =  "FD: " + args[0]
    elif func == "LET":
        variables[args[0]] = convert_int(args[1])
        evaled_codes[pc] = "LET: " + args[0] + " = " + f"{convert_int(args[1])}"
    elif func == "RIGHT":
        evaled_codes[pc] = "RIGHT: " + args[0]
    elif func == "DO":
        evaled_codes[pc] = "LOOP: " + args[0] 
        do_LOOP(convert_int(args[0]))
    elif func == "IF":
        evaled_codes[pc] = ""
    elif func == "DEF":
        evaled_codes[pc] = "DEF : " + args[0]
    else:
        evaled_codes[pc] = ""

tf.bind("<KeyRelease>", eval)

root.mainloop()