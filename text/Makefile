.PHONY: all thesis-text clean

OD=false

all: thesis-text

thesis-text: 
ifeq ($(OD),true)
	echo "\toggletrue{withofficialdesc}" > flags.tex
else
	echo "" > flags.tex
endif
	pdflatex -interaction=nonstopmode -synctex=1 index.tex
	bibtex index.aux
	pdflatex -interaction=nonstopmode -synctex=1 index.tex > /dev/null
	pdflatex -interaction=nonstopmode -synctex=1 index.tex > /dev/null

fast:
	pdflatex --interaction=nonstopmode -synctex=1 index.tex

start: thesis-text
	evince index.pdf

slice: thesis-text
ifeq ($(OD),true)
	pdftk thesis-text.pdf cat 12 19-20 24 26-31 33-35 46-47 output color-thesis.pdf
	pdftk thesis-text.pdf cat 1-11 13-18 21-23 25 32 36-45 48 output black-thesis.pdf
else
	pdftk thesis-text.pdf cat 11 18-19 23 25-30 32-34 45-46 output color-thesis.pdf
	pdftk thesis-text.pdf cat 1-10 12-17 20-22 24 31 35-44 47 output black-thesis.pdf
endif

clean:
	rm -rf *.{log,out,pdf,aux,tfm,600pk,514pk,fls,toc,bbl,blg,fdb_latexmk,synctex.gz} flags.tex
