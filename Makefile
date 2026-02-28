.PHONY: lint
lint:
	isort . && black . && pflake8 .