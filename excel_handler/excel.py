#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅

# std lib
import os

# project modules
from common import OUTPUT_PATH
from common.config_parser.config_manager import ConfigManager
from common.logger.log_handler import LogHandler

# rpa modules
from RPA.Excel.Application import Application
from RPA.Excel.Files import Files


config = ConfigManager()
log = LogHandler()
excel = Files()
workbook_name = 'workbook.xlsx'


def create_workbook():
    try:
        excel.create_workbook(workbook_name)
    except Exception as e:
        log.error(f"Failed to create workbook: {str(e)}")


def write_agencies_tiles(data):
    try:
        excel.create_worksheet(name='agencies_tiles')
        excel.set_worksheet_value(row=1, column=1, value='agency')
        excel.set_worksheet_value(row=1, column=2, value='tile')
        row = 2
        for agency, tile in data:
            excel.set_worksheet_value(row=row, column=1, value=agency)
            excel.set_worksheet_value(row=row, column=2, value=tile)
            row += 1
    except Exception as e:
        log.error(f"Failed to write agencies tiles: {str(e)}")


def write_investment_table(data):
    try:
        excel.create_worksheet(name='investment_table')
        excel.set_worksheet_value(row=1, column=1, value=str(data))
        # excel.set_worksheet_value(row=1, column=2, value='tile')
        # row = 2
        # for agency, tile in data:
        #     excel.set_worksheet_value(row=row, column=1, value=agency)
        #     excel.set_worksheet_value(row=row, column=2, value=tile)
        #     row += 1
    except Exception as e:
        log.error(f"Failed to write agencies tiles: {str(e)}")


def save_excel():
    excel.save_workbook(os.path.join(OUTPUT_PATH, workbook_name))
    excel.close_workbook()
