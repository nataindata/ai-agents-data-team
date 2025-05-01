# 🦾 AI Agents Tutorial: Replacing an Entire Data Team
Can you imagine replacing an entire data team with a fleet of AI agents? 

I was curious if I could delegate the usual tasks of a Data Engineer, Data Analyst and Data Scientist as if they were working together on 1 business request. Could we replace data team? Are we THERE already?
For that, with the help of CrewAI we are going to test how this Data team of AI agents will perform

## What is the Agent and how they collaborate:
The core component here is the Agent and it has several key properties:

- Role - defines the specific function of the agent, like a real job title
- Focus - the primary area the agent is designed to do, and sticks to it.
- Tools - resources it can utilize to perform its tasks, like APIs, databases, or analytical tools.
- Cooperation - how the agent interacts and collaborates with other agents. Or not.
- Guardrail - Sets the boundaries and constraints 
- Memory - Allows the agent to retain information from past interactions. Wow.

I'm super impressed with what CrewAI is doing right now - they are beating Langgraph. So as a test, I've decided to try it out.

## What problem are we solving? 

I’ve tried to mimic a typical business request from the Marketing department: 
`How can we identify the most valuable search queries and optimize our SEO strategy to improve organic search traffic?`

## Preparation:
- Have access to Search Console Tool
- Get account in GCP (you can get one with $300 credit for Free)
- Connect email from GCP account service account into Search Console itself and enable API 
- Have Docker installed and running
- OpenAI or Google API key 
- Configure Airbyte open source tool to quickly pull data from Google Search Console API, follow the tutorial https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart
- -> As the source choose Google Search Console -> add your domain -> choose start date to pull data from -> create new GCP keys and add it here -> set up source -> It will test the connection
- -> As the destination, choose Google Cloud Storage -> add your HMAC keys from the Cloud storage Settings -> Interoperability -> then Create your bucket and bucket path 
- -> Set up Connections -> choose source and destination -> select stream search_analytics_by_query and change to manual -> Set up a conneciton and run
- -> In the end you will see beautiful raw data in JSONL format landing into your Data lake.
