# Worder

Simple but powerful password-list generator. Combine lists, make lists, alter lists.
Dead simple. Dead powerful.

**Input files:** one word per line. Blank lines and lines starting with `#` are ignored.
**Output:** goes to the screen, or to a file with `-o`.

---

## 1. Join lists — every combination, in order

```bash
python3 Worder.py -i list1.txt -i list2.txt -o output.txt
```
```
tokio1    test1    user1    password1    random1
tokio2    test2    user2    password2    random2
...       (5 words x 5 numbers = 25 lines)
random5
```

```bash
python3 Worder.py -i list1.txt -ch "!" -i list2.txt -o output.txt
```
```
tokio!1
tokio!2
...
```

```bash
python3 Worder.py -i list1.txt -ch "?@" -i list2.txt -o output.txt
```
```
tokio?@1
tokio?@2
...
```

```bash
python3 Worder.py -i list1.txt -ch "abc" -i list2.txt -o output.txt
```
```
tokioabc1
tokioabc2
...
```

```bash
python3 Worder.py -i list1.txt -ch "ABC" -i list2.txt -o output.txt
```
```
tokioABC1
tokioABC2
...
```

```bash
python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o output.txt
```
```
AtokioB1C
AtokioB2C
...
```

### How `-ch` works

Its **position** on the command line decides where the text goes:
- **before** the first `-i` = prefix
- **between** two `-i` = separator
- **after** the last `-i` = suffix

The **whole value** is inserted literally (`-ch "TEST"` -> `decemberTEST2000`).
Repeat `-ch` at the same spot to try several alternatives. Add `--random` to pick
one alternative at random per line instead of trying them all.

```bash
python3 Worder.py -i list1.txt -ch "!" -ch "?" -i list2.txt -o out.txt
# -> tokio!1, tokio?1, tokio!2, tokio?2, ...

python3 Worder.py -i list1.txt -ch "!" -ch "?" -i list2.txt --random -o out.txt
# -> tokio!1, tokio?2, tokio?3, ... (random pick per line)
```

---

## 2. Alter lists — case flags

Case flags apply **only to the `-i` list that follows them**, so each list can
get its own case.

```bash
python3 Worder.py --upper -i list1.txt -o output.txt
```
```
Tokio
Test
User
Password
Random
```

```bash
python3 Worder.py --upper-all -i list1.txt -o output.txt
```
```
TOKIO
TEST
...
```

```bash
python3 Worder.py --lower -i list1.txt -o output.txt
```
```
tokio
test
...
```

```bash
python3 Worder.py --lower-all -i list1.txt -o output.txt
```
```
tokio
test
...
```

Mix them freely:

```bash
python3 Worder.py --upper-all -i months.txt -ch "!" --lower-all -i seasons.txt
```
```
NOVEMBER!spring
NOVEMBER!summer
NOVEMBER!autumn
NOVEMBER!winter
DECEMBER!spring
...
```

---

## 3. Make lists — ready-made word lists

```bash
python3 Worder.py --months -o months.txt
```
```
January
February
...
December
```

```bash
python3 Worder.py --years 2020-2025 -o years.txt
```
```
2020
2021
2022
2023
2024
2025
```

```bash
python3 Worder.py --years 1990-1999,2024 -o years.txt
```
```
1990
1991
...
1999
2024
```

```bash
python3 Worder.py --seasons -o seasons.txt
```
```
Spring
Summer
Autumn
Winter
```

```bash
python3 Worder.py --numbers 0-99 --pad 2 -o numbers.txt
```
```
00
01
...
99
```

Flags can be combined into one bigger list (`--months --seasons --years 2000-2030`).

---

## 4. Full workflow

```bash
python3 Worder.py --years 2020-2025 -o years.txt
python3 Worder.py -i words.txt -i years.txt -o output.txt
```

---

## 5. Make it permanent — use `worder` / `Worder` from anywhere

```bash
mkdir -p ~/.local/bin
cp ~/Worder/Worder.py ~/.local/bin/worder
chmod +x ~/.local/bin/worder
ln -sf ~/.local/bin/worder ~/.local/bin/Worder
grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then, from any directory:

```bash
worder -i list1.txt -i list2.txt -o output.txt
Worder --months -o months.txt
```

If you update the script later, re-copy it:
`cp ~/Worder/Worder.py ~/.local/bin/worder`

---

## 6. All options

```bash
python3 Worder.py --help
```
