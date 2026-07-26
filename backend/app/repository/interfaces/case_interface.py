"""
Interface for CaseRepository.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.models.case_master import CaseMaster
from app.common.queries.case_query import CaseQueryOptions


class ICaseRepository(ABC):
    @classmethod
    @abstractmethod
    def create_case(cls, case: CaseMaster) -> CaseMaster:
        pass

    @classmethod
    @abstractmethod
    def get_case_by_id(cls, case_master_id: str) -> Optional[CaseMaster]:
        pass

    @classmethod
    @abstractmethod
    def get_case_by_case_number(cls, case_no: str) -> Optional[CaseMaster]:
        pass

    @classmethod
    @abstractmethod
    def get_case_by_crime_number(cls, crime_no: str) -> Optional[CaseMaster]:
        pass

    @classmethod
    @abstractmethod
    def get_all_cases(cls) -> list[CaseMaster]:
        pass

    @classmethod
    @abstractmethod
    def update_case(cls, case: CaseMaster) -> Optional[CaseMaster]:
        pass

    @classmethod
    @abstractmethod
    def delete_case(cls, case_master_id: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def case_exists(cls, case_master_id: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def query_cases(cls, options: CaseQueryOptions) -> tuple[list[CaseMaster], int]:
        pass
