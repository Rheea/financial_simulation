
import sys 
import os

from my_functions import calculate_take_home_salary

# clean printout
# For Windows
if os.name == 'nt':
    os.system('cls')
# For macOS and Linux
else:
    os.system('clear')


# Campute Taxes and Insurance
salary_details = calculate_take_home_salary(50000)  # Example salary: £60,000
for key, value in salary_details.items():
    print(f"{key}: £{value}")
