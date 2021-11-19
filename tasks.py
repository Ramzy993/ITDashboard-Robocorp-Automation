#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅


# project modules
from common.logger.log_handler import LogHandler
from itdashboard_handler.it_dashboard import *
from excel_handler.excel import *


if __name__ == '__main__':
    open_browser()
    click_dive_in()
    agency_tile_list = get_all_agencies()

    create_workbook()
    write_agencies_tiles(agency_tile_list)

    click_agency()
    investment_table = get_agency_investment_table()
    write_investment_table(investment_table)

    save_excel()
    uii_link_rows = get_all_uii_elements()

    current_url = open_another_window()
    for row in uii_link_rows:
        download_business_case(row, current_url)
