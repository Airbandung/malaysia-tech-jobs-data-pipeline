import re
from enrichment.constant import SKILL_ALIASES


def extract_skills_from_text(text):

    if not text:
        return []

    text = text.lower()

    found = set()

    for keyword, skill_name in SKILL_ALIASES.items():

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found.add(skill_name)

    return list(found)