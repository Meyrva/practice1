import json

with open('sample-data.json', 'r') as file:
    sample_data = json.load(file)

attributes1 = sample_data['imdata'][0]['l1PhysIf']['attributes']

attributes2 = sample_data['imdata'][1]['l1PhysIf']['attributes']

attributes3 = sample_data['imdata'][2]['l1PhysIf']['attributes']

print(attributes1['dn'],attributes1['descr'],attributes1['speed'],attributes1['mtu'])
print(attributes2['dn'],attributes2['descr'],attributes2['speed'],attributes2['mtu'])
print(attributes3['dn'],attributes3['descr'],attributes3['speed'],attributes3['mtu'])