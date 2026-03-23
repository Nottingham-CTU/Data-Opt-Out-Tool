# Generated from Selenium IDE
# Test name: t01 - Configure module settings
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class Test_01_Configure_module_settings:
  def setup_method(self, method):
    self.driver = self.selectedBrowser
    self.vars = {}
  def teardown_method(self, method):
    self.driver.quit()

  def test_01_Configure_module_settings(self):
    self.driver.get("http://127.0.0.1/")
    self.driver.find_element(By.LINK_TEXT, "My Projects").click()
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test C')]")) > 0
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test L')]")) > 0
    self.vars["projtypes"] = self.driver.execute_script("return ['C','L']")
    for self.vars["projtype"] in self.vars["projtypes"]:
      self.vars["projtype_desc"] = self.driver.execute_script("return arguments[0] == 'C' ? 'classic' : 'longitudinal'", self.vars["projtype"])
      self.driver.execute_script("//SAVEDESC:-- Testing arguments[0] project --", self.vars["projtype_desc"])
      self.driver.find_element(By.LINK_TEXT, "Data Opt Out Tool Test "+self.vars["projtype"]).click()
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"ExternalModules/manager/project.php\"]").click()
      self.driver.find_element(By.ID, "external-modules-enable-modules-button").click()
      self.driver.find_element(By.CSS_SELECTOR, "tr[data-module=\"data_opt_out_tool\"] button.enable-button").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr[data-module=\"data_opt_out_tool\"] button.external-modules-configure-button")))
      self.driver.find_element(By.CSS_SELECTOR, "tr[data-module=\"data_opt_out_tool\"] button.external-modules-configure-button").click()
      self.driver.find_element(By.CSS_SELECTOR, "[name*=\"process-roles\"]").find_element(By.XPATH, "//option[. = 'Role1']").click()
      self.driver.find_element(By.NAME, "record-label-field").send_keys("first_name")
      None if (element := self.driver.find_element(By.NAME, "record-label-filter")).is_selected() else element.click()
      if self.driver.execute_script("return (arguments[0] == 'C')", self.vars["projtype"]):
        self.driver.execute_script("//SETDESC:Click \"Longitudinal: repeating form\"")
        None if (element := self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-mode\"][value=\"longitudinal-form\"]")).is_selected() else element.click()
        self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-event\"]").send_keys(".")
        self.vars["errmsg"] = self.driver.execute_script("return 'An error occurred while saving settings:'+decodeURIComponent('%0a%0a')+'Longitudinal repeat type selected, but project is classic.'")
      else:
        self.driver.execute_script("//SETDESC:Click \"Classic: repeating form\"")
        None if (element := self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-mode\"][value=\"classic-form\"]")).is_selected() else element.click()
        self.vars["errmsg"] = self.driver.execute_script("return 'An error occurred while saving settings:'+decodeURIComponent('%0a%0a')+'Classic repeat type selected, but project is longitudinal.'")
      self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-form\"]").find_element(By.CSS_SELECTOR, "*[value='upload']").click()
      self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-field\"]").find_element(By.CSS_SELECTOR, "*[value='upload_file']").click()
      self.driver.find_element(By.CSS_SELECTOR, "#external-modules-configure-modal .modal-footer button.save").click()
      time.sleep(3)
      self.driver.execute_script("//SAVEDESC:Assert error message shown (classic/longitudinal mismatch).")
      assert self.driver.switch_to.alert.text == self.vars["errmsg"]
      self.driver.switch_to.alert.accept()
      if self.driver.execute_script("return (arguments[0] == 'C')", self.vars["projtype"]):
        self.driver.execute_script("$('[name*=\"upload-event\"]').val('')")
        self.driver.execute_script("//SETDESC:Click \"Classic: repeating form\"")
        None if (element := self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-mode\"][value=\"classic-form\"]")).is_selected() else element.click()
      else:
        self.driver.execute_script("//SETDESC:Click \"Longitudinal: repeating form\"")
        None if (element := self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-mode\"][value=\"longitudinal-form\"]")).is_selected() else element.click()
        self.driver.find_element(By.CSS_SELECTOR, "[name*=\"upload-event\"]").find_element(By.CSS_SELECTOR, "*[value='event_2_arm_1']").click()
      self.driver.execute_script("$('#south').remove()")
      self.driver.find_element(By.CSS_SELECTOR, "#external-modules-configure-modal .modal-footer button.save").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "south")))
      self.driver.find_element(By.LINK_TEXT, "My Projects").click()
