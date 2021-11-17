#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅


# project modules
from common.logger.log_handler import LogHandler
from itdashboard_handler.it_dashboard import *


if __name__ == '__main__':
    open_browser()
    click_dive_in()
    get_all_agencies()
    click_agency()
    get_agency_investment_table()
    uii_link_rows = get_all_uii_elements()

    current_url = open_another_window()
    for row in uii_link_rows:
        download_business_case(row, current_url)
