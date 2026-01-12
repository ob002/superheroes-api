# routes.py
from flask import jsonify, request, abort
from app import db
from models import Hero, Power, HeroPower

def register_routes(app):

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
            "hero_powers": [hp.to_dict() for hp in hero.hero_powers]
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

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["Invalid request body"]}), 400

        required_fields = ['strength', 'hero_id', 'power_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"errors": [f"{field} is required"]}), 400

        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])

        if not hero:
            return jsonify({"errors": ["Hero not found"]}), 404
        if not power:
            return jsonify({"errors": ["Power not found"]}), 404

        try:
            hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )
            db.session.add(hero_power)
            db.session.commit()
            return jsonify(hero_power.to_dict()), 201
        except Exception as e:
            return jsonify({"errors": [str(e)]}), 400