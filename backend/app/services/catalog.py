from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DISCLAIMER = "Prices and specifications are approximate and should be verified with an authorized dealer."


@dataclass
class Vehicle:
    id: str
    name: str
    manufacturer: str
    model_year: int | None
    fuel_type: str
    transmission: str
    body_type: str
    seating_capacity: int
    price_min_inr: float | None
    price_max_inr: float | None
    specifications: dict[str, Any] = field(default_factory=dict)
    features: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)
    advantages: list[str] = field(default_factory=list)
    considerations: list[str] = field(default_factory=list)
    source: str = "curated catalog"

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "body_type": self.body_type,
            "seating_capacity": self.seating_capacity,
            "price_min_inr": self.price_min_inr,
            "price_max_inr": self.price_max_inr,
        }

    def detail(self) -> dict[str, Any]:
        return {
            **self.summary(),
            "model_year": self.model_year,
            "specifications": self.specifications,
            "features": self.features,
            "use_cases": self.use_cases,
            "advantages": self.advantages,
            "considerations": self.considerations,
            "source": self.source,
            "disclaimer": DISCLAIMER,
        }


class CatalogService:
    def __init__(self, source_dir: str | Path):
        self.source_dir = Path(source_dir)
        self.vehicles: dict[str, Vehicle] = {}
        self.reload()

    def reload(self) -> None:
        self.vehicles = {}
        self.source_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(self.source_dir.glob("*.md")):
            vehicle = self._parse(path)
            self.vehicles[vehicle.id] = vehicle

    def _parse(self, path: Path) -> Vehicle:
        text = path.read_text(encoding="utf-8")
        metadata, body = self._frontmatter(text, path)
        sections = self._sections(body)
        required = ["id", "name", "manufacturer", "fuel_type", "transmission", "body_type", "seating_capacity"]
        missing = [key for key in required if key not in metadata]
        if missing:
            raise ValueError(f"{path}: missing required fields: {', '.join(missing)}")
        return Vehicle(
            id=str(metadata["id"]),
            name=str(metadata["name"]),
            manufacturer=str(metadata["manufacturer"]),
            model_year=self._number(metadata.get("model_year"), int),
            fuel_type=str(metadata["fuel_type"]).casefold(),
            transmission=str(metadata["transmission"]).casefold(),
            body_type=str(metadata["body_type"]).casefold(),
            seating_capacity=int(metadata["seating_capacity"]),
            price_min_inr=self._number(metadata.get("price_min_inr"), float),
            price_max_inr=self._number(metadata.get("price_max_inr"), float),
            specifications=self._key_values(sections.get("Specifications", "")),
            features=self._bullets(sections.get("Features", "")),
            use_cases=self._bullets(sections.get("Best for", "")),
            advantages=self._bullets(sections.get("Advantages", "")),
            considerations=self._bullets(sections.get("Considerations", "")),
            source=str(path),
        )

    @staticmethod
    def _frontmatter(text: str, path: Path) -> tuple[dict[str, Any], str]:
        if not text.startswith("---"):
            raise ValueError(f"{path}: front matter is required")
        parts = text.split("---", 2)
        if len(parts) != 3:
            raise ValueError(f"{path}: invalid front matter")
        metadata: dict[str, Any] = {}
        for line in parts[1].strip().splitlines():
            if not line.strip() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = CatalogService._value(value.strip())
        return metadata, parts[2]

    @staticmethod
    def _value(value: str) -> Any:
        if value.startswith("["):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return value
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if re.fullmatch(r"-?\d+(\.\d+)?", value):
            return float(value)
        return value.strip('"\'')

    @staticmethod
    def _sections(body: str) -> dict[str, str]:
        result: dict[str, str] = {}
        current = "Overview"
        lines: list[str] = []
        for line in body.splitlines():
            if line.startswith("## "):
                result[current] = "\n".join(lines).strip()
                current = line[3:].strip()
                lines = []
            else:
                lines.append(line)
        result[current] = "\n".join(lines).strip()
        return result

    @staticmethod
    def _bullets(text: str) -> list[str]:
        return [line[2:].strip() for line in text.splitlines() if line.strip().startswith("-")]

    @staticmethod
    def _key_values(text: str) -> dict[str, str]:
        values = {}
        for line in text.splitlines():
            if line.strip().startswith("-") and ":" in line:
                key, value = line[1:].split(":", 1)
                values[key.strip()] = value.strip()
        return values

    @staticmethod
    def _number(value: Any, converter):
        return None if value is None or value == "" else converter(value)

    def get(self, vehicle_id: str) -> Vehicle | None:
        return self.vehicles.get(vehicle_id)

    def list(self, filters: dict[str, Any] | None = None) -> list[Vehicle]:
        filters = {key: value for key, value in (filters or {}).items() if value not in (None, "")}
        values = list(self.vehicles.values())
        result = []
        for vehicle in values:
            if filters.get("fuel_type") and vehicle.fuel_type != str(filters["fuel_type"]).casefold():
                continue
            if filters.get("transmission") and vehicle.transmission != str(filters["transmission"]).casefold():
                continue
            if filters.get("body_type") and vehicle.body_type != str(filters["body_type"]).casefold():
                continue
            if filters.get("seating_capacity") and vehicle.seating_capacity < int(filters["seating_capacity"]):
                continue
            if filters.get("price_max_inr") and (vehicle.price_min_inr or 0) > float(filters["price_max_inr"]):
                continue
            if filters.get("price_min_inr") and (vehicle.price_max_inr or float("inf")) < float(filters["price_min_inr"]):
                continue
            query = str(filters.get("q", "")).casefold()
            if query and query not in f"{vehicle.name} {vehicle.manufacturer} {vehicle.body_type} {' '.join(vehicle.use_cases)}".casefold():
                continue
            result.append(vehicle)
        return result

    def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 3) -> list[Vehicle]:
        candidates = self.list(filters)
        words = set(re.findall(r"[a-z0-9]+", query.casefold()))
        ranked = sorted(
            candidates,
            key=lambda vehicle: len(words & set(re.findall(r"[a-z0-9]+", f"{vehicle.name} {vehicle.body_type} {' '.join(vehicle.use_cases)}".casefold()))),
            reverse=True,
        )
        return ranked[:limit]
