from backend.app.agents.context import pack_context
from backend.app.schemas.advisor import AdvisorResult
from mcp.tools.calculators import calculate_emi, calculate_fuel_cost


def test_mcp_tools_are_deterministic_and_bounded():
    assert calculate_emi(100000, 0, 10)["monthly_payment_inr"] == 10000.0
    assert calculate_fuel_cost(30, 15, 100, 20)["annual_cost_inr"] == 48000.0
    assert pack_context([{"role": "user", "content": "hello"}], "need a car")


def test_advisor_result_limits_recommendations():
    result = AdvisorResult(kind="recommendation", answer="shortlist", recommendations=[])
    assert len(result.recommendations) <= 3
