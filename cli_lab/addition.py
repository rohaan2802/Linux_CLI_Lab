"""Add two finite decimal numbers with exact decimal arithmetic."""
import argparse
from decimal import Decimal, InvalidOperation


def finite_number(value):
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise argparse.ArgumentTypeError("enter a valid decimal number") from error
    if not number.is_finite():
        raise argparse.ArgumentTypeError("enter a finite number")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=finite_number)
    parser.add_argument("second", type=finite_number)
    parser.add_argument("--roll", default="i222327")
    args = parser.parse_args()
    total = args.first + args.second
    print(f"Hey {args.roll}, the sum of Two Numbers is: {total}")


if __name__ == "__main__":
    main()
