from config import db


class DslData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    expression = db.Column(db.String(80), unique = False, nullable = False)
    inputs = db.Column(db.String(80), unique = False, nullable = False)
    outputs = db.Column(db.String(80), unique = False, nullable = False)
    
    def convert_to_json(self):
        return {
            "id" : self.id,
            "expression": self.expression,
            "inputs" : self.inputs,
            "outputs" : self.outputs
            
        }