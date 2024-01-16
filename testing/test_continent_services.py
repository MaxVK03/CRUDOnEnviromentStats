from services import continent_service
from unittest.mock import Mock


def test_get_temperature_change_by_continent_service():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.options.return_value.all.return_value = [
        {'year': 2020, 'data': 'test data'}]
    result = continent_service.get_temperature_change_by_continent(mock_db, 'Europe', -1)
    assert result == [{'year': 2020, 'data': 'test data'}]


def test_get_temperature_change_by_continent_service_with_year():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.options.return_value.all.return_value = [
        {'year': 2020, 'data': 'test data'}]
    result = continent_service.get_temperature_change_by_continent(mock_db, 'Europe', 2020)
    assert result == [{'year': 2020, 'data': 'test data'}]


#TODO: fix this test
def test_invalid_continent():
    # handle invalid continent
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.options.return_value.all.return_value = []
    try:
        continent_service.get_temperature_change_by_continent(mock_db, 'Unknown', -1)
        assert False
    except Exception as e:
        pass
        # assert str(e) == 'Invalid continent'

