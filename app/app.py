from flask import Flask, render_template, request
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route('/chain', methods=['post'])
def chain():
  llm = OpenAI(streaming=True, temperature=0)
  tools = load_tools(["google-search"], llm=llm)
  agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
  instruction = request.form.get('instruction')
  output_format = request.form.get('output_format')

  if output_format == 'mindmap':
    diagram = agent.run(instruction + 'について日本語でマインドマップにまとめて、@startmindmapではじまり@endmindmapで終わるPlantUMLで出力してください。')
    return render_template('mindmap.html', diagram = diagram)
  else:
    response = agent.run(prompt + 'について日本語でプレーンテキストでまとめて、出力してください。')
    return response
