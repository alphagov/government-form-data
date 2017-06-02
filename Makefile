.PHONY: data clean

# data maintained by hand
SOURCE_DATA=\
	data/task.tsv\
	data/question.tsv

# data derived from GOV.UK and registers
TARGET_DATA=\
	data/page.tsv\
	data/history.tsv\
	data/organisation.tsv\
	data/download.tsv\
	data/attachment.tsv

DATA=\
	$(SOURCE_DATA) \
	$(TARGET_DATA)


# data made for visualisations
INDEXES=\
	vis/orgs.json\
	vis/pages.tsv

all: $(DATA) $(INDEXES)

server: $(INDEXES)
	python3 -m http.server

#
#  build target data
#
data/organisation.tsv:	bin/organisations.py
	@mkdir -p cache/page
	python3 bin/organisations.py > $@

data/page.tsv:	bin/pages.py cache/govuk-pages.jsonl data/slug.tsv
	@mkdir -p cache/page
	python3 bin/pages.py < cache/govuk-pages.jsonl > $@

data/attachment.tsv:	bin/attachments.py data/page.tsv
	python3 bin/attachments.py < data/page.tsv > $@

data/history.tsv:	bin/history.py data/page.tsv
	python3 bin/history.py < data/page.tsv > $@

data/download.tsv:	bin/downloads.py data/attachment.tsv
	zcat cache/downloads.gz | python3 bin/downloads.py > $@

#
#  forms pages from GOV.UK search API
#
cache/govuk-pages.jsonl:	bin/govuk-pages.py
	@mkdir -p cache
	bin/govuk-pages.py > $@

#
#  visualisation data
#
vis/pages.tsv:	$(DATA) vis/pages.py
	python3 vis/pages.py > $@

vis/orgs.json:	$(DATA) vis/orgs.py
	python3 vis/orgs.py > $@

#
#  python
#
init::
	pip3 install -r requirements.txt

flake8:
	flake8

clobber:
	rm -f $(TARGET_DATA) $(INDEXES)

clean:	clobber
	-rm -rf ./cache
	-find . -name '*.pyc' | xargs rm -f
	-find . -name '__pycache__' | xargs rm -rf
