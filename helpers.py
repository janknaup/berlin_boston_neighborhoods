import locale
import numpy as np
import pandas as pd
from typing import AnyStr

def price_parse(pstring):
    """parses price strings removes USD symbol

    :param pstring: price string to parse
    :returns: floating point price value
    """
    if pstring.startswith('$'):
        return locale.atof(pstring[1:])
    else:
        return np.nan


def percent_parse(pstring):
    """parses percentage strings, scale to fraction

    :returns: floating point fraction value
    """
    if pstring.strip().endswith('%'):
        return int(pstring.strip()[:-1]) / 100
    else:
        return np.nan


def fit_prepare(df, target, numerics, categorcials, indicators=None):
    """prepares a data frame for model fitting

    :param df: data frame containing the data to be cleaned
    :param target: name of the fit target column (y)
    :param numerics: list of numerical columns to include
    :param categorcials: list of categorcial columns to include
    :param indicators: optional list of preexisting indicator columns to include
    :returns: DataFrame of predictor vectors X and Series of target values y
    """
    if target in numerics:
        num = list(numerics)
        num.remove(target)
        cat = categorcials
    else:
        num = numerics
        cat = list(categorcials)
        cat.remove(target)
    df_trg = df.dropna(subset=[target], axis=0)
    y = df_trg[target]
    X = df_trg[num].apply(lambda col: col.fillna(col.mean()))
    X = X.join(make_dummies(df_trg[cat]))
    if indicators is not None:
        for col in indicators:
            X = X.join(df_trg[col])
    return X, y


def make_dummies(df_trg):
    for idx, col in enumerate(df_trg.columns):
        if idx == 0:
            x = pd.get_dummies(df_trg[col], prefix=col, prefix_sep='_', dummy_na=True, drop_first=True)
        else:
            x = x.join(pd.get_dummies(df_trg[col], prefix=col, prefix_sep='_', dummy_na=True, drop_first=True))
    return x


def valid_value_intbool(val):
    """check if a vlaue is valid or NaN

    :param val:
    :return: 0 if val is NaN, 1 otherwise
    """
    if val is not np.nan:
        return 1
    else:
        return 0


def multicategorical_to_dummies(multi: pd.Series, sep: AnyStr = ',', include_nan: bool = False, skip_first=False,
                                strip_brackes: bool = True, strip_quotes: bool = True) -> pd.DataFrame:
    """split a column containing a variable number of categorcial labels into a set of bollean indicator column

    :param multi: multiple catagorical values column to split up
    :param sep: separator character between
    :param include_nan: create indicator column for NaN valued rows
    :param skip_first: drop first tag
    :param strip_brackes: strip brackets from column value
    :param strip_quotes: strip quotes from categorcial tags
    :return: data frame of 0/1 valued indicator columns for categorcial tags from input column
    """
    ssp = multi.str.split(sep, expand=True)
    ssp['indx'] = multi.index
    mlt = ssp.melt(id_vars='indx')
    mlt['value'] = mlt['value'].apply(lambda x: x.strip() if x is not None else np.nan)
    mlt.dropna(subset=['value'], inplace=True)
    if strip_brackes:
        mlt['value'] = mlt['value'].apply(lambda x: x.strip().strip('[](){}'))
    if strip_quotes:
        mlt['value'] = mlt['value'].apply(lambda x: x.strip().strip("'\""))
    mlt.drop_duplicates(subset=['indx', 'value'], inplace=True)
    pvt = mlt.pivot(index='indx', columns='value', values='variable')
    for col in pvt.columns:
        pvt[col] = pvt[col].apply(valid_value_intbool)
    pvt.rename(mapper=lambda x: multi.name + '_' + x, axis='columns', inplace=True)
    return pvt


def cross_distances(df_row: pd.DataFrame, df_col: pd.DataFrame, distance_function=None):
    """Calculate distances between overlapping numeric columns of

    :param df_row: input data frame that will be enumerated along rows
    :param df_col: input data frame that will be enumeratid along columns
    :param distance_function: function thjat will be called to calculate distances, use cartesian if None
    :return: data frame of cartesian distances between rows of input data frames
    """
    if distance_function is None:
        disf = lambda x1, x2: (np.sqrt(np.sum(np.power(x2-x2, 2))))
    else:
        disf = distance_function
    dist = pd.DataFrame(index=df_row.index)
    for colname, cvals in df_col.iterrows():
        dist[colname] = df_row.apply(lambda x: disf(x, cvals.values), axis='columns')
    return dist
