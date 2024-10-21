<!-- ABOUT THE PROJECT -->
## About The Project
A django app that allows you to perform Retrieval-Augmented Generation (RAG) on your documents.

**Project Link:** https://edven-fe.onrender.com
### Built With

- **Django**: Web framework for building the backend.
- **LangChain**: Framework for managing and interacting with language models.
- **OpenAI API**: For leveraging language models for text generation.
- **Chroma DB**: A vector store to handle embeddings for semantic search.
- **SQLite**: Lightweight database for storing application data.


<!-- GETTING STARTED -->
## Getting Started


### Running this project

To get this project up and running you should start by having Python installed on your computer.

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) terminal, run the following command in the base directory of this project
```
cd edventures_test-codebase
```

That will create a new folder `myenv` in your project directory
```
python -m venv env
```

Next activate it with this command on mac/linux

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py runserver
```

**Note** For inferencing to work you will need to create an '.env' file at the root directory and put your own OpenAI API keys 

```
OPENAI_API_KEY= 'your_api_key'
```




<!-- USAGE EXAMPLES -->
## Usage

### Setup
To upload your own documents for RAG, follow the instructions below :

Create a superuser
```
python manage.py createsuperuser
```

Run the server
```
python manage.py runserver
```

After creating a superuser, navigate to the admin site at http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

Add a new document object
- Set file_name to match the name of the file you are uploading (e.g., if the file is named abc.pdf, enter abc.pdf)
- Key in corresponding file type (csv or pdf)
- Upload file in file field
- Provide a descriptive title for the document for title.

**Note** Currently only support multiple csv documents and one pdf document


### Using the RAG
Now that the documents are uploaded, you are able to call a post request to perform rag on your documents at http://127.0.0.1:8000/api/query/

the json format must follow the example below:

```
{
  "query": "Give me the background to GEM in  gem report"
}
```
## Testing

To run tests:

```
python manage.py test api
```


