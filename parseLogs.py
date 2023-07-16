# Simple way to read a whole directory full of logs into a pandas data
# frame. The date parsing is what makes it really slow...maybe disable it?

from datetime import datetime
import pandas as pd
import re

# 2984 2021-04-29 23:44:41.184 debug2: fd 3 setting O_NONBLOCK


from datetime import datetime

def date_parser(value1, value2):
  """
  Ignore the timezone...
  """
  return datetime.strptime(value1,
    "[%d/%b/%Y:%H:%M:%S")

def getValue(data, key, default):
  if key in data.keys():
    return data[key]
  else: 
    return default

all_logs = None

# Get the files
file = "/Users/someuser/Downloads/sshlog.log"
# header = ['computer', 'timestamp', 'user', 'pid', 'ppid', 'cli', 'parent cli', 'description']
regex = re.compile(r'(?P<process>\d{1,4})\ (?P<timestamp>\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}\.\d{3})\ (?P<loglevel>[a-z]+\w)?[:\ ]?(?P<message>.+)')

pandaEvents = []

with open(file) as f:
  for row in f:
    if row is None:
      continue
    try:
      pandaEvents.append(regex.search(row).groupdict())
    except:
      print(f'skipping: ${row}')


# for ev in events:
#   pandaEvents.append(
#     [
#       getValue(ev['Event']['System'], 'Computer', ''),
#       getValue(ev['Event']['EventData'], 'UtcTime', ''),
#       getValue(ev['Event']['EventData'], 'User', ''),
#       getValue(ev['Event']['EventData'], 'ProcessId', ''),
#       getValue(ev['Event']['EventData'], 'ParentProcessId', ''),
#       getValue(ev['Event']['EventData'], 'CommandLine', ''),
#       getValue(ev['Event']['EventData'], 'ParentCommandLine', ''),
#       getValue(ev['Event']['EventData'], 'Description', '')
#     ]
#   )

print(pandaEvents[1])

pd.set_option('display.max_colwidth', None)
df = pd.DataFrame.from_records(pandaEvents)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
df.head(5)

sorted = df.sort_index()
sorted.to_csv('sorted.csv')

top_procs = df[['message']]\
            .value_counts()\
            .rename_axis(['message'])\
            .reset_index(name='counts')
top_procs.head(10)

top_procs.to_csv('results.csv')

filtered = df[['message']]
# ('Connection closed by invalid user ? 192.168.1.17 port ? [preauth]')
