from pydantic import BaseModel, Field
from typing import Literal

class IntentionSchema(BaseModel):
    intent: Literal['normal', 'irrelevant', 'order_id'] = Field(
        description="Intent of customer query"
    )
    order_id: int = Field(
        description="Extracted order ID. If none found return 0"
    )
