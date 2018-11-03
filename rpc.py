import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BTCRPCClient(object):
    """
    RPC client for communicating with groestlcoind.
    """

    def __init__(self, username, password, host='127.0.0.1', port='17766'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def _make_request(self, rpcmethod, *args):
        """
        Handles formatting the request JSON that will be sent to groestlcoind.
        :param rpcmethod: The name of the RPC method to call on groestlcoind
        :param args: Additional arguments for the method
        :return: the deserialized JSON result of calling the RPC method on groestlcoind
        """
        logger.debug('Args %s', args)
        payload = {'method': rpcmethod, 'params': args, 'id': 'BTCRPCClient', 'jsonrpc': '1.0'}
        logger.debug('payload %s', payload)
        resp = self.session.post(self.service_url, json=payload)
        logger.debug('resp body: %s', resp.text)
        resp.raise_for_status()
        resp_json = resp.json()
        if resp_json.get('Error') is not None:
            logger.error('Error making RPC request: ', resp_json.get('Error'))
        return resp_json

    def getbestblockhash(self):
        """
        Queries groestlcoind for the tip of the blockchain hash
        :return: string hash of the tip of the block chain
        """
        resp_json = self._make_request('getbestblockhash')
        return resp_json.get('result')

    def getblock(self, blockhash, verbosity=2):
        """
        Queries groestlcoind for the data about block :blockhash:

        If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'.
        If verbosity is 1, returns an Object with information about block <hash>.
        If verbosity is 2, returns an Object with information about block <hash> and information about each transaction.

        :param blockhash: The hash of the block to lookup.
        :param verbosity: How verbose the response from groestlcoind should be.
        :return: The data for the block with hash :blockhash:
        """

        resp_json = self._make_request('getblock', blockhash, verbosity)
        return resp_json.get('result')

    def getblockhash(self, block_number):
        """

        :param block_number:
        :return: String hash of :block_number:
        """
        resp_json = self._make_request('getblockhash', block_number)
        return resp_json.get('result')

    def getblockcount(self):
        """
        Returns the number of blocks in the longest blockchain.
        :return: integer number of blocks in the longest blockchain
        """

        resp_json = self._make_request('getblockcount')
        return resp_json.get('result')

    def gettx(self, txid):
        resp_json = self._make_request('getrawtransaction', txid, 2)
        return resp_json.get('result')

    def sendtoaddress(self, address, amount):
        resp_json = self._make_request('sendtoaddress', address, amount)
        return resp_json.get('result')

    def create_raw_transaction(self, inputs, outputs):
        """
        Creates a raw, unsigned transaction
        :param inputs: list of dicts describing the inputs
        :param outputs: dictionary of address: btc_amount pairs
        :return: hex string of the transaction
        """
        resp_json = self._make_request('createrawtransaction', inputs, outputs)
        return resp_json.get('result')

    def sign_transaction(self, raw_tx):
        """
        Signs a transaction
        :param tx: Hex string of raw tx
        :return: Signed transaction
        """
        resp_json = self._make_request('signrawtransaction', raw_tx)
        return resp_json.get('result')

    def send_raw_transaction(self, signed_tx):
        """

        :param signed_tx:
        :return:
        """
        resp_json = self._make_request('sendrawtransaction', signed_tx)
        return resp_json.get('result')

    def list_unspent(self, addresses, min_conf=6, max_conf=9999999):
        """
        Returns a list of unspent transaction data
        [
            {
                "txid": "029c2eb4fb8c582ee884057e0f5e0cb1cee78b1a838f2a01541d2b63e13985e4",
                "vout": 0,
                "address": "mzrXS5ZgeLyEGSQZeYFBbfs61ZQZfMJtkX",
                "scriptPubKey": "76a9144d7a2c91ded4f5861ce46f98ba47c475debbfe3e88ac",
                "amount": 0.0999377,
                "confirmations": 35051,
                "spendable": true,
                "solvable": true,
                "safe": true
            }
        ]

        :param addresses:
        :param min_conf:
        :param max_conf:
        :return:
        """
        resp_json = self._make_request('listunspent', min_conf, max_conf, addresses)
        return resp_json.get('result')
