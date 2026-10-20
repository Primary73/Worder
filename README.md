# Worder

Simple but powerful password-list generator. Combine lists, make lists, alter lists.

Input files: one word per line. Output: screen or file with `-o`.

## Join lists (every combination, in order)

```bash
python3 Worder.py -i list1.txt -i list2.txt -o output.txt
# tokio1, tokio2, ... test1, ... (every combination)

python3 Worder.py -i list1.txt -ch "!" -i list2.txt -o output.txt
# tokio!1, tokio!2, ...

python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o output.txt
# AtokioB1C, AtokioB2C, ...
```

`-ch` position = prefix (before first `-i`) / separator (between `-i`) / suffix (after last `-i`).
Value is inserted literally. Repeat `-ch` for alternatives, add `--random` to pick one per line:

```bash
python3 Worder.py -i list1.txt -ch "!" -ch "?" -i list2.txt -o output.txt
# tokio!1, tokio?1, tokio!2, tokio?2, ...
```

## Alter lists (case flags apply only to the next `-i`)

```bash
python3 Worder.py --upper-all -i months.txt -ch "!" --lower-all -i seasons.txt
# NOVEMBER!spring, NOVEMBER!summer, ...
```

`--upper` = Tokio | `--upper-all` = TOKIO | `--lower` = tokio | `--lower-all` = tokio

## Make lists

```bash
python3 Worder.py --months -o months.txt          # January ... December
python3 Worder.py --seasons -o seasons.txt        # Spring, Summer, Autumn, Winter
python3 Worder.py --years 2020-2025 -o years.txt  # 2020 ... 2025
python3 Worder.py --numbers 0-99 --pad 2 -o nums.txt  # 00 ... 99
```

## Typical workflow

```bash
python3 Worder.py --years 2020-2025 -o years.txt
python3 Worder.py -i words.txt -i years.txt -o output.txt
```

## Install permanently (Ubuntu)

```bash
mkdir -p ~/.local/bin
cp ~/Worder/Worder.py ~/.local/bin/worder
chmod +x ~/.local/bin/worder
ln -sf ~/.local/bin/worder ~/.local/bin/Worder
grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then from anywhere: `worder -i list1.txt -i list2.txt -o output.txt`

All options: `python3 Worder.py --help`
