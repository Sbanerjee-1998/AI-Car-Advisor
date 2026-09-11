from mcp.server.fastmcp import FastMCP

from mcp.tools.calculators import calculate_emi, calculate_fuel_cost

mcp = FastMCP("ai-car-advisor")


@mcp.tool()
def emi(principal_inr: float, annual_interest_rate_percent: float, term_months: int) -> dict[str, float | str]:
    """Estimate monthly payment, total payment, and interest for a vehicle loan."""
    return calculate_emi(principal_inr, annual_interest_rate_percent, term_months)


@mcp.tool()
def fuel_cost(daily_distance_km: float, mileage_km_per_litre: float, fuel_price_inr_per_litre: float, monthly_driving_days: int) -> dict[str, float | str]:
    """Estimate daily, monthly, and annual fuel cost for a vehicle."""
    return calculate_fuel_cost(daily_distance_km, mileage_km_per_litre, fuel_price_inr_per_litre, monthly_driving_days)


if __name__ == "__main__":
    mcp.run(transport="stdio")
