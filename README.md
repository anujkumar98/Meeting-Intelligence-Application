# Meeting Intelligence Application



[![PyPI](https://img.shields.io/pypi/pyversions/locust.svg)](https://pypi.org/project/locust/)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

# Overview 📝

The Meeting Intelligence Application is a powerful tool that streamlines audio transcription, query options, transcript summarization, and semantic search capabilities. By leveraging advanced technologies such as the Whisper API, GPT 3.5 APIs, and the Pinecone vector database, this application revolutionizes the way meetings are processed and analyzed.




# Key Features

1. Audio Transcription: The application utilizes the Whisper API and GPT 3.5 APIs to transcribe audio from meetings, ensuring accurate and efficient conversion of spoken words into text.
2. Custom Query Options: Users can easily search and retrieve specific information from the meeting transcripts by utilizing custom query options, enabling quick access to relevant content.   
3. Transcript Summarization: Long transcripts are summarized to provide concise and comprehensive insights, allowing users to grasp key points and important discussions more efficiently.
4. Semantic Search Capability: By leveraging the power of the Pinecone vector database, the application enables semantic search, delivering highly relevant and contextual search results.
5. Workflow Orchestration: The workflow of the application is orchestrated using Airflow on Google Cloud Composer, ensuring efficient task execution and seamless integration of various components.
6. User-Friendly Interface: The web application is deployed on Streamlit Cloud, providing a user-friendly interface that makes it easy to interact with the application's features and access meeting insights effortlessly.

# Project Architecture

Project Architecture Diagram and technologies used

![image](https://github.com/anujkumar98/Meeting-Intelligence-Application/blob/862f2576ca275489f71dbc94ba0f73adaaa7a1f3/Architecture%20Diagram/architecture_diagram.png)

# Process Outline

1. Creating 2 DAGs, first Adhoc (runs on single audio file), second Batch (runs on a batch of audio files)

2. Download audio file from GCP.

3. Transcribe audio to transcript using Whisper API

4. Pass the transcript along with related queries to Pinecone for storage. Search audio files based on keywords.

5. Query GPT 3.5 API for answers using transcript as context.

6. Store user activity logs(Queries) into DB.

