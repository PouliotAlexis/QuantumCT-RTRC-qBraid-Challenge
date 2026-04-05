import csv
import os

import pytest

from utils.save_instance_results import save_run_results


class TestSaveInstanceResults:
    @pytest.fixture
    def csv_path(self, tmpdir):
        return str(tmpdir.join("test_data.csv"))

    def test_save_instance_results_creates_file_and_header(self, csv_path):
        assert not os.path.exists(csv_path)
        save_run_results(1, 10, 100, 1.2345, csv_path)

        assert os.path.exists(csv_path)
        with open(csv_path, "r") as f:
            reader = list(csv.reader(f))
            assert len(reader) == 2
            assert reader[0] == [
                "CVRP Instance #",
                "# of Qubits",
                "# of Gate Operations",
                "Execution Time",
            ]
            assert reader[1] == ["1", "10", "100", "1.2345"]

    @pytest.mark.parametrize("runs", [2, 5])
    def test_save_instance_results_appends_data(self, csv_path, runs):
        for i in range(runs):
            save_run_results(i, i * 10, i * 100, i * 1.1, csv_path)

        with open(csv_path, "r") as f:
            reader = list(csv.reader(f))
            assert len(reader) == runs + 1  # 1 header + runs

            for i in range(runs):
                assert reader[i + 1][0] == str(i)
                assert reader[i + 1][1] == str(i * 10)
                assert reader[i + 1][2] == str(i * 100)
                assert reader[i + 1][3] == f"{i*1.1:.4f}"
                assert reader[i + 1][1] == str(i * 10)
                assert reader[i + 1][2] == str(i * 100)
                assert reader[i + 1][3] == f"{i*1.1:.4f}"
