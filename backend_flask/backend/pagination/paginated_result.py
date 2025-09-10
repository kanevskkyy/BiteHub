from math import ceil
from dataclasses import dataclass
from typing import List, Any, Optional


@dataclass
class PaginatedResult:
    items: List[Any]
    total: int
    page: int
    per_page: int

    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.per_page) if self.per_page > 0 else 0

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> Optional[int]:
        return self.page + 1 if self.has_next else None

    @property
    def prev_page(self) -> Optional[int]:
        return self.page - 1 if self.has_prev else None

    def to_dict(self):
        return {
            'items': self.items,
            'total': self.total,
            'page': self.page,
            'perPage': self.per_page,
            'totalPages': self.total_pages,
            'hasNext': self.has_next,
            'hasPrev': self.has_prev,
            'nextPage': self.next_page,
            'prevPage': self.prev_page
        }