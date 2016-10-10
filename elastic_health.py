#!/usr/bin/python

"""Retrieve Elasticsearch Cluster Health and Stats.

This scripts is used to retrieve the health status of an Elasticsearch cluster and stats.
It will output the health as either red, yellow or green.
The cluster stats are CPU utilization percentage and JVM RAM usage.

Example:
   ./elastic_health.py --hosts 10.10.80.10 --username admin --password secret


"""

import argparse
from elasticsearch import Elasticsearch


cli_parser = argparse.ArgumentParser(prog='elastic_health.py',
                                     description='Elasticsearch Cluster health and CPU/RAM stats.')
cli_parser.add_argument('-i', '--hosts', required=True, help='host or hosts to connect to')
cli_parser.add_argument('-u', '--username', help='http_auth username')
cli_parser.add_argument('-pw', '--password', help='http_auth password')
cli_parser.add_argument('-p', '--port', default="9200", help='elasticsearch node connection port')
cli_arguments = cli_parser.parse_args()

es = Elasticsearch(cli_arguments.hosts,
                   http_auth=(cli_arguments.username, cli_arguments.password),
                   port=cli_arguments.port)

cluster_health = es.cluster.health()['status']
cluster_stats = es.cluster.stats()

print('The cluster\'s health status is: ', cluster_health)

print('Cluster CPU load: {}%\nCluster RAM utilization: {}%'.format(
    cluster_stats['nodes']['process']['cpu']['percent'],
    cluster_stats['nodes']['jvm']['mem']['heap_used_in_bytes'] /
    cluster_stats['nodes']['jvm']['mem']['heap_max_in_bytes'])
     )
