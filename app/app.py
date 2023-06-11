from flask import Flask, render_template, request
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route('/chain', methods=['post'])
def chain():
  llm = OpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0)
  tools = load_tools(["serpapi", "llm-math"], llm=llm)
  agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
  # prompt = request.args.get('prompt')
  # response = agent.run(prompt)
  instruction = request.form.get('instruction')
  output_format = request.form.get('output_format')

  prompt = instruction + 'について、Web上の最新情報でリサーチした内容を元に日本語で'
  if output_format == 'mindmap':
      diagram = agent.run(prompt + 'をマインドマップにまとめて、@startmindmapで始まり@endmindmapで終わるPlantUMLで出力してください。')
    return render_template('mindmap.html', diagram = diagram)
  else:
    response = agent.run(prompt + 'をプレーンテキストでまとめて、出力してください。')
    return response
