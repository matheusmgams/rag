import os
from dotenv import load_dotenv

class EnvironmentLoader:
    @staticmethod
    def load_env_variables():
        load_dotenv()
        codes = os.environ.get('CODES')
        archives = os.environ.get('DOCUMENTS')
        websites = os.environ.get('WEBSITES').split(';')
        model = os.environ.get('MODEL')
        rules = '\n\n'.join(rule.strip() for rule in os.environ.get('RULES').split(';') if rule.strip())
        return archives, websites, codes, model, rules
