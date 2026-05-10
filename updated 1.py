import math
import json
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import requests

# =========================
# Utility Functions
# =========================

def clear():
    print("\n" + "=" * 60 + "\n")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input!")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input!")

def get_save_path(filename):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, filename)

# =========================
# API Functions
# =========================

def fetch_all_funds():
    try:
        return requests.get("https://api.mfapi.in/mf", timeout=10).json()
    except:
        print("API Error")
        return []

def fetch_history(code):
    try:
        data = requests.get(f"https://api.mfapi.in/mf/{code}", timeout=10).json()
        return data["data"]
    except:
        return []

# =========================
# Financial Logic
# =========================

def calculate_return(nav_old, nav_new):
    return ((nav_new - nav_old) / nav_old) * 100

def calculate_cagr(nav_old, nav_new, years):
    return ((nav_new / nav_old) ** (1/years) - 1) * 100

# =========================
# Mutual Fund Features
# =========================

def mutual_fund_lookup():
    clear()
    print("Mutual Fund Lookup\n")

    funds = fetch_all_funds()
    keyword = input("Enter fund name: ").lower()

    matches = [f for f in funds if keyword in f["schemeName"].lower()][:5]

    for i, f in enumerate(matches):
        print(f"{i+1}. {f['schemeName']}")

    choice = get_int("Select: ") - 1
    code = matches[choice]["schemeCode"]

    history = fetch_history(code)

    if len(history) < 2:
        print("Not enough data")
        return

    latest = float(history[0]["nav"])
    old_1y = float(history[min(365, len(history)-1)]["nav"])

    ret_1y = calculate_return(old_1y, latest)

    print(f"\nLatest NAV: ₹{latest}")
    print(f"1-Year Return: {ret_1y:.2f}%")

def historical_return_calculator():
    clear()
    print("Historical Return Calculator\n")

    funds = fetch_all_funds()
    keyword = input("Enter fund name: ").lower()

    matches = [f for f in funds if keyword in f["schemeName"].lower()][:5]

    for i, f in enumerate(matches):
        print(f"{i+1}. {f['schemeName']}")

    choice = get_int("Select: ") - 1
    code = matches[choice]["schemeCode"]

    history = fetch_history(code)

    if len(history) < 100:
        print("Not enough data")
        return

    nav_latest = float(history[0]["nav"])
    nav_1y = float(history[min(365, len(history)-1)]["nav"])
    nav_3y = float(history[min(365*3, len(history)-1)]["nav"])

    ret_1y = calculate_return(nav_1y, nav_latest)
    cagr_3y = calculate_cagr(nav_3y, nav_latest, 3)

    print("\n===== RETURNS =====")
    print(f"1-Year Return: {ret_1y:.2f}%")
    print(f"3-Year CAGR : {cagr_3y:.2f}%")

    # Graph
    navs = [float(x["nav"]) for x in history[:200]][::-1]
    plt.plot(navs)
    plt.title("NAV Trend")
    plt.show()

def top_funds_analyzer():
    clear()
    print("Top Mutual Funds Analyzer\n")

    funds = fetch_all_funds()
    keyword = input("Category (e.g. large cap, flexi cap): ").lower()

    filtered = [f for f in funds if keyword in f["schemeName"].lower()][:20]

    results = []

    for fund in filtered:
        history = fetch_history(fund["schemeCode"])

        if len(history) < 365:
            continue

        try:
            latest = float(history[0]["nav"])
            old = float(history[min(365, len(history)-1)]["nav"])
            ret = calculate_return(old, latest)

            results.append((fund["schemeName"], ret))
        except:
            continue

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n===== TOP FUNDS =====")
    for name, ret in results[:5]:
        print(f"{name[:50]} | {ret:.2f}%")

# =========================
# SIP (unchanged core)
# =========================

class InvestmentCalculator:
    def sip_future_value_stepup(self, monthly, rate, years, step_up):
        r = rate / 12 / 100
        balance = 0
        invested = 0
        data = []
        sip = monthly

        for y in range(1, years+1):
            for _ in range(12):
                balance = (balance + sip) * (1+r)
                invested += sip
            data.append((y, invested, balance))
            sip *= (1 + step_up/100)

        return balance, invested, data

# =========================
# SIP UI
# =========================

def sip_simulator(calc):
    clear()
    print("SIP Simulator\n")

    m = get_float("Monthly: ")
    y = get_int("Years: ")
    r = get_float("Return %: ")
    s = get_float("Step-up %: ")

    final, invested, data = calc.sip_future_value_stepup(m, r, y, s)

    print(f"\nFinal Value: ₹{final:,.2f}")
    print(f"Invested: ₹{invested:,.2f}")

    plt.plot([d[2] for d in data])
    plt.title("Growth")
    plt.show()

# =========================
# Main
# =========================

def main():
    calc = InvestmentCalculator()

    while True:
        clear()
        print("ADVANCED INVESTMENT TOOL\n")
        print("1. SIP Simulator")
        print("2. Mutual Fund Lookup")
        print("3. Historical Return Calculator")
        print("4. Top Funds Analyzer")
        print("5. Exit")

        c = input("Select: ")

        if c == "1":
            sip_simulator(calc)
        elif c == "2":
            mutual_fund_lookup()
        elif c == "3":
            historical_return_calculator()
        elif c == "4":
            top_funds_analyzer()
        elif c == "5":
            break

        input("\nPress Enter...")

if __name__ == "__main__":
    main()