import sys
import getopt
import telnetlib
import re

class Memcached:
	def __init__(self, agentConfig, checksLogger, rawConfig):
                self.agentConfig = agentConfig
                self.checksLogger = checksLogger
                self.rawConfig = rawConfig

	def run(self):
		stats = {}

		host = "127.0.0.1"
		port = 11211

		telnet = telnetlib.Telnet()
		telnet.open(host, port)
		telnet.write('stats\r\n')

		out = telnet.read_until("END")
		
		telnet.write('quit\r\n')
		telnet.close()

		# Current / Total
		stats['curr_items'] = int(re.search("curr_items (\d+)", out).group(1))
		stats['total_items']  = int(re.search("total_items (\d+)", out).group(1))

		# Memory Usgae
		stats['limit_maxbytes'] = int(re.search("limit_maxbytes (\d+)", out).group(1))
		stats['bytes'] = int(re.search("bytes (\d+)", out).group(1))

		# Network Traffic
		stats['bytes_read'] = int(re.search("bytes_read (\d+)", out).group(1))
		stats['bytes_written'] = int(re.search("bytes_written (\d+)", out).group(1))

		# Connections
		stats['curr_connections'] = int(re.search("curr_connections (\d+)", out).group(1))
		stats['total_connections'] = int(re.search("total_connections (\d+)", out).group(1))

		# Hits / Misses
		stats['cmd_get'] = int(re.search("cmd_get (\d+)", out).group(1))
		stats['cmd_set'] = int(re.search("cmd_set (\d+)", out).group(1))
		stats['get_hits'] = int(re.search("get_hits (\d+)", out).group(1))
		stats['get_misses'] = int(re.search("get_misses (\d+)", out).group(1))
		stats['delete_hits'] = int(re.search("delete_hits (\d+)", out).group(1))
		stats['delete_misses'] = int(re.search("delete_misses (\d+)", out).group(1))
		stats['incr_hits'] = int(re.search("incr_hits (\d+)", out).group(1))
		stats['decr_hits'] = int(re.search("decr_hits (\d+)", out).group(1))
		stats['incr_misses'] = int(re.search("incr_misses (\d+)", out).group(1))
		stats['decr_misses'] = int(re.search("decr_misses (\d+)", out).group(1))

		# Evictions
		stats['evictions'] = int(re.search("evictions (\d+)", out).group(1))
		stats['reclaimed'] = int(re.search("reclaimed (\d+)", out).group(1))

		return stats
