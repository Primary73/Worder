# Worder
Simple but powerful Password-list Generator, Combine lists, Make lists, Alter lists. Dead simple, Dead powerful.

# Worder

Build word lists and join them into password lists.

## Build lists

```bash
python3 Worder.py --months -o months.txt        # January ... December
python3 Worder.py --seasons -o seasons.txt      # Spring, Summer, Autumn, Winter
python3 Worder.py --years 2020-2025 -o years.txt
python3 Worder.py --years 1990-1999,2024 -o years.txt
python3 Worder.py --numbers 0-99 --pad 2 -o numbers.txt   # 00 ... 99
```

## Join lists (every combination, in order)

```bash
python3 Worder.py -i list1.txt -i list2.txt -o output.txt
python3 Worder.py -i list1.txt -ch "TEST" -i list2.txt -o output.txt
```

`-ch` position matters:
- **before** first `-i` = prefix
- **between** two `-i` = separator
- **after** last `-i` = suffix

The whole `-ch` value is inserted literally. Repeat `-ch` at the same spot to try several alternatives. Add `--random` to pick one at random per line.

```bash
python3 Worder.py -ch "A" -i list1.txt -ch "B" -i list2.txt -ch "C" -o out.txt
python3 Worder.py -i list1.txt -ch "!" -ch "?" -i list2.txt -o out.txt
python3 Worder.py -i list1.txt -ch "abc" -i list2.txt --random -o out.txt
```

## Case (applies only to the `-i` list that follows)

```bash
python3 Worder.py --upper -i list.txt -o out.txt        # Tokio
python3 Worder.py --upper-all -i list.txt -o out.txt    # TOKIO
python3 Worder.py --lower -i list.txt -o out.txt        # tOKIO / tokio
python3 Worder.py --lower-all -i list.txt -o out.txt    # tokio

python3 Worder.py --upper-all -i months.txt -ch "!" --lower-all -i seasons.txt
# -> NOVEMBER!spring ...
```

## Full workflow

```bash
python3 Worder.py --years 2020-2025 -o years.txt
python3 Worder.py -i words.txt -i years.txt -o output.txt
```

## All options

```bash
python3 Worder.py --help
