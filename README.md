# GRS Address Monitor

This is a simple proof of concept GRS address monitoring application. It should be provided with a watchlist of
addresses. The application will then monitor transactions on the blockchain and watch for deposits into the addresses
that are contained in the watch list.

### Watchlist format example

```json
{"addresses": ["n47gr2mkPfqXHYiWV7wrPSo3m5VdYV8JUU", "2My1Z5TAQRscU2BhJZQAEEF3D5gWsjui8s9"]}
```

### Application usage

#### Start groestlcoind

The application requires a connection to `groestlcoind`. An example of starting groestlcoind is as follows:
`groestlcoind -testnet -datadir=testnet -server -rpcuser=user -rpcpassword=pass -txindex=1`. This
will run groestlcoind on 127.0.0.1 and port 17766.

#### Running the application

To run the application execute `python monitor.py user pass` where `user` matches the `-rpcuser` for the RPC
user of your groestlcoind process and `pass` matches the `-rpcpassword` you set when starting groestlcoind.
