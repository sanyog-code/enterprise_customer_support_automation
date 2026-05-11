import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.rag_tool import TicketRAGTool
 
load_dotenv()
# Using your paid-tier Gemini
llm_string = "gemini/gemini-2.5-flash"
 
@CrewBase
class SupportBotCrew():
    """Support Pipeline for Enterprise Data"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
 
    @agent
    def query_understanding_agent(self) -> Agent: return Agent(config=self.agents_config['query_understanding_agent'], llm=llm_string)
    @agent
    def sentiment_analysis_agent(self) -> Agent: return Agent(config=self.agents_config['sentiment_analysis_agent'], llm=llm_string)
    @agent
    def rag_retrieval_agent(self) -> Agent: return Agent(config=self.agents_config['rag_retrieval_agent'], tools=[TicketRAGTool()], llm=llm_string)
    @agent
    def escalation_resolution_agent(self) -> Agent: return Agent(config=self.agents_config['escalation_resolution_agent'], llm=llm_string)
    @agent
    def quality_assurance_agent(self) -> Agent: return Agent(config=self.agents_config['quality_assurance_agent'], llm=llm_string)
 
    @task
    def analyze_query_task(self) -> Task: return Task(config=self.tasks_config['analyze_query_task'])
    @task
    def analyze_sentiment_task(self) -> Task: return Task(config=self.tasks_config['analyze_sentiment_task'])
    @task
    def retrieve_solution_task(self) -> Task: return Task(config=self.tasks_config['retrieve_solution_task'])
    @task
    def draft_response_task(self) -> Task: return Task(config=self.tasks_config['draft_response_task'])
    @task
    def quality_review_task(self) -> Task: return Task(config=self.tasks_config['quality_review_task'])
 
    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)
 