import pandas as pd

def initialize_data(id):
    # Dicionário com dados de entrada
    data = {
        "generalRevenue" : pd.DataFrame(),
        "estabelecimentoTransaction" : pd.DataFrame(),
        "groupsCompanies" : pd.DataFrame(),
        "generalRevenueOportunity" : pd.DataFrame(),
        "generalRevenueEvents": pd.DataFrame(),
        "generalRevenueBrigada" : pd.DataFrame(),
        "generalCosts" : pd.DataFrame(),
        "costDetails" : pd.DataFrame(),
        "ratingsRank" : pd.DataFrame(),
        "ratingsRankDetails" : pd.DataFrame(),
        "generalCostsBlueme" : pd.DataFrame(),
        "costsBluemeDetails" : pd.DataFrame(),
        "ratingsRankBlueme" : pd.DataFrame(),
        "ratingsRankDetailsBlueme" : pd.DataFrame(),
        "billingCompanies" : pd.DataFrame(),
        "worksByFunctions" : pd.DataFrame(),
        "averageFreelaValueAndHourlyRate" : pd.DataFrame(),
        "id": id,
    }

    return data