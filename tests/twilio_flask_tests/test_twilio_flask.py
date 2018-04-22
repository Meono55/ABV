import abv.twilio_api.twilio_flask as twilio_flask
from pytest import fixture
from requests_mock import Mocker
import re


@fixture()
def app():
    twilio_flask.app.testing = True
    app = twilio_flask.app.test_client()
    return app


def test_valid_twilio_format(app):
    with Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}, {"name":"foo"}]')
        result = app.get('/', data={'Body': 'stout'})
        assert result.status_code == 200
        assert result.data.startswith(b'<?xml')


def test_no_results(app):
    with Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[]')
        result = app.get('/', data = {'Body':'stout'})
        assert b'Sorry, no results for stout' in result.data


def test_one_result(app):
    with Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}]')
        result = app.get('/', data={'Body': 'porter'})
        assert b'There is 1 beer with the style porter' in result.data

def test_tw0_result(app):
    with Mocker() as m:
        m.register_uri('GET', re.compile('beerapi'), text='[{"name":"foo"}, {"name":"bar"}]')
        result = app.get('/', data={'Body': 'IPA'})
        assert b'There are 2 beers with the style IPA' in result.data



def test_count_beers():
    assert twilio_flask.count_beers('[{}, {}]') == 2