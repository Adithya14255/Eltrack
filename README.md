# ElTrack - Elephant Tracking System

## Project Overview

ElTrack is a sophisticated web application designed to track elephants in real-time and prevent accidents with trains and other hazards. This system uses LoRa (Long Range) wireless technology to monitor elephant movements near railway tracks and electrical installations, providing timely alerts to prevent accidents.

![ElTrack Logo](static/logo.png)

## Features

### Core Functionality
* Real-time tracking of elephants via LoRa ID
* Distance calculation between elephants and potential hazards (like trains)
* Visual traffic light warning system (red, yellow, green) based on proximity
* Interactive map visualization with elephant and train markers
* Tracking history and data logging

### Technical Enhancements
* Modern, responsive UI with improved user experience
* Real-time map updates
* Better visualization of risk zones
* Historical tracking data display
* Flash message system for user feedback
* Improved error handling
* About page with project information

## Project Structure

```
eltrack/
├── app.py                  # Main Flask application
├── static/                 # Static assets
│   ├── logo.png            # ElTrack logo
│   ├── elephant.png        # Elephant marker icon
│   ├── train.png           # Train marker icon
│   ├── style.css           # Custom CSS
│   └── app.js              # JavaScript for dynamic updates
├── templates/              # HTML templates
│   ├── home.html           # Main interface
│   ├── about.html          # About page
│   └── map_view.html       # Map visualization
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/eltrack.git
   cd eltrack
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask phonenumbers folium opencage
   ```

4. Set up environment variables (optional):
   ```bash
   export OPENCAGE_API_KEY=your_api_key_here  # On Windows: set OPENCAGE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a LoRa ID to track an elephant and visualize its proximity to trains.

## Danger Zone System

ElTrack uses a three-tier warning system based on the distance between elephants and trains:

* **Red Zone** (< 2 km): Immediate action required - high risk of collision
* **Yellow Zone** (2-3.5 km): Caution - moderate risk, prepare for preventive measures
* **Green Zone** (> 3.5 km): Safe - low risk, continue monitoring

## API Endpoints

* **GET /** - Main interface for tracking
* **GET /map_view** - Interactive map view
* **GET /about** - Project information
* **GET /api/tracking_data/{lora_id}** - JSON API for tracking history

## Future Enhancements

* Mobile application integration
* SMS alerts for railway staff
* Machine learning for predictive movement patterns
* Integration with railway scheduling systems
* Extended coverage for multiple wildlife species

## Credits

Developed by: Adithya G  
Last Updated: April 2025

## License

MIT License