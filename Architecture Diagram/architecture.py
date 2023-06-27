#Architecture diagram


from diagrams import Diagram
from diagrams import Cluster, Edge, Node
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.gcp.analytics import Composer
from diagrams.onprem.client import Client
from diagrams.gcp.database import SQL
from diagrams.azure.web import AppServiceDomains
from diagrams.azure.web import APIConnections
from diagrams.gcp.storage import Storage
from diagrams.programming.framework import Fastapi
from diagrams.gcp.compute import AppEngine
from diagrams.programming.language import Bash
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker


with Diagram("Architecture Diagram", show=False):
    ingress = Users("Users")
    with Cluster("Application"):
      with Cluster("Airflow"):
        airflow = Airflow("Airflow")
      with Cluster("Streamlit cloud"):
          streamlit = AppServiceDomains("Streamlit Cloud ")
      with Cluster("Docker"):
        docker = Docker("Docker Container")
        with Cluster("FastAPI"):
            fastapi= Fastapi("Fastapi")
      with Cluster("Google SQL"):
          db = SQL("SQL")
      with Cluster("OpenAI Services"):
          openai=APIConnections("OpenAI API")
      with Cluster("Cloud Storage"):
          storage = Storage("GCS")
      with Diagram("Pinecone"):
          pineconedb=Bash("Pinecone DB")


    streamlit << Edge(label="Website") << ingress
    fastapi << Edge(label="Data Fetch") << db
    db << Edge(label="Data Fetch") << fastapi
    fastapi << Edge(label="Data Upload") << storage
    storage << Edge(label="Data Fetch") << fastapi
    streamlit << Edge(label="API Calls Response") << fastapi
    fastapi << Edge(label="API Calls to backend") << streamlit
    fastapi << Edge(label="API Call to ChatGPT") << openai
    openai << Edge(label="API Calls Response") << fastapi
    pineconedb << Edge(label="Embeddings") << openai
    airflow << Edge(label="ETL Pipelines ") << storage
    airflow << Edge(label="ETL Pipelines") << pineconedb