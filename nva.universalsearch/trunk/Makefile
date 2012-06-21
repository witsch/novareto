
version = 2.6
python = python$(version)

test: .installed.cfg
	bin/test

.installed.cfg: bin/buildout buildout.cfg
	bin/buildout

bin/buildout: bootstrap.py
	$(python) bootstrap.py

clean:
	-rm -rf .installed.cfg bin parts develop-eggs fake-eggs

.PHONY: test clean
