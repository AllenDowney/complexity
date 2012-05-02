LATEX = latex

DVIPS = dvips

PDFFLAGS = -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
           -dCompressPages=true -dUseFlateCompression=true  \
           -dEmbedAllFonts=true -dSubsetFonts=true -dMaxSubsetPct=100

%.dvi: %.tex
	$(LATEX) $<

%.ps: %.dvi
	$(DVIPS) -o $@ $<

%.pdf: %.ps
	ps2pdf $(PDFFLAGS) $<

all:	book.tex
	makeindex book.idx
	pdflatex book
	mv book.pdf thinkcomplexity.pdf
	evince thinkcomplexity.pdf

hevea:
	rm -rf html
	mkdir html
	hevea -e latexonly htmlonly book
	imagen -png book
	hacha book.html
	cp up.png next.png back.png html
	mv index.html book*.html book*.png *motif.gif html

DEST = /home/downey/public_html/greent/complexity

distrib:
	rm -rf dist
	mkdir dist dist/tex dist/tex/figs
	rsync -a thinkcomplexity.pdf html dist
	rsync -a Makefile book.tex latexonly htmlonly dist/tex
	rsync -a figs/*.fig figs/*.eps dist/tex/figs
	cd dist; zip -r complexity.tex.zip tex; rm -r tex
	rsync -a dist/* $(DEST)
	chmod -R o+r $(DEST)/*

plastex:
	# Before running plastex, we need the current directory in PYTHONPATH
	# export PYTHONPATH=$PYTHONPATH:.
	python Filist.py book.tex > book.plastex
	rm -rf /home/downey/complexity/trunk/book
	plastex --renderer=DocBook --theme=book --image-resolution=300 --filename=book.xml book.plastex
	rm -rf /home/downey/complexity/trunk/book/.svn

diff:
	diff book/book.xml /home/downey/complexity/branches/manuscript.1.1/book/book.xml > patch

xxe:
	~/Downloads/xxe-perso-4_8_0/bin/xxe book/book.xml

OREILLY = /home/downey/oreilly/complexity

oreilly:
	rsync -a book/ $(OREILLY)
	rsync -a figs/* $(OREILLY)/figs
	rsync -a thinkcomplexity.pdf $(OREILLY)/pdf

clean:
	rm -f *~ *.aux *.log *.dvi *.idx *.ilg *.ind *.toc

