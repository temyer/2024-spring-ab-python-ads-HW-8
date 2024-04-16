import typing as tp
from pydantic import BaseModel, field_validator


class ScoreRequest(BaseModel):
    approach: tp.Literal["two-model"] | tp.Literal["solo-model"]
    classifier: tp.Literal["catboost"] | tp.Literal["random-forest"]
    train_size: float

    @field_validator("train_size")
    @classmethod
    def train_size_validator(cls, v: float) -> float:
        if not 0 < v <= 1:
            raise ValueError("train_size must be in interval (0, 1]")
        return v
