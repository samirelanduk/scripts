from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
import json

USERNAME = ""
PASSWORD = ""

browser = Chrome()
browser.get("https://www.myfitnesspal.com/account/login")
form = browser.find_element_by_class_name("LoginForm")
email, password = form.find_elements_by_tag_name("input")[2:4]
email.send_keys(USERNAME)
password.send_keys(PASSWORD)
submit = form.find_element_by_class_name("submit").find_element_by_tag_name("input")
submit.click()

browser.get("http://www.myfitnesspal.com/food/diary/")
data = []
while True:
    prev = browser.find_element_by_class_name("icon-caret-left")
    prev.click()
    time = browser.find_element_by_tag_name("time")
    row = browser.find_element_by_class_name("total")
    cells = row.find_elements_by_tag_name("td")
    values = [int(cell.text.replace(",", "")) for cell in cells[1:-1]]
    data.append({
     "day": time.text, "calories": values[0],
     "carbs": values[1], "fat": values[2],
     "protein": values[3], "sugar": values[5]
    })
    with open("mfp.json", "w") as f:
        json.dump(data, f)


browser.quit()
