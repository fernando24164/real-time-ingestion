from locust import HttpUser, task, between
from typing import List
import random

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
