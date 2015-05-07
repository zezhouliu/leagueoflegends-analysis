fbasen := paper
targs := $(patsubst %,%.pdf,$(fbasen))

.PHONY: default
default: all 

.PHONY: targs
targs: $(targs)

%.pdf: %.tex $(wildcard *.tex) $(wildcard figure/*.tex) $(wildcard figure/*.eps)
	pdflatex $< 
	bibtex $* 
	pdflatex $<
	pdflatex $<

.PHONY: figs
figs:
	$(MAKE) -C figures

.PHONY: clean
clean:
	rm -f *~ *.bak $(patsubst %,%.pdf,$(fbasen)) $(patsubst %,%.dvi,$(fbasen)) $(patsubst %,%.log,$(fbasen)) $(patsubst %,%.aux,$(fbasen)) $(patsubst %,%.bbl,$(fbasen)) $(patsubst %,%.blg,$(fbasen)) 

.PHONY: cleanmost
cleanmost:
	rm -f *~ *.bak $(patsubst %,%.dvi,$(fbasen)) $(patsubst %,%.log,$(fbasen)) $(patsubst %,%.aux,$(fbasen)) $(patsubst %,%.bbl,$(fbasen)) $(patsubst %,%.blg,$(fbasen))

.PHONY: all
all: clean $(targs) cleanmost
