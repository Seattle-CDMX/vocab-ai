from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LexicalSense:
    sense_number: int
    definition: str
    examples: List[str]
    explained: bool = False


@dataclass
class TargetLexicalItem:
    phrase: str
    senses: List[LexicalSense]

    @property
    def total_senses(self) -> int:
        return len(self.senses)

    @property
    def explained_senses(self) -> int:
        return sum(1 for sense in self.senses if sense.explained)

    @property
    def remaining_senses(self) -> int:
        return self.total_senses - self.explained_senses

    def get_next_unexplained_sense(self) -> LexicalSense | None:
        for sense in self.senses:
            if not sense.explained:
                return sense
        return None

    def mark_sense_explained(self, sense_number: int) -> bool:
        for sense in self.senses:
            if sense.sense_number == sense_number:
                sense.explained = True
                return True
        return False


@dataclass
class MySessionInfo:
    user_name: str
    age: int
    target_lexical_item: Optional[TargetLexicalItem]


def create_target_lexical_item(
    phrase: str, sense_data: List[dict]
) -> TargetLexicalItem:
    senses = []
    for data in sense_data:
        sense = LexicalSense(
            sense_number=data["senseNumber"],
            definition=data["definition"],
            examples=data["examples"],
        )
        senses.append(sense)

    return TargetLexicalItem(phrase=phrase, senses=senses)
