from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from . import Base


class PlatformType(str, Enum):
    # Nintendo Systems
    NES = "NINTENDO_ENTERTAINMENT_SYSTEM"
    SNES = "SUPER_NINTENDO"
    N64 = "NINTENDO_64"
    GAMECUBE = "GAMECUBE"
    GAMEBOY = "GAME_BOY"
    GAMEBOY_COLOR = "GAME_BOY_COLOR"
    GAMEBOY_ADVANCE = "GAME_BOY_ADVANCE"
    DS = "NINTENDO_DS"

    # Sega Systems
    MASTER_SYSTEM = "SEGA_MASTER_SYSTEM"
    GENESIS = "SEGA_GENESIS"  # Mega Drive in Europe/Japan
    SEGA_CD = "SEGA_CD"
    SATURN = "SEGA_SATURN"
    DREAMCAST = "SEGA_DREAMCAST"
    GAME_GEAR = "SEGA_GAME_GEAR"

    # Sony Systems
    PS1 = "PLAYSTATION_1"
    PS2 = "PLAYSTATION_2"
    PSP = "PLAYSTATION_PORTABLE"

    # Microsoft Systems
    XBOX = "XBOX_ORIGINAL"

    # Atari Systems
    ATARI_2600 = "ATARI_2600"
    ATARI_5200 = "ATARI_5200"
    ATARI_7800 = "ATARI_7800"
    ATARI_JAGUAR = "ATARI_JAGUAR"

    # Other Classic Systems
    NEO_GEO = "NEO_GEO"
    NEO_GEO_POCKET = "NEO_GEO_POCKET"
    TURBOGRAFX_16 = "TURBOGRAFX_16"  # PC Engine in Japan
    COMMODORE_64 = "COMMODORE_64"
    MSX = "MSX"

    # Multi-platform
    MULTI = "MULTI_PLATFORM"
    OTHER = "OTHER_PLATFORM"


class RegionType(str, Enum):
    NTSC = "NTSC"  # North America, Japan
    PAL = "PAL"  # Europe, Australia
    NTSC_J = "NTSC-J"  # Japan
    NTSC_C = "NTSC-C"  # China
    NTSC_K = "NTSC-K"  # South Korea
    NTSC_US = "NTSC-US"  # United States
    PAL_B = "PAL-B"  # UK, Ireland, and others
    PAL_I = "PAL-I"  # Australia and others
    REGION_FREE = "REGION_FREE"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# Many-to-many relationship table for games and genres
game_genre = Table(
    "game_genre",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Float(precision=2), nullable=False)
    release_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    publisher_id: Mapped[int] = mapped_column(Integer, ForeignKey("publishers.id"))
    platform: Mapped[PlatformType] = mapped_column(
        SQLAlchemyEnum(PlatformType), nullable=False
    )
    stock: Mapped[int] = mapped_column(Integer, default=0)
    is_digital: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    region: Mapped[RegionType] = mapped_column(
        SQLAlchemyEnum(RegionType), nullable=True
    )  # NTSC, PAL, NTSC-J, etc.
    condition_rating: Mapped[Optional[int]] = mapped_column(
        Integer
    )  # 1-10 rating for physical items
    has_original_box: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_manual: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_rare: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    collector_value: Mapped[Optional[Decimal]] = mapped_column(
        Float(precision=2)
    )  # Estimated collector's value
    serial_number: Mapped[Optional[str]] = mapped_column(
        String(100)
    )  # For authenticity verification
    special_edition: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    publisher = relationship("Publisher", back_populates="games")
    genres = relationship("Genre", secondary=game_genre, back_populates="games")
    reviews = relationship("Review", back_populates="game")
    order_items = relationship("OrderItem", back_populates="game")
    web_events = relationship("WebEvents", back_populates="game")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)

    # Relationships
    games = relationship("Game", secondary=game_genre, back_populates="genres")


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    website: Mapped[Optional[str]] = mapped_column(String(255))
    founded_year: Mapped[Optional[int]] = mapped_column(Integer)

    # Relationships
    games = relationship("Game", back_populates="publisher")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # New relationships for e-commerce
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    web_events = relationship("WebEvents", back_populates="user")


class WebEvents(Base):
    __tablename__ = "web_events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    game_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("games.id"), nullable=True  # Added ForeignKey constraint
    )
    event_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        # Types: VIEW, ADD_TO_CART, REMOVE_FROM_CART, WISHLIST, PURCHASE, REVIEW
    )
    session_id: Mapped[str] = mapped_column(String, nullable=False)
    time_spent: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,  # Time spent in seconds on game page
    )
    referrer_page: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    platform: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Web, mobile, app
    search_query: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    filters_applied: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # JSON string of applied filters
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="web_events")
    game = relationship("Game", back_populates="web_events")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 stars
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    game = relationship("Game", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(
        SQLAlchemyEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    total_amount: Mapped[Decimal] = mapped_column(Float(precision=2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Float(precision=2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    game = relationship("Game", back_populates="order_items")


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"))
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Relationships
    cart = relationship("Cart", back_populates="items")
    game = relationship("Game")
