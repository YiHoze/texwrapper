import os, argparse
from random import randint
parser = argparse.ArgumentParser(
    description = 'Pick lottery numbers.'
)
parser.add_argument(
    'frequency',
    type = int,
    nargs = '?',
    default = 5
)
parser.add_argument(
   '-p',
   dest = 'print',
   action = 'store_true',
   default = False,
   help = 'Print lottery numbers in PDF using LuaLaTeX.'
)
args = parser.parse_args()

def display_on_console():
    m, n = 6, 45
    balls = []
    tmps = []
    for x in range(args.frequency):
        balls.clear()
        tmps.clear()
        for i in range(n-m+1, n+1):
            drawn = randint(1, i) 
            already = False
            for j in range(len(balls)):
                if balls[j] == drawn:            
                    already = True
            if not already:
                balls.append(drawn)
            else:
                balls.append(i)
        balls.sort()
        print(balls)

def generate_pdf():    
    if os.path.exists('lotto.tex'):
        os.remove('lotto.tex')        
    content = """
    \\documentclass{article}
    \\usepackage{xparse, expl3}
    \\usepackage{luacode}
    \\usepackage{tikz}
    \\newcommand\\DrawBalls{
        \\luaexec{
            local m, n = 6, 45
            local balls = {}
            local tmps = {}
            for i = n-m+1, n do
                local drawn = math.random(i)
                if not tmps[drawn] then
                tmps[drawn] = drawn	   
                else
                tmps[i] = i
                drawn = i
                end
                balls[\\#balls+1] = drawn
            end
            table.sort(balls)
            for i=1,\\#balls do
                tex.print("\\\\LottoBall{", balls[i], "}")
            end
        }
    }
    \\ExplSyntaxOn
    \\newcommand*\\LottoBall[1]{
        \\tikz\\node[
                circle, shade, draw=white, thin, inner~sep=1pt,
                ball~color=red,
                text~width=1em,
                font=\\sffamily, text~badly~centered, white
        ]{#1};}
    \\NewDocumentCommand \\lotto { O{5} }
    {
        \\int_step_inline:nnnn {1}{1}{#1}
        {
            \\DrawBalls\\\\
        }
    }
    \\ExplSyntaxOff
    \\setlength\\parindent{0pt}
    \\begin{document}
    \\lotto[%s]    
    \\end{document}""" %(str(args.frequency))
    with open('lotto.tex', mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('lualatex lotto.tex')

if args.print:
    generate_pdf()
else:
    print(str(args.frequency))
    display_on_console()
    