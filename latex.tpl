[article]
output: mydoc
tex:   	\documentclass[a4paper]{article}
		
		\begin{document}
		Hello.
		\end{document}

[hzbeamer]
description: The hzbeamer class is available from https://github.com/YiHoze/HzGuide.
output: mybeamer
tex:   \documentclass[10pt,flier=false,hangul=true]{hzbeamer}

		\usepackage{csquotes}
		\MakeOuterQuote{"}

		\title{}
		\author{}
		\institute{}
		\date{}

		\begin{document}    
		\begin{frame}[fragile, allowframebreaks=1]{}
		Hello.
		\end{frame}
		\end{document}

[hzguide]
description: The hzguide class is available from https://github.com/YiHoze/HzGuide.
output: mydoc
tex:    \documentclass[Noto]{hzguide}
		\LayoutSetup{}

		\begin{document}
		Hello.
		\end{document}

[memoir]
output: mydoc
tex:   	\documentclass[a4paper]{memoir} 
		\usepackage{xparse}
		\usepackage{fontspec}

		\begin{document}
		Hello.
		\end{document}

[oblivoir]
output: mydoc
tex:   \documentclass{oblivoir} 

		\usepackage{fapapersize}
		\usefapapersize{*,*,30mm,*,30mm,*}

		\begin{document}
		Hello.
		\end{document}

[glyph]
description: This template shows the glyphs contained in a font.
	usage: mytex.py glyph -s FONT STARTING_CODE ENDING_CODE
	defaults: "Noto Serif CJK KR" 0020 FFFF
output: myfont
placeholders: 3
defaults: Noto Serif CJK KR, 0020, FFFF
tex:    `\documentclass{article}
		`
		`\usepackage[a4paper, margin=2cm]{geometry}
		`\usepackage{fontspec}
		`\usepackage{xcolor}
		`
		`\XeTeXuseglyphmetrics=0
		`
		`\ExplSyntaxOn
		`\int_new:N \l_glyph_number
		`\int_new:N \l_glyph_slot
		`\tl_new:N \l_glyph_code 
		`\int_new:N \l_linebreak_int
		`\int_new:N \l_pagebreak_int
		`
		`\cs_new:Npn \line_page_break:nnn #1 #2 #3
		`{
		`	\int_set:Nn \l_linebreak_int { \int_mod:nn { #1 }{ #2 } }
		`	\int_set:Nn \l_pagebreak_int { \int_mod:nn { #1 }{ #3 } }
		`	\int_compare:nTF { \l_linebreak_int = 0 }
		`	{
		`	\int_compare:nTF { \l_pagebreak_int = 0 }
		`		{
		`			\clearpage
		`		}{
		`			\par
		`		}
		`	}{
		`		\hspace{.5em}
		`	}
		`}
		`
		`\NewDocumentCommand \ShowGlyphsByUnicode { m m m } 
		`{
		`	\setlength\parskip{-2ex}
		`	\setmainfont{#1}\fontsize{11pt}{13pt}\selectfont
		`	\group_begin:			
		`	\int_set:Nn \l_tmpa_int { \int_from_hex:n {#2} }
		`	\int_set:Nn \l_glyph_number { \int_from_hex:n {#3} }	
		`	\int_do_while:nn {	\l_tmpa_int <= \l_glyph_number } 
		`	{                
		`		\tl_set:Nn \l_glyph_code { \int_to_Hex:n {\l_tmpa_int} }
		`		\int_set:Nn \l_glyph_slot {\the\XeTeXcharglyph"\l_glyph_code} 
		`		\int_compare:nTF { \l_glyph_slot != 0 }
		`		{
		`			\parbox{1.5em}{
		`				\centering 			
		`				\raisebox{-2ex}{\sffamily\color{gray} \tiny \int_use:N \l_glyph_slot} \
		`				\char"\l_glyph_code \
		`				\raisebox{2ex}{\sffamily\color{darkgray} \tiny \l_glyph_code }
		`			}
		`		}{
		`			\parbox{1.5em}{
		`				\centering
		`				\raisebox{-2ex}{\sffamily\color{gray} \tiny \int_use:N \l_glyph_slot} \
		`				\fbox{\parbox{0.75em}{\rule{0pt}{2ex}}} \
		`				\raisebox{2ex}{\sffamily\color{darkgray} \tiny \l_glyph_code }
		`			}
		`		}       
		`		\line_page_break:nnn {  \l_tmpa_int }{ 16 }{ 256 }		         
		`		\int_incr:N \l_tmpa_int
		`	}	
		`	\group_end:
		`	\par
		`}
		`\NewDocumentCommand \ShowGlyphsBySlot { m O{1} d() }
		`{
		`	\setlength\parskip{.1ex}
		`	\font\MyFont="#1"~at~11pt \MyFont
		`	\IfValueTF{ #3 }
		`	{
		`		\int_set:Nn \l_tmpa_int { #3 }
		`	}{
		`		\int_set:Nn \l_tmpa_int { \the\XeTeXcountglyphs\MyFont }
		`	}
		`	\int_decr:N \l_tmpa_int	
		`	\int_step_inline:nnn { #2 }{ \l_tmpa_int }
		`	{
		`		\parbox{1.5em}{
		`			\centering
		`			\raisebox{-2ex}{\sffamily\color{gray} \tiny ##1} \
		`			\XeTeXglyph##1
		`		}
		`		\line_page_break:nnn { ##1 }{ 20 }{ 400 }		
		`	}	
		`}
		`\ExplSyntaxOff
		`
		`\linespread{1}
		`\setlength\parindent{0pt}
		`
		`\begin{document}     
		`%%\ShowGlyphsBySlot{\1}[1](10000)
		`\ShowGlyphsByUnicode{\1}{\2}{\3}
		`\end{document}

[manual]
description: Use this template to write manuals such as user guides.
	This requires the hzguide class, which is available from https://github.com/YiHoze/HzGuide.
output: manual
compiler: -w
tex:	\documentclass[10pt, openany, english, template]{hzguide}
		
		\LayoutSetup{}
		\HeadingSetup{chapterstyle=tandh}		
		\setsecnumdepth{chapter}
		\SectionNewpageOn
		\DecolorHyperlinks*[blue]
		\ChapterContentsEnable(5)

		\CoverSetup{    
			FrontLogoImage = {alertsymbol},
			BackLogoImage = {alertsymbol},
			ProductImage = {uncertain},
			title = {Product X},
			DocumentType = {User Guide},
			revision = {Rev. 1},
			note = {Keep this manual for later use.},
			manufacturer = Manufacturer,
			address = Seoul
		}
		
		\begin{document} 
		\frontmatter* 
		\FrontCover
		\tableofcontents
		
		\mainmatter*
		\chapter{Introduction}\tplpara
		\section{Features}\tpllist
		\section{Package Items}\tplimagetable
		\section{Specifications}\tplspectables
		\chapter{Safety}
		\section{General Precautions}\tpllist[itemize][itemize]
		\section{Tools}\tplimagetable
		\section{Safety Gear}\tplimagetable
		\chapter{Installation}
		\section{Installation Requirements}\tpllist
		\section{Installing X}\tplprocedure[5]
		\section{Checking X}\tplprocedure
		\section{Starting X}\tpllist*
		\chapter{Operation}\tplactions
		\chapter{Troubleshooting}\tplproblems
		\chapter{Maintenance}
		\section{Precautions for Maintenance}\tpllist
		\section{Scheduled Inspection}\tpllist
		\chapter{Warranty}
		\section{Warranty Coverage}\tplpara*
		\section{Limitation of Liability}\tplpara*\tpllist
		\section{Contact Information}\tplpara*
		
		\appendix
		\chapter{Technical Information}\tplspectables
		\chapter{Glossary}\tpllist[terms]
		
		\BackCover
		\end{document}

[album]
description: This template generates an album which contains the image files (jpg, png, pdf) gathered from the current directory. 
	This requires the hzguide class, which is available from https://github.com/YiHoze/HzGuide.
	usage: mytex.py album -s IMAGE_SCALE 
	defaults: 1
output: album
image_list: im@ges.txt
placeholders: 1
defaults: 1
compiler: -c
tex:	`\documentclass{hzguide}
		`
		`\LayoutSetup{ulmargin=15mm, lrmargin=15mm}
		`\HeadingSetup{article}
		`
		`\begin{document}
		`\MakeAlbum[\1]{%(image_list)s}
		`%% use \MakeAlbum* to hide image names.
		`\end{document}

[merge]
description: Use this template to merge multiple PDF files different from one another in paper size.
	However, this template wouldn't be needed but cpdf would be adequate in most cases. For example:
	cpdf.exe -scale-to-fit "5.5in 8.5in" foo.pdf -o out.pdf
	cpdf.exe -scale-to-fit "176mm 250mm" A4.pdf -o B5_1.pdf
	cpdf.exe -scale-to-fit "176mm 250mm" A5.pdf -o B5_2.pdf
	cpdf.exe -merge B5_1.pdf B5_2.pdf -o B5.pdf
	usage: mytex.py merge -s PAPER_WIDTH PAPER_HEIGHT TARGET_PDF_FILES
	defaults: 210mm 297mm "foo, ..."
output: merged
placeholders: 3
defaults: 210mm, 297mm, foo,...
tex:	`\documentclass{minimal}
		`
		`\usepackage{xparse}
		`\usepackage[a4paper]{geometry}
		`\geometry{paperwidth=\1, paperheight=\2, margin={0pt, 0pt}}
		`\usepackage{graphicx}
		`
		`\ExplSyntaxOn
		`\sys_if_engine_pdftex:T { \pdfminorversion=6 }
		`
		`\NewDocumentCommand \mergepdf { m }
		`{
		`	\bool_gset_false:N \g_tmpa_bool %% Not to break the last page
		`	\clist_set:Nn \l_tmpa_clist { #1 }    
		`	\int_set:Nn \l_tmpa_int { \clist_count:N \l_tmpa_clist }
		`	\int_step_inline:nn { \l_tmpa_int }
		`	{
		`		\clist_pop:NN \l_tmpa_clist \l_tmpa_tl
		`		\int_compare:nT { ##1 == \l_tmpa_int }
		`		{
		`			\bool_gset_true:N \g_tmpa_bool
		`		}
		`		\fetchpage{ \l_tmpa_tl }
		`	}
		`}
		`
		`\int_new:N \g_lastximage_int
		`\NewDocumentCommand \lastpageofpdf { m }
		`{
		`	\get_last_page_of_pdf:nN { #1 } \g_lastximage_int
		`}
		`
		`\cs_new_nopar:Npn \get_last_page_of_pdf:nN #1 #2
		`{
		`	\str_case_e:nn { \c_sys_engine_str }
		`	{
		`		{ xetex } {
		`			\int_gset:Nn #2 { \xetex_pdfpagecount:D "#1" }
		`		}
		`		{ pdftex } {
		`			\pdfximage{#1}
		`			\int_gset:Nn #2 { \pdflastximagepages }
		`		}
		`		{ luatex } {
		`			\saveimageresource { #1 }
		`			\int_gset:Nn #2 { \lastsavedimageresourcepages }
		`		}
		`	}
		`}
		`
		`\NewDocumentCommand \fetchpage { m }
		`{    
		`	\lastpageofpdf{#1.pdf}
		`	\int_step_inline:nn { \g_lastximage_int }    
		`	{
		`		\mbox{}\vfill
		`		\centering{\includegraphics[width=\paperwidth, page=##1]{#1}}
		`		\vfill
		`		\bool_if:NTF \g_tmpa_bool 
		`		{
		`			\int_compare:nT { ##1 < \g_lastximage_int }
		`			{
		`				\break
		`			}            
		`		}{
		`			\break
		`		}        
		`	}
		`}
		`\ExplSyntaxOff
		`
		`\begin{document}
		`\mergepdf{\3}
		`\end{document}

[numbers]
description: Use this template to have each of circled numbers in separate one-page PDF files.
	This requires the hzguide class, which is available from https://github.com/YiHoze/HzGuide.
	Find and use "numbers.cmd" which is created together with the latex file.
	The command requires cpdf, or alternatively pdftk, to split the resulting PDF.
	usage: mytex.py number -s ENDING_NUMBER
	default: 20
output: numbers
placeholders: 1
defaults: 20
cmd: 	ltx.py \TEX
		pdfcrop \PDF @@@.pdf
		rem pdftk @@@.pdf burst
		cpdf -split @@@.pdf -o %%%%.pdf 
tex:	`\documentclass{hzguide}
		`
		`\LayoutSetup{}
		`\CirnumSetup{
		`	font=\sffamily\bfseries\Large,
		`	fgcolor=white,
		`	bgcolor=red,
		`	sep=0.25pt,
		`	raise=-.5ex,
		`	base=99
		`}
		`
		`\ExplSyntaxOn
		`\NewDocumentCommand \numbers { m }
		`{
		`	\int_step_inline:nn { #1 }
		`	{
		`		\cirnum{##1}
		`		\newpage
		`	}	
		`}
		`\ExplSyntaxOff
		`
		`\pagestyle{empty}
		`
		`\begin{document}
		`\numbers{\1}
		`\end{document}

[permute]
description: Use this template to permute letters
	usage: mytex.py permute -s LETTERS
	defaults: adei
output:	permute
placeholders: 1
defaults: adei
compiler: -l, -c
tex:	`\documentclass{article}
		`\usepackage{kotex}
		`\ExplSyntaxOn
		`\tl_new:N \l_out_tl
		`\NewDocumentCommand \PermuteWord { m }
		`{
		`	\v_permute_word:nno { #1 } { 1 } { \tl_count:n { #1 } }
		`}
		`\cs_new:Npn \v_permute_word:nnn #1 #2 #3
		`{
		`	\int_compare:nTF { #2 == #3 }
		`	{
		`		\v_print_swapped_word:n { #1 }
		`	}
		`	{
		`		\int_step_inline:nnn { #2 } { #3 }
		`		{
		`			\v_tlswap_fn:nnnN { #2 } { ##1 } { #1 } \l_out_tl
		`			\v_permute_word:Von \l_out_tl { \int_eval:n { #2 + 1 } } { #3 }
		`		}
		`	}
		`}
		`\cs_generate_variant:Nn \v_permute_word:nnn { Von, nno }
		`\cs_new:Npn \v_tlswap_fn:nnnN #1 #2 #3 #4
		`{
		`	\tl_clear:N #4
		`	\tl_set:Nx \l_tmpa_tl { #3 }
		`
		`	\int_step_inline:nn { \tl_count:N \l_tmpa_tl }
		`	{
		`		\int_case:nnF { ##1 }
		`		{
		`			{ #1 } { \tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { #2 } } }
		`			{ #2 } { \tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { #1 } } }
		`		}
		`		{
		`			\tl_put_right:Nx #4 { \tl_item:Nn \l_tmpa_tl { ##1 } }
		`		}
		`	}
		`}
		`\cs_new:Npn \v_print_swapped_word:n #1
		`{
		`	\mbox{ #1 }
		`	\space\space
		`}
		`\ExplSyntaxOff
		`\setlength\parindent{0pt}
		`\begin{document}
		`\PermuteWord{\1}
		`\end{document}

[lotto]
description: Use this template to pick lotto numbers randomly.
	usage: mytex.py lotto -s WEEKS FREQUENCY
	defaults: 8 5
output:	lotto
compiler: -l, -c
placeholders: 2
defaults: 8, 5
tex:	`\documentclass[12pt, twocolumn]{article}
		`\usepackage[a5paper,margin=1.5cm]{geometry}
		`\usepackage{xparse}
		`\usepackage{luacode}
		`\usepackage{tikz}
		`\newcommand\DrawBalls{
		`	\luaexec{
		`		local m, n = 6, 45
		`		local balls = {}
		`		local tmps = {}
		`		for i = n-m+1, n do
		`			local drawn = math.random(i)
		`			if not tmps[drawn] then
		`				tmps[drawn] = drawn	   
		`			else
		`				tmps[i] = i
		`				drawn = i
		`			end
		`			balls[\#balls+1] = drawn
		`		end
		`		table.sort(balls)
		`		for i=1,\#balls do
		`			tex.print("\\LottoBall{", balls[i], "}")
		`		end
		`	}
		`}
		`\newcommand*\LottoBall[1]{%%
		`	\GetBallColor
		`	\tikz\node[
		`			circle,shade,draw=white,thin,inner sep=1pt,
		`			ball color=ball,
		`			text width=1em,
		`			font=\sffamily,text badly centered,white
		`	]{#1};%%
		`}
		`\ExplSyntaxOn    	
		`\tl_new:N \l_R_tl
		`\tl_new:N \l_G_tl
		`\tl_new:N \l_B_tl
		`\NewDocumentCommand \GetBallColor { }
		`{
		`	\tl_set:Nx \l_R_tl { \int_rand:nn {0}{255} }
		`	\tl_set:Nx \l_G_tl { \int_rand:nn {0}{255} }
		`	\tl_set:Nx \l_B_tl { \int_rand:nn {0}{255} }
		`	\definecolor{ball}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}		
		`}
		`\NewDocumentCommand \DrawWeek { m }
		`{
		`	\int_step_inline:nn {#1}
		`	{
		`		\DrawBalls\\
		`	}
		`}	
		`\ExplSyntaxOff
		`\newcommand*\lotto[2]{
		`	\luaexec{
		`		today = os.time{year=os.date("\%%Y"), month=os.date("\%%m"), day=os.date("\%%d")}
		`		saturday_index = 6 - (os.date("\%%w"))
		`		for i=1, #1 do    
		`			next_saturday = today + (saturday_index * 86400)				
		`			date = os.date("\%%Y-\%%m-\%%d", next_saturday)
		`			tex.print("\\par\\textbf{",date,"}\\par\\nopagebreak")
		`			tex.print("\\DrawWeek{#2}")
		`			saturday_index = saturday_index + 7
		`		end
		`	}              
		`}	
		`\setlength\parindent{0pt}
		`\setlength\parskip{.5ex}
		`\begin{document}
		`\lotto{\1}{\2}
		`\end{document}  

[tys]
description: Use this template to convert numbers to ancient Chinese numerals.
	The Apple Symbols font is required.
	usage: mytex.py tys -s NUMBERS 
	defaults: "12.86, 302.9534, -8276.1,5.1064, 389.56"
output:	tys
placeholders: 1
defaults: 12.86,302.9534,-8276.1,5.1064,389.56
sty:	`\RequirePackage{fontspec}
		`\RequirePackage{xcolor}
		`\RequirePackage{cancel}
		`\RequirePackage{varwidth}
		`
		`\providecommand\disablekoreanfonts{}
		`
		`\ExplSyntaxOn
		`\keys_define:nn { tys }
		`{
		`	tysfont          .tl_set:N = \l_tys_font_tys_tl,
		`	otherfont        .tl_set:N = \l_tys_font_other_tl,
		`	fontsize         .tl_set:N = \l_tys_font_size_tl,
		`	charwidth        .dim_set:N = \l_tys_char_width_dim,
		`	decimalsymbol    .tl_set:N = \l_tys_decimal_symbol_tl,
		`	zerosymbol       .tl_set:N = \l_tys_zero_symbol_tl,
		`	linespacing      .tl_set:N = \l_tys_linespacing_tl,
		`	poscolor         .tl_set:N = \l_tys_positive_color_tl,
		`	negcolor         .tl_set:N = \l_tys_negative_color_tl,
		`}
		`
		`\NewDocumentCommand \TysSetup { m }
		`{
		`	\keys_set:nn { tys }{ #1  }
		`}
		`
		`\bool_new:N \l_tys_minus_bool
		`\bool_new:N \l_tys_before_decimal_bool
		`\bool_new:N \l_tys_after_decimal_bool
		`\bool_new:N \l_tys_horizon_bool
		`\tl_new:N \l_tys_absolute_tl
		`\int_new:N \l_tys_decimal_position_int
		`\int_new:N \l_tys_digits_before_decimal_int
		`\int_new:N \l_tys_digits_after_decimal_int
		`\int_new:N \l_tys_cnt_int
		`\int_new:N \l_tys_digit_int
		`\int_new:N \l_tys_space_int
		`
		`\NewDocumentCommand \Tys { o >{\SplitList{,}} m }
		`{
		`	\group_begin:
		`	\IfValueT {#1} { 
		`		\keys_set:nn { tys }{ #1 } 
		`	}
		`	\begin{varwidth}{\linewidth}
		`	\disablekoreanfonts
		`	\setlength\parindent{0pt}
		`	\tl_set:Nn \baselinestretch {\l_tys_linespacing_tl}
		`	\int_zero:N \l_tys_decimal_position_int
		`	\int_zero:N \l_tys_digits_before_decimal_int
		`	\int_zero:N \l_tys_digits_after_decimal_int
		`	\ProcessList{#2}{ \tys_get_decimal_position:n }
		`	\ProcessList{#2}{ \tys_process:n }
		`	\vspace{-\baselineskip}  
		`	\end{varwidth}
		`	\group_end:
		`}
		`
		`\cs_new:Npn \tys_get_decimal_position:n #1
		`{
		`	\exp_args:Nx \tl_if_eq:nnTF { \tl_head:n {#1} }{-}
		`	{ 
		`		\tl_set:Nn \l_tys_absolute_tl { \tl_tail:n {#1} } 
		`	}{ 
		`		\tl_set:Nn \l_tys_absolute_tl {#1} 
		`	}
		`	\int_zero:N \l_tys_cnt_int
		`	\exp_args:Nx \tl_map_inline:nn { \l_tys_absolute_tl }
		`	{
		`		\int_incr:N \l_tys_cnt_int
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_compare:nT { \l_tys_decimal_position_int < \l_tys_cnt_int  }
		`			{
		`				\int_set:Nn \l_tys_decimal_position_int { \l_tys_cnt_int }
		`			}
		`		}    
		`	}
		`}
		`
		`\cs_new:Npn \tys_process:n #1
		`{
		`	\fp_compare:nTF { #1 < 0 } 
		`	{ 
		`		\bool_set_true:N \l_tys_minus_bool 
		`	}{ 
		`		\bool_set_false:N \l_tys_minus_bool 
		`	}
		`	\exp_args:Nx \tl_if_eq:nnTF { \tl_head:n {#1} }{-}
		`	{
		`		\tl_set:Nn \l_tys_absolute_tl { \tl_tail:n {#1} } 
		`	}{
		`		\tl_set:Nn \l_tys_absolute_tl {#1} 
		`	}
		`
		`	\int_zero:N \l_tys_cnt_int
		`	\exp_args:Nx \tl_map_inline:nn { \l_tys_absolute_tl }
		`	{
		`		\int_incr:N \l_tys_cnt_int    
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_set:Nn \l_tys_space_int { \l_tys_decimal_position_int - \l_tys_cnt_int }
		`		}
		`	}
		`	\int_step_inline:nnnn {1}{1}{ \l_tys_space_int } { \hspace*{\l_tys_char_width_dim} }
		`	\exp_args:Nx \tys_convert:n { \l_tys_absolute_tl }
		`}
		`
		`\cs_new:Npn \tys_convert:n #1
		`{ 
		`	\bool_if:NTF \l_tys_minus_bool
		`	{ 
		`		\color{\l_tys_negative_color_tl} 
		`	}{ 
		`		\color{\l_tys_positive_color_tl} 
		`	}
		`	\tys_get_digit_numbers:n {#1}
		`	\int_if_even:nTF { \l_tys_digits_before_decimal_int }
		`	{ 
		`		\bool_set_true:N \l_tys_horizon_bool 
		`	}{ 
		`		\bool_set_false:N \l_tys_horizon_bool 
		`	}
		`	\int_set:Nn \l_tys_cnt_int { \l_tys_digits_before_decimal_int }
		`	\tl_map_inline:nn {#1} 
		`	{ 
		`		\tl_if_eq:nnTF {##1}{.}
		`		{ 
		`			\fontspec{\l_tys_font_other_tl}
		`			\l_tys_font_size_tl
		`			\l_tys_decimal_symbol_tl      
		`			\bool_set_true:N \l_tys_horizon_bool
		`		}{
		`			\bool_if:NTF \l_tys_horizon_bool
		`			{         
		`				\tyschar*{##1}
		`				\bool_set_false:N \l_tys_horizon_bool
		`			}{
		`				\int_compare:nTF { \l_tys_cnt_int = 1 }
		`				{
		`					\bool_if:NTF \l_tys_minus_bool
		`					{ \tyschar|{##1} }
		`					{ \tyschar{##1} }
		`				}{
		`					\tyschar{##1}
		`				}
		`				\bool_set_true:N \l_tys_horizon_bool 
		`			}
		`		}
		`		\int_decr:N \l_tys_cnt_int
		`	}
		`	\newline
		`}
		`
		`\cs_new:Npn \tys_get_digit_numbers:n #1
		`{
		`	\bool_set_true:N \l_tys_before_decimal_bool
		`	\bool_set_false:N \l_tys_after_decimal_bool
		`	\int_zero:N \l_tys_cnt_int
		`	\tl_map_inline:nn {#1}
		`	{
		`		\int_incr:N \l_tys_cnt_int
		`		\tl_if_eq:nnT {##1}{.}
		`		{
		`			\int_zero:N \l_tys_cnt_int
		`			\bool_set_false:N \l_tys_before_decimal_bool
		`			\bool_set_true:N \l_tys_after_decimal_bool
		`		}
		`		\bool_if:NT \l_tys_before_decimal_bool
		`		{ 
		`			\int_set:Nn \l_tys_digits_before_decimal_int { \l_tys_cnt_int }
		`		}
		`		\bool_if:NT \l_tys_after_decimal_bool
		`		{ 
		`			\int_set:Nn \l_tys_digits_after_decimal_int { \l_tys_cnt_int }
		`		}
		`	}
		`}
		`
		`%% 1D360 = 119648 : 1, 100, ...
		`%% 1D369 = 119657 : 10, 1000, ...
		`\NewDocumentCommand \tyschar { s t{|} m }
		`{  
		`	\group_begin:  
		`	\l_tys_font_size_tl
		`	\tl_if_eq:nnTF {#3}{0}
		`	{
		`		\fontspec{\l_tys_font_other_tl}
		`		\makebox[\l_tys_char_width_dim]{
		`			\l_tys_zero_symbol_tl
		`		}
		`	}{
		`		\IfBooleanTF {#1}
		`		{ 
		`			\int_set:Nn \l_tys_digit_int { #3 + 119656 } 
		`		}{ 
		`			\int_set:Nn \l_tys_digit_int { #3 + 119647 } 
		`		}
		`		\fontspec{\l_tys_font_tys_tl}
		`		\makebox[\l_tys_char_width_dim]{
		`			\IfBooleanTF {#2} 
		`			{ 
		`				\cancel{\char"\int_to_Hex:n{\l_tys_digit_int} } 
		`			}{ 
		`				\char"\int_to_Hex:n{\l_tys_digit_int} 
		`			}
		`		}
		`	}  
		`	\group_end:
		`}
		`\ExplSyntaxOff
		`
		`\TysSetup{
		`	linespacing=1,
		`	tysfont={Apple Symbols},
		`	otherfont={Arial},
		`	fontsize=\normalsize,
		`	charwidth=0.5em,
		`	decimalsymbol=.,
		`	zerosymbol={\char"25CB},
		`	poscolor=black,
		`	negcolor=black
		`}
tex:	\documentclass[a4paper]{article}
		\usepackage{tys}
		\begin{document}
		\Tys{\1}
		\end{document}

[multilingual]
description: Use this template to see how many languaegs are supported by a font.
	usage: mytex.py multilingual -s FONT 
	default: "Noto Serif"
output: multilingual
placeholders:1 
defaults: Noto Serif
compiler: -c
tex:	\documentclass{minimal} 
		\usepackage{fontspec} 
		\setlength\parskip{1.25\baselineskip} 
		\setlength\parindent{0pt}
		\setmainfont{\1}
		\begin{document}
		0 1 2 3 4 5 6 7 8 9 

		english: 
		© Keep this manual® for future use. These---lines--are-dashes.   

		chinese 中文: 
		请妥善保存本手册，以备将来使用。

		czech ČEŠTINA: 
		Uchovejte tuto příručku pro pozdější použití.

		danish DANSK: 
		Gem vejledningen til senere brug.

		dutch NEDERLANDS: 
		Bewaar deze handleiding voor later gebruik.

		finnish SUOMI: 
		Säilytä tämä käsikirja myöhempää käyttöä varten.

		french FRANÇAIS: 
		Conservez ce manuel pour un usage ultérieur.

		german DEUTSCH: 
		Bewahren Sie diese Anleitung für spätere Nutzung auf.

		greek Ελληνικά:
		Φυλάξτε αυτό το εγχειρίδιο για μελλοντική χρήση.

		italian ITALIANO: 
		Conservare questo manuale per utilizzi successivi.

		japanese 日本語: 
		後で使用するために、この取扱説明書を保管してください。

		korean 한국어: 
		나중에 참조할 수 있도록 이 매뉴얼을 잘 보관하십시오.

		norwegian NORSK:
		Oppbevar denne håndboken til senere bruk.

		polish POLSKI: 
		Zachowaj tę instrukcję na przyszłość.

		portuguese PORTUGUÊS (Brazilian): 
		Guarde este manual para uso posterior.

		russian РУССКИЙ ЯЗЫК: 
		Сохраните это руководство на будущее.

		slovakian SLOVENČINA: 
		Odložte si tento návod na neskoršie použitie.

		spanish ESPAÑOL (Latin): 
		Conserve este manual para poder usarlo más adelante.

		swedish SVENSKA: 
		Behåll denna handbok för framtida användning.

		thai ไทย:
		เก็บคู่มือนี้ไว้เพื่อใช้ในอนาคต

		turkish TÜRKÇE: 
		Bu kılavuzu daha sonra kullanmak üzere saklayın.
		\end{document}

[leaflet]
description: Use this template to impose multiple pages in a sheet.
	However, this template wouldn't needed but the pdfpages package would be adequate in most cases. For example:
	\includepdf[pages={1-3, 12, 4, 5}, nup=3x2]{foo.pdf}
	usage: mytex.py leaflet -s TARGET_PDF COLUMNS LAST_PAGE
	defalts: foo.pdf 3 12	
output: myleaflet
placeholders: 3
defaults: foo.pdf, 3, 12
tex:	`\documentclass{minimal}
		`
		`\usepackage{xparse, expl3}
		`\usepackage{graphicx}
		`\usepackage[a4paper]{geometry}
		`\usepackage{pdfpages}
		`
		`\setlength\fboxsep{0pt}
		`\setlength\parindent{0pt}
		`
		`\ExplSyntaxOn
		`\tl_new:N \leaflet_target_file_tl
		`\int_new:N \leaflet_logic_number
		`\int_new:N \leaflet_real_number
		`\int_new:N \leaflet_back_position
		`\dim_new:N \leaflet_vspace_dim
		`\keys_define:nn { leaflet }
		`{
		`	scale	.tl_set:N = \leaflet_scale_tl,
		`	column	.int_set:N = \leaflet_column_int,
		`	last	.int_set:N = \leaflet_last_page_int,
		`	hspace	.dim_set:N = \leaflet_hspace_dim,
		`	vspace	.code:n = { \dim_set:Nn \leaflet_vspace_dim { #1 -\baselineskip - 0.01pt} },
		`	frame	.bool_set:N	= \leaflet_frame_bool,
		`}
		`
		`\NewDocumentCommand \LeafletSetup { m }
		`{
		`	\keys_set:nn { leaflet } {#1}
		`}
		`
		`\cs_new:Npn \leaflet_impose:n #1
		`{
		`	\hspace{\leaflet_hspace_dim}
		`	\bool_if:NTF \leaflet_frame_bool
		`		{ \fbox{\includegraphics[scale=\leaflet_scale_tl, page=#1]{\leaflet_target_file_tl}} }
		`		{ \includegraphics[scale=\leaflet_scale_tl, page=#1]{\leaflet_target_file_tl} }
		`	\int_compare:nTF { \int_mod:nn {\leaflet_logic_number}{\leaflet_column_int} = 0 }	
		`	{
		`		\int_compare:nT { \leaflet_logic_number < \leaflet_last_page_int }
		`			{ \vspace{\leaflet_vspace_dim} \newline }
		`	}{
		`		\hspace{\leaflet_hspace_dim}
		`	}
		`}
		`
		`\NewDocumentCommand \LeafletImpose { s O{} m }
		`{
		`	\LeafletSetup{#2}
		`	\tl_set:Nn \leaflet_target_file_tl {#3}
		`
		`	\int_compare:nTF { \leaflet_last_page_int = 4 }
		`	{ 
		`		\int_set:Nn \leaflet_back_position {1} 
		`	}{ 
		`		\int_set:Nn \leaflet_back_position { \leaflet_column_int + 1 } 
		`	}
		`
		`	\int_do_until:nn { \leaflet_logic_number = \leaflet_last_page_int }
		`	{
		`		\int_incr:N \leaflet_logic_number
		`		\int_incr:N \leaflet_real_number
		`		\IfBooleanT {#1}
		`		{
		`			\int_compare:nT { \leaflet_logic_number = \leaflet_back_position } 
		`			{ 
		`				\leaflet_impose:n { \leaflet_last_page_int }
		`				\int_incr:N \leaflet_logic_number
		`			}
		`		}
		`		\leaflet_impose:n { \leaflet_real_number }		
		`	}
		`}
		`\ExplSyntaxOff
		`
		`\geometry{
		`	papersize={464mm, 440mm}, 
		`	layoutsize={444mm, 420mm},
		`	margin={0pt, 0pt},
		`	layoutoffset={10mm, 10mm}, 
		`	showcrop
		`}
		`
		`\LeafletSetup{
		`	frame=false,
		`	scale=1, 
		`	hspace=0pt, 
		`	vspace=0pt
		`}
		`
		`\begin{document}
		`\LeafletImpose*[column=\2, last=\3]{\1}
		`%%\includepdf[pages={1-3, 12, 4, 5}, nup=3x2]{\1}
		`%%\includepdf[pages={6-11}, nup=3x2]{\1}
		`\end{document}

[lettercolor]
description: Use this template to apply gradient or random colors to letters.	
	Applying different colors to jamo requires lualatex and the colorjamo package, which is available from https://github.com/dohyunkim/colorjamo
	usage: mytex.py lettercolor -s FONT 
	default: "Noto Serif CJK KR"
output: lettercolor
placeholders:1 
defaults: Noto Serif CJK KR
compiler: -l
sty:	`\RequirePackage{kotex}
		`\RequirePackage{tikz}
		`\RequirePackage{environ}
		`
		`\ExplSyntaxOn
		`\sys_if_engine_luatex:TF
		`{
		`	\RequirePackage{colorjamo} %% https://github.com/dohyunkim/colorjamo
		`}{
		`	\XeTeXuseglyphmetrics=0
		`}
		`\ExplSyntaxOff
		`\setmainhangulfont[Script=Hangul,Language=Korean]{Noto Serif CJK KR}
		`
		`\ExplSyntaxOn
		`\cs_generate_variant:Nn \tl_if_eq:nnTF { V }
		`\cs_generate_variant:Nn \tl_if_eq:nnT { V }
		`\cs_generate_variant:Nn \tl_if_eq:nnF { V }
		`
		`\tl_new:N \l_R_tl
		`\tl_new:N \l_G_tl
		`\tl_new:N \l_B_tl
		`\int_new:N \l_R_int
		`\int_new:N \l_G_int
		`\int_new:N \l_B_int
		`\int_new:N \l_R_incr_int
		`\int_new:N \l_G_incr_int
		`\int_new:N \l_B_incr_int
		`\seq_new:N \l_lettercolor_words_seq
		`
		`\keys_define:nn { LetterColor }
		`{
		`	effect			.tl_set:N = 	\l_lettercolor_effect_tl,
		`	letters			.int_set:N = 	\l_lettercolor_letters_int,
		`	words			.clist_set:N = 	\l_lettercolor_words_clist,
		`	font			.tl_set:N = 	\l_lettercolor_font_tl,
		`	foreground		.tl_set:N = 	\l_lettercolor_fg_color_tl,
		`	background		.tl_set:N = 	\l_lettercolor_bg_color_tl,
		`	transition		.tl_set:N = 	\l_lettercolor_transition_tl,
		`	rand-min 		.tl_set:N = 	\l_lettercolor_rand_min_tl,
		`	rand-max		.tl_set:N = 	\l_lettercolor_rand_max_tl,
		`	grad-continue	.bool_set:N = 	\l_lettercolor_gradient_cont_bool,
		`	grad-RGB		.tl_set:N = 	\l_lettercolor_gradient_RGB_tl,
		`	grad-step		.int_set:N = 	\l_lettercolor_gradient_step_int,
		`	cho				.tl_set:N = 	\l_lettercolor_cho_color_tl,
		`	jung			.tl_set:N = 	\l_lettercolor_jung_color_tl,
		`	jong			.tl_set:N = 	\l_lettercolor_jong_color_tl
		`}
		`
		`\cs_new:Npn \lettercolor_RGB_decompose:N #1
		`{
		`	\tl_set:Nx \l_R_tl { \str_range:Nnn #1 { 1 }{ 2 } }
		`	\tl_set:Nx \l_G_tl { \str_range:Nnn #1 { 3 }{ 4 } }
		`	\tl_set:Nx \l_B_tl { \str_range:Nnn #1 { 5 }{ 6 } }
		`	\int_set:Nn \l_R_int { \exp_args:NV \int_from_hex:n \l_R_tl }
		`	\int_set:Nn \l_G_int { \exp_args:NV \int_from_hex:n \l_G_tl }
		`	\int_set:Nn \l_B_int { \exp_args:NV \int_from_hex:n \l_B_tl }
		`}
		`
		`\NewDocumentCommand \LetterColorSetup { s m }
		`{
		`	\keys_set:nn { LetterColor }{ #2 }
		`	\colorlet{foreground}{\l_lettercolor_fg_color_tl}
		`	\colorlet{background}{\l_lettercolor_bg_color_tl}
		`	\IfBooleanT { #1 }
		`	{
		`		\lettercolor_RGB_decompose:N \l_lettercolor_gradient_RGB_tl
		`	}
		`	\int_set_eq:NN \l_R_incr_int \l_lettercolor_gradient_step_int
		`	\int_set_eq:NN \l_G_incr_int \l_lettercolor_gradient_step_int
		`	\int_set_eq:NN \l_B_incr_int \l_lettercolor_gradient_step_int
		`	\seq_clear:N \l_lettercolor_words_seq
		`	\clist_map_inline:Nn \l_lettercolor_words_clist
		`	{
		`		\seq_put_right:Nx \l_lettercolor_words_seq { \str_foldcase:n { ##1 }}
		`	}
		`}
		`
		`
		`\LetterColorSetup*{
		`	effect = letter, %% ball, initial, count, word
		`	letters = 5,
		`	font = \bfseries,
		`	foreground = orange,
		`	background = blue,
		`	transition = none, %% gradient, random
		`	rand-min = 0, %% greater than or equal to 0
		`	rand-max = 255, %% less than or equal to 255
		`	grad-continue = false,
		`	grad-RGB = FF0000,
		`	grad-step = 5,
		`	cho = FF0000,
		`	jung = 00FF00,
		`	jong = 0000FF
		`}
		`
		`\NewDocumentCommand \lettercolor { o +m }
		`{
		`	\IfValueT { #1 }
		`	{
		`		\LetterColorSetup{#1}
		`	}
		`	\bool_if:NF \l_lettercolor_gradient_cont_bool
		`	{
		`		\lettercolor_RGB_decompose:N \l_lettercolor_gradient_RGB_tl
		`	}
		`	\seq_set_split:Nnn \l_tmpa_seq { \par }{ #2 }
		`	\seq_map_function:NN \l_tmpa_seq \lettercolor_split_lines:n
		`}
		`
		`\int_new:N \l_seq_count_int
		`
		`\cs_new:Npn \lettercolor_split_lines:n #1
		`{
		`	\seq_set_split:Nnn \l_tmpb_seq { \\ }{ #1 }
		`	\int_set:Nn \l_seq_count_int { \seq_count:N \l_tmpb_seq }
		`
		`	\seq_map_inline:Nn \l_tmpb_seq
		`	{
		`		\seq_set_split:Nnn \l_tmpc_seq { ~ }{ ##1 }
		`		\str_case:VnF \l_lettercolor_effect_tl
		`		{
		`			{ initial }{
		`				\seq_map_function:NN \l_tmpc_seq \lettercolor_initial:n
		`			}
		`			{ count }{
		`				\seq_map_function:NN \l_tmpc_seq \lettercolor_count_letters:n
		`			}
		`			{ word }{
		`				\seq_map_function:NN \l_tmpc_seq \lettercolor_emphasize_words:n
		`			}
		`		}{
		`			\seq_map_function:NN \l_tmpc_seq \lettercolor_split_words:n
		`		}
		`		\int_decr:N \l_seq_count_int
		`		\int_compare:nT { \l_seq_count_int > 0 }
		`		{
		`			\newline
		`		}
		`	}\par
		`}
		`
		`\NewDocumentCommand\textlc{m}{
		`	\textcolor{foreground}{\l_lettercolor_font_tl #1}
		`}
		`
		`
		`\cs_new:Npn \lettercolor_count_letters:n #1
		`{
		`	\exp_args:NNx \int_set:Nn \l_tmpa_int { \tl_count:n { #1 } }
		`	\int_compare:nTF { \l_tmpa_int >= \l_lettercolor_letters_int }
		`	{
		`		\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`		{
		`			\lettercolor_assign_color:
		`		}
		`		\textlc{#1}
		`	}{
		`		#1
		`	}\space
		`}
		`
		`\cs_new:Npn \lettercolor_emphasize_words:n #1
		`{
		`	\tl_set:Nn \l_tmpa_tl { #1 }
		`	\tl_set:Nn \l_tmpb_tl { #1 }
		`	\regex_replace_all:nnN { ['":;,.!?(){}\[\]] }{} \l_tmpb_tl
		`	%% for Latin
		`	\exp_args:NNx \regex_set:Nn \l_tmpa_regex { \l_tmpb_tl }
		`	\seq_if_in:NxTF \l_lettercolor_words_seq { \str_foldcase:V \l_tmpb_tl }
		`	{
		`		\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`		{
		`			\lettercolor_assign_color:
		`		}
		`		\regex_replace_once:NnN \l_tmpa_regex { \c{textlc}\cB\{ \0 \cE\} } \l_tmpa_tl
		`	}{	%% for Hangul
		`		\tl_if_head_eq_catcode:oNT { \l_tmpb_tl } \c_catcode_other_token
		`		{
		`			\seq_map_inline:Nn \l_lettercolor_words_seq
		`			{
		`				\tl_if_in:NnT \l_tmpa_tl { ##1 }
		`				{
		`					\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`					{
		`						\lettercolor_assign_color:
		`					}
		`					\regex_replace_once:nnN { ##1 }{ \c{textlc}\cB\{ \0 \cE\} } \l_tmpa_tl
		`				}
		`			}
		`		}
		`	}	
		`	\l_tmpa_tl\space
		`}
		`
		`\cs_new:Npn \lettercolor_initial:n #1
		`{
		`	\str_set:Nx \l_tmpa_str { \str_head:n {#1} }
		`	\str_set:Nx \l_tmpb_str { \str_tail:n {#1} }
		`	\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`	{
		`		\lettercolor_assign_color:
		`	}
		`	\textlc{\l_tmpa_str}\l_tmpb_str\space
		`}
		`
		`\cs_new:Npn \lettercolor_split_words:n #1
		`{
		`	\tl_set:Nn \l_tmpc_tl { #1 }
		`	\tl_map_inline:Nn \l_tmpc_tl
		`	{
		`		\tl_if_eq:VnF \l_lettercolor_transition_tl { none }
		`		{
		`			\lettercolor_assign_color:
		`		}
		`		\str_case:Vn { \l_lettercolor_effect_tl }
		`		{
		`			{ letter }{ \lettercolor_letter:n ##1 }
		`			{ ball }{ \LetterBall{##1}\allowbreak }
		`		}
		`	}
		`	\str_case:Vn { \l_lettercolor_effect_tl }
		`	{
		`			{ letter }{ \space }
		`			{ ball }{ \space\space }
		`	}
		`}
		`
		`\cs_new:Npn \lettercolor_letter:n #1
		`{
		`	\sys_if_engine_xetex:TF
		`	{
		`		\textcolor{foreground}{#1}
		`	}{
		`		\begin{colorjamo}
		`			\textcolor{foreground}{#1}
		`		\end{colorjamo}
		`	}
		`}
		`
		`\cs_new:Nn \lettercolor_assign_color:
		`{
		`	\str_case:Vn \l_lettercolor_transition_tl
		`	{
		`		{ random }{ \lettercolor_assign_color_rand: }
		`		{ gradient }{ \lettercolor_assign_color_grad: }
		`	}
		`}
		`\cs_new:Nn \lettercolor_assign_color_grad:
		`{
		`	\tl_set:Nx \l_R_tl { \int_use:N \l_R_int }
		`	\tl_set:Nx \l_G_tl { \int_use:N \l_G_int }
		`	\tl_set:Nx \l_B_tl { \int_use:N \l_B_int }
		`	\definecolor{foreground}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_complementary:N \l_R_tl
		`	\lettercolor_complementary:N \l_G_tl
		`	\lettercolor_complementary:N \l_B_tl
		`	\definecolor{background}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_grad_incr:NN \l_R_int \l_R_incr_int
		`	\lettercolor_grad_incr:NN \l_G_int \l_G_incr_int
		`	\lettercolor_grad_incr:NN \l_B_int \l_B_incr_int
		`	\tl_if_eq:VnT \l_lettercolor_effect_tl { letter }
		`	{
		`		\sys_if_engine_luatex:T
		`		{
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_cho_color_tl \jamocolorcho
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_jung_color_tl \jamocolorjung
		`			\lettercolor_jamo_color_grad:NN \l_lettercolor_jong_color_tl \jamocolorjong
		`		}
		`	}
		`}
		`
		`\cs_new:Npn \lettercolor_jamo_color_grad:NN #1 #2
		`{
		`	\exp_args:NV #2 #1
		`	\lettercolor_RGB_decompose:N #1
		`	\lettercolor_grad_incr:NN \l_R_int \l_R_incr_int
		`	\lettercolor_grad_incr:NN \l_G_int \l_G_incr_int
		`	\lettercolor_grad_incr:NN \l_B_int \l_B_incr_int
		`	\tl_clear:N \l_tmpa_tl
		`	\clist_set:Nn \l_tmpa_clist { \l_R_int, \l_G_int, \l_B_int }
		`	\clist_map_inline:Nn \l_tmpa_clist
		`	{
		`		\tl_set:Nx \l_tmpb_tl { \int_to_Hex:n { ##1 } }
		`		\exp_args:NNx \int_set:Nn \l_tmpb_int { \tl_count:N \l_tmpb_tl }
		`		\int_compare:nT { \l_tmpb_int == 1 }
		`		{
		`			\tl_put_right:Nn \l_tmpb_tl { 0 }
		`			\tl_reverse:N \l_tmpb_tl
		`		}
		`		\tl_put_right:Nx \l_tmpa_tl { \l_tmpb_tl }
		`	}
		`	\tl_set:NV #1 \l_tmpa_tl
		`}
		`
		`\cs_new:Nn \lettercolor_assign_color_rand:
		`{
		`	\lettercolor_assign_rand_dec:N \l_R_tl
		`	\lettercolor_assign_rand_dec:N \l_G_tl
		`	\lettercolor_assign_rand_dec:N \l_B_tl
		`	\definecolor{foreground}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\lettercolor_complementary:N \l_R_tl
		`	\lettercolor_complementary:N \l_G_tl
		`	\lettercolor_complementary:N \l_B_tl
		`	\definecolor{background}{RGB}{\l_R_tl, \l_G_tl, \l_B_tl}
		`	\tl_if_eq:VnT \l_lettercolor_effect_tl { letter }
		`	{
		`		\sys_if_engine_luatex:T
		`		{
		`			\lettercolor_assign_rand_hex:N \jamocolorcho
		`			\lettercolor_assign_rand_hex:N \jamocolorjung
		`			\lettercolor_assign_rand_hex:N \jamocolorjong
		`		}
		`	}
		`}
		`\cs_new:Npn \lettercolor_complementary:N #1
		`{
		`	\exp_args:NNx \int_set:Nn \l_tmpa_int { 255 - #1 }
		`	\tl_set:Nx #1 { \int_use:N \l_tmpa_int }
		`}
		`\cs_new:Npn \lettercolor_grad_incr:NN #1 #2
		`{
		`	\int_gadd:Nn #1 { #2 }
		`	\int_compare:nT { #1 > 255}
		`	{
		`		\int_gset:Nn #2 { \l_lettercolor_gradient_step_int * -1 }
		`		\int_gset:Nn #1 { 255 }
		`	}
		`	\int_compare:nT { #1 < 0}
		`	{
		`		\int_gset:Nn #2 { \l_lettercolor_gradient_step_int }
		`		\int_gset:Nn #1 { 0 }
		`	}
		`}
		`\cs_new:Npn \lettercolor_assign_rand_hex:N #1
		`{
		`	\tl_clear:N \l_tmpa_tl
		`	\int_step_inline:nn { 3 }
		`	{
		`		\tl_set:Nx \l_tmpb_tl {
		`			\int_to_Hex:n {
		`				\int_rand:nn {\l_lettercolor_rand_min_tl}{\l_lettercolor_rand_max_tl}
		`			}
		`		}
		`		\exp_args:NNx \int_set:Nn \l_tmpb_int { \tl_count:N \l_tmpb_tl }
		`		\int_compare:nT { \l_tmpb_int == 1 }
		`		{
		`			\tl_put_right:Nn \l_tmpb_tl { 0 }
		`			\tl_reverse:N \l_tmpb_tl
		`		}
		`		\tl_put_right:Nx \l_tmpa_tl { \l_tmpb_tl }
		`	}
		`	\exp_args:NV #1 \l_tmpa_tl
		`}
		`\cs_new:Npn \lettercolor_assign_rand_dec:N #1
		`{
		`	\pgfmathparse { random (\l_lettercolor_rand_min_tl, \l_lettercolor_rand_max_tl) }
		`	\tl_set:No #1 \pgfmathresult
		`}
		`
		`\NewDocumentCommand \LetterBall { m }
		`{
		`	\tikz\node[
		`		circle,shade,draw=white,thin,inner~sep=1pt,
		`		ball~color=background,
		`		text~width=1em,
		`		font=\l_lettercolor_font_tl,text~badly~centered
		`	]{\textcolor{foreground}{#1}};
		`}
		`
		`\NewEnviron{LetterColor}[1][]
		`{
		`	\LetterColorSetup{#1}
		`	\exp_args:NV \lettercolor \BODY
		`}
		`\ExplSyntaxOff
tex:	\documentclass{article}
		\usepackage{lettercolor}
		\setlength\parskip{.5\baselineskip}
		\setlength\parindent{0pt}
		\begin{document}

		\LetterColorSetup{
			letters = 5,
			font = \bfseries,
			foreground = orange,
			background = blue,
			grad-continue = true,
			grad-RGB = FF0000,
			grad-step = 3,
			cho = FF0000,
			jung = 00FF00,
			jong = 0000FF
		}

		\subsection*{글자 색을 서서히 바꾸기}

		\begin{LetterColor}[effect=letter, transition=gradient]
		I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.

		우리 역사에서 자유를 위한 가장 훌륭한 시위가 있던 날로 기록될 오늘 이 자리에 여러분과 함께하게 된 것을 기쁘게 생각합니다.
		\end{LetterColor}

		\subsection*{글자 색을 아무렇게나 바꾸기}

		\begin{LetterColor}[effect=letter, transition=random]
		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity.

		백 년 전, 위대한 어느 미국인이 노예해방령에 서명을 했습니다. 지금 우리가 서 있는 이곳이 바로 그 자리입니다. 그 중대한 선언은 불의의 불길에 시들어가고 있던 수백만 흑인 노예들에게 희망의 횃불로 다가왔습니다. 그것은 그 긴 속박의 밤을 끝낼 흥겨운 새벽으로 왔습니다.
		\end{LetterColor}

		\subsection*{단어의 첫자만 색칠하기}

		\begin{LetterColor}[effect=initial, transition=none]
		I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.

		우리나라 역사상 자유를 위한 가장 위대한 시위가 있었던 날로서 역사에 기록될 오늘 나는 여러분과 함께 하게 되어 행복합니다.
		\end{LetterColor}

		\subsection*{첫자 색을 서서히 바꾸기}

		\begin{LetterColor}[effect=initial, transition=gradient]
		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation.

		백년 전, 오늘 우리가 서있는 자리의 상징적 그림자의 주인공인, 한 위대한 미국인이, 노예해방선언문에 서명하였습니다.
		\end{LetterColor}

		\subsection*{첫자 색을 아무렇게나 바꾸기}

		\begin{LetterColor}[effect=initial, transition=random]
		This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice.

		그 중대한 법령은 억압적 불평등의 불길에 타들어가던 수백만 흑인 노예들에게 위대한 희망의 횃불로서 다가왔습니다.
		\end{LetterColor}

		\subsection*{글자를 공에 넣기}

		\begin{LetterColor}[effect=ball, transition=none, foreground=yellow, font=\sffamily\bfseries]
		It came as a joyous daybreak to end the long night of their captivity.

		그 법령은 그들의 길었던 구속의 밤을 종식하는 기쁨의 새벽이었습니다.
		\end{LetterColor}

		\subsection*{글자 색과 공 색을 서서히 바꾸기}

		\begin{LetterColor}[effect=ball, transition=gradient, font=\sffamily\bfseries]
		But one hundred years later, the Negro still is not free.

		그러나 백년이 지난 후에도, 흑인들은 여전히 자유롭지 못합니다.
		\end{LetterColor}

		\subsection*{글자 색과 공 색을 아무렇게나 바꾸기}

		\begin{LetterColor}[effect=ball, transition=random, font=\sffamily\bfseries]
		One hundred years later, the life of the Negro is still sadly crippled by the manacles of segregation and the chains of discrimination.

		백년이 지난 후에도, 분리의 수갑과 차별의 쇠사슬에 의해 흑인들의 삶은 여전히 슬픈 불구의 상태입니다.
		\end{LetterColor}

		\subsection*{다섯 자 이상인 단어만 색칠하기}

		\begin{LetterColor}[effect=count, letters=5, transition=none]
		One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity.

		백년이 지난 후에도, 물질적 번영이라는 거대한 대양의 한가운데 홀로 떨어진 빈곤의 섬에서 흑인들은 살아가고 있습니다.
		\end{LetterColor}

		\subsection*{네 자 이상인 단어의 색을 서서히 바꾸기}

		\begin{LetterColor}[effect=count, letters=4, transition=gradient, grad-step=5, grad-continue=false, font=\itshape\bfseries]
		One hundred years later, the Negro is still languished in the corners of American society and finds himself an exile in his own land.

		백년이 지난 후에도, 흑인들은 미국사회의 한 구석에서 여전히 풀이 죽고 자신의 땅에서 유배당한 자신을 보게 됩니다.
		\end{LetterColor}

		\LetterColorSetup{
			words={자유, 권리, 정의, 헌법, 민주주의, freedom, right, justice, liberty, Constitution, democracy}
		}

		\subsection*{특정 단어들을 색칠하기: 자유, 권리, ..., freedom, right, ...}

		\begin{LetterColor}[effect=word, transition=none, foreground=blue]
		And so we’ve come here today to dramatize a shameful condition.

		그래서 이 수치스런 상황을 알리고 바꾸고자 우리는 오늘 이 자리에 나온 것입니다.

		In a sense we’ve come to our nation’s capital to cash a check.

		어떤 의미로는 수표를 현금으로 바꾸기 위해서 우리는 우리나라의 수도에 온 것입니다.

		When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir.

		우리나라를 건국한 사람들은 헌법과 독립선언문에 숭고한 단어들을 써넣었으며, 모든 미국인들이 상속받게 될 약속어음에 서명하였습니다.

		This note was a promise that all men, yes, black men as well as white men, would be guaranteed the “unalienable Rights” of “Life, Liberty and the pursuit of Happiness.”

		그 약속어음은 모든 사람들에게, 예, 백인들처럼 흑인들에게도, 생존, 자유, 그리고 행복추구라는 양도할 수 없는 권리가 보장된다는 하나의 약속이었습니다.

		It is obvious today that America has defaulted on this promissory note, insofar as her citizens of color are concerned.

		오늘날 미국이 시민들의 피부색과 관련하여서만은 지금까지 그 약속어음 대로 이행하지 않고 있다는 것이 명백합니다.

		Instead of honoring this sacred obligation, America has given the Negro people a bad check, a check which has come back marked “insufficient funds.”

		이 신성한 의무를 존중하지 않고서, 미국은 잔고부족이라고 표기되어 되돌아 온 수표, 부도수표를 흑인들에게 주었습니다.
		\end{LetterColor}

		\subsection*{특정 단어들의 색을 서서히 바꾸기}

		\begin{LetterColor}[effect=word, transition=gradient, grad-continue=false, grad-step=15]
		But we refuse to believe that the bank of justice is bankrupt.

		그러나 우리는 정의의 은행이 파산했다고 믿기를 거부합니다.

		We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation.

		우리는 이 기회의 나라의 금고에 자금이 부족하다고 믿기를 거부합니다.

		And so, we’ve come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice.

		그래서 우리는 우리에게 넘치는 자유와 정의의 보장을 가져다 줄 수표, 그 수표를 현금으로 바꾸기 위해서 여기에 왔습니다.

		We have also come to this hallowed spot to remind America of the fierce urgency of now.

		우리는 또한 미국으로 하여금 지금의 이 무서운 절박함을 깨닫게 해주기 위해 이 신성한 장소에 왔습니다.

		This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism.

		지금은 ‘냉정하자’ 라는 사치스런 말이나 점진주의라는 안정제를 취할 때가 아닙니다.

		Now is the time to make real the promises of democracy.

		지금은 민주주의에 대한 약속을 지켜야 할 때입니다.

		Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice.

		지금은 어둡고 황량한 차별의 계곡에서 양지 바른 인종적 정의의 길로 나와야 할 때입니다.

		Now is the time to lift our nation from the quicksands of racial injustice to the solid rock of brotherhood.

		지금은 인종적 불평등이라는 모래에서 형제애라는 단단한 바위 위로 우리 나라를 들어올려야 할 때입니다.

		Now is the time to make justice a reality for all of God’s children.

		지금은 모든 하느님의 자식들을 위해 정의를 현실화 해야 할 때입니다.

		It would be fatal for the nation to overlook the urgency of the moment.

		지금의 절박함을 무시한다면 그것은 이 나라에 치명적이 될 것입니다.

		This sweltering summer of the Negro’s legitimate discontent will not pass until there is an invigorating autumn of freedom and equality.

		흑인들의 정당한 불만으로 가득찬 이 무더운 여름은 자유와 평등이라는 상쾌한 가을이 오기까지 사라지지 않을 것입니다.

		Nineteen sixty-three is not an end, but a beginning.

		1963년은 끝이 아니라 시작입니다.

		And those who hope that the Negro needed to blow off steam and will now be content will have a rude awakening, if the nation returns to business as usual.

		흑인들이 흥분을 가라앉힐 필요가 있고 적당히 만족할 것을 바라는 사람들은 만약 이 나라가 예전의 그 일상으로 되돌아 가려고 한다면, 거친 깨달음을 얻게 될 것 입니다.

		And there will be neither rest nor tranquility in America until the Negro is granted his citizenship rights.

		흑인들이 그들의 시민권을 인정받기 전까지 미국에는 휴식도 평온도 없을 것입니다.

		The whirlwinds of revolt will continue to shake the foundations of our nation until the bright day of justice emerges.

		저항의 회오리바람은 정의가 출현하는 밝은 날이 올 때까지 우리나라의 기반을 흔들 것입니다.

		But there is something that I must say to my people, who stand on the warm threshold which leads into the palace of justice.

		그러나 정의의 궁전에 이르는 흥분되는 입구에 서있는 여러분께 내가 드려야 할 말이 있습니다.

		In the process of gaining our rightful place, we must not be guilty of wrongful deeds.

		우리의 정당한 지위를 얻는 과정에서 우리는 불법행위에 따른 범법자가 되어서는 안됩니다.

		Let us not seek to satisfy our thirst for freedom by drinking from the cup of bitterness and hatred.

		비통과 증오의 잔에서 흘러내린 물로써 자유를 향한 우리의 갈증을 풀려고 하지 맙시다.

		We must forever conduct our struggle on the high plane of dignity and discipline.

		우리는 품위와 절제의 고귀한 수준을 유지해 가면서 우리의 투쟁을 영원히 수행해 나가야 합니다.

		We must not allow our creative protest to degenerate into physical violence.

		우리의 건설적 항거가 물리적 파괴로 변질되도록 해서는 안될 것입니다.

		Again and again, we must rise to the majestic heights of meeting physical force with soul force.

		계속, 계속해서, 우리는 영혼의 힘과 물리적 힘을 함께 만날 수 있는 저 장엄한 고지를 올라가야 합니다.

		The marvelous new militancy which has engulfed the Negro community must not lead us to a distrust of all white people.

		흑인사회를 휘감고 있는 새로운 투쟁의 기운이 우리를 모든 백인들의 불신의 대상으로 이끌지 않도록 해야 합니다.

		For many of our white brothers, as evidenced by their presence here today, have come to realize that their destiny is tied up with our destiny.

		오늘 이 자리의 참석으로 증명되듯, 많은 우리의 백인형제들은, 그들의 운명이 우리의 운명과 맺어져 있음을 깨달았습니다.

		And they have come to realize that their freedom is inextricably bound to our freedom.

		그리고 그들의 자유가 우리의 자유와 떨어질 수 없게 묶여져 있음을 깨달았습니다.

		We cannot walk alone.

		우리는 홀로 걸어갈 수 없습니다.

		And as we walk, we must make the pledge that we shall always march ahead.

		그리고 걸으며, 우리는 언제나 행진에 앞장설 것을 맹세해야 합니다.

		We cannot turn back.

		우리는 되돌아갈 수 없습니다.

		There are those who are asking the devotees of civil rights, “When will you be satisfied? ”

		인권운동가들에게 다음과 같이 묻는 사람들이 있습니다, “언제쯤 당신들은 만족하겠느냐? ”

		We can never be satisfied as long as the Negro is the victim of the unspeakable horrors of police brutality.

		우리는 절대 만족할 수 없습니다, 흑인들이 경찰들의 만행에 아무런 말도 할 수 없는 두려움의 희생자가 되는 한.

		We can never be satisfied as long as our bodies, heavy with the fatigue of travel, cannot gain lodging in the motels of the highways and the hotels of the cities.

		우리는 절대 만족할 수 없습니다, 우리의 몸이 여행의 피곤으로 무거울 때 고속도로의 모텔과 시내의 호텔에서 잠자리를 얻지 못하는 한.

		We cannot be satisfied as long as the Negro’s basic mobility is from a smaller ghetto to a larger one.

		우리는 만족할 수 없습니다, 흑인들의 이동이 작은 빈민가에서 큰 빈민가로 가는 한.

		We can never be satisfied as long as our children are stripped of their selfhood and robbed of their dignity by signs stating “for white only.”

		우리는 절대 만족할 수 없습니다, 우리의 어린이들이 자존심을 박탈당하고 “백인 전용”이라 쓰여진 문구에 자신들의 존엄성을 강탈당하는 한.

		We cannot be satisfied as long as a Negro in Mississippi cannot vote and a Negro in New York believes he has nothing for which to vote.

		우리는 만족할 수 없습니다, 미시시피의 흑인들이 투표조차 할 수 없고 뉴욕의 흑인들이 투표할 대상이 없다고 믿는 한.

		No, no, we are not satisfied, and we will not be satisfied until justice rolls down like waters, and righteousness like a mighty stream.

		절대로, 절대로, 우리는 만족하지 않습니다. 정의가 강물처럼 흘러내리고, 정당함이 거대한 흐름이 될 때까지, 우리는 만족하지 않을 것입니다.

		I am not unmindful that some of you have come here out of great trials and tribulations.

		여러분들 중 일부는 거대한 시련과 고통으로부터 벗어나 여기에 왔다는 것을 나는 주목하고 있습니다.

		Some of you have come fresh from narrow jail cells.

		여러분들 중 일부는 좁은 감방에서 이제 막 나왔습니다.

		And some of you have come from areas where your quest for freedom left you battered by the storms of persecution and staggered by the winds of police brutality.

		여러분들 중 일부는 자유에 대한 당신의 요구가 당신을 박해의 폭풍 앞에서 부서지게 하고 공권력의 만행이란 바람에 비틀거리게 했던 곳에서 왔습니다.

		You have been the veterans of creative suffering.

		여러분들은 의미있는 고통에 익숙해진 노련한 사람들이 되었습니다.

		Continue to work with the faith that unearned suffering is redemptive.

		그 고통도 과분하다 여기고 보상을 받으리란 믿음으로 계속 해나가십시요.

		Go back to Mississippi, go back to Alabama, go back to South Carolina, go back to Georgia, go back to Louisiana, go back to the slums and ghettos of our northern cities, knowing that somehow this situation can and will be changed.

		돌아가십시요, 알라바마로, 남부 캘리포니아로, 조지아로, 루이지애나로, 북부 도시들의 빈민가와 흑인거주지로, 어떻게든 지금의 이 상황이 변화될 수 있다는 그리고 변화될 것이라는 인식을 갖고서 돌아가십시요.

		Let us not wallow in the valley of despair, I say to you today, my friends.

		절망의 계곡에서 몸부림치지 말자고, 나의 친구들이여, 나는 오늘 여러분께 말합니다.

		And so even though we face the difficulties of today and tomorrow, I still have a dream.

		그래서 우리가 오늘과 내일의 역경을 만나게 된다고 할지라도, 나는 아직도 꿈이 있습니다.

		It is a dream deeply rooted in the American dream.

		그 꿈은 아메리칸 드림에 깊이 뿌리를 둔 꿈입니다.

		I have a dream that one day this nation will rise up and live out the true meaning of its creed, “We hold these truths to be self-evident, that all men are created equal.”

		나에게는 꿈이 있습니다, 언젠가는, 이 나라가 일어나 “모든 사람은 평등하 게 태어났다라는 진실을 우리는 자명으로 유지한다”라는 이 나라 강령의 참뜻대로 살아가는 날이 있을 것이라는 꿈이 있습니다.

		I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.

		나에게는 꿈이 있습니다, 언젠가는, 조지아주의 붉은 언덕 위에서 노예들의 후손들과 노예소유주들의 후손들이 형제애의 식탁에서 함께 자리할 수 있을 것이라는 꿈이 있습니다.

		I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.

		나에게는 꿈이 있습니다, 언젠가는, 불의의 열기로 무더운, 억압의 열기로 무더운, 저 미시시피마저도 자유와 정의의 오아시스로 변모할 것이라는 꿈이 있습니다.

		I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.

		나에게는 꿈이 있습니다, 언젠가는, 나의 네명의 어린 아이들이 그들의 피부 색깔로서 판단되지 않고 그들의 개별성으로 판단되는 그런 나라에서 살게 될 것이라는 꿈이 있습니다.

		I have a dream today.

		오늘 나에게는 꿈이 있습니다.

		I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of “interposition” and “nullification”, one day right there in Alabama little black boys and black girls will be able to join hands with little white boys and white girls as sisters and brothers. I have a dream today.

		나에게는 꿈이 있습니다, 언젠가는, 사악한 인종차별주의자들이 있는 알라바마주, 연방정부의 법과 조치를 따르지 않겠다는 발언을 내뱉는 주지사가 있는 알라바마주, 언젠가는 바로 그 알라바마주에서, 어린 흑인 소년들과 어린 흑인 소녀들이, 어린 백인 소년들과 어린 백인 소녀들과 형제자매로서 손을 맞잡을 수 있을 것이라는 꿈이 있습니다. 오늘 나에게는 꿈이 있습니다.

		I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight, and the glory of the Lord shall be revealed, and all flesh shall see it together.

		나에게는 꿈이 있습니다, 언젠가는, 모든 골짜기들은 메워지고, 모든 언덕과 산들은 낮아지고, 거친 곳은 평평해지고, 굽은 곳은 펴지고, 하느님의 영광이 나타나고, 모든 사람들이 다같이 그 영광을 보게 될 것이라는 꿈이 있습니다.

		This is our hope, and this is the faith that I go back to the South with.

		이것이 우리의 희망이며, 이것이 내가 남부로 돌아갈 때 함께 하게 될 신념입니다.

		With this faith, we will be able to hew out of the mountain of despair a stone of hope.

		이 신념으로서, 우리는 절망의 산을 깎아 희망의 돌을 만들어 낼 수 있을 것입니다.

		With this faith, we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood.

		이 신념으로써, 우리는 우리나라의 소란한 불협화음을 아름다운 형제애의 교향곡으로 변화시킬 수 있을 것입니다.

		With this faith, we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for preedom together, knowing that we will be free one day.

		이 신념으로써, 우리가 언젠가는 자유로워 질 것이라 믿으면서, 우리는 함께 일하고, 함께 기도하며, 함께 투쟁하며, 함께 감옥에 가고, 함께 자유를 위해 버텨낼 수 있을 것입니다.

		And this will be the day, this will be the day when all of God’s children will be able to sing with new meaning.

		이 날이, 이 날이 모든 하느님의 자식들이 새로운 의미의 노래를 부를 수 있는 바로 그 날이 될 것입니다.

		My country ‘tis of thee, sweet land of liberty, of thee I sing. Land where my fathers died, land of the Pilgrim’s pride, From every mountainside, let freedom ring.

		나의 나라 그것은 하느님의 것, 달콤한 자유의 땅, 내가 노래하는 하느님의 것 나의 조상들이 죽은 땅, 개척자의 자부심이 있는 땅, 모든 산으로부터 자유가 울려 퍼지게 합시다.

		And if America is to be a great nation, this must become true.

		미국이 위대한 나라가 되려면, 이것은 현실이 되어야 합니다.

		And so let freedom ring from the prodigious hilltops of New Hampshire. Let freedom ring from the mighty mountains of New York. Let freedom ring from the heightening Alleghenies of Pennsylvania. Let freedom
		ring from the snow-capped Rockies of Colorado. Let freedom ring from the curvaceous slopes of California.

		그래서 뉴햄프셔주의 경이로운 언덕으로부터 자유가 울려 퍼지게 합시다. 뉴욕의 거대한 산맥들로부터 자유가 울려 퍼지게 합시다. 펜실베니아주의 높다란 엘리게니산맥으로부터 자유가 울려 퍼지게 합시다. 콜로라도주의
		눈덮인 록키산맥으로부터 자유가 울려 퍼지게 합시다. 캘리포니아주의 굽이진 비탈로부터 자유가 울려 퍼지게 합시다.

		But not only that Let freedom ring from Stone Mountain of Georgia. Let freedom ring from Lookout Mountain of Tennessee. Let freedom ring from every hill and molehill of Mississippi. From every mountainside, let freedom ring.

		그것 뿐만이 아닙니다. 조지아주의 스톤산으로부터 자유가 울려 퍼지게 합시다. 테네시주의 룩아웃산으로부터 자유가 울려 퍼지게 합시다. 미시시피주의 크고 작은 모든 언덕으로부터 자유가 울려 퍼지게 합시다. 모든 산으로부터 자유가 울려 퍼지게 합시다.

		And when this happens, when we allow freedom ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God’s children, black men and white men, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the old Negro spiritual.

		이렇게 될 때, 자유가 울리게 할 때, 모든 마을과 부락으로부터, 모든 주와 도시로부터, 자유가 울려 퍼지게 할 때, 모든 하느님의 자식들이, 흑인과 백인이, 유대인과 이교도들이, 개신교도와 카톨릭교도들이, 손을 잡고 옛 흑인영가의 구절을 노래부를 수 있는 그날을 우리는 앞당길 수 있을 것입니다.

		Free at last, Free at last.

		마침내 자유, 마침내 자유.

		Thank God Almighty, we are free at last.

		전능하신 하느님 감사합니다, 저희는 마침내 자유가 되었습니다.
		\end{LetterColor}
		\end{document}

[metapost]
description: Use this template and lualatex to draw metapost images
output: mymp
compiler: -l
tex:	`\documentclass{article}
		`\usepackage{luamplib}
		`\begin{document}
		`\begin{mplibcode}
		`beginfig(1)
		`z0 = origin; %% short form for (0,0)
		`z1 = (60,40); z2 = (40,90);
		`z3 = (10,70); z4 = (30,50);
		`pickup pencircle scaled 1mm;
		`draw z0; draw z1; draw z2;
		`draw z3; draw z4;
		`pickup defaultpen;
		`draw z0--z1--z2--z3--z4 withcolor blue;
		`draw z0..z1..z2..z3..z4 withcolor red;
		`draw z0..z1..z2..z3..z4..z0 withcolor green;
		`endfig;
		`
		`beginfig(2)
		`for i=0 upto 100:
		`fill unitsquare
		`scaled ((100-i)*0.1mm)
		`rotated 31i
		`withcolor (0.01i)[red,blue];
		`endfor;
		`endfig;
		`
		`beginfig(3)
		`pair a;
		`a = right*15mm;
		`draw a
		`for i=30 step 30 until 3600:
		`	.. a rotated i
		`	scaled ((3600-i)/3600)
		`endfor;
		`endfig;
		`
		`beginfig(3)
		`z1=right*28mm; z2=right*30mm;
		`draw origin;
		`for i=0 step 10 until 350:
		`	if (i < 100) or (i > 270):
		`		label.rt(decimal(i),origin) shifted z2 rotated i withcolor blue;
		`	else:
		`		label.lft(decimal(i),origin) rotated 180 shifted z2 rotated i withcolor red;
		`	fi;
		`	draw (z1--z2) rotated i;
		`endfor;
		`endfig;
		`
		`beginfig(10)
		`pair A,B,C,D;
		`u:=2cm;
		`A=(0,0); B=(u,0); C=(u,u); D=(0,u);
		`
		`transform T;
		`A transformed T = 1/5[A,B];
		`B transformed T = 1/5[B,C];
		`C transformed T = 1/5[C,D];
		`
		`path p;
		`p = A--B--C--D--cycle;
		`for i=0 upto 100:
		`	draw p;
		`	p:= p transformed T;
		`endfor;
		`endfig;		
		`\end{mplibcode}		
		`\end{document}

[bibtex]
description: Use this tempalte to see an example of bibtex.
output: mybib
compiler: -f, -bib
bib:	`@article{ahu61,
		`	author={Arrow, Kenneth J. and Leonid Hurwicz and Hirofumi Uzawa},
		`	title={Constraint qualifications in maximization problems},
		`	journal={Naval Research Logistics Quarterly},
		`	volume={8},
		`	year=1961,
		`	pages={175-191}
		`}
		`
		`@book{ab94,
		`	author = {Charalambos D. Aliprantis and Kim C. Border},
		`	year = {1994},
		`	title = {Infinite Dimensional Analysis},
		`	publisher = {Springer},
		`	address = {Berlin}
		`}
		`
		`@incollection{m85,
		`	author={Maskin, Eric S.},
		`	year={1985},
		`	title={The theory of implementation in {N}ash equilibrium: a survey},
		`	booktitle={Social Goals and Social Organization},
		`	editor={Leonid Hurwicz and David Schmeidler and Hugo Sonnenschein},
		`	pages={173-204},
		`	publisher={Cambridge University Press},
		`   address={Cambridge}
		`}
		`
		`@inproceedings{ah2006,
		`	author={Aggarwal, Gagan and Hartline, Jason D.},
		`	year={2006},
		`	title={Knapsack auctions},
		`	booktitle={Proceedings of the 17th Annual ACM-SIAM Symposium on Discrete Algorithms},
		`	pages={1083-1092},
		`	publisher={Association for Computing Machinery},
		`	address={New York}
		`}
		`
		`@techreport{arrow48,
		`	author = {Arrow, Kenneth J.},
		`	title = {The possibility of a universal social welfare function},
		`	institution = {RAND Corporation},
		`	year = {1948},
		`	number = {P-41},
		`	type = {Report}
		`}
		`
		`@unpublished{FudenbergKreps1988,
		`	title = {A theory of learning, experimentation, and equilibrium in games},
		`	author = {Fudenberg, Drew and Kreps, David M.},
		`	year = {1988},
		`	note = {Unpublished paper}
		`}
tex:	\documentclass{article}
		\usepackage{natbib}
		\begin{document}
		\title{BibTeX in action}
		\author{Martin Osborne}
		\maketitle
		\section{Introduction}
		This document illustrates the use of BibTeX.  
		You may want to refer to \cite{ahu61} or \cite{ab94} or \cite{m85}.  
		Or you may want to cite a specific page in a reference, like this: see \citet[p.~199]{m85}. 
		Or perhaps you want to cite more than one paper by Maskin: \cite{m85, arrow48}.
		Or you want to make a parenthetical reference to one or more articles, 
		in which case the \verb+\citealt+ command omits the parentheses around the year (\citealt{ahu61}).
		\bibliographystyle{plainnat} 
		\bibliography{mybib}
		\end{document}

[protractor]
description: This template draws a protractor using tikz.
output: protrator
compiler: -c
tex: 	`\documentclass{standalone}
		`\usepackage{tikz}
		`\begin{document}
		`	\begin{tikzpicture}
		`		\draw (6,0) arc [radius=6, start angle=0, end angle=180] -- (-6,-0.5) -- (6,-0.`5) -- cycle;
		`		\ExplSyntaxOn
		`		\int_step_inline:nnnn {0}{10}{180}
		`		{ 
		`			\draw[red] (#1\c_colon_str 5.2) -- (#1\c_colon_str 6);
		`			\node[red, rotate=-90+#1] at (#1\c_colon_str 5) {#1};
		`			\node[rotate=90-#1] at (180-#1\c_colon_str 4.5) {#1};
		`			\draw (#1\c_colon_str 1) -- (#1\c_colon_str 3);            
		`		}
		`		\int_step_inline:nnnn {0}{1}{180}
		`		{
		`			\int_compare:nF { \int_mod:nn {#1}{10} = 0 }
		`			{
		`				\int_compare:nTF { \int_mod:nn {#1}{10} = 5 }
		`				{			
		`					\draw[blue] (#1\c_colon_str 5.4) -- (#1\c_colon_str 6);
		`				}{
		`					\draw (#1\c_colon_str 5.6) -- (#1\c_colon_str 6);
		`				}	
		`			}
		`		}
		`		\ExplSyntaxOff
		`		\draw[->, line width=1] (0,0) -- (4,0);
		`		\draw[->, line width=1] (0,0) -- (0,4);
		`		\draw[->, line width=1] (0,0) -- (-4,0);
		`		\filldraw[fill=white] (0,0) circle [radius=0.2] node {+};
		`	\end{tikzpicture}
		`\end{document}

[xindy]
description: This template shows how to change index style for texindy.
output: myxindy
compiler: -w, -i, -ist, myxindy.xdy
xdy:	(require "lang/general/utf8-lang.xdy")
		(require "lang/korean/utf8.xdy")

		(markup-index :open "\begin{theindex}\sffamily~n
		\providecommand*\lettergroupDefault[1]{}
		\providecommand*\lettergroup[1]{%%
		\par\textbf{\large#1}\par
		\nopagebreak
		}"
		:close "~n~n\end{theindex}~n"
		:tree)

		(markup-indexentry :open "~n  \item "       :depth 0)
		(markup-indexentry :open "~n  \subitem "    :depth 1)
		(markup-indexentry :open "~n  \subsubitem " :depth 2)

		(markup-locclass-list :open "\dotfill " :sep ", ")
		(markup-locref-list   :sep ", ")
		(markup-range :sep "--")
tex:	\documentclass[a4paper]{article}
		\usepackage{kotex}
		\usepackage{makeidx}
		\usepackage{hyperref}
		\newcommand\term[1]{#1\index{#1}}
		\makeindex
		\begin{document}
		I am happy to join with you today in what will go down in \term{history} as the greatest \term{demonstration} for freedom in the history of our nation.

		우리 \term{역사}에서 자유를 위한 가장 훌륭한 \term{시위}가 있던 날로 기록될 오늘 이 자리에 여러분과 함께하게 된 것을 기쁘게 생각합니다.

		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the \term{Emancipation Proclamation}. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity.

		백 년 전, 위대한 어느 미국인이 노예해방령에\index{노예!노예행방령} 서명을 했습니다. 지금 우리가 서 있는 이곳이 바로 그 자리입니다. 그 중대한 선언은 불의의 불길에 시들어가고 있던 수백만 흑인 \term{노예}들에게 희망의 횃불로 다가왔습니다. 그것은 그 긴 속박의 밤을 끝낼 흥겨운 새벽으로 왔습니다.

		I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.

		우리나라 역사상 자유를 위한 가장 위대한 시위가 있었던 날로서 역사에 기록될 오늘 나는 여러분과 함께 하게 되어 행복합니다.

		Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation.\index{Proclamation@Emancipation Proclamation}

		백년 전, 오늘 우리가 서있는 자리의 상징적 그림자의 주인공인, 한 위대한 미국인이, \term{노예해방선언문}에 서명하였습니다.

		This momentous \term{decree} came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice.

		그 중대한 \term{법령}은 억압적 불평등의 불길에 타들어가던 수백만 흑인 노예들에게 위대한 희망의 횃불로서 다가왔습니다.

		It came as a joyous daybreak to end the long night of their captivity.

		그 법령은 그들의 길었던 구속의 밤을 종식하는 기쁨의 새벽이었습니다.

		But one hundred years later, the Negro still is not free.

		그러나 백년이 지난 후에도, 흑인들은 여전히 자유롭지 못합니다.

		One hundred years later, the life of the Negro is still sadly crippled by the manacles of \term{segregation} and the chains of \term{discrimination}.

		백년이 지난 후에도, \term{분리}의 수갑과 \term{차별}의 쇠사슬에 의해 흑인들의 삶은 여전히 슬픈 불구의 상태입니다.

		One hundred years later, the Negro lives on a lonely island of poverty in the midst of a vast ocean of material prosperity.

		백년이 지난 후에도, 물질적 번영이라는 거대한 대양의 한가운데 홀로 떨어진 빈곤의 섬에서 흑인들은 살아가고 있습니다.

		One hundred years later, the Negro is still languished in the corners of American society and finds himself an exile in his own land.

		백년이 지난 후에도, 흑인들은 미국사회의 한 구석에서 여전히 풀이 죽고 자신의 땅에서 유배당한 자신을 보게 됩니다.

		And so we’ve come here today to dramatize a shameful \term{condition}.

		그래서 이 수치스런 상황을 알리고 바꾸고자 우리는 오늘 이 자리에 나온 것입니다.
		\printindex
		\end{document}

[arabic]
description: This template shows how to typeset Arabic.
output: arabic
tex: 	\documentclass[a4paper]{article}
		\usepackage{polyglossia}
		\setotherlanguage{arabic}
		\setdefaultlanguage{english}
		\newfontfamily\arabicfont[Script=Arabic]{Noto Naskh Arabic}
		%% \usepackage{arabxetex}

		\begin{document}
		\begin{Arabic}
		عندما يريد العالم أن ‪يتكلّم ‬ ، فهو يتحدّث بلغة يونيكود. تسجّل الآن لحضور المؤتمر الدولي العاشر ليونيكود \textenglish{(Unicode Conference)}، الذي سيعقد في 10\textenglish{--}12 آذار 1997 بمدينة مَايِنْتْس، ألمانيا. و سيجمع المؤتمر بين خبراء من كافة قطاعات الصناعة على الشبكة العالمية انترنيت ويونيكود، حيث ستتم، على الصعيدين الدولي والمحلي على حد سواء مناقشة سبل استخدام يونكود في النظم القائمة وفيما يخص التطبيقات الحاسوبية، الخطوط، تصميم النصوص والحوسبة متعددة اللغات.

		مَمِمّمَّمِّ
		\end{Arabic}
		\end{document}

[japanese]
description: This template shows how to typeset Japanese.
output: japanese
tex: 	\documentclass[a4paper]{article}
		\usepackage{xeCJK}
		\setCJKmainfont{Noto Serif CJK JP}[Language=Japanese,Script=Kana]
		\setCJKsansfont{Noto Sans CJK JP}[Language=Japanese,Script=Kana]
		\punctstyle{fullwidth}

		\begin{document}
		ハネウェルAnalyticsは、本機器の運用寿命の期間、通常の使用及びサービスの下で、製品に材料および製造上の欠陥がないことを保証します。 
		この保証は最初の購入者に新しい、未使用の製品の販売にまで及びます。
		ハネウェルAnalyticsの保証義務は制限されています。ハネウェルAnalyticsのオプションで、購入代金の払い戻し、 保証期間内にハネウェルAnalytics認定サービスセンターに返送された欠陥製品の修理または交換です。 
		いかなる場合においても、以下のハネウェルAnalyticsの責任は、実際に製品のバイヤーが支払った購入価格を超えません。
		\end{document}

[chinese]
description: This template shows how to typeset Japanese.
output: chinese
tex: 	\documentclass[a4paper]{article}
		\usepackage{xeCJK}
		\setCJKmainfont{Noto Serif CJK SC}
		\setCJKsansfont{Noto Sans CJK SC}
		\punctstyle{fullwidth}

		\begin{document}
		Honeywell Analytics保证本产品在材料和工艺上没有缺陷，可在设备的使用寿命内正常使用。 
		将全新和未使用过的产品销售给原始买方时，本保修方可延长。
		Honeywell Analytics承担有限的保修义务，Honeywell Analytics可自行决定退回购买金额、修理还是更换保修期内退回Honeywell Analytics授权服务中心的存在缺陷的产品。 
		在任何情况下，Honeywell Analytics没有义务承担超出买方购买本产品实际支付的金额。
		\end{document}

[vertical]
description: This template shows how to make vertical typesetting.
output: vertical
tex:	\documentclass[a4paper, twocolumn]{article}
		\usepackage{kotex}

		\setmainhangulfont{Noto Serif CJK KR}[Vertical=Alternates, RawFeature=vertical]
		\setsanshangulfont{Noto Sans CJK KR}[Vertical=Alternates, RawFeature=vertical]

		%% \begin{vertical}{12em}
		%% \hangulfontspec{Noto Sans CJK KR}[Vertical=Alternates, RawFeature=vertical ]
		%% 그러나 少女가 끝까지 나를 멀리하는 그러한 괴로움을
		%% \end{vertical}

		\verticaltypesetting

		\begin{document}
		그러나 少女가 끝까지 나를 멀리하는 그러한 괴로움을
		나에게 준다면 나에겐 이 괴로움을 이겨낼 道理와 自信은 없소。
		나는 이젠 마지막 길을 떠나야 하겠습니다。
		그렇게 되면 당신은 그제야 비로소 모든 것을 알 것이며、 또한 나에게
		돌아올 것입니다。

		나는 그 캄캄한 그 地獄에 가서도 나는 촛불을 켜들고 그대 少女가
		돌아오는、 진정 그대 少女를 기다리고 있겠습니다。

		\textsf{그 자리에 나가겠습니다}

		明民氏。

		어제 黃昏이 깃들 무렵 明民氏의 편지를 받아 읽었어요。
		몇번이고 몇번이고 되풀이해 읽었어요。

		明民氏가 새삼스럽게 제게 편지를 띄웠구나 하는 생각에서
		저는 封筒을 뜯을 念을 하지 않고 한참이나 편지를 이리저리 뒤졌어요。
		그러면서 생각을 했답니다。

		（말로써 할 수 없는 중대한 어떤 사연이 필연코 적혀 있으리라。）

		저의 斷案은 꼭 맞고 말았어요。

		明民氏、 눈물겹도록 반갑고 感謝해요。

		저같은 사람에게 求婚을 하신다니⋮。
		明民氏와 저는 너무나 彼此를 잘 알고 있다고 여겨집니다。
		저희들은 少年 少女 時節을 한 이웃에서 成長하지 않았어요?

		童心의 世界에서 明民氏와 저는 소꿉장난으로 같이 成長한
		竹馬之友였습니다。
		점차로 철이 들면서부터 저희들은 男女有別을 깨닫지 않았어요。
		그때부터 저희들은 저희들 自身이 부끄럽고 남의 눈이 두려워 疏遠해지지 않았어요。

		허전한 不安을 안고서도 저희들은 자주 만나지를 못했죠。

		六·二五라는 커다란 不幸은、 不幸 속에서도 저희들을 길러주지 않았어요。

		서울이 완전수복이 된 몇 달 後 정말로 奇跡的으로 明民氏와 邂逅하지 않았어요。
		그때부터 저희들은 童心에서의 友情보다 異性間의 友情이 나날이 두터워지지 않았습니까。

		생각하면 꿈같은 過去였어요。

		자주 만날수록 明民氏와 저는 괴로움을 맛보게 됐어요。

		저나 明民氏나 어떤 告白을 하고 받아야 될 岐路線上에서 허덕이지 않았어요。

		지금 생각해보니 明民氏와 저 사이엔 告白이 必要치 않았어요。

		봄의 季節이 뭇 植物을 蘇生케 하는 自然의 法則과도 같이 저희들 사이는
		이미 봄의 過程을 지나 結實의 季節인 가을이었어요。
		그 가을의 結實을 彼此 말 못하고 주저하지 않았어요。

		明民氏가 오늘 제게 보내주신 편지 句節句節은 제가 明民氏에게 하고픈
		告白의 全部였어요。

		（저의 애정 고백에 찬동하신다는 표시로 오는 토요일 오후 두 시에
		덕수궁 정문에서 만납시다）고⋮。

		꼭 나가겠어요。 이제 그날 만나서 서로 여러 말을 주고받지 않아도
		좋아요。 이미 제 마음도 明民氏처럼 確固不動해요。

		明民氏와 저라면 이 險한 世波를 勇敢하게 헤엄쳐 나갈 수 있으리라는
		마음이 샘솟는 탓은 제가 明民氏를 너무 過信하는 탓일까요?

		사람이 사람을 믿는다는 것은 퍽 어려운 일이라고 생각됩니다。

		이 世上 許多한 사람들 가운데 몇 명이나 자기처럼 남을 믿을 수 있겠
		어요。

		믿는다는 것과 믿음을 相對便에 준다는 것은 어려운 일이라고 생각이 자꾸 돼요。
		그러나 이제 비로소 저는 남을 믿을 수 있고 저를 남이 믿어준다는 
		벅찬 感激을 어떻게 表現해야 옳을까요?

		그날이 지금부터 기다려져요。 무슨 빛깔의 옷을 입고 가야 하는가를 지금부터
		自問自答하고 있어요。

		明民氏는 웃으실 거예요。

		（우리 사이에 무슨 모양 운운의 말을 하느냐고요?）

		그러나 너무나 幸福하면 사람이란 本來의 自己 理性을 잊을 수가 빈번히 있지
		않을까 생각이 돼요。

		저희들은 世間의 稱讚과 非難에 左右되지 않는 明民氏와 저가 돼야 해요。
		約束하시겠죠。

		어서 그날이 無事히 다가오기를 祈願하면서 \rule{3.5em}{.4pt}

		明民氏 안녕히 주무세요。

		\textsf{동의할 수 없습니다}

		朴선생님。

		사실을 말씀드리오면、 어떻게 할까하고 며칠 동안을 괴로움 가운데 망설이다가
		결국은 편지로써 회답을 올립니다。
		선생님의 뜻밖의 글월을 받잡고 저는 참으로 당황했습니다。

		거기에는 선생님의 큰 착오가 계신 것을 깨달았기 때문입니다。
		어떻게 할까 하고 저는 깊은 생각에 잠겼습니다。

		처음에는 만나서 직접 말씀으로 저의 지금 심정을 알려드릴까 했습니다。
		그리하여 선생님께서 만나자고 하신 장소로 갔었습니다。

		그러나 저는 결국 근처까지 갔다가 그대로 집으로 돌아왔습니다。
		선생님을 만나뵙고 저의 심경을 말씀드리는 것은 아무리하여도 부자연스러움을
		느꼈기 때문입니다。
		그리하여 마침내 이렇게 편지를 드리게 된 것입니다。

		朴선생님。

		선생님의 고마우신 뜻을 받아들이지 못하는 저를 용서해 주십시오。
		저는 알고보면 선생님께는 알맞지 않는 여자입니다。
		저는 평범하고、 초라하고、 미거한 여자입니다。

		선생님은 여러 해 동안 職場에서 뵈어서 잘 알지마는
		어느 때나 비범한 것을 좋아하시고 華麗한 것을 좋아하시며 平坦한 것보다는
		曲折을 사랑하시는 분입니다。
		그러한 분이 저에게 잠시 사랑을 求하셨다 하더래도 저는 安心하고 선뜻
		따라나설 수가 없습니다。
		지금은 結婚할 생각이 조금도 없습니다마는、 앞으로 萬一 結婚을 한다며는
		저에게는 저와 마찬가지로 平凡하고 素朴한 분이 적당하리라고 생각합니다。
		그렇게 되면 저는 屈曲이 없이 平坦한 대로 一生동안 파란 없는 지어미의 
		길을 걸을 수 있을 것입니다。

		그러나 萬一 지금 선생님께서 말씀하시는 대로 거저 기분에 끌려서
		따라간다며는 선생님은 선생님으로서、 저는 또 저로서 반드시 크게 후회할 날이
		올 것입니다。

		선생님께서는 절대로 그렇지 않다고 하실는지 모르지만 제 좁은 소견에 그것은
		확실한 것으로 생각됩니다。
		그런 것을 선생님께서는 잠시 기분에 끌리어서 저같은 것을 要求하고 계신 것입니다。
		제가 알기에 남자분들은 대개가 맹목적으로 애정 문제를 처리하려고 드십니다。
		그러나 일생을 함께 살아간다는 것은 그렇게 손쉽게 처리할 수 있는 문제는
		아닌가 합니다。

		선생님께서는 제가 선생님께 호감을 가지고 있는 것처럼 해석하고 계신 것 같은데
		그에 대해서는 이 기회에 곡해를 풀어주시기 바랍니다。
		저는 물론 같은 職場에서 일하는 先輩님으로 선생님을 존경합니다。
		그것을 호감이라고 부른다면 불러도 무방할 것입니다。
		그러나 異性으로서 호감을 가져본 일은 한번도 없습니다。 그것은 거듭 말씀드리거니와
		선생님과 저 사이에는 도저히 메꾸려 하여도 메꿀 수 없는 異質的 間隔이
		가로놓여 있기 때문입니다。
		한 마디로 말씀드리면 선생님은 초라하게 살아가야 할 범용한 여자인 저에게는
		너무도 높아서 손이 닿지 않는 분입니다。

		부디 저를 괘씸스러운 여자라고 생각지 말아 주십시오。 제가 여러 날 동안 망설이고
		괴로워 한 것은 바로 그 때문이었습니다。
		만일 저같은 보잘것없는 여자로 해서 선생님의 마음에 조금이라도 누를 끼친다면 
		그것은 결코 저의 본의가 아닙니다。

		그러므로 이 편지를 드린 후에도 저는 선생님과 그 전과 다름없이 사귈 것이며
		선생님께서도 그렇게 해주시기 바랍니다。
		저는 어떠한 일이 있든지 이 사실을 발설치 않을 것이오니、 선생님께서도 어김없이
		그처럼 해 주신다면、 우리는 순수한 우정으로 계속하여 사귈 수 있을 것입니다。
		그러나 끝으로 한번 더 부탁드릴 것은 지금의 선생님께 대한 이런 판단은
		저로서는 결정적인 것이오니 부디 널리 용서하시고、 만일 저를 사랑하신다면、
		저의 이 진심을 담박한 심경으로 받아주시기 바랍니다。
		\end{document}

[greek]
description: This template shows how to type ancient Greek.
output: greek 
tex: 	\documentclass{article}

		\usepackage{polyglossia}
		\setdefaultlanguage[variant=ancient]{greek}
		\PolyglossiaSetup{greek}{language=greek}
		\newfontfamily\greekfont[Script=Greek]{Noto Serif}
		\usepackage[modulo]{lineno}
		\linenumbers

		\begin{document}
		\selectlanguage{greek}
		ἀλλ᾽ ὦ κρατύνων Οἰδίπους χώρας ἐμῆς, 
		ὁρᾷς μὲν ἡμᾶς ἡλίκοι προσήμεθα 
		βωμοῖσι τοῖς σοῖς: οἱ μὲν οὐδέπω μακρὰν 
		πτέσθαι σθένοντες, οἱ δὲ σὺν γήρᾳ βαρεῖς, 
		ἱερῆς, ἐγὼ μὲν Ζηνός, οἵδε τ᾽ ᾐθέων 
		λεκτοί: τὸ δ᾽ ἄλλο φῦλον ἐξεστεμμένον 
		ἀγοραῖσι θακεῖ πρός τε Παλλάδος διπλοῖς 
		ναοῖς, ἐπ᾽ Ἰσμηνοῦ τε μαντείᾳ σποδῷ. 
		πόλις γάρ, ὥσπερ καὐτὸς εἰσορᾷς, ἄγαν 
		ἤδη σαλεύει κἀνακουφίσαι κάρα 
		βυθῶν ἔτ᾽ οὐχ οἵα τε φοινίου σάλου, 
		φθίνουσα μὲν κάλυξιν ἐγκάρποις χθονός, 
		φθίνουσα δ᾽ ἀγέλαις βουνόμοις τόκοισί τε 
		ἀγόνοις γυναικῶν: ἐν δ᾽ ὁ πυρφόρος θεὸς 
		σκήψας ἐλαύνει, λοιμὸς ἔχθιστος, πόλιν, 
		ὑφ᾽ οὗ κενοῦται δῶμα Καδμεῖον, μέλας δ᾽ 
		Ἅιδης στεναγμοῖς καὶ γόοις πλουτίζεται. 
		θεοῖσι μέν νυν οὐκ ἰσούμενόν σ᾽ ἐγὼ 
		οὐδ᾽ οἵδε παῖδες ἑζόμεσθ᾽ ἐφέστιοι, 
		ἀνδρῶν δὲ πρῶτον ἔν τε συμφοραῖς βίου 
		κρίνοντες ἔν τε δαιμόνων συναλλαγαῖς: 
		ὅς γ᾽ ἐξέλυσας ἄστυ Καδμεῖον μολὼν 
		σκληρᾶς ἀοιδοῦ δασμὸν ὃν παρείχομεν, 
		καὶ ταῦθ᾽ ὑφ᾽ ἡμῶν οὐδὲν ἐξειδὼς πλέον 
		οὐδ᾽ ἐκδιδαχθείς, ἀλλὰ προσθήκῃ θεοῦ 
		λέγει νομίζει θ᾽ ἡμὶν ὀρθῶσαι βίον: 
		νῦν τ᾽, ὦ κράτιστον πᾶσιν Οἰδίπου κάρα, 
		ἱκετεύομέν σε πάντες οἵδε πρόστροποι 
		ἀλκήν τιν᾽ εὑρεῖν ἡμίν, εἴτε του θεῶν 
		φήμην ἀκούσας εἴτ᾽ ἀπ᾽ ἀνδρὸς οἶσθά του: 
		ὡς τοῖσιν ἐμπείροισι καὶ τὰς ξυμφορὰς 
		ζώσας ὁρῶ μάλιστα τῶν βουλευμάτων. 
		ἴθ᾽, ὦ βροτῶν ἄριστ᾽, ἀνόρθωσον πόλιν, 
		ἴθ᾽, εὐλαβήθηθ᾽: ὡς σὲ νῦν μὲν ἥδε γῆ 
		σωτῆρα κλῄζει τῆς πάρος προθυμίας: 
		ἀρχῆς δὲ τῆς σῆς μηδαμῶς μεμνώμεθα 
		στάντες τ᾽ ἐς ὀρθὸν καὶ πεσόντες ὕστερον. 
		ἀλλ᾽ ἀσφαλείᾳ τήνδ᾽ ἀνόρθωσον πόλιν: 
		ὄρνιθι γὰρ καὶ τὴν τότ᾽ αἰσίῳ τύχην 
		παρέσχες ἡμῖν, καὶ τανῦν ἴσος γενοῦ. 
		ὡς εἴπερ ἄρξεις τῆσδε γῆς, ὥσπερ κρατεῖς, 
		ξὺν ἀνδράσιν κάλλιον ἢ κενῆς κρατεῖν: 
		ὡς οὐδέν ἐστιν οὔτε πύργος οὔτε ναῦς 
		ἔρημος ἀνδρῶν μὴ ξυνοικούντων ἔσω.
		\end{document}

[lwarp]
description: This template shows an example for lwarp.
output: mylwarp
cmd:	ltx.py mylwarp -v
		lwarpmk html mylwarp
		rem when using the lateximage environment 
		rem lwarpmk limages mylwarp 
		open.py mylwarp.html
css: 	`@import url("lwarp.css") ;
		`/* @import url("lwarp_formal.css") ; */
		`/* @import url("lwarp_sagebrush.css") ; */
		`body {
		`	font-family: "Noto Serif CJK KR", "DejaVu Serif", "Bitstream Vera Serif",
		`		"Lucida Bright", Georgia, serif;
		`	background: #FAF7F4 ;
		`	color: black ;
		`	margin:0em ;
		`	padding:0em ;
		`	font-size: 100%% ;
		`	line-height: 1.2 ;
		`}
		`div.my {
		`	font-style: italic;
		`	font-weight: bolder;
		`	font-size: 400%%; 
		`}
tex:	\documentclass[a4paper]{article}
		\usepackage{graphicx}
		\usepackage{kotex}
		\usepackage[mathjax]{lwarp}
		\usepackage{amsmath}
		\CSSFilename{mylwarp.css}
		\setmainhangulfont{Noto Serif CJK KR}
		\setsanshangulfont{Noto Sans CJK KR}
		\setmainfont{Noto Serif}
		\setsansfont{Noto Sans}
		\renewcommand\baselinestretch{1.5}
		\newcommand\my[1]{{\Huge\itshape\bfseries #1}}
		\begin{warpHTML}
		%% \renewcommand\my[1]{\begin{lateximage}\Huge\itshape\bfseries #1\end{lateximage}}
		\renewcommand\my[1]{\begin{BlockClass}{my}#1\end{BlockClass}}
		\end{warpHTML}

		\begin{document}
		\section{HTML로 변환하자}
		\my{My 나의} 함수 $f(x)$가 다음과 같다고 하자.
		\begin{equation}
		f(x)=e^{-ix} (\cos x+i \sin x) \tag{1}\label{eq:1}
		\end{equation}
		양변을 미분하면
		\begin{align*}
		\frac{d}{dx} f(x) &= -ie^{-ix} (\cos x + i \sin x ) + e^{-ix} (\sin x + i \cos x ) \\
		&= e^{-ix} ( -i \cos x+ \sin x - \sin x + i\cos x ) = 0 \\
		f(x) &= C \quad (\text{단, $C$는 상수})
		\end{align*}
		식 (\ref{eq:1})에 $x=0$을 대입하면
		\begin{align*}
		f(0) &= 1 \\
		C &= 1.
		\end{align*}
		이로부터,
		\[
		e^{-ix} (\cos x + i\sin x) = 1
		\]
		이므로,
		\[
		e^{ix} = \cos x + i \sin x.
		\]
		\end{document} 

[target]
description: This template draws shooting targets using tikz.
output: shooting_target
compiler: -c
tex: 	`\documentclass{minimal}
		`\usepackage[a3paper,hmargin=0cm,vmargin=0cm]{geometry}
		`\usepackage{tikz}
		`\usepackage{ifthen}
		`\usepackage{xparse}
		`\tikzset{x=1.25cm,y=1.25cm}
		`\ExplSyntaxOn
		`\bool_new:N \g_monochrome_bool
		`\clist_set:Nn \l_tmpa_clist 
		`{
		`	white,white,black,black,blue,blue,red,red,yellow,yellow
		`}
		`\clist_set:Nn \l_tmpb_clist 
		`{
		`	black,black,white,white,white,white,black,black,black,black,black
		`}
		`\NewDocumentCommand \setcolors { }
		`{
		`	\bool_if:NTF \g_monochrome_bool
		`	{
		`		\tl_set:Nn \bgcolor {white}
		`		\tl_set:Nn \fgcolor {black}
		`	}{
		`		\clist_gpop:NN \l_tmpa_clist \bgcolor
		`		\clist_gpop:NN \l_tmpb_clist \fgcolor
		`	}
		`}
		`\NewDocumentCommand \points { m }
		`{
		`	\int_set:Nn \l_tmpa_int { 11 - #1 }
		`	\textcolor{\fgcolor}{\sffamily\bfseries \int_use:N \l_tmpa_int}
		`}
		`
		`\NewDocumentCommand \target { s }
		`{
		`	\IfBooleanTF{#1}
		`	{
		`		\bool_gset_true:N \g_monochrome_bool
		`	}{
		`		\bool_gset_false:N \g_monochrome_bool
		`	}
		`	\null\vfill
		`	\centering{\DrawTarget}
		`	\vfill
		`}
		`\ExplSyntaxOff
		`\NewDocumentCommand \DrawTarget { }
		`{
		`	\begin{tikzpicture}
		`	\sffamily
		`	\foreach \i in {10,9,...,1}{
		`		\setcolors
		`		\filldraw[fill=\bgcolor, draw=\fgcolor] (0,0) circle [ radius=\i ];
		`		\ifthenelse{\i=1}{
		`			\node at (180:0) { \points{\i} };
		`		}{
		`			\node at (180:\i-0.5) { \points{\i} };
		`		}
		`	}
		`	\end{tikzpicture}
		`}
		`
		`\begin{document}
		`\target
		`\newpage
		`\target*
		`\end{document}

[persian]
description: This template shows how to typeset Old Persian in cuineform.
output: old_persian
cmd: 	teckit_compile.exe old_persian.map
		ltx.py old_persian -v
map: ; TECkit mapping for TeX input conventions <-> Unicode characters

		LHSName "old_persian"
		RHSName "UNICODE"

		pass(Unicode)

		; ligatures from Knuth's original CMR fonts
		U+002D U+002D           <>  U+2013  ; -- -> en dash
		U+002D U+002D U+002D    <>  U+2014  ; --- -> em dash

		U+0027          <>  U+2019  ; ' -> right single quote
		U+0027 U+0027   <>  U+201D  ; '' -> right double quote
		U+0022           >  U+201D  ; " -> right double quote

		U+0060          <>  U+2018  ; ` -> left single quote
		U+0060 U+0060   <>  U+201C  ; `` -> left double quote

		U+0021 U+0060   <>  U+00A1  ; !` -> inverted exclam
		U+003F U+0060   <>  U+00BF  ; ?` -> inverted question

		; additions supported in T1 encoding
		U+002C U+002C   <>  U+201E  ; ,, -> DOUBLE LOW-9 QUOTATION MARK
		U+003C U+003C   <>  U+00AB  ; << -> LEFT POINTING GUILLEMET
		U+003E U+003E   <>  U+00BB  ; >> -> RIGHT POINTING GUILLEMET

		;U+0020    >  U+0020 ;  space maps to space
		U+002D    >  U+200D ;  hyphen as Zero Width Joiner
		U+002E    >  U+200D ;  dot as Zero Width Joiner
		U+007C    >  U+200C ;  pipe as Zero Width Non-Joiner

		U+0061         <>  U+103A0    ;  a 𐎠 
		U+0069         <>  U+103A1    ;  i 𐎡
		U+0075         <>  U+103A2    ;  u 𐎢
		U+006B U+0061        <>  U+103A3    ;  ka 𐎣
		U+006B U+0075        <>  U+103A4    ;  ku 𐎤
		U+0067 U+0061        <>  U+103A5    ;  ga 𐎥
		U+0067 U+0075        <>  U+103A6    ;  gu 𐎦
		U+0078 U+0061        <>  U+103A7    ;  xa 𐎧
		U+0063 U+0068 U+0061       <>  U+103A8    ;  cha 𐎨
		U+006A U+0061        <>  U+103A9    ;  ja 𐎩
		U+006A U+0069        <>  U+103AA    ;  ji 𐎪
		U+0074 U+0061        <>  U+103AB    ;  ta 𐎫
		U+0074 U+0075        <>  U+103AC    ;  tu 𐎬
		U+0064 U+0061        <>  U+103AD    ;  da 𐎭
		U+0064 U+0069        <>  U+103AE    ;  di 𐎮
		U+0064 U+0075        <>  U+103AF    ;  du 𐎯
		U+0074 U+0068 U+0061       <>  U+103B0    ;  tha 𐎰
		U+0070 U+0061        <>  U+103B1    ;  pa 𐎱
		U+0062 U+0061        <>  U+103B2    ;  ba 𐎲
		U+0066 U+0061        <>  U+103B3    ;  fa 𐎳
		U+006E U+0061        <>  U+103B4    ;  na 𐎴
		U+006E U+0075        <>  U+103B5    ;  nu 𐎵
		U+006D U+0061        <>  U+103B6    ;  ma 𐎶
		U+006D U+0069        <>  U+103B7    ;  mi 𐎷
		U+006D U+0075        <>  U+103B8    ;  mu 𐎸
		U+0079 U+0061        <>  U+103B9    ;  ya 𐎹
		U+0076 U+0061        <>  U+103BA    ;  va 𐎺
		U+0076 U+0069        <>  U+103BB    ;  vi 𐎻
		U+0072 U+0061        <>  U+103BC    ;  ra 𐎼
		U+0072 U+0075        <>  U+103BD    ;  ru 𐎽
		U+006C U+0061        <>  U+103BE    ;  la 𐎾
		U+0073 U+0061        <>  U+103BF    ;  sa 𐎿
		U+007A U+0061        <>  U+103C0    ;  za 𐏀
		U+0073 U+0068 U+0061       <>  U+103C1    ;  sha 𐏁
		U+0073 U+0073 U+0061       <>  U+103C2    ;  ssa 𐏂
		U+0068 U+0061        <>  U+103C3    ;  ha 𐏃

		U+0061 U+0075 U+0072       <>  U+103C8    ;  aur 𐏈
		U+0061 U+0075 U+0072 U+0032      <>  U+103C9    ;  aur2 𐏉
		U+0061 U+0075 U+0072 U+0033      <>  U+103CA    ;  aur3 𐏊
		U+0078 U+0078        <>  U+103CB    ;  xx 𐏋
		U+0064 U+0061 U+0068       <>  U+103CC    ;  dah 𐏌
		U+0064 U+0061 U+0068 U+0032      <>  U+103CD    ;  dah2 𐏍
		U+0062 U+0061 U+0067 U+0061      <>  U+103CE    ;  baga 𐏎
		U+0062 U+0075 U+0075       <>  U+103CF    ;  buu 𐏏

		U+0064 U+0069 U+0076       <>  U+103D0    ;  div 𐏐
		U+0031         <>  U+103D1    ;  1 𐏑
		U+0032         <>  U+103D2    ;  2 𐏒
		U+0031 U+0030        <>  U+103D3    ;  10 𐏓
		U+0032 U+0030        <>  U+103D4    ;  20 𐏔
		U+0031 U+0030 U+0030       <>  U+103D5    ;  100 𐏕
tex:	\documentclass[a4paper]{article}
		\usepackage{fontspec}
		\usepackage{graphicx}
		\usepackage{xcolor}
		\usepackage{stackengine}

		\newfontface\OldPersianFont[Mapping=old_persian ,Colour=darkgray]{Noto Sans Old Persian}
		\DeclareTextFontCommand{\textop}{\large\OldPersianFont}

		\newenvironment{OldPersian}
		{\OldPersianFont\Large\ignorespaces}
		{\ignorespacesafterend}

		\ExplSyntaxOn
		\NewDocumentCommand{\transop}{m}
		{
		\tl_set:Nn \l_xander_oper_tl { #1 }
		%% change every run of lowercase letters into italic
		\regex_replace_all:nnN
		{ [a-z]+ }
		{ \c{textit}\cB\{\0\cE\} }
		\l_xander_oper_tl
		%% change every xx to name
		\regex_replace_all:nnN
		{ ([xx]){2,2} }
		{ |Xshaayathiya| }
		\l_xander_oper_tl
		%% change every ch into c U+030c
		\regex_replace_all:nnN
		{ ([ch]){2,2} }
		{ c \x{030c} }
		\l_xander_oper_tl
		%% change every th into θ = U+03b8
		\regex_replace_all:nnN
		{ ([th]){2,2} }
		{ \x{03b8} }
		\l_xander_oper_tl
		%% change every ss into c U+0327
		\regex_replace_all:nnN
		{ ([ss]){2,2} }
		{ c \x{0327} }
		\l_xander_oper_tl  
		%% change every s into s U+030C
		\regex_replace_all:nnN
		{ ([sh]){2,2} }
		{ s \x{030c} }
		\l_xander_oper_tl
		%% change every am into AM
		\regex_replace_all:nnN
		{ ([aur]){3,3} }
		{ |AuraMazda| }
		\l_xander_oper_tl
		%% change every dah into Dah
		\regex_replace_all:nnN
		{ ([dah]){3,3} }
		{ |Dahya \x{0304}ush| }
		\l_xander_oper_tl
		%% change every baga into Baga
		\regex_replace_all:nnN
		{ ([baga]){4,4} }
		{ |BAGA| }
		\l_xander_oper_tl
		%% change every buu into Buumish
		\regex_replace_all:nnN
		{ ([buu]){3,3} }
		{ |Buumish| }
		\l_xander_oper_tl
		%% change |...| into raised small-caps
		\regex_replace_all:nnN
		{ \|([^|]+)\| }
		{ \c{raisebox}\cB\{0.5ex\cE\}\cB\{\c{textsc}\cB\{\1\cE\}\cE\} }
		\l_xander_oper_tl
		%% change every buu into Buumish
		\regex_replace_all:nnN
		{ ([Buumish]){7,7} }
		{ Bu\x{0304}mis\x{030c} }
		\l_xander_oper_tl
		%% print the result
		\tl_use:N \l_xander_oper_tl
		}
		\ExplSyntaxOff

		\setstackgap{L}{.75\normalbaselineskip}
		\newcommand\rubyop[1]{\Longstack{\transop{#1} \textop{#1}}}  

		\setlength\parindent{0pt}
		\setlength\parskip{1.25\baselineskip}
		\def\baselinestretch{1.5}

		\begin{document}

		\section{Old Persian \textop{la-da div pa-aur-ra-sa-i-a-na}}

		\begin{center}
		\rubyop{a}
		\rubyop{i}
		\rubyop{u}
		\rubyop{ka}
		\rubyop{ku}
		\rubyop{ga}
		\rubyop{gu}
		\rubyop{xa} \par
		\rubyop{a-i-u-ka-ku-ga-gu-xa}
		\end{center}

		\begin{center}
		\rubyop{cha}
		\rubyop{tha}
		\rubyop{sha}
		\rubyop{ssa} \par
		\rubyop{cha-tha-sha-ssa}
		\end{center}

		\begin{center}
		\rubyop{aur}
		\rubyop{aur2}
		\rubyop{aur3}
		\rubyop{xx} \par
		\rubyop{aur-aur2-aur3-xx}
		\end{center}

		\begin{center}
		\rubyop{dah}
		\rubyop{dah2}
		\rubyop{baga}
		\rubyop{buu} \par
		\rubyop{dah-dah2-baga-buu}
		\end{center}

		\section{Son of Darius}

		\verb|\textop{da-a-ra-ya-va-ha-u-sha}| → \textop{da-a-ra-ya-va-ha-u-sha} 

		\verb|\transop{da-a-ra-ya-va-ha-u-sha}| → \transop{da-a-ra-ya-va-ha-u-sha}

		\verb|\rubyop{da-a-ra-ya-va-ha-u-sha}| → \rubyop{da-a-ra-ya-va-ha-u-sha}

		\end{document}

[jamo]
description: This template shows an usage example of the pmhanguljamo package.
output: myjamo
compiler: -c
tex: 	\documentclass{article}

		\usepackage{fontspec}
		\usepackage{pmhanguljamo}
		\setmainfont{Noto Serif CJK KR}[Script=Hangul]
		\setlength\parskip{.5\baselineskip}
		\setlength\parindent{0pt}

		\begin{document}

		\section{Old Hangul}

		\verb|\jamoword{an/nyex/ha/sei/yo}| 
		→ \jamoword{an/nyex/ha/sei/yo}

		\begin{verbatim}
		\begin{verse}
		\begin{jamotext}
		na bo/gi/ga yeg/gye/ue \\
		ga/sir ddai/ei/nvn \\
		mar ebs/i go/i bo/nai dv/ri/u/ri/da/.
		yex/byen/ei yag/san \\
		jin/dar/rai ggoc \\
		a/rvm dda/da ga/sir gir/ei bbu/ri/u/ri/da/.
		ga/si/nvn ger/vm ger/vm \\
		noh/in gv ggoc/vr \\
		sa/bbun/hi jv/rye/barb/go ga/si/ob/so/se
		na bo/gi/ga yeg/gye/ue \\
		ga/sir ddai/ei/nvn \\
		jug/e/do a/ni nun/mur hvr/ri/u/ri/da/.
		\end{jamotext}
		\end{verse}
		\end{verbatim}

		\begin{verse}
		\begin{jamotext}
		na bo/gi/ga yeg/gye/ue \\
		ga/sir ddai/ei/nvn \\
		mar ebs/i go/i bo/nai dv/ri/u/ri/da/.
		yex/byen/ei yag/san \\
		jin/dar/rai ggoc \\
		a/rvm dda/da ga/sir gir/ei bbu/ri/u/ri/da/.
		ga/si/nvn ger/vm ger/vm \\
		noh/in gv ggoc/vr \\
		sa/bbun/hi jv/rye/barb/go ga/si/ob/so/se
		na bo/gi/ga yeg/gye/ue \\
		ga/sir ddai/ei/nvn \\
		jug/e/do a/ni nun/mur hvr/ri/u/ri/da/.
		\end{jamotext}
		\end{verse}

		\begin{verbatim}
		\begin{jamotext}
		na/ras;mar:ss@/mi; dyuq/guig;ei; dar/a;
		mun/jj@x;oa;ro; se/rv s@/m@s/di; a/ni;h@r/ss@i;
		i;ren jyen/c@;ro; e/rin; b@ig;syeq;i;
		ni/rv/go;jye; horf; bai;
		i/sye;do; m@/c@m;nai: jey bdv;dvr; si/re; pye/di;
		mod:h@rf no;mi; ha/ni;ra;.
		\end{jamotext}
		\end{verbatim}

		\begin{jamotext}
		na/ras;mar:ss@/mi; dyuq/guig;ei; dar/a;
		mun/jj@x;oa;ro; se/rv s@/m@s/di; a/ni;h@r/ss@i;
		i;ren jyen/c@;ro; e/rin; b@ig;syeq;i;
		ni/rv/go;jye; horf; bai;
		i/sye;do; m@/c@m;nai: jey bdv;dvr; si/re; pye/di;
		mod:h@rf no;mi; ha/ni;ra;.
		\end{jamotext}

		\newpage

		\section{Revised Romanization of Korean}

		\let\jamoword\relax
		\let\jamotext\relax
		\let\endjamotext\relax
		\ExplSyntaxOn
		\input{pmhanguljamo-rrk.sty}
		\ExplSyntaxOff

		\begin{verbatim}
		\usepackage[RRK]{pmhanguljamo}
		\end{verbatim}

		\verb|\jamoword{annyeonghase-yo}| 
		→ \jamoword{annyeonghase-yo}

		\begin{verbatim}
		\begin{jamotext}
		na bogiga yeoggyeo-wo \\
		gasil ttae-eneun \\
		mal eobs-i go-i bonae deuli-ulida.
		yeongbyeon-e yagsan \\
		jindallae kkoch \\
		aleum ttada gasil gil-e ppuli-ulida.
		gasineun geol-eum geol-eum \\
		noh-in geu kkoch-eul \\
		sappunhi jeulyeobalbgo gasi-obsoseo
		na bogiga yeoggyeo-wo \\
		gasil ttae-eneun \\
		jug-eodo ani nunmul heulli-ulida.
		\end{jamotext}
		\end{verbatim}

		\begin{jamotext}
		na bogiga yeoggyeo-wo \\
		gasil ttae-eneun \\
		mal eobs-i go-i bonae deuli-ulida.
		yeongbyeon-e yagsan \\
		jindallae kkoch \\
		aleum ttada gasil gil-e ppuli-ulida.
		gasineun geol-eum geol-eum \\
		noh-in geu kkoch-eul \\
		sappunhi jeulyeobalbgo gasi-obsoseo
		na bogiga yeoggyeo-wo \\
		gasil ttae-eneun \\
		jug-eodo ani nunmul heulli-ulida.
		\end{jamotext}

		\end{document}

[Steve]
description: Steve Jobs's commencement speech addressed at Standford University in 2005.
output:	SteveSpeech
cmd: 	wi.py https://www.nydailynews.com/resizer/Y-gbFbQokC9Cw2PdW3Z-HNE2CpU=/800x532/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/OVN7AWY3V4IGG6CKIYUEF657WY.jpg -o SteveJobs
		ltx.py SteveSpeech -b -c -v
tex:	\documentclass{article}
		\usepackage[a4paper, margin={3cm, 3cm}]{geometry}
		\usepackage{graphicx}
		\usepackage{wrapfig}

		\author{Steve Jobs}
		\title{Commencement Speech at Stanford University}
		\date{June 12, 2005}

		\begin{document}

		\maketitle

		\begin{wrapfigure}{l}{.5\textwidth}
		\includegraphics[width=\linewidth]{SteveJobs.jpg}
		\end{wrapfigure}

		I am honored to be with you today at your commencement from one of the finest universities in the world. I never graduated from college. Truth be told, this is the closest I've ever gotten to a college graduation. Today I want to tell you three stories from my life. That's it. No big deal. Just three stories.
		
		The first story is about connecting the dots.
		
		I dropped out of Reed College after the first 6 months, but then stayed around as a drop-in for another 18 months or so before I really quit. So why did I drop out?
		
		It started before I was born. My biological mother was a young, unwed college graduate student, and she decided to put me up for adoption. She felt very strongly that I should be adopted by college graduates, so everything was all set for me to be adopted at birth by a lawyer and his wife. Except that when I popped out they decided at the last minute that they really wanted a girl. So my parents, who were on a waiting list, got a call in the middle of the night asking: "We have an unexpected baby boy; do you want him?" They said: "Of course." My biological mother later found out that my mother had never graduated from college and that my father had never graduated from high school. She refused to sign the final adoption papers. She only relented a few months later when my parents promised that I would someday go to college.
		
		And 17 years later I did go to college. But I naively chose a college that was almost as expensive as Stanford, and all of my working-class parents' savings were being spent on my college tuition. After six months, I couldn't see the value in it. I had no idea what I wanted to do with my life and no idea how college was going to help me figure it out. And here I was spending all of the money my parents had saved their entire life. So I decided to drop out and trust that it would all work out OK. It was pretty scary at the time, but looking back it was one of the best decisions I ever made. The minute I dropped out I could stop taking the required classes that didn't interest me, and begin dropping in on the ones that looked interesting.
		
		It wasn't all romantic. I didn't have a dorm room, so I slept on the floor in friends' rooms, I returned coke bottles for the 5¢ deposits to buy food with, and I would walk the 7 miles across town every Sunday night to get one good meal a week at the Hare Krishna temple. I loved it. And much of what I stumbled into by following my curiosity and intuition turned out to be priceless later on. Let me give you one example:
		
		Reed College at that time offered perhaps the best calligraphy instruction in the country. Throughout the campus every poster, every label on every drawer, was beautifully hand calligraphed. Because I had dropped out and didn't have to take the normal classes, I decided to take a calligraphy class to learn how to do this. I learned about serif and san serif typefaces, about varying the amount of space between different letter combinations, about what makes great typography great. It was beautiful, historical, artistically subtle in a way that science can't capture, and I found it fascinating.
		
		None of this had even a hope of any practical application in my life. But ten years later, when we were designing the first Macintosh computer, it all came back to me. And we designed it all into the Mac. It was the first computer with beautiful typography. If I had never dropped in on that single course in college, the Mac would have never had multiple typefaces or proportionally spaced fonts. And since Windows just copied the Mac, it's likely that no personal computer would have them. If I had never dropped out, I would have never dropped in on this calligraphy class, and personal computers might not have the wonderful typography that they do. Of course it was impossible to connect the dots looking forward when I was in college. But it was very, very clear looking backwards ten years later.
		
		Again, you can't connect the dots looking forward; you can only connect them looking backwards. So you have to trust that the dots will somehow connect in your future. You have to trust in something — your gut, destiny, life, karma, whatever. This approach has never let me down, and it has made all the difference in my life.
		
		My second story is about love and loss.
		
		I was lucky — I found what I loved to do early in life. Woz and I started Apple in my parents garage when I was 20. We worked hard, and in 10 years Apple had grown from just the two of us in a garage into a \$2 billion company with over 4000 employees. We had just released our finest creation — the Macintosh — a year earlier, and I had just turned 30. And then I got fired. How can you get fired from a company you started? Well, as Apple grew we hired someone who I thought was very talented to run the company with me, and for the first year or so things went well. But then our visions of the future began to diverge and eventually we had a falling out. When we did, our Board of Directors sided with him. So at 30 I was out. And very publicly out. What had been the focus of my entire adult life was gone, and it was devastating.
		
		I really didn't know what to do for a few months. I felt that I had let the previous generation of entrepreneurs down - that I had dropped the baton as it was being passed to me. I met with David Packard and Bob Noyce and tried to apologize for screwing up so badly. I was a very public failure, and I even thought about running away from the valley. But something slowly began to dawn on me — I still loved what I did. The turn of events at Apple had not changed that one bit. I had been rejected, but I was still in love. And so I decided to start over.
		
		I didn't see it then, but it turned out that getting fired from Apple was the best thing that could have ever happened to me. The heaviness of being successful was replaced by the lightness of being a beginner again, less sure about everything. It freed me to enter one of the most creative periods of my life.
		
		During the next five years, I started a company named NeXT, another company named Pixar, and fell in love with an amazing woman who would become my wife. Pixar went on to create the worlds first computer animated feature film, Toy Story, and is now the most successful animation studio in the world. In a remarkable turn of events, Apple bought NeXT, I returned to Apple, and the technology we developed at NeXT is at the heart of Apple's current renaissance. And Laurene and I have a wonderful family together.
		
		I'm pretty sure none of this would have happened if I hadn't been fired from Apple. It was awful tasting medicine, but I guess the patient needed it. Sometimes life hits you in the head with a brick. Don't lose faith. I'm convinced that the only thing that kept me going was that I loved what I did. You've got to find what you love. And that is as true for your work as it is for your lovers. Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. As with all matters of the heart, you'll know when you find it. And, like any great relationship, it just gets better and better as the years roll on. So keep looking until you find it. Don't settle.
		
		My third story is about death.
		
		When I was 17, I read a quote that went something like: "If you live each day as if it was your last, someday you'll most certainly be right." It made an impression on me, and since then, for the past 33 years, I have looked in the mirror every morning and asked myself: "If today were the last day of my life, would I want to do what I am about to do today?" And whenever the answer has been "No" for too many days in a row, I know I need to change something.
		
		Remembering that I'll be dead soon is the most important tool I've ever encountered to help me make the big choices in life. Because almost everything — all external expectations, all pride, all fear of embarrassment or failure - these things just fall away in the face of death, leaving only what is truly important. Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to lose. You are already naked. There is no reason not to follow your heart.
		
		About a year ago I was diagnosed with cancer. I had a scan at 7:30 in the morning, and it clearly showed a tumor on my pancreas. I didn't even know what a pancreas was. The doctors told me this was almost certainly a type of cancer that is incurable, and that I should expect to live no longer than three to six months. My doctor advised me to go home and get my affairs in order, which is doctor's code for prepare to die. It means to try to tell your kids everything you thought you'd have the next 10 years to tell them in just a few months. It means to make sure everything is buttoned up so that it will be as easy as possible for your family. It means to say your goodbyes.
		
		I lived with that diagnosis all day. Later that evening I had a biopsy, where they stuck an endoscope down my throat, through my stomach and into my intestines, put a needle into my pancreas and got a few cells from the tumor. I was sedated, but my wife, who was there, told me that when they viewed the cells under a microscope the doctors started crying because it turned out to be a very rare form of pancreatic cancer that is curable with surgery. I had the surgery and I'm fine now.
		
		This was the closest I've been to facing death, and I hope it's the closest I get for a few more decades. Having lived through it, I can now say this to you with a bit more certainty than when death was a useful but purely intellectual concept:
		
		No one wants to die. Even people who want to go to heaven don't want to die to get there. And yet death is the destination we all share. No one has ever escaped it. And that is as it should be, because Death is very likely the single best invention of Life. It is Life's change agent. It clears out the old to make way for the new. Right now the new is you, but someday not too long from now, you will gradually become the old and be cleared away. Sorry to be so dramatic, but it is quite true.
		
		Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma — which is living with the results of other people's thinking. Don't let the noise of others' opinions drown out your own inner voice. And most important, have the courage to follow your heart and intuition. They somehow already know what you truly want to become. Everything else is secondary.
		
		When I was young, there was an amazing publication called The Whole Earth Catalog, which was one of the bibles of my generation. It was created by a fellow named Stewart Brand not far from here in Menlo Park, and he brought it to life with his poetic touch. This was in the late 1960's, before personal computers and desktop publishing, so it was all made with typewriters, scissors, and polaroid cameras. It was sort of like Google in paperback form, 35 years before Google came along: it was idealistic, and overflowing with neat tools and great notions.
		
		Stewart and his team put out several issues of The Whole Earth Catalog, and then when it had run its course, they put out a final issue. It was the mid-1970s, and I was your age. On the back cover of their final issue was a photograph of an early morning country road, the kind you might find yourself hitchhiking on if you were so adventurous. Beneath it were the words: "Stay Hungry. Stay Foolish." It was their farewell message as they signed off. Stay Hungry. Stay Foolish. And I have always wished that for myself. And now, as you graduate to begin anew, I wish that for you.
		
		Stay Hungry. Stay Foolish.
		
		Thank you all very much.
		\end{document}

[critic]
description: Yi Jeonhwa's criticism of an exhibition of art
output: us_against_you
compiler: -c
tex:	\documentclass[korean, Noto]{hzguide}

		\LayoutSetup{}
		\HeadingSetup{
			paragraphstyle=indent,
			linespacing=1.5,
		}
		\pagestyle{plain}
		\DecolorHyperlinks*
		\setmainhangulfont{Noto Serif CJK KR}[UprightFont={* Medium}, BoldFont={* SemiBold}]
		\AnnotateSetup{font=\footnotesize}
		\ExplSyntaxOn
		\NewDocumentCommand \piece { s m }
		{
			\IfBooleanTF { #1 }{《 }{〈 }
			\textcolor{Navy}{ \textbf{#2} }
			\IfBooleanTF { #1 }{ 》}{ 〉}    
		}
		\ExplSyntaxOff

		\title{(이미) 우리와 (아직) 당신들}
		\author{이정화\anota{미술 비평}}
		\date{2020년 5월}

		\begin{document}

		\maketitle

		뉴노멀\anota{new normal} 시대는 코로나로 인해 실감케 된 것 같다.
		면대면으로 경험한 모든 것들이 더 이상 기능하지 않으면서 비대면으로 가능한 가상들이 대안이 되었다.
		이번 전시 역시 온라인으로 먼저 감상해야 했다.\footnote{\url{http://usagainstyou.com}}
		실토하자면, 몸을 이끌고 간 전시장보다 어느 면에서는 더 잘 봤다.
		정리된 아카이브의 도움을 받았고, 소리로 전달되는 작업은 외부 잡음이 없으니 집중이 잘 되었다.
		시각 체험은 가상과 실재라는 두 개의 장이 마련되어 입체성을 띠며, 지평이 넓어졌다.
		이러다 가상 공간의 전시가 전시의 표준이 되는 것은 아닐까.
		작가들은 이제 지구상 동시 접속이 가능한 감상자와 우주 어딘가에서 웹을 여는 외계 감상자를 의식해야 하나.
		비대면 시대가 지속되고, VR, AI, 3D 등을 포함한 가상 플랫폼이 시각예술 활동의 반경을 규정하는 기준이 된다면 가상은 실재의 자리를 대체할 것이고, 사실상 그 경계는 무의미해지리라.
		우리의 상상은 어느 지평에서나 대안을 찾는다.

		\piece*{우리와 당신들\anota{Us Against You}}은 이러한 상념에 점을 찍어 주는 전시였다.\anota{2020년 4월 17일부터 8월 30일까지, 경기도미술관}
		전시는 우리가 함께 살아가게 될 이웃은 과연 누구이고, 그들이 어떠한 공존과 협업의 관계를 제안하는지 모색한다.
		변화하는 세계와 다양한 존재자들, 그들이 가져오는 협업의 방식들에 대해 고민한 열한 명\anota{권병준, 김규호, 노진아, 삼손 영, 소니아 쿠라나, 심학철, 이우성, 이장원, 전진경, 파트타임스위트, 황연주}의 작가와 두 팀\anota{아크로바틱 코스모스, 아트 레이버}이 참여했다.

		하루 쉰 명의 제한된 인원만 감상이 가능한 미술관 2층 전시장에---마스크를 쓴 채---들어서자 심학철 작가의 \piece{이방인 시리즈}\anota{2014--2018}와 유연주 작가의 \piece{H양의 그릇가게}\anota{2016--}가 먼저 눈에 들어온다.
		연변에서 사진을 찍었던 심학철 작가는 안산에서 만난 외국인 노동자들의 모습을 사진에 담았다.
		그의 작업이 이곳이 여전히 균열투성이 현실계임을 인지하게 했다면, 유연주 작가의 그릇 오브제들은 당황스러웠다.
		물성이 낯선 동시에 반가웠기 때문이다.
		세상에 유용한 상품가치와 교환가치가 대체할 수 없는 진정한 가치를 드러내는 작가의 작업을 인지하기도 전에, 바닥 위에 오롯이 놓인 물\anota{物} 자체에서 온기가 전달되었다.
		가상이 과연 이 직접성을 전달할 수 있을까.
		본 전시는 우리를 어제와 다르게 재구성되는 물질적, 정보적 개체로 정의하고, 우리와 다른 곳에서 왔고, 다른 말로 노래를 부르고, 신체 모양이 다르며, 때로 법의 테두리 바깥에서 지내는 존재들인 당신들을 호명한다.
		당신들은 한국, 남성, 정치적 시민, 이성애자, 그리고 이방인이자 여성, 식물과 동물, 기계, 그리고 지구다.

		\section*{(이미) 우리는}

		우리는 이미 포스트휴먼 시대에 도착했다.
		포스트휴먼적 관점에서 인간은 다른 형태의 생명이나 존재를 분리하거나 예외적인 것으로 바라보지 않는다.
		인간은 생물학적 유기체로서의 인간이든 기술적으로 변형된 인간이든 다양한 형태의 주체이자 행위자이며, 여타의 생명 및 기계와 더불어 살아가고 진화해 나간다.
		인간은 그 다양한 것들에서 위안을 얻고 그것과 관계 맺으며 세계의 의미를 형성한다.
		이때 인간은 다양한 기계 및 생명의 우위에 있거나 위계를 형성하는 것이 아니며, 다른 형태의 생명과 서로 의존하면서 공진화한다.
		이러한 포스트휴먼적 관점을 보여 주는 작품이 파트타임스위트의 \piece{이웃들}\anota{2019--2020}이다.
		이 작업에서는 전 세계 온라인 웹캠이 송출하는 이미지들과 미술관 곳곳에 설치된 IP 카메라가 보내는 삼차원 이미지들이 실시간으로 모여 마치 은하계처럼 보이는 세계를 구성한다.
		인간은 유용한 정보 중심으로 이미지들을 구성하지만, 파트타임스위트의 작업에서 유용성의 기준은 모든 존재와의 조화로운 공생으로 보인다.
		마치 영화 \piece{콘텍트}에서 외계 생명체가 인간에게 그려내 보이는 상형문자와 같이 생경한 이미지를 구현하지만, 그 방향은 다른 생명의 형태와 생태계 모든 것들을 향해 열려 있다.

		노진아 작가의 \piece{나의 기계 엄마}\anota{2019}는 진짜 내 어머니의 얼굴과 목소리를 가지고 딥러닝\anota{deep learning}을 통해 우리의 감정을 배운 기계 엄마를 보여 준다.
		기계 엄마는 심지어 모성애마저 학습하여 진짜 엄마의 마음과 가까워진다.
		작가의 작업은 최근 MIT에서 자식과 부모의 돌봄을 받지 못하는 노인과 고아들을 위해 개발한 돌봄 로봇을 연상시킨다.
		냉혹하고 잔인한 인간 엄마와 따듯하고 사랑을 지닌 기계 엄마 중 당신은 누구를 선택하게 될까.
		이장원 작가는 여기서 더 나아가, 미래의 모습을 기술적 진화를 거듭하고 있는 컴퓨터 운영체계\anota{operating system}에서 발견한다.
		OS는 모든 하드웨어와 소프트웨어를 포함하여 시스템 전체를 관리, 감독하는 실행자이며, 미래의 기술적 존재자의 핵심이다.
		작가가 상상하는 미래의 OS인 \piece{윌슨}은 우주에 존재하는 태양을 데이터 기반의 모션 기법으로 시각화한 것으로, 영화 \piece{캐스트 어웨이}에서 무인도에 혼자 남겨진 주인공의 유일한 친구\anota{배구공} 이름이기도 하다.
		작가의 작업에서 영화 \piece{HER}에 등장하는 전지전능한 OS 그녀가 어른거린다.
		그녀를 독점할 수 있다면 인간 아닌 것이 문제가 될까.
		이러한 작업들은 포스트휴먼 시대의 진정한 가치가 무엇인지 질문하게 한다.
		우리는 원하든 원치 않든 이질적인 것들과 함께 있다.

		\section*{(아직) 당신들은}

		당신들은 아직 포스트휴머니즘\anota{posthumanism}에 도착하지 않았다.
		포스트휴머니즘은 인간의 경계를 확장하는 것에서 나아가, 우리와 당신들을 구분하는 모든 차별들을 극복하는 것에 목적을 둔다.
		인간이 모든 비인간 존재들과 연결되어 있다는 인식을 공유한다면 이웃과의 이질적 거리를 극복할 수 있을까.
		그러나 우리가 감수하는 이질성은 우리에게 유용할 때, 우리의 결핍을 채워 줄 때다.
		이웃의 결핍을 보았을 때 우리의 태도는 어떠한가.
		소니아 쿠라나는 광장이나 묘지 바닥에 누워 있는 퍼포먼스를 통해 정해진 (성의) 역할에 저항하는 주체가 된다.
		작가는 페미니즘을 하나의 스타일이 아닌 삶의 철학이나 태도, 정치적 도구로 여기며, 눕는 행위를 통해 물질과 중력의 법칙에 맞서고 관습과 편견에 도전한다.
		타인들의 무관심 속에서 먼지를 뒤집어 쓴 채 광장에 누워 있는 작가의 주변을 둘러싼 이웃은 비인간 존재인 새 떼들이다.
		그들은 목적 없이 작가의 연대에 동참하듯 그 신체를 에워싼다.

		호치민에서 결성한 콜렉티브인 아트 레이버\anota{아를레트 퀸, 안 트란, 타오 능옌 판, 트루옹 콩퉁}는 수백 년간 풍부한 문화적 수혜를 누리며 살아온 베트남 중부 고원 지라이 지방 사람들이 급속한 산업화에 떠밀려 임금 노동자가 된 현실을 환기시키며, 지라이의 이슬 해먹이 놓인 카페를 꾸몄다.
		인간에서 비인간(자연)으로, 그리고 다시 이슬처럼 증발하는 윤회적 세계관을 감상자는 지라이의 이슬에 누워 경험하게 된다.
		바로 옆에 전진경 작가가 만든 EPS의 공간 \piece{마당의 실내}\anota{2015-2020}이 놓여 있다.
		작가는 콜트콜텍 기타 노동자들의 농성 천막에 작업실을 만들고 매주 그림을 그렸고, 농성장이 강제로 철거되자 작업실을 경의선 공유지의 EPS 안으로 옮겨 왔다.
		홍콩을 기반으로 활동하는 삼손 영은 홍콩에서 가장 오래된 노조에서 만든 콴 싱 합창단에게 \piece{위 아 더 월드}(2017)를 음을 소거한 채 소리 없이 불러 달라 청했다.
		1985년 아프리카 기아 난민들을 위한 모금을 독려하기 위해 마이클 잭슨을 비롯한 유명 팝 가수들이 함께 부른 이 노래는 희망의 하모니로 기억되지만, 현재 당신들에게 희망은 멀다.
		연대하는 이들은 여전히 소수이고, 여기는 당신들이 귀환할 수 있는 고향도 유토피아도 아니다.

		\piece*{우리와 당신들}은 이미 우리에게 도착한 포스트휴먼\anota{posthuman}의 세계에 대해 조망케 하고, 아직 당신들에게 도착하지 않은 부조리한 현실을 바라보게 한다.
		전시를 통해 우리는 이 인류세라는 현실에서 우리가 이미 당신들과 다양한 관계를 맺고 있음을, 나는 (이미) 친숙한 우리이자 (아직) 낯선 당신들인 이웃과 마주해야 함을 되새기게 한다.
		우리라는 단어는 양가감정을 일으킨다.
		내가 우리 안에 속해 있을 때 이 단어는 친밀한 느낌이 든다.
		반면 내가 우리 안에 속해 있지 않을 때 이 단어는 낯설고 무섭다.
		우리는 이웃이라는 외상과 만나야만 주체가 되며, 우리 안의 이질적인 것이 함께 있음을 자각해야만 이웃과 공생할 수 있다.
		우리가 온전한 인간이라고 착각하며 우리의 이질적 이웃을 망각한다면, 도래하는 뉴노멀 시대에 우리의 자리는 어디에서도 찾을 수 없을지 모른다.
		우리는 이미 한국, 남성, 정치적 시민, 이성애자, 그리고 이방인이자 여성, 식물과 동물, 기계, 그리고 지구이기에.
		\end{document} 

[oesol]
output: oesolscript
compiler: -c
sty:	`\ProvidesPackage{oesolscript}[2020/05/26 v0.3.3]
		`\RequirePackage{xparse}
		`\RequirePackage{l3keys2e}
		`\RequirePackage{fontspec}
		`
		`\ExplSyntaxOn
		`\bool_new:N \g_ui_bool
		`
		`\keys_define:nn { oesolscript }
		`{
		`	fontfile	.tl_set:N = \g_fontfile_tl,
		`	uivowel		.choice:,
		`	uivowel/ui	.code:n = { \bool_gset_true:N \g_ui_bool },
		`	uivowel/wi	.code:n = { \bool_gset_false:N \g_ui_bool },
		`}
		`
		`\keys_set:nn { oesolscript }
		`{
		`	fontfile = CMUOSerif-Roman.otf,
		`	uivowel = ui
		`}
		`
		`\ProcessKeysOptions { oesolscript }
		`
		`\seq_new:N \l_oesol_seq
		`
		`\NewDocumentCommand \oesolscript { m }
		`{
		`	\seq_set_split:Nnn \l_oesol_seq { ~ } { #1 }
		`	
		`	\int_set:Nn \l_tmpa_int { \seq_count:N \l_oesol_seq }
		`	
		`	\seq_indexed_map_inline:Nn \l_oesol_seq
		`	{
		`		\oesol_process_a_word:n { ##2 }
		`		\int_compare:nT { \l_tmpa_int > ##1 }
		`		{
		`			{}~  
		`		}
		`	}
		`}
		`
		`\NewDocumentCommand \oesolvar { m }
		`{
		`	\seq_set_split:Nnn \l_oesol_seq { ~ } { #1 }
		`	
		`	\int_set:Nn \l_tmpa_int { \seq_count:N \l_oesol_seq }
		`	
		`	\seq_indexed_map_inline:Nn \l_oesol_seq
		`	{
		`		\script_a_word:n { ##2 }
		`		\int_compare:nT { \l_tmpa_int > ##1 }
		`		{
		`			{}~
		`		}
		`	}
		`}
		`
		`\cs_new:Npn \oesol_process_a_word:n #1
		`{
		`	\oesolProcessAWord { #1 }
		`}
		`
		`\int_new:N \l_code_int
		`\int_const:Nn \c_start_point { 44032 }   %% `가'
		`
		`\tl_new:N \g_output_tl
		`
		`\prop_new:N \dict_cho
		`\prop_new:N \dict_jung
		`\prop_new:N \dict_jong
		`
		`\cs_new:Npn \dict_fn:nn #1 #2
		`{
		`	\clist_set:Nn \l_tmpb_clist { #2 }
		`	\clist_map_inline:Nn \l_tmpb_clist
		`	{
		`		\use:c { items_to_prop_ #1 :w } ##1 \q_stop
		`	}
		`}
		`
		`\cs_new:Npn \items_to_prop_cho:w #1 = #2 \q_stop
		`{
		`	\prop_put:Nnn \dict_cho { #1 } { #2 }
		`}
		`
		`\cs_new:Npn \items_to_prop_jung:w #1 = #2 \q_stop
		`{
		`	\prop_put:Nnn \dict_jung { #1 } { #2 }
		`}
		`
		`\cs_new:Npn \items_to_prop_jong:w #1 = #2 \q_stop
		`{
		`	\prop_put:Nnn \dict_jong { #1 } { #2 }
		`}
		`
		`\cs_new:Npn \get_value:nn #1 #2 
		`{
		`	\str_case:nn { #1 } 
		`	{
		`		{ jong } {
		`			\prop_get:cnN { dict _ #1 } { #2 } \l_tmpa_tl
		`			\quark_if_no_value:NTF \l_tmpa_tl
		`			{
		`				\tl_gset:Nn \g_jongcho_tl { \empty }
		`			}
		`			{
		`				\tl_gset_eq:NN \g_jongcho_tl \l_tmpa_tl
		`			}
		`		}
		`		{ cho  } {
		`			\prop_get:cnN { dict _ #1 } { #2 } \l_tmpa_tl
		`			\quark_if_no_value:NTF \l_tmpa_tl
		`			{
		`				\tl_gput_right:Nn \g_output_tl { \g_jongcho_tl }
		`			}
		`			{
		`				\tl_gconcat:NNN \g_jong_and_cho \g_jongcho_tl \l_tmpa_tl
		`				\tl_gput_right:Nx \g_output_tl { \g_jong_and_cho }
		`			}
		`		}
		`		{ jung } {
		`			\prop_get:cnN { dict _ #1 } { #2 } \l_tmpa_tl
		`			\quark_if_no_value:NTF \l_tmpa_tl
		`			{
		`			}
		`			{
		`				\tl_gput_right:Nx \g_output_tl { \l_tmpa_tl }
		`			}
		`		}
		`	}
		`}
		`
		`\dict_fn:nn { cho }
		`{
		`	0=g, 1=gg, 2=n, 3=d, 4=dd, 5=l, 6=m, 7=b, 8=bb, 9=s,
		`	10=ss, 11={}, 12=j, 13=jj, 14=c, 15=k, 16=t, 17=p, 18=h
		`}
		`
		`\bool_if:NTF \g_ui_bool
		`{
		`	\dict_fn:nn { jung }
		`	{
		`		0=a, 1=axi, 2=ya, 3=yaxi, 4=e, 5=exi, 6=ye, 7=yexi,
		`		8=o, 9=voa, 10=voaxi, 11=oxi, 12=yo, 13=u, 14=vue,
		`		15=vuexi, 16=vui, 17=yu, 18=z, 19=vzi, 20=i
		`	}
		`}
		`{
		`	\dict_fn:nn { jung }
		`	{
		`		0=a, 1=axi, 2=ya, 3=yaxi, 4=e, 5=exi, 6=ye, 7=yexi,
		`		8=o, 9=voa, 10=voaxi, 11=oxi, 12=yo, 13=u, 14=vue,
		`		15=vuexi, 16=uxi, 17=yu, 18=z, 19=vzi, 20=i
		`	}
		`}
		`
		`\dict_fn:nn { jong }
		`{
		`	0=\empty,
		`	1=g, 2=gg, 3=gs, 4=n, 5=nj, 6=nh, 7=d, 8=l, 
		`	9=lg, 10=lm, 11=lb, 12=ls, 13=lt, 14=lp, 15=lh,
		`	16=m, 17=b, 18=bs, 19=s, 20=ss, 21=q, 22=j, 23=c, 24=k,
		`	25=t, 26=p, 27=h
		`}
		`
		`\NewDocumentCommand \oesolProcessAWord { m }
		`{
		`	\tl_gclear:N \g_output_tl
		`	\tl_clear:N \g_jongcho_tl
		`	\tl_clear:N \g_jong_and_cho
		`
		`	\tl_set:Nn \l_tmpa_tl { #1 }
		`	
		`	\tl_put_right:Nn \l_tmpa_tl { ! }
		`
		`	\tl_map_inline:Nn \l_tmpa_tl
		`	{
		`		\str_case:nnTF { ##1 } 
		`		{
		`			{ - } {	\tl_gput_right:Nn \g_jongcho_tl { - } }
		`			{ ! } { \tl_gput_right:Nx \g_output_tl { \g_jongcho_tl } }
		`			{ * } { \tl_gput_right:Nx \g_jongcho_tl { * } }
		`			{ + } { \tl_gput_right:Nn \g_jongcho_tl { + } }
		`			{ . } { \tl_gput_right:Nn \g_jongcho_tl { . } }
		`			{ , } { \tl_gput_right:Nn \g_jongcho_tl { , } }
		`		}
		`		{ } 
		`		{
		`			\to_RR_a_char:n { ##1 }
		`		}
		`	}
		`
		`	\regex_replace_all:nnN { \* } { \c{tl_upper_case:n }  } \g_output_tl
		`	\regex_replace_all:nnN { \+(.+)\+ } { \c{tl_upper_case:n} \cB({) \1 \cE(}) } \g_output_tl
		`	
		`	\exp_args:Nx \script_a_word:n { \g_output_tl }
		`}
		`
		`\cs_new:Npn \to_RR_a_char:n #1
		`{
		`	\split_hangul:n #1
		`	\exp_args:Nnf \get_value:nn { cho  } { \int_use:N \g_cho_int }
		`	\exp_args:Nnf \get_value:nn { jung } { \int_use:N \g_jung_int }
		`	\exp_args:Nnf \get_value:nn { jong } { \int_use:N \g_jong_int }
		`}
		`
		`\cs_new:Npn \split_hangul:n #1
		`{
		`	\int_zero_new:N \l_basecode_int
		`	\int_zero_new:N \g_cho_int
		`	\int_zero_new:N \g_jung_int
		`	\int_zero_new:N \g_jong_int
		`	\str_set_convert:Nnnn \l_code_tl { #1 } { } { clist }
		`	\exp_args:NNx \int_set:Nn \l_code_int { \l_code_tl }
		`	\bool_if:nT
		`	{
		`		\int_compare_p:n { \l_code_int >= \c_start_point }
		`	&&
		`		\int_compare_p:n { \l_code_int <= 55219 }
		`	}
		`	{
		`		\int_set:Nn \l_basecode_int { \l_code_int - \c_start_point }
		`		\exp_args:Nx \get_lvt_code:n { \int_use:N \l_basecode_int }
		`	}
		`}
		`
		`\cs_new:Npn \get_lvt_code:n #1
		`{
		`	\int_set:Nn \g_cho_int { \int_div_truncate:nn { #1 } { 588 } }
		`	\int_set:Nn \g_jung_int { \int_div_truncate:nn { #1 - 588 * \g_cho_int } { 28 } }
		`	\int_set:Nn \g_jong_int { #1 - \g_cho_int * 588 - \g_jung_int * 28 }
		`}
		`
		`\cs_new:Npn \script_a_word:n #1
		`{
		`	\group_begin:
		`	\bool_set_false:N \g_marker_bool
		`	\exp_args:No \fontspec { \g_fontfile_tl } [ BoldFont = \g_fontfile_tl, BoldFeatures = { FakeBold = 1.06 }, AutoFakeSlant ]
		`	\tl_set:Nn \l_tmpa_tl { #1 }
		`	\tl_map_function:NN \l_tmpa_tl \treat_a_char:n
		`	\group_end:
		`}
		`
		`\bool_new:N \g_marker_bool
		`
		`\cs_new:Npn \treat_a_char:n #1
		`{
		`	\str_case:nnTF { #1 }
		`	{
		`		{ y } { }
		`		{ x } { }
		`		{ v } { }
		`		{ Y } { }
		`		{ X } { }
		`		{ V } { }
		`	}
		`	{ 
		`		\bool_gset_true:N \g_marker_bool
		`		\tl_gset:Nn \g_marker_tl { #1 }
		`	}
		`	{
		`		\bool_if:NTF \g_marker_bool
		`		{
		`			\bool_gset_false:N \g_marker_bool
		`			\tl_gput_right:Nn \g_marker_tl { #1 }
		`			\prop_get:NoN \c_test_prop { \g_marker_tl } \l_tmpb_tl
		`			\quark_if_no_value:NTF \l_tmpb_tl 
		`			{
		`				\tl_use:N \g_marker_tl 
		`			}
		`			{
		`				\tl_use:N \l_tmpb_tl
		`			}
		`		}
		`		{
		`			\prop_get:NnN \c_test_prop { #1 } \l_tmpb_tl
		`			\quark_if_no_value:NTF \l_tmpb_tl
		`			{
		`				\tl_use:N \g_marker_tl
		`			}
		`			{
		`				\tl_use:N \l_tmpb_tl
		`			}
		`		}
		`	}	
		`}
		`
		`\prop_const_from_keyval:Nn \c_test_prop
		`{
		`	g = , G = ,
		`	n = , N = ,
		`	d = , D = ,
		`	l = , L = ,
		`	m = , M = ,
		`	b = , B = ,
		`	s = , S = ,
		`	q = , Q = ,  %% 받침 이응
		`	j = , J = ,
		`	c = , C = ,
		`	k = , K = ,
		`	t = , T = ,
		`	p = , P = ,
		`	h = , H = ,
		`	r = , R = ,
		`	A = , YA = ,
		`	E = , YE = ,
		`	O = , YO = ,
		`	U = , YU = ,
		`	Z = , I = ,   %% 모음 ‘eu(ㅡ)’를 z에 할당
		`	a = , ya = ,
		`	e = , ye = ,
		`	o = , yo = ,
		`	u = , yu = ,
		`	z = , i = ,
		`	XI = , Xi = , %% ㅐ = axi, ㅔ = exi
		`	VO = , VU = , %% ㅘ = voa, ㅝ = voe
		`	VZ = , VI = , %% ㅢ = vzi, ㅑ = via
		`	xi = , vo = ,
		`	vu = , vz = , 
		`	vi = , 
		`	Ya = , Ye = ,
		`	Yo = , Yu = ,
		`	Vo = , Vu = ,
		`	Vz = , Vi = , 
		`	- = {{\rmfamily -}},
		`	. = {{\rmfamily .}},
		`	{,} = {{\rmfamily ,}},
		`	{=} = {\empty},
		`	? = {{\rmfamily ?}},
		`	! = {{\rmfamily !}},
		`	“ = {{\rmfamily “}},
		`	” = {{\rmfamily ”}},
		`	` = {{\rmfamily `}},
		`	' = {{\rmfamily '}},
		`}
		`\seq_new:N \l_oespara_seq
		`\seq_new:N \l_oeswd_seq
		`\tl_new:N  \l_oesword_tl
		`
		`\newcommand*\oesolalign{\raggedright}
		`
		`\NewDocumentEnvironment { oesoltext } { s +b }
		`{
		`	\oesolalign
		`	\oesolpar { #2 }
		`	\IfBooleanTF { #1 } {} { \par }
		`}{}
		`
		`\NewDocumentCommand \oesolpar { +m }
		`{
		`	\seq_set_split:Nnn \l_oespara_seq { \par } { #1 }
		`	\seq_indexed_map_function:NN \l_oespara_seq \oesolpar_proc:nn
		`}
		`
		`\cs_new:Npn \oesolpar_proc:nn #1 #2
		`{
		`	\regex_split:nnN { \s } { #2 } \l_oeswd_seq
		`	\seq_indexed_map_inline:Nn \l_oeswd_seq
		`	{
		`		\oesolpar_prcword:n { ##2 }
		`		\int_compare:nT { ##1 < \seq_count:N \l_oeswd_seq }
		`		{ \space }
		`	}
		`	\int_compare:nT { #1 < \seq_count:N \l_oespara_seq }
		`	{ \par }
		`}
		`
		`\cs_new:Npn \oesolpar_prcword:n #1
		`{
		`	\tl_set:Nn \l_oesword_tl { #1 }
		`	\tl_replace_all:Nnn \l_oesword_tl  { ch } { c }
		`	\tl_replace_all:Nnn \l_oesword_tl  { CH } { C }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Ch } { C }
		`	\tl_replace_all:Nnn \l_oesword_tl  { r  } { l }
		`	\tl_replace_all:Nnn \l_oesword_tl  { R  } { L }
		`	\tl_replace_all:Nnn \l_oesword_tl  { kk } { gg }
		`	\tl_replace_all:Nnn \l_oesword_tl  { tt } { dd }
		`	\tl_replace_all:Nnn \l_oesword_tl  { pp } { bb }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Kk } { Gg }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Tt } { Dd }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Pp } { Bb }
		`	\tl_replace_all:Nnn \l_oesword_tl  { KK } { GG }
		`	\tl_replace_all:Nnn \l_oesword_tl  { TT } { DD }
		`	\tl_replace_all:Nnn \l_oesword_tl  { PP } { BB }
		`	\tl_replace_all:Nnn \l_oesword_tl  { ng } { q  }
		`	\tl_replace_all:Nnn \l_oesword_tl  { NG } { Q  }
		`	
		`	\tl_replace_all:Nnn \l_oesword_tl  { ui } { vzi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { UI } { VZI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Ui } { VZi }
		`
		`	\tl_replace_all:Nnn \l_oesword_tl  { wae } { voaxi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wae } { VOaxi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Ae  } { Axi }
		`
		`	\tl_replace_all:Nnn \l_oesword_tl  { ae  } { axi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { wa  } { voa }
		`	\bool_if:NTF \g_ui_bool
		`	{ \tl_replace_all:Nnn \l_oesword_tl  { wi } { vui } }
		`	{ \tl_replace_all:Nnn \l_oesword_tl  { wi } { uxi } }
		`	\tl_replace_all:Nnn \l_oesword_tl  { e    } { exi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { exio } { e } 
		`	\tl_replace_all:Nnn \l_oesword_tl  { exiu } { z }
		`	\tl_replace_all:Nnn \l_oesword_tl  { wo   } { vue }
		`	\tl_replace_all:Nnn \l_oesword_tl  { wexi } { vuexi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { oexi } { oxi }
		`
		`	\tl_replace_all:Nnn \l_oesword_tl  { WAE } { VOAXI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { AE } { AXI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { WA } { VOA }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wa } { VOa }
		`	\bool_if:NTF \g_ui_bool
		`	{ \tl_replace_all:Nnn \l_oesword_tl  { WI } { VUI } 
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wi } { VUi }
		`	}
		`	{ \tl_replace_all:Nnn \l_oesword_tl  { WI } { UXI } 
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wi } { Uxi }
		`	}
		`	\tl_replace_all:Nnn \l_oesword_tl  { E } { EXI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { EXIO } { E } 
		`	\tl_replace_all:Nnn \l_oesword_tl  { EXIo } { E } 
		`	\tl_replace_all:Nnn \l_oesword_tl  { EXIU } { Z }
		`	\tl_replace_all:Nnn \l_oesword_tl  { EXIu } { Z }
		`	\tl_replace_all:Nnn \l_oesword_tl  { WO } { VUE }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wo } { VUe }
		`	\tl_replace_all:Nnn \l_oesword_tl  { WEXI } { VUEXI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Wexi } { VUexi }
		`	\tl_replace_all:Nnn \l_oesword_tl  { OEXI } { OXI }
		`	\tl_replace_all:Nnn \l_oesword_tl  { Oexi } { Oxi }	
		`	\exp_args:No \oesolvar { \l_oesword_tl }
		`	}
		`	\cs_set_eq:NN \oesol \oesolpar
		`	\ExplSyntaxOff
tex:	\documentclass[a4paper]{article}
		\usepackage{kotex}
		\usepackage[fontfile={CMUO Serif Roman}]{oesolscript}
		\usepackage{hyperref}
		\setmainfont{Noto Serif}
		\setmainhangulfont{Noto Serif CJK KR}

		\setlength\parindent{0pt}
		\def\baselinestretch{1.1}
		\setlength\parskip{1.2\baselineskip}

		\begin{document}

		Tzetachi가 개발한 외솔체 폰트 CMUOSerif-Roman.otf는 \url{https://github.com/Tzetachi/Computer-Modern-Unicode-Oesol}에서 구할 수 있다.
		외솔체 폰트를 이용하여 풀어쓰기를 구현하는 oesolscript 패키지와 설명서는 \url{https://bitbucket.org/novadh/oesolscript/src/master/}에서 구할 수 있다.

		\textbackslash oesol 명령과 oesoltext 환경은 알파벳을 받아서, \textbackslash oesolscript는 한글을 받는다.

		\verb|\oesol{egeseo han=geul eul baewoss=eul ppunman anila}|
		\oesol{egeseo han=geul eul baewoss=eul ppunman anila}

		\begin{verbatim}
		\begin{oesoltext}
		uri mal uri geul e sarang gwa geu yeon=gu ui chwimi reul gilleosseumyeo
		\end{oesoltext}
		\end{verbatim}

		\begin{oesoltext}
		uri mal uri geul e sarang gwa geu yeon=gu ui chwimi reul gilleosseumyeo
		\end{oesoltext}

		\verb|\oesolscript{과학스럽게 만들어 진 글.}| 
		\oesolscript{과학스럽게 만들어 진 글.}

		\newcommand\hanoe[1]{#1\\\oesolscript{#1}}

		\hanoe{가 냐 더 려 모 뵤 수 유 즈 치}

		\hanoe{캐 턔 페 혜}

		\hanoe{괴 놰 뒤 뒈}

		\hanoe{각 난 닫 랄 맘 밥 삿 앙 잦 찿 캌 탙 팦 핳} 
		\end{document}

[circled]
 description: Use this template to draw circled numbers or letters.
 output: circled
 compiler: -c
 tex:	`\documentclass[a4paper]{article}
		`\usepackage{xparse}
		`\usepackage{tikz}
		`\ExplSyntaxOn
		`\NewDocumentCommand\cirnum{ m }
		`{
		`	\raisebox{-.5ex}{
		`		\tikz\node[
		`			circle, draw=white, thin, inner~sep=0.25pt,
		`			top~color=black, bottom~color=black,
		`			text~width=1em,
		`			font=\sffamily\footnotesize\bfseries, text~badly~centered, white
		`			]{#1};}
		`}
		`\NewDocumentCommand \cirnumuntil { m }
		`{
		`	\int_step_inline:nn { #1 }{ \cirnum{ ##1 }\space }
		`}
		`\ExplSyntaxOff
		`\begin{document}
		`\cirnumuntil{25}
		`\end{document}

[pstricks]
description: This a simple example of pstricks.
output: mypstricks
cmd:	REM Use this script or xelatex.
		latex.exe \TEX
		dvips.exe \DVI
		ps2pdf.exe \PS
tex: 	`\documentclass[a4paper]{article}
		`\usepackage{pstricks}
		`\newcount\n              
		`\newcount\x\newcount\y   
		`\newcount\xo\newcount\yo 
		`\newcount\dx\newcount\dy 
		`\newcount\t              
		`\def\swp{\t=\dx\dx=\dy\dy=\t}
		`\def\L{\swp\multiply\dx by-1}
		`\def\R{\swp\multiply\dy by-1}
		`\def\S{%%
		`	\xo=\x \yo=\y %%
		`	\advance\x by\dx%%
		`	\advance\y by\dy%%
		`	\ln{\the\xo}{\the\yo}{\the\x}{\the\y}%%
		`}
		`\def\ln#1#2#3#4{\qline(#1,#2)(#3,#4)}
		`\def\h#1#2{\ifnum\n=0\relax\else%%
		`	\advance\n by-1%%
		`	#1\h#2#1\S#2\h#1#2\S\h#1#2#2\S\h#2#1#1%%
		`	\advance\n by1\fi%%
		`}
		`\begin{document}
		`\psset{unit=2mm}
		`\centerline{\textbf{\LARGE Hilbert Curve}}
		`\bigskip
		`\makebox[\textwidth]{%%
		`	\begin{pspicture}(0,0)(63,63)
		`		\x=0 \y=0
		`		\dx=1 \dy=0
		`		\n=6 \h\L\R
		`	\end{pspicture}%%
		`}
		`\end{document}

[counter]
description: This template shows all available counter representations supported by KoTeX and dingbats.
output: counters
compiler: -c
tex: 	`\documentclass[twocolumn]{article}
		`
		`\usepackage{kotex}
		`\usepackage{enumitem}
		`\usepackage{pifont}
		`\usepackage{xcolor}
		`
		`\ExplSyntaxOn
		`\NewDocumentCommand \dingbat { m }
		`{
		`	\int_set:Nn \l_tmpa_int { #1 + 32 }
		`	\ding{\l_tmpa_int}    
		`}
		`\def\Ding#1{\expandafter\dingbat\csname c@#1\endcsname}
		`\ExplSyntaxOff
		`
		`\AddEnumerateCounter{\Ding}{\dingbat}{M}
		`\AddEnumerateCounter{\jaso}{\@jaso}{M}
		`\AddEnumerateCounter{\gana}{\@gana}{M}
		`\AddEnumerateCounter{\ojaso}{\@ojaso}{M}
		`\AddEnumerateCounter{\ogana}{\@ogana}{M}
		`\AddEnumerateCounter{\pjaso}{\@pjaso}{M}
		`\AddEnumerateCounter{\pgana}{\@pgana}{M}
		`\AddEnumerateCounter{\onum}{\@onum}{M}
		`\AddEnumerateCounter{\pnum}{\@pnum}{M}
		`\AddEnumerateCounter{\oeng}{\@oeng}{M}
		`\AddEnumerateCounter{\peng}{\@peng}{M}
		`\AddEnumerateCounter{\hroman}{\@hroman}{ⅻ}
		`\AddEnumerateCounter{\hRoman}{\@hRoman}{Ⅻ}
		`\AddEnumerateCounter{\hnum}{\@hnum}{스물하나}
		`\AddEnumerateCounter{\Hnum}{\@Hnum}{스물넷째}
		`\AddEnumerateCounter{\hNum}{\@hNum}{이십사}
		`\AddEnumerateCounter{\hanjanum}{\@hanjanum}{二十四}
		`
		`\ExplSyntaxOn
		`\NewDocumentCommand \HangulCounter { m O{14} }
		`{
		`	\begin{enumerate}[font=\color{blue}\bfseries,label=#1]
		`	\int_step_inline:nn {#2}{\item 천상에서~다시~만나면~그대를~다시~만나면}
		`	\end{enumerate}    
		`}
		`\ExplSyntaxOff
		`
		`%% \setlist[enumerate,1]{label=\onum*}
		`
		`\begin{document}
		`\HangulCounter{\Ding*}[90]
		`\HangulCounter{\jaso*.}
		`\HangulCounter{\gana*.}
		`\HangulCounter{\ojaso*}
		`\HangulCounter{\ogana*}
		`\HangulCounter{\pjaso*}
		`\HangulCounter{\pgana*}
		`\HangulCounter{\onum*}[15]
		`\HangulCounter{\pnum*}[15]
		`\HangulCounter{\oeng*}[26]
		`\HangulCounter{\peng*}[26]
		`\HangulCounter{\hroman*.}[12]
		`\HangulCounter{\hRoman*.}[12]
		`\HangulCounter{\hnum*.}[24]
		`\HangulCounter{\Hnum*.}[24]
		`\HangulCounter{\hNum*.}[24]
		`\HangulCounter{\hanjanum*.}[24]
		`\end{document}

[babel]
description: This template shows the basic usage of babel and polyglossia packages.
output: mybabel
compiler: -w
tex: 	\documentclass[a5paper]{memoir}

		\usepackage[main=russian, english]{babel}
		\babelfont[english]{rm}{Noto Serif Light}
		\babelfont[russian]{rm}{CMU Serif}
		\babelfont[english]{sf}{Noto Sans Light}
		\babelfont[russian]{sf}{CMU Sans Serif}

		%% \usepackage{polyglossia}
		%% \setdefaultlanguage{russian}
		%% \setotherlanguage{english}
		%% \newfontfamily\englishfont{Noto Serif Light}
		%% \newfontfamily\englishfontsf{Noto Sans Light}
		%% \newfontfamily\cyrillicfont{CMU Serif}
		%% \newfontfamily\cyrillicfontsf{CMU Sans Serif}

		\newcommand*\oxygen{O\textsubscript{2}}

		\begin{document}

		\tableofcontents

		\selectlanguage{english}

		\chapter{Introduction}

		XXX is a portable gas detector, featuring the following:

		Activate the detector before the activation date on the package.

		This product is a gas detector, not a measurement device.

		Ensure that the sensor grill is free of dirt, debris, and is not obstructed.

		Clean the exterior with a soft, damp cloth.

		For optimal performance, periodically zero the sensor in a normal atmosphere (20.9\%% v/v \oxygen) that is free of hazardous gas.

		\sffamily

		Portable safety gas detectors are life safety devices. Accuracy of ambient gas reading(s) is dependent upon factors such as accuracy of the calibration gas standard used for calibration and frequency of calibration.
		Honeywell Analytics recommends performing a calibration at least once every 180 days (6 months).

		The combustible gas sensor is initially calibrated to 50\%% LEL methane. Only methane gas should be used to calibrate or bump test the combustible gas sensor.

		Only the combustible gas detection portion of this instrument has been assessed for performance.

		High off-scale readings may indicate an explosive concentration.

		Any rapid up scaling reading followed by a declining or erratic reading may indicate a gas concentration beyond the upper scale limit, which can be hazardous.

		Products may contain materials that are regulated for transportation under domestic and international dangerous goods regulations. Return product in compliance with appropriate dangerous goods regulations. Contact freight carrier for further instructions.

		Recycling: this instrument contains a lithium battery.
		Do not mix with the solid waste stream.
		Spent batteries should be disposed of by a qualified recycler or hazardous materials handler.

		\selectlanguage{russian}

		\rmfamily

		\chapter{Введение}

		XXX – это переносной газоанализатор со следующими характеристиками:

		Газоанализатор необходимо активировать до истечения срока активации, указанного на упаковке.

		Не допускайте загрязнения и блокирования отверстий решетки сенсора.

		Для очистки корпуса пользуйтесь мягкой, влажной салфеткой.

		Для оптимальной работы газоанализатора следует периодически обнулять сенсор в нормальной атмосфере (с объемной долей 20,9\%% \oxygen), не содержащей опасных газов.

		\sffamily

		Переносные газоанализаторы обеспечивают безопасность жизнедеятельности. Точность показаний окружающего газа зависит от таких факторов, как точность калибровочного газа, который используется для калибровки, а также от частоты проведения калибровок.  
		Honeywell Analytics рекомендует выполнять калибровку не реже, чем каждые 180 дней (6 месяцев).

		сенсор горючего газа изначально откалиброван на НКПР 50\%% по метану. Следует использовать только метан для калибровки датчики и ударного теста на горючий газ.

		Оценивалась только работа той части прибора, которая улавливает горючие газы.

		Зашкаливающие показания могут свидетельствовать о взрывоопасной концентрации газа.

		Любое резкое увеличение показаний, за которым идет спад или неустойчивость значений, может свидетельствовать о том, что концентрация газа превышает верхний предел, а это может быть опасно.

		Оборудование может содержать материалы, подпадающие под действие национальных и международных правил перевозки опасных грузов.  В случае возврата оборудования необходимо обеспечить соблюдение правил перевозки опасных грузов. Для получения дополнительных указаний обратитесь в транспортную компанию.

		Утилизация: в данном приборе есть литиевая батарея. 
		Не бросайте газоанализатор в поток твердых отходов. 
		Отработавшие батареи следует сдавать в специализированный пункт переработки опасных материалов. 

		\end{document}

[combination]
description: This template contains a lua code to calculate combinations.
	example: mytex.py combinations -s 45 6
output: comb
compiler: -l
placeholders: 2
defaults: 45, 6 
tex: 	`\documentclass[a5paper]{article}
		`\newcommand\comb[2]{
		`	${#1\choose #2} =  \directlua{
		`		local res, n, r = 1, #1, #2
		`		for j=1, r do
		`		res = res * (n - r + j) / j
		`		end
		`		tex.print(math.floor(res))
		`	}$
		`}
		`\begin{document}
		`\comb{\1}{\2}
		`\end{document} 

[abreast]
description: This template immitates the wrapfig package.
output: abreast
compiler: -c
tex: 	`\documentclass[a4paper]{article}
		`\usepackage{graphicx}
		`\usepackage{xparse}
		`
		`\ExplSyntaxOn
		`\box_new:N \l_image_box
		`\box_new:N \l_text_box
		`\dim_new:N \l_image_box_wd
		`\dim_new:N \l_image_box_ht
		`\dim_new:N \l_text_box_wd
		`\dim_new:N \l_text_box_ht
		`\dim_new:N \l_box_sep
		`\dim_set:Nn \l_box_sep { 1em }
		`\bool_new:N \l_bigger_bool
		`
		`\NewDocumentCommand \abreast { m +m }
		`{    
		`    \group_begin:
		`    \hyphenchar\font=-1
		`    \sloppy
		`
		`    %% 이미지 크기를 재고
		`    \hbox_set:Nn \l_image_box { \includegraphics[scale=1]{#1} }
		`    \dim_set:Nn \l_image_box_wd { \box_wd:N \l_image_box }
		`    \dim_set:Nn \l_image_box_ht { \box_ht:N \l_image_box + \box_dp:N \l_image_box }
		`
		`    %% 텍스트를 위한 폭을 지정하여, 박스에 넣고 높이를 잰다.
		`    \dim_set:Nn \l_text_box_wd { \linewidth - \l_image_box_wd - \l_box_sep }
		`    \vbox_set:Nn \l_tmpa_box { \hsize=\l_text_box_wd #2 }
		`    \dim_set:Nn \l_text_box_ht { \box_ht:N \l_tmpa_box + \box_dp:N \l_tmpa_box }
		`
		`    %% 텍스트 박스가 이미지보다 크면 이미지와 같은 높이로 자른다.
		`    \dim_compare:nTF { \l_text_box_ht > \l_image_box_ht } 
		`    {        
		`        \vbox_set_split_to_ht:NNn \l_text_box \l_tmpa_box { \l_image_box_ht }
		`    }{
		`        \vbox_set_to_ht:Nnn \l_text_box { \l_image_box_ht } { \vbox_unpack:N \l_tmpa_box }        
		`    }      
		`    \mbox{} \box_use_drop:N \l_image_box \hfill \box_use_drop:N \l_text_box
		`
		`    %% 텍스트 박스가 이미보다 크면 자르고 남은 텍스트를 식자한다.
		`    \dim_compare:nT { \l_text_box_ht > \l_image_box_ht } 
		`    {
		`        \newline
		`        \exp_args:No \abreast_tail:n { #2 }
		`    }
		`    \group_end:
		`}
		`
		`%% 공백을 기준으로 텍스트를 나누어 시퀀스에 넣는다.
		`\cs_new:Npn \abreast_tail:n #1
		`{    
		`    \str_clear:N \l_tmpa_tl
		`    \str_clear:N \l_tmpb_tl
		`    \bool_set_false:N \l_bigger_bool
		`    \seq_set_split:Nnn \l_tmpa_seq { ~ }{ #1 }
		`    %% 나머지 텍스트를 구한다.
		`    \seq_map_function:NN \l_tmpa_seq \abreast_determine_tail:n
		`    \tl_use:N \l_tmpb_tl
		`
		`}
		`
		`\cs_new:Npn \abreast_determine_tail:n #1
		`{
		`    %% 텍스트 박스가 이미지보다 커지면 남은 텍스트를 따로 모은다.
		`    \bool_if:NTF \l_bigger_bool
		`    {
		`        \tl_put_right:Nn \l_tmpb_tl { #1~ }
		`    }{
		`        %% 이미지와 같은 높이가 될 때까지 한 단어씩 박스에 집어넣고 높이를 잰다.
		`        \tl_put_right:Nn \l_tmpa_tl { #1~ }            
		`        \vbox_set:Nn \l_tmpa_box { \hsize=\l_text_box_wd  \tl_use:N \l_tmpa_tl }
		`        \dim_set:Nn \l_text_box_ht { \box_ht:N \l_tmpa_box + \box_dp:N \l_tmpa_box }
		`        \dim_compare:nT { \l_text_box_ht > \l_image_box_ht }
		`        {
		`            \bool_gset_true:N \l_bigger_bool
		`        }
		`    }
		`}
		`\ExplSyntaxOff
		`
		`\def\ltext{Vertical boxes inherit their baseline from their contents. The standard case is that the baseline of the box is at the same position as that of the last item added to the box.}
		`\def\rtext{The functions above for using box contents work in exactly the same way as for any other expl3 variable. However, for efficiency reasons, it is also useful to have functions which drop box contents on use. \par When a box is dropped, the box becomes empty at the group level where the box was originally set rather than necessarily at the current group level. Vertical boxes inherit their baseline from their contents. The standard case is that the baseline of the box is at the same position as that of the last item added to the box.}
		`\setlength\parindent{0pt}
		`
		`\begin{document}
		`
		`\abreast{uncertain}{\ltext}\\
		`\abreast{uncertain}{\rtext}
		`
		`\end{document}

[jamoemph]
description: This template highlights hangul vowels in different colors. It requires lualatex and the colorjamo package.
output: jamoemph
compiler: -l
tex: 	`\documentclass[a4paper]{article}
		`
		`\usepackage{kotex}
		`\usepackage{colorjamo}
		`\usepackage{environ}
		`
		`\setmainhangulfont{Noto Serif CJK KR}[
		`    Script=Hangul,
		`    Language=Korean,
		`    BoldFont={* SemiBold}
		`]
		`\setsanshangulfont{Noto Sans CJK KR}[
		`    Script=Hangul,
		`    Language=Korean,
		`    BoldFont={* Medium}
		`]
		`\jamotransparency{FF}
		`
		`\ExplSyntaxOn
		`
		`\clist_new:N \l_color_jung_clist
		`
		`\keys_define:nn { JamoEmph }
		`{
		`	font	.tl_set:N = \l_jamoemph_font_tl,
		`	cho		.tl_set:N = \l_color_cho_tl,
		`	jung	.tl_set:N = \l_color_jung_tl,
		`	jong	.tl_set:N = \l_color_jong_tl,
		`    distinct    .bool_set:N = \l_jamoemph_distinct_bool,
		`    a       .tl_set:N = \l_jung_a_tl,
		`    ae      .tl_set:N = \l_jung_ae_tl,
		`    ya      .tl_set:N = \l_jung_ya_tl,
		`    yae     .tl_set:N = \l_jung_yae_tl,
		`    eo      .tl_set:N = \l_jung_eo_tl,
		`    e       .tl_set:N = \l_jung_e_tl,
		`    yeo     .tl_set:N = \l_jung_yeo_tl,
		`    ye      .tl_set:N = \l_jung_ye_tl,
		`    o       .tl_set:N = \l_jung_o_tl,
		`    wa      .tl_set:N = \l_jung_wa_tl,
		`    wae     .tl_set:N = \l_jung_wae_tl,
		`    oe      .tl_set:N = \l_jung_oe_tl,
		`    yo      .tl_set:N = \l_jung_yo_tl,
		`    u       .tl_set:N = \l_jung_u_tl,
		`    wo      .tl_set:N = \l_jung_wo_tl,
		`    we      .tl_set:N = \l_jung_we_tl,
		`    wi      .tl_set:N = \l_jung_wi_tl,
		`    yu      .tl_set:N = \l_jung_yu_tl,
		`    eu      .tl_set:N = \l_jung_eu_tl,
		`    ui      .tl_set:N = \l_jung_ui_tl,
		`    i       .tl_set:N = \l_jung_i_tl
		`}
		`
		`\NewDocumentCommand \JamoEmphSetup { m }
		`{
		`	\keys_set:nn { JamoEmph }{ #1 }
		`    \exp_args:NV \jamocolorcho \l_color_cho_tl
		`    \exp_args:NV \jamocolorjung \l_color_jung_tl
		`    \exp_args:NV \jamocolorjong \l_color_jong_tl
		`    \clist_set:No \l_color_jung_clist {
		`        \l_jung_a_tl,
		`        \l_jung_ae_tl,
		`        \l_jung_ya_tl,
		`        \l_jung_yae_tl,
		`        \l_jung_eo_tl,
		`        \l_jung_e_tl,
		`        \l_jung_yeo_tl,
		`        \l_jung_ye_tl,
		`        \l_jung_o_tl,
		`        \l_jung_wa_tl,
		`        \l_jung_wae_tl,
		`        \l_jung_oe_tl,
		`        \l_jung_yo_tl,
		`        \l_jung_u_tl,
		`        \l_jung_wo_tl,
		`        \l_jung_we_tl,
		`        \l_jung_wi_tl,
		`        \l_jung_yu_tl,
		`        \l_jung_eu_tl,
		`        \l_jung_ui_tl,
		`        \l_jung_i_tl
		`    }
		`}
		`
		`\JamoEmphSetup{
		`    font = {},    
		`    cho = 000000,
		`    jung= FF0000,
		`    jong= 000000,
		`    distinct = true,
		`    a   = 7FFFD4,
		`    ae  = FFE4C4,
		`    ya  = 8A2BE2,
		`    yae = DEB887,
		`    eo  = D2691E,
		`    e   = A52A2A,
		`    yeo = A9A9A9,
		`    ye  = BDB76B,
		`    o   = FF8C00,
		`    wa  = 8B008B,
		`    wae = 556B2F,
		`    oe  = 9932CC,
		`    yo  = 483D8B,
		`    u   = 2F4F4F,
		`    wo  = 9400D3,
		`    we  = B22222,
		`    wi  = 228B22,
		`    yu  = FFD700,
		`    eu  = DAA520,
		`    ui  = 4B0082,
		`    i   = F0E68C
		`}
		`
		`\NewDocumentCommand \jamoemph { o +m }
		`{
		`	\IfValueT { #1 }
		`	{
		`		\JamoEmphSetup{#1}
		`	}
		`    \bool_if:NTF \l_jamoemph_distinct_bool
		`    {
		`	    \seq_set_split:Nnn \l_tmpa_seq { \par }{ #2 }
		`	    \seq_map_function:NN \l_tmpa_seq \jamoemph_split_lines:n
		`    }{
		`        \begin{colorjamo}
		`            #2
		`        \end{colorjamo}
		`    }
		`}
		`
		`\int_new:N \l_seq_count_int
		`
		`\cs_new:Npn \jamoemph_split_lines:n #1
		`{
		`	\seq_set_split:Nnn \l_tmpb_seq { \\ }{ #1 }
		`	\int_set:Nn \l_seq_count_int { \seq_count:N \l_tmpb_seq }
		`
		`	\seq_map_inline:Nn \l_tmpb_seq
		`	{
		`		\seq_set_split:Nnn \l_tmpc_seq { ~ }{ ##1 }
		`		\seq_map_function:NN \l_tmpc_seq \jamoemph_split_words:n
		`
		`		\int_decr:N \l_seq_count_int
		`		\int_compare:nT { \l_seq_count_int > 0 } { \newline }
		`	}\par
		`}
		`
		`\cs_new:Npn \jamoemph_split_words:n #1
		`{
		`	\tl_set:Nn \l_tmpa_tl { #1 }
		`	\tl_map_inline:Nn \l_tmpa_tl
		`	{
		`        \jamoemph_identify_character:n ##1
		`        \begin{colorjamo} \l_jamoemph_font_tl
		`            ##1
		`        \end{colorjamo}
		`	}\space
		`}
		`
		`\int_new:N \l_code_int
		`\int_const:Nn \c_start_point { 44032 }   %% 가'
		`\int_new:N \l_basecode_int
		`\int_new:N \l_cho_int
		`\int_new:N \l_jung_int
		`\int_new:N \l_jong_int
		`
		`%% basecode = 문자코드 - 44032
		`%% 초성코드 = basecode / 588
		`%% 중성코드 = (basecode - 588*초성코드) / 28
		`%% 종성코드 = (basecode - 588*초성코드 - 28*중성코드)
		`
		`\cs_new:Npn \get_lvt_code:n #1
		`{
		`	\int_set:Nn \l_cho_int { \int_div_truncate:nn { #1 } { 588 } }
		`	\int_set:Nn \l_jung_int { \int_div_truncate:nn { #1 - 588 * \l_cho_int } { 28 } }
		`	\int_set:Nn \l_jong_int { #1 - \l_cho_int * 588 - \l_jung_int * 28 }
		`}
		`
		`\cs_new:Npn \jamoemph_identify_character:n #1
		`{
		`	\int_zero:N \l_basecode_int
		`	\int_zero:N \l_cho_int
		`	\int_zero:N \l_jung_int
		`	\int_zero:N \l_jong_int
		`
		`	\str_set_convert:Nnnn \l_code_tl { #1 } { } { clist }
		`	\exp_args:NNx \int_set:Nn \l_code_int { \l_code_tl }
		`
		`	\bool_if:nT
		`	{
		`		\int_compare_p:n { \l_code_int >= \c_start_point }
		`	  &&
		`		\int_compare_p:n { \l_code_int <= 55199 }
		`	}
		`	{
		`		\int_set:Nn \l_basecode_int { \l_code_int - \c_start_point }
		`		\exp_args:Nx \get_lvt_code:n { \int_use:N \l_basecode_int }
		`        \tl_set:Nx \l_tmpb_tl
		`        {
		`            \clist_item:Nn \l_color_jung_clist { \l_jung_int + 1 }
		`        }
		`        \exp_args:NV \jamocolorjung \l_tmpb_tl
		`	}
		`}
		`
		`\NewEnviron{JamoEmph}[1][]
		`{
		`	\JamoEmphSetup{#1}
		`	\exp_args:NV \jamoemph \BODY
		`}
		`
		`\ExplSyntaxOff
		`
		`\begin{document}
		`
		`\begin{JamoEmph}
		`우리 역사에서 자유를 위한 가장 훌륭한 시위가 있던 날로 기록될 오늘 이 자리에 여러분과 함께하게 된 것을 기쁘게 생각합니다.
		`
		`백 년 전, 위대한 어느 미국인이 노예해방령에 서명을 했습니다. 지금 우리가 서 있는 이곳이 바로 그 자리입니다. 그 중대한 선언은 불의의 불길에 시들어가고 있던 수백만 흑인 노예들에게 희망의 횃불로 다가왔습니다. 그것은 그 긴 속박의 밤을 끝낼 흥겨운 새벽으로 왔습니다.
		`
		`우리나라 역사상 자유를 위한 가장 위대한 시위가 있었던 날로서 역사에 기록될 오늘 나는 여러분과 함께 하게 되어 행복합니다.
		`\end{JamoEmph}
		`
		`\begin{JamoEmph}[distinct=false]
		`우리 역사에서 자유를 위한 가장 훌륭한 시위가 있던 날로 기록될 오늘 이 자리에 여러분과 함께하게 된 것을 기쁘게 생각합니다.
		`
		`백 년 전, 위대한 어느 미국인이 노예해방령에 서명을 했습니다. 지금 우리가 서 있는 이곳이 바로 그 자리입니다. 그 중대한 선언은 불의의 불길에 시들어가고 있던 수백만 흑인 노예들에게 희망의 횃불로 다가왔습니다. 그것은 그 긴 속박의 밤을 끝낼 흥겨운 새벽으로 왔습니다.
		`
		`우리나라 역사상 자유를 위한 가장 위대한 시위가 있었던 날로서 역사에 기록될 오늘 나는 여러분과 함께 하게 되어 행복합니다.
		`\end{JamoEmph}
		`
		`\end{document}

[zigzag]
description: This template makes zigzag-shaped paragraphs.
output: zigzag
compiler: -w, -c
sty:	`\RequirePackage{tikzpagenodes}
		`\RequirePackage{xparse}
		`
		`\ExplSyntaxOn
		`\int_new:N \l_shape_lines_int
		`\bool_new:N \l_shape_forth_bool
		`\dim_new:N \l_shape_indent_dim
		`\dim_new:N \l_shape_position_dim
		`\tl_new:N \l_shape_position_tl
		`\dim_new:N \l_shape_length_dim
		`\dim_new:N \l_shape_increment_dim
		`\tl_new:N \l_shape_length_tl
		`\tl_new:N \l_shape_tl
		`
		`%% \zigzagpar[number of lines]<indentation length>(text length){text}
		`\NewDocumentCommand \zigzagpar { o D<>{2em} D(){.5\linewidth} +m }
		`{
		`    \IfValueTF { #1 }
		`    {
		`        \int_set:Nn \l_shape_lines_int { #1 }
		`    }{
		`        \vbox_set:Nn \l_tmpa_box { \hsize=\linewidth #4 }
		`        \dim_set:Nn \l_tmpa_dim { \box_ht:N \l_tmpa_box + \box_dp:N \l_tmpa_box }
		`        \int_set:Nn \l_tmpa_int
		`        {
		`            \fp_eval:n { round (\dim_ratio:nn {\l_tmpa_dim}{\baselineskip}) }
		`        }
		`        \int_set:Nn \l_shape_lines_int { \l_tmpa_int * 2 }
		`    }
		`
		`    \dim_set:Nn \l_shape_indent_dim { #2 }    
		`    \dim_set:Nn \l_shape_position_dim { #2 * -1 }
		`    \dim_set:Nn \l_shape_length_dim { #3 }
		`    \tl_set:Nn \l_shape_length_tl { #3 }
		`    \bool_set_true:N \l_shape_forth_bool
		`
		`    \tl_set:No \l_shape_tl { \int_use:N \l_shape_lines_int }
		`    \tl_put_right:Nn \l_shape_tl { ~ }
		`    \int_step_function:nN { \l_shape_lines_int } \zigzagpar_shift:n 
		`    \exp_last_unbraced:Nx \parshape \l_shape_tl #4
		`}
		`
		`\cs_new:Nn \zigzagpar_shift:n 
		`{
		`    \bool_if:NTF \l_shape_forth_bool
		`    {
		`        \dim_add:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_set:Nn \l_tmpa_dim { \l_shape_position_dim + \l_shape_length_dim }
		`        \dim_compare:nT { \l_tmpa_dim > \linewidth }
		`        {
		`            \dim_sub:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }
		`    }{
		`        \dim_sub:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_compare:nT { \l_shape_position_dim < 0pt }
		`        {
		`            \dim_add:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }
		`    }    
		`    \tl_set:Nx \l_shape_position_tl { \dim_to_decimal:n { \l_shape_position_dim } }
		`    \tl_put_right:Nx \l_shape_tl 
		`    { 
		`        \l_shape_position_tl pt ~ \l_shape_length_tl ~ 
		`    }
		`}
		`
		`%% \diamondpar*[number of lines]<indentation length>{text}
		`\NewDocumentCommand \diamondpar { s o D<>{1em} +m }
		`{   
		`    \IfValueTF { #2 }
		`    {
		`        \int_set:Nn \l_shape_lines_int { #2 }
		`    }{
		`        \vbox_set:Nn \l_tmpa_box { \hsize=\linewidth #4 }
		`        \dim_set:Nn \l_tmpa_dim { \box_ht:N \l_tmpa_box + \box_dp:N \l_tmpa_box }
		`        \int_set:Nn \l_tmpa_int
		`        {
		`            \fp_eval:n { round (\dim_ratio:nn {\l_tmpa_dim}{\baselineskip}) }
		`        }
		`        \int_set:Nn \l_shape_lines_int { \l_tmpa_int * 3 }
		`    }
		`
		`    \dim_set:Nn \l_shape_indent_dim { #3 }    
		`    \dim_set:Nn \l_shape_increment_dim { #3 * 2 }
		`    \IfBooleanTF { #1 }
		`    {
		`        \dim_set:Nn \l_shape_position_dim { 0pt }
		`        \dim_set:Nn \l_shape_length_dim { \linewidth }
		`        \bool_set_true:N \l_shape_forth_bool
		`    }{
		`        \dim_set:Nn \l_shape_position_dim { .5\linewidth }
		`        \dim_set:Nn \l_shape_length_dim { 0pt }
		`        \bool_set_false:N \l_shape_forth_bool
		`    }
		`    
		`    \tl_set:No \l_shape_tl { \int_use:N \l_shape_lines_int }
		`    \tl_put_right:Nn \l_shape_tl { ~ }    
		`    \int_step_function:nN { \l_shape_lines_int } \diamondpar_shift:n
		`    \exp_last_unbraced:Nx \parshape \l_shape_tl #4
		`}
		`
		`\cs_new:Nn \diamondpar_shift:n 
		`{
		`    \bool_if:NTF \l_shape_forth_bool
		`    {
		`        \dim_add:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_compare:nTF { \l_shape_position_dim > .5\linewidth }
		`        {
		`            \dim_sub:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \dim_add:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }{
		`            \dim_sub:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        }
		`    }{
		`        \dim_sub:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_compare:nTF { \l_shape_position_dim < 0pt }
		`        {        
		`            \dim_add:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \dim_sub:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }{
		`            \dim_add:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        }
		`    }
		`    \tl_set:Nx \l_shape_position_tl { \dim_to_decimal:n { \l_shape_position_dim } }
		`    \tl_set:Nx \l_shape_length_tl { \dim_to_decimal:n { \l_shape_length_dim } }
		`    \tl_put_right:Nx \l_shape_tl 
		`    { 
		`       \l_shape_position_tl pt ~ \l_shape_length_tl pt ~ 
		`    }
		`}
		`
		`%% \diamondpar*/[number of lines]<increment>{text}
		`%% the right angle is at 
		`%% \diamondpar*/ : top left
		`%% \diamondpar* : top right
		`%% \diamondpar : bottom left
		`%% \diamondpar/ : bottom right
		`
		`\NewDocumentCommand \rtrianglepar { s t{/} o D<>{1.5em} +m }
		`{   
		`    \IfValueTF { #3 }
		`    {
		`        \int_set:Nn \l_shape_lines_int { #3 }
		`    }{
		`        \vbox_set:Nn \l_tmpa_box { \hsize=\linewidth #5 }
		`        \dim_set:Nn \l_tmpa_dim { \box_ht:N \l_tmpa_box + \box_dp:N \l_tmpa_box }
		`        \int_set:Nn \l_tmpa_int
		`        {
		`            \fp_eval:n { round (\dim_ratio:nn {\l_tmpa_dim}{\baselineskip}) }
		`        }
		`        \int_set:Nn \l_shape_lines_int { \l_tmpa_int * 3 }
		`    }
		`
		`    \dim_set:Nn \l_shape_indent_dim { #4 }
		`    \dim_set:Nn \l_shape_increment_dim { #4 }
		`    \IfBooleanTF { #1 }
		`    {
		`        \dim_set:Nn \l_shape_length_dim { \linewidth + #4 }
		`        \IfBooleanTF { #2 }
		`        {
		`            \tl_set:Nn \l_shape_position_tl { 0pt }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }{
		`            \dim_set:Nn \l_shape_position_dim { #4 * -1 }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }
		`    }{
		`        \dim_set:Nn \l_shape_length_dim { 0pt }
		`        \IfBooleanTF { #2 }
		`        {
		`            \dim_set:Nn \l_shape_position_dim { \linewidth + #4 }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }{
		`            \tl_set:Nn \l_shape_position_tl { 0pt }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }
		`    }
		`    
		`    \tl_set:No \l_shape_tl { \int_use:N \l_shape_lines_int }    
		`    \tl_put_right:Nn \l_shape_tl { ~ }
		`
		`    \IfBooleanTF { #1 }
		`    {
		`        \IfBooleanTF { #2 }
		`        {
		`            \int_step_function:nN { \l_shape_lines_int } \rtrianglepar_bottom_left:n
		`        }{
		`            \int_step_function:nN { \l_shape_lines_int } \rtrianglepar_bottom_right:n
		`        }
		`    }{
		`        \IfBooleanTF { #2 }
		`        {
		`            \int_step_function:nN { \l_shape_lines_int } \rtrianglepar_bottom_right:n
		`        }{
		`            \int_step_function:nN { \l_shape_lines_int } \rtrianglepar_bottom_left:n
		`        }
		`    }
		`    \exp_last_unbraced:Nx \parshape \l_shape_tl #5 
		`}
		`
		`\cs_new:Nn \rtrianglepar_bottom_left:n 
		`{
		`    \bool_if:NTF \l_shape_forth_bool
		`    {
		`        \dim_add:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        \dim_compare:nT { \l_shape_length_dim > \linewidth }
		`        {
		`            \dim_sub:Nn \l_shape_length_dim { 2\l_shape_increment_dim }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }
		`    }{
		`        \dim_sub:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        \dim_compare:nT { \l_shape_length_dim < 0pt }
		`        {        
		`            \dim_add:Nn \l_shape_length_dim { 2\l_shape_increment_dim }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }
		`    }
		`    
		`    \tl_set:Nx \l_shape_length_tl { \dim_to_decimal:n { \l_shape_length_dim } }
		`    \tl_put_right:Nx \l_shape_tl 
		`    { 
		`       \l_shape_position_tl ~ \l_shape_length_tl pt ~ 
		`    }
		`}
		`
		`\cs_new:Nn \rtrianglepar_bottom_right:n 
		`{
		`    \bool_if:NTF \l_shape_forth_bool
		`    {
		`        \dim_add:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_compare:nTF { \l_shape_position_dim > \linewidth }
		`        {
		`            \dim_sub:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \dim_add:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`            \bool_set_false:N \l_shape_forth_bool
		`        }{
		`            \dim_sub:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        }
		`    }{
		`        \dim_sub:Nn \l_shape_position_dim { \l_shape_indent_dim }
		`        \dim_compare:nTF { \l_shape_position_dim < 0pt }
		`        {        
		`            \dim_add:Nn \l_shape_position_dim { 2\l_shape_indent_dim }
		`            \dim_sub:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`            \bool_set_true:N \l_shape_forth_bool
		`        }{
		`            \dim_add:Nn \l_shape_length_dim { \l_shape_increment_dim }
		`        }
		`    }
		`    \tl_set:Nx \l_shape_position_tl { \dim_to_decimal:n { \l_shape_position_dim } }
		`    \tl_set:Nx \l_shape_length_tl { \dim_to_decimal:n { \l_shape_length_dim } }
		`    \tl_put_right:Nx \l_shape_tl 
		`    { 
		`       \l_shape_position_tl pt ~ \l_shape_length_tl pt ~ 
		`    }
		`}
		`
		`\ExplSyntaxOff
		`%% \cornerpar*[text width](font size)<increment>{text}
		`\NewDocumentCommand \cornerpar {  s O{.2\paperwidth} D(){\scriptsize} D<>{1em} m }
		`{
		`    \IfBooleanTF { #1 }
		`    {
		`        \begin{tikzpicture}[every node/.style={inner sep=0pt},remember picture,overlay]        
		`        #3 
		`        \node[shift={(-1.0cm,1.0cm)},anchor=north west] at (current page.north west)
		`            {\rotatebox{45}{\parbox{#2}{\diamondpar<#4>{#5}}}};
		`        \node[shift={(1.0cm,1.0cm)},anchor=north east] at (current page.north east)
		`            {\rotatebox{-45}{\parbox{#2}{\diamondpar<#4>{#5}}}};
		`        \node[shift={(-1.0cm,-1.0cm)},anchor=south west] at (current page.south west)
		`            {\rotatebox{135}{\parbox{#2}{\diamondpar<#4>{#5}}}};
		`        \node[shift={(1.0cm,-1.0cm)},anchor=south east] at (current page.south east)
		`            {\rotatebox{-135}{\parbox{#2}{\diamondpar<#4>{#5}}}};
		`        \end{tikzpicture}
		`    }{
		`        \begin{tikzpicture}[every node/.style={inner sep=0pt},remember picture,overlay]
		`        #3 
		`        \node[shift={(.5cm,-.5cm)},anchor=north west] at (current page.north west)
		`            {\parbox{#2}{\rtrianglepar*/<#4>{#5}}};
		`        \node[shift={(-.5cm,-.5cm)},anchor=north east] at (current page.north east)
		`            {\parbox{#2}{\rtrianglepar*<#4>{#5}}};
		`        \node[shift={(.5cm,.5cm)},anchor=south west] at (current page.south west)
		`            {\parbox{#2}{\rtrianglepar<#4>{#5}}};
		`        \node[shift={(-.5cm,.5cm)},anchor=south east] at (current page.south east)
		`            {\parbox{#2}{\rtrianglepar/<#4>{#5}}};
		`        \end{tikzpicture}
		`    }
		`}
		` 
tex:	\documentclass{article}
		\usepackage[a4paper]{geometry}
		\usepackage{kotex}
		\usepackage{zigzag}

		\def\shorttext{김약국의 딸들. 통영은 다도해 부근에 있는 조촐한 어항이다.
		부산과 여수 사이를 내왕하는 항로의 중간 지점으로서 그 고장의 젊은이들은 조선의 나폴리라고 한다.}
		\def\longtext{그러니만큼 바닷빛은 맑고 푸르다.
		북쪽에 두루미 목만큼 좁은 육로를 빼면 통영 역시 섬과 별다름이 없이 사면이 바다이다. 벼랑가에 얼마쯤 포전(浦田)이 있고, 언덕배기에 대부분의 집들이 송이버섯처럼 들앉은 지세는 빈약하다.}
		\def\verylongtext{\shorttext\longtext\shorttext\longtext\shorttext\longtext\shorttext\longtext}

		\setlength\parindent{0pt}
		\pagestyle{empty}

		\begin{document}
		\mbox{}\vfill
		\cornerpar[.16\paperwidth]<1.25em>{\shorttext}
		\diamondpar<2em>{\verylongtext}
		\vfill
		\newpage
		\mbox{}\vfill
		\cornerpar*[.25\paperwidth]<1.1em>{\longtext}
		\zigzagpar{\verylongtext}
		\vfill
		\end{document}	

[pythontex]
description: This template shows an example of pythontex.
output: pytex
compiler: -P, -w
tex:	\documentclass{article}
		\usepackage{kotex}
		\usepackage{xcolor}
		\usepackage{tabto}
		\usepackage{pythontex}

		\newcommand\codetail[1]{\textcolor{blue}{#1}}
		\newcommand\bytehead[1]{\textcolor{red}{#1}}
		\newcommand\bytetail[1]{\textcolor{brown}{#1}}
		\TabPositions{0pt, .15\linewidth, .5\linewidth}

		\begin{document}
		\begin{pyblock}
		import sys
		sys.path.append('c:\\home\\bin')
		from wordutil import UTFanalyzer
		utf = UTFanalyzer( chars="aA가①⑴⒜ⓐⅰⅠㄱ㉠㉮㈀㈎", \
		    upper=True, tex=True)
		utf.show()
		\end{pyblock}
		\small \texttt{\printpythontex}
		\end{document}  

[timeline]
description: This template draws horizontal graphs to show when ones were born and when they died.
output: timeline
compiler: -v
sty:	`\RequirePackage{tikz}
		`\RequirePackage{tikz}
		`\ExplSyntaxOn 
		`\makeatletter
		`\cs_if_exist:NT \tikz@ensure@dollar@catcode
		`{
		`    \cs_set_eq:NN \tikz@ensure@dollar@catcode \scan_stop:
		`}
		`\makeatother
		`
		`\keys_define:nn { kstimeline }
		`{
		`    length    .dim_set:N = \l_xtllength_dim,
		`    start    .int_set:N = \l_xtlstart_int,
		`    stop    .int_set:N = \l_xtlstop_int,
		`    place    .int_set:N = \l_xtlplace_int,
		`    nameboxwidth    .dim_set:N = \l_xtlnamebox_dim,
		`}
		`
		`\keys_set:nn { kstimeline }
		`{
		`    nameboxwidth = 6em,
		`    length = 10cm,
		`    start = 2000,
		`    stop = 2020,
		`    place = 2010
		`}
		`
		`\dim_new:N \l_xtlunit_dim
		`\int_new:N \l_xtlbirth_int
		`\int_new:N \l_xtldeath_int
		`\dim_new:N \l_xtlbirth_dim
		`\dim_new:N \l_xtldeath_dim
		`\dim_new:N \l_xtlplace_dim
		`
		`\NewDocumentCommand \xtlsetup { m }
		`{
		`    \keys_set:nn { kstimeline } { #1 }
		`
		`    \dim_set:Nn \l_xtlunit_dim { \l_xtllength_dim / ( \l_xtlstop_int - \l_xtlstart_int ) }
		`    \dim_set:Nn \l_xtlplace_dim { \l_xtlunit_dim * ( \l_xtlplace_int - \l_xtlstart_int ) }
		`}
		`
		`\bool_new:N \l_bday_bool
		`
		`\NewDocumentCommand \xtldraw { m m }
		`{
		`    \str_if_eq:eeTF { \tl_head:n { #1 } } { * }
		`    {
		`        \bool_set_true:N \l_bday_bool
		`        \tl_set:No \l_tmpb_tl { \tl_tail:n { #1 } }
		`    }
		`    {
		`        \bool_set_false:N \l_bday_bool
		`        \tl_set:Nn \l_tmpb_tl { #1 }
		`    }
		`
		`    \xtl_split_years:w #2 \q_stop
		`
		`    \dim_set:Nn \l_xtlbirth_dim { \l_xtlunit_dim * ( \l_xtlbirth_int - \l_xtlstart_int ) }
		`
		`    \dim_set:Nn \l_xtldeath_dim { \l_xtllength_dim -  \l_xtlunit_dim * ( \l_xtlstop_int - 		`\l_xtldeath_int ) }
		`
		`    \exp_args:No \xtl_draw_tl:n { \l_tmpb_tl }    
		`}
		`
		`
		`\cs_new:Npn \xtl_split_years:w #1-#2\q_stop
		`{
		`    \int_set:Nn \l_xtlbirth_int { #1 }
		`    \int_set:Nn \l_xtldeath_int { #2 }
		`}
		`
		`\cs_new:Npn \xtl_draw_tl:n #1
		`{
		`    \begin{tikzpicture}
		`    \node [anchor=west] at (-\dim_use:N \l_xtlnamebox_dim -3em -.5em,0) { \makebox		`[\l_xtlnamebox_dim ][l]{#1} };
		`    \node [anchor=west] at (-3em-.5em, 0) { \makebox [3em][l]{\int_use:N \l_xtlbirth_int}};
		`    \draw (0,0) -- ( \dim_use:N \l_xtllength_dim,0);
		`    \xtltick{0pt};
		`    \xtltick{\l_xtllength_dim};
		`    \xtltick{\l_xtlbirth_dim};
		`    \xtltick{\l_xtldeath_dim};
		`    \draw [line~width=4pt,gray!120] ( \dim_use:N \l_xtlbirth_dim,0) -- ( \dim_use:N 		`\l_xtldeath_dim,0);
		`    \draw [fill=white,white] ( \dim_use:N \l_xtlplace_dim - 3mm,2mm) rectangle ( \dim_use:N 		`\l_xtlplace_dim + 3mm, -2mm);
		`    \bool_if:NTF \l_bday_bool
		`    {
		`        \int_set:Nn \l_tmpa_int { \l_xtlplace_int - \l_xtlbirth_int -1 }
		`    }
		`    {
		`        \int_set:Nn \l_tmpa_int { \l_xtlplace_int - \l_xtlbirth_int }
		`    }
		`    \node [anchor=center] at ( \dim_use:N \l_xtlplace_dim,0) { \small ( \int_use:N \l_tmpa_int 		`) };
		`    \node [anchor=west] at ( \dim_use:N \l_xtllength_dim + .5em,0) { \int_use:N \l_xtldeath_int 		`};
		`    \end{tikzpicture}
		`    \par
		`}
		`
		`\NewDocumentCommand \xtltick { m }
		`{
		`    \draw (#1,2mm) -- (#1,-2mm)
		`}
		`
		`\ior_new:N \l_file_ior
		`
		`\NewDocumentEnvironment { xtimeline } { }
		`{
		`    \exp_args:Nno \verbatimoutput { \jobname-tllist.txt }
		`}
		`{
		`    \endverbatimoutput
		`
		`    \clist_clear:N \l_tmpa_clist
		`    \ior_open:Nn \l_file_ior { \jobname-tllist.txt }
		`    \ior_str_map_inline:Nn \l_file_ior
		`    {
		`        \clist_put_right:Nx \l_tmpa_clist { ##1 }
		`    }
		`    \ior_close:N \l_file_ior
		`
		`    \clist_sort:Nn \l_tmpa_clist 
		`    {
		`        \tl_set:Nn \l_tmpa_tl { ##1 }
		`        \tl_set:Nn \l_tmpb_tl { ##2 }
		`        \regex_replace_all:nnN { [^0-9] } { } \l_tmpa_tl
		`        \regex_replace_all:nnN { [^0-9] } { } \l_tmpb_tl
		`        \exp_args:Nx \int_compare:nTF { \l_tmpa_tl > \l_tmpb_tl }
		`            { \sort_return_swapped: }
		`            { \sort_return_same: }
		`    }
		`
		`    \clist_map_inline:Nn \l_tmpa_clist
		`    {
		`        \xtl_draw_fn:w ##1 \q_stop 
		`    }
		`}
		`
		`\cs_new:Npn \xtl_draw_fn:w #1 | #2 \q_stop
		`{
		`    \xtldraw { #1 } { #2 } 
		`}
		`\ExplSyntaxOff
tex:	\documentclass[9pt, a4paper, oneside]{memoir}
		\usepackage{kotex}
		\usepackage{timeline}
		\setmainfont{TeX Gyre Termes}
		\setlength\parindent{0pt}
		\begin{document}
		\xtlsetup{nameboxwidth=8em,length=8cm,start=1822,stop=1917,place=1874}
		\begin{boxedverbatim}
		\xtldraw{*사카타니 시로시}{1822-1881}
		\xtldraw{미쓰쿠리 슈헤이}{1826-1886}
		\xtldraw{*니시무라 시게키}{1828-1902}
		\xtldraw{*스기 코지}{1828-1917}
		\end{boxedverbatim}
		\xtldraw{*사카타니 시로시}{1822-1881}
		\xtldraw{미쓰쿠리 슈헤이}{1826-1886}
		\xtldraw{*니시무라 시게키}{1828-1902}
		\xtldraw{*스기 코지}{1828-1917}
		\begin{boxedverbatim}
		\begin{xtimeline}
		*쓰다 마미치 | 1829-1903
		*미쓰쿠리 린쇼 | 1846-1897
		*모리 아리노리 | 1847-1889
		니시 아마네 | 1829-1897
		*시미즈 우사부로 | 1829-1910
		*간다 다카히라 | 1830-1898
		미쓰쿠리 슈헤이 | 1826-1886
		*니시무라 시게키 | 1828-1902
		*나카무라 마사나오 | 1832-1891
		*가시와바라 다카아키 | 1835-1910
		후쿠자와 유키치 | 1835-1901
		*사카타니 시로시 | 1822-1881
		*스기 코지 | 1828-1917
		*가토 히로유키 | 1836-1916
		*쓰다 센 | 1837-1908
		*시바타 쇼키치 | 1842-1901
		\end{xtimeline}
		\end{boxedverbatim}
		\xtlsetup{nameboxwidth=10em,length=8.5cm,start=1822,stop=1917,place=1874}
		\begin{xtimeline}
		*쓰다 마미치 | 1829-1903
		*미쓰쿠리 린쇼 | 1846-1897
		*모리 아리노리 | 1847-1889
		니시 아마네 | 1829-1897
		*시미즈 우사부로 | 1829-1910
		*간다 다카히라 | 1830-1898
		미쓰쿠리 슈헤이 | 1826-1886
		*니시무라 시게키 | 1828-1902
		*나카무라 마사나오 | 1832-1891
		*가시와바라 다카아키 | 1835-1910
		후쿠자와 유키치 | 1835-1901
		*사카타니 시로시 | 1822-1881
		*스기 코지 | 1828-1917
		*가토 히로유키 | 1836-1916
		*쓰다 센 | 1837-1908
		*시바타 쇼키치 | 1842-1901
		\end{xtimeline}
		\end{document}

[tenthousand]
description: This template groups every four digits.
output: tenthousand
compiler: -c
tex:	`\documentclass[a4paper, oneside]{memoir}
		`\usepackage{kotex}
		`\ExplSyntaxOn
		`\bool_new:N \g_num_tenthousand_bool
		`\int_new:N \g_num_decimal_places_int
		`\NewDocumentCommand \SetDecimalPlaces { m }
		`{
		`    \int_gset:Nn \g_num_decimal_places_int { #1 }
		`}
		`\SetDecimalPlaces{2}
		`\NewDocumentCommand \SeparateThousands {}
		`{
		`    \bool_gset_false:N \g_num_tenthousand_bool
		`}
		`\NewDocumentCommand \SeparateTenThousands {}
		`{
		`    \bool_gset_true:N \g_num_tenthousand_bool
		`}
		`\dim_new:N \l_num_decimal_dim
		`\dim_new:N \l_num_zero_dim
		`\NewDocumentCommand \decimalspace {}
		`{
		`    \hspace*{\l_num_decimal_dim}
		`}
		`\NewDocumentCommand \zerospace {}
		`{
		`    \hspace*{\l_num_zero_dim}
		`}
		`\NewDocumentCommand \num { s m }
		`{
		`    \regex_split:nnN { \. }{ #2 } \l_tmpa_seq 
		`    \seq_pop:NN \l_tmpa_seq \l_tmpa_tl
		`    \tl_reverse:N \l_tmpa_tl
		`    \bool_if:NTF \g_num_tenthousand_bool
		`    {
		`        \regex_replace_all:nnN { (\d\d\d\d) } { \1, } \l_tmpa_tl
		`    }{
		`        \regex_replace_all:nnN { (\d\d\d) } { \1, } \l_tmpa_tl
		`    }
		`    \regex_replace_once:nnN { ,$ } {  } \l_tmpa_tl
		`    \tl_reverse:N \l_tmpa_tl
		`
		`    \IfBooleanTF{ #1 }
		`    {
		`        \seq_pop:NNTF \l_tmpa_seq \l_tmpb_tl
		`        {
		`            \int_set:Nn \l_tmpb_int { \tl_count:V \l_tmpb_tl }
		`            \int_step_inline:nn { \int_eval:n { \g_num_decimal_places_int - \l_tmpb_int } }
		`            {
		`                \tl_put_right:Nn \l_tmpb_tl { \zerospace  }
		`            }
		`            \seq_push:NV \l_tmpa_seq \l_tmpb_tl            
		`            \seq_push:NV \l_tmpa_seq \l_tmpa_tl
		`        }{
		`            \tl_put_right:Nn \l_tmpa_tl { \decimalspace }
		`            \int_step_inline:nn { \g_num_decimal_places_int }  
		`            {
		`                \tl_put_right:Nn \l_tmpa_tl { \zerospace  }
		`            }
		`            \seq_push:NV \l_tmpa_seq \l_tmpa_tl
		`        }
		`    }{
		`        \seq_push:NV \l_tmpa_seq \l_tmpa_tl
		`    }    
		`    \seq_use:Nnnn \l_tmpa_seq {.}{}{}    
		`}
		`\NewDocumentEnvironment{numbers}{}
		`{
		`    \exp_args:Nno \verbatimoutput { \jobname.tmp }
		`}{
		`    \endverbatimoutput
		`
		`    \clist_clear:N \l_tmpa_clist
		`    \ior_open:Nn \g_tmpa_ior { \jobname.tmp }
		`    \ior_str_map_inline:Nn \g_tmpa_ior
		`    {
		`        \clist_put_right:Nx \l_tmpa_clist { ##1 }
		`    }
		`    \ior_close:N \g_tmpa_ior
		`
		`    \hbox_set:Nn \l_tmpa_box { . }
		`    \dim_set:Nn \l_num_decimal_dim  { \box_wd:N \l_tmpa_box }
		`    \hbox_set:Nn \l_tmpa_box { 0 }
		`    \dim_set:Nn \l_num_zero_dim  { \box_wd:N \l_tmpa_box }
		`
		`    \raggedleft
		`    \clist_map_inline:Nn \l_tmpa_clist
		`    {
		`        \num*{##1} \\        
		`    }    
		`}
		`\ExplSyntaxOff
		`\setlength\parindent{0pt}
		`\begin{document}
		`
		`\begin{boxedverbatim}
		`\SeparateThousands
		`\num{123456.7890} 
		`\end{boxedverbatim}
		`
		`\SeparateThousands
		`\num{123456.7890} 
		`
		`\begin{boxedverbatim}
		`\SeparateTenThousands
		`\num{123456.7890} 
		`\end{boxedverbatim}
		`
		`\SeparateTenThousands
		`\num{123456.7890} 
		`
		`\bigskip
		`
		`\begin{boxedverbatim}
		`\SetDecimalPlaces{4}
		`\begin{minipage}{.25\linewidth}
		`\begin{numbers}
		`2345.89
		`123
		`2345.9
		`97698.573
		`8976231
		`768923121
		`\end{numbers}
		`\end{minipage}
		`\end{boxedverbatim}
		`
		`\SetDecimalPlaces{4}
		`\begin{minipage}{.25\linewidth}
		`\begin{numbers}
		`2345.89
		`123
		`2345.9
		`97698.573
		`8976231
		`768923121
		`\end{numbers}
		`\end{minipage}
		`
		`\end{document}

[graphviz]
description: This template shows an example for graphviz.
output: graphviz
cmd:	dot -T pdf graphviz.gv -o latex_process.pdf
		ltx.py graphviz -v
gv:		`digraph G {
		`	 margin=0;
		`    rankdir=TB;
		`    node [fontname=D2Coding, fontsize=10, penwidth=0.25];
		`    edge [arrowhead=vee, arrowsize=0.5, fontname=Arial, fontsize=9];
		`
		`    node [shape=ellipse, style=filled, fillcolor=lightgrey];
		`        { rank=same; 
		`            tex[label="foo.tex", fillcolor=lightsalmon]; 
		`            pdf[label="foo.pdf", fillcolor=navy, fontcolor=white]; }
		`        latex [shape=box, style=filled, fillcolor=lightblue];
		`        { rank=same; 
		`            aux[label="foo.aux"]; 
		`            toc[label="foo.toc"]; 
		`            idx[label="foo.idx"]; 
		`            log[label="foo.log"]; }
		`        { rank=same;             
		`            makeindex[shape=box, style=filled, fillcolor=lightblue];
		`            bib[label="ref.bib", fillcolor=lightsalmon];
		`            bibtex[shape=box, style=filled, fillcolor=lightblue]; }
		`        { rank=same; 
		`            ist[label="goo.ist", fillcolor=khaki3]; 
		`            ind [label="foo.ind"]; 
		`            bst[label="hoo.bst", fillcolor=khaki3]; 
		`            bbl[label="foo.bbl"];  }
		`
		`    tex -> latex -> {pdf; log}
		`    latex -> {aux; toc} [dir=both, arrowtail=vee];
		`    latex -> idx -> makeindex -> ind -> latex;
		`    ist -> makeindex;
		`    aux -> bibtex -> bbl -> latex;
		`    { bst; bib } -> bibtex;
		`} 
tex:	\documentclass[a4paper]{article}
		\usepackage{graphicx}
		\begin{document}
		\noindent\includegraphics[width=\textwidth]{latex_process}
		\begin{verbatim}
		latex = pdflatex / xelatex / lualatex
		.toc = .lof / .lot
		makeindex = komkindex / texindy
		.ist = .xdy
		bibtex = biber
		\end{verbatim}
		\end{document}

[symbol]
description: This template collects frequently-used symbols using the HCR Batang font.
output: symbols
compiler: -c
sty:	`\RequirePackage{xparse}
		`\RequirePackage{etoolbox}
		`\AtEndPreamble{
		`	\@ifpackageloaded{fontspec}{}{\RequirePackage{fontspec}}
		`	\@ifpackageloaded{graphicx}{}{\RequirePackage{graphicx}}
		`}
		`\ExplSyntaxOn 
		`\tl_if_exist:NF \keyfontname
		`{
		`	\tl_set:Nn \keyfontname { HCR~Batang }
		`}
		`\prop_new:N \g_hcrkey_prop
		`\prop_set_from_keyval:Nn \g_hcrkey_prop
		`{
		`	f1 = F035F,
		`	f2 = F0360,
		`	f3 = F0361,
		`	f4 = F0362,
		`	f5 = F0363,
		`	f6 = F0364,
		`	f7 = F0365,
		`	f8 = F0366,
		`	f9 = F0367,
		`	f10 = F0368,
		`	f11 = F0369,
		`	f12 = F036A,
		`	alt = F036B,
		`	ctrl = F036D,
		`	shift = F036C,
		`	tab = F036E,
		`	space = F039E,
		`	esc = F03A2,
		`	backquote = F036F,
		`	tilde = F036F,
		`	! = F0370,
		`	1 = F0370,
		`	@ = F0371,
		`	2 = F0371,
		`	hash = F0372,
		`	3 = F0372,
		`	dollar = F0373,
		`	4 = F0373,
		`	percent = F0374,
		`	5 = F0374,
		`	caret = F0375,
		`	6 = F0375,
		`	ampersand = F0376,
		`	7 = F0376,
		`	* = F0377,
		`	8 = F0377,
		`	( = F0378,
		`	9 = F0378,
		`	) = F0379,
		`	0 = F0379,
		`	- = F037A,
		`	_ = F037A,
		`	+ = F037B,
		`	{=} = F037B,
		`	| = F037C,
		`	backslash = F037C,
		`	a = F037D,
		`	b = F037E,
		`	c = F037F,
		`	d = F0380,
		`	e = F0381,
		`	f = F0382,
		`	g = F0383,
		`	h = F0384,
		`	i = F0385,
		`	j = F0386,
		`	k = F0387,
		`	l = F0388,
		`	m = F0389,
		`	n = F038A,
		`	o = F038B,
		`	p = F038C,
		`	q = F038D,
		`	r = F038E,
		`	s = F038F,
		`	t = F0390,
		`	u = F0391,
		`	v = F0392,
		`	w = F0393,
		`	x = F0394,
		`	y = F0395,
		`	z = F0396,
		` 	\{ = F0397,
		`	leftbrace = F0397,
		`	[ = F0397,
		`	\} = F0398,
		`	rightbrace = F0398,
		`	] = F0398,
		`	: = F0399,
		`	; = F0399,
		`	" = F039A,
		`	' = F039A,
		`	< = F039B,
		`	, = F039B,
		`	> = F039C,
		`	. = F039C,
		`	? = F039D,
		`	/ = F039D,
		`	space = F039E,
		`	backspace = F03A1,
		`	enter = F03A0,
		`	capslock = F039F,
		`	numlock = F03A3,
		`	scrolllock = F03A4,
		`	sysreq = F03A5,
		`	numprtsc = F03A6,
		`	num+ = F03A8,
		`	num- = F03A7,
		`	numdel = F03A9,
		`	numdot = F03A9,
		`	numins = F03AA,
		`	num0 = F03AA,
		`	numend = F03AB,
		`	num1 = F03AB,
		`	numdown = F03AC,
		`	num2 = F03AC,
		`	numpgdn = F03AD,
		`	num3 = F03AD,
		`	numleft = F03AE,
		`	num4 = F03AE,
		`	num5 = F03AF,
		`	numright = F03B0,
		`	num6 = F03B0,
		`	numhome = F03B1,
		`	num7 = F03B1,
		`	numup = F03B2,
		`	num8 = F03B2,
		`	numpgup = F03B3,
		`	num9 = F03B3,
		`	numenter = F03C0,
		`	num* = F03C1,
		`	num/ = F03C2,
		`	prtsc = F03C3,
		`	numpause = F03C4,
		`	pause = F03C4,
		`	insert = F03B6,
		`	ins = F03B6,
		`	delete = F03B7,
		`	del = F03B7,
		`	home = F03B8,
		`	end = F03B9,
		`	pageup = F03BA,
		`	pgup = F03BA,
		`	pagedown = F03BB,
		`	pgdn = F03BB,
		`	left = F03BC,
		`	right = F03BD,
		`	up = F03BE,
		`	down = F03BF,
		`	blank = F03C5,
		`}
		`
		`\NewDocumentCommand \hcrkey { m }
		`{
		`	\tl_set:Nx \l_tmpa_tl { \str_foldcase:n { #1 } }
		`	\str_case_e:nnF { \l_tmpa_tl } 
		`	{
		`		{ windows }
		`		  {
		`    		\group_begin:
		`    		\fontspec {\keyfontname} 
		`    		\raisebox{-.09em}{\includegraphics[width=.9em]{hcrkey_winlogo}\hspace{.05em}}
		`			\sys_if_engine_luatex:TF 
		`			{
		`				\hbox_overlap_left:n { \symbol { "F03C7 } }
		`			}{
		`				\hbox_overlap_left:n { \symbol{"F03C5 } }
		`			}
		`    		\group_end:
		`		  }
		`		{ fn }  
		`		  {
		`        	\group_begin:
		`        	\fontspec { \keyfontname }
		`        	\hbox_set:Nn \l_tmpa_box { \sffamily Fn \hspace{.1em} }
		`        	\box_resize_to_wd:Nn \l_tmpa_box { .9em }
		`        	\box_use_drop:N \l_tmpa_box 
		`			\sys_if_engine_luatex:TF
		`			{
		`				\hbox_overlap_left:n { \symbol { "F03C7 } }
		`			}{
		`				\hbox_overlap_left:n { \symbol{"F03C5 } }
		`			}
		`        	\group_end:
		`		  }
		`	}{
		`    	\prop_get:NVN \g_hcrkey_prop \l_tmpa_tl \l_tmpb_tl
		`    	\sys_if_engine_luatex:T 
		`		{ 
		`			\exp_args:NNx \int_set:Nn \l_tmpa_int { \exp_args:No \int_from_hex:n { \l_tmpb_tl } }
		`			\int_add:Nn \l_tmpa_int { 2 }
		`			\tl_set:Nx \l_tmpb_tl { \exp_args:No \int_to_Hex:n { \l_tmpa_int } }
		`		}
		`		\quark_if_no_value:NF \l_tmpb_tl
		`		{
		`			\group_begin: 
		`				\exp_args:No \fontspec {\keyfontname}
		`				\exp_args:Nx \symbol { " \l_tmpb_tl }
		`			\group_end:
		`		}
		`	 }
		`}
		`\ExplSyntaxOff

tex:	\documentclass{article}
		\usepackage{symbols}
		\def\keyfontname{HCR Batang}
		\setlength\parindent{0pt}
		\begin{document}
		\setmainfont{HCR Batang}
		\Large
		− minus \\
		– en dash \\
		— em dash \\
		″ double prime for inch \\
		〜 wave dash (301C) \\
		• · 『 』「 」≪ ≫ … ⧵ \\
		± ÷ × ≤ ≥ ² ³ ₂ ₃ \\
		 ◯ ✓ ✔ ✗ ✘ □ ☐ ☑ \\
		°C °F ㈜ ₩ © ® ™  ㈜ \\		
		← → ↑ ↓ ⇐ ⇒ ⇑ ⇓ ⇦ ⇨ ⇧ ⇩ ► ◄ ▲ ▼ \\
		① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ \\
		Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ Ⅵ Ⅶ Ⅷ Ⅸ Ⅹ \\
		Α	α	Β	β	Γ	γ	Δ	δ	Ε	ε	Ζ	ζ	Η	η	Θ	θ	Ι	ι	Κ	κ	Λ	λ	Μ	μ	\\
		Ν	ν	Ξ	ξ	Ο	ο	Π	π	Ρ	ρ	Σ	σ ς Τ	τ	Υ	υ	Φ	φ	Χ	χ	Ψ	ψ	Ω	ω \\
		⌀ diameter, available with Noto Sans Symbols \\
		ø o with stroke, as an alternative to ⌀ \\		
		↵ \\
		\hcrkey{f1} \hcrkey{f2} \hcrkey{f3} \hcrkey{f4} \hcrkey{f5} \hcrkey{f6} \hcrkey{f7} \hcrkey{f8} \hcrkey{f9} \hcrkey{f10} \hcrkey{f11} \hcrkey{f12} \\
		\hcrkey{a} \hcrkey{b} \hcrkey{c} \hcrkey{d} \hcrkey{e} \hcrkey{f} \hcrkey{g} \hcrkey{h} \hcrkey{i} \hcrkey{j} \hcrkey{k} \hcrkey{l} \hcrkey{m} \hcrkey{n} \hcrkey{o} \hcrkey{p} \hcrkey{q} \hcrkey{r} \hcrkey{s} \hcrkey{t} \hcrkey{u} \hcrkey{v} \hcrkey{w} \hcrkey{x} \hcrkey{y} \hcrkey{z} \\
		\hcrkey{ESC} \hcrkey{Alt} \hcrkey{Ctrl} \hcrkey{TAB} \hcrkey{capslock} \hcrkey{Shift} \hcrkey{space} \hcrkey{backspace} \hcrkey{del} \hcrkey{ins} \hcrkey{enter} \\
		\hcrkey{left} \hcrkey{right} \hcrkey{up} \hcrkey{down} \hcrkey{pgup} \hcrkey{pgdn} \hcrkey{home} \hcrkey{end} \\
		\hcrkey{backquote} \hcrkey{1} \hcrkey{2} \hcrkey{3} \hcrkey{4} \hcrkey{5} \hcrkey{6} \hcrkey{7} \hcrkey{8} \hcrkey{9} \hcrkey{0}\\
		\hcrkey{-} \hcrkey{+} \hcrkey{\{} \hcrkey{\}} \hcrkey{backslash} \hcrkey{:} \hcrkey{"} \hcrkey{<} \hcrkey{>} \hcrkey{?}\\
		\hcrkey{PrtSc} \hcrkey{ScrollLock} \hcrkey{Pause} \hcrkey{NumLock} \\
		\hcrkey{num/} \hcrkey{num*} \hcrkey{num-} \hcrkey{num+} \hcrkey{numEnter} \\
		\hcrkey{num1} \hcrkey{num2} \hcrkey{num3} \hcrkey{num4} \hcrkey{num5} \hcrkey{num6} \hcrkey{num7} \hcrkey{num8} \hcrkey{num9} \\
		\hcrkey{numins} \hcrkey{numdel} 
		\end{document}