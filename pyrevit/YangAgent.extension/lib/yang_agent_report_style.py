# -*- coding: utf-8 -*-
"""Helpers for shared themed report styling."""

from __future__ import print_function

from yang_agent_theme import get_theme_definition


def build_intro_block(theme_id, title, note):
    tokens = get_theme_definition(theme_id)["tokens"]
    return (
        u"<div style=\"border-left: 4px solid {accent}; "
        u"background: {surface}; padding: 12px 14px; margin: 8px 0 16px 0;\">"
        u"<div style=\"font-size: 18px; font-weight: 700; color: {accent};\">{title}</div>"
        u"<div style=\"margin-top: 6px; color: {text};\">{note}</div>"
        u"</div>"
    ).format(
        accent=tokens["report_accent"],
        surface=tokens["report_surface"],
        text=tokens["text_secondary"],
        title=title.lstrip("# ").strip(),
        note=note,
    )


def build_status_block(theme_id, heading, lines):
    tokens = get_theme_definition(theme_id)["tokens"]
    body = u"".join([u"<li>{0}</li>".format(line) for line in lines])
    return (
        u"<div style=\"border: 1px solid {border}; border-radius: 6px; "
        u"background: {surface}; padding: 10px 14px; margin: 8px 0 16px 0;\">"
        u"<div style=\"font-weight: 700; color: {accent}; margin-bottom: 6px;\">{heading}</div>"
        u"<ul style=\"margin: 0; padding-left: 18px; color: {text};\">{body}</ul>"
        u"</div>"
    ).format(
        border=tokens["border"],
        surface=tokens["report_surface"],
        accent=tokens["report_accent"],
        text=tokens["text_secondary"],
        heading=heading,
        body=body,
    )
