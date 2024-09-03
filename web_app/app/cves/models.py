from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class CveModel(Base):
    __tablename__ = 'cves'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    cve_id: Mapped[str] = mapped_column(nullable=False, unique=True)

    description: Mapped[str] = mapped_column(nullable=True, default='No description available')
    title: Mapped[str] = mapped_column(nullable=True, default='Unknown Title')
    problem_types: Mapped[str] = mapped_column(nullable=True, default='No problem types available')

    published_date: Mapped[datetime] = mapped_column(nullable=False)
    last_modified_date: Mapped[datetime] = mapped_column(nullable=False)

    def __str__(self):
        return f'<CveModel(cve_id={self.cve_id}, published_date={self.published_date})>'

    async def to_dict(self):
        return {
            'id': await self.awaitable_attrs.id,
            'cve_id': self.cve_id,
            'description': self.description,
            'title': self.title,
            'problem_types': self.problem_types,
            'published_date': self.published_date,
            'last_modified_date': self.last_modified_date,
        }
