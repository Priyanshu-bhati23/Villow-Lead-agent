from app.villow.adapter import VillowAdapter

def test_villow_adapter_execution(db_session):
    adapter = VillowAdapter()
    job_payload = {
        "job_id": "villow-job-101",
        "icp_description": "Find SaaS companies in India hiring engineers",
        "target_industry": "SaaS",
        "target_geography": "India",
        "max_leads": 3
    }

    res = adapter.process_job(job_payload, db=db_session)
    assert res.job_id == "villow-job-101"
    assert res.status == "completed"
    assert res.lead_count > 0
    assert len(res.results) > 0
