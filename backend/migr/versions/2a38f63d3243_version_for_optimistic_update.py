"""version for optimistic update

Revision ID: 2a38f63d3243
Revises: f4f89c94c677
Create Date: 2024-04-17 12:33:55.872418

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "2a38f63d3243"
down_revision: Union[str, None] = "f4f89c94c677"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
