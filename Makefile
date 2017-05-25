.PHONY: data clean

# data maintained by hand
SOURCE_DATA=\
	data/task.tsv\
	data/question.tsv

# data derived from GOV.UK and registers
TARGET_DATA=\
	data/page.tsv\
	data/organisation.tsv\
	data/attachment.tsv

DATA=\
	$(SOURCE_DATA) \
	$(TARGET_DATA)


# data made for visualisations
INDEXES=\
	vis/orgs.json
#	vis/pages.json

all: $(DATA) $(INDEXES)

server: $(INDEXES)
	python3 -m http.server

#
#  build explorer data
#
data/page.tsv:	bin/pages.py cache/govuk-pages.jsonl data/slug.tsv
	@mkdir -p cache/page
	bin/pages.py < cache/govuk-pages.jsonl > $@

data/attachment.tsv:	bin/attachments.py data/page.tsv
	python3 bin/attachments.py < data/page.tsv > $@

#
#  forms pages from GOV.UK search API
#
cache/govuk-pages.jsonl:	bin/govuk-pages.py
	bin/govuk-pages.py > $@

#
#  visualisation data
#
vis/pages.json:	$(DATA) vis/pages.py
	python3 vis/pages.py > $@

vis/orgs.json:	$(DATA) vis/orgs.py
	python3 vis/orgs.py > $@


clobber:
	rm -f $(TARGET_DATA)

clean:	clobber
	-rm -rf ./cache
	-find . -name '*.pyc' | xargs rm -f
	-find . -name '__pycache__" | xargs rm -rf
