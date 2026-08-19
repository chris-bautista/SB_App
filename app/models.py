"""
Modelos de datos: una Nota de servicio con sus Conceptos (líneas de
producto/mano de obra). Sin Cliente/Vehiculo aparte a propósito: sus datos
viven directamente en la Nota, no hay necesidad de normalizarlos en este
alcance.

Los nombres de campo de Concepto (tipo, descripcion, posicion, lado,
cantidad, importe) replican a propósito el shape de
contenido.NOTA_EJEMPLO["conceptos"], para consistencia con el resto del
proyecto.
"""

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Nota(Base):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(primary_key=True)
    creado_en: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    cliente_nombre: Mapped[str] = mapped_column(String(120))
    cliente_telefono: Mapped[str | None] = mapped_column(String(20), default=None)

    vehiculo_marca: Mapped[str] = mapped_column(String(60))
    vehiculo_modelo: Mapped[str] = mapped_column(String(60))
    vehiculo_anio: Mapped[int | None] = mapped_column(Integer, default=None)
    vehiculo_placas: Mapped[str | None] = mapped_column(String(20), default=None)

    trabajo: Mapped[str] = mapped_column(String(200))
    aviso: Mapped[str | None] = mapped_column(Text, default=None)

    conceptos: Mapped[list["Concepto"]] = relationship(
        back_populates="nota",
        cascade="all, delete-orphan",
        order_by="Concepto.id",
    )

    @property
    def total(self) -> float:
        """
        Se calcula siempre a partir de los conceptos, nunca se guarda: así
        no hay riesgo de que un total quede desincronizado si algún día se
        agrega edición de notas.
        """
        return sum(c.cantidad * c.importe for c in self.conceptos)


class Concepto(Base):
    __tablename__ = "conceptos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nota_id: Mapped[int] = mapped_column(ForeignKey("notas.id"))

    tipo: Mapped[str] = mapped_column(String(30))          # "Producto" | "Servicio"
    descripcion: Mapped[str] = mapped_column(String(200))
    posicion: Mapped[str | None] = mapped_column(String(30), default=None)
    lado: Mapped[str | None] = mapped_column(String(30), default=None)
    cantidad: Mapped[int] = mapped_column(Integer, default=1)
    importe: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=False))

    nota: Mapped["Nota"] = relationship(back_populates="conceptos")
