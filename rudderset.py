#!/usr/bin/env python
#
# Name:     rudder-set-node-props.py 
# Required: Python docopt module
# Author:   Dennis Cabooter <Dennis.Cabooter@snow.nl>
#

""" 
Add key=value properties to a Rudder node - multiple key=value properties

Usage: rudder-set-node-props.py [--node=<fqdn>] 

Options:
  -n --node=<fqdn>  The node's FQDN

"""

# Imports
import sys
import requests
import json
from docopt import docopt

# Main
def main():
  # Global vars
  api_url = "https://rudder.in.ac-nice.fr/rudder/api" # lien rudder
  api_token = "0T6F2jOgkT1DKuMxrSi0AJ1PXu8DDuI1" # ID API 
  nodes_url = "%s/latest/nodes" % (api_url) 
  #groups_url = "%s/lamachineIsa/groups" % (api_url)
  headers = {"X-API-Token": api_token, "Content-type": "application/json"}  

  # Parse options
  options = docopt(__doc__, options_first=True)
  node_name = options["--node"]

  # Get from API
  r = requests.get(nodes_url, headers=headers, verify=False)
 # g = requests.get(groups_url, headers=headers, verify=False)

  # Parse JSON
  j = json.loads(r.content) #recupere les nodes dans rudder

  # Define nodes
  nodes = j["data"]["nodes"]
  keys = []
  testok = 1

  # recuperer les donnees ISAWA (hostname et groupe minimum)	
  gg = json.load(open('/home/sta-infra/Documents/test.json'))
  node_isa = gg["data"]
  data_container = []
  machineIsa = "test"
  
  # Loop nodes
  for node in nodes:
      if (testok != 0):
        machineIsa = node_isa.pop()
	testok = 0
      if node["hostname"] == machineIsa["hostname"][0]:
	node_id = node["id"]
	node_hostname = node["hostname"]

  while len(machineIsa["groupe"]) != 0: #Changer keys par les liste groupe ISAWA
      # Populate dict
      data = {}
      data["name"] = machineIsa["groupe"].pop()
      data["value"] = "true"
      data_container.append(data)

  api_container = { "properties": data_container }
  node_url = "%s/latest/nodes/%s" % (api_url, node_id)
  requests.post(node_url, data=json.dumps(api_container), headers=headers, verify=False)

if __name__ == "__main__":
  main()
