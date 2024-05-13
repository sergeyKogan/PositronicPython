import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class TaskDetails(BaseModel):
    task_description: str
    related_files_content: Optional[Dict[str, str]]

    def to_prompt(self) -> str:
        prompt = f"Task description: {self.task_description}\nRelated files:\n"
        prompt += json.dumps(self.related_files_content)
        return prompt


class UserRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: UserRole
    content: str

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role.value, "content": self.content}

    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> "Message":
        assert isinstance(obj.get("role"), str)
        assert isinstance(obj.get("content"), str)
        return Message(role=obj.get("role"), content=obj.get("content"))

    def __repr__(self) -> str:
        return f"Message(role={self.role}, content={self.content})"

    def __str__(self) -> str:
        return f"Message(role={self.role}, content={self.content})"

    def __init__(self, role: UserRole, content: str) -> None:
        self.role = role
        self.content = content

    @classmethod
    def system(cls, message):
        return Message(UserRole.SYSTEM, message)

    @classmethod
    def user(cls, message):
        return Message(UserRole.USER, message)

    @classmethod
    def assistant(cls, message):
        return Message(UserRole.ASSISTANT, message)
