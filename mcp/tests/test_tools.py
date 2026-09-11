from mcp.tools.calculators import calculate_emi, calculate_fuel_cost


def test_mcp_calculators_use_canonical_backend_math():
    assert calculate_emi(100000, 0, 10)["monthly_payment_inr"] == 10000.0
    result = calculate_fuel_cost(30, 15, 100, 20)
    assert result["monthly_cost_inr"] == 4000.0
    assert result["annual_cost_inr"] == 48000.0
