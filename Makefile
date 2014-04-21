default: test

test: env
	.env/bin/py.test

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

env: .env/.up-to-date

.PHONY: env

.env/.up-to-date: Makefile setup.py test_requirements.txt
	@echo "\x1b[32;01mSetting up environment. This could take a while...\x1b[0m"
	virtualenv --no-site-packages .env
	.env/bin/pip install -r test_requirements.txt
	.env/bin/pip install -e .
	touch .env/.up-to-date

