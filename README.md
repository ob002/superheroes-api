# superheroes-api

A RESTful Flask API for managing superheroes, their superpowers, and the strength of each hero-power association.

Built for the Flatiron School assessment with full CRUD operations, validations, and JSON responses matching the provided Postman collection.

---

# Features

- List all heroes
- View a hero with their associated powers
- List all superpowers
- View or update a superpower (with validation)
- Assign a power to a hero with a strength rating (`Strong`, `Weak`, `Average`)
- Proper error handling (`404`, `400`) with JSON error messages

---

 # Tech Stack

- Python 3.12
- Flask – Web framework
- Flask-SQLAlchemy – ORM for database interactions
- Flask-Migrate** – Database migrations (Alembic)
- SQLite – Lightweight database (for development)

---

 # Project Structure

superheroes-api/
├── app.py # Application factory & setup
├── config.py # Configuration settings
├── models.py # Hero, Power, HeroPower models
├── routes.py # All API endpoints
├── seed.py # Database seeding script
├── requirements.txt # Dependencies
├── migrations/ # Auto-generated migration files
└── superheroes.db # SQLite database (created on first run)

---

 # Setup & Installation

1. Clone the repository
   ```bash
   git clone https://github.com/ob002/superheroes-api
   cd superheroes-api

2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
Install dependencies

4. Initialize the database
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial tables"
flask db upgrade

5. Seed the database (recommended)
python seed.py
The API will be available at:http://127.0.0.1:5000

 API Endpoints
 Method
Endpoint
Description
GET
/heroes
Get all heroes
GET
/heroes/<id>
Get a hero by ID with their powers
GET
/powers
Get all powers
GET
/powers/<id>
Get a power by ID
PATCH
/powers/<id>
Update a power’s description
POST
/hero_powers
Create a new hero-power association

 Validations
Power.description: Must be present and at least 20 characters long
HeroPower.strength: Must be one of:
"Strong"
"Weak"
"Average"
Violations return a 400 Bad Request with: 
{ "errors": ["Description must be at least 20 characters long."] }
 Testing
Import the provided Postman collection (challenge-2-superheroes.postman_collection.json) to test all endpoints.

All tests should pass when the API is running locally on port 5000.

 Example Requests

GET /heroes
[
  { "id": 1, "name": "Kamala Khan", "super_name": "Ms. Marvel" },
  ...
]

{
  "strength": "Strong",
  "power_id": 1,
  "hero_id": 3
}

{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Strong",
  "hero": { "id": 3, "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
  "power": { "id": 1, "name": "super strength", "description": "..." }
} 

 Submission
Repository is private
Technical Mentor added as collaborator
Includes working requirements.txt, README.md, and seeded database support
