import os
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time

def scrape_flight_data(chrome_driver_path, from_location, to_location, depart_date, return_date, adt, chd, inf):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Tham số tìm kiếm
    params = {
        'From': from_location,
        'To': to_location,
        'Depart': depart_date,
        'Return': return_date,
        'ADT': adt,
        'CHD': chd,
        'INF': inf
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
                    # Tìm flight-details div
                    flight_details_div = item.find_element(By.CLASS_NAME, 'flight-details')

                    # Tìm thẻ chứa thông tin
                    flight_info_html = flight_details_div.get_attribute('innerHTML')
                    soup = BeautifulSoup(flight_info_html, 'html.parser')

                    # Trích xuất thông tin chuyến bay 1
                    flight_from_1 = soup.find('b', class_='data_flight_from').get_text(strip=True) if soup.find('b', class_='data_flight_from') else ''
                    airport_from_1 = soup.find_all('div', class_='margin-bottom-5')[1].get_text(strip=True) if len(soup.find_all('div', class_='margin-bottom-5')) > 1 else ''
                    flight_time_from_1 = soup.find('b', class_='data_flight_time_from').get_text(strip=True) if soup.find('b', class_='data_flight_time_from') else ''
                    flight_date_from_1 = soup.find('span', class_='data_flight_date_from').get_text(strip=True) if soup.find('span', class_='data_flight_date_from') else ''
                    flight_code_1 = soup.find('span', class_='data_flight_airline_code').get_text(strip=True) if soup.find('span', class_='data_flight_airline_code') else ''
                    airline_name_1 = soup.find('strong').get_text(strip=True) if soup.find('strong') else ''

                    # Lưu thông tin chuyến bay vào file
                    file.write(f"Infor ticket {index+1}:\n")
                    file.write(f"Từ: {flight_from_1}, {airport_from_1}\n")
                    file.write(f"Thời gian đi: {flight_time_from_1}, {flight_date_from_1}\n")
                    file.write(f"Sân bay đi: {flight_code_1} - {airline_name_1}\n\n")

                    # Trích xuất giá vé
                    price_element = flight_details_div.find_element(By.CLASS_NAME, 'pull-right')
                    price_html = price_element.get_attribute('outerHTML')
                    price_soup = BeautifulSoup(price_html, 'html.parser')

                    price_rows = price_soup.find_all('div', class_='row margin-bottom-10')
                    for row in price_rows:
                        label = row.find('div', class_='col-xs-6').get_text(strip=True) if row.find('div', class_='col-xs-6') else ''
                        value = row.find('div', class_='price-value').get_text(strip=True) if row.find('div', class_='price-value') else ''
                        if label and value:
                            file.write(f"{label}: {value}\n")

                    file.write("\n---------------------------------------------------\n\n")

                except Exception as inner_e:
                    print(f"Đã xảy ra lỗi khi xử lý thẻ 'bpv-list-item' số {index+1}: {inner_e}")

        print(f"Nội dung đã được ghi vào file '{file_path}'")

    except Exception as e:
        print("Đã xảy ra lỗi:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Công cụ lấy dữ liệu chuyến bay.")
    parser.add_argument('--from_location', type=str, required=True, help='Nơi khởi hành (vd: Shanghai (PVG))')
    parser.add_argument('--to_location', type=str, required=True, help='Nơi đến (vd: Hà Nội (HAN))')
    parser.add_argument('--depart_date', type=str, required=True, help='Ngày khởi hành (vd: 16/09/2024)')
    parser.add_argument('--return_date', type=str, default='', help='Ngày về (tùy chọn)')
    parser.add_argument('--adt', type=str, default='1', help='Số người lớn')
    parser.add_argument('--chd', type=str, default='0', help='Số trẻ em')
    parser.add_argument('--inf', type=str, default='0', help='Số em bé')
    parser.add_argument('--chrome_driver_path', type=str, required=True, help='Đường dẫn đến chromedriver')

    args = parser.parse_args()

    # Gọi hàm scrape_flight_data với các tham số từ dòng lệnh
    scrape_flight_data(
        chrome_driver_path=args.chrome_driver_path,
        from_location=args.from_location,
        to_location=args.to_location,
        depart_date=args.depart_date,
        return_date=args.return_date,
        adt=args.adt,
        chd=args.chd,
        inf=args.inf
    )
