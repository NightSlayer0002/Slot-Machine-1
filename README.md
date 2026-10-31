# Slot Machine

A small Python terminal game with a 3×3 grid and virtual credits.

## Run

Requires Python 3.10 or newer. No external dependencies.

```sh
python main.py
```

Enter a starting balance, choose one to three horizontal lines, and set a bet
of 1–100 credits per line within your balance. Press Enter to play another
round, or enter `q` at any prompt to quit. Credits reset when the program exits.

## Rules

- Selected lines are counted from the top row down.
- Three matching symbols across a selected row pay the multiplier below.
- The total stake is deducted once per spin; winning payouts are then added.
- Columns are sampled independently. Each column draws three symbols without
  replacement from a pool containing 2 A, 4 B, 6 C, and 8 D symbols.

| Symbol | Payout per credit bet on a winning line |
| --- | --- |
| A | 5 |
| B | 4 |
| C | 3 |
| D | 2 |

For example, a 2-credit bet on one matching A line pays 10 credits.
After the 2-credit stake, the net gain is 8 credits.

This is a learning project using virtual credits, with no real-money features.

## Tests

```sh
python -m unittest -v
```
