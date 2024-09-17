import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class MS2_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.upper_categories= ["one", "two", "three", "four", "five", "six"]
        self.lower_categories= ["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
        self.score_elements=["upper_score", "upper_bonus", "upper_total", "lower_score", "upper_total_lower", "grand_total"]
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_save_load_button_UI(self): 
        self.browser.get(self.url)
        ids=["save_game", "load_game"]
        for id in ids:
            try:
                button = self.browser.find_element(By.ID, f"{id}")
            except:
                self.fail(f"{id} element does not exist!")
            
        print("test_save_load_button_UI passed")
    
    def test_upper_categories_UI(self): 
        
        for id in self.upper_categories:
            self.browser.get(self.url)
            try:
                roll_button = self.browser.find_element(By.ID, "roll_button")
            except:
                self.fail("roll_button element does not exist!")
            roll_button.click()

            try:
                category = self.browser.find_element(By.ID, f"{id}_input")
            except:
                self.fail(f"{id}_input element does not exist!")

            self.assertTrue(category.is_displayed())
            self.assertTrue(category.tag_name == "input")
            self.assertTrue(category.is_enabled())

            category.send_keys("0"+Keys.RETURN)

            self.assertFalse(category.is_enabled())
            
        print("test_upper_categories_UI passed")

    def test_lower_categories_UI(self): 
        for id in self.lower_categories:
            self.browser.get(self.url)
            try:
                roll_button = self.browser.find_element(By.ID, "roll_button")
            except:
                self.fail("roll_button element does not exist!")
            roll_button.click()

            try:
                category = self.browser.find_element(By.ID, f"{id}_input")
            except:
                self.fail(f"{id}_input element does not exist!")

            self.assertTrue(category.is_displayed())
            self.assertTrue(category.tag_name == "input")
            self.assertTrue(category.is_enabled())

            category.send_keys("0"+Keys.RETURN)

            self.assertFalse(category.is_enabled())
        
        print("test_lower_categories_UI passed")
    
    def test_score_elements_UI(self): 
        self.browser.get(self.url)
        for id in self.score_elements:
            try:
                element = self.browser.find_element(By.ID, f"{id}")
                self.assertTrue(element.is_displayed())
            except:
                self.fail(f"{id} element does not exist!")
        
        print("test_score_elements_UI passed")

if __name__ == '__main__':
    unittest.main()
    