# agents/tasks.py

class ScheduleMeetingTask:
    def __init__(self, proposed_time):
        self.proposed_time = proposed_time
    
    def execute(self, agent):
        return agent.propose_meeting(self.proposed_time)
