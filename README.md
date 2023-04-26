# SlidoGetQuestion

![GitHub repo size](https://img.shields.io/github/repo-size/ckctc/SlidoGetQuestion)

---

**Developed by: &nbsp; _[Chen Kuan-Chung](https://github.com/ckctc)_**

---

## 目錄

- [SlidoGetQuestion](#SlidoGetQuestion)
  - [目錄](#目錄)
  - [背景](#背景)
  - [用法](#用法)
  - [更新方向](#更新方向)
  - [Maintainers](#maintainers)

## 背景
第一屆政大電影節規劃舉行特殊放映聊天場，使用Slido網站讓現場觀眾留言，因無法使用Slido API，故開發此應用爬取留言內容。


## 用法 （示範畫面為v1.0.0）
1. 下載並運行 SlidoGetQuestion.exe
2. 於輸入框中輸入 Slido Event 的網址
>![url.png](https://drive.google.com/uc?id=1uIbm7WzlhFiG6UfqUlTo2YGYgJCb4iCB)
4. 將持續爬取並顯示最新的留言
>![ref.png](https://drive.google.com/uc?id=1wqKBo5Kph0vFQiICRB0qDITcl7_Q2q_X)
5. 應用實例（背景影片為 "Who Killed Captain Alex: Uganda's First Action Movie"）
>![example.png](https://drive.google.com/uc?id=1bOkETcLjauIsRdK0X0Ge5vMpcsV5aaMd)

## 更新方向
1. 完善UI/UX設計（由Tkinter轉為PyQt5）
2. QuestionBox繪製順序位置邏輯
3. 更改預設字型（目前因 Noto Sans TC 的 letterspacing 呈現上過於壅擠，故先使用微軟正黑體）
4. 新增英文版README.md
5. 優化程式效率及資源使用
6. 測試MacOS環境
7. 新增綁定「切換邊框模式熱鍵」之方式


## Maintainers

- [Chen Kuan-Cheng](https://github.com/ckctc)
