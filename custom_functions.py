import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as scs
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, make_scorer
from sklearn.model_selection import train_test_split, cross_val_score
from statsmodels.stats.diagnostic import het_breuschpagan, het_goldfeldquandt


# set seaborn styling
palette = sns.color_palette("Purples")
palette.reverse()
sns.set_palette(palette)
sns.set_style('darkgrid')

# calculate VIF 
def calculate_vif(df, target_col, show_res=False):
    x = df.drop(columns=[target_col])
    y = df[target_col]
    ols = sm.OLS(y, x).fit()
    if show_res:
        print(ols.summary())
    vif = 1 / (1 - ols.rsquared)
    return vif

# execute a SQLite query and return a dataframe
def make_frame_from_query(cur, query):
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [i[0] for i in cur.description]
    return df

# make an OLS model
def build_sm_ols(df, features_to_use, target, add_constant=False, show_summary=True):
    X = df[features_to_use]
    if add_constant:
        X = sm.add_constant(X)
    y = df[target]
    ols = sm.OLS(y, X).fit()
    if show_summary:
        print(ols.summary())
    return ols


# assumptions of ols
# residuals are normally distributed
def check_residuals_normal(ols):
    residuals = ols.resid
    t, p = scs.shapiro(residuals)
    if p <= 0.05:
        return False
    return True

# residuals are homoskedasticitous
def check_residuals_homoskedasticity(ols):
    import statsmodels.stats.api as sms
    resid = ols.resid
    exog = ols.model.exog
    lg, p, f, fp = sms.het_breuschpagan(resid=resid, exog_het=exog)
    if p >= 0.05:
        return True
    return False

def check_vif(df, features_to_use, target_feature):
    ols = build_sm_ols(df=df, features_to_use=features_to_use, target=target_feature, show_summary=False)
    r2 = ols.rsquared
    return 1 / (1 - r2)
 
# no multicollinearity in our feature space
def check_vif_feature_space(df, features_to_use, vif_threshold=3.0):
    all_good_vif = True
    for feature in features_to_use:
        target_feature = feature
        _features_to_use = [f for f in features_to_use if f!=target_feature]
        vif = check_vif(df=df, features_to_use=_features_to_use, target_feature=target_feature)
        if vif >= vif_threshold:
            print(f"{target_feature} surpassed threshold with vif={vif}")
            all_good_vif = False
        else:
             print(f'No multicollinearity detected for {target_feature}.')
    return all_good_vif
        
def check_model(df, 
                features_to_use, 
                target_col, 
                add_constant=False, 
                show_summary=True, 
                vif_threshold=3.0):
    has_multicollinearity = check_vif_feature_space(df=df, 
                                                    features_to_use=features_to_use, 
                                                    vif_threshold=vif_threshold)
    if not has_multicollinearity:
        print("Model contains multicollinear features")
    
    # build model 
    ols = build_sm_ols(df=df, features_to_use=features_to_use, 
                       target=target_col, add_constant=add_constant, 
                       show_summary=show_summary)
    
    # check residuals
    resids_are_norm = check_residuals_normal(ols)
    resids_are_homo = check_residuals_homoskedasticity(ols)
    
    if not resids_are_norm:
        print("[n] Residuals are not normally distributed")
    if not resids_are_homo:
        print("[n] Residuals are not homoskedastic")
    return ols


def plot_residuals_and_qq(ols):
    residuals = ols.resid
    fig, axs = plt.subplots(ncols=2, figsize=(18, 6.5))
    sm.graphics.qqplot(residuals, dist=scs.norm, line='45', fit=True, ax=axs[0])
    axs[0].set_title('QQ Plot of Residuals', fontsize='x-large')
    sns.distplot(residuals, bins=50, ax=axs[1])
    axs[1].set_title('Distribution of Residuals', fontsize='x-large')
    plt.show()

def hetersked_plot(df, model, target):
    pred_val = model.fittedvalues.copy()
    true_val = df[target].values.copy()
    residual = true_val - pred_val
    fig, ax = plt.subplots(figsize=(10,5))
    homo_plot = ax.scatter(pred_val, residual)
    ax.axhline(color='red') 
    plt.show()

