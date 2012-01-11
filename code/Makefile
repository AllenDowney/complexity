FILES = GraphCode.py  GraphWorld.py  RandomGraph.py  Map.py  listsum.py \
Pmf.py  SmallWorldGraph.py  Zipf.py CA.py CADrawer.py CircularCA.py \
Forest.py Fourier.py Life.py Highway.py Boids.py \
ipd/Referee.py ipd/PlayerFlipper.py \
Graph.py GraphTest.py populations.py \
DirectedGraph.py ants.py normsGame.py volunteersDilemma.py \
Sugarscape.zip

SFILES = Sugarscape/Agent.py Sugarscape/DataCollect.py Sugarscape/Gui.py \
Sugarscape/Matrix.py  Sugarscape/Sugarscape.py \
Sugarscape/Button.py  Sugarscape/Government.py   Sugarscape/Location.py  \
Sugarscape/Slider.py

DOCS = 

DOCPY = 

DEST = /home/downey/public_html/greent/complexity

FIGS = listsum1.pdf listsum1.pdf cdf_example.pdf \
fractal-254-4.pdf fractal-254-8.pdf fractal_dim-18-64.pdf \
rule-50-10.pdf rule-18-64.pdf rule-30-100.pdf rule-110-100.pdf \
rule-110-600-random.pdf

code:
	zip -r Sugarscape.zip $(SFILES)
	rsync -a $(FILES) $(CS_FILES) $(DEST)
	chmod -R o+r $(DEST)/*

cas:
	python fractal.py
	python draw_cas.py 50 10 eps
	python draw_cas.py 18 64 eps
	python draw_cas.py 30 100 eps
	python draw_cas.py 110 100 eps
	python draw_cas.py 110 600 random trim eps

figs:
	epstopdf rule-50-10.eps
	epstopdf rule-18-64.eps
	epstopdf rule-30-100.eps
	epstopdf rule-110-100.eps
	epstopdf rule-110-600-random.eps
	rsync -a $(FIGS) $(FIGDEST)

make_figs:
	python listsum.py
	python cdf_example.py
	python draw_cas.py
	python fractal.py

FIGDEST = ../figs

%.html: %.py
	pydoc -w $<

.PHONY: docs $(DOCPY)

docs: $(DOCPY)

$(DOCPY):
	pydoc -w ./$@