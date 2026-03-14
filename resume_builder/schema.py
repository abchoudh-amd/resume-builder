from typing import Optional
from pydantic import BaseModel


class Personal(BaseModel):
    name: str
    title: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None


class Experience(BaseModel):
    company: str
    role: str
    start: str
    end: str
    highlights: list[str] = []


class Education(BaseModel):
    institution: str
    degree: str
    year: str


class Skill(BaseModel):
    category: str
    items: list[str]


class Project(BaseModel):
    name: str
    description: str
    url: Optional[str] = None


class Resume(BaseModel):
    personal: Personal
    experience: list[Experience] = []
    education: list[Education] = []
    skills: list[Skill] = []
    projects: list[Project] = []
