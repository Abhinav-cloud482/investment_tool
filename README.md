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



## Screenshots

<img width="982" height="514" alt="1" src="https://github.com/user-attachments/assets/320e9159-f32c-476b-8898-d6baf8682d5c" />

<img width="979" height="525" alt="2" src="https://github.com/user-attachments/assets/67201f66-92b3-44ef-8f12-9ee55f2ed615" />

<img width="979" height="512" alt="3" src="https://github.com/user-attachments/assets/1b9aaed4-1b7d-4200-a619-7ddc0587c385" />

<img width="684" height="588" alt="4" src="https://github.com/user-attachments/assets/de80f48c-a065-4fac-a868-14f947dd9f61" />

<img width="981" height="519" alt="1" src="https://github.com/user-attachments/assets/c4627936-7008-436a-8ed5-ada0bf0f12a0" />

<img width="269" height="110" alt="Saved Output 1" src="https://github.com/user-attachments/assets/ac22a063-6ab2-4f80-801e-1e597b6291b4" />

<img width="829" height="375" alt="Saved Output 2" src="https://github.com/user-attachments/assets/df0e9881-6367-45dc-bf75-2bc1ff8f1eac" />


## Disclaimer

This tool is for educational purposes only.

It does not provide financial advice. Please consult a certified financial advisor before making investment decisions.


## Contributing

Contributions are welcome!

- Fork the repo
- Create a new branch
- Make your changes
- Submit a pull request


## License

This project is licensed under the MIT License.


## Author

Abhinav Dixit

Python Developer | Data & ML Enthusiast
