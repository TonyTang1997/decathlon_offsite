import pandas as pd

def get_shortage_rate(data,group,store="ALL"):
    """ 
    Grouping by "group" together with store (optional) and then create a shortage_rate column 

    :param data: provided dataframe
    :param group: list of column to be grouped. Example: ["sport","family"]
    :param store: to filter results of specific store. Default: "ALL", no filter on store 
    :return: dataframe with colums [group] + ["shortage_rate"]

    """
    filter_cols = group + ["shortage_rate"]  # get filter columns before "store" is added to group
    
    if store != "ALL":
        group = ["store"] + group 
    
    zero_count = data[data.quantity == 0].groupby(group)["quantity"].count().reset_index()
    total_count = data.groupby(group)["quantity"].count().reset_index()
    joined_count  = total_count.merge(zero_count,how="left",on=group).fillna(0)
    joined_count.columns = group + ["total_count","zero_count"]
    joined_count["shortage_rate"] = joined_count.zero_count/joined_count.total_count
    
    if store == "ALL":
        shortage_rate = joined_count[filter_cols]
    else:
        shortage_rate = joined_count[joined_count["store"] == store][filter_cols]

    return shortage_rate

def get_df_shortage_rate(data, group):
    """
    Generating dataframes with shortage_rate filtered by different store and merging them together

    :param data: provided dataframe 
    :param group: list of column to be grouped. Example: ["sport","family"]
    :return: dataframe with columns GROUP + shortage_rate in all stores, 1614, 1618 and 2350

    """
    result = get_shortage_rate(data,group) # get dataframe of all store first and left join dataframes of different stores to it

    for i in df.store.unique():
        result = result.merge(get_shortage_rate(data, group,i),how="left",on=group)
    
    GROUP = [i.upper() for i in group] # follow output format
    
    result.columns = GROUP + ["ALL STORE", "1614", "1618", "2350"]
    
    return result

df = pd.read_csv("./data/q2.csv")

#get dataframes with shortage_rate grouped by different columns
sport_family = get_df_shortage_rate(df,["sport","family"])
sport = get_df_shortage_rate(df,["sport"])
family = get_df_shortage_rate(df,["family"])

#concat the dataframes 
result = pd.concat([sport_family,sport,family])
result = result[["SPORT","FAMILY","1614","1618","2350","ALL STORE"]]  # rearrange the columns to following output format 
result["SPORT"] = result["SPORT"].fillna("ALL")     # fill "ALL" back 
result["FAMILY"] = result["FAMILY"].fillna("ALL")

#get ALL, ALL dataframe 
shortage_rate_1614 = df[(df.quantity == 0) & (df.store == 1614)]["quantity"].count()/df[df.store == 1614]["quantity"].count()
shortage_rate_1618 = df[(df.quantity == 0) & (df.store == 1618)]["quantity"].count()/df[df.store == 1618]["quantity"].count()
shortage_rate_2350 = df[(df.quantity == 0) & (df.store == 2350)]["quantity"].count()/df[df.store == 2350]["quantity"].count()
shortage_rate_all = df[df.quantity == 0]["quantity"].count()/df["quantity"].count()

all_result = pd.DataFrame([["ALL","ALL",shortage_rate_1614,shortage_rate_1618,shortage_rate_2350,shortage_rate_all]],\
                  columns = result.columns)

final_output = pd.concat([result,all_result]).reset_index(drop=True)






