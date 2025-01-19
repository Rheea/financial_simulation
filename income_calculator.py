
import sys, os, argparse

from my_functions import calculate_take_home_salary

# clean printout
# For Windows
if os.name == 'nt':
    os.system('cls')
# For macOS and Linux
else:
    os.system('clear')


# Arguments passed
n = len(sys.argv)
print("Total arguments passed:", n)
if n == 1:
    annual_salary =  1000000
else:
    annual_salary =  float(sys.argv[1])



# Campute Taxes and Insurance
salary_details = calculate_take_home_salary(annual_salary)  # Example salary: £60,000
for key, value in salary_details.items():
    print(f"{key}: £{value}")
