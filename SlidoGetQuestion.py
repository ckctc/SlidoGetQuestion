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
BOX_HEIGHT = 50
BOX_FILL_COLOR = 'white'
BOX_OUTLINE_COLOR = 'green'

font_author = tkFont.Font(family='Noto Sans TC', size=8)
font_content = tkFont.Font(family='Noto Sans TC', size=12, weight='bold')
font_vote = tkFont.Font(family='Noto Sans TC', size=12)

current_questions = []

canvas = tk.Canvas(root, width=300, height=705, bg='green')
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

    new_questions = get_questions(driver)

    current_questions = new_questions + \
        current_questions[:MAX_QUESTIONS-len(new_questions)]

    current_questions.reverse()

    while len(current_questions) > MAX_QUESTIONS:
        question_box = current_questions.pop(0)
        if 'box' in question_box:
            canvas.delete(question_box['box'])

    for i, question in enumerate(current_questions):
        y = 10 + i * 70

        if 'box' in question:
            canvas.itemconfigure(question['author'], text=question['author'])
            canvas.itemconfigure(question['text'], text=question['content'])
            vote = question.get('vote', 0)
            canvas.itemconfigure(
                question['vote'], text=f'{vote} votes')

        else:
            box = canvas.create_rectangle(
                10, y, 290, y+60, fill=BOX_FILL_COLOR, outline='green')
            author = canvas.create_text(
                20, y+10, anchor=tk.NW, text=question['author'], font=font_author)
            content = canvas.create_text(
                20, y+30, anchor=tk.NW, text=question['content'], font=font_content)
            vote = canvas.create_text(
                280, y+30, anchor=tk.NE, text=f"{question['vote']} votes", font=font_vote)
            question['box'] = box
            question['author'] = author
            question['text'] = content
            question['vote'] = vote

    current_questions.reverse()

    root.after(1500, update_questions)


chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://app.sli.do/event/fHCaUDHRvdDdVFAQt8ABnv/live/questions')

# questions_text = tk.Text(root, width=50, height=20)
# questions_text.pack()

root.after(3000, update_questions)

root.mainloop()

driver.quit()
