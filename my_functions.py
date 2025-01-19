def calculate_take_home_salary(annual_salary):
    """
    Calculate the UK National Insurance, Income Tax, and take-home salary.
    
    :param annual_salary: Annual gross salary (in GBP)
    :return: A dictionary containing tax, NIC, and take-home salary.
    """
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


