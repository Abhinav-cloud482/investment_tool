# investment_tool

## Advanced Investment Tool (CLI-Based)

A powerful command-line investment calculator built in Python to help you simulate wealth creation, plan retirement, track financial goals, and estimate financial independence (FIRE).


## Features

### SIP Simulator (with Step-Up)

- Monthly investment simulation
- Annual SIP increase (Step-Up)
- Risk-based return selection (Conservative / Moderate / Aggressive)
- Inflation-adjusted real returns
- Tax-adjusted final value
- CAGR calculation
- Investment insights
- Graph visualization
- Export results to CSV
- Save & load investment plans

### FIRE Calculator

- Estimate corpus required for Financial Independence
- Based on the 25x annual expense rule

### Retirement Planner

- Calculates future monthly expenses (inflation-adjusted)
- Estimates total retirement corpus required

### Goal Tracker

- Tracks savings progress toward a financial goal
- Shows completion percentage


## Tech Stack
- Python 3
- Matplotlib (for graphs)
- JSON (for saving plans)
- CSV (for exporting data)

## Project Structure

```
investment_tool.py   # Main application file
README.md            # Project documentation
```


## Installation

1. Clone the repository :-

```
git clone https://github.com/your-username/investment-tool.git
cd investment-tool
```

2. Install dependencies :-

```
pip install matplotlib
```

3. Run the application :-

```
python investment_tool.py
```

## How It Works

### SIP Calculation

- Compounds monthly investments using :-

```
FV = (SIP + Growth) compounded monthly
```

- Supports :-

    - Annual step-up
    - Inflation adjustment
    - Tax calculation on gains
 


## Output Example

```
===== INVESTMENT SUMMARY =====
Total Invested   : ₹ 12,00,000
Future Value     : ₹ 32,45,000
Wealth Gained    : ₹ 20,45,000
CAGR             : 11.23%
================================
```


## File Outputs

- CSV Export → Saved on Desktop
- Saved Plan → saved_plan.json on Desktop


## Future Improvements

- GUI version (Tkinter / Web App)
- More tax rules (LTCG/STCG)
- Mutual fund / stock API integration
- Goal-based SIP suggestions
- Multi-asset portfolio simulation


## Disclaimer

This tool is for educational purposes only.

It does not provide financial advice. Please consult a certified financial advisor before making investment decisions.


## Contributing

Contributions are welcome!

Fork the repo
Create a new branch
Make your changes
Submit a pull request
