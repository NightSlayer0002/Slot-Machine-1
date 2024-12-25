MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1


def deposit():      #make a function
    while True:
        amount = input("Enter the amount: $")  #taking input with print
        if amount.isdigit():
            amount =int(amount)
            if amount>0:
                break
            else:
                print("Amount must be greater than $0")
        else:
            print("Please enter a number.")
    return amount

def get_num_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + "): ")  #converted the MAX_NUM to str for the print, since the rest is a string
        if lines.isdigit():
            lines =int(lines)
            if 1 <= lines <= MAX_LINES:    #if its under the maximum lines
                break
            else:
                print("Enter a validnumber of lines")
        else:
            print("Please enter a number.")
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line: $")  #taking input
        if amount.isdigit():
            amount =int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be bteween ${MIN_BET} - ${MAX_BET}")     #f and {variable} that converts to string if it can be
        else:
            print("Please enter a number.")
    return amount

def main():
    balance = deposit()   #call the function
    lines = get_num_of_lines()
    bet = get_bet()
    total_bet = bet*lines
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

