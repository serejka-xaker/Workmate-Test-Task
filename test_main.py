from main import CoffeeReport
import pytest
from unittest.mock import patch
from contextlib import nullcontext as does_not_raise
import csv


class TestCoffeReport:
    @pytest.mark.parametrize("data, res, expectation",[
        (
        [{'student': 'Михаил Павлов', 'coffee_spent': '300'},
         {'student': 'Михаил Павлов', 'coffee_spent': '200'},
         {'student': 'Михаил Павлов', 'coffee_spent': '100'},
         {'student': 'Саша Иванова', 'coffee_spent': '125'},
         {'student': 'Саша Иванова', 'coffee_spent': '50'}],
        [['Михаил Павлов', 200.0], ['Саша Иванова', 87.5]],
        does_not_raise()
    ),
    (
        [], 
        None, 
        pytest.raises(ValueError, match="Нет данных для расчета медианы")
    ),
    (
        [{'student': 'Саша Павлов', 'coffee_spent': '200'},],
        [['Саша Павлов', 200.0]],
        does_not_raise()
    ),
    ])
    def test_get_report_median_coffee(self, data, res, expectation):
        with expectation:
            result = CoffeeReport.get_report_median_coffee(data)
            assert result == res
    

    @pytest.mark.parametrize("file_names, content, expected_res, expectation", [
        (
            ["valid.csv"], 
            [{'student': 'Михаил Павлов', 'coffee_spent': '200'}],
            [{'student': 'Михаил Павлов', 'coffee_spent': '200'}],
            does_not_raise()
        ),
        (
            ["nevalid.csv"], 
            None, 
            None, 
            pytest.raises(FileNotFoundError, match="Файл .*nevalid.csv не найден")
        ),
        (
            [],
            [], 
            [], 
            does_not_raise()
        ),
    ])
    def test_load_data_parametrized(self, tmp_path, file_names, content, expected_res, expectation):
        paths = []
        for name in file_names:
            file_path = tmp_path / name
            paths.append(str(file_path))
            
            if content is not None:
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=["student", "coffee_spent"])
                    writer.writeheader()
                    writer.writerows(content)

        with expectation:
            result = list(CoffeeReport.load_data_from_files(paths))
            if expected_res is not None:
                assert result == expected_res

    @pytest.mark.parametrize("data, headers, expected_substring, expectation", [
        (
            [['Михаил Павлов', 200.0], ['Саша Иванова', 87.5]],
            ['student', 'coffee_spent'],
            "student",  
            does_not_raise()
        ),
        (
            [['Иван Иванов', 500.0]],
            ['student', 'median_coffee'],
            "500", 
            does_not_raise()
        ),
        (
            [], 
            ['student', 'median_coffee'],
            None, 
            pytest.raises(ValueError, match="Нет данных для отображения")
        ),
    ])
    def test_get_print_table(self, data, headers, expected_substring, expectation):
        with expectation:
            result = CoffeeReport.get_print_table(data, headers)
            if expected_substring:
                assert isinstance(result, str)
                assert expected_substring in result
                assert "+" in result or "-" in result 

    @pytest.mark.parametrize("mock_argv, expected_res, expectation", [
        (
            ["main.py", "--files", "1.csv", "2.csv", "--report", "median"],
            (["1.csv", "2.csv"], "median"),
            does_not_raise()
        ),
        (
            ["main.py", "--files", "data.csv"],
            None,
            pytest.raises(ValueError, match="Ошибка в аргументах командной строки|Неверные параметры")
        ),
        (
            ["main.py", "--files", "--report", "median"],
            None,
            pytest.raises(ValueError)
        ),
    ])
    def test_get_cmd_arguments(self, mock_argv, expected_res, expectation):
        with patch("sys.argv", mock_argv):
            with expectation:
                files, report = CoffeeReport.get_cmd_arguments()
                assert (files, report) == expected_res

    @pytest.mark.parametrize("report_name, expected_func, expectation", [
        (
            "median-coffee", 
            CoffeeReport.get_report_median_coffee, 
            does_not_raise()
        ),
        (
            "unknown-report", 
            None, 
            pytest.raises(ValueError, match="Отчет 'unknown-report' отсутствует")
        ),
        (
            "", 
            None, 
            pytest.raises(ValueError)
        ),
    ])
    def test_get_report_function(self, report_name, expected_func, expectation):
        with expectation:
            result = CoffeeReport.get_report_function(report_name)
            assert result == expected_func

