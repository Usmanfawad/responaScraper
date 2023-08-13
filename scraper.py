import os
import requests
import time
import random
from datetime import datetime

from google_sheets import GoogleSheets
from config import *

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Respona:

    def __init__(self):

        self.options = Options()
        # Comment below for dev mode
        self.options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--headless=new")
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument(f"--user-agent={USER_AGENT}")
        # self.options.add_experimental_option("detach", True)
        # Comment below for dev mode
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH") ,options=self.chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.driver.get(RESPONA_URL)

        self.login()
        self.workspace_page()

        time.sleep(10)
        self.driver.close()

    def click_workspace_btn(self, index):

        workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.workspace-select__short-content')))
        workspace_btn = self.driver.find_element(By.CSS_SELECTOR, '.workspace-select__short-content')
        print(all_navbar_links)
        print("Sidebar workspace")
        workspace_btn.click()
    def login(self):

        # Email input
        email_input = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[6]/input')))
        for each_letter in RESPONA_EMAIL:
            time.sleep(random.random())
            email_input.send_keys(each_letter)

        #Sleep time because the button is not interactable so early.
        time.sleep(1)

        # Continue button to proceed to password entry
        continue_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/button')))
        continue_button.send_keys(Keys.ENTER)

        # Password input
        password_input = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div[4]/input')))
        for each_letter in RESPONA_PASSWORD:
            time.sleep(random.random())
            password_input.send_keys(each_letter)

        time.sleep(1)

        # Login button
        login_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/button')))
        login_button.send_keys(Keys.ENTER)

    def workspace_page(self):

        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")

        # Current date time
        current_date = datetime.now()
        self.curr_day = current_date.day

        # Just waiting for the page to be interactable
        workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1)')))

        # Check the length of workspaces
        workspaces_tab_btn = self.driver.find_element(By.CSS_SELECTOR, '.sidebar__workspace')
        workspaces_tab_btn.click()
        all_workspaces = self.driver.find_elements(By.CLASS_NAME, 'workspaces-sidebar__workspace-row')
        workspaces_length = len(all_workspaces)
        print("Length of workspaces")
        print(workspaces_length)
        # Close workspace btn
        print("Closing workspace btn")
        close_btn = self.driver.find_element(By.CSS_SELECTOR, '.workspaces-sidebar__close-icon')
        close_btn.click()

        for each_workspace in range(workspaces_length):
            time.sleep(1)
            print("Workspace number: " + str(each_workspace))
            workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1)')))
            workspaces_tab_btn = self.driver.find_element(By.CSS_SELECTOR, '.sidebar__workspace')
            workspaces_tab_btn.click()

            time.sleep(1)
            print("Workspace clicked")

            all_campaigns_outer_div = self.driver.find_elements(By.CLASS_NAME, 'workspaces-sidebar__workspace-row')
            self.workspace_name = all_campaigns_outer_div[each_workspace].text
            print(self.workspace_name)
            all_campaigns_outer_div[each_workspace].click()

            # Close workspace btn
            close_btn = self.driver.find_element(By.CSS_SELECTOR, '.workspaces-sidebar__close-icon')
            close_btn.click()


            time.sleep(3)

            # Select date range
            date_range_div = self.driver.find_element(By.CSS_SELECTOR, '.header-date-filter')
            date_range_div.click()

            all_days = self.driver.find_elements(By.CSS_SELECTOR, 'button.rdrDay')
            for each_day in all_days:
                if each_day.text == str(self.curr_day):
                    each_day.click()
                    break

            time.sleep(2)

            # Wait for the dashboard analytics div to appear.
            analytics_div = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')))

            # Dashboard data

            delivery_rate = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Delivery rate: " + str(delivery_rate.text.split('%')[0]))
            self.delivery_rate = str(delivery_rate.text.split('%')[0])

            open_rate = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Open rate: " + str(open_rate.text.split('%')[0]))
            self.open_rate = str(open_rate.text.split('%')[0])


            reply_rate = self.driver.find_element(By.CSS_SELECTOR,'div.analytics-email-report-card:nth-child(3) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Reply rate: " + str(reply_rate.text.split('%')[0]))
            self.reply_rate = str(reply_rate.text.split('%')[0])

            campaign_nav_btn = self.driver.find_element(By.CSS_SELECTOR, 'a.sidebar__link:nth-child(2)')
            campaign_nav_btn.click()


            self.campaigns_page()


    def campaigns_page(self):

        # time.sleep(2)
        # Just waiting for the page to be interactable
        workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.campaigns-table-wrapper')))
        print("--------------------------------")
        # Get all campaigns
        all_campaigns_outer_div = self.driver.find_elements(By.CSS_SELECTOR, 'tr.campaigns-table__row')
        len_campaigns = len(all_campaigns_outer_div)
        # if

        for each_campaign in range(len_campaigns):
            # Just waiting for the page to be interactable
            print("Campaign no: " + str(each_campaign))
            workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.campaigns-table-wrapper')))
            all_campaigns_outer_div = self.driver.find_elements(By.CSS_SELECTOR, 'tr.campaigns-table__row')

            self.row_data = []


            self.row_data.append(self.dt_string, value_input_option='USER_ENTERED')
            self.row_data.append(self.workspace_name)

            self.row_data.append(self.delivery_rate)
            self.row_data.append(self.open_rate)
            self.row_data.append(self.reply_rate)

            try:
                # No need to check the toggle, if the progress is draft and it has empty values, just don't enter anything
                # check_active_btn = each_campaign.find_element(By.CLASS_NAME, 'colored-toggler__slider--active')
                campaign_name_campaign_main_page = all_campaigns_outer_div[each_campaign].find_element(By.CLASS_NAME, 'title-cell__title')
                print(campaign_name_campaign_main_page.text)
                self.row_data.append(campaign_name_campaign_main_page.text)
                print("^Campaign name")
                temp_check_lst = []
                status_campaign_main_page = all_campaigns_outer_div[each_campaign].find_element(By.CLASS_NAME, 'status-cell__status')
                print(status_campaign_main_page.text)
                self.row_data.append(status_campaign_main_page.text)
                opportunities_campaign_main_page = all_campaigns_outer_div[each_campaign].find_elements(By.CLASS_NAME, 'table__td')[3]
                print(opportunities_campaign_main_page.text)
                self.row_data.append(opportunities_campaign_main_page.text)
                temp_check_lst.append(int(opportunities_campaign_main_page.text))
                sent_campaign_main_page = all_campaigns_outer_div[each_campaign].find_element(By.CLASS_NAME, 'delivered-cell')
                print(sent_campaign_main_page.text)
                self.row_data.append(sent_campaign_main_page.text)
                temp_check_lst.append(int(sent_campaign_main_page.text))
                open_rate_reply_rate_campaign_main_page = all_campaigns_outer_div[each_campaign].find_elements(By.CLASS_NAME, 'rate-cell__value')
                open_rate_campaign_main_page = open_rate_reply_rate_campaign_main_page[0].text.split('%')[0]
                reply_rate_campaign_main_page = open_rate_reply_rate_campaign_main_page[1].text.split('%')[0]
                print(open_rate_campaign_main_page)
                self.row_data.append(open_rate_campaign_main_page)
                temp_check_lst.append(int(open_rate_campaign_main_page))
                print(reply_rate_campaign_main_page)
                self.row_data.append(reply_rate_campaign_main_page)
                temp_check_lst.append(int(reply_rate_campaign_main_page))

                if sum(temp_check_lst) == 0:
                    print("Drafted campaign")
                    for x in range(9):
                        self.row_data.append("0")

                    insert_to_sheet = GoogleSheets(self.row_data)

                else:
                    # Clicking each campaign now, calling another function that will perform all campaign related scraping
                    all_campaigns_outer_div[each_campaign].click()
                    self.campaign_inner_page()

                    print("\n\n\n\n")

            except Exception as e:
                print(e)
                print("Toggle off")

        # Back to the dashboard main page
        dashboard_nav_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/a[1]')
        dashboard_nav_btn.click()

    def campaign_inner_page(self):

        time.sleep(1)

        try:
            # Wait for the add opportunities button to be interactable
            add_opportunities_btn_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/button')))


            # Click insights button inside campaigns page
            insights_btn_campaign_page = self.driver.find_element(By.CSS_SELECTOR, 'div.configurable-sidebar__link-wrapper:nth-child(3) > a:nth-child(1)')
            insights_btn_campaign_page.click()
            # Now wait for a div to appear
            page_header_interactable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.page-header')))
            # Select date range
            date_range_div = self.driver.find_element(By.CSS_SELECTOR, '.header-date-filter')
            date_range_div.click()

            all_days = self.driver.find_elements(By.CSS_SELECTOR, 'button.rdrDay')
            for each_day in all_days:
                if each_day.text == str(self.curr_day):
                    each_day.click()
                    break

            # Wait for the dashboard analytics div to appear.
            analytics_div = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')))

            # Insights from inside the campaign page now
            delivery_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Delivery rate: " + str(delivery_rate_campaign_insights.text.split('%')[0]))
            self.delivery_rate_campaign_insights = str(delivery_rate_campaign_insights.text.split('%')[0])

            open_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Open rate: " + str(open_rate_campaign_insights.text.split('%')[0]))
            self.open_rate_campaign_insights = str(open_rate_campaign_insights.text.split('%')[0])

            reply_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(3) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
            print("Reply rate: " + str(reply_rate_campaign_insights.text.split('%')[0]))
            self.reply_rate_campaign_insights = str(reply_rate_campaign_insights.text.split('%')[0])

            self.row_data.append(self.delivery_rate_campaign_insights)
            self.row_data.append(self.open_rate_campaign_insights)
            self.row_data.append(self.reply_rate_campaign_insights)

            # Now find the button and click it
            add_opportunities_btn = self.driver.find_element(By.CSS_SELECTOR,'.button--size-m')
            add_opportunities_btn.click()

            time.sleep(4)

            # Check an interactable event, checking the automation and manual toggle button
            toggle_btn_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.boolean-toggler__button:nth-child(2)')))
            print(toggle_btn_check)
            print("Toggle btn found")
            # Once it is clickable, checking for how many headings there are, googlesearch, import etc.

            time.sleep(4)


        except Exception as e:
            print(e)
            print("In the exception. Draft thing which means that it will not have any campaign insights.")
            self.row_data.append(0)
            self.row_data.append(0)
            self.row_data.append(0)
            pass


        # Now the second tab i.e. "Find opporunities"
        # Check if the main div of selected opportunities has appeared or not
        try:
            selected_opportunities_main_div_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.opportunity-groups__item-title')))
            print(selected_opportunities_main_div_check)
            print("Opportunity div")
            titles_lst_inner = self.driver.find_elements(By.CSS_SELECTOR, '.opportunity-groups__item-title')
            numbers_lst_inner = self.driver.find_elements(By.CSS_SELECTOR, '.opportunity-groups__count')
            print(len(titles_lst_inner))
            time.sleep(4)
            if len(titles_lst_inner) > 1:
                if titles_lst_inner[0].text == "GoogleSearch":
                    google_search_text_find_opportunities_page = numbers_lst_inner[0].text.strip()
                    self.row_data.append(google_search_text_find_opportunities_page)
                    import_text_find_opportunities_page = numbers_lst_inner[1].text.strip()
                    self.row_data.append(import_text_find_opportunities_page)
                elif titles_lst_inner[0].text == "Import":
                    google_search_text_find_opportunities_page = numbers_lst_inner[1].text.strip()
                    self.row_data.append(google_search_text_find_opportunities_page)
                    import_text_find_opportunities_page = numbers_lst_inner[0].text.strip()
                    self.row_data.append(import_text_find_opportunities_page)
            else:
                if titles_lst_inner[0].text == "GoogleSearch":
                    google_search_text_find_opportunities_page = numbers_lst_inner[0].text.strip()
                    self.row_data.append(google_search_text_find_opportunities_page)
                    self.row_data.append(0)
                elif titles_lst_inner[0].text == "Import":
                    import_text_find_opportunities_page = numbers_lst_inner[0].text.strip()
                    self.row_data.append(0)
                    self.row_data.append(import_text_find_opportunities_page)
        except Exception as e:
            print(e)
            print("Error occured in tab 1 of campaign")
            self.row_data.append(0)
            self.row_data.append(0)

        # Now the second tab i.e. "Get contacts"
        time.sleep(4)
        try:
            get_contacts_btn = self.driver.find_element(By.CSS_SELECTOR, 'div.step-link__container:nth-child(3) > a:nth-child(1)')
            get_contacts_btn.click()
            # Checking if the div is interactable
            interaction_div = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.opportunities-contacts-bar')))
            outer_div = self.driver.find_elements(By.CLASS_NAME, 'opportunities-bar-type-select__button')
            identified_contacts = outer_div[0].text
            unidentified_contacts = outer_div[1].text
            print(identified_contacts)
            self.row_data.append(identified_contacts)
            print(unidentified_contacts)
            self.row_data.append(unidentified_contacts)
        except Exception as e:
            print(e)
            print("Error occured in tab 2 of campaign")
            self.row_data.append(0)
            self.row_data.append(0)

        # Now the third tab i.e. "Personalize & touch"
        time.sleep(4)
        try:
            personalize_and_launch_btn = self.driver.find_element(By.CSS_SELECTOR, 'div.step-link__container:nth-child(7) > a:nth-child(1)')
            personalize_and_launch_btn.click()
            time.sleep(4)
            print("Inside the personalized tab")
            # Checking if the div is interactable
            interaction_div = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.opportunities-contacts-bar__type-select')))
            print("Personalize and launch")
            outer_div_personalize = self.driver.find_elements(By.CLASS_NAME, 'opportunities-bar-type-select__button')
            print("Personalized buttons found: " + str(len(outer_div_personalize)))
            personalized_opportunities = outer_div_personalize[0].text
            need_personalization = outer_div_personalize[1].text
            print(personalized_opportunities)
            self.row_data.append(personalized_opportunities)
            print(need_personalization)
            self.row_data.append(need_personalization)
            time.sleep(4)
        except Exception as e:
            print(e)
            print("Error occured in tab 3 of campaign")
            self.row_data.append(0)
            self.row_data.append(0)


        # Back to the campaigns tab
        campaign_navbar_btn = self.driver.find_element(By.CSS_SELECTOR,'a.sidebar__link:nth-child(2)')
        campaign_navbar_btn.click()

        insert_to_sheet = GoogleSheets(self.row_data)



        time.sleep(2)

if __name__ == "__main__":
    Respona()