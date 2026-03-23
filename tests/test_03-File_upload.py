# Generated from Selenium IDE
# Test name: t03 - File upload
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from fn_switchuser import Test_fn_switchuser as Sub1

class Test_03_File_upload:
  def setup_method(self, method):
    self.driver = self.selectedBrowser
    self.vars = {}
  def teardown_method(self, method):
    self.driver.quit()

  def test_03_File_upload(self):
    self.driver.get("http://127.0.0.1/")
    self.driver.find_element(By.LINK_TEXT, "My Projects").click()
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test C')]")) > 0
    assert len(self.driver.find_elements(By.XPATH, "//*[@id='table-proj_table'][contains(.,'Data Opt Out Tool Test L')]")) > 0
    self.vars["list1"] = self.driver.execute_script("return '1\\n2\\n3'")
    self.vars["list2"] = self.driver.execute_script("return '4\\n5\\n6'")
    self.vars["list3"] = self.driver.execute_script("return '7\\n8\\n9'")
    self.vars["username"] = "user1"
    sub=Sub1();sub.driver=self.driver;sub.vars=self.vars;sub.test_fn_switchuser() # Run fn switchuser
    self.vars["projtypes"] = self.driver.execute_script("return ['C','L']")
    for self.vars["projtype"] in self.vars["projtypes"]:
      self.vars["projtype_desc"] = self.driver.execute_script("return arguments[0] == 'C' ? 'classic' : 'longitudinal'", self.vars["projtype"])
      self.driver.execute_script("//SAVEDESC:-- Testing arguments[0] project --", self.vars["projtype_desc"])
      self.driver.find_element(By.LINK_TEXT, "Data Opt Out Tool Test "+self.vars["projtype"]).click()
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"DataEntry/record_status_dashboard.php\"]").click()
      self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"DataEntry/record_home.php\"]").click()
      self.driver.find_element(By.CSS_SELECTOR, "#event_grid_table a[href*=\"DataEntry/index.php\"][href*=\"page=demographics\"]").click()
      self.driver.find_element(By.NAME, "first_name").send_keys("Hello")
      self.driver.find_element(By.NAME, "last_name").send_keys("World")
      self.driver.find_element(By.ID, "submit-btn-saverecord").click()
      self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"prefix=data_opt_out_tool\"][href*=\"page=process\"]").click()
      self.vars["uploads"] = self.driver.execute_script("return [{id:'1',ex:arguments[0],in:''},{id:'2',ex:'',in:arguments[1]},{id:'3',ex:arguments[0],in:arguments[2]}]", self.vars["list1"], self.vars["list2"], self.vars["list3"])
      for self.vars["upload"] in self.vars["uploads"]:
        self.vars["upload_ex"] = self.driver.execute_script("return arguments[0].ex", self.vars["upload"])
        self.vars["upload_in"] = self.driver.execute_script("return arguments[0].in", self.vars["upload"])
        self.vars["removed"] = self.driver.execute_script("return ''+(Math.floor((arguments[0]+'.').length/2) == 0 ? Math.floor((arguments[1]+'.').length/2) : (9-Math.floor((arguments[0]+'.').length/2)))", self.vars["upload_in"], self.vars["upload_ex"])
        self.vars["remain"] = self.driver.execute_script("return ''+(9 - arguments[0])", self.vars["removed"])
        self.driver.find_element(By.ID, "doot-file-input").send_keys("REPODIR/tests/testdata.csv")
        self.driver.find_element(By.ID, "doot-header-row").send_keys("2")
        self.driver.execute_script("document.getElementById('doot-header-row').dispatchEvent(new Event('input'))")
        assert self.driver.find_element(By.ID, "doot-header-preview").text == "Columns found: 1 • 2025-01-01 • 5634 • hiuelrhic"
        self.driver.find_element(By.ID, "doot-header-row").send_keys("1")
        self.driver.execute_script("document.getElementById('doot-header-row').dispatchEvent(new Event('input'))")
        assert self.driver.find_element(By.ID, "doot-header-preview").text == "Columns found: id • date • num • text"
        self.driver.find_element(By.ID, "doot-step1-next").click()
        self.driver.find_element(By.ID, "doot-id-column").find_element(By.XPATH, "//option[. = 'id']").click()
        self.driver.find_element(By.ID, "doot-step2-next").click()
        self.driver.find_element(By.ID, "doot-exclude").send_keys(self.vars["upload_ex"])
        self.driver.find_element(By.ID, "doot-include").send_keys(self.vars["upload_in"])
        self.driver.find_element(By.ID, "doot-process-btn").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "doot-record-select")))
        time.sleep(0.5)
        self.driver.execute_script("//SETDESC:Assert correct number of rows removed/remain")
        self.driver.find_element(By.ID, "doot-results-msg").send_keys("SAVESCREENSHOT")
        assert self.driver.find_element(By.ID, "doot-results-msg").text == self.vars["removed"]+" row(s) removed. "+self.vars["remain"]+" row(s) remain."
        self.driver.find_element(By.ID, "doot-record-select").find_element(By.CSS_SELECTOR, "*[value='1']").click()
        self.driver.find_element(By.ID, "doot-upload-btn").click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.ID, "doot-restart-btn")))
        self.driver.find_element(By.ID, "doot-restart-btn").click()
      for self.vars["upload"] in self.vars["uploads"]:
        self.vars["upload_id"] = self.driver.execute_script("return arguments[0].id", self.vars["upload"])
        self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"DataEntry/record_status_dashboard.php\"]").click()
        self.driver.execute_script("//SETDESC:Click \"Upload\" (show instances)")
        self.driver.find_element(By.CSS_SELECTOR, "a[onclick*=\"showFormInstanceSelector\"]").click()
        self.driver.execute_script("//SETDESC:Click \"Instance arguments[0]\"", self.vars["upload_id"])
        self.driver.find_element(By.CSS_SELECTOR, "a[href*=\"DataEntry/index.php\"][href*=\"page=upload\"][href*=\"instance="+self.vars["upload_id"]+"\"]").click()
        self.vars["upload_data"] = self.driver.execute_async_script("var cb=arguments[arguments.length-1];$.get($('#upload_file-link').attr('href'),function(d){cb(d)})")
        self.driver.execute_script("//SETDESC:Assert data correct")
        self.driver.execute_script("simpleDialog('<span id=\"uploadedfiledata\">'+(arguments[0].replace(/\\n/g,'<br>'))+'</span>','Uploaded data')", self.vars["upload_data"])
        self.driver.find_element(By.ID, "uploadedfiledata").send_keys("SAVESCREENSHOT")
        self.vars["upload_valid"] = self.driver.execute_script("return (arguments[0].indexOf('\\n1,')==-1 && arguments[0].indexOf('\\n2,')==-1 && arguments[0].indexOf('\\n3,')==-1 && (arguments[1] == '3' ? (arguments[0].indexOf('\\n4,')==-1 && arguments[0].indexOf('\\n5,')==-1 && arguments[0].indexOf('\\n6,')==-1) : (arguments[0].indexOf('\\n4,')!=-1 && arguments[0].indexOf('\\n5,')!=-1 && arguments[0].indexOf('\\n6,')!=-1)) && (arguments[1] == '2' ? (arguments[0].indexOf('\\n7,')==-1 && arguments[0].indexOf('\\n8,')==-1 && arguments[0].indexOf('\\n9,')==-1) : (arguments[0].indexOf('\\n7,')!=-1 && arguments[0].indexOf('\\n8,')!=-1 && arguments[0].indexOf('\\n9,')!=-1)) ) ? '1' : '0'", self.vars["upload_data"], self.vars["upload_id"])
        assert(self.vars["upload_valid"] == "1")
        self.driver.find_element(By.CSS_SELECTOR, "button.close-button").click()
      self.driver.find_element(By.LINK_TEXT, "My Projects").click()
