from app.agents.icp_agent import ICPAgent

def test_icp_parsing_heuristic_fallback():
    agent = ICPAgent()
    prompt = "Find SaaS companies in India with 50-500 employees that recently raised funding and are hiring engineers."
    parsed = agent.parse(prompt)

    assert "SaaS" in parsed.industry
    assert parsed.geography == "India"
    assert "50-500" in parsed.employee_range
    assert len(parsed.required_signals) > 0
