from datetime import datetime
from matplotlib import pyplot
import numpy as np
import pandas as pd

# function to prompt user for full name
def getFullName():
    while True:
        try:
            full_name = str(input('Please enter first name and last name:   '))

            # only accept non-empty input, otherwise prompt message to allow retry
            if full_name == '':
                print('Sorry, the full name can\'t be an empty string. Please try again!')
                continue
            else:
                break
        except ValueError:
            print('Sorry, that was not a valid string. Please try again!')

    return full_name

# fucntion to prompt user for gender
def getGender():

    gender_list = ['M', 'F']

    while True:
        try:
            gender = str(input('Please enter your gender [Male/Female or M/F]:  ')).upper()[0]

            # only accept non-empty input, otherwise prompt message to allow retry
            if gender == '' or gender == ' ':
                print('Sorry, gender can\'t be an empty string. Please try again!')
                continue
            elif not (gender in gender_list):
                print('Sorry, ensure the input gender such as "Male" or "Female". Please try again!')
                continue
            else:
                break
        except IndexError:
            print('Sorry, that was not a valid string. Please try again!')

    return gender

# function to prompt user for birthday
def getBirthday():

    while True:
        try:
            birthday = datetime.strptime(input('Please enter your birthday [YYYY-MM-DD]:  '), '%Y-%m-%d').date()

            # only accept non-empty input, otherwise prompt message to allow retry
            if birthday == '':
                print('Sorry, birthday can\'t be an empty string. Please try again!')
                continue
            else:
                break
        except ValueError:
            print('Sorry, that was not a valid birthday. Please ensure the birthday is in "YYYY-MM-DD" format and try again!')

    return birthday

# function to return age given birthday
def getAge(birthday):
    today = datetime.now().date()

    return (today - birthday).days/365

# function to return accumulation years and decumulation years given gender and age
def getAccumDecumYears(gender, age):

    # assume 85 years of life expectance for male and 90 for female
    if gender == 'M':
        life_expectancy = 85
    else:
        life_expectancy = 90

    retire_age = 65

    # time user have before retirement
    accumulation_years = max(0, retire_age - age)

    # time user have after retirement
    decumulation_years = max(0, min(life_expectancy - retire_age, life_expectancy - age))

    return accumulation_years, decumulation_years

# function to read in the text for a specified question
def getQuestion(number):
    inputFile = 'question' + str(number) + '.txt'
    question = ''
    with open(inputFile, "r") as infile:
        line = infile.readline()
        while line != "" :
            question += line
            line = infile.readline()

    return question

# function to ask user a question and return option user entered
def askQuestion(question):

    option_list = ['A', 'B', 'C', 'D', 'E']

    while True:
        try:
            option = str(input(question)).upper()

            # only accept non-empty input, otherwise prompt message to allow retry
            if option == '':
                print('Sorry, option selected can\'t be empty. Please try again!')
                continue
            elif not (option in option_list):
                print('Sorry, ensure input is a valid option [A, B, C, D, E]. Please try again!')
                continue
            else:
                break
        except ValueError:
            print('Sorry, that was not a valid option. Please try again!')

    return option

# function to accumulate score based on option user selected
def accumulateScore(score, answer, metrics):
    if answer == 'A':
        score[metrics[0]] += 1
    elif answer == 'B':
        score[metrics[1]] += 1
    elif answer == 'C':
        score[metrics[2]] += 1
    elif answer == 'D':
        score[metrics[3]] += 1
    elif answer == 'E':
        score[metrics[4]] += 1

    return score

# function to display and return calculated question score
def doCategoryQuestion(number, score, metrics):
    question = getQuestion(number)
    answer = askQuestion(question)
    score = accumulateScore(score, answer, metrics)

    return score

# function to get user's investment objectives
def getInvestmentObjectives():
    metrics = ['safty', 'income', 'balanced', 'LT growth', 'speculative']
    inv_obj = dict.fromkeys(metrics, 0)

    # do question 0
    inv_obj = doCategoryQuestion(0, inv_obj, metrics)

    # do question 1
    inv_obj = doCategoryQuestion(1, inv_obj, metrics)

    max_val = list(inv_obj.values())
    max_key = list(inv_obj.keys())

    return max_key[max_val.index(max(max_val))]

# function to get user's investment time horizon
def getInvestmentHorizon():
    metrics = ['1-3 years', '3-5 years', '5-10 years', '10-15 years', '15+ years']
    inv_hor = dict.fromkeys(metrics, 0)

    # do question 2
    inv_hor = doCategoryQuestion(2, inv_hor, metrics)

    max_val = list(inv_hor.values())
    max_key = list(inv_hor.keys())

    return max_key[max_val.index(max(max_val))]

# function to get user's income requirement
def getIncomeRequirement():
    metrics = ['0%', '1%-3%', '3%-6%', '6%-9%', '>9%']
    inc_req = dict.fromkeys(metrics, 0)

    # do question 3
    inc_req = doCategoryQuestion(3, inc_req, metrics)

    max_val = list(inc_req.values())
    max_key = list(inc_req.keys())

    return max_key[max_val.index(max(max_val))]

# function to get user's risk tolerance
def getRiskTolerance(accumulation_years, decumulation_years):
    metrics = ['zero', 'low', 'medium', 'high', 'very high']
    risk_tol = dict.fromkeys(metrics, 0)

    # do question 4
    risk_tol = doCategoryQuestion(4, risk_tol, metrics)

    # do question 5
    risk_tol = doCategoryQuestion(5, risk_tol, metrics)

    # do question 6
    risk_tol = doCategoryQuestion(6, risk_tol, metrics)

    # do question 7
    risk_tol = doCategoryQuestion(7, risk_tol, metrics)

    # adjust user's risk tolerance to be less conservative if the user have more time to
    # save up than spending
    if accumulation_years > decumulation_years:
            risk_tol['zero'] -= 1
            risk_tol['low'] -= 1
            risk_tol['medium'] -= 0.5

    max_val = list(risk_tol.values())
    max_key = list(risk_tol.keys())

    return max_key[max_val.index(max(max_val))]

# function to return investment mandate given objectives, time, incom and risk tolerance
def getInvestmentMandate(objectives, time, income, risk):

    # ensure user who require some income to be classified with income mandate
    if (income == '3%-6%') or (income == '6%-9%') or (income == '>9%') :
        mandate = 'Income'

    # ensure user with minimum risk tolerance to be classified with the most conservative
    # mandate
    elif risk == 'zero':
        mandate = 'Income'
    elif objectives == 'safty':
        mandate = 'Income'
    elif (objectives == 'income') and (time == '1-3 years'):
        mandate = 'Income'
    elif (objectives == 'income') and (time == '3-5 years'):
        mandate = 'Income'
    elif (objectives == 'income') and (time == '5-10 years'):
        mandate = 'Balanced Income'
    elif (objectives == 'income') and (time == '10-15 years'):
        mandate = 'Balanced Income'
    elif (objectives == 'income') and (time == '15+ years'):
        mandate = 'Balanced Income'
    elif (objectives == 'balanced') and (income == '3%-6%'):
        mandate = 'Balanced Income'
    elif (objectives == 'balanced') and (income == '6%-9%'):
        mandate = 'Balanced Income'
    elif (objectives == 'balanced') and (income == '>9%'):
        mandate = 'Balanced Income'
    elif (objectives == 'balanced') and (income == '0%'):
        mandate = 'Balanced'
    elif (objectives == 'balanced') and (income == '1%-3%'):
        mandate = 'Balanced'
    elif (objectives == 'LT growth') and (risk == 'low'):
        mandate = 'Balanced'
    elif (objectives == 'LT growth') and (risk == 'medium'):
        mandate = 'Balanced'
    elif (objectives == 'LT growth') and (risk == 'high'):
        mandate = 'Balanced Growth'
    elif (objectives == 'LT growth') and (risk == 'very high'):
        mandate = 'Balanced Growth'
    elif objectives == 'speculative':
        if (time == '5-10 years') or (time == '10-15 years') or (time == '15+ years'):
            mandate = 'Growth'
        elif (risk == 'medium') or (risk == 'high') or (risk == 'very high'):
            mandate = 'Growth'
        else:
            mandate = 'Balanced Growth'

    return mandate

# fucntion to return asset mix given mandate
def getAssetMix(mandate):
    if mandate == 'Income':
        asset_mix = [15, 85, 0, 0, 0, 0]
    elif mandate == 'Balanced Income':
        asset_mix = [10, 50, 20, 0, 20, 0]
    elif mandate == 'Balanced':
        asset_mix = [5, 40, 30, 5, 15, 5]
    elif mandate == 'Balanced Growth':
        asset_mix = [2, 30, 40, 9, 10, 9]
    elif mandate == 'Growth':
        asset_mix = [0, 20, 50, 15, 0, 15]

    return asset_mix

# function to plot asset mix pie chart
def plotAssetMix(asset_mix, full_name, mandate):

    # initialize and convert data to list
    asset_class = ['Cash', 'Fixed Income', 'Public Equity', 'Private Equity', 'Liquid Real Estate', 'Hedge Fund']
    asset_mix = np.array(asset_mix)

    # initialize a dataframe for pie char display
    data = {'Asset Class':asset_class, 'Amount':asset_mix}
    df = pd.DataFrame(data)

    # drop asset classes with zero amount of allocation
    df = df[(df['Amount']!=0)]

    # display asset allocation in pie chart
    print('Please see recommended asset mix chart below')
    pyplot.pie(df['Amount'], labels = df['Asset Class'], autopct='%1.1f%%')
    pyplot.title(f'Recommended Asset Mix with "{mandate}" Mandate for {full_name}')
    pyplot.legend(title = 'Asset Class')
    pyplot.show()

# function to get gernal information from user
def getGenericInfo():
    full_name = getFullName()
    gender = getGender()
    birthday = getBirthday()
    age = getAge(birthday)
    accumulation_years, decumulation_years = getAccumDecumYears(gender, age)

    return full_name, accumulation_years, decumulation_years

# function to get investment mandate
def getMandate(accumulation_years, decumulation_years):
    inv_obj = getInvestmentObjectives()
    inv_hor = getInvestmentHorizon()
    inc_req = getIncomeRequirement()
    risk_tol = getRiskTolerance(accumulation_years, decumulation_years)
    mandate = getInvestmentMandate(inv_obj, inv_hor, inc_req, risk_tol)

    return mandate

def main():
    full_name, accumulation_years, decumulation_years = getGenericInfo()
    mandate = getMandate(accumulation_years, decumulation_years)
    asset_mix = getAssetMix(mandate)
    plotAssetMix(asset_mix, full_name, mandate)

main()