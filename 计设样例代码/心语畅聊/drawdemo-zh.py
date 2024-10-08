# encoding: utf-8
from PIL import Image
from VisCPM import VisCPMChat
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
DRAW_ROUTE = "/draw"
iframe_dimensions = "height=585px width=1300px"

index_html = ''' <!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Draw</title>

    <style>
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
<div style="background-color:rgb(255, 249, 249);height:900px""><br>
    <h2 style="color:rgb(144, 110, 110);padding-left:50px"> Draw —— 解析您绘画心理的小助手</h2>
<text style="border-width:1.5px;
        background-color: rgb(255, 249, 249)
        border-color: rgb(250, 227, 232);
        font-family:黑体;
        font-size: 17px;
        font-weight: 300;
        outline: none;
        color:rgb(150, 101, 101);">
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbspSTEP 1：点击“绘画”按钮跳转开展绘画，并将您的画保存至本地 <br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbspSTEP 2：点击下方的空白展示框或“上传”按钮可上传您想分析的图片<br>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbspSTEP 3：在文本框进行聊天<br>
</text><br>
'''+f'''<br>
    <div style="background-color: rgb(255, 249, 249)"><center>
    <iframe src={DRAW_ROUTE} {iframe_dimensions} style="box-shadow: 1px 2px 5px 2px rgba(245, 212, 216,0.5), 
                2px 2px 4px 4px rgba(245, 219, 229,0.5), 
                1px 3px 2px 3px rgba(246, 227, 245,0.5);
                border: 2px solid white;border-radius: 10px;background-color:#fff;"></iframe>
    </center></div>
</div>
</body>
</html>
'''

# ========================================
#             Model Initialization
# ========================================

model_path = '/root/autodl-tmp/pytorch_model.zhplus.bin'
viscpm_chat = VisCPMChat(model_path, image_safety_checker=False)
print("load  model  success !")

# ========================================
#             Gradio Setting
# ========================================


def upload_img(image,_chatbot,_app_session):
    image = Image.fromarray(image)
    _app_session['sts']=None
    _app_session['ctx']="这里可以写提示词"
    _app_session['img']=image
    # _chatbot.append(('图片解析成功，可以和我对话了', ''))
    return _chatbot,_app_session

def respond( _question, _chat_bot,_app_cfg):
    _answer, _context, sts = viscpm_chat.chat(_app_cfg['img'], _question, _app_cfg['ctx'],
                                            vision_hidden_states=_app_cfg['sts'])
    _chat_bot.append((_question, _answer))
    _app_cfg['ctx']=_context
    _app_cfg['sts']=sts
    print('use it:')
    print(_app_cfg['img'])
    return '',_chat_bot,_app_cfg

@app.get("/", response_class=HTMLResponse)
def index():
    return index_html

with gr.Blocks(theme='ParityError/Anime',css="""footer {visibility: hidden};
                    theme='ParityError/Anime';
                    .gradio-container{background-color:white;}
                    """) as drawdemo:
    app_session = gr.State({'sts':None,'ctx':None,'img':None})
    with gr.Row():
        with gr.Column():
            bt_pic = gr.Image(label="先上传一张图片")
            draw=gr.Button("心情画板",link="http://127.0.0.1:5500/toPaint/index.html")
            # upload_button = gr.Button(value="上传 & 开始聊天", interactive=True, variant="primary")
            # clear = gr.Button("重画")#要接一个清除的函数
        with gr.Column():
            chat_bot = gr.Chatbot(label="心晴解画")
            txt_message = gr.Textbox(label="关于这幅画有什么想说的吗？")

    txt_message.submit(respond, [ txt_message, chat_bot,app_session], [txt_message,chat_bot,app_session])
    bt_pic.upload(lambda: None, None, chat_bot, queue=False).then(upload_img, inputs=[bt_pic,chat_bot,app_session], outputs=[chat_bot,app_session])

# drawdemo.launch(share=True, enable_queue=True)

app = gr.mount_gradio_app(app, drawdemo, path=DRAW_ROUTE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=8080,share=True)