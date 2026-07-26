"""
Mapper between Section domain model and SectionORM.
"""

from datetime import datetime
from typing import Dict, Any
from app.models.section import Section
from app.database.orm.section import SectionORM

_SECTION_CACHE: Dict[str, Dict[str, Any]] = {}


class SectionMapper:
    @classmethod
    def cache_domain(cls, domain: Section):
        if not domain:
            return
        data = {
            "section_number": domain.section_number,
            "title": domain.title,
            "is_cognizable": getattr(domain, "is_cognizable", None),
            "is_bailable": getattr(domain, "is_bailable", None),
            "maximum_punishment": getattr(domain, "maximum_punishment", None),
        }
        if domain.section_id:
            _SECTION_CACHE[domain.section_id] = data
        if domain.section_number:
            _SECTION_CACHE[domain.section_number] = data

    @classmethod
    def to_domain(cls, orm: SectionORM) -> Section:
        now = datetime.now()
        cached = _SECTION_CACHE.get(orm.sectioncode) or {}

        sec_no = cached.get("section_number")
        if not sec_no:
            sec_no = orm.sectioncode or ""
            for prefix in ("SEC-IT", "SEC-BNSS", "SEC-BNS", "SEC-NDPS", "SEC-POCSO", "SEC-CrPC", "SEC-"):
                if sec_no.startswith(prefix):
                    sec_no = sec_no[len(prefix):]
                    break

        title = cached.get("title") or orm.sectiondescription or f"Section {orm.sectioncode}"

        return Section(
            section_id=orm.sectioncode,
            act_id=orm.actcode,
            section_number=sec_no,
            title=title,
            description=orm.sectiondescription,
            is_cognizable=cached.get("is_cognizable"),
            is_bailable=cached.get("is_bailable"),
            maximum_punishment=cached.get("maximum_punishment"),
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Section) -> SectionORM:
        cls.cache_domain(domain)
        return SectionORM(
            sectioncode=domain.section_id or domain.section_number,
            actcode=domain.act_id,
            sectiondescription=domain.description or domain.title,
            active=True,
        )
