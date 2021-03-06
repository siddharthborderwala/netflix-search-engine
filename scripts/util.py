import re
import unicodedata


def remove_puncts(text):
    if text is None:
        return None
    return re.sub(r"[^\w\s]", '', text)


def store_dict(d, filename):
    with open(filename, 'w', encoding="UTF-8") as f:
        for k, v in d.items():
            f.write(k + ':')
            for i in v:
                f.write("{};".format(i))
            f.write('\n')


def soundex(s):

    if not s:
        return ""

    s = unicodedata.normalize("NFKD", s)
    s = s.upper()

    replacements = (
        ("BFPV", "1"),
        ("CGJKQSXZ", "2"),
        ("DT", "3"),
        ("L", "4"),
        ("MN", "5"),
        ("R", "6"),
    )
    result = [s[0]]
    count = 1

    # find would-be replacment for first character
    for lset, sub in replacements:
        if s[0] in lset:
            last = sub
            break
    else:
        last = None

    for letter in s[1:]:
        for lset, sub in replacements:
            if letter in lset:
                if sub != last:
                    result.append(sub)
                    count += 1
                last = sub
                break
        else:
            if letter != "H" and letter != "W":
                # leave last alone if middle letter is H or W
                last = None
        if count == 4:
            break

    result += "0" * (4 - count)
    return "".join(result)
