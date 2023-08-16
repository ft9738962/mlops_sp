import gradio as gr

from src.model.inference import load_model_predictor
from src.utils.config import get_config
from src.utils.directory_utils import find_root

# 加载模型
config = get_config()
model_path = find_root() / config['file_path']['model_path']

predictor = load_model_predictor(model_path)
print(predictor.predict({'sentence':['good']}))

def predict(comment:str) -> int:
    return predictor.predict({'sentence':[comment]})[0]


with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown('# 奥本海默评分预测家')
        gr.HTML('''
                <div style="width: 400px; height: 200px; overflow: hidden;">
                <img src="https://balboapark.org/wp-content/uploads/2023/06/Oppenheimer-Christopher-Nolan-0.jpeg" 
                alt="Oppenheimer Poster" style="width: 95%; object-fit: contain; object-position: 50% 50%;">
                </div>
                ''')
    with gr.Column():
        inp = gr.Textbox(lines=5, label='输入评论',placeholder="请发表评论...")
        pbtn = gr.Button("开始预测")
        out = gr.Number(label='预测评分')
    pbtn.click(fn=predict, inputs=inp, outputs=out)

demo.launch(debug=True)
