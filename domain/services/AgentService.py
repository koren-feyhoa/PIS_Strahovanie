from domain.repositories.agent_repo import AgentRepository


class AgentServise:
    def __init__(self,agent_repo:AgentRepository):
        self.repo=agent_repo
    def get_all_clients(self):
        clients=self.repo.get_all_clients()
        return clients