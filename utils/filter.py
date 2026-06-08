import re

STANDARD_PATTERNS = [
    "EN 17860",
    "ISO 4210",
    "TBIS 4210",
    "AS NZS 1927",
    "AS 1927",
    "NZS 1927",
    "CNS 366",
    "CNS 15348",
    "CNS 15349",
    "BS EN 14764",
    "BS EN 14765",
    "BS EN 14766",
    "BS EN 14781",
    "BS EN 14782",
    "EN 14764",
    "EN 14765",
    "EN 14766",
    "EN 14781",
    "EN 14782",
    "BS 14764",
    "BS 14765",
    "BS 14766",
    "BS 14781",
    "BS 14782",
    "ISO 8098",
    "DIN 79010",
    "DIN 79009",
    "CNS 14126",
    "JIS D9115",
    "JIS D9207",
    "UL 2849",
    "ANSI CAN UL 2849",
    "ISO 2575",
    "EN 15194",
    "BS EN 15194",
    "BS 15194",
    "DS 15194",
    "DS EN 15194",
    "EN 17404",
    "DS 17404",
    "DS EN 17404",
    "ANSI RESNA WC-1",
    "RESNA WC-1",
    "ANSI WC-1",
    "CNS 19894",
    "CNS 60335",
    "CNS 15562",
    "BS EN ISO 24415-1",
    "ISO 24415-1",
    "EN 24415-1",
    "BS 24415-1",
    "CNS 15192",
    "CNS 15024",
    "CNS 15037",
    "CNS 15191",
    "CNS 13575",
    "CNS 14964",
    "CNS 15628",
    "CNS 14430",
    "CNS 15340",
    "CNS 15420",
    "CNS 3555",
    "CNS 14393",
    "CNS 14889",
    "CNS 14989",
    "CNS 15469",
    "CNS 15508",
    "CNS 31000",
    "CNS 31010",
    "CNS 3765",
    "CNS 11253",
    "CNS 11529",
    "CNS 13494",
    "CNS 14126",
    "CNS 14978",
    "CNS 15331",
    "CNS 17025",
    "ISO 17025",
    "CNS 14165",
    "CNS 15759",
    "CNS 16077",
    "ISO 10535",
    "CNS 17966",
    "ISO 17966",
    "ISO 7176",
    "ISO 11199",
    "CPSA 0073"
]


def _compile_patterns(patterns):
    compiled = []
    for pattern in patterns:
        normalized = pattern.strip()
        if not normalized:
            continue

        normalized = re.escape(normalized)
        normalized = normalized.replace(r"\ ", r"\s+")
        compiled.append(re.compile(rf"\b{normalized}\b", re.IGNORECASE))

    return compiled


STANDARD_REGEX = _compile_patterns(STANDARD_PATTERNS)


def match(text):
    if not text:
        return False

    return any(regex.search(text) for regex in STANDARD_REGEX)
