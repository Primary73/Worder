#!/usr/bin/env python3
"""Worder - build word lists and join them into password lists.

Two functions:

1) BUILD LISTS - print ready-made word lists, one entry per line:

   python3 Worder.py --months                      January ... December
   python3 Worder.py --months -o months.txt        save to a file
   python3 Worder.py --seasons                     Spring, Summer, Autumn, Winter
   python3 Worder.py --years 2020-2025             2020, 2021, ... 2025
   python3 Worder.py --years 1990-1999,2024,2025   several ranges / values
   python3 Worder.py --numbers 0-99 --pad 2        00, 01, ... 99
   python3 Worder.py --months --seasons --lower-all  combine several lists
                                                   (order: months, seasons,
                                                    years, numbers)

2) JOIN LISTS - every combination across the input lists, in order:

   python3 Worder.py -i list1.txt -i list2.txt -o output.txt
   python3 Worder.py -i list1.txt -ch "!" -i list2.txt -o output.txt
   python3 Worder.py -i list1.txt -ch "?@" -i list2.txt -o output.txt
   python3 Worder.py -i list1.txt -ch "abc" -i list2.txt -o output.txt
   python3 Worder.py -i list1.txt -ch "ABC" -i list2.txt -o output.txt
   python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o output.txt

   python3 Worder.py --upper -i list1.txt -o output.txt
   python3 Worder.py --upper-all -i list1.txt -o output.txt
   python3 Worder.py --lower -i list1.txt -o output.txt
   python3 Worder.py --lower-all -i list1.txt -o output.txt

   Case flags apply ONLY to the -i list that follows them, so each list
   can get its own case:

   python3 Worder.py --upper-all -i months.txt -ch "!" --lower-all -i seasons.txt
   -> NOVEMBER!spring, NOVEMBER!summer, ...

   -ch position matters: BEFORE the first -i = prefix, BETWEEN two -i =
   separator, AFTER the last -i = suffix. The whole -ch value is inserted
   literally (e.g. -ch "TEST" -> decemberTEST2000). Repeat -ch at the same
   spot to try several alternatives; use --random to pick one of them at
   random per line instead of trying every one.

Input files: one word per line; blank lines and lines starting with '#'
are ignored. Output goes to stdout, or to the file given with -o.
"""

import argparse
import secrets
import sys
from itertools import product
from pathlib import Path

MONTHS_FULL = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]
SEASONS = ["spring", "summer", "autumn", "winter"]


def load_words(path):
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as e:
        sys.exit(f"error: cannot read word list {path}: {e}")
    words = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    if not words:
        sys.exit(f"error: word list {path} is empty")
    return words


def expand_ranges(spec):
    """'1990-1999,2020' -> ['1990', ..., '1999', '2020']."""
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                a, b = part.split("-", 1)
                a, b = int(a), int(b)
            except ValueError:
                sys.exit(f"error: bad range '{part}' (expected N-M)")
            if a > b:
                sys.exit(f"error: bad range '{part}' (start > end)")
            out.extend(str(v) for v in range(a, b + 1))
        else:
            out.append(part)
    return out


def apply_case(word, case):
    if case == "upper":
        return word[:1].upper() + word[1:]
    if case == "upper-all":
        return word.upper()
    if case == "lower":
        return word[:1].lower() + word[1:]
    if case == "lower-all":
        return word.lower()
    return word


class SeqOption(argparse.Action):
    """Record -i / -ch options in the exact order they appear on the line."""

    def __call__(self, parser, namespace, values, option_string=None):
        seq = getattr(namespace, "seq", None)
        if seq is None:
            seq = namespace.seq = []
        seq.append((self.dest, values if values else self.const))


def build_lists(args, emit):
    entries = []
    if args.months:
        entries += list(MONTHS_FULL)
    if args.seasons:
        entries += list(SEASONS)
    if args.years:
        entries += expand_ranges(args.years)
    if args.numbers:
        entries += expand_ranges(args.numbers)
    if args.pad:
        entries = [e.zfill(args.pad) if e.isdigit() else e for e in entries]
    case = args.case if args.case else "upper"
    entries = [apply_case(e, case) for e in entries]
    if not entries:
        sys.exit("error: nothing to build")
    for e in entries:
        emit(e)


def join_lists(word_lists, positions, args, emit):
    total = 1
    for lst in word_lists:
        total *= len(lst)
    print(f"# {total} combinations", file=sys.stderr)

    def assemble(combo, chars):
        line = chars[0]
        for k, w in enumerate(combo):
            line += w + chars[k + 1]
        return line

    if args.random:
        for combo in product(*word_lists):
            chars = [secrets.choice(p) if p else "" for p in positions]
            emit(assemble(combo, chars))
    else:
        cands = [p if p else [""] for p in positions]
        for combo in product(*word_lists):
            for chars in product(*cands):
                emit(assemble(combo, chars))


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Worder: build word lists (months/seasons/years/numbers) "
                    "and join your own lists into every combination.",
        epilog="examples:\n"
               "  python3 Worder.py -i list1.txt -i list2.txt -o output.txt\n"
               '  python3 Worder.py -i list1.txt -ch "!" -i list2.txt -o output.txt\n'
               '  python3 Worder.py -i list1.txt -ch "?@" -i list2.txt -o output.txt\n'
               '  python3 Worder.py -i list1.txt -ch "abc" -i list2.txt -o output.txt\n'
               '  python3 Worder.py -i list1.txt -ch "ABC" -i list2.txt -o output.txt\n'
               '  python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o output.txt\n'
               "\n"
               "  python3 Worder.py --upper -i list1.txt -o output.txt\n"
               "  python3 Worder.py --upper-all -i list1.txt -o output.txt\n"
               "  python3 Worder.py --lower -i list1.txt -o output.txt\n"
               "  python3 Worder.py --lower-all -i list1.txt -o output.txt\n"
               '  python3 Worder.py --upper-all -i Months.txt -ch "!" --lower -i Seasons.txt\n'
               "\n"
               "  python3 Worder.py --months -o months.txt\n"
               "  python3 Worder.py --years 2020-2025 -o years.txt\n"
               "  python3 Worder.py --seasons -o seasons.txt\n"
               "  python3 Worder.py --numbers 0-99 --pad 2 -o numbers.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    j = p.add_argument_group("join mode")
    j.add_argument("-i", "--input", action=SeqOption, dest="file", metavar="FILE",
                   help="input word list; use several -i, one per list, in order")
    j.add_argument("-ch", "--chars", action=SeqOption, dest="ch", metavar="STRING",
                   help='string to insert here, literally: before the first -i '
                        '(prefix), between two -i (separator) or after the last -i '
                        '(suffix); repeat -ch at the same spot to try several '
                        'alternatives (unless --random is used)')
    j.add_argument("--random", action="store_true",
                   help="pick one -ch character at random per line instead of "
                        "trying every variant")
    j.add_argument("--upper", action=SeqOption, dest="case", const="upper", nargs=0,
                   help="capitalize first letters; applies ONLY to the -i list "
                        "that follows it")
    j.add_argument("--upper-all", action=SeqOption, dest="case", const="upper-all",
                   nargs=0, help="ALL CAPS; applies ONLY to the -i list that follows it")
    j.add_argument("--lower", action=SeqOption, dest="case", const="lower", nargs=0,
                   help="lowercase first letters; applies ONLY to the -i list "
                        "that follows it")
    j.add_argument("--lower-all", action=SeqOption, dest="case", const="lower-all",
                   nargs=0, help="all lowercase; applies ONLY to the -i list that follows it")

    b = p.add_argument_group("build mode",
                             "print a word list (one entry per line) instead of joining")
    b.add_argument("--months", action="store_true",
                   help="build month list: January, February, ...")
    b.add_argument("--seasons", action="store_true",
                   help="build season list: Spring, Summer, Autumn, Winter")
    b.add_argument("--years", metavar="SPEC",
                   help="build years, e.g. --years 2020-2025 or 1990-1999,2020")
    b.add_argument("--numbers", metavar="SPEC",
                   help="build numbers, e.g. --numbers 0-99 or 1,2,3")
    b.add_argument("--pad", type=int, default=0, metavar="N",
                   help="zero-pad built numbers/years to N digits (e.g. --pad 2 -> 07)")

    p.add_argument("-o", "--output", type=Path, metavar="FILE",
                   help="write results to FILE instead of stdout")

    args = p.parse_args(argv)
    seq = getattr(args, "seq", None) or []

    builder = bool(args.months or args.seasons or args.years or args.numbers)
    if builder and any(t == "file" for t, _ in seq):
        p.error("build options (--months/--seasons/--years/--numbers) "
                "cannot be combined with -i")
    if builder:
        cases = [v for t, v in seq if t == "case"]
        args.case = cases[-1] if cases else None
        args.files, args.file_cases, args.positions = [], [], []
        return args

    files, file_cases, positions = [], [], [[]]
    pending_case = None
    for t, v in seq:
        if t == "case":
            pending_case = v
        elif t == "file":
            files.append(v)
            file_cases.append(pending_case)
            pending_case = None
            positions.append([])
        else:
            positions[-1].append(v)
    if pending_case is not None:
        p.error("--upper/--upper-all/--lower/--lower-all must be followed "
                "by an -i list")
    args.files, args.file_cases, args.positions = files, file_cases, positions
    if not args.files:
        p.error("nothing to do: give -i lists to join, or build lists "
                "with --months/--seasons/--years/--numbers")
    if args.random and not any(args.positions):
        p.error("--random needs at least one -ch")
    return args


def main(argv=None):
    args = parse_args(argv)
    fout = open(args.output, "w", encoding="utf-8", newline="\n") if args.output else None

    def emit(line):
        if fout:
            fout.write(line + "\n")
        else:
            print(line)

    try:
        if args.months or args.seasons or args.years or args.numbers:
            build_lists(args, emit)
        else:
            lists = []
            for f, case in zip(args.files, args.file_cases):
                words = load_words(f)
                if case:
                    words = [apply_case(w, case) for w in words]
                lists.append(words)
            join_lists(lists, args.positions, args, emit)
    finally:
        if fout:
            fout.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
