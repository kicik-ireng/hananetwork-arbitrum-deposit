# hananetwork-arbitrum-deposit

ETH auto-deposit tool for Hanafuda on Arbitrum.

## Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install web3 python-dotenv rich
```

## Setup

1. Clone this repository
2. Create a `.env` file in the root directory with the following content:

```env
PRIVATE_KEY=your_private_key
WALLET_ADDRESS=your_wallet_address
```

3. Run the script:

```bash
python main.py
```

## Details

- **Network**: Arbitrum One  
- **Contract**: `depositETH()` at `0xC5bf05cD32a14BFfb705Fb37a9d218895187376c`  
- Customize **ETH amount per transaction** and **repeat count** via prompt

