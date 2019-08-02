import os
from bart import Bart
from datadog import initialize, api

bart = Bart()
options = {
    'api_key': os.getenv("DD_API_KEY", "")
}
initialize(**options)

api.Metric.send(metric='bart.train_count', type='count', points=int(bart.train_count()))

all_est_deps = bart.etd("ALL")
origin = ""
dest = ""

for line in all_est_deps.splitlines():
    print(line)
    if line[0:10] == "Departures":
        origin = line[15:][0:-3].replace(" ", "_").replace("'", "")
    elif line[0:3] == "For":
        dest = line[21:][0:-1]
    elif line and line[0:3] != "Est":
        i = line.find("platform")
        platform = line[i+9:i+10]

        i = line.find("in ")
        min = line[i+3:][0:-9]

        if min != "Leaving":
            api.Metric.send(metric='bart.estimated_wait_time',
                            points=int(min),
                            tags=["origin:" + origin,
                                  "dest:" + dest,
                                  "platform:" + str(platform)])

