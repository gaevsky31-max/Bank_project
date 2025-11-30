""" Тест для processing.py"""

from src.processing import filter_by_state
from src.processing import sort_by_date


def test_filter_by_state() -> None:
    """ Тестируем функцию сортировки операций"""
    # Тестовые данные:
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    # Тест со статусом по умолчанию (EXECUTED):
    result_default = filter_by_state(test_data)
    assert len(result_default) == 2
    for operation in result_default:
        assert operation['state'] == 'EXECUTED'

    # Тест со статусом (CANCELED):
    result_canceled = filter_by_state(test_data, state='CANCELED')
    assert len(result_canceled) == 2
    for operation in result_canceled:
        assert operation['state'] == 'CANCELED'

def test_sort_by_date() -> None:
    """ Тестируем функцию сортировки даты """
    # Тестовые данные:
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    # Тест: сортировка по убыванию
    result_desc = sort_by_date(test_data)
    assert len(result_desc) == 4
    assert result_desc[0]['date'] == '2019-07-03T18:35:29.512364'
    assert result_desc[1]['date'] == '2018-10-14T08:21:33.419441'
    assert result_desc[2]['date'] == '2018-09-12T21:27:25.241689'
    assert result_desc[3]['date'] == '2018-06-30T02:08:58.425572'

    # Тест: сортировка по возрастанию
    result_asc = sort_by_date(test_data, False)
    assert len(result_asc) == 4
    assert result_asc[0]['date'] == '2018-06-30T02:08:58.425572'
    assert result_asc[1]['date'] == '2018-09-12T21:27:25.241689'
    assert result_asc[2]['date'] == '2018-10-14T08:21:33.419441'
    assert result_asc[3]['date'] == '2019-07-03T18:35:29.512364'



if __name__ == '__main__':
    test_filter_by_state()
    test_sort_by_date()
    print("Все тесты пройдены")



