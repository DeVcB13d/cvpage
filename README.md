# RESUME PROCESSOR

## Installation

### Install dependencies

```
pip install -r requirements.txt
```


### Installing spacy and nltk weights

```
python -m spacy download en_core_web_sm

python -m nltk.downloader stopwords

```

### Wkhtmltopdf

```
sudo apt-get -y install wkhtmltopdf

```

### Set openai key
Create a file ```.env``` and set the key variable
```OPENAI_API_KEY = sk-```

Refer to link [https://platform.openai.com/docs/quickstart?context=python] for API KEY instructions

### Run the program

```
streamlit run app.py
```


 
