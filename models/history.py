from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.news import News
from models.users import User


class History(Base):
    __tablename__ = "history"
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_user_viewed', 'user_id', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史记录ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    viewed_time: Mapped[datetime] = mapped_column("view_time", DateTime, default=datetime.now, nullable=False, comment="浏览时间")


    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, viewed_time={self.viewed_time})>"