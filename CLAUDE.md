# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

Run the main income calculator with:
```bash
python3 income_calculator.py [annual_salary]
```

If no salary argument is provided, it defaults to £1,000,000 for demonstration purposes.

Examples:
```bash
python3 income_calculator.py 60000    # Calculate for £60,000 salary
python3 income_calculator.py 100000   # Calculate for £100,000 salary
```

## Code Architecture

This is a UK-focused financial simulation tool with two main components:

### Core Files
- `income_calculator.py`: Main entry point that processes command line arguments and orchestrates calculations
- `my_functions.py`: Contains all calculation logic for UK tax, National Insurance, and pension contributions

### Key Functions in my_functions.py
- `calculate_take_home_salary(annual_salary)`: Computes UK Income Tax and National Insurance contributions based on current rates and thresholds
- `calculate_pension_contribution_tas(annual_salary, take_home_salary, pension_contribution_percentage)`: Calculates pension contributions with tax relief for "Tax At Source" (TAS) schemes
- `pension_matching_my_company(desired_pension_contribution_employee)`: Implements company-specific pension matching logic (5% to 3% match, plus 1% extra per employee 1%, up to 8% employee/6% employer)

### UK Tax System Implementation
The code implements current UK tax rates and thresholds:
- Personal Allowance: £12,570
- Basic rate (20%): £12,571 to £50,270
- Higher rate (40%): £50,271 to £125,140
- Additional rate (45%): above £125,140
- National Insurance: 8% between thresholds, 2% above upper threshold

### Pension Calculations
- Uses qualifying earnings between Lower Earnings Level (£6,240) and Upper Earnings Level (£50,270)
- Implements Tax At Source (TAS) pension scheme with automatic 20% basic rate tax relief
- Calculates additional tax relief for higher and additional rate taxpayers

## Development Notes

- No external dependencies beyond Python standard library
- UK tax rates and thresholds are defined as constants at the top of my_functions.py
- The application clears the terminal screen on startup for clean output
- All monetary values are displayed in GBP with appropriate formatting