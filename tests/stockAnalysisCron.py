import json

import requests


# Request all the stocks from the the spesified stock exchange (NYSE, NASDAQ)
def request(exchange):
    exchanges = ["NYSE", "NASDAQ"]

    if exchange.upper() not in exchanges:
        return "0"

    url = ""

    querystring = {"m": "marketCap", "s": "desc",
                   "c": "no,s,n,marketCap,price,change,revenue,volume,industry,sector,revenueGrowth,netIncome,fcf,netCash,priceChang,country,priceChange,openPrice,previousClose,lowPrice,highPrice,premarketPrice,premarketChange,premarketPercentChange,afterHoursPrice,afterHoursChange,afterHoursPercentChange,enterpriseValue,marketCapGroup,peRatio,forwardPE,exchange,dividendYield,priceChange1W,priceChange1M,priceChange6M,priceChangeYTD,priceChange1Y,priceChange3Y,priceChange5Y,priceChange10Y,priceChange15Y,priceChange20Y,week52Low,week52High,priceChange52WLow,priceChange52WHigh,allTimeHigh,allTimeHighChange,allTimeLow,allTimeLowChange,analystRating,topAnalystRating,analystCount,topAnalystCount,priceTarget,priceTargetDiffPercent,topAnalystPTDiffPercent,country,employees,empChange,empGrowth,founded,financialReportDate,last10KReleaseDate,IPODate,IPOPrice,IPOPriceLow,IPOPriceHigh,isSPAC,revenueGrowthQ,revenueGrowth3Y,revenueGrowth5Y,grossProfit,grossProfitGrowth,grossProfitGrowthQ,grossProfitGrowth3Y,grossProfitGrowth5Y,operatingIncome,opIncomeGrowth,opIncomeGrowthQ,opIncomeGrowth3Y,opIncomeGrowth5Y,netIncomeGrowth,netIncomeGrowthQ,netIncomeGrowth3Y,netIncomeGrowth5Y,EPS,EPSGrowth,EPSGrowthQ,EPSGrowth3Y,EPSGrowth5Y,EBIT,EBITDA,researchAndDevelopment,RnDRevenue,operatingCashFlow,investingCashFlow,financingCashFlow,netCashFlow,capitalExpenditures,FCFGrowth,FCFGrowthQ,FCFGrowth3Y,FCFGrowth5Y,FCFShare,freeCashFlowSBC,stockBasedCompensation,SBCRevenue,assets,totalCash,totalDebt,debtGrowthYoY,debtGrowthQoQ,debtGrowth3Y,debtGrowth5Y,netCashGrowth,netCashMarketCap,liabilities,grossMargin,operatingMargin,profitMargin,FCFMargin,EBITDAMargin,EBITMargin,PSRatio,forwardPS,PBRatio,PFCFRatio,PEGRatio,EVSales,forwardEVSales,EVEarnings,EVEBITDA,EVEBIT,EVFCF,earningsYield,FCFYield,dividend,dividendGrowth,payoutRatio,payoutFrequency,buybackYield,shareholderYield,averageVolume,relativeVolume,beta1Y,relativeStrengthIndex,shortPercentFloat,shortPercentShares,shortRatio,sharesOut,floatShares,sharesChYoY,sharesChQoQ,sharesInsiders,sharesInstitut,earningsDate,exDivDate,paymentDate,ROE,ROE5Y,ROA,ROA5Y,returnOnCapital,returnOnCapital5Y,revPerEmployee,profitPerEmployee,assetTurnover,inventoryTurnover,currentRatio,quickRatio,debtEquity,debtEBITDA,debtFCF,interestCoverageRatio,incomeTax,effectiveTaxRate,taxRevenue,shareholdersEquity,workingCapital,lastStockSplit,lastSplitDate,AltmanZScore,PiotroskiFScore,views,EPSGrowthThisQuarter,EPSGrowthNextQuarter,EPSGrowthThisYear,EPSGrowthNextYear,revenueGrowthThisQuarter,revenueGrowthNextQuarter,revenueGrowthThisYear,revenueGrowthNextYear,EPSGrowthNext5Y,revenueGrowthNext5Y",
                   "f": f"exchange-is-{exchange.upper()}", "p": "1", "dd": "true", "i": "allstocks"}

    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)

    return json.loads(response.content)["data"]["data"]


# Function to parse the data and remove based on certain arguments that the user provided
def parse(data, marketCap=None, price=None, change=None, shortRatio=None):
    # Create a new list to store the filtered data
    filtered_data = []

    # Loop over the data
    for stock in data:
        # Check if the data is within the range of the arguments
        if marketCap is not None and stock["marketCap"] < marketCap:
            continue

        if price is not None and stock["price"] > price:
            continue

        if change is not None and stock["change"] < change:
            continue

        if shortRatio is not None and stock["shortRatio"] < shortRatio:
            continue

        # If all conditions pass, add the stock to the filtered data list
        filtered_data.append(stock)

    # Return the final filtered array
    return filtered_data


def export(json_list):
    # Write the header line to the csv file
    header_keys = list(json_list[0].keys())
    clean_header_keys = []
    for key in header_keys:
        clean_header_keys.append(
            key.replace(",", "").replace('"', "'").replace('\n', '').replace('\r', '').replace('\t', '').replace("\\",
                                                                                                                 ""))
    header = ",".join(clean_header_keys)

    with open("stocks.csv", "a") as f:
        f.write(header)

    # Write the data to the csv file
    for stock in json_list:
        values = list(stock.values())
        clean_values = []
        for value in values:
            clean_values.append(
                str(value).replace(",", "").replace('"', "'").replace('\n', '').replace('\r', '').replace('\t',
                                                                                                          '').replace(
                    "\\", ""))

        line = ",".join(clean_values)
        with open("stocks.csv", "a") as f:
            f.write("\n" + line)


# Test the function if being run from this file
if __name__ == "__main__":
    # Get the data
    data = request("NYSE")
    # Parse the data
    data = parse(data, price=10)
    # Export the data to csv
    export(data)
