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
            print("Invalid input! Enter a number.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Enter an integer.")

def get_save_path(filename):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, filename)

# =========================
# Mutual Fund API (AMFI)
# =========================

def fetch_all_funds():
    try:
        url = "https://api.mfapi.in/mf"
        response = requests.get(url, timeout=10)
        return response.json()
    except:
        print("❌ Unable to fetch mutual fund list (Check Internet)")
        return []

def fetch_nav(scheme_code):
    try:
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["data"][0]  # latest NAV
    except:
        print("❌ Unable to fetch NAV")
        return None

def mutual_fund_lookup():
    clear()
    print("Mutual Fund Lookup (Live Data)\n")

    funds = fetch_all_funds()

    if not funds:
        return

    name = input("Enter fund name keyword: ").lower()

    matches = [f for f in funds if name in f["schemeName"].lower()][:5]

    if not matches:
        print("No matching funds found.")
        return

    for i, fund in enumerate(matches):
        print(f"{i+1}. {fund['schemeName']}")

    choice = get_int("Select fund: ") - 1

    if choice < 0 or choice >= len(matches):
        print("Invalid choice")
        return

    scheme_code = matches[choice]["schemeCode"]

    nav_data = fetch_nav(scheme_code)

    if nav_data:
        print("\nLatest NAV Details:")
        print(f"Date : {nav_data['date']}")
        print(f"NAV  : ₹ {nav_data['nav']}")

# =========================
# Core Class
# =========================

class InvestmentCalculator:

    def sip_future_value_stepup(self, monthly, rate, years, step_up):
        monthly_rate = rate / 12 / 100
        balance = 0
        yearly_data = []
        invested = 0

        current_sip = monthly

        for year in range(1, years + 1):
            for _ in range(12):
                balance = (balance + current_sip) * (1 + monthly_rate)
                invested += current_sip

            yearly_data.append((year, invested, balance))
            current_sip *= (1 + step_up / 100)

        return balance, invested, yearly_data

    def real_return(self, return_rate, inflation):
        return ((1 + return_rate/100) / (1 + inflation/100) - 1) * 100

    def apply_tax(self, gain):
        if gain <= 100000:
            return gain
        return gain - (gain - 100000) * 0.10

# =========================
# Features
# =========================

def show_dashboard(invested, final_value, years):
    gain = final_value - invested

    if invested > 0 and years > 0:
        cagr = ((final_value / invested) ** (1/years) - 1) * 100
    else:
        cagr = 0

    print("\n===== INVESTMENT SUMMARY =====")
    print(f"Total Invested   : ₹ {invested:,.2f}")
    print(f"Future Value     : ₹ {final_value:,.2f}")
    print(f"Wealth Gained    : ₹ {gain:,.2f}")
    print(f"CAGR             : {cagr:.2f}%")
    print("=" * 40)

def plot_graph(data):
    try:
        years = [x[0] for x in data]
        invested = [x[1] for x in data]
        value = [x[2] for x in data]

        plt.figure()
        plt.plot(years, invested, '--', label="Invested")
        plt.plot(years, value, label="Portfolio Value")
        plt.xlabel("Years")
        plt.ylabel("Amount (₹)")
        plt.title("Investment Growth")
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print("Graph error:", e)

def export_csv(data):
    try:
        filename = f"investment_{datetime.now().strftime('%H%M%S')}.csv"
        path = get_save_path(filename)

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Year", "Invested", "Value"])
            writer.writerows(data)

        print(f"✅ CSV saved at: {path}")

    except Exception as e:
        print("❌ Error saving CSV:", e)

def save_plan(plan):
    try:
        path = get_save_path("saved_plan.json")
        with open(path, "w") as f:
            json.dump(plan, f)
        print("✅ Plan saved on Desktop")
    except Exception as e:
        print("Error saving plan:", e)

def load_plan():
    try:
        path = get_save_path("saved_plan.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        print("No saved plan found.")
        return None

# =========================
# Calculators
# =========================

def sip_simulator(calc):
    clear()
    print("SIP Simulator\n")

    monthly = get_float("Monthly Investment (₹): ")
    years = get_int("Years: ")
    inflation = get_float("Inflation (%): ")
    step_up = get_float("Step-Up (%): ")

    rate = get_float("Expected Return (%): ")

    real_rate = calc.real_return(rate, inflation)

    final, invested, data = calc.sip_future_value_stepup(monthly, rate, years, step_up)

    taxed_gain = calc.apply_tax(final - invested)
    final_after_tax = invested + taxed_gain

    clear()
    show_dashboard(invested, final_after_tax, years)

    print(f"\nReal Return: {real_rate:.2f}%")

    plot_graph(data)

    if input("Export CSV? (y/n): ").lower() == 'y':
        export_csv(data)

# =========================
# Main Menu
# =========================

def main():
    calc = InvestmentCalculator()

    while True:
        clear()
        print("ADVANCED INVESTMENT TOOL\n")
        print("1. SIP Simulator")
        print("2. Mutual Fund Lookup (LIVE)")
        print("3. Load Saved Plan")
        print("4. Exit")

        choice = input("Select: ")

        if choice == "1":
            sip_simulator(calc)
        elif choice == "2":
            mutual_fund_lookup()
        elif choice == "3":
            plan = load_plan()
            if plan:
                print(plan)
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()