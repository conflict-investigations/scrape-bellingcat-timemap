import json
from urllib import request

BASE_ENDPOINT = 'https://ukraine.bellingcat.com/ukraine-server/api/ukraine'
EVENTS_ENDPOINT = BASE_ENDPOINT + '/export_events/deeprows'
SOURCES_ENDPOINT = BASE_ENDPOINT + '/export_sources/deepids'
ASSOCIATIONS_ENDPOINT = BASE_ENDPOINT + '/export_associations/deeprows'

data = {}
data['events'] = json.loads(
    request.urlopen(EVENTS_ENDPOINT).read().decode('utf-8'))
data['sources'] = json.loads(
    request.urlopen(SOURCES_ENDPOINT).read().decode('utf-8'))
data['associations'] = json.loads(
    request.urlopen(ASSOCIATIONS_ENDPOINT).read().decode('utf-8'))
# For testing:
# def mock(item):
#     with open(f"{item}.json", 'r') as f:
#         data[item] = json.load(f)
# mock('events')
# mock('sources')
# mock('associations')

def get_source(source_id, event_id):
    src = data['sources'].get(source_id)
    return dict(id=event_id, path=src.get('paths')[0],
                description=src.get('description'))
def get_association(association):
    assoc = list(filter(None,
        (a for a in data['associations'] if a.get('id') == association)
    ))[0]
    return {
        'key': assoc['filter_paths'][0],
        'value': assoc['filter_paths'][1],
    }
def mangle(e):
    eventid = e.get('id')
    return dict(
        id=eventid,
        date=e.get('date'),
        latitude=e.get('latitude'),
        longitude=e.get('longitude'),
        location=e.get('location'),
        description=e.get('description'),
        sources=[get_source(s, eventid) for s in e.get('sources')],
        filters=[get_association(a) for a in e.get('associations')],
    )


events = [mangle(e) for e in data['events']]
print(json.dumps(events, indent=None))

"""
Reference:
https://github.com/bellingcat/ukraine-timemap/blob/590cb66a2b069fc3041662404bb0e34c896501a7/src/components/controls/DownloadButton.js#L37-L63

const exportEvents = events.map((e) => {
  return {
    id: e.civId,
    date: e.date,
    latitude: e.latitude,
    longitude: e.longitude,
    location: e.location,
    description: e.description,
    sources: e.sources.map((id) => {
      const s = sources[id];
      return {
        id,
        path: s.paths[0],
        description: s.description,
      };
    }),
    filters: e.associations.map((a) => {
      return {
        key: a.filter_paths[0],
        value: a.filter_paths[1],
      };
    }),
  };
});
return JSON.stringify(exportEvents);
"""
