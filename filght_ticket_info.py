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

# Đường dẫn đến chromedriver
chrome_driver_path = "C:/Users/hungb/Downloads/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Tham số tìm kiếm
params = {
    'From': 'Shanghai (PVG)',
    'To': 'Hà Nội (HAN)',
    'Depart': '20/09/2024',
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

    with open(file_path, 'w', encoding='utf-8') as file:
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

                # Ghi vào file
                file.write(f"Infor ticket {index+1}:\n")
                file.write("Chuyến bay 1:\n")
                # file.write(f"Từ: {flight_from_1}, {airport_from_1}\n")
                file.write(f"Tên thành phố đi: {city_name_start_1}\n")
                file.write(f"Mã thành phố đi: {city_code_start_1}\n")
                file.write(f"Thời gian đi: {format_time_start_1}\n")
                file.write(f"Sân bay đi: {airport_from_1}\n")
                file.write(f"Mã máy bay: {flight_code_1}\n")
                file.write(f"Hãng bay: {airline_name_1}\n")
                file.write(f"Tên thành phố đến: {city_name_to_1}\n")
                file.write(f"Mã thành phố đến: {city_code_to_1}\n")
                file.write(f"Thời gian đến: {format_time_to_1}\n")
                file.write(f"Sân bay đến: {airport_to_1}\n\n")

                if destination != '' and wait_time != '':
                    file.write(f"Thông tin đổi máy bay:\n")
                    file.write(f"Đổi máy bay tại: {destination}\n")
                    file.write(f"Thời gian chờ: {wait_time}\n\n")

                if flight_from_2 and airport_from_2 and flight_time_from_2 and flight_date_from_2 and flight_code_2 and airline_name_2 and flight_to_2 and airport_to_2 and flight_time_to_2:
                    file.write("Chuyến bay 2:\n")
                    file.write(f"Tên thành phố đi: {city_name_start_2}\n")
                    file.write(f"Mã thành phố đi: {city_code_start_2}\n")
                    file.write(f"Sân bay đi: {airport_to_1}\n")
                    file.write(f"Thời gian đi: {format_time_start_2}\n")
                    file.write(f"Mã máy bay: {flight_code_2}\n")
                    file.write(f"Hãng bay: {airline_name_2}\n")
                    file.write(f"Tên thành phố đến: {city_name_to_2}\n")
                    file.write(f"Mã thành phố đến: {city_code_to_2}\n")
                    file.write(f"Thời gian đến: {format_time_to_2}\n")
                    file.write(f"Sân bay đến: {airport_to_2}\n\n")

                file.write(f"Price(VND):\n")

                price_element = flight_details_div.find_element(By.CLASS_NAME, 'pull-right')
                price_html = price_element.get_attribute('outerHTML')
                soup = BeautifulSoup(price_html, 'html.parser')

                rows = soup.find_all('div', class_='row margin-bottom-10')
                for row in rows:
                    label_div = row.find('div', class_='col-xs-6')
                    label = label_div.get_text(strip=True) if label_div else ''
                    value_div = row.find('div', class_='price-value')
                    value = value_div.get_text(strip=True) if value_div else ''
                    file.write(f"{label} {value}\n")

                rows2 = soup.find_all('div', class_='row')
                for row in rows2:
                    label_div = row.find('div', class_='label-total')
                    label = label_div.get_text(strip=True) if label_div else ''
                    value_div = row.find('div', class_='price-total')
                    value = value_div.get_text(strip=True) if value_div else ''
                    total_price = re.sub(r'\D', '', value)
                    # format_total_price = int(total_price)
                    if label and value:
                        file.write(f"----------------------\n")
                        file.write(f"{label} {total_price} VND\n")

                file.write("\n------------------------------------------------------------------------------\n\n")

            except Exception as inner_e:
                print(f"Đã xảy ra lỗi khi xử lý thẻ div 'bpv-list-item' số {index+1}: {inner_e}")

    print(f"Nội dung đã được ghi vào file '{file_path}'")

except Exception as e:
    print("Đã xảy ra lỗi:", e)

finally:
    driver.quit()
