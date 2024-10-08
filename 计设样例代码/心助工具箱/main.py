# encoding: utf-8
from PIL import Image
from VisCPM import VisCPMChat
import gradio as gr
import os
import time
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

TABLE_ROUTE = "/table"
iframe_dimensions = "height=480px width=1300px"

index_html = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心助工具箱</title>

    <style>
        body{
            background-image: url("https://github.com/NoraNotDora/hello-streamlit/raw/master/%E6%B8%90%E5%8F%98%E8%83%8C%E6%99%AF.png");
            background-size:cover;
        }
        .nav {
            text-indent: 50px;
            height: 90px;
            background-color: #fff;
        }

        .nav a {
            text-decoration: none;
            color: rgb(244, 105, 105);
            font-weight: 700;
            font-size: 19px;
            padding-right: 9px;
            padding-left: 1px;
            line-height: 96px;
        }

        .nav a:hover {
            color: rgb(223, 7, 64);
        }</style>
</head>
<body>
<div class="nav" >
        <a href="http://127.0.0.4:5500/">HOME</a>
        <a href="http://127.0.0.1:8000/">CHAT</a>
        <a href="http://127.0.0.3:8001">TEST</a>
        <a href="http://127.0.0.2:8080">TOOL</a>
    </div>

    <div><br>
    <h2 style="color:rgb(144, 110, 110);padding-left:50px">心晴日记</h2>
        <text style="border-width:1.5px;
        background-color: rgb(255, 249, 249)
        border-color: rgb(250, 227, 232);
        font-family:黑体;
        font-size: 17px;
        font-weight: 300;
        outline: none;
        color:rgb(150, 101, 101);">
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp说明：自动思维监控表填写步骤<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp1 记录下自己的情绪体验（用一个词或几个词来表示自己的情绪）<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp2 填写情景，周围发生了什么或者注意到/意识到什么<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp3 觉察自动思维内容，询问自己：在体验到这种情绪的时候，自己在想什么？<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp4 自动思维和情绪进行评估（1-10分）。
    </text><br><br><br><br>
"""+f"""
<div><center>
<iframe src={TABLE_ROUTE} {iframe_dimensions} style="box-shadow: 1px 2px 5px 2px rgba(245, 212, 216,0.5), 
                2px 2px 4px 3px rgba(245, 219, 229,0.5), 
                1px 3px 2px 3px rgba(246, 227, 245,0.5);
                border: 2px solid white;border-radius: 10px;background-color:#fff;"></iframe>
</center></div>
</div>

</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return index_html

def respond_to_table(records):
    res='自动思维记录表的最新记录如下：'
    scene ='情景：'+records['情景'][len(records)-1] # 根据最新的对话进行回复
    thought = '自动性思维：' + records['自动性思维'][len(records) - 1]
    emotion = '情绪：' + records['情绪'][len(records) - 1]
    score = '分数：' + str(records['分数'][len(records) - 1])
    res=res+scene+thought+emotion+score+'请给来访者进行分析，并鼓励来访者感知自己的情况，改变消极思维（要说成一段自然的话，我就是来访者）'

    response_raw = requests.post(url, headers=headers, json=data)
    response = response_raw.json()

    try:
        response = eval(response)
        if isinstance(response, list):
            response = response[0]
            response = response[0]
    except:
        response = response

    return response

table_app=gr.Interface(
        respond_to_table,
        [
            gr.Dataframe(
                label="自动思维记录表",
                headers=["情景", "自动性思维", "情绪","分数"],
                datatype=["str", "str", "str", "number"],
                row_count=1,
                col_count=(4, "fixed"),
            )
        ],
        outputs=[
            gr.Textbox(label="心晴正在思考中",lines=5)
        ],
    allow_flagging="never",
    css="footer {visibility: hidden;}"
    )
app = gr.mount_gradio_app(app, table_app, path=TABLE_ROUTE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.2', port=8080)