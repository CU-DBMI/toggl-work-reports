import os
import pprint
from datetime import datetime, timedelta

from toggl.TogglPy import Toggl

# init a pretty printer
pp = pprint.PrettyPrinter(indent=4)

# gather the api token from environment
api_token = os.environ["TOGGL_API_TOKEN"]

# form the toggl client
toggl = Toggl()
toggl.setAPIKey(api_token)


def get_flattened_summary_data(toggl: Toggl, date: str) -> dict:
    """
    Find and return data structure which includes flattened
    summary stats from toggl workday based on date str provided
    """

    # gather a workspace for making report requests
    workspaces = toggl.getWorkspaces()
    default_workspace_id = workspaces[0]["id"]

    # specify that we want reports from this week
    req_data = {
        "workspace_id": default_workspace_id,
        "since": date,
        "until": date,
    }

    # gather the report data
    report_data = toggl.getSummaryReport(req_data)

    # filter the report data
    filtered_report_data = [
        {"title": item["title"]["project"].split(" - ")[0], "time": item["time"]}
        for item in report_data["data"]
    ]

    # group time values together
    grouped = {}
    for item in filtered_report_data:
        if item["title"] not in grouped.keys():
            grouped[item["title"]] = item["time"]
        else:
            grouped[item["title"]] += item["time"]

    # percentage of total time for grouped values
    return {
        key: round((val / (report_data["total_grand"])) * 100, 2)
        for key, val in grouped.items()
    }


# gather the last 3 days of work as flattened report data
for num in range(1, 4):
    date = (datetime.now() - timedelta(num)).strftime("%Y-%m-%d")
    print(date)
    pp.pprint(get_flattened_summary_data(toggl, date))
