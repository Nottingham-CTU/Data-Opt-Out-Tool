# Generated from Selenium IDE
# Test name: t02 - User access
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from fn_switchuser import Test_fn_switchuser as Sub1

class Test_02_User_access:
  def setup_method(self, method):
    self.driver = self.selectedBrowser
    self.vars = {}
  def teardown_method(self, method):
    self.driver.quit()

  def test_02_User_access(self):
    self.driver.get("http://127.0.0.1/")
    self.driver.find_element(By.LINK_TEXT, "My Projects").click()
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test C')]")) > 0
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test L')]")) > 0
    self.vars["projtypes"] = self.driver.execute_script("return ['C','L']")
    for self.vars["projtype"] in self.vars["projtypes"]:
      self.vars["projtype_desc"] = self.driver.execute_script("return arguments[0] == 'C' ? 'classic' : 'longitudinal'", self.vars["projtype"])
      self.driver.execute_script("//SAVEDESC:-- Testing arguments[0] project --", self.vars["projtype_desc"])
      self.driver.find_element(By.LINK_TEXT, "Data Opt Out Tool Test "+self.vars["projtype"]).click()
      self.vars["projpage"] = self.driver.execute_script("return window.location.href")
      self.driver.execute_script("//SAVEDESC:Assert \"Process Opt-Outs\" link available.")
      assert len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]")) > 0
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]").click()
      self.driver.execute_script("//SAVEDESC:Assert Process Opt-Outs page loaded.")
      assert len(self.driver.find_elements(By.ID, "doot-file-input")) > 0
      self.vars["dootpage"] = self.driver.execute_script("return window.location.href")
      self.vars["username"] = "user1"
      sub=Sub1();sub.driver=self.driver;sub.vars=self.vars;sub.test_fn_switchuser() # Run fn switchuser
      self.driver.execute_script("//SAVEDESC:Assert \"Process Opt-Outs\" link available.")
      assert len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]")) > 0
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]").click()
      self.driver.execute_script("//SAVEDESC:Assert Process Opt-Outs page loaded.")
      assert len(self.driver.find_elements(By.ID, "doot-file-input")) > 0
      self.vars["username"] = "user2"
      sub=Sub1();sub.driver=self.driver;sub.vars=self.vars;sub.test_fn_switchuser() # Run fn switchuser
      self.driver.execute_script("//SAVEDESC:Assert \"Process Opt-Outs\" link not available.")
      assert len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]")) == 0
      self.driver.execute_script("//SETDESC:Navigate to Process Opt-Outs page.")
      self.driver.execute_script("$('#south').remove();window.location = arguments[0]", self.vars["dootpage"])
      time.sleep(2)
      self.driver.find_element(By.CSS_SELECTOR, "body").send_keys("SAVESCREENSHOT")
      self.driver.execute_script("//SAVEDESC:Assert Process Opt-Outs page not loaded.")
      assert len(self.driver.find_elements(By.ID, "doot-file-input")) == 0
      self.driver.execute_script("window.location = arguments[0]", self.vars["projpage"])
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "south")))
      self.vars["username"] = "admin"
      sub=Sub1();sub.driver=self.driver;sub.vars=self.vars;sub.test_fn_switchuser() # Run fn switchuser
      self.driver.find_element(By.LINK_TEXT, "My Projects").click()
