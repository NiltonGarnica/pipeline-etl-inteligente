from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    precio: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"), nullable=False
    )

class AnalisisRegistro(Base):
    __tablename__ = "analisis_registros"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    texto_original: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    resultado: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )