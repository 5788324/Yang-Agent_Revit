# -*- coding: utf-8 -*-
"""Set YangAgent user nickname and avatar path."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import get_language, get_user_profile, save_user_profile


output = script.get_output()


TEXT = {
    "zh": {
        "title": u"用户设置",
        "nickname_prompt": u"请输入你的简称",
        "avatar_title": u"选择头像图片（可取消）",
        "done": u"用户设置已保存。",
        "nickname": u"简称",
        "avatar": u"头像",
        "cancel": u"已取消。",
        "failed": u"用户设置失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "title": u"User Settings",
        "nickname_prompt": u"Enter your nickname",
        "avatar_title": u"Select avatar image (optional)",
        "done": u"User settings saved.",
        "nickname": u"Nickname",
        "avatar": u"Avatar",
        "cancel": u"Cancelled.",
        "failed": u"User settings failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def main():
    lang = get_language()
    profile = get_user_profile()
    nickname = forms.ask_for_string(
        default=profile.get("nickname") or "",
        prompt=tr(lang, "nickname_prompt"),
        title=tr(lang, "title"),
    )
    if nickname is None:
        forms.alert(tr(lang, "cancel"), title="Yang Agent")
        return

    avatar_path = profile.get("avatar_path") or ""
    picked = forms.pick_file(title=tr(lang, "avatar_title"))
    if picked:
        avatar_path = picked

    save_user_profile(nickname=nickname, avatar_path=avatar_path)

    output.print_md(u"# {0}".format(tr(lang, "title")))
    output.print_md(u"")
    output.print_md(u"- {0}: `{1}`".format(tr(lang, "nickname"), nickname))
    output.print_md(u"- {0}: `{1}`".format(tr(lang, "avatar"), avatar_path))

    forms.alert(tr(lang, "done"), title="Yang Agent")


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# User Settings failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed"] + u"\n\n" + TEXT["en"]["failed"], title="Yang Agent")
