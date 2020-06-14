import requests
import re
import pandas as pd
import math

def make_requests(ticker):

    """
    :param ticker:  The stock ticker
    :return: tuple with 3 elements each is string

    """
    # dropdown=['is','cf','ratios','ovr']
    # request 3 'pages'
    ratios_response = requests.get("https://api.quickfs.net/stocks/"+ticker+":US/ratios/Annual/grL0gNYoMoLUB1ZoAKLfhXkoMoLODiO1WoL9.grLtk3PoMoLmqFEsMasbNK9fkXudkNBtR2jpkr5dINZoAKLtRNZoMlG1MQx1MJG1PiPcOpEfqXGoMwcoqNWaka9tIKO6OlZ1PiPoAKLahSVthKO6OwqfR3EfhGHwhSVthK5lh20oAKLsRNWiq29rIKO6OlVnPwkiIJErOosokFLtqpacISqaOlmsAKLrISqth25Zkpa2Olt7OaBJOlmnAKLQZCO6PF19vZ.pgYRsakz8o7Q78EVDruHCDDAm8-TG3qWQgFNNHQj82D")
    is_response = requests.get("https://api.quickfs.net/stocks/" + ticker + ":US/is/Annual/grL0gNYoMoLUB1ZoAKLfhXkoMoLODiO1WoL9.grLtk3PoMoLmqFEsMasbNK9fkXudkNBtR2jpkr5dINZoAKLtRNZoMlG1MQx1MJG1PiPcOpEfqXGoMwcoqNWaka9tIKO6OlZ1PiPoAKLahSVthKO6OwqfR3EfhGHwhSVthK5lh20oAKLsRNWiq29rIKO6OlVnPwkiIJErOosokFLtqpacISqaOlmsAKLrISqth25Zkpa2Olt7OaBJOlmnAKLQZCO6PF19vZ.pgYRsakz8o7Q78EVDruHCDDAm8-TG3qWQgFNNHQj82D")
    cf_response = requests.get("https://api.quickfs.net/stocks/" + ticker + ":US/cf/Annual/grL0gNYoMoLUB1ZoAKLfhXkoMoLODiO1WoL9.grLtk3PoMoLmqFEsMasbNK9fkXudkNBtR2jpkr5dINZoAKLtRNZoMlG1MQx1MJG1PiPcOpEfqXGoMwcoqNWaka9tIKO6OlZ1PiPoAKLahSVthKO6OwqfR3EfhGHwhSVthK5lh20oAKLsRNWiq29rIKO6OlVnPwkiIJErOosokFLtqpacISqaOlmsAKLrISqth25Zkpa2Olt7OaBJOlmnAKLQZCO6PF19vZ.pgYRsakz8o7Q78EVDruHCDDAm8-TG3qWQgFNNHQj82D")
    ovr_response = requests.get("https://api.quickfs.net/stocks/" + ticker + ":US/ovr/Annual/")
    # convert to json format
    ratios_response = ratios_response.json()
    is_response = is_response.json()
    cf_response = cf_response.json()
    ovr_response = ovr_response.json()
    # extract only the string
    ratios_response = ratios_response['datasets']['ratios']
    is_response = is_response['datasets']['is']
    cf_response = cf_response['datasets']['cf']
    ovr_response = ovr_response['datasets']['ovr']

    return(ratios_response,ovr_response, is_response, cf_response)


pages=make_requests('BABA')

def remove_str(page_object):
    """

    :return:
    """
    #Key Ratios Page
    # extract the years and text
    regex = r"(class='thead')(.+)(Returns)"
    years = re.findall(regex, page_object[0])
    # extract the years only
    regex = r"(\d+)"
    years = re.findall(regex, years[0][1])
    # Converting list strings to list of integers
    years = [int(i) for i in years]

    # Extract the Return on Invested Capital
    regex = r"(>Return on Invested Capital)(.+)(Return on Capital Employed<)"
    ROIC = re.findall(regex, page_object[0])
    # Clean the string
    regex = r"(</td><td class='dataCell' data-type='percentage')"
    ROIC = re.sub(regex, "", ROIC[0][1])
    regex = r"(</td></tr><tr class=' '><td class='labelCell'>)"
    ROIC = re.sub(regex, "", ROIC)
    # separate the numbers
    regex = r"(data-value=')(\d+\.\d+)"
    ROIC = re.findall(regex, ROIC)
    ROIC = [num[1] for num in ROIC]
    ROIC = [float(i)*100 for i in ROIC]

    # Extract the Book Value per-Share
    regex = r"(>Per-Share Items)(.+)(Valuation)"
    BVPS = re.findall(regex, page_object[0])
    regex = r"(>Book Value)(.+)(Tangible Book)"
    BVPS = re.findall(regex, BVPS[0][1])
    # Clean the string
    regex = r"(</td><td class='dataCell' data-type='ratio-2')"
    BVPS = re.sub(regex, "", BVPS[0][1])
    regex = r"(</td></tr><tr class=' '><td class='labelCell'>)"
    BVPS = re.sub(regex, "", BVPS)
    # separate the numbers
    regex = r"(data-value=')+(\d+\.\d+)"
    BVPS = re.findall(regex, BVPS)
    BVPS = [num[1] for num in BVPS]
    # Converting list strings to list of float
    BVPS = [float(i) for i in BVPS]

    # Extract Free Cash Flow
    regex = r"(>Supplementary Items)(.+)(>Per-Share Items)"
    FCF=re.findall(regex, page_object[0])
    regex = r"(>Free Cash Flow)(.+)(>Book Value)"
    FCF = re.findall(regex, FCF[0][1])
    # Clean the string
    regex = r"(</td><td class='dataCell' data-type='normal')"
    FCF = re.sub(regex, "", FCF[0][1])
    regex = r"(</td></tr><tr class=' '><td class='labelCell')"
    FCF = re.sub(regex, "", FCF)
    # separate the numbers
    regex = r"(data-value=')(\d+)"
    FCF = re.findall(regex, FCF)
    FCF = [num[1] for num in FCF]
    # Converting list strings to list of float
    FCF = [float(i)/1000000 for i in FCF]
    #
    # df1 = [years, BVPS, ROIC, FCF]
    # df1 = pd.DataFrame(df1, index=["years", "BVPS", "ROIC%", "FCF" ])
    #
    df1 = pd.DataFrame(list(zip(years, BVPS, ROIC, FCF)),
                      columns=["years", "BVPS", "ROIC%", "FCF"])
    # Overview  Page
    #extract the years and text
    regex = r"(class='thead')(.+)(Revenue<)"
    years = re.findall(regex, page_object[1])
    # extract the years only
    regex = r"(\d+)"
    years = re.findall(regex, years[0][1])
    # Converting list strings to list of integers
    years = [int(i) for i in years]

    # extract the Revenues (Sales)
    regex = r"(>Revenue)(.+)(>Revenue Growth)"
    REV = re.findall(regex, page_object[1])
    # Clean the string
    regex = r"(</td><td class='dataCell' data-type='normal')"
    REV = re.sub(regex, "", REV[0][1])
    regex = r"(</td></tr><tr class=' '><td class='labelCell italic indent')"
    REV = re.sub(regex, "", REV)
    # separate the numbers
    regex = r"(data-value=')(\d+)"
    REV = re.findall(regex, REV)
    REV = [num[1] for num in REV]
    # Converting list strings to list of float
    REV = [float(i)/1000000 for i in REV]

    # extract the EPS (Earnings Per Share)
    regex = r"(>Earnings Per Share)(.+)(>EPS Growth)"
    EPS = re.findall(regex, page_object[1])
    regex = r"(data-value=')((\-\d+\.\d+)|(\d+\.\d+))"
    EPS = re.findall(regex, EPS[0][1])
    EPS = [num[1] for num in EPS]
    # Converting list strings to list of float
    EPS = [float(i) for i in EPS]

    # extract the EPS (Earnings Per Share) of TTM trailing 12 Months
    regex = r"(>EPS \(Basic\)<)(.+)(>EPS \(Diluted\)<)"
    EPS_TTM = re.findall(regex, page_object[2])

    regex = r"(</td><td class='dataCell' data-type='eps)|(</td></tr><tr class=' '><td class='labelCell')"
    EPS_TTM = re.sub(regex, "", EPS_TTM[0][1])
    # separate the numbers
    regex = r"(data-value=')(\d+\.\d+)"
    EPS_TTM = re.findall(regex, EPS_TTM)
    EPS_TTM = [num[1] for num in EPS_TTM]

    # Converting list strings to list of float
    EPS_TTM = [float(i) for i in EPS_TTM]

    # df2 = [years, REV, EPS]
    # df2 = pd.DataFrame(df2)
    df2 = pd.DataFrame(list(zip(years, REV, EPS)),
                       columns=["years", "REV", "EPS"])
    return (df1,df2 ,EPS_TTM)

table1,table2,table3=remove_str(pages)

#avg = sum(tables["ROIC%"][-5:])/len(tables["ROIC%"][-5:])

def Number_of_doublings_in_X_years(num_years,data):
    """
    :param num_years: This is numeric value - the X. 
    :param data: Column vector 
    :return: 
    """
    tot_years = len(data)-1
    current = data[tot_years]
    past = data[-num_years:-num_years+1]
    # cond = (current/past)> 0
    cond = current > past
    # if current>past:
    if cond.any():
        result = math.log2(current/past)
    else:
        result = 'The current value is lower than the past'
    return(result)

def Years_2_1_doubling(num_years, Number_of_doubling ):
    """
    :param Number_of_doubling: the result value (a float) of the function  Number_of_doublings_in_X_years
    :param num_years: same value as in Number_of_doublings_in_X_years the X value
    :return:
    """
    if isinstance( Number_of_doubling, (int, float)):
        return (num_years/Number_of_doubling )
    else:
        return (Number_of_doubling)

def Growth_rate_percen_for_the_last_X_Years(Years_2_1):
    """

    :param Years_2_1: the result of Years_2_1_doubling
    :return: is the growth rate in X years we are looking for values greater then 15 %
    """
    if isinstance(Years_2_1, (int, float)):
        return (72/Years_2_1)
    else:
        return (Years_2_1)

try1=Number_of_doublings_in_X_years(5,tables["BVPS"])
try2=Years_2_1_doubling(5, try1)
try3= Growth_rate_percen_for_the_last_X_Years(try2)

