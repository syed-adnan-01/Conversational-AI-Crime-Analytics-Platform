"""
Mapper between Act domain model and ActORM with year parsing and extension cache.
"""

from datetime import datetime
import re
from typing import Optional, Dict
from app.models.act import Act
from app.database.orm.act import ActORM

_ACT_CACHE: Dict[str, Dict] = {}


class ActMapper:
    @classmethod
    def cache_domain(cls, domain: Act):
        if domain.act_id:
            _ACT_CACHE[domain.act_id] = {
                "year": domain.year,
            }

    @classmethod
    def to_domain(cls, orm: ActORM) -> Act:
        cached = _ACT_CACHE.get(orm.actcode, {})
        year_val = cached.get("year")
        if year_val is None and orm.shortname:
            match = re.search(r"\b(19\d\d|20\d\d)\b", orm.shortname)
            if match:
                year_val = int(match.group(1))
        if year_val is None and orm.actdescription:
            match = re.search(r"\b(19\d\d|20\d\d)\b", orm.actdescription)
            if match:
                year_val = int(match.group(1))
        if year_val is None:
            year_val = 2023

        now = datetime.now()
        return Act(
            act_id=orm.actcode,
            name=orm.actdescription or orm.shortname or orm.actcode,
            short_name=orm.shortname or orm.actcode,
            year=year_val,
            description=orm.actdescription,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Act) -> ActORM:
        cls.cache_domain(domain)
        return ActORM(
            actcode=domain.act_id or domain.short_name,
            actdescription=domain.name or domain.description or domain.short_name,
            shortname=domain.short_name,
            active=True,
        )
