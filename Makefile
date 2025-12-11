.PHONY: serve install pdf-deps generate-pdf publish-resume clean

VENV_PATH := $(CURDIR)/venv
PYTHON := $(VENV_PATH)/bin/python3
PIP := $(VENV_PATH)/bin/pip

# --- Setup & Environment ---
install:
	@echo "Setting up Python virtual environment and installing dependencies..."
	@python3 -m venv $(VENV_PATH)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Setup complete. To activate the venv, run 'source venv/bin/activate'."

# --- Jekyll Site ---
serve:
	@echo "Serving Jekyll site locally..."
	bundle install
	bundle exec jekyll serve

# --- PDF Generation ---
pdf-deps:
	@echo "Ensuring PDF generation dependencies are installed..."
	@if [ ! -d "$(VENV_PATH)" ]; then \
		$(MAKE) install; \
	fi
	@$(PIP) install -r requirements.txt

generate-pdf: pdf-deps
	@echo "Generating resume.pdf from index.md..."
	@$(PYTHON) generate_pdf.py

publish-resume: generate-pdf
	@echo "Publishing spevack.org (pushing changes to GitHub)..."
	git add .
	git commit -m "chore: Update website and resume PDF" || true # '|| true' to allow no-change commits
	git push

# --- Cleanup ---
clean:
	@echo "Cleaning up generated files..."
	rm -f resume.pdf
	@echo "Cleanup complete."