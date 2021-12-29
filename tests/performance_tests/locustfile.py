from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    # ajout d'un temps entre deux visiteurs ?
    wait_time = between(0, 1)

    @task
    def home(self):
        response = self.client.get("/")

    @task(3)
    def display_list_clubs(self):
        response = self.client.get("/clubsList")

    @task()
    def login(self):
        response = self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task()
    def not_access_to_book_page(self):
        response = self.client.get(f'/book/Spring Festival/Simply Lift')

    @task()
    def access_to_book_page(self):
        response = self.client.get(f'/book/Fall Classic/Simply Lift')

    @task(5)
    def book_competition_places(self):
        self.client.post("/purchasePlaces", {'club': 'Simply Lift', 'competition': 'Fall Classic',
                                             'places': '2'})
