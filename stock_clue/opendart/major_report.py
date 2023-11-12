from typing import Dict

from stock_clue.error import HttpError
from stock_clue.opendart.base_dto import BaseListDto
from stock_clue.opendart.base_dto import BaseParamDto
from stock_clue.opendart.major_report_dto import (
    AcquisitionOfTreasuryStocksOutputDto,
)
from stock_clue.opendart.major_report_dto import (
    CapitalIncreaseAndDecreaseOutputDto,
)
from stock_clue.opendart.major_report_dto import (
    DisposalOfTreasuryStocksOutputDto,
)
from stock_clue.opendart.major_report_dto import BondWithWarrantsOutputDto
from stock_clue.opendart.major_report_dto import CapitalIncreaseOutputDto
from stock_clue.opendart.major_report_dto import CapitalReductionOutputDto
from stock_clue.opendart.major_report_dto import CaptitalDecreaseOutputDto
from stock_clue.opendart.major_report_dto import ConvertibleBondOutputDto
from stock_clue.opendart.major_report_dto import ExchangeableBondOutputDto
from stock_clue.opendart.open_dart import OpenDart
from stock_clue.opendart.utils import str_to_float
from stock_clue.opendart.utils import str_to_int


class MajorReport:
    def __init__(self, open_dart: OpenDart):
        super().__init__()
        self.open_dart = open_dart
    
    def get_capital_increase(
        self, corp_code: str, bgn_de: str, end_de: str
    ) -> BaseListDto[CapitalIncreaseOutputDto]:
        """
        유상증자 결정 공시 조회

        Args:
            corp_code (str): The corporation code to retrieve capital increase information for.
            bgn_de (str): The start date of the period to retrieve capital increase information for in the format of YYYYMMDD.
            end_de (str): The end date of the period to retrieve capital increase information for in the format of YYYYMMDD.

        Returns:
            BaseListDto[CapitalIncrease]: A list of CapitalIncrease objects containing the retrieved information.
        """
        path = "/api/piicDecsn.json"
        params = BaseParamDto(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de)
        
        response = self.open_dart.get(path=path, params=params.dict())
        if response.status_code != 200:
            raise HttpError(path)
        
        def _mapping(x: Dict[str, str]) -> CapitalIncreaseOutputDto:
            return CapitalIncreaseOutputDto(
                rcept_no=x["rcept_no"],
                corp_cls=x["corp_cls"],
                corp_code=x["corp_code"],
                corp_name=x["corp_name"],
                nstk_ostk_cnt=str_to_int(x["nstk_ostk_cnt"]),
                nstk_estk_cnt=str_to_int(x["nstk_estk_cnt"]),
                fv_ps=str_to_int(x["fv_ps"]),
                bfic_tisstk_ostk=str_to_int(x["bfic_tisstk_ostk"]),
                bfic_tisstk_estk=str_to_int(x["bfic_tisstk_estk"]),
                fdpp_fclt=str_to_int(x["fdpp_fclt"]),
                fdpp_bsninh=str_to_int(x["fdpp_bsninh"]),
                fdpp_op=str_to_int(x["fdpp_op"]),
                fdpp_dtrp=str_to_int(x["fdpp_dtrp"]),
                fdpp_ocsa=str_to_int(x["fdpp_ocsa"]),
                fdpp_etc=str_to_int(x["fdpp_etc"]),
                ic_mthn=x["ic_mthn"],
                ssl_at=x["ssl_at"],
                ssl_bgd=x["ssl_bgd"],
                ssl_edd=x["ssl_edd"],
            )
        
        data = response.json()
        
        return BaseListDto[CapitalIncreaseOutputDto](
            status=data["status"],
            message=data["message"],
            list=[_mapping(x) for x in data["list"]],
        )
    
    def get_capital_decrease(
        self, corp_code: str, bgn_de: str, end_de: str
    ) -> BaseListDto[CaptitalDecreaseOutputDto]:
        path = "/api/fricDecsn.json"
        params = BaseParamDto(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de)
        
        response = self.open_dart.get(path=path, params=params.dict())
        if response.status_code != 200:
            raise HttpError(path)
        
        def _mapping(x: Dict[str, str]) -> CaptitalDecreaseOutputDto:
            return CaptitalDecreaseOutputDto(
                rcept_no=x["rcept_no"],
                corp_cls=x["corp_cls"],
                corp_code=x["corp_code"],
                corp_name=x["corp_name"],
                nstk_ostk_cnt=str_to_int(x["nstk_ostk_cnt"]),
                nstk_estk_cnt=str_to_int(x["nstk_estk_cnt"]),
                fv_ps=str_to_int(x["fv_ps"]),
                bfic_tisstk_ostk=str_to_int(x["bfic_tisstk_ostk"]),
                bfic_tisstk_estk=str_to_int(x["bfic_tisstk_estk"]),
                nstk_asstd=x["nstk_asstd"],
                nstk_ascnt_ps_ostk=str_to_float(x["nstk_ascnt_ps_ostk"]),
                nstk_ascnt_ps_estk=str_to_float(x["nstk_ascnt_ps_estk"]),
                nstk_dividrk=x["nstk_dividrk"],
                nstk_dlprd=x["nstk_dlprd"],
                nstk_lstprd=x["nstk_lstprd"],
                bddd=x["bddd"],
                od_a_at_t=str_to_int(x["od_a_at_t"]),
                od_a_at_b=str_to_int(x["od_a_at_b"]),
                adt_a_atn=x["adt_a_atn"],
            )
        
        data = response.json()
        
        return BaseListDto[CaptitalDecreaseOutputDto](
            status=data["status"],
            message=data["message"],
            list=[_mapping(x) for x in data["list"]],
        )
    
    def get_capital_increase_and_decrease(
        self, corp_code: str, bgn_de: str, end_de: str
    ) -> BaseListDto[CapitalIncreaseAndDecreaseOutputDto]:
        path = "/api/pifricDecsn.json"
        params = BaseParamDto(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de)
        
        response = self.open_dart.get(path=path, params=params.dict())
        if response.status_code != 200:
            raise HttpError(path)
        
        def _mapping(x: Dict[str, str]) -> CapitalIncreaseAndDecreaseOutputDto:
            return CapitalIncreaseAndDecreaseOutputDto(
                rcept_no=x["rcept_no"],
                corp_cls=x["corp_cls"],
                corp_code=x["corp_code"],
                corp_name=x["corp_name"],
                piic_nstk_ostk_cnt=str_to_int(x["piic_nstk_ostk_cnt"]),
                piic_nstk_estk_cnt=str_to_int(x["piic_nstk_estk_cnt"]),
                piic_fv_ps=str_to_int(x["piic_fv_ps"]),
                piic_bfic_tisstk_ostk=str_to_int(x["piic_bfic_tisstk_ostk"]),
                piic_bfic_tisstk_estk=str_to_int(x["piic_bfic_tisstk_estk"]),
                piic_fdpp_fclt=str_to_int(x["piic_fdpp_fclt"]),
                piic_fdpp_bsninh=str_to_int(x["piic_fdpp_bsninh"]) if x["piic_fdpp_bsninh"] else None,
                piic_fdpp_op=str_to_int(x["piic_fdpp_op"]),
                piic_fdpp_dtrp=str_to_int(x["piic_fdpp_dtrp"]) if x["piic_fdpp_dtrp"] else None,
                piic_fdpp_ocsa=str_to_int(x["piic_fdpp_ocsa"]),
                piic_fdpp_etc=str_to_int(x["piic_fdpp_etc"]),
                piic_ic_mthn=x["piic_ic_mthn"],
                fric_nstk_ostk_cnt=str_to_int(x["fric_nstk_ostk_cnt"]),
                fric_nstk_estk_cnt=str_to_int(x["fric_nstk_estk_cnt"]),
                fric_fv_ps=str_to_int(x["fric_fv_ps"]),
                fric_bfic_tisstk_ostk=str_to_int(x["fric_bfic_tisstk_ostk"]),
                fric_bfic_tisstk_estk=str_to_int(x["fric_bfic_tisstk_estk"]),
                fric_nstk_asstd=x["fric_nstk_asstd"],
                fric_nstk_ascnt_ps_ostk=str_to_float(x["fric_nstk_ascnt_ps_ostk"]),
                fric_nstk_ascnt_ps_estk=str_to_float(x["fric_nstk_ascnt_ps_estk"]),
                fric_nstk_dividrk=x["fric_nstk_dividrk"],
                fric_nstk_dlprd=x["fric_nstk_dlprd"],
                fric_nstk_lstprd=x["fric_nstk_lstprd"],
                fric_bddd=x["fric_bddd"],
                fric_od_a_at_t=str_to_int(x["fric_od_a_at_t"]),
                fric_od_a_at_b=str_to_int(x["fric_od_a_at_b"]),
                fric_adt_a_atn=x["fric_adt_a_atn"],
                ssl_at=x["ssl_at"],
                ssl_bgd=x["ssl_bgd"],
                ssl_edd=x["ssl_edd"],
            )
        
        data = response.json()
        
        return BaseListDto[CapitalIncreaseAndDecreaseOutputDto](
            status=data["status"],
            message=data["message"],
            list=[_mapping(x) for x in data["list"]],
        )
    
    def get_capital_reduction(self, corp_code: str, bgn_de: str, end_de: str) -> BaseListDto[CapitalReductionOutputDto]:
        path = "/api/crDecsn.json"
        
        params = BaseParamDto(
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de
        )
        
        response = self.open_dart.get(path=path, params=params.dict())
        if response.status_code != 200:
            raise HttpError(path)
        
        def _mapping(x: Dict[str, str]) -> CapitalReductionOutputDto:
            return CapitalReductionOutputDto(
                rcept_no=x["rcept_no"],
                corp_cls=x["corp_cls"],
                corp_code=x["corp_code"],
                corp_name=x["corp_name"],
                crstk_ostk_cnt=str_to_int(x["crstk_ostk_cnt"]),
                crstk_estk_cnt=str_to_int(x["crstk_estk_cnt"]),
                fv_ps=str_to_int(x["fv_ps"]),
                bfcr_cpt=str_to_int(x["bfcr_cpt"]),
                atcr_cpt=str_to_int(x["atcr_cpt"]),
                bfcr_tisstk_ostk=str_to_int(x["bfcr_tisstk_ostk"]),
                atcr_tisstk_ostk=str_to_int(x["atcr_tisstk_ostk"]),
                bfcr_tisstk_estk=str_to_int(x["bfcr_tisstk_estk"]),
                atcr_tisstk_estk=str_to_int(x["atcr_tisstk_estk"]),
                cr_rt_ostk=x["cr_rt_ostk"],
                cr_rt_estk=x["cr_rt_estk"],
                cr_std=x["cr_std"],
                cr_mth=x["cr_mth"],
                cr_rs=x["cr_rs"],
                crsc_gmtsck_prd=x["crsc_gmtsck_prd"],
                crsc_trnmsppd=x["crsc_trnmsppd"],
                crsc_osprpd=x["crsc_osprpd"],
                crsc_trspprpd=x["crsc_trspprpd"],
                crsc_osprpd_bgd=x["crsc_osprpd_bgd"],
                crsc_osprpd_edd=x["crsc_osprpd_edd"],
                crsc_trspprpd_bgd=x["crsc_trspprpd_bgd"],
                crsc_trspprpd_edd=x["crsc_trspprpd_edd"],
                crsc_nstkdlprd=x["crsc_nstkdlprd"],
                crsc_nstklstprd=x["crsc_nstklstprd"],
                cdobprpd_bgd=x["cdobprpd_bgd"],
                cdobprpd_edd=x["cdobprpd_edd"],
                ospr_nstkdl_pl=x["ospr_nstkdl_pl"],
                bddd=x["bddd"],
                od_a_at_t=str_to_int(x["od_a_at_t"]),
                od_a_at_b=str_to_int(x["od_a_at_b"]),
                adt_a_atn=x["adt_a_atn"],
                ftc_stt_atn=x["ftc_stt_atn"],
            )
        
        data = response.json()
        
        return BaseListDto[CapitalReductionOutputDto](
            status=data["status"],
            message=data["message"],
            list=[_mapping(x) for x in data["list"]],
        )
    
    def get_convertible_bond(self) -> BaseListDto[ConvertibleBondOutputDto]:
        pass
    
    def get_bond_with_warrants(self) -> BaseListDto[BondWithWarrantsOutputDto]:
        pass
    
    def get_exchangeable_bond(self) -> BaseListDto[ExchangeableBondOutputDto]:
        pass
    
    def get_disposal_of_treasury_stocks(
        self,
    ) -> BaseListDto[DisposalOfTreasuryStocksOutputDto]:
        pass
    
    def get_acquisition_of_treasury_stocks(
        self,
    ) -> BaseListDto[AcquisitionOfTreasuryStocksOutputDto]:
        pass
