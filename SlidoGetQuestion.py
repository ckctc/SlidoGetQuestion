from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk
from tkinter import simpledialog
import tkinter.font as tkFont

import textwrap


root = tk.Tk()
root.title('Slido Questions')
root.overrideredirect(False)


BORDERLESS_HOTKEY = "<Control-Shift-C>"

MAX_QUESTIONS = 10

BOX_WIDTH = 280
BOX_HEIGHT = 60
BOX_fill_COLOR = 'black'
BOX_OUTLINE_COLOR = 'black'
BOX_SPACING = 10
RADIUS = 5

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 750

fill_COLOR = 'white'
AUTHOR_FONT = tkFont.Font(family='微軟正黑體', size=8)
CONTENT_FONT = tkFont.Font(family='微軟正黑體', size=12, weight='bold')
VOTE_FONT = tkFont.Font(family='微軟正黑體', size=12)


current_questions = []

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='green', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

url = simpledialog.askstring("Slido URL", "Enter the Slido URL:")
driver.get(url)


def on_keys_press(event):
    HOTKEY = event.keysym
    dialog_title = "Hotkey Setting"
    diakog_text = "Press the hotkey you want to bind: "
    HOTKEY = simpledialog.askstring(dialog_title, diakog_text)
    root.focus_set()


def toggle_borderless(event=None):
    current_BorderState = root.overrideredirect()
    root.overrideredirect(not current_BorderState)


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

    canvas.delete(tk.ALL)

    global current_questions

    current_questions = get_questions(driver)
    current_questions.reverse()

    while len(current_questions) > MAX_QUESTIONS:
        question_box = current_questions.pop(0)
        if 'box' in question_box:
            box_id = question_box.pop('box')
            canvas.delete(box_id)

    y = 10
    canvas_height = 0

    for i, question in enumerate(current_questions):
        content_lines = textwrap.wrap(question['content'], width=12)
        num_lines = len(content_lines)
        content_text = '\n'.join(content_lines)

        box_height = 50 + 20 * num_lines

        x1, y1 = 10, y
        x2, y2 = 10+BOX_WIDTH, y+box_height
        arc = 2 * RADIUS
        box_arc1 = canvas.create_arc(x1, y1, x1+arc, y1+arc, start=90, extent=90, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)
        box_arc2 = canvas.create_arc(x2-arc, y1, x2, y1+arc, start=0, extent=90, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)
        box_arc3 = canvas.create_arc(x1, y2-arc, x1+arc, y2, start=180, extent=90, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)
        box_arc4 = canvas.create_arc(x2-arc, y2-arc, x2, y2, start=270, extent=90, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)
        box_rectangle1 = canvas.create_rectangle(x1+RADIUS, y1, x2-RADIUS, y2, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)
        box_rectangle2 = canvas.create_rectangle(x1, y1+RADIUS, x2, y2-RADIUS, fill=BOX_fill_COLOR, outline=BOX_OUTLINE_COLOR)

        author = canvas.create_text(
            20, y+10, anchor=tk.NW, text=question['author'], font=AUTHOR_FONT, fill=fill_COLOR)
        content = canvas.create_text(
            20, y+box_height-10-20*num_lines, anchor=tk.NW, text=content_text, font=CONTENT_FONT, fill=fill_COLOR)
        vote = canvas.create_text(
            280, y+box_height-30, anchor=tk.NE, text=f"❤ {question['vote']}", font=VOTE_FONT, fill=fill_COLOR)

        question['box_arc1'] = box_arc1
        question['box_arc2'] = box_arc2
        question['box_arc3'] = box_arc3
        question['box_arc4'] = box_arc4
        question['box_rectangle1'] = box_rectangle1
        question['box_rectangle2'] = box_rectangle2
        question['author'] = author
        question['text'] = content
        question['vote'] = vote

        y += box_height + BOX_SPACING
        canvas_height += box_height + BOX_SPACING

        if i == MAX_QUESTIONS - 1:
            break

    current_questions.reverse()
    canvas.configure(scrollregion=(0, 0, WINDOW_WIDTH,
                     canvas_height + BOX_SPACING))
    canvas.yview_moveto(1.0)
    canvas.after(1000, update_questions)


root.bind(BORDERLESS_HOTKEY, toggle_borderless)

root.after(3000, update_questions)

root.mainloop()

driver.quit()
