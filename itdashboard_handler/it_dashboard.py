#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅

# std lib
import time
from datetime import timedelta
import re

# project modules
from common import OUTPUT_PATH
from common.config_parser.config_manager import ConfigManager
from common.logger.log_handler import LogHandler

# rpa modules
from RPA.Browser.Selenium import Selenium


config = ConfigManager()
log = LogHandler()
selenium = Selenium()
selenium.set_download_directory(directory=OUTPUT_PATH, download_pdf=True)


def open_browser():
    url = config.get_str('ID_DASHBOARD', 'url')
    log.info(f"trying to open {url}")
    try:
        selenium.open_available_browser(url, alias="main")
        locator = r"xpath:/html/body/header/nav/div[1]/div[1]/a"
        selenium.wait_until_element_is_visible(locator=locator)
        log.info(f"{url} opened successfully")
    except Exception as e:
        log.error(f"failed to open {url} due to: {str(e)}")


def click_dive_in():
    try:
        # locator = "xpath://a[@class='navbar-brand trend_sans_oneregular']"
        locator = "CSS: #node-23 > div > div > div > div > div > div > div > a"
        selenium.click_element_when_visible(locator=locator)
        selenium.wait_until_element_is_visible(locator="id:agency-tiles-container")
    except Exception as e:
        log.error(f"failed to locate dive in button due to: {str(e)}")


def click_agency():
    agency_to_click = config.get_str('ID_DASHBOARD', 'agency_to_click')
    for section in range(1, 50):
        if selenium.is_element_visible(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section})"):
            for agency in range(1, 10):
                if selenium.is_element_visible(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency})"):
                    if agency_to_click == selenium.get_text(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency}) > div > div > div > div:nth-child(2) > a > span.h4.w200"):
                        try:
                            selenium.click_link(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency}) > div > div > div > div:nth-child(2) > a")
                            return
                        except:
                            log.critical(f"failed to find this agency: {agency_to_click}")
                else:
                    break
        else:
            break


def get_all_agencies():
    try:
        # locator = "id:agency-tiles-container"
        # agency_tiles = selenium.find_element(locator=locator)
        agency_tile_list = []
        for section in range(1, 50):
            if selenium.is_element_visible(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section})"):
                for agency in range(1, 10):
                    if selenium.is_element_visible(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency})"):
                        agency_tile_list.append((
                            selenium.get_text(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency}) > div > div > div > div:nth-child(2) > a > span.h4.w200"),
                            selenium.get_text(locator=f"CSS:#agency-tiles-widget > div > div:nth-child({section}) > div:nth-child({agency}) > div > div > div > div:nth-child(2) > a > span.h1.w900"),
                        ))
                    else:
                        break
            else:
                break
        return agency_tile_list
    except Exception as e:
        log.error(f"failed to agencies due to: {str(e)}")


def get_agency_investment_table():
    try:
        selenium.wait_until_element_is_visible(locator="CSS:#investments-table-object_wrapper > div.dataTables_scroll", timeout=timedelta(seconds=20))
        selenium.click_element_when_visible("CSS:#investments-table-object_length > label > select")
        selenium.click_element_when_visible("CSS:#investments-table-object_length > label > select > option:nth-child(4)")

        time.sleep(config.get_int("ID_DASHBOARD", "investment_last_button_disabled_sleep", 10))
        investment_table = selenium.find_element(locator="CSS:#investments-table-object_wrapper > div.dataTables_scroll").get_attribute('outerHTML')

        return investment_table
    except Exception as e :
        log.error(f"failed to element inside locate investment table: {str(e)}")


def get_all_uii_elements():
    numbers = re.findall('[0-9]+', selenium.get_text(locator="CSS:#investments-table-object_info"))
    max_num_of_uii = max([int(num) for num in numbers])
    uii_link_rows = []
    for row in range(1, max_num_of_uii):
        try:
            if selenium.is_element_visible(locator=f"CSS:#investments-table-object > tbody > tr:nth-child({row}) > td.left.sorting_2 > a"):
                uii_link_rows.append(row)
        except Exception as e:
            log.error(f"failed to locate uii element due to: {str(e)}")

    return uii_link_rows


def open_another_window():
    current_url = selenium.get_location()
    selenium.open_available_browser(url=current_url, alias="second")
    return current_url


def download_business_case(uii_element_num, base_url):
    try:
        selenium.switch_browser('main')
        locator = f"CSS:#investments-table-object > tbody > tr:nth-child({uii_element_num}) > td.left.sorting_2 > a"
        uii = selenium.get_text(locator=locator)
        uii_url = f"{base_url}/{uii}"
        selenium.switch_browser('second')
        selenium.go_to(url=uii_url)
        selenium.wait_until_element_is_visible(locator="CSS:#business-case-pdf > a", timeout=timedelta(seconds=10))
        selenium.click_link(locator="CSS:#business-case-pdf > a")
        for i in range(config.get_int("ID_DASHBOARD", "uii_pdf_download_wait", 10)):
            if selenium.does_page_contain("Generating PDF..."):
                time.sleep(1)
            else:
                break
    except Exception as e:
        log.error(f"failed to locate uii report download due to: {str(e)}")


