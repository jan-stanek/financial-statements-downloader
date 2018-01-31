Financial statements downloader
===============================

Task
----
Create terminal application for downloading financial statements from czech business register (https://or.justice.cz/)
and extracting information from them and storing them in structured form.

Input is a file with ICOs, one ICO per line.

At first the application downloads pdfs with financial statements. In the next step it extracts information specified in
config file and stores them in structured form.

The application must allow downloading documents of large number of companies, while respecting information system
limits (https://or.justice.cz/ias/ui/podminky).

Installation
------------
* ``pip install financial-statements-downloader``

Commands
--------
* ``import_icos <filepath>`` - imports ICOs from file
* ``download`` - downloads information about subjects and documents
* ``extract`` - extract information from financial statements

Config
------
::

  [downloader]
  base_url = https://or.justice.cz/ias/ui/  # information system url
  search_url = rejstrik-$firma?jenPlatne=VSECHNY&ico=  #search url
  limit_day = 3000  # download limit
  download_extract = true  # download information from extract
  download_documents = true  # download documents
  documents_type = závěrka  # document type
  documents_dir = documents  # directory for downloaded documents

  [parser]  # example of specification extracted information
  vlastni_kapital = Vlastní kapitál
  cizi_zdroje = Cizí zdroje
