from dotenv import load_dotenv
from textwrap import dedent
from crewai import Agent, Task, Crew
from crewai_tools import CodeInterpreterTool, FileReadTool
import os
import time
import random

run_id = f"{int(time.time())}_{random.randint(1000, 9999)}"
print(f"Starting new run with ID: {run_id}")


def main():

    load_dotenv()
    
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    google_api_model= "gemini-2.5-pro-preview-03-25"


# Data Engineering Agent
    senior_data_engineer_agent = Agent(
        role="Senior Data Engineer",
        goal="Design and implement efficient data pipelines",
        backstory=dedent("""
            You are an experienced data engineer with expertise in Google Cloud Platform,
            particularly in GCS and BigQuery. You excel at designing scalable data pipelines
            and implementing best practices for data transformation and schema design.
            You understand the importance of data quality and performance optimization.
        """),
        verbose=True,
        allow_delegation=False,
        llm_config={"api_key": google_api_key, "model": google_api_model} 
    )


    data_pipeline_task = Task(
        description=dedent(f"""Run ID: {run_id} - Extract & Load Data from GCS to BigQuery about {{requested_data}}:
            Your environment variables GCP_PROJECT_ID, BQ_DATASET_ID, GCS_BUCKET_PATH
            and GCP_KEY_FILE are already set and should be derived from the .env file.
            Use them for the exact values in the code.
            The data is stored in the {{requested_data}} folder in the GCS bucket.
            
            1. Use Python and SQL 
            2. Pull all credentials from .env files
            3. Use .env credentials to specify correct source and destination tables or projects
            4. Create external table to directly query data from GCS to load into BigQuery:
                - CRITICAL: The data in the JSONL files has a nested structure where the main fields are inside an '_airbyte_data' object. 
                - IMPORTANT: Extract ALL relevant columns from JSONL files. 
                - You MUST access ALL fields using '_airbyte_data.' in your SQL queries. 
            5. Creare final table by converting data from external table into final table in BigQuery for analytics:
                - pull in all the columns necessary for Senior Data Analyst to make further analysis
                - Normalize query values (lowercase, remove special characters, standardize formats)
            6. The output file should be ready to executed for data loading into BigQuery.
            
        """),
        expected_output=dedent("""
            Your deliverable is clean, structured code ready to be used for loading data into BigQuery for analysis.         
        """),
        tools=[CodeInterpreterTool(), FileReadTool()],
        output_file="data_pipeline_task.py",
        agent=senior_data_engineer_agent
    )


# Data Quality Assurance Agent
    data_quality_assurance_agent = Agent(
        role="Senior Software Engineer",
        goal="Get recognition for providing the "
        "best coding and data quality assurance in your team",
        backstory=(
            "You work as a Senior Software Engineer "
            "and are now working with your team"
            "to ensure that their code is correct, by making a review of the code"
            "your team mates have written."
            "You are running the code provided by the Senior Data Engineer."
            "You need to make sure that data is loaded into BigQuery"
        ),
        verbose=True,
        llm_config={"api_key": google_api_key, "model": google_api_model} 
    )

    data_quality_assurance_task = Task(
        description=(
            f"Run ID: {run_id} - Review the text with code provided by the Senior Data Engineer in data_pipeline_task.py. "
            "Ensure that the code is comprehensive, accurate, and adheres to the high-quality standards.\n"
            "All environment variables are already set and should be derived from the .env file."
            
            "SPECIFIC VALIDATION CHECKLIST:\n"
            "1. Check if ALL SQL queries use _airbyte_data prefix for field references\n"
            "2. Verify that all parts of the code have proper credentials from .env file.\n"
            "3. Verify authentication is using the key file correctly.\n"
            "4. Confirm the code includes validation that checks row counts.\n"
            "5. IMPORTANT: Execute the data_pipeline_task.py.\n"
            "6. Validate that data is loaded properly using credentials from .env file.\n"
            
            "Also check if imports are correct, credentials are properly loaded, "
            "and source/destination tables are correct.\n"
            
            "If you can't execute the script or if any table is empty after execution, "
            "ask the Senior Data Engineer to fix the code and explain why."
        ),
        expected_output=(
            "Code is reviewed, executed, and data is successfully loaded into BigQuery with "
            "verification that tables contain actual data."
        ),
        tools=[CodeInterpreterTool(), FileReadTool()],
        agent=data_quality_assurance_agent,
    )


# Data Analysis Agent
    senior_data_analyst_agent = Agent(
        role="Senior Data Analyst",
        goal="Extract actionable insights from search query data",
        backstory=dedent("""
            You are a senior data analyst with expertise in SEO analytics and search performance data.
            Your strength lies in identifying patterns and opportunities within large datasets.
            You excel at transforming raw data into strategic insights and visualizations that drive
            business decisions. You have a deep understanding of search engine behavior and user intent.
        """),
        verbose=True,
        allow_delegation=False,
        llm_config={"api_key": google_api_key, "model": google_api_model}
    )

    da_performance_analysis_task = Task(
        description=dedent(f"""Run ID: {run_id} - Analyze Query Performance from BigQuery data from final table provided by Data Engineer:
            
            1. Use Python and SQL
            2. Pull all credentials from .env files.
            3. Connect to BigQuery using credentials from the .env file.
            4. Use .env credentials to specify correct source and destination tables or projects.
            5. IMPORTANT: Create a view in the same dataset as final table with high-impression, low-CTR queries that represent potential optimization opportunities based on the data from final table from Data Engineer agent's task.
            6. Query the view and:
                - output a ranked list of the top 10 optimization candidates.
                - explain why these queries represent optimization opportunities.
            7. Provide recommendations for potential next steps.
        
        """),
        expected_output=dedent("""
            - BigQuery view with the analysis is created.
            - Explanation of why these queries represent optimization opportunities.
            - Recommendations for potential next steps.
        """),
        tools=[CodeInterpreterTool(), FileReadTool(file_path='./.env') ],
        output_file="task_query_performance_analysis.py",
        agent=senior_data_analyst_agent
    )


# Data Science Agent
    senior_data_scientist_agent = Agent(
        role="Senior Data Scientist",
        goal="Extract actionable insights from search query data using NLP clustering",
        backstory=dedent("""
            You are a senior data scientist specialized in NLP and text analytics with expertise in SEO.
            Your strength lies in using unsupervised learning techniques to identify natural groupings 
            in text data. You excel at transforming unstructured text into meaningful clusters that 
            reveal user intent patterns. You have a deep understanding of semantic similarity, 
            topic modeling, and dimensionality reduction techniques for text data.
        """),
        verbose=True,
        allow_delegation=False,
        llm_config={"api_key": google_api_key, "model": google_api_model}
    )


    ds_clustering_task = Task(
        description=dedent(f"""Run ID: {run_id} - Perform clustering analysis of search queries from 
                           final table in BigQuery provided by Data Engineer:
            
            1. Use Python, SQL, and NLP libraries.
            2. Pull all credentials from .env files.
            3. Connect to BigQuery using credentials from the .env file.
            4. Extract search queries from final table in BigQuery provided by Data Engineer.
            5. Perform the following NLP clustering analysis:
                5.1. Generate embeddings for each query (using techniques like TF-IDF, Word2Vec, or sentence transformers).
                5.2. Apply dimensionality reduction if needed (UMAP, t-SNE, or PCA).
                5.3. Perform clustering (K-means, DBSCAN, or hierarchical clustering).
                5.4. Label each cluster with representative topics.
                5.5 Output all topics found.
        """),
        expected_output=dedent("""
            - Topics found in the NLP clustering analysis
        """),
        tools=[CodeInterpreterTool(), FileReadTool()],
        output_file="task_data_scientist_clustering.py",
        agent=senior_data_scientist_agent
    )


    data_crew = Crew(
        agents=[senior_data_engineer_agent, data_quality_assurance_agent, senior_data_analyst_agent, senior_data_scientist_agent],
        tasks=[data_pipeline_task, data_quality_assurance_task, da_performance_analysis_task, ds_clustering_task],
        verbose=True,
        crew_name=f"DataCrew_{run_id}",
        memory=True
    )

    
    inputs = {
        "requested_data": "search_analytics_by_query",
        "run_id": run_id
    }
    
    print("Starting data engineering pipeline...")
    result = data_crew.kickoff(inputs=inputs)
    print("\n=== Pipeline Execution Complete ===\n")
    print(result)

if __name__ == "__main__":
    main() 
