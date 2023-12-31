import os

from stock_clue.opendart import OpenDart
from stock_clue.opendart.major_report import MajorReport


class TestMajorReport:
    def test_get_capital_increase(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_capital_increase(
            corp_code="00378363", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_capital_decrease(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_capital_decrease(
            corp_code="00121932", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_capital_increase_and_decrease(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_capital_increase_and_decrease(
            corp_code="00359395", bgn_de="20190101", end_de="20210131"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_capital_reduction(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_capital_reduction(
            corp_code="00121932", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_convertible_bond(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_convertible_bond(
            corp_code="00155355", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_bond_with_warrants(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_bond_with_warrants(
            corp_code="00140131", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_exchangeable_bond(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_exchangeable_bond(
            corp_code="00273420", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_disposal_of_treasury_stocks(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_disposal_of_treasury_stocks(
            corp_code="00121932", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0

    def test_get_acquisition_of_treasury_stocks(self):
        major_report = MajorReport(OpenDart(os.environ["OPENDART_API_KEY"]))
        result = major_report.get_acquisition_of_treasury_stocks(
            corp_code="00164742", bgn_de="20190101", end_de="20191231"
        )

        assert result is not None
        assert result.status == "000"
        assert result.message == "정상"
        assert len(result.list) != 0
