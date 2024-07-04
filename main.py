import re
from decimal import Decimal, ROUND_HALF_UP

pattern = re.compile(r"(\d{4})\s(\w+)\s(\w+)\s(.+?)\s(\d+\.\d+)\s(\w+)\s(\d+)")

transcript = open("./transcript.txt", "r")
transcript_lines = transcript.readlines()


def print_transcript(transcript_lines):
    print("Your transcript: ")
    for line in transcript_lines:
        if (
            line
            == " Year Session Unit of study code Unit of study name Mark Grade Credit points\n"
        ):
            continue
        print(line, end="")


def round_half_up(number, decimals=1):
    decimal_number = Decimal(str(number))
    format_string = "1." + ("0" * decimals)
    rounded_number = decimal_number.quantize(
        Decimal(format_string), rounding=ROUND_HALF_UP
    )
    return float(rounded_number)


def wam(transcript_lines):
    total_credits = []
    total_marks = []

    for line in transcript_lines:
        line = line.rstrip().strip()
        match = pattern.match(line)

        if not match:
            continue

        year, session, code, name, mark, grade, credits = match.groups()
        # print(year, session, code, name, mark, grade, credits)

        total_credits.append(int(credits))
        total_marks.append(float(mark))

    if len(total_credits) != len(total_marks):
        print("error calculating WAM")
        return

    numerator = 0
    denominator = 0
    for i in range(len(total_credits)):
        numerator += total_credits[i] * total_marks[i]
        denominator += total_credits[i]

    return round_half_up(numerator / denominator, 1)
    pass


def eihwam(transcript_lines):
    """EIHWAM is calculated utilising this formula  EIHWAM=Σ(Wi x CPi x Mi) / Σ(Wi x CPi), from this course page (https://www.sydney.edu.au/handbooks/engineering/engineering_honours/engineering_honours_resolutions.html)"""

    total_weightings = []
    total_credits = []
    total_marks = []

    for line in transcript_lines:
        line = line.rstrip().strip()
        match = pattern.match(line)

        if not match:
            continue

        year, session, code, name, mark, grade, credits = match.groups()
        # print(year, session, code, name, mark, grade, credits)

        code_level = code[4]  # starting number indicates level
        match code_level:
            case "1":  # 0 for 1000 level units
                total_weightings.append(0)
            case "2":  # 2 for 2000 level units
                total_weightings.append(2)
            case "3":  # 3 for 3000 level units
                total_weightings.append(3)
            case _:  # 4 for 4000+ level units
                total_weightings.append(4)

        total_credits.append(int(credits))
        total_marks.append(float(mark))

    if len(total_weightings) != len(total_credits) or len(total_weightings) != len(
        total_marks
    ):
        print("error calculating EIHWAM")
        return

    numerator = 0
    denominator = 0
    for i in range(len(total_weightings)):
        numerator += total_weightings[i] * total_credits[i] * total_marks[i]
        denominator += total_weightings[i] * total_credits[i]

    return round_half_up(numerator / denominator, 1)


# print_transcript(transcript_lines=transcript_lines)
print("EIHWAM:", eihwam(transcript_lines=transcript_lines))
print("WAM", wam(transcript_lines=transcript_lines))
