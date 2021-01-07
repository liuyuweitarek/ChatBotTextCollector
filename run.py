"""
File: run.py
Author: YUWEI LIU
Institution:  Modeling and Informatics Laboratory
Version: v0.1.0
"""

from woo_server import WooServer
from threading import Thread
from rpyc.utils.server import ThreadedServer
import time, subprocess, os, rpyc, argparse, sys

class WooStatus(object):
    server_counter_verification = False
    server_ready = False
    server_close = True

class WooService(rpyc.Service):
    def exposed_server_ready(self, value=None):
        if value is not None:
            wMaster.server_ready = value
        return wMaster.server_ready
    def exposed_server_close(self, value=None):
        if value is not None:
            wMaster.server_close = value
        return wMaster.server_close
    def exposed_server_counter_verification(self, value=None):
        if value is not None:
            wMaster.server_counter_verification = value
        return wMaster.server_counter_verification

def launchService(Service, Port):
    parser_server = ThreadedServer(Service, port=Port, protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    t = Thread(target=parser_server.start)
    t.daemon = True
    t.start()
    return


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    
    # Load Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--W_rpyc_port', type=int, default=12345, help='Default:12345 \n Description:RPYC Service PORT need to be int 10000-65535')
    parser.add_argument('--W_webdriver_type', type=str, default='chrome', help='Support types: chrome')
    parser.add_argument('--W_base_url', type=str, default='https:\/\/wootalk.today', help='Support URLS: \"https:\/\/wootalk.today\"')
    parser.add_argument('--W_user_agent', type=str, default='user-agent=\"Mozilla\/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit\/535.19 (KHTML, like Gecko) Chrome\/18.0.1025.133 Mobile Safari/535.19\"')
    args = parser.parse_args()

    # Status Manager
    wMaster = WooStatus()

    while True:
        while wMaster.server_close:
            # Lauch Service
            time.sleep(3)
            launchService(WooService, args.W_rpyc_port)
            subprocess.Popen(['python3', path + '/woo_server/server.py',
                        '--W_rpyc_port', str(args.W_rpyc_port),
                        '--W_webdriver_type', args.W_webdriver_type],
                        stderr=sys.stderr, stdout=sys.stdout)

            # Wait until the process signals its ready to continue the main thread
            if not wMaster.server_ready:
                time.sleep(3)
        time.sleep(3)

