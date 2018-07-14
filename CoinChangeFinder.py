import random
import math
from statistics import median


def make_change(value, coins, best_cost=float("inf")):
    if value == 0:
        return [], 0

    best_solution = None
    for i, (coin, count, cost) in enumerate(coins):
        max_num = min(count, value // coin, best_cost // cost if cost else float("inf"))
        for num in range(max_num, 0, -1):
            coin_value = num * coin
            coin_cost = num * cost
            if coin_cost < best_cost:  # this is always true the first iteration, but may not be later
                solution, solution_cost = make_change(value - coin_value, coins[i + 1:],
                                                      best_cost - coin_cost)
                if solution is not None:
                    best_solution = [(coin, num)] + solution
                    best_cost = coin_cost + solution_cost
    return best_solution, best_cost


def parse():
    value = int(input().replace(".", ""))
    wallet = dict(zip(*[iter(map(int, input().replace(".", "").split()))] * 2))
    cashier = list(map(int, input().replace(".", "").split()))
    print(value)
    print(wallet)
    print(cashier)
    return value, wallet, cashier


def print_output(pay, change, final_wallet):
    print("pay", " ".join("{:.2f} {}".format(coin / 100, count) for coin, count in pay if count != 0))
    print("change returned", " ".join("{:.2f} {}".format(coin / 100, count) for coin, count in change if count != 0))
    print("wallet", " ".join("{:.2f} {}".format(coin / 100, count) for coin, count in final_wallet if count != 0))
    totalcoins = sum(count for coin, count in final_wallet if count != 0)
    print("total coins", totalcoins)
    return final_wallet, totalcoins


def solve(value, wallet, coins):
    result, cost = make_change(value, coins)
    pay = []
    change = []
    for coin, count in result:
        if coin in wallet:
            if wallet[coin] > count:
                pay.append((coin, wallet[coin] - count))
            elif wallet[coin] < count:
                change.append((coin, count - wallet[coin]))
            del wallet[coin]
        else:
            change.append((coin, count))
    pay.extend(wallet.items())
    pay.sort()
    change.sort()
    result.sort()
    return pay, change, result


def minimize_wallet(value, wallet, cashier):
    wallet_value = sum(coin * count for coin, count in wallet.items())
    coin_dict = wallet.copy()
    coin_dict.update((coin, wallet_value // coin) for coin in cashier)
    coin_list = [(coin, count, 1) for coin, count in sorted(coin_dict.items(), reverse=True)]
    return solve(wallet_value - value, wallet, coin_list)


def minimize_change(value, wallet, cashier):
    wallet_value = sum(coin * count for coin, count in wallet.items())
    coin_list = [(coin, count, 0) for coin, count in wallet.items()]
    coin_list.extend((coin, wallet_value // coin, 1) for coin in cashier)
    coin_list.sort(key=lambda x: (-x[0], x[2]))
    return solve(wallet_value - value, wallet, coin_list)


def simulatespending(denominations,transactions, final_wallet={},inprice=0):
    cumtotalcoins = 0
    #inal_wallet = {}
    for i in range(1, transactions + 1):

        print("*****Transaction*****", i)
        fin_wallet2 = {}
        totalfunds = 0
        for x in final_wallet:
            # print(x[0],x[1])
            fin_wallet2[x[0]] = fin_wallet2.get(x[0], 0) + x[1]
            totalfunds += x[0] * x[1]

        # print(fin_wallet2)
        print("total funds", totalfunds)
        if inprice != 0:
            price = inprice
        else:
            #price = random.randint(1, max(denominations))
            price = math.floor(max(denominations)**random.random())

        # Get mininum currency denomination
        # print(price)
        if price - price % min(denominations) > 0:
            price = price - price % min(denominations)
        else:
            price = price + min(denominations) - price % min(denominations)

        # Make sure price is divisible

        print("price", price)

        if price > totalfunds:
            highestnote = max(denominations)
            print(f"atm withdrawal {highestnote}")
            fin_wallet2[max(denominations)] = 1

        final_wallet, totalcoins = print_output(*minimize_change(price,
                                                                 fin_wallet2,
                                                                 denominations))

        cumtotalcoins += totalcoins
        print("Average coins", cumtotalcoins / i)
    return cumtotalcoins / i


def GenerateExistingCurrency():
    # removed 2000 from japan, its never used
    # need special logic to handle aus no 1 or 2 and candada and swiss and yean
    # need special logic to handle eur 200000
    currencies = [
        ["Australia",   [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]],
        ["NZ",          [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]],
        ["HK",          [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000]],
        ["Japan",       [1, 5, 10, 50, 100, 500, 1000, 5000, 10000]],
        ["USA",         [1, 5, 10, 25, 100, 500, 1000, 2000, 5000, 10000]],
        ["Euro",        [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]],
        ["Pound",       [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]],
        ["Canada",      [5, 10, 25, 100, 200, 500, 1000, 2000, 5000, 10000]],
        ["Swiss",       [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 100000]],
        ["Yuan",        [10, 50, 100, 500, 1000, 2000, 5000, 10000]],
        ["Swedish",     [1, 5, 10, 20, 50, 100, 200, 500]],
        ["Mexican",     [50,100,200,500,1000,2000,5000,10000,20000,50000,100000]],
        ["Singapore",   [5,10,20,50,100,200,500,1000,5000]],
        ["Norwegian",   [1,5,10,20,50,100,200,500,1000]],
        ["South Korea", [100,500,1000,5000,10000,50000]],
        ["Turkish",     [5,10,25,50,100,500,1000,2000,5000]],
        ["Indian",      [50,100,200,500,1000,2000,5000,10000,50000,200000]],
        ["Russian",     [10,50,100,200,500,5000,10000,50000,100000,500000]],
        ["Brazilian",   [5,10,25,50,100,500,1000,2000,5000,10000]],
        ["South Africa",[5,10,20,100,200,1000,2000,5000,10000,20000]],
    ]
    return currencies


def SimulateTransactions(currencies,transactions):
    for x in currencies:
        print("*********************************", x[0], "*********************************")
        print("Denominations ", x[1])
        x.append(simulatespending(x[1],transactions))
        # x = (x[0],x[1],y)

    currencies2 = sorted(currencies, key=lambda x: x[2])

    for x in currencies2:
        print("Currency", f"{x[0]:<15}", end='\t\t')
        print("Average coins + notes in wallet", f'{x[2]:8.2f}', end='\t\t')
        print("Denominations", x[1])
        #print(max(x[1]) / min(x[1]))


def GenerateNewCurrency(numcurrencies):
    cXurrencies = []
    for currencies in range(1, numcurrencies + 1):
        denominations = []
        prevcurrencyunit = 0
        for numberofcurrencyunits in range(random.randint(8,14)):
            if numberofcurrencyunits == 0:
                #first currency unit between 1 and 10
                currencyunit = random.randint(1, 10)
            else:
                currencymultiplier = min(random.randint(20, 100),
                                         random.randint(20, 100),
                                         random.randint(20, 100),
                                         random.randint(20, 100))
                currencyunit = int(prevcurrencyunit * currencymultiplier / 10)
                currencyunit = currencyunit - currencyunit % prevcurrencyunit

            #     if currencyunit > 1000000:
            #         currencyunit = currencyunit - currencyunit%1000000
            #     elif currencyunit > 100000:
            #         currencyunit = currencyunit - currencyunit%100000
            #     elif currencyunit > 10000:
            #         currencyunit = currencyunit - currencyunit%10000
            #     elif currencyunit > 1000:
            #         currencyunit = currencyunit - currencyunit % 1000
            #     elif currencyunit > 100:
            #         currencyunit = currencyunit - currencyunit%100
            #     elif currencyunit > 50:
            #         currencyunit = currencyunit - currencyunit%10
            #     elif currencyunit > 5:
            #         currencyunit = currencyunit - currencyunit%5
            # #print(currencyunit)

                if currencyunit / denominations[0] > 20000:
                    break

            denominations.append(currencyunit)
            prevcurrencyunit = currencyunit
        #print(denominations)
        cXurrencies.append(["Random " + str(currencies),denominations])
    #print(cXurrencies)
    print('\n'.join(map(str, cXurrencies)))
    return cXurrencies


def buy(price=867,
        wallet=[(1,2), (5,2), (10,2), (50,2), (100,2), (1000,2), (5000,2), (10000,2)],
        denomination=[1, 5, 10, 50, 100, 1000, 5000, 10000]):
    simulatespending(denomination, 1, wallet,price)


def generate_base_x_currencies():
    cXurrencies = []
    newunit = 0
    for i in range(2,11):
        prevunit = 0
        denominations = []
        for j in range(1,12):
            if j == 1:
                #cXurrencies.append(["Random " + str(i), 1])
                newunit = 1
            else:
                newunit = prevunit * i
                #print(cXurrencies[j-1] * i)
                #cXurrencies.append(["Random " + str(i), cXurrencies[j-1] * i])

                if newunit / denominations[0] > 20000:
                    break
            denominations.append(newunit)
            #print('\n'.join(map(str, denominations)))
            #print(newunit)
            prevunit = newunit

        #print(denominations)

        cXurrencies.append(["Base " + str(i), denominations])
    print('\n'.join(map(str, cXurrencies)))
    return cXurrencies


def main():
    #listofcurrencies = generate_base_x_currencies()
    #listofcurrencies = GenerateNewCurrency(5)
    listofcurrencies = GenerateExistingCurrency()
    #calculate_ratio_of_max_to_min_currency(listofcurrencies)
    SimulateTransactions(listofcurrencies, 100)
    #buy()


def calculate_ratio_of_max_to_min_currency(inCurrencies):
    for currency in inCurrencies:
        #pass
        print(currency[0], min(currency[1]), max(currency[1]),max(currency[1]) / min(currency[1]))


if __name__ == "__main__":
    # print_output(*minimize_wallet(*parse()))
    # print_output(*minimize_change(*parse())) # use this if the scoring rules are changed
    main()
    #generate_base_x_currencies()




# my currency
# smallest value must be 10 or less
# must have no more than 13 units
# must have at least 8 units
# each unit must be between 2-10 times of hte preceding unit
# maximum unit must be 500-20000 times size of lowest unit

#TODO base x currency
