from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk


def click_Recent_tab(driver):
    # Wait for the "Recent" tab to become visible
    Recent_tab = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Recent']")))

    # Click on the "Recent" tab
    Recent_tab.click()

    # Wait for the new order of questions to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".question-item__body")))


def get_questions(driver):

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.question-item__body')))

    click_Recent_tab(driver)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all('div', class_='question-item__body')
    votes = soup.find_all(
        'button', class_='score__btn score__btn--plus btn-plain')

    questions = []
    for i, (comment, vote) in enumerate(zip(comments, votes)):
        question_text = comment.text.strip()
        vote_text = vote.get('aria-label').split()[0]
        questions.append(f'{question_text} ({vote_text} votes)')

    return questions


def update_questions():

    current_questions = get_questions(driver)

    questions_text.delete('1.0', tk.END)
    for question in current_questions:
        questions_text.insert(tk.END, f'{question}\n')

    root.after(3000, update_questions)


chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://app.sli.do/event/fHCaUDHRvdDdVFAQt8ABnv/live/questions")

root = tk.Tk()
root.title('Slido Questions')
questions_text = tk.Text(root, width=50, height=20)
questions_text.pack()

root.after(3000, update_questions)

root.mainloop()

driver.quit()
