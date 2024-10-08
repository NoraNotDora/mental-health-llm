# encoding: utf-8
from PIL import Image
from VisCPM import VisCPMChat
import gradio as gr
import os
import time
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import base64

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

app = FastAPI()
CHAT_ROUTE = "/chat"
iframe_dimensions = "height=585px width=1300px"

index_html = ''' <!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>心语畅聊</title>

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
<div style="background-image:url("https://github.com/NoraNotDora/hello-streamlit/blob/master/%E6%B8%90%E5%8F%98%E8%83%8C%E6%99%AF.png");background-size:cover;height:900px""><br>
    <h2 style="color:rgb(144, 110, 110);padding-left:50px"> Chat —— 心语畅聊</h2>
<text style="border-width:1.5px;
        border-color: rgb(250, 227, 232);
        font-family:黑体;
        font-size: 17px;
        font-weight: 300;
        outline: none;
        color:rgb(150, 101, 101);">
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbspSTEP 1：在左方对话框和心晴聊聊你的心事 <br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbspSTEP 2：可以向心晴出示右方的OH卡表达你的想法<br>
</text><br>
'''+f'''<br>
    <div><center>
    <iframe src={CHAT_ROUTE} {iframe_dimensions} style="box-shadow: 1px 2px 5px 2px rgba(245, 212, 216,0.5), 
                2px 2px 4px 4px rgba(245, 219, 229,0.5), 
                1px 3px 2px 3px rgba(246, 227, 245,0.5);
                border: 2px solid white;border-radius: 10px;background-color:#fff;"></iframe>
    </center></div>
</div>
</body>
</html>
'''

prompt = """现在你扮演一位专业的心理咨询师，你具备丰富的心理学和心理健康知识。你擅长运用多种心理咨询技巧，例如认知行为疗法原则、动机访谈技巧和解决问题导向的短期疗法。以温暖亲切的语气，展现出共情和对来访者感受的深刻理解。以自然的方式与来访者进行对话，避免过长或过短的回应，确保回应流畅且类似人类的对话。提供深层次的指导和洞察，使用具体的心理概念和例子帮助来访者更深入地探索思想和感受。避免教导式的回应，更注重共情和尊重来访者的感受。根据来访者的反馈调整回应，确保回应贴合来访者的情境和需求。请为以下的对话生成一个回复。"""


@app.get("/", response_class=HTMLResponse)
def index():
    return index_html

path="./欧卡牌电子版/图卡"

def fake_gan():
    images = []
    for i in range(88):
        images.append((path +str(i+1)+".jpg", 'OH卡'+str(i+1)))
    return images

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.
def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history
count = 0

def bot(history):
    global count
    response_raw = requests.post(url, headers=headers, json=data)
    response=response_raw.json()
    try:
        response=eval(response)
        if isinstance(response, list):
            response = response[0]
            response = response[0]
    except:
        response=response
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history
    count = count + 1

def bot2(history):
    # Getting the base64 string
    print(history[-1][0][0])
    base64_image = encode_image(history[-1][0][0])
    response = response_raw.json()
    try:
        response = eval(response)
        if isinstance(response, list):
            response = response[0]
            response = response[0]
    except:
        response = response
    print(response)
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history
    pass

with gr.Blocks(
               css="""footer {visibility: hidden};"""
               ) as demo:
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(
                [],
                label='我是心晴🌈',
                elem_id="xinqing",
                bubble_full_width=False,
                avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
            )
            with gr.Row():
                txt = gr.Textbox(
                    scale=4,
                    show_label=False,
                    placeholder="想和心晴说说话吗？",
                    container=False,
                )
                btn = gr.UploadButton("上传图片🎨", file_types=["image", "video", "audio"])
                # gr.Image(value=os.path.join(os.path.dirname(__file__))+"\\flw.png")
        with gr.Column():
            gallery = gr.Gallery()
            btnn = gr.Button("展示OH卡").style(full_width=False)
            btnn.click(fake_gan, None, gallery)

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot2, chatbot, chatbot
    )
    chatbot.like(print_like_dislike, None, None)

demo.queue()

app = gr.mount_gradio_app(app, demo, path=CHAT_ROUTE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)