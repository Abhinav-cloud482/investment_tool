import math
import json
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

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
    print("SIP with Step-Up Simulator\n")

    monthly = get_float("Monthly Investment (₹): ")
    years = get_int("Years: ")
    inflation = get_float("Inflation (%): ")
    step_up = get_float("Annual SIP Increase (%): ")

    print("\nRisk Profile:")
    print("1. Conservative (8%)")
    print("2. Moderate (12%)")
    print("3. Aggressive (15%)")

    choice = input("Choose: ")
    rate = {"1":8, "2":12, "3":15}.get(choice, 12)

    real_rate = calc.real_return(rate, inflation)

    final, invested, data = calc.sip_future_value_stepup(monthly, rate, years, step_up)

    taxed_gain = calc.apply_tax(final - invested)
    final_after_tax = invested + taxed_gain

    clear()
    show_dashboard(invested, final_after_tax, years)

    print(f"\nReal Return (after inflation): {real_rate:.2f}%")

    # Insights
    if final_after_tax < 10000000:
        print("\nInsight:")
        print("→ Increase SIP, step-up, or duration to reach ₹1 Crore")

    plot_graph(data)

    if input("Export CSV? (y/n): ").lower() == 'y':
        export_csv(data)

    if input("Save plan? (y/n): ").lower() == 'y':
        save_plan({
            "monthly": monthly,
            "years": years,
            "rate": rate
        })

def fire_calculator():
    clear()
    print("FIRE Calculator\n")

    monthly_exp = get_float("Monthly Expenses (₹): ")
    corpus = monthly_exp * 12 * 25

    print(f"\nRequired Corpus: ₹ {corpus:,.2f}")

def retirement_planner(calc):
    clear()
    print("Retirement Planner\n")

    age = get_int("Current Age: ")
    retire = get_int("Retirement Age: ")
    expense = get_float("Monthly Expense (₹): ")
    inflation = get_float("Inflation (%): ")

    years = retire - age

    if years <= 0:
        print("Invalid retirement age!")
        return

    future_expense = expense * (1 + inflation/100) ** years
    corpus = future_expense * 12 * 25

    print(f"\nFuture Monthly Expense: ₹ {future_expense:,.2f}")
    print(f"Required Corpus: ₹ {corpus:,.2f}")

def goal_tracker():
    clear()
    print("Goal Tracker\n")

    goal = get_float("Goal Amount (₹): ")
    current = get_float("Current Savings (₹): ")

    if goal == 0:
        print("Invalid goal amount!")
        return

    progress = (current / goal) * 100
    print(f"\nProgress: {progress:.2f}%")

# =========================
# Main Menu
# =========================

def main():
    calc = InvestmentCalculator()

    while True:
        clear()
        print("ADVANCED INVESTMENT TOOL\n")
        print("1. SIP Simulator")
        print("2. FIRE Calculator")
        print("3. Retirement Planner")
        print("4. Goal Tracker")
        print("5. Load Saved Plan")
        print("6. Exit")

        choice = input("Select: ")

        if choice == "1":
            sip_simulator(calc)
        elif choice == "2":
            fire_calculator()
        elif choice == "3":
            retirement_planner(calc)
        elif choice == "4":
            goal_tracker()
        elif choice == "5":
            plan = load_plan()
            if plan:
                print(plan)
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()