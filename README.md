# Worder

Makes word lists and combines them into password lists.

The idea is simple:
- **Make lists** (`--months`, `--years`, ...) or use your own text files (one word per line)
- **Combine them** with `-i` - you get every combination of all lists
- **Add characters** with `-ch` — before, between or after the words
- **Change case** with `--upper` / `--lower` - per list, however you want

Everything goes to the screen, or to a file with `-o`.

---

## Examples

Join two lists (every combination, in order):

```bash
python3 Worder.py -i list1.txt -i list2.txt -o output.txt
# tokio1, tokio2, ... test1, test2, ...
```

`-ch` puts characters where you place it:
- before the first `-i` = in front
- between two `-i` = in between
- after the last `-i` = at the end

```bash
python3 Worder.py -i list1.txt -ch "!" -i list2.txt -o output.txt
# tokio!1, tokio!2, ...

python3 Worder.py -i list1.txt -ch "?@" -i list2.txt -o output.txt
# tokio?@1, tokio?@2, ...

python3 Worder.py -i list1.txt -ch "abc" -i list2.txt -o output.txt
# tokioabc1, tokioabc2, ...

python3 Worder.py -i list1.txt -ch "ABC" -i list2.txt -o output.txt
# tokioABC1, tokioABC2, ...

python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o output.txt
# AtokioB1C, AtokioB2C, ...
```

Case flags (`--upper`, `--upper-all`, `--lower`, `--lower-all`) change only the
`-i` list that comes right after them - so every list can look different:

```bash
python3 Worder.py --upper -i list1.txt -o output.txt
# Tokio, Test, User, ...

python3 Worder.py --upper-all -i list1.txt -o output.txt
# TOKIO, TEST, USER, ...

python3 Worder.py --lower -i list1.txt -o output.txt
# tokio, test, user, ...

python3 Worder.py --lower-all -i list1.txt -o output.txt
# tokio, test, user, ...
```

Mix everything together - case, characters, as many lists as you want:

```bash
python3 Worder.py --upper-all -i Months.txt -ch "!" --lower -i Seasons.txt
# NOVEMBER!spring, NOVEMBER!summer, ... DECEMBER!winter
```

Worder can also create lists for you (save them, then reuse with `-i`):

```bash
python3 Worder.py --months -o months.txt
# January, February, ... December

python3 Worder.py --years 2020-2025 -o years.txt
# 2020, 2021, 2022, 2023, 2024, 2025

python3 Worder.py --seasons -o seasons.txt
# Spring, Summer, Autumn, Winter

python3 Worder.py --numbers 0-99 --pad 2 -o numbers.txt
# 00, 01, 02, ... 99
```

---

## Install permanently (Ubuntu) - use `worder` from anywhere

```bash
mkdir -p ~/.local/bin
cp ~/Worder/Worder.py ~/.local/bin/worder
chmod +x ~/.local/bin/worder
ln -sf ~/.local/bin/worder ~/.local/bin/Worder
grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

```bash
worder -i list1.txt -i list2.txt -o output.txt
```

## All options

```bash
python3 Worder.py --help
```
