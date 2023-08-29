from sqlalchemy import orm

from typing import List, Optional

from schemas.blocks import Block
from schemas.receipts import Receipt
from schemas.traces import Trace

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
