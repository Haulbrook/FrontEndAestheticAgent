# Disney Trip Planning Agent

An AI-powered trip planning assistant to help you create the perfect Disney vacation! This intelligent agent helps with checklists, brainstorming ideas, countdown timers, and all your pre-trip planning needs.

## Features

### Core Capabilities

- **Comprehensive Checklists**: AI-generated, personalized checklists based on your trip details
  - Time-sensitive items (bookings, reservations)
  - Pre-trip preparations
  - Packing essentials
  - Easily forgotten items (chargers, medications, rain gear, etc.)
  - Disney-specific items (MagicBands, Genie+, etc.)

- **Intelligent Brainstorming**: Creative ideas and suggestions tailored to your party
  - Unique dining experiences
  - Hidden gems and lesser-known attractions
  - Photo opportunities
  - Budget-friendly magic moments
  - Special surprises for kids/families

- **Countdown Timer**: Real-time countdown to your magical adventure

- **AI Assistant**: Ask questions and get personalized recommendations

- **Trip Progress Tracking**: Visual progress tracking for your planning journey

### Highlights

- **Personalized**: Customized for your party size, ages, interests, and budget
- **Comprehensive**: Covers obvious needs AND easily forgotten items
- **Beautiful UI**: Modern, Disney-themed web interface
- **Smart**: Powered by OpenAI's GPT-4 for intelligent suggestions

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Haulbrook/Disney-Agent.git
   cd Disney-Agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

## Usage

### Running the Application

Start the Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Getting Started

1. **Enter Trip Details** (in the sidebar):
   - Select your Disney destination
   - Choose your trip dates
   - Enter party size and ages
   - Select interests and preferences
   - Specify budget range
   - Add any special considerations

2. **Create Your Trip Plan**:
   - Click "Create/Update Trip Plan"
   - The AI will generate a personalized checklist and ideas

3. **Use the Features**:
   - **Checklists Tab**: View and manage your trip planning tasks
     - Check off completed items
     - Filter by priority and category
     - Find forgotten items with AI assistance
     - Add custom checklist items

   - **Ideas & Suggestions Tab**: Explore creative ideas for your trip
     - Generate ideas focused on dining, activities, surprises, etc.
     - Save your favorite ideas

   - **AI Assistant Tab**: Chat with the AI for personalized advice
     - Ask questions about your trip
     - Get recommendations
     - Troubleshoot planning challenges

   - **Trip Summary Tab**: View your planning progress
     - See trip details at a glance
     - Track checklist completion
     - Monitor your planning progress

### Tips for Best Results

- **Be Specific**: The more details you provide about your party (ages, interests, special needs), the better the AI's suggestions
- **Update Regularly**: Regenerate checklists as your trip approaches for phase-appropriate items
- **Use the AI Assistant**: Don't hesitate to ask questions - the AI has extensive Disney knowledge
- **Check Forgotten Items**: Use the "Find Forgotten Items" button to ensure you haven't missed anything important

## Project Structure

```
Disney-Agent/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── trip_planner_agent.py  # Core AI agent logic
    ├── models/
    │   ├── __init__.py
    │   └── trip_data.py           # Data models (Pydantic)
    └── utils/
        ├── __init__.py
        └── helpers.py             # Helper functions (countdown, etc.)
```

## Key Components

### TripPlannerAgent

The core AI agent (`src/agents/trip_planner_agent.py`) handles:
- Generating comprehensive checklists
- Brainstorming creative ideas
- Providing personalized suggestions
- Analyzing checklists for forgotten items

### Data Models

Defined in `src/models/trip_data.py`:
- `TripDetails`: Trip information and preferences
- `ChecklistItem`: Individual checklist tasks
- `IdeaSuggestion`: Brainstormed ideas
- `TripPlan`: Complete trip plan

### Utilities

Helper functions in `src/utils/helpers.py`:
- Countdown timer calculations
- Trip phase determination
- ID generation

## Customization

### Changing the AI Model

Edit your `.env` file:
```
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo for lower cost
```

### Modifying the UI

The Streamlit interface can be customized in `app.py`:
- Edit the CSS in the `st.markdown()` section for styling
- Modify colors, fonts, and layouts
- Add new tabs or features

### Extending Agent Capabilities

Add new methods to `TripPlannerAgent` class for additional features:
- Custom prompt engineering
- New brainstorming categories
- Additional planning tools

## Troubleshooting

### "OpenAI API key not found"
- Ensure your `.env` file exists and contains a valid API key
- Check that the `.env` file is in the project root directory
- Verify the key name is exactly `OPENAI_API_KEY`

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8 or higher
- Try recreating your virtual environment

### API Rate Limits
- If using GPT-4, be aware of rate limits
- Consider using `gpt-3.5-turbo` for development/testing
- Add delay between API calls if needed

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is provided as-is for personal use. Please ensure your use of the OpenAI API complies with their terms of service.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by the magic of Disney

## Support

For questions or issues:
1. Check this README
2. Review the code comments
3. Open an issue on GitHub

---

**Have a magical trip planning experience!** ✨🏰✨
