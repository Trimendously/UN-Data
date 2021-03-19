from pandastable import Table
import matplotlib.pyplot as plt

def mean(df):
    df = df['Value']
    return df.mean()

def median(df):
    df = df['Value']
    return df.median()

def mode(df):
    df = df['Value']
    return df.mode()

def IQR(df):
    df = df['Value']
    q1 = df.quantile(.25)
    q3 = df. quantile(.75)
    return q3-q1

def variance(df):
    df = df['Value']
    return df.var()

def std(df):
    df = df['Value']
    return df.std()

def hist(df):
    df = df['Value']
    plt.interactive(True)
    plt.hist(df)
    plt.show(df)

def box(df):
    df = df['Value']
    plt.interactive(True)
    plt.boxplot(df)
    plt.show(df)

def pear(df):
    corr = df['Value'].corr(df['Year'],method = 'pearson',min_periods=1)
    return corr

def spear(df):
    corr = df['Value'].corr(df['Year'],method = 'spearman',min_periods=1)
    return corr

def kendall(df):
    corr = df['Value'].corr(df['Year'],method = 'kendall',min_periods=1)
    return corr

def hoeffding(df): #Error hoeffding not existing???
    corr = df['Value'].corr(df['Year'],method = 'hoeffding',min_periods=1)
    return corr

def scatter(df):
    plt.interactive(True)
    plot = df.plot.scatter(x='Year',y='Value',c='Black')
    plt.show(plot)
def vert(df):
    df = df['Value']
    plt.interactive(True)
    plt.boxplot(df)
    plt.show(df)
def hor(df):
    df = df['Value']
    plt.boxplot(df, vert = False)
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(rotation=25)
    plt.show()
