from typing import Optional

from pydantic import validator

from .utils import CamelModel

from mev_inspect.utils import hex_to_int

class Receipt(CamelModel):
    block_number: int
    transaction_hash: str
    transaction_index: int
    gas_used: int
    effective_gas_price: int
    cumulative_gas_used: int
    to: Optional[str]

    @validator(
        "block_number",
        "transaction_index",
        "gas_used",
        "effective_gas_price",
        "cumulative_gas_used",
        pre=True,
    )
    def maybe_hex_to_int(v):
        if isinstance(v, str):
            return hex_to_int(v)
        return v
