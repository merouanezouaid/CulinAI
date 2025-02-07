import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from tool import SimpleTool

tool = SimpleTool()

tool.push_to_hub("CallmeKaito/get-recipe-tool")