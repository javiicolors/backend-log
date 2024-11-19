#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:59:38 2024

@author: javiicolors
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from supabase_ import Base

class Download(Base):
    __tablename__ = "downloads"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    downloaded_at = Column(DateTime, default=datetime.utcnow)

    # Relación con la tabla `users`
    user = relationship("User", back_populates="downloads")