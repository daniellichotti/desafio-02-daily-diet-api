from flask import Flask, jsonify, request
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

db.init_app(app)

@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    onDiet = data.get("onDiet")
    if onDiet:
        onDiet = True
    else:
        onDiet = False
    meal = Meal(name=name, description=description, onDiet=onDiet)
    db.session.add(meal)
    db.session.commit()
    
    return jsonify({'message': 'Refeição cadastrada com sucesso'})


@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    serialized_meals = []
    for meal in meals:
        serialized_meals.append({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'dateTime': meal.dateTime,
            'onDiet': meal.onDiet,
        })
    return jsonify({'meals': serialized_meals})

@app.route('/meals/<int:id_meal>', methods=['GET'])
def get_meal(id_meal):
    meal = Meal.query.get(id_meal)
    meal = {
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'dateTime': meal.dateTime,
                'onDiet': meal.onDiet,
            }

    if meal:
        return {"meal": meal}
    return jsonify({'message': 'Refeição não encontrada'}), 404

@app.route('/meals/<int:id_meal>', methods=['PUT'])
def update_meal(id_meal):
    data = request.json
    meal = Meal.query.get(id_meal)

    if meal:
        meal.name = data.get("name")
        meal.description = data.get("description")
        onDiet = data.get("onDiet")
        if onDiet:
            meal.onDiet = onDiet
        else:
            meal.onDiet = False
        db.session.commit()

        return jsonify({'message': f'Refeição {id_meal} atualizada com sucesso'})
    return jsonify({'message': 'Refeição não encontrada'}), 404 

@app.route('/meals/<int:id_meal>', methods=['DELETE'])
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'message': 'Refeição deletada com sucesso'})
    
    return jsonify({'message': 'Refeição não encontrada'}), 404



if __name__ == '__main__':
  app.run(debug=True)