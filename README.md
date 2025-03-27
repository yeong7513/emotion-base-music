# Emotion-Based Music Recommendation

This project provides emotion-based music recommendations by analyzing user input text (emotion) and extracting relevant keywords. Using emotion analysis and keyword extraction, it constructs a query to the YouTube API to recommend appropriate music based on the user’s emotional state.

## Features

- **Emotion Analysis**: Analyzes user input text to detect emotional sentiment using `distilroberta-base`.
- **Keyword Extraction**: Extracts keywords from the user input using **KeyBERT** and the **SentenceTransformer** (`sentence-transformers/all-MiniLM-L6-v2`).
- **Music Recommendation**: Constructs a query for the YouTube API based on the emotion analysis and extracted keywords, then recommends songs accordingly.

## Tech Stack

- **Backend**: FastAPI
- **Emotion Analysis**: Hugging Face Transformers (`distilroberta-base` for sentiment analysis)
- **Keyword Extraction**: KeyBERT with `sentence-transformers/all-MiniLM-L6-v2`
- **Music Recommendation**: YouTube API

## Project Workflow

1. **Emotion Detection**: The user provides input text (e.g., "I am feeling happy"). The system analyzes the sentiment using the `distilroberta-base` model to determine whether the user’s emotion is positive, negative, or neutral.
   
2. **Keyword Extraction**: The text is processed to extract relevant keywords using **KeyBERT** and the **SentenceTransformer** (`sentence-transformers/all-MiniLM-L6-v2`). This helps identify important topics or concepts that can improve music recommendation.

3. **YouTube API Query Construction**: The system combines the detected emotion and extracted keywords to form a query for the YouTube API. Based on the query, the system requests music recommendations that match the user’s emotional state.

4. **Music Recommendation**: The YouTube API returns a list of relevant music videos that align with the user’s emotional state and keywords.

## Installation

### Prerequisites

- Python 3.8+
- YouTube Data API (API Key required)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yeong7513/emotion-base-music.git
   ```

2. Navigate to the project directory:
   ```bash
   cd emotion-base-music
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Setting up YouTube API

To use the YouTube API, you'll need an API key from the [Google Developers Console](https://console.developers.google.com/). Once you have the key, set it in your environment or `.env` file.

## Running the Project

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Send a POST request to the `/emotion/music-recommendation/` endpoint with the user input text (emotion). The server will return a list of YouTube music recommendations based on the emotion and keywords.

## Example Request

**Endpoint**: `/emotion/music-recommendation/`  
**Method**: POST  
**Payload**:
```json
{
  "text": "I am feeling excited today!"
}
```

## Example Response
```json
{
  "recommended_songs": [
    {
      "title": "Happy - Pharrell Williams",
      "url": "https://www.youtube.com/watch?v=Y6Sxv-sUYtM"
    },
    {
      "title": "Don't Stop Me Now - Queen",
      "url": "https://www.youtube.com/watch?v=HgzGwKwLmgM"
    }
  ]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
