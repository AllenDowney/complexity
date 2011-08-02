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
	latex book
	makeindex book
	latex book
	dvips -t letter -Ppdf -o downey08compmod.ps book	
#	dvips -T 7.444in,9.93in -Ppdf -o downey08compmod.ps book
	gv downey08compmod.ps

pdf:
	ps2pdf $(PDFFLAGS) downey08compmod.ps


html:	book.tex
	rm -rf html
	mkdir html
	hevea -e latexonly htmlonly book
	# the following line is a kludge to prevent imagen from seeing
	# the definitions in latexonly
	grep -v latexonly book.image.tex > a; mv a book.image.tex
	imagen -png book
	hacha book.html
	mv index.html book*.html book*.png *motif.gif html

DEST = /home/downey/public_html/greent/compmod

distrib:
	rm -rf dist
	mkdir dist dist/tex dist/tex/figs
	rsync -a downey08compmod.pdf downey08compmod.ps html dist
	rsync -a Makefile book.tex latexonly htmlonly dist/tex
	rsync -a figs/*.fig figs/*.eps dist/tex/figs
	cd dist; zip -r downey08compmod.tex.zip tex
	cd dist; zip -r downey08compmod.html.zip html
	rsync -a dist/* $(DEST)
	chmod -R o+r $(DEST)/*

clean:
	rm -f *~ *.aux *.log *.dvi *.idx *.ilg *.ind *.toc



