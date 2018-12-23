from typing import Dict, Any  # noqa


# TODO: Separate dev, test and prod configs into different files.
# TODO: Pass environment as a CLI command and then choose that environment's config file.
coinbase = {
    'url': 'https://api-public.sandbox.pro.coinbase.com',
    "websocket-feed": "wss://ws-feed-public.sandbox.pro.coinbase.com",
    "accounts": {
        "btc": "25fc4fbb-8d7f-42f5-b7c0-d826d0e1ed3f",
        "ltc": "e6f22960-1ddc-4f00-a095-8ed435456176",
        "eth": "6090e7d3-5e9a-4f58-9619-4b4e146fdf50",
        "usd": "e6a8d351-027e-487f-94e7-985a9a075090"
    },
    'passphrase': 'bf4zovy42ca',
    'secret_key': 'K+0gUKEBKTZ0SWIqq3PxVjCjvf+HTPAnnffW/aCDtlbYxKDBKM2Mec8Apfr3oxrV4x6urdvoXye5oBJuC/6XOA==',
    'access_key': '309832aa37a7698c9e1e63fd4322a094',
}  # type: Dict[str, Any]

aws = {
        "s3": {
            "bucket": "algo-trading-config-bucket",
            "key": "dev/config.json"
        },
        "sqs": {
            "queue-name": "algo_trading_test_queue.fifo"
        },
}  # type: Dict[str, Dict[str, Any]]

db = {
    'mongodb': {
        'host': 'localhost',
        'port': 27017,
        'database': 'algotrader',
    }
}
