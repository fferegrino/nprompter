TOOL_RUN=poetry run

fmt:
	$(TOOL_RUN) black .
	$(TOOL_RUN) isort .

lint:
	$(TOOL_RUN) pflake8 .
	$(TOOL_RUN) isort . --check-only
	$(TOOL_RUN) black . --check

docs:
	$(TOOL_RUN) sphinx-build -M html docs/ docs/_build

clean:
	rm -rf .content dist

patch:
	./release.sh patch

minor:
	./release.sh minor

major:
	./release.sh major
