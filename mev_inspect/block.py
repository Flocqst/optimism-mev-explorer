# Setup
from dotenv import load_dotenv
import os

from sqlalchemy import orm
from web3 import Web3

from typing import List, Optional

from schemas.blocks import Block
from schemas.receipts import Receipt
from schemas.traces import Trace

load_dotenv()
alchemy_url = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Print if web3 is successfully connected
print(w3.is_connected())

# Get the latest block number
latest_block = w3.eth.block_number
print(latest_block)

# Get the balance of an account
balance = w3.eth.get_balance('0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
print(balance)

# Get the information of a transaction
tx = w3.eth.get_transaction('0xbde52a2e10c85ef4779244cfb786ce25dea1cb11639cb997b858e6fb6cde06c5')
print(tx)

blockz = w3.eth.get_block(latest_block)
print(blockz)

"""
async def create_from_block_number(
    w3: Web3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> Block:
    block_timestamp, receipts, traces, base_fee_per_gas = await asyncio.gather(
        _find_or_fetch_block_timestamp(w3, block_number, trace_db_session),
        _find_or_fetch_block_receipts(w3, block_number, trace_db_session),
        _find_or_fetch_block_traces(w3, block_number, trace_db_session),
        _find_or_fetch_base_fee_per_gas(w3, block_number, trace_db_session),
    )

    miner_address = _get_miner_address_from_traces(traces)

    return Block(
        block_number=block_number,
        block_timestamp=block_timestamp,
        miner=miner_address,
        base_fee_per_gas=base_fee_per_gas,
        traces=traces,
        receipts=receipts,
    )
"""

async def _find_or_fetch_block_timestamp(
    w3,
    block_number: int,
    trace_db_session: Optional[orm.Session],
) -> int:
    if trace_db_session is not None:
        existing_block_timestamp = _find_block_timestamp(trace_db_session, block_number)
        if existing_block_timestamp is not None:
            return existing_block_timestamp

    return await _fetch_block_timestamp(w3, block_number)

async def _fetch_block_timestamp(w3, block_number: int) -> int:
    block_json = await w3.eth.get_block(block_number)
    return block_json["timestamp"]


async def _fetch_block_receipts(w3, block_number: int) -> List[Receipt]:
    receipts_json = await w3.eth.get_block_receipts(block_number)
    return [Receipt(**receipt) for receipt in receipts_json]


async def _fetch_block_traces(w3, block_number: int) -> List[Trace]:
    traces_json = await w3.eth.trace_block(block_number)
    return [Trace(**trace_json) for trace_json in traces_json]

def _find_block_timestamp(
    trace_db_session: orm.Session,
    block_number: int,
) -> Optional[int]:
    result = trace_db_session.execute(
        "SELECT block_timestamp FROM block_timestamps WHERE block_number = :block_number",
        params={"block_number": block_number},
    ).one_or_none()

    if result is None:
        return None
    else:
        (block_timestamp,) = result
        return block_timestamp
