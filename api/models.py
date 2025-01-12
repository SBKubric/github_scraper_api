from datetime import datetime

from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    owner: str
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str


class RepositoryActivity(BaseModel):
    name: str
    owner: str
    date: datetime
    commits: int
    authors: str
