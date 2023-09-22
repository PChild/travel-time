import tbapy
import googlemaps
import os
import pandas as pd
from ortools.sat.python import cp_model
from typing import List
import math
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from schedules import Schedule, FRCEvent
from tbaConsts import EventType
import chsSeasons

tba = tbapy.TBA(os.getenv('TBA_KEY'))
gmaps = googlemaps.Client(key=os.getenv("MAPS_KEY"))


@dataclass
class FRCTeam:
    key: str
    loc: str = ""


def buildTeamList(dist: str) -> List[FRCTeam]:
    return_list = []

    for team in tba.district_teams(dist):
        events = [e for e in tba.team_events(
            team=team.key, year=int(dist[:4])) if e.event_type == EventType.DISTRICT]
        if len(events) > 0:
            team_postal = " " + team.postal_code if team.postal_code is not None else ""
            addr = team.city + ", " + team.state_prov + team_postal
            return_list.append(FRCTeam(team.key, addr))

    return return_list


def buildTravelCosts(events: List[FRCEvent], teamList: List[FRCTeam], name='SIM'):
    origins = [team.loc for team in teamList]
    destinations = [event.loc for event in events]

    maxElements = 100
    eventCodes = [event.code for event in events]
    rowsPerChunk = math.floor(maxElements / len(eventCodes))
    numChunks = math.ceil(len(teamList) / rowsPerChunk)

    dist_data = []

    for chunk in range(0, numChunks):
        startIdx = chunk * rowsPerChunk
        stopIdx = (chunk + 1) * rowsPerChunk
        stopIdx = len(teamList) if stopIdx > len(teamList) else stopIdx

        matrix = gmaps.distance_matrix(
            origins[startIdx:stopIdx],
            destinations,
            mode="driving",
            language="en-US",
            units="imperial",
            departure_time=datetime.now(),
            traffic_model="pessimistic",
        )

        for team_idx, row in enumerate(matrix['rows']):
            dists = {'Team': teamList[startIdx + team_idx].key}
            for evt_idx, elem in enumerate(row['elements']):
                dists[eventCodes[evt_idx]] = round(
                    elem['duration']['value'] / 60)

            dist_data.append(dists)
    pd.DataFrame(dist_data).to_csv(
        './data/' + name + '_COSTS.csv', index=False)


def runSolver(sched: Schedule, costs: pd.DataFrame, name="SIM", minSize=26, maxSize=40, playsPerTeam=2, save=False, shouldPrint=True) -> int:
    eventsPerWeek = sched.getEventsPerWeek()

    numWeeks = len(eventsPerWeek)
    numEvents = max(eventsPerWeek)
    numTeams = len(costs)

    all_weeks = range(numWeeks)
    all_teams = range(numTeams)
    all_events = range(numEvents)

    model = cp_model.CpModel()

    slots = {}
    # Set up the play slot matrix
    for t in all_teams:
        for w in all_weeks:
            for e in all_events:
                slots[(t, w, e)] = model.NewBoolVar(
                    f"slots_t{t}_w{w}_e{e}")

    for t in all_teams:
        team_plays = []

        for w in all_weeks:
            # teams are only allowed to play one event per week
            model.Add(sum(slots[(t, w, e)]for e in all_events) <= 1)

            for e in all_events:
                team_plays.append(slots[(t, w, e)])

        # teams must play the same amount of events (typically 2)
        model.Add(sum(team_plays) == playsPerTeam)

    for w in all_weeks:
        # only iterate on as many events as there are per week
        for e in range(eventsPerWeek[w]):

            # send no more than max_size teams to an event
            model.Add(sum(slots[t, w, e] for t in all_teams) <= maxSize)
            # send at least min_Size teams to an event
            model.Add(sum(slots[t, w, e] for t in all_teams) >= minSize)

    travel_costs = []
    for t in all_teams:
        for w in all_weeks:
            for e in all_events:
                # If the event is invalid set cost extremely high
                if e >= eventsPerWeek[w]:
                    cost = 999999
                else:
                    team_val = costs.index[t]
                    event_val = sched.getEvent(w + 1, e).code

                    cost = costs.loc[team_val, event_val]
                travel_costs.append(cost * slots[(t, w, e)])

    model.Minimize(sum(travel_costs))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    res = []
    ret = np.nan
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        status_str = 'Optimal solution' if status == cp_model.OPTIMAL else 'Feasible solution'
        if shouldPrint:
            print(status_str, "for", name,
                  f"\t total travel time = {solver.ObjectiveValue()}\n")
        ret = int(solver.ObjectiveValue())
        for t in all_teams:
            obj = {'Team': costs.index[t], 'E1': 0, 'E2': 0}
            for w in all_weeks:
                for e in all_events:
                    if solver.BooleanValue(slots[(t, w, e)]):
                        if obj['E1'] == 0:
                            # w + 1 used because matrix is zero indexed
                            obj['E1'] = sched.getEvent(w + 1, e).code
                            obj['E1_COST'] = costs.loc[obj['Team'], obj['E1']]
                        else:
                            obj['E2'] = sched.getEvent(w + 1, e).code
                            obj['E2_COST'] = costs.loc[obj['Team'], obj['E2']]
            res.append(obj)
        if save:
            pd.DataFrame(res).to_csv('./data/' + name +
                                     '_ASSIGNMENTS.csv', index=False)
    else:
        if shouldPrint:
            print("No solution found.")
    return ret


def main():

    generateTravelCosts = False

    if generateTravelCosts:
        teamList = buildTeamList('2023chs')
        buildTravelCosts(events=chsSeasons.all_events,
                         teamList=teamList, name="2024chs")

    costs = pd.read_csv('./data/2024chs_COSTS.csv', index_col=0)

    for sched in chsSeasons.options2024:
        runSolver(sched, costs, sched.name, save=True)


if __name__ == "__main__":
    main()
