refactor:
	format lint
	
format:
	black *.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py

container-lint:
	docker run --rm -i hadolint/hadolint < DockerFile

deploy:


all:
	install lint test format deploy
