from typing import Dict, Any  # noqa


coinbase = {
    'url': 'https://api-public.sandbox.pro.coinbase.com',
    'passphrase': 'bf4zovy42ca',
    'secret_key': 'K+0gUKEBKTZ0SWIqq3PxVjCjvf+HTPAnnffW/aCDtlbYxKDBKM2Mec8Apfr3oxrV4x6urdvoXye5oBJuC/6XOA==',
    'access_key': '309832aa37a7698c9e1e63fd4322a094',
}

aws = {
    "dev": {
        "s3": {
            "bucket": "algo-trading-config-bucket",
            "key": "dev/config.json"
        },
        "sqs": {
            "queue-name": "algo_trading_test_queue.fifo"
        },
        "coinbase": {
            "base-endpoint": "https://api-public.sandbox.pro.coinbase.com",
            "websocket-feed": "wss://ws-feed-public.sandbox.pro.coinbase.com",
            "accounts": {
                "btc": "25fc4fbb-8d7f-42f5-b7c0-d826d0e1ed3f",
                "ltc": "e6f22960-1ddc-4f00-a095-8ed435456176",
                "eth": "6090e7d3-5e9a-4f58-9619-4b4e146fdf50",
                "usd": "e6a8d351-027e-487f-94e7-985a9a075090"
            }
        }
    },
    "prod": {
        "s3": {
            "bucket": "algo-trading-config-bucket",
            "key": "prod/config.json"
        },
        "coinbase": {
            "base-endpoint": "https://api.pro.coinbase.com",
            "websocket-feed": "wss://ws-feed.pro.coinbase.com",
            "accounts": {
                "btc": "0a36989e-7306-43e6-ad40-89d8fa591884",
                "ltc": "e6f22960-1ddc-4f00-a095-8ed435456176",
                "eth": "543f1ce9-df3e-4129-b39f-99f4564c1497",
                "usd": "ced494de-2f42-4af3-8eb6-51987a2eaf3c"
            }
        }
    }
}  # type: Dict[str, Dict[str, Any]]
