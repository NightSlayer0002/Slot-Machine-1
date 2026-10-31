"""A small terminal slot machine using virtual credits only."""

import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100
ROWS = 3
COLS = 3
SYMBOL_COUNTS = {"A": 2, "B": 4, "C": 6, "D": 8}
SYMBOL_VALUES = {"A": 5, "B": 4, "C": 3, "D": 2}


def read_integer(prompt, minimum, maximum=None):
    """Read an integer in range; q, EOF, or Ctrl+C ends the session."""
    while True:
        value = input(prompt).strip()
        if value.lower() == "q":
            raise EOFError
        try:
            number = int(value)
        except ValueError:
            print("Enter a whole number.")
            continue
        if number >= minimum and (maximum is None or number <= maximum):
            return number
        limit = f"{minimum}-{maximum}" if maximum is not None else f"at least {minimum}"
        print(f"Enter {limit}.")


def get_slot_machine_spin(rng=None):
    """Sample each column without replacement from its own symbol pool."""
    rng = rng if rng is not None else random
    symbols = [
        symbol
        for symbol, count in SYMBOL_COUNTS.items()
        for _ in range(count)
    ]
    return [rng.sample(symbols, ROWS) for _ in range(COLS)]


def check_winnings(columns, lines, bet):
    """Return gross payouts and winning row numbers (starting at one)."""
    winnings = 0
    winning_lines = []
    for row in range(lines):
        symbol = columns[0][row]
        if all(column[row] == symbol for column in columns):
            winnings += SYMBOL_VALUES[symbol] * bet
            winning_lines.append(row + 1)
    return winnings, winning_lines


def play_round(balance):
    """Collect an affordable bet, spin, and return the updated balance."""
    lines = read_integer(
        f"Lines to bet on (1-{min(MAX_LINES, balance)}, top to bottom): ",
        1, min(MAX_LINES, balance),
    )
    maximum_bet = min(MAX_BET, balance // lines)
    bet = read_integer(f"Bet per line ({MIN_BET}-{maximum_bet}): ", MIN_BET, maximum_bet)
    stake = bet * lines
    columns = get_slot_machine_spin()
    print()
    for row in range(ROWS):
        print(" | ".join(column[row] for column in columns))
    winnings, winning_lines = check_winnings(columns, lines, bet)
    print(f"Stake: {stake} | Payout: {winnings} | Net: {winnings - stake:+}")
    if winning_lines:
        print("Winning lines: " + ", ".join(map(str, winning_lines)))
    else:
        print("No winning lines.")
    return balance - stake + winnings


def main():
    """Run a session; credits are not persisted between runs."""
    balance = 0
    print("Slot Machine | Virtual credits only")
    print("Match three symbols across a selected horizontal line.")
    print("Payout per credit: A=5, B=4, C=3, D=2. Enter q anytime to quit.")
    try:
        balance = read_integer("Starting credits: ", 1)
        while balance >= MIN_BET:
            print(f"\nBalance: {balance} credits")
            balance = play_round(balance)
            if balance < MIN_BET:
                print("No credits remaining.")
                break
            while True:
                choice = input("Press Enter to spin again, or q to quit: ").strip().lower()
                if choice == "q":
                    raise EOFError
                if not choice:
                    break
                print("Press Enter or enter q.")
    except (EOFError, KeyboardInterrupt):
        print()
    print(f"Final balance: {balance} credits. Goodbye!")


if __name__ == "__main__":
    main()
