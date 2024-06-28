from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Manuel123-@localhost/Makrosoft_Test_MVallejo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'  # Nombre de la tabla en PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    peso_acumulado = db.Column(db.Integer, default=0, nullable=False)

class Soportes(db.Model):
    __tablename__ = 'soportes'  # Nombre de la tabla en PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    prioridad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    trabajador_asignado = db.Column(db.Integer, db.ForeignKey('trabajador.id'), nullable=True)
    trabajador = db.relationship('Trabajador', back_populates='soporte')

Trabajador.soporte = db.relationship('Soportes', order_by=Soportes.id, back_populates='trabajador')

@app.route('/asignar_soporte', methods=['POST'])
def asignar_soporte():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    prioridad = data['prioridad']
    peso = data['peso']
    
    trabajadores = Trabajador.query.all()
    min_peso = min(trabajadores, key=lambda w: w.peso_acumulado).peso_acumulado
    eligible_trabajadores = [w for w in trabajadores if w.peso_acumulado == min_peso]
    trabajador_seleccionado = choice(eligible_trabajadores)
    
    nuevo_soporte = Soportes(nombre=nombre, descripcion=descripcion, prioridad=prioridad, peso=peso, trabajador=trabajador_seleccionado)
    trabajador_seleccionado.peso_acumulado += peso
    
    db.session.add(nuevo_soporte)
    db.session.commit()
    
    return jsonify({
        'id': nuevo_soporte.id,
        'trabajador_asignado': trabajador_seleccionado.nombre,
        'trabajador_peso_acumulado': trabajador_seleccionado.peso_acumulado
    })

@app.route('/trabajadores', methods=['GET'])
def get_trabajadores():
    trabajadores = Trabajador.query.all()
    result = []
    for trabajador in trabajadores:
        result.append({
            'nombre': trabajador.nombre,
            'peso_acumulado': trabajador.peso_acumulado
        })
    return jsonify(result)

@app.route('/reiniciar_valores', methods=['POST'])
def reiniciar_valores():
    try:
        # Reiniciar valores en la base de datos
        db.session.query(Trabajador).update({Trabajador.peso_acumulado: 0})
        db.session.query(Soportes).update({Soportes.trabajador_asignado: None})
        db.session.commit()
        return jsonify({'message': 'Valores reiniciados correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        reiniciar_valores()
    app.run()
