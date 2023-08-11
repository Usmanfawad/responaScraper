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
        self.options.add_argument(f"--user-agent={USER_AGENT}")
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.driver.get(RESPONA_URL)
        # self.driver.maximize_window()

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
        time.sleep(3)

        # Continue button to proceed to password entry
        continue_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/button')))
        continue_button.send_keys(Keys.ENTER)

        # Password input
        password_input = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div[4]/input')))
        for each_letter in RESPONA_PASSWORD:
            time.sleep(random.random())
            password_input.send_keys(each_letter)

        time.sleep(3)

        # Login button
        login_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/button')))
        login_button.send_keys(Keys.ENTER)

    def workspace_page(self):


        # Current date time
        current_date = datetime.now()
        self.curr_day = current_date.day


        # Just waiting for the page to be interactable
        workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1)')))

        # Select date range
        date_range_div = self.driver.find_element(By.CSS_SELECTOR, '.header-date-filter')
        date_range_div.click()

        all_days = self.driver.find_elements(By.CSS_SELECTOR, 'button.rdrDay')
        for each_day in all_days:
            print(each_day.text)
            if each_day.text == str(self.curr_day):
                each_day.click()
                break

        time.sleep(2)

        # Wait for the dashboard analytics div to appear.
        analytics_div = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')

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

        # Just waiting for the page to be interactable
        workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/table/tbody')))

        # Get all campaigns
        all_campaigns_outer_div = self.driver.find_elements(By.CSS_SELECTOR, 'tr.campaigns-table__row')
        len_campaigns = len(all_campaigns_outer_div)

        for each_campaign in range(len_campaigns):
            # Just waiting for the page to be interactable
            workspace_btn_clickable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/table/tbody')))
            all_campaigns_outer_div = self.driver.find_elements(By.CSS_SELECTOR, 'tr.campaigns-table__row')

            self.row_data = []

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            self.row_data.append(dt_string)
            workspace_name = "XYZ"
            self.row_data.append(workspace_name)

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

    def campaign_inner_page(self):

        # Wait for the add opportunities button to be interactable
        add_opportunities_btn_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/button')))


        # Click insights button inside campaigns page
        insights_btn_campaign_page = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div[3]')
        insights_btn_campaign_page.click()
        # Now wait for a div to appear
        page_header_interactable = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.page-header')))
        # Select date range
        date_range_div = self.driver.find_element(By.CSS_SELECTOR, '.header-date-filter')
        date_range_div.click()

        all_days = self.driver.find_elements(By.CSS_SELECTOR, 'button.rdrDay')
        for each_day in all_days:
            print(each_day.text)
            if each_day.text == str(self.curr_day):
                each_day.click()
                break

        # Insights from inside the campaign page now
        delivery_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
        print("Delivery rate: " + str(delivery_rate_campaign_insights.text.split('%')[0]))
        self.delivery_rate = str(delivery_rate_campaign_insights.text.split('%')[0])

        open_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
        print("Open rate: " + str(open_rate_campaign_insights.text.split('%')[0]))
        self.open_rate_campaign_insights = str(open_rate_campaign_insights.text.split('%')[0])

        reply_rate_campaign_insights = self.driver.find_element(By.CSS_SELECTOR, 'div.analytics-email-report-card:nth-child(3) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)')
        print("Reply rate: " + str(reply_rate_campaign_insights.text.split('%')[0]))
        self.reply_rate_campaign_insights = str(reply_rate.text.split('%')[0])

        self.row_data.append(self.delivery_rate_campaign_insights)
        self.row_data.append(self.open_rate_campaign_insights)
        self.row_data.append(self.reply_rate_campaign_insights)

        # Now find the button and click it
        add_opportunities_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/button')
        add_opportunities_btn.click()

        time.sleep(1)

        # Check an interactable event, checking the automation and manual toggle button
        toggle_btn_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.boolean-toggler__button:nth-child(2)')))
        print(toggle_btn_check)
        print("Toggle btn found")
        # Once it is clickable, checking for how many headings there are, googlesearch, import etc.

        time.sleep(1)

        # Now the second tab i.e. "Find opporunities"
        # Check if the main div of selected opportunities has appeared or not
        selected_opportunities_main_div_check = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.opportunity-groups__item-title')))
        print(selected_opportunities_main_div_check)
        print("Opportunity div")
        titles_lst_inner = self.driver.find_elements(By.CSS_SELECTOR, '.opportunity-groups__item-title')
        numbers_lst_inner = self.driver.find_elements(By.CSS_SELECTOR, '.opportunity-groups__count')
        print(len(titles_lst_inner))
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

        # Now the second tab i.e. "Get contacts"
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

        # Now the third tab i.e. "Personalize & touch"
        personalize_and_launch_btn = self.driver.find_element(By.CSS_SELECTOR, 'div.step-link__container:nth-child(7) > a:nth-child(1)')
        personalize_and_launch_btn.click()
        # Checking if the div is interactable
        interaction_div = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.opportunities-contacts-bar__type-select')))
        print("Personalize and launchc")
        outer_div = self.driver.find_elements(By.CLASS_NAME, 'opportunities-bar-type-select__button')
        personalized_opportunities = outer_div[0].text
        need_personalization = outer_div[1].text
        print(personalized_opportunities)
        self.row_data.append(personalized_opportunities)
        print(need_personalization)
        self.row_data.append(need_personalization)


        # Back to the campaigns tab
        campaign_navbar_btn = self.driver.find_element(By.CSS_SELECTOR,'a.sidebar__link:nth-child(2)')
        campaign_navbar_btn.click()

        insert_to_sheet = GoogleSheets(self.row_data)

        time.sleep(2)

if __name__ == "__main__":
    Respona()