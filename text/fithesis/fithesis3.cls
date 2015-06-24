%%
%% This is file `fithesis3.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% fithesis.dtx  (with options: `class')
%% 
%% Copyright 1998--2015  Daniel Marek (DM), Jan Pavlovi^^c4^^8d (JP),
%%                       V^^c3^^adt Novotn^^c3^^bd (VN), Petr Sojka (PS)
%% http://www.fi.muni.cz/tech/unix/tex/fithesis.xhtml
%% Faculty of Informatics, Masaryk University (Brno, Czech Republic)
%% 
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version
%% 1.3 of this license or (at your option) any later version.
%% The latest version of this license is available at
%% 
%%   http://www.latex-project.org/lppl.txt
%% 
%% and version 1.3 or later is part of all distributions of LaTeX
%% version 2005/12/01 or later.
%% 
%% This work has the LPPL maintenance status `maintained'.
%% 
%% The Current Maintainer of this work is V^^c3^^adt Novotn^^c3^^bd (VN).
%% Send bug reports, requests for additions and questions
%% either to the fithesis discussion forum at
%% 
%%   http://is.muni.cz/auth/df/fithesis-sazba/
%% 
%% or to the e-mail address <witiko@mail.muni.cz>.
%% 
%% 
%% IMPORTANT COPYRIGHT NOTICE:
%% 
%% You are NOT ALLOWED to distribute this file alone.
%% 
%% If you receive only some of these files from someone, complain!
%% 
%% However, NO PERMISSION is granted to generate or to distribute a
%% modified version of this file under its original name.
%% 
%% You are NOT ALLOWED to change this file.
%% 
%% 
%% MODIFICATION ADVICE:
%% 
%% If you want to customize this file, it is best to make a copy of
%% the source file(s) from which it was produced.  Use a different
%% name for your copy(ies) and modify the copy(ies); this will ensure
%% that your modifications do not get overwritten when you install a
%% new release of the standard system.  You should also ensure that
%% your modified source file does not generate any modified file with
%% the same name as a standard file.
%% 
%% You will also need to produce your own, suitably named, .ins file to
%% control the generation of files from your source file; this file
%% should contain your own preambles for the files it generates, not
%% those in the standard .ins files.
%% 
%% The names of the source files used are shown above.
%% 
\NeedsTeXFormat{LaTeX2e}
\def\thesis@version{2015/06/24 v0.3.18 fithesis3 MU thesis class}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ProvidesClass{fithesis3}[\thesis@version]
\LoadClass[a4paper]{rapport3}
\RequirePackage{keyval}
\RequirePackage{etoolbox}
\RequirePackage{ifxetex}
\RequirePackage{ifluatex}
\ifxetex\else\ifluatex\else
  \RequirePackage[utf8]{inputenc}
\fi\fi
\def\thesissetup#1{%
  \setkeys{thesis}{#1}}
\def\thesis@basepath{fithesis/}
\define@key{thesis}{basePath}{%
  \ifx\thesis@empty#1\thesis@empty%
    \def\thesis@basepath{}%
  \else%
    \def\thesis@basepath{#1/}%
  \fi}
\def\thesis@logopath{\thesis@basepath logo/\thesis@university/}
\define@key{thesis}{logoPath}{%
  \def\thesis@logopath{\thesis@subdir#1%
    \empty\empty\empty\empty}}
\def\thesis@stylepath{\thesis@basepath style/}
\define@key{thesis}{stylePath}{%
  \def\thesis@stylepath{\thesis@subdir#1%
    \empty\empty\empty\empty}}
\def\thesis@localepath{\thesis@basepath locale/}
\define@key{thesis}{localePath}{%
  \def\thesis@localepath{\thesis@subdir#1%
    \empty\empty\empty\empty}}
\def\thesis@subdir#1#2#3#4\empty{%
  \ifx#1\empty%           <empty> -> <basepath>
    \thesis@basepath
  \else
    \if#1/%
      \ifx#2\empty%             / -> /
        /%
      \else%              /<path> -> /<path>/
        #1#2#3#4/%
      \fi
    \else%
      \if#1.%
        \ifx#2\empty%           . -> ./
          ./%
        \else
          \if#2.%
            \ifx#3\empty%      .. -> ../
              ../%
            \else
              \if#3/%   ../<path> -> ../<path>/
                ../#4/%
              \else
                \thesis@basepath#1#2#3#4/%
              \fi
            \fi
          \else
            \if#2/%      ./<path> -> ./<path>/
              ./#3#4/%
            \else
              \thesis@basepath#1#2#3#4/%
            \fi
          \fi
        \fi
      \else
        \thesis@basepath#1#2#3#4/%
      \fi
    \fi%
  \fi}
\newcommand{\thesis@def}[2][]{%
  \expandafter\def\csname thesis@#2\endcsname{%
    <<\ifx\thesis@empty#1\thesis@empty#2\else#1\fi>>}}
\def\thesis@declaration{\thesis@@{declaration}}
\long\def\KV@thesis@declaration#1{%
  \long\def\thesis@declaration{#1}}
\newif\ifthesis@woman\thesis@womanfalse
\define@key{thesis}{gender}{%
  \def\thesis@male{m}%
  \def\thesis@arg{#1}%
  \ifx\thesis@male\thesis@arg%
    \thesis@womanfalse%
  \else%
    \thesis@womantrue%
  \fi}
\def\thesis@parseAuthor#1{%
  \def\thesis@author{#1}%
  \def\thesis@author@head{\expandafter\expandafter\expandafter%
    \@gobble\thesis@head#1 \relax}%
  \def\thesis@author@tail{\thesis@tail#1 \relax}}
\thesis@def{author}%
\thesis@def[author]{author@head}%
\thesis@def[author]{author@tail}%
\define@key{thesis}{author}{%
  \thesis@parseAuthor{#1}}
\thesis@def{id}
\define@key{thesis}{id}{%
  \def\thesis@id{#1}}
\def\thesis@bachelors{bc}
\def\thesis@masters{mgr}
\def\thesis@doctoral{d}
\def\thesis@rigorous{r}
\let\thesis@type\thesis@bachelors
\define@key{thesis}{type}{%
  \def\thesis@type{#1}}
\def\thesis@university{mu}
\define@key{thesis}{university}{%
  \def\thesis@university{#1}}
\def\thesis@faculty{fi}
\define@key{thesis}{faculty}{%
  \def\thesis@faculty{#1}}
\thesis@def{department}
\define@key{thesis}{department}{%
  \def\thesis@department{#1}}
\thesis@def{departmentEn}
\define@key{thesis}{departmentEn}{%
  \def\thesis@departmentEn{#1}}
\thesis@def{programme}
\define@key{thesis}{programme}{%
  \def\thesis@programme{#1}}
\thesis@def{programmeEn}
\define@key{thesis}{programmeEn}{%
  \def\thesis@programmeEn{#1}}
\thesis@def{field}
\define@key{thesis}{field}{%
  \def\thesis@field{#1}}
\thesis@def{fieldEn}
\define@key{thesis}{fieldEn}{%
  \def\thesis@fieldEn{#1}}
\def\thesis@universityLogo{fithesis-base}
\define@key{thesis}{universityLogo}{%
  \def\thesis@universityLogo{#1}}
\def\thesis@facultyLogo{fithesis-\thesis@faculty}
\define@key{thesis}{facultyLogo}{%
  \def\thesis@facultyLogo{#1}}
\def\thesis@style{\thesis@university/fithesis-\thesis@faculty}
\define@key{thesis}{style}{%
  \def\thesis@style{#1}}
\newif\ifthesis@style@inheritance\thesis@style@inheritancetrue
\define@key{thesis}{styleInheritance}[true]{%
  \def\@true{true}%
  \def\@arg{#1}%
  \ifx\@true\@arg%
    \thesis@style@inheritancetrue%
  \else%
    \thesis@style@inheritancefalse%
  \fi}
\def\thesis@locale{%
  % Babel detection
  \ifx\languagename\undefined%
  english\else\languagename\fi}
\define@key{thesis}{locale}{%
  \def\thesis@locale{#1}}
\def\ifthesis@english{
  \expandafter\def\expandafter\@english\expandafter{\string%
  \english}%
  \expandafter\expandafter\expandafter\def\expandafter%
  \expandafter\expandafter\@locale\expandafter\expandafter%
  \expandafter{\expandafter\string\csname\thesis@locale\endcsname}%
  \expandafter\csname\expandafter i\expandafter f\ifx\@locale%
  \@english%
    true%
  \else%
    false%
  \fi\endcsname}
\newif\ifthesis@locale@inheritance\thesis@locale@inheritancetrue
\define@key{thesis}{localeInheritance}[true]{%
  \def\@true{true}%
  \def\@arg{#1}%
  \ifx\@true\@arg%
    \thesis@locale@inheritancetrue%
  \else%
    \thesis@locale@inheritancefalse%
  \fi}
\def\thesis@parseDate#1/#2/#3|{{
  % Basic info
  \gdef\thesis@date{#1/#2/#3}%
  \gdef\thesis@year{#1}%
  \gdef\thesis@month{#2}%
  \gdef\thesis@day{#3}%

  % Season and academic year
  \newcount\@year \expandafter\@year \thesis@year \relax%
  \newcount\@month\expandafter\@month\thesis@month\relax%
  \ifnum\@month<7%
    \gdef\thesis@season{winter}%
    \advance\@year-1\edef\@yearA{\the\@year}%
    \advance\@year 1\edef\@yearB{\the\@year}%
  \else%
    \gdef\thesis@season{summer}%
                    \edef\@yearA{\the\@year}%
    \advance\@year 1\edef\@yearB{\the\@year}%
  \fi%
  \global\edef\thesis@academicYear{\@yearA/\@yearB}}}

\edef\thesis@date{\the\year/\the\month/\the\day}%
\expandafter\thesis@parseDate\thesis@date|%

\define@key{thesis}{date}{{%
  \edef\@date{#1}%
  \expandafter\thesis@parseDate\@date|}}
\def\thesis@place{Brno}
\define@key{thesis}{place}{%
  \def\thesis@place{#1}}
\thesis@def{title}
\define@key{thesis}{title}{%
  \def\thesis@title{#1}}
\def\thesis@TeXtitle{\thesis@title}
\define@key{thesis}{TeXtitle}{%
  \def\thesis@TeXtitle{#1}}
\thesis@def{titleEn}
\define@key{thesis}{titleEn}{%
  \def\thesis@titleEn{#1}}
\def\thesis@TeXtitleEn{\thesis@titleEn}
\define@key{thesis}{TeXtitleEn}{%
  \def\thesis@TeXtitleEn{#1}}
\thesis@def{keywords}
\define@key{thesis}{keywords}{%
  \def\thesis@keywords{#1}}
\def\thesis@TeXkeywords{\thesis@keywords}
\define@key{thesis}{TeXkeywords}{%
  \def\thesis@TeXkeywords{#1}}
\thesis@def{keywordsEn}
\define@key{thesis}{keywordsEn}{%
  \def\thesis@keywordsEn{#1}}
\def\thesis@TeXkeywordsEn{\thesis@keywordsEn}
\define@key{thesis}{TeXkeywordsEn}{%
  \def\thesis@TeXkeywordsEn{#1}}
\thesis@def{abstract}
\long\def\KV@thesis@abstract#1{%
  \long\def\thesis@abstract{#1}}
\thesis@def{abstractEn}
\long\def\KV@thesis@abstractEn#1{%
  \long\def\thesis@abstractEn{#1}}
\thesis@def{advisor}
\define@key{thesis}{advisor}{\def\thesis@advisor{#1}}
\long\def\KV@thesis@thanks#1{%
  \long\def\thesis@thanks{#1}}
\define@key{thesis}{assignment}{%
  \def\thesis@assignmentFiles{#1}}
\newif\ifthesis@auto\thesis@autotrue
\define@key{thesis}{autoLayout}[true]{%
  \def\@true{true}%
  \def\@arg{#1}%
  \ifx\@true\@arg%
    \thesis@autotrue%
  \else%
    \thesis@autofalse%
  \fi}
\def\thesis@preamble{}
\def\thesis@postamble{}
\long\def\thesislong#1#2{%
  \csname KV@thesis@#1\endcsname{#2}}
\newif\ifthesis@loaded\thesis@loadedfalse
\AtEndPreamble{\thesis@load}
\def\thesis@load{%
  \ifthesis@loaded\else%
    \thesis@loadedtrue
    \makeatletter%
      \ifx\thesis@locale\empty\else
        \thesis@requireLocale{\thesis@locale}
      \fi
      \ifx\thesis@style\empty\else
        \thesis@requireStyle{\thesis@style}
      \fi
       \thesis@require{hyperref}%
      {\hypersetup{unicode,
         pdftitle={\thesis@title},%
         pdfauthor={\thesis@author},%
         pdfkeywords={\thesis@keywords},%
         pdfcreator={\thesis@version},%
     }}%
      \ifthesis@auto%
        \AtBeginDocument{\thesis@preamble}%
        \AtEndDocument{\thesis@postamble}%
      \fi%
      \AtEndDocument{%
        % Define \thesis@pages for the next run
        \write\@auxout{\noexpand\gdef\noexpand%
          \thesis@pages{\thepage}}}
    \makeatother%
  \fi}
\def\thesis@input#1{%
  \thesis@exists{#1}{\input{#1}}}
\def\thesis@exists#1#2{%
  \IfFileExists{#1}{#2}{%
  \ClassWarning{fithesis3}{File #1 doesn't exist}}}
\def\thesis@require#1{%
  \@ifpackageloaded{#1}{}{\RequirePackage{#1}}}
\def\thesis@requireWithOptions#1{\thesis@exists{#1.sty}{%
  \@ifpackageloaded{#1}{}{\RequirePackageWithOptions{#1}}}}
\def\thesis@requireStyle#1{%
  \ifthesis@style@inheritance%
    \thesis@requireWithOptions{\thesis@stylepath fithesis-base}%
    \thesis@requireWithOptions{\thesis@stylepath\thesis@university%
      /fithesis-base}
  \fi%
  \thesis@requireWithOptions{\thesis@stylepath#1}}
\def\thesis@requireLocale#1{%
  % Prevent redundant entries
  \expandafter\ifx\csname thesis@#1@required\endcsname\relax%
    \expandafter\def\csname thesis@#1@required\endcsname{}%
      \thesis@input{\thesis@localepath#1.def}
      \ifthesis@locale@inheritance%
        \thesis@input{\thesis@localepath\thesis@university/#1.def}%
        \thesis@input{\thesis@localepath\thesis@university/%
          \thesis@faculty/#1.def}%
      \fi%
  \fi}
\def\thesis@#1{\csname thesis@#1\endcsname}
\def\thesis@@#1{\thesis@{\thesis@locale @#1}}
\def\thesis@lower#1{{%
  \let\ea\expandafter%
  \ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\lowercase\ea\ea\ea
  \ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea{\ea\ea\ea\ea\ea\ea\ea\ea\ea
  \ea\ea\ea\ea\ea\ea\@gobble\ea\ea\ea\string\ea\csname\csname the%
  sis@#1\endcsname\endcsname}}}
\def\thesis@upper#1{{%
  \let\ea\expandafter%
  \ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\uppercase\ea\ea\ea
  \ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea\ea{\ea\ea\ea\ea\ea\ea\ea\ea\ea
  \ea\ea\ea\ea\ea\ea\@gobble\ea\ea\ea\string\ea\csname\csname the%
  sis@#1\endcsname\endcsname}}}
\def\thesis@@lower#1{\thesis@lower{\thesis@locale @#1}}
\def\thesis@@upper#1{\thesis@upper{\thesis@locale @#1}}
\def\thesis@head#1 #2{%
  \ifx\relax#2%
    \expandafter\@gobbletwo%
  \else%
    \ #1%
  \fi%
  \thesis@head#2}%
\def\thesis@tail#1 #2{%
  \ifx\relax#2%
    #1%
    \expandafter\@gobbletwo%
  \fi%
  \thesis@tail#2}%
\ifx\thesis@pages\undefined\def\thesis@pages{??}\fi
\endinput
%%
%% End of file `fithesis3.cls'.
