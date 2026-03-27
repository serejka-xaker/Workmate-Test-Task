import argparse
import csv
import sys
from statistics import median
from tabulate import tabulate
from typing import List, Dict, Tuple, Callable, Optional, Union, Iterable
from collections import defaultdict

Row = Dict[str, str]
ReportRow = List[Union[str, float]]

class CoffeeReport:
    @staticmethod
    def get_report_median_coffee(data: Iterable[Row]) -> List[ReportRow]:
        student_spends = defaultdict(list)
        for row in data:
            name = row['student']
            spend = float(row['coffee_spent'])
            student_spends[name].append(spend)
        report_data = [[name, median(spends)] for name, spends in student_spends.items()]
        if not report_data:
            raise ValueError("Нет данных для расчета медианы.")
        return sorted(report_data, key=lambda x: x[1], reverse=True)

    @staticmethod
    def load_data_from_files(file_paths: List[str]) -> Iterable[Row]:
        for path in file_paths:
            try:
                with open(path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        yield row
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл {path} не найден.")

    
    @staticmethod
    def get_print_table(data: List[ReportRow], headers: List[str] = ['student', 'median_coffee'])-> Optional[str]:
        if not data:
            raise ValueError("Нет данных для отображения.")
        return tabulate(data, headers=headers, tablefmt='grid')

    @staticmethod
    def get_cmd_arguments() -> Tuple[List[str], str]:
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument('--files', nargs='+', required=True)
        parser.add_argument('--report', required=True)
        try:
            arguments = parser.parse_args()
            return arguments.files, arguments.report
        except argparse.ArgumentError as e:
            raise ValueError(f"Ошибка в аргументах командной строки: {e}")
        except SystemExit:
            raise ValueError("Неверные параметры командной строки.")

    @classmethod
    def get_report_function(cls, report_name: str) -> Callable[[Iterable[Row]], List[ReportRow]]:
        reports = {
            "median-coffee": cls.get_report_median_coffee,
        }
        report_function = reports.get(report_name)
        if report_function is None:
            raise ValueError(f"Отчет '{report_name}' отсутствует.")
        return report_function


def main():
    try:
        files, report = CoffeeReport.get_cmd_arguments()
        report_func = CoffeeReport.get_report_function(report)
        raw_data = CoffeeReport.load_data_from_files(files)
        data = report_func(raw_data)
        coffee_table = CoffeeReport.get_print_table(data)
        print(coffee_table)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__":
    main()