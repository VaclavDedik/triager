.PHONY: all thesis-text clean

all: thesis-text

thesis-text: 
	pdflatex -interaction=nonstopmode -synctex=1 thesis.tex
	bibtex thesis.aux
	pdflatex -interaction=nonstopmode -synctex=1 thesis.tex > /dev/null
	pdflatex -interaction=nonstopmode -synctex=1 thesis.tex > /dev/null

fast:
	pdflatex --interaction=nonstopmode -synctex=1 thesis.tex

start: thesis-text
	evince thesis.pdf

clean:
	rm -rf *.{log,out,pdf,aux,tfm,600pk,514pk,fls,toc,bbl,blg,fdb_latexmk,synctex.gz}