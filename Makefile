install: ## Installs development requirments
install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	# python -m pytest -vv --cov=main --cov=mylib test_*.py

format:	
	black *.py

run:
	## 

clean:
	-find . -name '*.pyc' -exec rm -rf {} \;
	-find . -name '__pycache__' -exec rm -rf {} \;
	-rm -rf .cache
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info
	-rm -rf htmlcov*
	-rm -rf .tox/
	-rm -rf docs/_build
	-rm -r .coverage
	-rm -rf .pytest_cache

codestyle:
	pycodestyle $(PROJECT)

docstyle:
	pydocstyle $(PROJECT)

lint:
lint: ## Lint and static-check
	flake8 Web_Scrapping_Experiments MLflow_Experiments HuggingFaces_Experiments Data_Quality_Experiments Clustering_Experiments
	pylint Web_Scrapping_Experiments MLflow_Experiments HuggingFaces_Experiments Data_Quality_Experiments Clustering_Experiments
	mypy Web_Scrapping_Experiments MLflow_Experiments HuggingFaces_Experiments Data_Quality_Experiments Clustering_Experiments

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy
