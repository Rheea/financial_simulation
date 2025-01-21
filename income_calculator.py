
import sys, os, argparse

from my_functions import calculate_take_home_salary, calculate_pension_contribution_tas

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



# Compute Taxes and Insurance
salary_details = calculate_take_home_salary(annual_salary)  # Example salary: £60,000
for key, value in salary_details.items():
    print(f"{key}: £{value}")

print("\n")

take_home_salary = salary_details['Take-Home Salary']
# Compute pension - contribution - taxed at the source version 
pension_contribution_percentage = 8
take_home_salary_after_tas_pension = calculate_pension_contribution_tas(annual_salary, take_home_salary, pension_contribution_percentage)
for key, value in take_home_salary_after_tas_pension.items():
    print(f"{key}: £{value}")
