# Define thresholds and rates
tax_free_allowance = 12570  # Personal Allowance (Income below this is tax-free)
basic_rate_threshold = 50270  # Income above this threshold is taxed at higher rate
additional_rate_threshold = 125140  # Income above this threshold has no Personal Allowance

# Income Tax rates
basic_rate = 0.2  # 20% for income between £12,571 and £50,270
higher_rate = 0.4  # 40% for income between £50,271 and £125,140
additional_rate = 0.45  # 45% for income above £125,140

# National Insurance thresholds and rates
ni_primary_threshold = 12570  # Income below this is not subject to NIC
ni_upper_threshold = 50270  # Income above this has lower NIC rate
ni_standard_rate = 0.08  # 8% for income between thresholds
ni_upper_rate = 0.02  # 2% for income above upper threshold

# Lower and Upper levels for qualified earnings
# Explained here https://www.nestpensions.org.uk/schemeweb/helpcentre/contributions/calculating-contributions/calculate-contributions-using-qualifying-earnings.html
lel = 6240 # Lower Earnings Level 
uel = 50270 # Upper Earnings Level

def pension_matching_my_company(desired_pension_contribution_employee):
    # Pension variables
    pension_contribution = desired_pension_contribution_employee
    # Employer matches 5% to 3% and 1% extra every employee 1%, up to 8% employee, 6% employer
    if pension_contribution<=8:
        pension_matching = pension_contribution - 2
        if pension_matching <0:
            pension_matching = 0 
    else:
        pension_matching = 6
    return pension_matching


def calculate_take_home_salary(annual_salary):
    """
    Calculate the UK National Insurance, Income Tax, and take-home salary.
    
    :param annual_salary: Annual gross salary (in GBP)
    :return: A dictionary containing tax, NIC, and take-home salary.
    """
    # # Define thresholds and rates
    # tax_free_allowance = 12570  # Personal Allowance (Income below this is tax-free)
    # basic_rate_threshold = 50270  # Income above this threshold is taxed at higher rate
    # additional_rate_threshold = 125140  # Income above this threshold has no Personal Allowance
    
    # # Income Tax rates
    # basic_rate = 0.2  # 20% for income between £12,571 and £50,270
    # higher_rate = 0.4  # 40% for income between £50,271 and £125,140
    # additional_rate = 0.45  # 45% for income above £125,140

    # # National Insurance thresholds and rates
    # ni_primary_threshold = 12570  # Income below this is not subject to NIC
    # ni_upper_threshold = 50270  # Income above this has lower NIC rate
    # ni_standard_rate = 0.08  # 8% for income between thresholds
    # ni_upper_rate = 0.02  # 2% for income above upper threshold

    print(f"Annual salary: £{annual_salary}")
    # Calculate Income Tax
    print("===== Income Tax Breakdown=====")
    if annual_salary > additional_rate_threshold:
        taxable_income = annual_salary  # No Personal Allowance
        print(f"£{0} at {0}% = {0}")

    else:
        taxable_income = max(0, annual_salary - tax_free_allowance)
        print(f"£{tax_free_allowance} at {0}% = {0}")
    basic_tax = max(0, min(taxable_income, basic_rate_threshold - tax_free_allowance)) * basic_rate
    higher_tax = max(0, min(taxable_income - basic_rate_threshold, additional_rate_threshold - basic_rate_threshold)) * higher_rate
    additional_tax = max(0, taxable_income - additional_rate_threshold) * additional_rate
    total_tax = basic_tax + higher_tax + additional_tax


    print(f"£{max(0, min(taxable_income, basic_rate_threshold - tax_free_allowance))} at {basic_rate*100}% = {basic_tax}")
    print(f"£{max(0, min(taxable_income - basic_rate_threshold, additional_rate_threshold - basic_rate_threshold))} at {higher_rate*100}% = {higher_tax}")
    print(f"£{max(0, taxable_income - additional_rate_threshold)} at {additional_rate*100}% = {additional_tax}")

   

    print("===== National Insurance Breakdown=====")
    # Calculate National Insurance Contributions (NIC)
    print(f"£{ni_primary_threshold} at {0}% = {0}")
    ni_taxable_income = max(0, annual_salary - ni_primary_threshold)
    ni_basic = max(0, min(ni_taxable_income, ni_upper_threshold - ni_primary_threshold)) * ni_standard_rate
    print(f"£{max(0, min(ni_taxable_income, ni_upper_threshold - ni_primary_threshold))} at {ni_standard_rate*100}% = {ni_basic}")
    ni_additional = max(0, ni_taxable_income - ni_upper_threshold) * ni_upper_rate
    print(f"£{max(0, ni_taxable_income - ni_upper_threshold)} at {ni_upper_rate*100}% = {ni_additional}")
    total_nic = ni_basic + ni_additional

    # Calculate Take-Home Salary
    take_home_salary = annual_salary - total_tax - total_nic
    print("\n")

    return {
        "Annual Salary": annual_salary,
        "Income Tax": round(total_tax, 2),
        "National Insurance": round(total_nic, 2),
        "Take-Home Salary": round(take_home_salary, 2),
    }


def calculate_pension_contribution_tas(annual_salary, take_home_salary, pension_contribution_percentage):

    # Compute qualifying income 
    if annual_salary > uel:
        qualifying_income = uel - lel
    else:
        qualifying_income = annual_salary - lel

    # Gross pension contribution (based on percentage of qualifying salary)
    gross_contribution = (qualifying_income * pension_contribution_percentage) / 100
    
    # Tax relief added by provider (20% of the gross contribution)
    basic_rate_tax_relief = gross_contribution * 0.2

    # Net contribution (deducted from take-home pay)
    net_contribution = gross_contribution - basic_rate_tax_relief

    pension_matching = pension_matching_my_company(pension_contribution_percentage)
    print(f"Employee contribution {pension_contribution_percentage:.2f}%")
    print(f"Company matches {pension_matching:.2f}%")
    print("\n")

    # Determine additional relief based on salary
    if annual_salary <= basic_rate_threshold:
        additional_relief = 0  # No extra relief for basic-rate taxpayers
    elif annual_salary <= additional_rate_threshold:
        additional_relief = gross_contribution * (higher_rate - basic_rate)
    else:
        additional_relief = gross_contribution * (additional_rate - basic_rate)

    # Total tax relief (basic + additional)
    total_tax_relief = basic_rate_tax_relief + additional_relief

    return {
        "Annual Gross Salary": annual_salary,
        "Take-Home Salary (Before Pension)": round(take_home_salary, 2),
        "Gross Pension Contribution": round(gross_contribution, 2),
        "Net Pension Contribution": round(net_contribution, 2),
        "Take-Home Salary (After Pension)": round(take_home_salary - net_contribution, 2),
        "Gross Pension Contribution": round(gross_contribution, 2),
        "Basic Rate Tax Relief (20%)": round(basic_rate_tax_relief, 2),
        "Additional Tax Relief (40% and/or 45%)": round(additional_relief, 2),
        "Total Tax Relief": round(total_tax_relief, 2),
    }

