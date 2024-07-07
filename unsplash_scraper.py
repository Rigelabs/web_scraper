from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request


#run chrome in headless mode
options = Options()
"""
Comment out the --headless option, if you want Selenium to launch a Chrome window with the GUI. 
That will allow you to follow what the script does on the page in real time, which is useful for debugging. On production, keep the --headless option activated to save resources.
"""
options.add_argument("--headless") #comment while developing

#initialize a Chrme webDriver instance with the options
driver = webdriver.Chrome(service=ChromeService(executable_path="./chromedriver.exe"),options=options)

driver.maximize_window()

#You can now instruct Chrome to connect to the target page via Selenium by using the get() method:

url = "https://unsplash.com/s/photos/healthy potato?license=free"
driver.get(url)

#Use the findElements() method to select all desired HTML image nodes on the page

image_html_nodes = driver.find_elements(By.CSS_SELECTOR, "[data-test=\"photo-grid-masonry-img\"]")

image_urls = []

"""
Iterate over the nodes in image_html_nodes, collect the URL in src or the URL of the largest image from srcset (if present), and add it to image_urls:
"""
for image_html_node in image_html_nodes:
  try:
    # use the URL in the "src" as the default behavior
    image_url = image_html_node.get_attribute("src")

    # extract the URL of the largest image from "srcset",
    # if this attribute exists
    srcset =  image_html_node.get_attribute("srcset")
    if srcset is not None:
      # get the last element from the "srcset" value
      srcset_last_element = srcset.split(", ")[-1]
      # get the first element of the value,
      # which is the image URL
      image_url = srcset_last_element.split(" ")[0]

    # add the image URL to the list
    image_urls.append(image_url)
  except StaleElementReferenceException as e:
    continue
  
print(image_urls)

image_name_counter = 1

# download each image and add it
# to the "/images" local folder
for image_url in image_urls:
  print(f"downloading image no. {image_name_counter} ...")

  file_name = f"./images/{image_name_counter}.jpg"
  # download the image
  urllib.request.urlretrieve(image_url, file_name)

  print(f"images downloaded successfully to \"{file_name}\"\n")

  # increment the image counter
  image_name_counter += 1

# close the browser and free up its resources
driver.quit()
