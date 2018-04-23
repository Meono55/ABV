import re
from pytest import fixture
import abv.twilio_api.twilio_flask as twilio_flask
import requests_mock



@fixture()
def app():
    twilio_flask.app.testing = True
    inner_app = twilio_flask.app.test_client()
    return inner_app


# pylint: disable=redefined-outer-name
def test_bad_status_code(app):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[]', status_code=404)
        result = app.get('/', data={'Body':'stout'})
        assert b'Sorry, I cannot handle your request. Please try again later!' in result.data


# pylint: disable=redefined-outer-name
def test_valid_twilio_format(app):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}, {"name":"foo"}]')
        result = app.get('/', data={'Body': 'stout'})
        assert result.status_code == 200
        assert result.data.startswith(b'<?xml')


# pylint: disable=redefined-outer-name
def test_no_results(app):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[]')
        result = app.get('/', data={'Body':'stout'})
        assert b'Sorry, no results for stout' in result.data

# pylint: disable=redefined-outer-name
def test_one_result(app):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}]')
        result = app.get('/', data={'Body': 'porter'})
        assert b'There is 1 beer with the style porter' in result.data

# pylint: disable=redefined-outer-name
def test_tw0_result(app):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}, {"name":"bar"}]')
        result = app.get('/', data={'Body': 'IPA'})
        assert b'There are 2 beers with the style IPA' in result.data


def test_count_beers():
    assert twilio_flask.count_beers('[{}, {}]') == 2
