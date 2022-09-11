# %% import libraries
from IPython.display import display
import pandas as pd
import numpy as np
pd.options.display.max_rows = 500

# import fils
companies_df = pd.read_csv("All_Campenes.csv")
assciation_df = pd.read_csv("all_assciation.csv")
companies_in_liquidation_df = pd.read_csv("Companies_in_liquidation.csv")
AGUDOT_df = pd.read_csv("AGUDOT.csv")

our_companies_df = pd.read_csv("MYT_Accounting_Conversion_TJ.csv")


# tools
VALID_FREFIX = ["5"+str(i) for i in range(10)]


def valid_BN(num: np.int64) -> bool:
    "retunr if num is valid business number"
    return type(num) == np.int64 and len(str(num)) == 9


# %% clean and marge all csv's
companies_df.columns = [
    "Business_Number",
    "Account_Name",
    "account_name_en",
    "type",
    "status",
    "description",
    "campeny_gool",
    "date_created",
    "is_GOV_campeny",
    "limitations",
    "breaks_the_rules",
    "last_year",
    "city",
    "street_name",
    "home_number",
    "pin",
    "mailbox",
    "country",
    "person_name",
    "substatus",
    "what_is"
]
companies_df["Business_Number"] = companies_df["Business_Number"].astype(
    'int64')
companies_df = companies_df.drop(labels=['account_name_en', 'type', 'status',
                                         'description', 'campeny_gool', 'date_created', 'is_GOV_campeny',
                                         'limitations', 'breaks_the_rules', 'last_year', 'city', 'street_name',
                                         'home_number', 'pin', 'mailbox', 'country', 'person_name', 'substatus',
                                         'what_is'], axis=1)


assciation_df.rename(columns={
    "שם עמותה בעברית": "Account_Name",
    "מספר עמותה": "Business_Number"
}, inplace=True)
assciation_df = assciation_df.drop(labels=['תאריך רישום עמותה',
                                           'שם עמותה באנגלית', 'תאריך עדכון סטטוס', 'סטטוס עמותה',
                                           'סיווג פעילות ענפי', 'תחום פעילות משני', 'שנת דיווח דוח כספי אחרון',
                                           'מחזור כספי (הכנסות)', 'סך הוצאות העמותה', 'כמות מתנדבים',
                                           'כמות עובדים', 'מספר חברי עמותה', 'איזורי פעילות', 'שנת דיווח אחרונה',
                                           'שם אגודה עותומנית', 'כתובת - ישוב', 'כתובת - רחוב',
                                           'כתובת - מספר דירה', 'כתובת - מיקוד', 'מטרות עמותה', 'Column1'], axis=1)

# %%
companies_in_liquidation_df.rename(columns={
    'שם חברה': "Account_Name",
    "מספר חברה": "Business_Number"
}, inplace=True)
companies_in_liquidation_df = companies_in_liquidation_df.drop(labels=['שם באנגלית', ' סוג תאגיד', 'סטטוס חברה',
                                                                       'אישור בקשת הפירוק', 'מועד החיסול הצפוי', 'תת סטטוס', 'מפרה', 'שם עיר',
                                                                       'שם רחוב', 'מספר בית', 'מיקוד', 'ת.ד.', 'מדינה', 'אצל', 'Column1'], axis=1)

#%%
our_companies_df = our_companies_df.drop(labels=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8',
                                                 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'], axis=1)

our_companies_df["Business_Number"] = pd.to_numeric(our_companies_df["Business_Number"], errors='coerce')
# our_companies_df["Business_Number"].astype('int64')


result = pd.DataFrame(columns=["Supplier_Id",
                               "Business_Number",
                               "Account_Number",
                               "Account_Name"])
wrong_Business_Number = pd.DataFrame(
    data=None, columns=our_companies_df.columns)


# %%

companies_and_assciation_df = pd.concat(
    [companies_df, assciation_df, companies_in_liquidation_df, AGUDOT_df], ignore_index=True)
companies_and_assciation_df = companies_and_assciation_df.drop(labels=['account_name_en', 'type', 'status',
                                                                       'description', 'campeny_gool', 'date_created', 'is_GOV_campeny',
                                                                       'limitations', 'breaks_the_rules', 'last_year', 'city', 'street_name',
                                                                       'home_number', 'pin', 'mailbox', 'country', 'person_name', 'substatus',
                                                                       'what_is', 'תאריך רישום עמותה', 'שם עמותה באנגלית', 'תאריך עדכון סטטוס',
                                                                       'סטטוס עמותה', 'סיווג פעילות ענפי', 'תחום פעילות משני',
                                                                       'שנת דיווח דוח כספי אחרון', 'מחזור כספי (הכנסות)', 'סך הוצאות העמותה',
                                                                       'כמות מתנדבים', 'כמות עובדים', 'מספר חברי עמותה', 'איזורי פעילות',
                                                                       'שנת דיווח אחרונה', 'שם אגודה עותומנית', 'כתובת - ישוב', 'כתובת - רחוב',
                                                                       'כתובת - מספר דירה', 'כתובת - מיקוד', 'מטרות עמותה', 'Column1'], axis=1)


# 726561
# 723646 sort

# 730696
# 727778 sort

# %%
good_index = 0
for ind_row in range(len(our_companies_df)):
    business_number = our_companies_df.loc[ind_row]["Business_Number"]
    name = companies_and_assciation_df[companies_and_assciation_df["Business_Number"]
                                       == business_number]
    if name.empty:
        wrong_Business_Number.loc[wrong_Business_Number.shape[0]
                                  ] = our_companies_df.loc[ind_row]
        continue

    name = name.iloc[0][1]
    result.loc[good_index] = our_companies_df.loc[ind_row]["Supplier_Id"].astype(
        'int64'), business_number, 0, name
    good_index += 1


# %%
wrong_Business_Number["why"] = ""
for ind_row in range(wrong_Business_Number.shape[0]):
    name = wrong_Business_Number.loc[ind_row]["Account_Name"]
    business_number = wrong_Business_Number.loc[ind_row]["Business_Number"]
    if business_number == nan
    if len(str(business_number)) != 9:
        wrong_Business_Number.loc[ind_row]["why"] = "short_num"
    if str(business_number)[:2] not in VALID_FREFIX:
        wrong_Business_Number.loc[ind_row]["why"] = "frefix_not_valid"
    if business_number in companies_in_liquidation_df["Business_Number"].unique():
        wrong_Business_Number.loc[ind_row]["why"] = "companie_in_liquidation"


# %%


def fing_by_name(name):
    mask = companies_and_assciation_df["Account_Name"].str.contains(
        name, na=False, regex=False)

    display(companies_and_assciation_df[mask])
# %%
