[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![smolagents](https://img.shields.io/badge/powered%20by-smolagents-ff69b4.svg)](https://github.com/smol-ai/agents)
[![Spoonacular API](https://img.shields.io/badge/data%20source-Spoonacular-important.svg)](https://spoonacular.com/food-api)

<h3 align="center">
  <div style="display:flex;flex-direction:row;">
    <img src="https://github.com/user-attachments/assets/0e470bf1-e43f-499b-ba80-8321a03ea4fe" alt="Hugging Face mascot as chef" width=150px >
    <p style="padding: '20px';">culinai -- your ai cookbook agent!</p>
  </div>
</h3>


## Features ✨

- 🧠 AI-powered recipe suggestions with what's in your fridge using LLMs and Spoonacular high quality data
- 🥗 Dietary preference filtering (vegetarian, vegan, gluten-free)
- 📊 Ingredient utilization metrics (used/missing ingredients)
- 🔍 OpenTelemetry integration for performance monitoring

## Installation ⚙️

1. **Clone the repository**
```bash
git clone https://github.com/merouanezouaid/culinai.git
cd culinai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Spoonacular API key**
```bash
export SPOONACULAR_API_KEY="your_api_key_here"
```

## Usage 🚀

### Basic Usage
```python
from recipe_agent import get_recipe

response = get_recipe(
    ingredients="chickpeas, lamb, couscous, dried apricots",
    diet="vegetarian"
)
print(response)
```

### Example Output
```
Recipe suggestion: Moroccan Lamb and Apricot Tagine 
(used 4 of your ingredients, missing 3 additional ingredient(s)).
```

### Advanced Usage with Agent
```python
from smolagents import CodeAgent, HfApiModel
from recipe_agent import get_recipe

agent = CodeAgent(tools=[get_recipe], model=HfApiModel())
response = agent.run(
    "I have tofu, tomatoes, and basil. Suggest a vegan Italian dish!"
)
print(response)
```

## Observability 📡

The agent includes OpenTelemetry instrumentation for performance monitoring:

1. Start the OpenTelemetry collector
```bash
docker run -p 4317:4317 otel/opentelemetry-collector
```

2. Run the agent with tracing
```bash
python recipe_agent.py
```

View traces at `http://localhost:6006`

## Deployment to Hugging Face Spaces 🌐

1. Install hub client
```bash
pip install huggingface_hub
```

2. Push your tool
```python
from recipe_agent import get_recipe

get_recipe.push_to_hub(
    repo_id="yourusername/get-recipe-tool",
    repo_type="space",
    space_sdk="gradio"
)
```

## Configuration ⚙️

| Environment Variable       | Description                  | Default |
|----------------------------|------------------------------|---------|
| `SPOONACULAR_API_KEY`      | Spoonacular API key          | None    |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OpenTelemetry collector URL | `http://localhost:6006/v1/traces` |

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
