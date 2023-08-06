import json
import time

import requests

from src.helpers.fs import export_csv


# Create a function that can pull the data from the Private API
def fetch_stocks():
    # Setup Local variables
    url = "https://stockanalysis.com/api/screener/s/f"
    querystring = {"m": "marketCap", "s": "desc",
                   "c": "no,s,n,marketCap,price,change,revenue,volume,industry,sector,revenueGrowth,netIncome,fcf,netCash,priceChang,country,priceChange,openPrice,previousClose,lowPrice,highPrice,premarketPrice,premarketChange,premarketPercentChange,afterHoursPrice,afterHoursChange,afterHoursPercentChange,enterpriseValue,marketCapGroup,peRatio,forwardPE,exchange,dividendYield,priceChange1W,priceChange1M,priceChange6M,priceChangeYTD,priceChange1Y,priceChange3Y,priceChange5Y,priceChange10Y,priceChange15Y,priceChange20Y,week52Low,week52High,priceChange52WLow,priceChange52WHigh,allTimeHigh,allTimeHighChange,allTimeLow,allTimeLowChange,analystRating,topAnalystRating,analystCount,topAnalystCount,priceTarget,priceTargetDiffPercent,topAnalystPTDiffPercent,country,employees,empChange,empGrowth,founded,financialReportDate,last10KReleaseDate,IPODate,IPOPrice,IPOPriceLow,IPOPriceHigh,isSPAC,revenueGrowthQ,revenueGrowth3Y,revenueGrowth5Y,grossProfit,grossProfitGrowth,grossProfitGrowthQ,grossProfitGrowth3Y,grossProfitGrowth5Y,operatingIncome,opIncomeGrowth,opIncomeGrowthQ,opIncomeGrowth3Y,opIncomeGrowth5Y,netIncomeGrowth,netIncomeGrowthQ,netIncomeGrowth3Y,netIncomeGrowth5Y,EPS,EPSGrowth,EPSGrowthQ,EPSGrowth3Y,EPSGrowth5Y,EBIT,EBITDA,researchAndDevelopment,RnDRevenue,operatingCashFlow,investingCashFlow,financingCashFlow,netCashFlow,capitalExpenditures,FCFGrowth,FCFGrowthQ,FCFGrowth3Y,FCFGrowth5Y,FCFShare,freeCashFlowSBC,stockBasedCompensation,SBCRevenue,assets,totalCash,totalDebt,debtGrowthYoY,debtGrowthQoQ,debtGrowth3Y,debtGrowth5Y,netCashGrowth,netCashMarketCap,liabilities,grossMargin,operatingMargin,profitMargin,FCFMargin,EBITDAMargin,EBITMargin,PSRatio,forwardPS,PBRatio,PFCFRatio,PEGRatio,EVSales,forwardEVSales,EVEarnings,EVEBITDA,EVEBIT,EVFCF,earningsYield,FCFYield,dividend,dividendGrowth,payoutRatio,payoutFrequency,buybackYield,shareholderYield,averageVolume,relativeVolume,beta1Y,relativeStrengthIndex,shortPercentFloat,shortPercentShares,shortRatio,sharesOut,floatShares,sharesChYoY,sharesChQoQ,sharesInsiders,sharesInstitut,earningsDate,exDivDate,paymentDate,ROE,ROE5Y,ROA,ROA5Y,returnOnCapital,returnOnCapital5Y,revPerEmployee,profitPerEmployee,assetTurnover,inventoryTurnover,currentRatio,quickRatio,debtEquity,debtEBITDA,debtFCF,interestCoverageRatio,incomeTax,effectiveTaxRate,taxRevenue,shareholdersEquity,workingCapital,lastStockSplit,lastSplitDate,AltmanZScore,PiotroskiFScore,views,EPSGrowthThisQuarter,EPSGrowthNextQuarter,EPSGrowthThisYear,EPSGrowthNextYear,revenueGrowthThisQuarter,revenueGrowthNextQuarter,revenueGrowthThisYear,revenueGrowthNextYear,EPSGrowthNext5Y,revenueGrowthNext5Y",
                   "f": f"exchange-is-NYSE", "p": "1", "dd": "true", "i": "allstocks"}

    # Retrieve the data, retry a max of 10 times over the course of 20 minutes
    for i in range(10):
        try:
            response = requests.request("GET", url, data="", params=querystring)
            return json.loads(response.content)['data']['data']
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
            print(f"Retrying... {i}")
            time.sleep(120)

    return None


# Create a function that can parse the data based on the arguments
def parse(data, marketCap=None, price=None, change=None, shortRatio=None):
    # Setup Local variables
    parsed_data = []

    # Parse the data based on argument input
    for stock in data:
        if marketCap is not None and stock["marketCap"] < marketCap:
            continue

        if price is not None and stock["price"] > price:
            continue

        if change is not None and stock["change"] < change:
            continue

        if shortRatio is not None and stock["shortRatio"] < shortRatio:
            continue

            # If all conditions pass, add the stock to the filtered data list
        parsed_data.append(stock)

    return parsed_data


# Create a function that can export json data to csv file


if __name__ == '__main__':
    stocks = fetch_stocks()
    print("fetched stocks")
    parsed_stocks = parse(stocks, price=100)
    print("parsed stocks")
    if export_csv(parsed_stocks, "stocks_under_10usd"):
        print("exported stocks")
    else:
        print("failed to export stocks")
