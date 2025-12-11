.PHONY: serve install pdf

install:
	bundle install

serve:
	bundle exec jekyll serve

pdf:
	../fishwrap/venv/bin/python3 generate_pdf.py
