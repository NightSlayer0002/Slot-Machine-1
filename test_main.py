"""Regression tests for payouts, credit accounting, and terminal input."""
import contextlib
import importlib
import io
import random
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent


class SlotMachineTests(unittest.TestCase):
    def game(self):
        return importlib.import_module("main")

    def run_cli(self, inputs):
        return subprocess.run(
            [sys.executable, str(ROOT / "main.py")],
            input=inputs, text=True, capture_output=True, timeout=5,
        )

    def test_quit_is_clean(self):
        result = self.run_cli("q\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Goodbye", result.stdout)

    def test_eof_is_clean(self):
        result = self.run_cli("")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_invalid_deposit_and_accepts_integer(self):
        result = self.run_cli("hello\n0\n-1\n1.5\n²\n10\nq\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Balance: 10 credits", result.stdout)

    def test_counts_only_selected_horizontal_lines(self):
        game = self.game()
        columns = [["A", "B", "C"]] * 3
        self.assertEqual(game.check_winnings(columns, 1, 2), (10, [1]))
        self.assertEqual(game.check_winnings(columns, 3, 2), (24, [1, 2, 3]))

    def test_mixed_rows_do_not_pay(self):
        game = self.game()
        columns = [["A", "B", "C"], ["B", "C", "D"], ["C", "D", "A"]]
        self.assertEqual(game.check_winnings(columns, 3, 5), (0, []))

    def test_each_symbol_payout(self):
        game = self.game()
        for symbol, payout in [("A", 5), ("B", 4), ("C", 3), ("D", 2)]:
            with self.subTest(symbol=symbol):
                self.assertEqual(
                    game.check_winnings([[symbol] * 3] * 3, 1, 3),
                    (payout * 3, [1]),
                )

    def test_spin_is_three_columns_with_independent_symbol_pools(self):
        game = self.game()
        for seed in range(20):
            columns = game.get_slot_machine_spin(rng=random.Random(seed))
            self.assertEqual(len(columns), 3)
            for column in columns:
                self.assertEqual(len(column), 3)
                self.assertTrue(set(column) <= {"A", "B", "C", "D"})
                self.assertLessEqual(column.count("A"), 2)

    def test_winning_round_deducts_stake_before_paying(self):
        game = self.game()
        output = io.StringIO()
        with patch("builtins.input", side_effect=["1", "2"]), patch.object(
            game, "get_slot_machine_spin", return_value=[["A", "B", "C"]] * 3
        ), contextlib.redirect_stdout(output):
            balance = game.play_round(10)
        self.assertEqual(balance, 18)
        self.assertIn("A | A | A", output.getvalue())

    def test_losing_round_cannot_overdraw_balance(self):
        game = self.game()
        with patch("builtins.input", side_effect=["3", "2", "1"]), patch.object(
            game, "get_slot_machine_spin",
            return_value=[["A", "B", "C"], ["B", "C", "D"], ["C", "D", "A"]],
        ), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(game.play_round(3), 0)

    def test_quitting_mid_round_preserves_balance(self):
        game = self.game()
        with patch("builtins.input", side_effect=["10", "1", "q"]), contextlib.redirect_stdout(io.StringIO()) as output:
            game.main()
        self.assertIn("Final balance: 10 credits", output.getvalue())

    def test_zero_balance_finishes_session(self):
        game = self.game()
        with patch("builtins.input", side_effect=["1", "1", "1"]), patch.object(
            game, "get_slot_machine_spin",
            return_value=[["A", "B", "C"], ["B", "C", "D"], ["C", "D", "A"]],
        ), contextlib.redirect_stdout(io.StringIO()) as output:
            game.main()
        self.assertIn("Final balance: 0 credits", output.getvalue())

    def test_keyboard_interrupt_exits_without_traceback(self):
        game = self.game()
        with patch("builtins.input", side_effect=KeyboardInterrupt), contextlib.redirect_stdout(io.StringIO()) as output:
            game.main()
        self.assertIn("Goodbye", output.getvalue())


if __name__ == "__main__":
    unittest.main()
