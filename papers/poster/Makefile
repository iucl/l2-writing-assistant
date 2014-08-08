NAME=poster

$(NAME).pdf: $(NAME).tex
	pdflatex $(NAME)
	pdflatex $(NAME)

clean:
	rm -f *.nav *.snm *.bbl *.blg *.out *.aux *.log $(NAME).pdf
