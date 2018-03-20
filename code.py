import pandas as pd
import statsmodels.formula.api as sm
import tkinter as tk


df = pd.read_excel("data.xls")

result = sm.ols(formula="Severity_index ~ Forest + Rain + Population + Urban_Population + Temperature_diff + Dam_Proximity + Complaints" ,
                data=df).fit()

a = pd.DataFrame(result.predict(df))
a['1']=df.District.copy()

print(a)
