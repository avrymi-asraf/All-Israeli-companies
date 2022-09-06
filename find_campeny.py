# %%
import pandas as pd
import numpy as np
all_companies_df = pd.read_csv("All_Campenes.csv")
our_companies_df = pd.read_csv("our_companies.csv")
all_assciation_df = pd.read_csv("all_assciation.csv")
VALID_FREFIX = ["5"+str(i) for i in range(10)]


# %%
all_companies_df.columns = [
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
our_companies_df.columns = [
    "Supplier_Id",
    "Business_Number",
    "Account_Number",
    "Account_Name"]
result = pd.DataFrame(columns=["Supplier_Id",
                               "Business_Number",
                               "Account_Number",
                               "Account_Name"])
wrong_Business_Number = df2 = pd.DataFrame(
    data=None, columns=our_companies_df.columns)
all_companies_df["Business_Number"] = all_companies_df["Business_Number"].astype(
    'int64')
our_companies_df["Business_Number"] = our_companies_df["Business_Number"].astype(
    'int64')
all_assciation_df.rename(columns={
    "שם עמותה בעברית": "Account_Name",
    "מספר עמותה": "Business_Number"
    }, inplace=True)
companies_and_assciation_df = pd.concat(
    [all_companies_df, all_assciation_df], ignore_index=True)
companies_and_assciation_df.drop(labels=['account_name_en', 'type', 'status',
       'description', 'campeny_gool', 'date_created', 'is_GOV_campeny',
       'limitations', 'breaks_the_rules', 'last_year', 'city', 'street_name',
       'home_number', 'pin', 'mailbox', 'country', 'person_name', 'substatus',
       'what_is', 'תאריך רישום עמותה', 'שם עמותה באנגלית', 'תאריך עדכון סטטוס',
       'סטטוס עמותה', 'סיווג פעילות ענפי', 'תחום פעילות משני',
       'שנת דיווח דוח כספי אחרון', 'מחזור כספי (הכנסות)', 'סך הוצאות העמותה',
       'כמות מתנדבים', 'כמות עובדים', 'מספר חברי עמותה', 'איזורי פעילות',
       'שנת דיווח אחרונה', 'שם אגודה עותומנית', 'כתובת - ישוב', 'כתובת - רחוב',
       'כתובת - מספר דירה', 'כתובת - מיקוד', 'מטרות עמותה', 'Column1'],axis=1)

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
    # result.append(pd.DataFrame([our_companies_df.loc[ind_row]
    #                         ["Supplier_Id"], business_number, 0, name] ))
    good_index += 1


# %%
wrong_Business_Number["why"] = ""
for ind_row in range(wrong_Business_Number.shape[0]):
    name = wrong_Business_Number.loc[ind_row]["Account_Name"]
    business_number = wrong_Business_Number.loc[ind_row]["Business_Number"]
    if len(str(business_number)) != 9:
        wrong_Business_Number.loc[ind_row]["why"] = "short_num"
    if str(business_number)[:2] not in VALID_FREFIX:
        wrong_Business_Number.loc[ind_row]["why"] = "frefix_not_valid"


# %%
result.head()
# %%
result.to_csv("out.csv")
