from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

# https://xzgairkkaauiqwqcuzrx.supabase.co
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6Z2FpcmtrYWF1aXF3cWN1enJ4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDQ0MTk5MywiZXhwIjoyMDY2MDE3OTkzfQ.UuWi7adIJ72v3DICU9E-uuS6SfLQ52zBmKMvWlpBNKg
#testbucket
class User(Base):
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    credits = Column(Integer, default=0)