
import sys 
# Arguments passed
n = len(sys.argv)
print("Total arguments passed:", n)
if n == 1:
    pension_contrib_arg = 0.08
else:
    print("Percentage of employee contribution:", sys.argv[1])
    pension_contrib_arg =  float(sys.argv[1])


# import matplotlib.pyplot as plt
# monthly_netto = []
# yearly_contribution = []
# contrib_list = [3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# for contrib in contrib_list:
    # contrib = contrib*0.01
    # Income Tax Variables.
total_income = 110000
income_tax_none = 0.0
income_tax_low = 20.0
income_tax_high = 40.0
income_tax_vhigh = 45.0

tax_brackets = [0.0, 0.2, 0.4, 0.45]
income_brackets = [0, 12571,  50270, 125140, 10000000000]

# Pension variables
pension_contribution = pension_contrib_arg
# Employer matches 5% to 3% and 1% extra every employee 1%, up to 8% employee, 6% employer
if pension_contribution<=0.08:
    pension_matching = pension_contribution - 0.02
    if pension_matching <0:
        pension_matching = 0 
else:
    pension_matching = 0.06


# Lower and Upper levels for qualified earnings
# Explained here https://www.nestpensions.org.uk/schemeweb/helpcentre/contributions/calculating-contributions/calculate-contributions-using-qualifying-earnings.html
lel = 6240 # Lower Earnings Level 
uel = 50270 # Upper Earnings Level


national_insurance_monthly = 350.0

# Calculate income tax per bracket and total
print("===== INCOME TAX =====")
total_income_tax = 0
salary_reached = False
for i, tax in enumerate(tax_brackets):

    if income_brackets[i+1]>total_income:
        qualifying = total_income - income_brackets[i]        
        salary_reached = True
    else:
        qualifying = income_brackets[i+1] - income_brackets[i]


    marginal_tax = qualifying * tax
    print(f"£{qualifying} at {tax*100}% = {marginal_tax}")
    
    total_income_tax += marginal_tax
    if salary_reached:
        break


print(f"Total income = {total_income:.2f}")
print(f"Total income tax = {total_income_tax:.2f}")

# Calculate per month
monthly_tax = total_income_tax/12.0
monthly_income = total_income/12.0
print(f"Monthly income = {monthly_income:.2f}")
print(f"Monthly income tax = {monthly_tax:.2f}")


# Calculate pension:
print("===== PENSION =====")
# HMRC refunds 20% , so effective employee contribution is 80% of contribution
contrib_employee = ((uel-lel )* pension_contribution) * 0.8
contrib_hmrc = ((uel-lel )* pension_contribution) * 0.2
contrib_employer = ((uel-lel )* pension_matching)
contrib_total = contrib_employee + contrib_hmrc + contrib_employer

# Calculate final values
final_income = total_income - total_income_tax - contrib_employee - national_insurance_monthly*12
final_monthly_income = final_income /12.0
final_monthly_income_2 = monthly_income - monthly_tax - national_insurance_monthly- contrib_employee/12.0

if final_monthly_income-final_monthly_income_2 > 10:
    print("Monthly Calculations are wrong, please check")

print(f"With an Employee Contribution of = {pension_contribution*100:.2f}%")
print("---> Yearly")
print(f"Total Employee Contrib = {contrib_employee:.2f}")
print(f"Total HMRC Contrib = {contrib_hmrc:.2f}")
print(f"Total Employer Contrib = {contrib_employer:.2f}")
print(f"Total Yearly Pension Contribution =  {contrib_total:.2f}")
print(f"Final Yearly Income = {final_income:.2f}")
print("---> Monthly")
print(f"Monthly Employee Contrib = {contrib_employee/12.0:.2f}")
print(f"Monthly HMRC Contrib = {contrib_hmrc/12.0:.2f}")
print(f"Monthly Employer Contrib = {contrib_employer/12.0:.2f}")
print(f"Final Monthly Income = {final_monthly_income:.2f}")


#     monthly_netto.append(final_monthly_income)
#     yearly_contribution.append(contrib_total)

# plt.subplot(211)
# plt.plot(contrib_list, monthly_netto)
# plt.title("Monthly Netto Salary (£)")
# plt.subplot(212)
# plt.title("Yearly Pension Contribution(£)")
# plt.plot(contrib_list, yearly_contribution)
# plt.show()



## FURHER INFO:
# https://www.gov.uk/tax-on-your-private-pension/pension-tax-relief
# https://ukpersonal.finance/pensions/
# https://ukpersonal.finance/tax-traps-and-tax-efficiency/
# https://ukpersonal.finance/pensions/#How_do_I_claim_higher-rate_tax_relief
