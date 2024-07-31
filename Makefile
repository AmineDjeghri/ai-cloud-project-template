include $(wildcard .env)

install:
	pip install -r requirements.txt; pip install -r requirements-dev.txt; pre-commit install

run_frontend:
	@echo "Running frontend"
	cd src; streamlit run streamlit_ui.py --server.port $(STREAMLIT_PORT) --server.headless True;

run_backend:
	@echo "Running backend"
	python src/api_server.py;

run_all:
	make run_frontend run_backend -j2

pre-commit:
	@echo "Running pre-commit..."
	pre-commit run --all-files
test:
	@echo "Running tests..."
	cd src; pytest tests
