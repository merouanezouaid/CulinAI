from smolagents import launch_gradio_demo
from typing import Optional
from tool import SimpleTool

tool = SimpleTool()

launch_gradio_demo(tool)
