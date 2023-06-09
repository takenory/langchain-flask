from flask import Flask
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

app = Flask(__name__)

@app.route("/")
def index():
  llm = OpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0)
  tools = load_tools(["serpapi", "llm-math"], llm=llm)
  agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
  response = agent.run("FlaskというWebアプリケーションフレームワークが提供する機能をマインドマップにまとめて、PlantUMLのテキストデータとして生成してください。")

  return response
