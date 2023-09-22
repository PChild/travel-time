import pandas as pd
import chsSeasons
from matplotlib import pyplot as plt
import numpy as np


def boxPlotCompare(boxData, labels):
    plt.style.use('pchild.style')
    fig = plt.figure(figsize=(21, 15), dpi=100, layout='tight')
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    data = pd.DataFrame(boxData, index=labels).transpose()
    meds = data.median(axis='index')
    meds.sort_values(inplace=True)
    data = data[meds.index]

    props = dict(boxes=colors[1], whiskers="k", medians="k", caps="k")
    data.boxplot(color=props, patch_artist=True)

    plt.grid(axis='x')
    plt.yticks(np.arange(0, 500, 50))
    plt.xticks(np.arange(1, 7, 1))
    plt.xlabel("Schedule")
    plt.ylabel("Total Travel Time per Team")
    plt.title("Comparison of 2024 CHS Schedules")
    plt.show()


def main():
    costs = pd.read_csv('./data/2024chs_COSTS.csv', index_col=0)

    boxData = []
    labels = ["Real", "Edgewater", "Alexandria",
              "Six Events", "Bethesda", "Swap Ashland"]
    for season in chsSeasons.options2024:
        assigns = pd.read_csv('./data/' + season.name +
                              '_ASSIGNMENTS.csv')

        boxData.append(assigns.TOTAL_COST)

    boxPlotCompare(boxData, labels)


if __name__ == "__main__":
    main()
