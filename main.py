import random       #we want slot machine to give random values

MAX_LINES = 3        #defined the value here so that we dont have to change in the entire code
MAX_BET = 100
MIN_BET = 1

ROWS = 3            #In this project, we have a 3x3 slot machine and you only get a line when you get 3 in a row, i.e. you win
COLS = 3

symbol_count = {       #list for machine symbols A, B, C, D with A as most valued symbol
    "A": 2,
    "B": 4,
    "C": 6,
    "D", 8
}

#generate the outcome using the values
def get_slot_machine_spin(rows, cols, symbols):    #we need to generate, randomly pick, what symbols are going to be in each column (3 rows -> 3 symbols inside each col)
    all_symbols = []
    for symbol, symbol_count in symbols.items():  #add symbols in the add_symbols list
        for _ in range(symbol_count):       #_ is an anonymous variable in python, when loop without and extra count/index variable
            all_symbols.append(symbol)
            
    #select what values are going to go in every single column
    columns = []
    for col in range(cols):
        column = []
        for row in range(rows):
            value = random.choice(all_symbols)   #random choice from the all_symbols list

def deposit():      #make a function
    while True:
        amount = input("Enter the amount: $")  #taking input
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
    while True:
        bet = get_bet()
        total_bet = bet*lines
        
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is ${balance}")
        else:
            break
    
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

main()

