from flask import jsonify, request
from app import db
from models import Hero, Power, HeroPower


def register_routes(app):

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Superheroes API", "endpoints": ["/heroes", "/powers", "/hero_powers"]})

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({"error": "Hero not found"}), 404

        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "id": hp.id,
                    "hero_id": hp.hero_id,
                    "power_id": hp.power_id,
                    "strength": hp.strength,
                    "power": {
                        "id": hp.power.id,
                        "name": hp.power.name,
                        "description": hp.power.description
                    }
                }
                for hp in hero.hero_powers
            ]
        })

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404
        return jsonify(power.to_dict())

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return jsonify({"error": "Power not found"}), 404

        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({"errors": ["description is required"]}), 400

        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": ["Validation failed"]}), 400

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["Invalid JSON"]}), 400

        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        if not all([strength, hero_id, power_id]):
            return jsonify({"errors": ["strength, hero_id, and power_id are required"]}), 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero:
            return jsonify({"errors": ["Hero not found"]}), 404
        if not power:
            return jsonify({"errors": ["Power not found"]}), 404

        if strength not in ['Strong', 'Weak', 'Average']:
            return jsonify({"errors": ["strength must be 'Strong', 'Weak', or 'Average'"]}), 400

        try:
            hero_power = HeroPower(
                strength=strength,
                hero_id=hero_id,
                power_id=power_id
            )
            db.session.add(hero_power)
            db.session.commit()

            return jsonify({
                "id": hero_power.id,
                "hero_id": hero_power.hero_id,
                "power_id": hero_power.power_id,
                "strength": hero_power.strength,
                "hero": hero.to_dict(),
                "power": power.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": ["Validation failed"]}), 400