from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk
import tkinter.font as tkFont

import textwrap

root = tk.Tk()
root.title('Slido Questions')
root.attributes('-transparentcolor', 'green')

MAX_QUESTIONS = 10

BOX_WIDTH = 280
BOX_HEIGHT = 60
BOX_FILL_COLOR = 'white'
BOX_OUTLINE_COLOR = 'green'

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 705

font_author = tkFont.Font(family='Noto Sans TC', size=8)
font_content = tkFont.Font(family='微軟正黑體', size=12, weight='bold')
font_vote = tkFont.Font(family='Noto Sans TC', size=12)

current_questions = []

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='green')
canvas.pack(fill=tk.BOTH, expand=tk.YES)


def click_Recent_tab(driver):
    # Wait for the 'Recent' tab to become visible''
    Recent_tab = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Recent']")))

    # Click on the 'Recent' tab
    Recent_tab.click()

    # Wait for the new order of questions to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".question-item__body")))


def get_questions(driver):

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.question-item__body')))

    click_Recent_tab(driver)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    authors = soup.find_all('div', class_='question-item__author truncate')
    comments = soup.find_all('div', class_='question-item__body')
    votes = soup.find_all(
        'button', class_='score__btn score__btn--plus btn-plain')

    questions = []
    for i, (author, comment, vote) in enumerate(zip(authors, comments, votes)):
        author_text = author.text.strip()
        question_text = comment.text.strip()
        vote_text = vote.get('aria-label').split()[0]
        questions.append(
            {'author': author_text, 'content': question_text, 'vote': vote_text})

    return questions


def update_questions():

    global current_questions

    current_questions = get_questions(driver)

    current_questions.reverse()

    while len(current_questions) > MAX_QUESTIONS:
        question_box = current_questions.pop(0)
        if 'box' in question_box:
            canvas.delete(question_box['box'])

    y = 10  # 初始化y座標位置

    for i, question in enumerate(current_questions):
        content_lines = textwrap.wrap(question['content'], width=12)
        num_lines = len(content_lines)
        content_text = '\n'.join(content_lines)

        # 計算box的高度
        box_height = 50 + 20 * num_lines

        box = canvas.create_rectangle(
            10, y, 10+BOX_WIDTH, y+box_height, fill=BOX_FILL_COLOR, outline='green')
        author = canvas.create_text(
            20, y+10, anchor=tk.NW, text=question['author'], font=font_author)
        content = canvas.create_text(
            20, y+box_height-10-20*num_lines, anchor=tk.NW, text=content_text, font=font_content)
        vote = canvas.create_text(
            280, y+box_height-30, anchor=tk.NE, text=f"{question['vote']} votes", font=font_vote)

        question['box'] = box
        question['author'] = author
        question['text'] = content
        question['vote'] = vote

        # 更新y座標位置
        y += box_height + 10  # 加上10像素的間距

        if i == MAX_QUESTIONS - 1:
            break

    current_questions.reverse()
    root.after(1500, update_questions)


chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://app.sli.do/event/fHCaUDHRvdDdVFAQt8ABnv/live/questions')

root.after(3000, update_questions)

root.mainloop()

driver.quit()
