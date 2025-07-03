import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['overweight'] = (( df['weight'] / ((df['height'] / 100) ** 2) ) > 25).astype(int)

# 3
df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)
# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    

    # 6
    df_cat = df_cat.groupby(['cardio', 'value', 'variable']).size().reset_index(name='total')
    

    # 7
    plot = sns.catplot(data=df_cat, x='variable', y='total', hue='cardio', kind='bar', col='value')
    # x --> x-axis contains cholesterol, smoke, alcohol, overweight, etc
    # y --> y-axis contains all the different counts of if the people have cholesterol, smoke, alc, etc
    # hue --> in the counts, it shows via two diff colours which people suffer from cardiovascular disease and which do not 
    # kind --> the kind of graph it is

    # 8
    fig = plot.fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 - Setting parameters for the dataframe
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & # diastolic pressure should always be higher than systolic
        (df['height'] >= df['height'].quantile(0.025)) & # get rid of ppl under the 2.5th percentile
        (df['height'] <= df['height'].quantile(0.975)) & # get rid of ppl over the 97.5th percentile
        (df['weight'] >= df['weight'].quantile(0.025)) & # same thing but for weight
        (df['weight'] <= df['weight'].quantile(0.975))   # same thing but for weight
    ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    fig, ax = plt.subplots(figsize=(12,9))

    # 15
    sns.heatmap(corr, mask=mask, ax=ax, annot=True, fmt='.1f')
    # annot = True --> shows the actual numbers instead of just colours
    # fmt='.1f' --> rounds to one decimal place


    # 16
    fig.savefig('heatmap.png')
    return fig
