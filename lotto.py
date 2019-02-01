import os, argparse
from random import randint
parser = argparse.ArgumentParser(
    description = 'Pick lottery numbers.'
)
parser.add_argument(
    'frequency',
    type = int,
    nargs = '?',
    default = 5,
    help = 'Specify how many times to draw lots. (default: 5)'
)
parser.add_argument(
   '-p',
   dest = 'print',
   action = 'store_true',
   default = False,
   help = 'Print lottery numbers in PDF using LuaLaTeX.'
)
parser.add_argument(
    '-w',
    dest = 'weeks',
    type = int,
    default = 10,
    help = 'This option is available only with "-p". Specify how many weeks to continue lottery. (default: 10)'
)
args = parser.parse_args()

def display_on_console():
    m, n = 6, 45
    balls = []
    for x in range(args.frequency):
        balls.clear()
        for i in range(n-m+1, n+1):
            drawn = randint(1, i) 
            if drawn in balls:
                balls.append(i)
            else:
                balls.append(drawn)
        balls.sort()
        print(balls)

def generate_pdf():    
    if os.path.exists('lotto.tex'):
        os.remove('lotto.tex')        
    content = """        
    \\documentclass[11pt, landscape, twocolumn]{article}
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
    \\newcommand*\\LottoBall[1]{%%
        \\GetBallColor
        \\tikz\\node[
                circle,shade,draw=white,thin,inner sep=1pt,
                ball color=ball,
                text width=1em,
                font=\\sffamily,text badly centered,white
        ]{#1};%%
    }
    \\ExplSyntaxOn    	
	\\tl_new:N \\l_R_tl
	\\tl_new:N \\l_G_tl
	\\tl_new:N \\l_B_tl
	\\NewDocumentCommand \\GetBallColor { }
	{
		\\tl_set:Nx \\l_R_tl { \\int_rand:nn {0}{255} }
		\\tl_set:Nx \\l_G_tl { \\int_rand:nn {0}{255} }
		\\tl_set:Nx \\l_B_tl { \\int_rand:nn {0}{255} }
		\\definecolor{ball}{RGB}{\\l_R_tl, \\l_G_tl, \\l_B_tl}		
	}
	\\NewDocumentCommand \\DrawWeek { m }
	{
		\\int_step_inline:nnnn {1}{1}{#1}
        {
            \\DrawBalls\\\\
        }
	}	
	\\ExplSyntaxOff
    \\newcommand*\\lotto[2]{
		\\luaexec{
			today = os.time{year=os.date(\"\\%%Y\"), month=os.date(\"\\%%m\"), day=os.date(\"\\%%d\")}
			saturday_index = 6 - (os.date(\"\\%%w\"))
			for i=1, #1 do    
				next_saturday = today + (saturday_index * 86400)				
				date = os.date(\"\\%%Y-\\%%m-\\%%d\", next_saturday)
				tex.print(\"\\\\par\",date,\"\\\\par\")
				tex.print(\"\\\\DrawWeek{#2}\")
				saturday_index = saturday_index + 7
			end
		}              
    }	
    \\setlength\\parindent{0pt}
	\\setlength\\parskip{.5ex}
    \\begin{document}
	\\lotto{%d}{%d}
    \\end{document} """ %(args.weeks, args.frequency)
    with open('lotto.tex', mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('powershell -command ltx.py -l -b -c lotto.tex')
    os.system('powershell -command open.py lotto.pdf')    

if args.print:
    generate_pdf()
else:    
    display_on_console()
    