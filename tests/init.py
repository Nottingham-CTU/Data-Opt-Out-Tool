# Generated from Selenium IDE
# Test name: init
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class Test_init:
  def setup_method(self, method):
    self.driver = self.selectedBrowser
    self.vars = {}
  def teardown_method(self, method):
    self.driver.quit()

  def test_init(self):
    self.driver.get("http://127.0.0.1/")
    self.driver.find_element(By.LINK_TEXT, "My Projects").click()
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test')]")) == 0
    self.vars["projtypes"] = self.driver.execute_script("return ['C','L']")
    for self.vars["projtype"] in self.vars["projtypes"]:
      self.driver.find_element(By.LINK_TEXT, "New Project").click()
      self.driver.find_element(By.ID, "app_title").send_keys("Data Opt Out Tool Test "+self.vars["projtype"])
      self.driver.find_element(By.ID, "purpose").find_element(By.CSS_SELECTOR, "*[value='0']").click()
      self.driver.find_element(By.ID, "project_template_radio1").click()
      self.driver.find_element(By.XPATH, "//table[@id='table-template_projects_list']//tr[contains(.,'Basic Demography')]//input").click()
      self.driver.find_element(By.CSS_SELECTOR, ".btn-primaryrc").click()
      time.sleep(5)
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"Design/online_designer.php\"]").click()
      self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"showAddForm()\"]").click()
      self.driver.find_element(By.CSS_SELECTOR, "#new-demographics button[onclick*=\"addNewFormReveal\"]").click()
      self.driver.find_element(By.ID, "new_form-demographics").send_keys("Upload")
      if self.driver.execute_script("return ($('#new_form_var-demographics').length > 0)"):
        self.driver.find_element(By.ID, "new_form_var-demographics").send_keys("upload")
      self.driver.find_element(By.CSS_SELECTOR, "#new-demographics input[onclick*=\"addNewForm\"]").click()
      self.driver.find_element(By.CSS_SELECTOR, "[aria-describedby] .ui-dialog-buttonset .close-button").click()
      self.driver.find_element(By.ID, "formlabel-upload").click()
      self.driver.find_element(By.ID, "btn-last").click()
      self.driver.find_element(By.ID, "field_type").find_element(By.XPATH, "//option[. = 'File Upload (for users to upload files)']").click()
      self.driver.find_element(By.ID, "field_label").send_keys("File upload")
      self.driver.find_element(By.ID, "field_name").send_keys("upload_file")
      self.driver.find_element(By.CSS_SELECTOR, "[aria-describedby=\"div_add_field\"] .ui-dialog-buttonset button[style*=\"bold\"]").click()
      if self.driver.execute_script("return (arguments[0] == 'L')", self.vars["projtype"]):
        self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"ProjectSetup/index.php\"]").click()
        self.driver.find_element(By.ID, "setupLongiBtn").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@id='setupLongiBtn'][contains(.,'Disable')]")))
        self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"Design/define_events.php\"]").click()
        self.driver.find_element(By.ID, "descrip").send_keys("Event 2")
        self.driver.execute_script("$('#south').remove()")
        self.driver.find_element(By.ID, "addbutton").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "south")))
        self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"Design/designate_forms.php\"]").click()
        self.driver.find_element(By.ID, "beginEditBtn").click()
        None if (element := self.driver.find_element(By.XPATH, "(//*[@id='event_grid_table']//input)[1]")).is_selected() else element.click()
        None if not (element := self.driver.find_element(By.XPATH, "(//*[@id='event_grid_table']//input)[2]")).is_selected() else element.click()
        None if not (element := self.driver.find_element(By.XPATH, "(//*[@id='event_grid_table']//input)[3]")).is_selected() else element.click()
        None if (element := self.driver.find_element(By.XPATH, "(//*[@id='event_grid_table']//input)[4]")).is_selected() else element.click()
        self.driver.find_element(By.ID, "save_btn").click()
        None if len(elements := self.driver.find_elements(By.CSS_SELECTOR, "#beginEditBtn[disabled]")) == 0 else WebDriverWait(self.driver, 30).until(expected_conditions.staleness_of(elements[0]))
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"ProjectSetup/index.php\"]").click()
      self.driver.find_element(By.ID, "enableRepeatingFormsEventsBtn").click()
      if self.driver.execute_script("return (arguments[0] == 'L')", self.vars["projtype"]):
        self.driver.find_element(By.XPATH, "//table[@id='table-repeat_setup']//tr[contains(.,'Upload')]//select").find_element(By.CSS_SELECTOR, "*[value='PARTIAL']").click()
      None if (element := self.driver.find_element(By.XPATH, "//table[@id='table-repeat_setup']//tr[contains(.,'Upload')]//input[@type='checkbox']")).is_selected() else element.click()
      self.driver.find_element(By.XPATH, "//*[@aria-describedby='repeatingInstanceEnableDialog']//*[contains(@class,'ui-dialog-buttonset')]//button[contains(.,'Save')]").click()
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"UserRights/index.php\"]").click()
      self.driver.find_element(By.ID, "new_rolename").send_keys("Role1")
      self.driver.find_element(By.ID, "createRoleBtn").click()
      None if not (element := self.driver.find_element(By.CSS_SELECTOR, "input[name=\"design\"]")).is_selected() else element.click()
      self.driver.find_element(By.CSS_SELECTOR, "div[aria-describedby=\"editUserPopup\"] .ui-dialog-buttonset button[style*=\"bold\"]").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='table-user_rights_roles_table']//tr[contains(.,'Role1')]")))
      self.driver.find_element(By.ID, "new_username_assign").send_keys("user1")
      self.driver.find_element(By.ID, "assignUserBtn").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "notify_email_role")))
      None if not (element := self.driver.find_element(By.ID, "notify_email_role")).is_selected() else element.click()
      self.driver.find_element(By.ID, "user_role").find_element(By.XPATH, "//option[. = 'Role1']").click()
      self.driver.find_element(By.ID, "assignDagRoleBtn").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='table-user_rights_roles_table']//tr[contains(.,'user1')]")))
      self.driver.find_element(By.ID, "new_rolename").send_keys("Role2")
      self.driver.find_element(By.ID, "createRoleBtn").click()
      None if not (element := self.driver.find_element(By.CSS_SELECTOR, "input[name=\"design\"]")).is_selected() else element.click()
      self.driver.find_element(By.CSS_SELECTOR, "div[aria-describedby=\"editUserPopup\"] .ui-dialog-buttonset button[style*=\"bold\"]").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='table-user_rights_roles_table']//tr[contains(.,'Role2')]")))
      self.driver.find_element(By.ID, "new_username_assign").send_keys("user2")
      self.driver.find_element(By.ID, "assignUserBtn").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "notify_email_role")))
      None if not (element := self.driver.find_element(By.ID, "notify_email_role")).is_selected() else element.click()
      self.driver.find_element(By.ID, "user_role").find_element(By.XPATH, "//option[. = 'Role2']").click()
      self.driver.find_element(By.ID, "assignDagRoleBtn").click()
      WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='table-user_rights_roles_table']//tr[contains(.,'user2')]")))
      self.driver.find_element(By.LINK_TEXT, "My Projects").click()
