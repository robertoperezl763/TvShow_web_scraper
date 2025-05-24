import os
from dotenv import load_dotenv

load_dotenv()

TARGET_ROLES = {'Director', 'Executive Producer', 'Screenwriter'}


SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')