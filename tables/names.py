from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from config import NamesConfig

if TYPE_CHECKING:
    from fontTools.ttLib import TTFont

LOG = logging.getLogger(__name__)


def apply_names_policy(font: TTFont, config: NamesConfig) -> None:
    if config.records:
        update_font_names_from_records(font, config.records)
    elif config.family:
        update_font_family(font, config.family)


def update_font_family(font: TTFont, family: str) -> None:
    postscript = "".join(ch for ch in family if not ch.isspace())
    name_table = font["name"]
    for rec in name_table.names:
        if rec.nameID in {1, 4, 16, 21}:
            rec.string = family
        elif rec.nameID in {2, 17, 22}:
            rec.string = "Regular"
        elif rec.nameID == 6:
            rec.string = postscript
    LOG.debug("Updated family name records to %s", family)


def update_font_names_from_records(font: TTFont, records) -> None:
    name_table = font["name"]
    name_table.names = []

    for record in records:
        if hasattr(record, "name_id"):
            name_id = record.name_id
            platform_id = record.platform_id
            plat_enc_id = record.platform_encoding_id
            lang_id = record.language_id
            value = record.value
        else:
            name_id, platform_id, plat_enc_id, lang_id, value = record
        name_table.setName(value, name_id, platform_id, plat_enc_id, lang_id)

    LOG.debug("Updated name table from explicit records")
