# LangChain Learning Project

A demonstration project showcasing how to build intelligent conversational systems using LangChain.

## Features

1. **Weather Query**
   - Query weather for specified cities
   - Support temperature unit conversion (Celsius/Fahrenheit)

2. **Calculator**
   - Basic arithmetic operations
   - Natural language understanding for calculations

3. **Order Management**
   - Query user's historical orders
   - Filter by time range

4. **Package Customization**
   - Custom package creation
   - Flexible feature combinations
   - Dynamic pricing

5. **QPS Monitoring**
   - Real-time QPS data simulation
   - View QPS trends for specified time windows
   - Considers time periodicity, random fluctuations, and burst traffic
   - Returns 10 data points with smoothed curves

## Quick Start

1. Clone the project
```bash
git clone https://github.com/eadydb/langchain-learning.git
cd langchain-learning
```

2. Install dependencies
```bash
conda create -n llm-demo python=3.10
conda activate llm-demo
pip install -r requirements.txt
```

3. Run the demo
```bash
python -m src.demo.main
```

## Usage Examples

1. Weather Query
```
What's the weather like in Beijing?
```

2. Calculator
```
Calculate 23 times 45
```

3. Order Query
```
Show me user 12345's orders from the last 3 months
```

4. Package Customization
```
Create a 3-month premium package with data analytics and expert consultation
```

5. QPS Monitoring
```
Calculate QPS for the last 5 minutes
```

## Project Structure

```
src/demo/
├── main.py              # Main program entry
├── core/
│   └── services.py      # Core service definitions
├── services/
│   ├── calculator_service.py  # Calculator service
│   ├── order_service.py       # Order service
│   ├── package_service.py     # Package service
│   └── qps_service.py         # QPS monitoring service
├── models/
│   └── qps.py                 # QPS data models
└── schemas/
    └── base.py               # Base data models
```

## Tech Stack

- Python 3.10+
- LangChain
- Numpy
- FastAPI (API support)
- Pydantic (Data validation)

## Development Roadmap

- [ ] Add more data visualization features
- [ ] Support more complex natural language understanding
- [ ] Optimize QPS monitoring performance and accuracy
- [ ] Add unit tests
- [ ] Support more language models

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License
