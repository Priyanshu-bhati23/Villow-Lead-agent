def test_lead_generation_api(client):
    payload = {
        "icp": "SaaS companies in India with 50-500 employees hiring engineers",
        "industry": "SaaS",
        "geography": "India",
        "number_of_leads": 3
    }
    response = client.post("/api/leads/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert len(data["leads"]) == 3
    
    first_lead = data["leads"][0]
    assert "company_name" in first_lead
    assert "score" in first_lead
    assert "score_breakdown" in first_lead
    assert "why_this_is_a_good_lead" in first_lead
    assert "why_now" in first_lead
    assert "outreach_hook" in first_lead

    # Test GET /api/requests/{request_id}
    req_res = client.get(f"/api/requests/{data['request_id']}")
    assert req_res.status_code == 200
    assert req_res.json()["request_id"] == data["request_id"]

    # Test GET /api/leads/{lead_id}
    lead_id = first_lead["id"]
    lead_res = client.get(f"/api/leads/{lead_id}")
    assert lead_res.status_code == 200
    assert lead_res.json()["id"] == lead_id
