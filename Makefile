PYTHON ?= python3
VENV_DIR := .venv
ACTIVATE := . $(VENV_DIR)/bin/activate

.PHONY: all run deps open clean

all: run

$(VENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(VENV_DIR)

deps: $(VENV_DIR)/bin/activate
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

run: deps
	$(ACTIVATE) && FLASK_APP=app.py FLASK_ENV=development flask run --port 5001 & \
	sleep 2 && open http://127.0.0.1:5001/

clean:
	rm -rf $(VENV_DIR) polls.db __pycache__
