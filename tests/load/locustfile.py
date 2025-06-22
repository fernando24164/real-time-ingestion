from locust import HttpUser, task, between
from typing import List
import random
import uuid
import time

class CustomerInsightsUser(HttpUser):
    # Wait between 1 and 3 seconds between tasks
    wait_time = between(1, 3)
    
    # List of test user IDs from seed data
    TEST_USER_IDS: List[int] = [1, 2, 3]  # retrogamer, collector, casual_player

    @task(1)
    def get_customer_insights(self):
        """Load test the customer insights endpoint"""
        user_id = random.choice(self.TEST_USER_IDS)
        with self.client.get(
            f"/api/v1/customer/insights?user_id={user_id}",
            name="/api/v1/customer/insights",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                # Verify the response contains expected fields
                data = response.json()
                if all(key in data for key in ["preferences", "recent_interests", "platform_usage", "engagement_score"]):
                    response.success()
                else:
                    response.failure("Response missing required fields")
            else:
                response.failure(f"Request failed with status code: {response.status_code}")


class SessionInsightsUser(HttpUser):
    wait_time = between(1, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_ids = {}
        
    def on_start(self):
        """Create session IDs for each test user"""
        for user_id in [1, 2, 3]:
            self.session_ids[user_id] = f"loadtest-{uuid.uuid4()}"
    
    @task(3)
    def ingest_session_data(self):
        """Load test the ingestion endpoint with session data"""
        user_id = random.choice([1, 2, 3])
        session_id = self.session_ids[user_id]
        game_id = random.choice([1, 2, 3, 4, 5])
        event_type = random.choice(["VIEW", "CLICK", "ADD_TO_CART", "WISHLIST"])
        
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "event_type": event_type,
            "game_id": game_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "referrer_page": f"/games/{game_id}",
            "time_spent": random.randint(10, 300)
        }
        
        with self.client.post(
            "/api/v1/ingest",
            json=data,
            name="/api/v1/ingest",
            catch_response=True
        ) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f"Ingestion failed with status code: {response.status_code}")
    
    @task(1)
    def get_session_insights(self):
        """Load test the session insights endpoint"""
        user_id = random.choice([1, 2, 3])
        session_id = self.session_ids[user_id]
        
        with self.client.get(
            f"/api/v1/analytics/sessions/{session_id}/insights",
            name="/api/v1/analytics/sessions/insights",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if all(key in data for key in ["session_id", "user_id", "page_views", "unique_games_viewed", "event_breakdown"]):
                    response.success()
                else:
                    response.failure("Response missing required fields")
            elif response.status_code == 404 and "not found" in response.text:
                # This might happen if we try to get insights before any data is ingested
                # We'll mark it as a success for the load test
                response.success()
            else:
                response.failure(f"Request failed with status code: {response.status_code}")
