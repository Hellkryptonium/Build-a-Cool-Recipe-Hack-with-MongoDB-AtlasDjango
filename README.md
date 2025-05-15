# Smart Recipe Application with MongoDB Atlas

A Django-based recipe application that uses MongoDB Atlas for data storage, Voyage AI for generating embeddings of recipe ingredients, and Google Gemini for smart recipe suggestions.

## Features

- Store and manage recipes with MongoDB Atlas
- Generate vector embeddings for recipe ingredients using Voyage AI
- Get AI-powered recipe recommendations with Google Gemini
- Modern, responsive user interface

## Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Voyage AI API key
- Google Gemini API key
- Anthropic API key

## Setup Instructions

1. Clone the repository

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following environment variables:
   ```
   # MongoDB Atlas Connection
   MONGODB_URI=mongodb+srv://<your_username>:<your_password>@<your_cluster>.mongodb.net/<your_database>?retryWrites=true&w=majority

   # VoyageAI API Key
   VOYAGE_API_KEY=your_voyage_api_key

   # Google Gemini API Key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000 in your browser to use the application.

## MongoDB Atlas Setup

1. Create a free MongoDB Atlas account at https://www.mongodb.com/cloud/atlas/register
2. Create a new cluster
3. Create a database user with read/write permissions
4. Add your IP address to the IP Access List
5. Get your connection string and add it to the `.env` file

## API Keys Setup

1. Get a Voyage AI API key at https://voyageai.com
2. Get a Google Gemini API key at https://ai.google.dev/ (sign up for Google AI Studio)
3. Add both to your `.env` file

## Based on

This project is based on the tutorial at [MLH MongoDB Blog Post](https://mlh.link/ghwos525-mongodb-blogpost)
