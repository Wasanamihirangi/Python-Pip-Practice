import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


df = pd.read_csv("outputtrade.csv")
print(df)

# Count Trade and Extended Trade
Number_Of_Trades = (df[df["Tag"] == "TRADE"]["Tag"]).count()
Number_Of_ExtendedTrades = (df[df["Tag"] == "EXTRD"]["Tag"]).count()
print("Number of Trades : ", Number_Of_Trades)
print("Number of Extended Trades : ", Number_Of_ExtendedTrades)

# Total value of BUY trades and Sell Trades
df_trade_buy = df[(df["Direction"] == "B") | (df["Direction"] == "BUY")]
Total_value_of_BUY_trades = sum(df_trade_buy["Price"]*df_trade_buy["Quantity"])
print("Total value of BUY trades : ", Total_value_of_BUY_trades)

df_trade_sell = df[(df["Direction"] == "S") | (df["Direction"] == "SELL")]
Total_value_of_SELL_trades = sum(df_trade_sell["Price"]*df_trade_sell["Quantity"])
print("Total value of SELL trades : ", Total_value_of_SELL_trades)

# Length of the longest comment
Number_Of_Comments = df["comment"].dropna()
# print(Number_Of_Comments)
comments_list = [str(i).strip() for i in df['comment'].tolist()]
# print(comments_list)
Length_of_longest_comment = len(max(comments_list, key=len))
print("Length of longest comment : ", Length_of_longest_comment)

# Longest comment
Longest_comment = max(comments_list, key=len)
print("Longest comment : ", Longest_comment)

# Trade interval
TempLast_Time = df["Trade Date and Time"][len(df)-1]
TempFirst_Time = df["Trade Date and Time"][0]

Last_Time = dt.datetime(int(TempLast_Time[0:4]), int(TempLast_Time[5:7]), int(TempLast_Time[8:10]),
                        int(TempLast_Time[11:13]), int(TempLast_Time[14:16]), int(TempLast_Time[17:19]))
First_Time = dt.datetime(int(TempFirst_Time[0:4]), int(TempFirst_Time[5:7]), int(TempFirst_Time[8:10]),
                         int(TempFirst_Time[11:13]), int(TempFirst_Time[14:16]), int(TempFirst_Time[17:19]))
Trade_Interval = int((Last_Time-First_Time).total_seconds())
print("Trade_Interval : ", Trade_Interval)

#########################################################################
# List of Firms
# Number of unique firms
Number_of_unique_firms = len((df["Buyer"].append(df["seller"], ignore_index=True)).unique())
print("Number of unique firms : ", Number_of_unique_firms)

# Unique firm IDs
Unique_firm_IDs = "|".join((df["Buyer"].append(df["seller"], ignore_index=True)).unique())
print("Unique firm IDs : ", Unique_firm_IDs)

#########################################################################
# Totals per Item ID
# Item ID
Item_ID_List = ((df["ItemID"]).unique().tolist())
Item_ID_List.sort()
Item_ID = "|".join(Item_ID_List)
print("Item_ID :", Item_ID)

# Total value per item ID
df["total_value"] = df["Price"]*df["Quantity"]
df1 = df[["ItemID", "total_value"]].groupby("ItemID").sum()
df1 = df1.reset_index()
print(df1)

#########################################################################
# Convert into data frames
# Summary
Summary = pd.DataFrame({"Number_of_trades": [Number_Of_Trades],
                        "Number_of_extended_trades": [Number_Of_ExtendedTrades],
                        "Total_value_of_BUY_trades": [Total_value_of_BUY_trades],
                        "Total_value_of_SELL_trades": [Total_value_of_SELL_trades],
                        "Length_of_the_longest_comment": [Length_of_longest_comment],
                        "Longest_comment": [Longest_comment],
                        "Trade_interval": [Trade_Interval]
                        }).transpose().reset_index()
Summary.columns = ("Field_name", "Value")
print(Summary)

# List of Firms
List_of_Firms = pd.DataFrame({"Number of unique firms": [Number_of_unique_firms],
                              "Unique firm IDs": [Unique_firm_IDs]}).transpose().reset_index()
List_of_Firms.columns = ("Field_name", "Value")
print(List_of_Firms)

# Totals per Item ID
Totals_per_Item_ID = df1


# Convert to PDF
# Summary PDF
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
Summary_table = ax.table(cellText=Summary.values, colLabels=Summary.columns, loc="upper center")
pp = PdfPages("Summary.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()


# List of Firms PDF
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
Firms_table = ax.table(cellText=List_of_Firms.values, colLabels=List_of_Firms.columns, loc="upper center")
pp = PdfPages("Firms.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()

# Totals per Item ID
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
ItemID_table = ax.table(cellText=Totals_per_Item_ID.values, colLabels=Totals_per_Item_ID.columns, loc="upper center")
pp = PdfPages("ItemID.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
