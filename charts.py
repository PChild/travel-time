import pandas as pd
import chsSeasons
from matplotlib import pyplot as plt
import numpy as np


def boxPlotCompare(labels):
    boxData = []
    for season in chsSeasons.options2024:
        assigns = pd.read_csv('./data/' + season.name +
                              '_ASSIGNMENTS.csv')
        boxData.append(assigns.TOTAL_COST)
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


def eventSizePlot(labels):
    eventSizeData = {}
    for season in chsSeasons.options2024:
        eventSizeData[season.name] = {}
        for event in season.getAllEvents():
            if event.code not in eventSizeData[season.name]:
                eventSizeData[season.name][event.code] = 0

        assigns = pd.read_csv('./data/' + season.name + '_ASSIGNMENTS.csv')

        for row in assigns.iterrows():
            eventSizeData[season.name][row[1].E1] += 1
            eventSizeData[season.name][row[1].E2] += 1

    plt.style.use('pchild.style')
    fig = plt.figure(figsize=(21, 15), dpi=100, layout='tight')
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for idx, season in enumerate(eventSizeData):
        heights = [eventSizeData[season][event]
                   for event in eventSizeData[season]]
        x_vals = np.arange(1, len(eventSizeData[season]) + 1, 1)
        plt.subplot(2, 3, idx + 1)
        plt.bar(x=x_vals, height=heights)
        plt.xticks(x_vals, [e for e in eventSizeData[season]],
                   rotation=45, rotation_mode='anchor', ha='right')

        for i, x in enumerate(x_vals):
            plt.text(x, heights[i], heights[i],
                     color='w', ha='center', va='top', fontsize=18)

        if idx % 3 != 0:
            plt.tick_params(left=False)
            plt.gca().set(yticklabels=[])
        else:
            plt.ylabel("Number of Teams")
        plt.title(labels[idx], fontsize=24)
    plt.suptitle('Comparison of Schedules with No Minimum Event Size')
    plt.show()


def main():
    labels = ["Real", "Edgewater", "Alexandria",
              "Six Events", "Bethesda", "Swap Ashland"]
    # eventSizePlot(labels)
    boxPlotCompare(labels)


if __name__ == "__main__":
    main()
