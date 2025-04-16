# Cosci Guide Agent
```bash
.
├── .env
├── README.md
├── requirements.txt
├── vectordb
└── src
    ├── Data
    │   ├── info  # store activity & simulation info
    │   │   └── simulation_features_info.csv
    │   └── link  # store various links
    │       ├── activity_links.csv
    │       ├── all_links.csv
    │       ├── base_links.csv
    │       ├── base_links_name.csv
    │       ├── simulation_feature_links.csv
    │       ├── simulation_links.csv
    │       └── userinfo_links.csv
    ├── RAG
    │   ├── build_vectordb.py
    │   └── retrieve.py
    └── web_crawl
        ├── generate_web_info.py  # generate web info by gpt4o-mini
        ├── get_activity_link.py   # web crawl activity link
        ├── get_all_link.py        # web crawl all link in Cosci
        ├── get_base_link.py       # get base link (e.g., home, password...)
        ├── get_link.py            # general function to get links
        ├── get_simulation_info.py  # get simulation title and description
        ├── get_simulation_link.py  # retrieve specific simulation links
        ├── name_link.py           # handle naming conventions for links
        ├── read_write.py           # functions for input/output operations
        └── sep_link.py             # clear all_links.csv
```

## Environment Setup
- To run the project, follow these steps to create a virtual environment:
```
conda create --name cosci python=3.9
conda activate cosci
pip install -r requirements.txt
```

- Configure `.env` File
- Create a .env file in the project root directory and add your API key:
```
API_KEY = YOUR KEY
```

## Web crawl
- Use seleium to web crawl CosciUse Selenium to crawl links in Cosci. 
- Run the following commands:

```
python src/Web_crawl/get_all_link.py # get all link in cosci
python src/Web_crawl/sep_link.py # clear up all link to activity, simulation,...
python src/Web_crawl/get_base_link.py # get main link
python src/Web_crawl/generate_web_info.py # use gpt to generate main link info
python src/Web_crawl/get_simulation_link.py # get simulation link
python src/Web_crawl/get_simulation_info.py # use simulation link to get info
```

## RAG Module
- Use the RAG module to build the vector database and retrieve information:

```
python -m src.RAG.build_vectordb -> build vector db
python src/RAG/retrieve.py -> retrieve relative info
```