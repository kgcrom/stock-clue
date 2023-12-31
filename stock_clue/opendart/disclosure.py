"""공시정보 OpenDart 연동 Module"""
import logging
import tempfile
from typing import TYPE_CHECKING, Any, Dict, List, Optional
import zipfile

from xmlschema import XMLSchema

from stock_clue.error import HttpError
from stock_clue.opendart.disclosure_dto import CompanyOverviewOutputDto
from stock_clue.opendart.disclosure_dto import CorpCodeDto
from stock_clue.opendart.disclosure_dto import DisclosureSearchResultDto
from stock_clue.opendart.disclosure_dto import ListInputDto
from stock_clue.opendart.disclosure_dto import ListOutputDto
from stock_clue.opendart.request import Request
from stock_clue.opendart.utils import extract_file_name

if TYPE_CHECKING:
    from stock_clue.opendart import OpenDart


def unzip(tmp_path: str, file_name: str):
    """
    Unzips a file located at tmp_path with the given file_name.

    Args:
    - tmp_path (str): The path where the file is located.
    - file_name (str): The name of the file to be unzipped.
    """
    with zipfile.ZipFile(f"{tmp_path}/{file_name}") as z:
        z.extractall(path=tmp_path)


class Disclosure:
    def __init__(self, open_dart: "OpenDart"):
        self.request = Request(open_dart.api_key, open_dart.timeout)

    def list(
        self, input_dto: ListInputDto
    ) -> Optional[DisclosureSearchResultDto]:
        """
        공시검색 조회

        Args:
            input_dto (ListInputDto): 공시검색 조회를 위한 Input dto 클래스

        Returns:
            Optional[DisclosureSearchResultDto]: 공시검색 정보 조회 결과를 담는 dto 클래스
        """
        path = "/api/list.json"
        response = self.request.get(path, input_dto.dict())
        # TODO status, message 까지 포함한 클래스 리턴하도록
        # TODO python generic 이용 가능?
        #   - https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb

        if response.status_code != 200:
            raise HttpError()

        data = response.json()

        # TODO status error message와 응답 정보 로깅
        # TODO open dart 오류는 별도 class가 관리
        if data["status"] != "000":
            logging.error(
                "status: %s , message: %s", data["status"], data["message"]
            )
            return None

        def _mapping(x: Dict[str, str]) -> ListOutputDto:
            return ListOutputDto(
                corp_cls=x["corp_cls"],
                corp_name=x["corp_name"],
                corp_code=x["corp_code"],
                stock_code=x["stock_code"],
                report_nm=x["report_nm"],
                rcept_no=x["rcept_no"],
                flr_nm=x["flr_nm"],
                rcept_dt=x["rcept_dt"],
                rm=x["rm"],
            )

        return DisclosureSearchResultDto(
            status=data["status"],
            message=data["message"],
            page_no=data["page_no"],
            page_count=data["page_count"],
            total_count=data["total_count"],
            total_page=data["total_page"],
            list=list(map(_mapping, data["list"])),
        )

    def get_company_overview(
        self, corp_code: str
    ) -> Optional[CompanyOverviewOutputDto]:
        """
        기업개황 조회

        Args:
            corp_code (str): 기업개황 조회 할 corp code

        Returns:
            Optional[CompanyOverviewOutputDto]: 기업개황 조회 결과를 담는 dto 클래스
        """
        path = "/api/company.json"
        response = self.request.get(path, {"corp_code": corp_code})

        if response.status_code != 200:
            raise HttpError()

        data = response.json()

        if data["status"] != "000":
            logging.error(
                "status: %s, message %s", data["status"], data["message"]
            )
            return None

        return CompanyOverviewOutputDto(
            status=data["status"],
            message=data["message"],
            corp_name=data["corp_name"],
            corp_name_eng=data["corp_name_eng"],
            stock_name=data["stock_name"],
            stock_code=data["stock_code"],
            ceo_nm=data["ceo_nm"],
            corp_cls=data["corp_cls"],
            jurir_no=data["jurir_no"],
            bizr_no=data["bizr_no"],
            adres=data["adres"],
            hm_url=data["hm_url"],
            ir_url=data["ir_url"],
            phn_no=data["phn_no"],
            fax_no=data["fax_no"],
            induty_code=data["induty_code"],
            est_dt=data["est_dt"],
            acc_mt=data["acc_mt"],
        )

    def download_document(self, rcept_no: str, file_path: str):
        """
        공시서류원본 파일 조회

        Args:
            rcept_no (str): 공시 서류 접수번호
            file_path (str): 공시서류원본 파일 저장 경로

        Returns:
            None
        """
        if file_path is None:
            raise KeyError()

        path = "/api/document.xml"
        file_path = file_path
        response = self.request.get(path, {"rcept_no": rcept_no}, True)

        if response.status_code != 200:
            raise HttpError()

        file_name = extract_file_name(response)

        # TODO return값으로 적당한 것 고민하고 수정
        with open(f"{file_path}/{file_name}", mode="wb") as w:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                w.write(chunk)

    def get_corp_code_list(self) -> List[CorpCodeDto]:
        """
        고유번호 조회

        Returns:
            List[CorpCodeDto]: 고유번호 조회 결과를 담는 dto 클래스
        """
        path = "/api/corpCode.xml"

        response = self.request.get(path, is_stream=True)

        if response.status_code != 200:
            raise HttpError()

        file_name = extract_file_name(response)

        with tempfile.TemporaryDirectory() as tmp_path:
            file_full_path = f"{tmp_path}/{file_name}"
            with open(file_full_path, mode="wb") as w:
                for chunk in response.iter_content(chunk_size=10 * 1024):
                    w.write(chunk)

            unzip(tmp_path, file_name)

            xml_schema = XMLSchema(
                """
            <xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
              <xs:element name="result">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element maxOccurs="unbounded" name="list">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element name="corp_code" type="xs:string" />
                          <xs:element name="corp_name" type="xs:string" />
                          <xs:element name="stock_code" type="xs:string" />
                          <xs:element name="modify_date" type="xs:string" />
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:schema>
             """
            )
            data: Any = xml_schema.decode(f"{tmp_path}/CORPCODE.xml")

            return list(
                map(
                    lambda x: CorpCodeDto(
                        corp_code=x["corp_code"],
                        corp_name=x["corp_name"],
                        stock_code=x["stock_code"]
                        if len(x["stock_code"]) == 6
                        else None,
                        modify_date=x["modify_date"],
                    ),
                    data["list"],
                )
            )
