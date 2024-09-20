import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
from datetime import datetime
import re
import mysql.connector
from decimal import Decimal

# Đường dẫn đến chromedriver
chrome_driver_path = "C:/Users/hungb/Downloads/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Tham số tìm kiếm
params = {
    'From': 'Beijing (PEK)',
    'To': 'Hồ Chí Minh (SGN)',
    'Depart': '23/09/2024',
    'Return': '',
    'ADT': '1',
    'CHD': '0',
    'INF': '0'
}

# Xây dựng URL với tham số tìm kiếm
base_url = "https://www.bestprice.vn/ve-may-bay/tim-kiem-ve"
query_string = urlencode(params, doseq=True)
full_url = f"{base_url}?{query_string}"

print("URL: ", full_url)

driver.get(full_url)
time.sleep(15)

# Thiết lập kết nối MySQL
db = mysql.connector.connect(
    host='116.205.225.217',
    port=16306,
    database='yueya',
    user='root',
    password='6+Qj!hKT#D*1-YL<',
    charset='utf8mb4',
)
cursor = db.cursor()

sql = """
INSERT INTO yueya_airroute (start_cityname, start_citycode, mid_cityname, end_cityname, end_citycode, air_no, air_company, air_duration, step, start_time, end_time, start_price, normal_price, enable, source, createtime)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Chờ trang tải đầy đủ
try:
    flight_data_content = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "flight_data_content_depart"))
    )
    bpv_list_items = flight_data_content.find_elements(By.CLASS_NAME, 'bpv-list-item')

    print(f"Đã tìm thấy {len(bpv_list_items)} thẻ 'bpv-list-item'.")

    directory_path = "D:/Juhard"
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, 'flight_data.txt')

 
    for index, item in enumerate(bpv_list_items):
        try:
            flight_details_div = item.find_element(By.CLASS_NAME, 'flight-details')
            info_element = flight_details_div.find_element(By.CLASS_NAME, 'sep-line')
            info_html = info_element.get_attribute('outerHTML')
            soup = BeautifulSoup(info_html, 'html.parser')

            # lấy thông tin chuyến bay 1
            flight_from_1 = soup.find('b', class_='data_flight_from').get_text(strip=True)
            airport_from_1 = soup.find_all('div', class_='margin-bottom-5')[1].get_text(strip=True)
            flight_time_from_1 = soup.find('b', class_='data_flight_time_from').get_text(strip=True)
            flight_date_from_1 = soup.find('span', class_='data_flight_date_from').get_text(strip=True)
            flight_code_1 = soup.find('span', class_='data_flight_airline_code').get_text(strip=True)
            airline_name_1 = soup.find('strong').get_text(strip=True)

            # lấy thông tin chuyến bay 2
            flight_from_2_elements = soup.find_all('b', class_='data_flight_from')
            airport_from_2_elements = soup.find_all('div', class_='margin-bottom-5')
            flight_time_from_2_elements = soup.find_all('b', class_='data_flight_time_from')
            flight_date_from_2_elements = soup.find_all('span', class_='data_flight_date_from')
            flight_code_2_elements = soup.find_all('span', class_='data_flight_airline_code')
            airline_name_2_elements = soup.find_all('strong')

            if len(flight_from_2_elements) > 1 and len(airport_from_2_elements) > 6 and len(flight_time_from_2_elements) > 1:
                flight_from_2 = flight_from_2_elements[1].get_text(strip=True)
                airport_from_2 = airport_from_2_elements[6].get_text(strip=True)
                flight_time_from_2 = flight_time_from_2_elements[1].get_text(strip=True)
                flight_date_from_2 = flight_date_from_2_elements[1].get_text(strip=True)
                flight_code_2 = flight_code_2_elements[1].get_text(strip=True)
                airline_name_2 = airline_name_2_elements[1].get_text(strip=True)
            else:
                flight_from_2 = ''
                airport_from_2 = ''
                flight_time_from_2 = ''
                flight_date_from_2 = ''
                flight_code_2 = ''
                airline_name_2 = ''

            # Lấy thông tin điểm đến
            flight_to_elements = soup.find_all('b', class_='data_flight_to')
            airport_to_elements = soup.find_all('div', class_='margin-bottom-5')
            flight_time_to_elements = soup.find_all('b', class_='data_flight_time_to')


            # Lấy thông tin điểm đến 1
            if len(flight_to_elements) > 0:
                flight_to_1 = flight_to_elements[0].get_text(strip=True) if len(flight_to_elements) > 0 else ''
            else:
                flight_to_1 = ''

            if len(airport_to_elements) > 4:
                airport_to_1 = airport_to_elements[5].get_text(strip=True) if len(airport_to_elements) > 4 else ''
            else:
                airport_to_1 = ''

            if len(flight_time_to_elements) > 0:
                flight_time_to_1 = flight_time_to_elements[0].get_text(strip=True) if len(airport_to_elements) > 0 else ''
                date_text_1 = flight_time_to_elements[0].next_sibling.strip()
            else:
                flight_time_to_1 = ''


            # Lấy thông tin điểm đến 2
            if len(flight_to_elements) > 1 and len(airport_to_elements) > 9 and len(flight_time_to_elements) > 1:
                flight_to_2 = flight_to_elements[1].get_text(strip=True)
                airport_to_2 = airport_to_elements[12].get_text(strip=True)
                flight_time_to_2 = flight_time_to_elements[1].get_text(strip=True)
                date_text_2 = flight_time_to_elements[1].next_sibling.strip()
            else:
                flight_to_2 = ''
                airport_to_2 = ''
                flight_time_to_2 = ''
                date_text_2 = ''


            # Kiểm tra thông tin đổi máy bay
            try:
                change_flight_divs = flight_details_div.find_elements(By.CLASS_NAME, 'change-flight-time')
                if change_flight_divs:
                    change_flight_div = BeautifulSoup(change_flight_divs[0].get_attribute('innerHTML'), 'html.parser')
                    destination_elements = change_flight_div.find_all('b')
                    if len(destination_elements) > 1:
                        destination = destination_elements[0].get_text(strip=True)
                        wait_time = destination_elements[1].get_text(strip=True)
                    else:
                        destination = ''
                        wait_time = ''
                else:
                    destination = ''
                    wait_time = ''
            except Exception as e:
                destination = ''
                wait_time = ''
                print(f"Đã xảy ra lỗi khi kiểm tra thông tin đổi máy bay: {e}")
            

            # Thông tin về chuyến bay 1
            city_name_start_1 = flight_from_1.split(' (')[0]
            city_code_start_1 = flight_from_1.split('(')[1].replace(')', '')
            city_name_to_1 = flight_to_1.split(' (')[0]
            city_code_to_1 = flight_to_1.split('(')[1].replace(')', '')

            date_to_1 = date_text_1.strip(', ')
            time_start_1 = flight_date_from_1 + " " + flight_time_from_1
            time_to_1 = date_to_1 + " " + flight_time_to_1
            date_time_start_1 = datetime.strptime(time_start_1, "%d-%m-%Y %H:%M")
            format_time_start_1 = date_time_start_1.strftime("%Y-%m-%d %H:%M")
            date_time_to_1 = datetime.strptime(time_to_1, "%d-%m-%Y %H:%M")
            format_time_to_1 = date_time_to_1.strftime("%Y-%m-%d %H:%M")

            # Thông tin về chuyến bay 2
            city_name_start_2 = flight_from_2.split(' (')[0]
            city_code_start_2 = flight_from_2.split('(')[1].replace(')', '')
            city_name_to_2 = flight_to_2.split(' (')[0]
            city_code_to_2 = flight_to_2.split('(')[1].replace(')', '')

            date_to_2 = date_text_2.strip(', ')
            time_start_2 = flight_date_from_2 + " " + flight_time_from_2
            time_to_2 = date_to_2 + " " + flight_time_to_2
            date_time_start_2 = datetime.strptime(time_start_2, "%d-%m-%Y %H:%M")
            format_time_start_2 = date_time_start_2.strftime("%Y-%m-%d %H:%M")
            date_time_to_2 = datetime.strptime(time_to_2, "%d-%m-%Y %H:%M")
            format_time_to_2 = date_time_to_2.strftime("%Y-%m-%d %H:%M")

            
            price_element = flight_details_div.find_element(By.CLASS_NAME, 'pull-right')
            price_html = price_element.get_attribute('outerHTML')
            soup = BeautifulSoup(price_html, 'html.parser')

            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rows2 = soup.find_all('div', class_='row')
    
            for row in rows2:
                value_div = row.find('div', class_='price-total')
                value = value_div.get_text(strip=True) if value_div else ''
                total_price = re.sub(r'\D', '', value)

                if total_price:
                    total_price_decimal = Decimal(total_price) / Decimal('100') 

                    # Thực hiện chèn dữ liệu vào MySQL
                    values = (city_name_start_1, city_code_start_1, destination, city_name_to_2, city_code_to_2, flight_code_1, airline_name_1, 0, 2, format_time_start_1, format_time_to_2, total_price, total_price, 1, 'bestprice.vn', create_time)
            

            cursor.execute(sql, values)

        except Exception as inner_e:
            print(f"Đã xảy ra lỗi khi xử lý thẻ div 'bpv-list-item' số {index+1}: {inner_e}")

     # Lưu thay đổi vào MySQL
    db.commit()
    print(f"Nội dung đã được lưu vào cơ sở dữ liệu.")

except Exception as e:
    print("Đã xảy ra lỗi:", e)

finally:
    driver.quit()
    cursor.close()
    db.close()
