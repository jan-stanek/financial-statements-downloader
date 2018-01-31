from financial_statements_downloader.data import Data

data = Data("tests/fixtures/database/db.json")


def test_import_icos():
    data.import_icos('tests/fixtures/icos/icos1.csv')

    assert len(data.db) == 3

    data.import_icos('tests/fixtures/icos/icos2.csv')

    assert len(data.db) == 2


def test_get_not_downloaded():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.db.update({'downloaded': True}, data.query.query.ico == '00014010')

    subject = data.get_not_downloaded()

    assert subject['downloaded'] == False


def test_get_not_downloaded_empty():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.db.update({'downloaded': True})

    subject = data.get_not_downloaded()

    assert subject is None


def test_get_not_parsed():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.db.update({'parsed': True}, data.query.query.ico == '00014010')

    subject = data.get_not_parsed()

    assert subject['parsed'] == False


def test_get_not_parsed_empty():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.db.update({'parsed': True})

    subject = data.get_not_parsed()

    assert subject is None


def test_update_downloaded():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.update_downloaded('00014010', 200000, False, [])

    subject = data.db.get(data.query.ico == '00014010')

    assert subject['downloaded'] == True
    assert subject['capital_base'] == 200000
    assert subject['insolvency'] == False


def test_update_failed():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.update_failed('00014010')

    subject = data.db.get(data.query.ico == '00014010')

    assert subject['invalid'] == True


def test_update_parsed():
    data.import_icos('tests/fixtures/icos/icos2.csv')

    data.db.update({'documents': [{'file': 'file'}]}, data.query.ico == '00014010')

    data.update_parsed('00014010', 'file', {'test': 100000})

    subject = data.db.get(data.query.ico == '00014010')

    assert subject['parsed'] == True
    assert subject['documents'][0]['file'] == 'file'
    assert subject['documents'][0]['test'] == 100000