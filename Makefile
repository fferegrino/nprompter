TOOL_RUN=uv run

fmt:
	$(TOOL_RUN) ruff format .
	$(TOOL_RUN) ruff check . --select I --fix

lint:
	$(TOOL_RUN) pflake8 .
	$(TOOL_RUN) ruff format . --check
	$(TOOL_RUN) ruff check . --select I

docs:
	$(TOOL_RUN) mkdocs build

docs-serve:
	$(TOOL_RUN) mkdocs serve

clean:
	rm -rf .content dist

patch:
	./release.sh patch

minor:
	./release.sh minor

major:
	./release.sh major
