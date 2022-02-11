"""Coinbase view"""
__docformat__ = "numpy"

import logging
import os

from gamestonk_terminal.cryptocurrency.overview import coinbase_model
from gamestonk_terminal.decorators import log_start_end
from gamestonk_terminal.helper_funcs import (
    export_data,
    long_number_format,
    print_rich_table,
)
from gamestonk_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def display_trading_pairs(top: int, sortby: str, descend: bool, export: str) -> None:
    """Displays a list of available currency pairs for trading. [Source: Coinbase]

    Parameters
    ----------
    top: int
        Top n of pairs
    sortby: str
        Key to sortby data
    descend: bool
        Sort descending flag
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = coinbase_model.get_trading_pairs()
    df_data = df.copy()

    for col in [
        "base_min_size",
        "base_max_size",
        "min_market_funds",
        "max_market_funds",
    ]:
        df[col] = df[col].apply(lambda x: long_number_format(x))

    df = df.sort_values(by=sortby, ascending=descend).head(top)

    print_rich_table(
        df,
        headers=list(df.columns),
        show_index=False,
        title="Available Pairs for Trading",
    )
    console.print("")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "pairs",
        df_data,
    )