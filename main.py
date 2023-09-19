from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import time
import random
import logging

# Configure logging
log_file = "availability_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# User-agent to simulate a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

url = "https://nl.gymshark.com/products/gymshark-worldwide-graphic-oversized-t-shirt-white-ss23?gclid=Cj0KCQjwwvilBhCFARIsADvYi7JFF0ecZwQyvoNMiaxbto8Rwy8dITcUn7aFF07GnoB0cAXPa2P1S8kaAs6FEALw_wcB"


def check_availability(url, size):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during the request: {e}")
        return False

    soup = BeautifulSoup(response.content, "html.parser")
    size_buttons = soup.select('div.add-to-cart_sizes__qtfGR button')

    available_sizes = []
    for button in size_buttons:
        if "size_size--out-of-stock__hBcxj" not in button.get('class', []):
            available_sizes.append(button.text.strip())

    return size in available_sizes


def send_notification():
    noti_link = "https://maker.ifttt.com/trigger/available/with/key/dKhXKhDB-IF3R_qhVRkhD2ue5Dw2nR1_xcFBhKivbVZ"
    requests.post(noti_link)


if __name__ == "__main__":
    os.system("cls")

    logging.info("Starting script! [Sending test notification]")
    send_notification()

    size_to_check = "l"  # Change this to the desired size to check
    count = 0
    while True:
        try:
            if check_availability(url, size_to_check):
                logging.info("T-Shirt size 'L' is now available. Notification sent.")
                send_notification()
                break
            else:
                logging.info(f"T-Shirt size not available. Tried {count} times")
                count += 1
        except KeyboardInterrupt:
            logging.info("Exiting the script.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        # Wait for a random time between 10 and 15 minutes (in seconds)
        random_wait_time = random.randint(600, 900)
        time.sleep(random_wait_time)
