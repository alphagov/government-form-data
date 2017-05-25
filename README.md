Experimental data for exploring forms found on GOV.UK

<a href="https://www.flickr.com/photos/psd/34781307466/in/dateposted-ff/" title="government-form-explorer"><img src="https://c1.staticflickr.com/5/4160/34781307466_ef8d5f5574.jpg" alt="government-form-explorer"></a>

* [page](data/page.tsv) — GOV.UK pages with [form content](https://docs.publishing.service.gov.uk/document-types/form.html)
* [attachment](data/attachment.tsv) — GOV.UK attachments associated with form pages
* [organisation](data/page.tsv) — organisations responsible for forms, data assembled from various registers
* [slug](data/slug.tsv)

* [form](data/form.tsv) — forms, as understood by users
* [task](data/task.tsv) — user tasks, and the people who design and process forms used to complete them
* [question](data/question.tsv) — questions found in forms

# Building

Use make to download and build the data from GOV.UK and registers
– we recommend using a [Python virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv -p python3 government-form-data
    $ workon government-form-data
    $ make init
    $ make

To refresh pages and organisations:

    $ make clobber
    $ make

# Licence

The software in this project is covered by LICENSE file.

The data is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
