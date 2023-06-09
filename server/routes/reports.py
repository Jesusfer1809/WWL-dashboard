from flask import Blueprint, request, jsonify
from app import db
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from flask_cors import  cross_origin
from sqlalchemy import text

reports_routes = Blueprint('reports_routes', __name__)


class Incident_report(db.Model):

    __tablename__ = 'incident_reports'

    id = db.Column(db.String(length=50), primary_key=True)
    from_user = db.Column(db.Integer(), nullable=False)
    photo = db.Column(db.String(length=100), default="incident-default" )
    title= db.Column(db.String(length=50), nullable=False)
    paddock= db.Column(db.String(length=20), nullable=False)
    date= db.Column(db.String(length=20), nullable=False)

    latitude = db.Column(db.Numeric(), nullable=False)
    longitude= db.Column(db.Numeric(), nullable=False)
    elevation= db.Column(db.Numeric(), nullable=False)
    description= db.Column(db.String(length=150), nullable=False)

    supervisors= db.Column(db.ARRAY(db.String(length=40)))
    

    def __init__(self, id, from_user, photo, title, paddock, date, latitude, longitude, elevation, description, supervisors ):
        self.id = id
        self.from_user = from_user
        self.photo = photo
        self.title = title
        self.paddock=paddock
        self.date=date
        self.latitude=latitude
        self.longitude=longitude
        self.elevation=elevation
        self.description=description
        self.supervisors=supervisors
        

    def obj_to_dict(self):
        return {
            "id":self.id,
            "from_user":self.from_user,
            "photo":self.photo,
            "title":self.title,
            "paddock":self.paddock,
            "date":self.date,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "elevation":self.elevation,
            "description":self.description,
            "supervisors":self.supervisors,      
        }


class Piezometer_report(db.Model):

    __tablename__ = 'piezometer_reports'

    id = db.Column(db.String(length=50), primary_key=True)
    from_user = db.Column(db.Integer(), nullable=False)
    photo = db.Column(db.String(length=100), default="piezoreport-default" )
    title= db.Column(db.String(length=50), nullable=False)
    paddock= db.Column(db.String(length=20), nullable=False)
    piezo= db.Column(db.String(length=20), nullable=False)
    date= db.Column(db.String(length=20), nullable=False)
    description= db.Column(db.String(length=150), nullable=False)
    supervisors= db.Column(db.ARRAY(db.String(length=40)))

    def __init__(self, id, from_user,photo, title, paddock, piezo, date, description, supervisors ):
        self.id = id
        self.from_user = from_user
        self.photo = photo
        
        self.title = title
        self.paddock=paddock
        self.piezo = piezo
        self.date = date
        self.description=description
        self.supervisors=supervisors

    def obj_to_dict(self):
        return {
            "id":self.id,
            "from_user":self.from_user,
            "photo":self.photo,
            "title":self.title,
            "paddock":self.paddock,
            "piezo":self.piezo,
            "date":self.date,
            "description":self.description,
            "supervisors":self.supervisors,
        }
        


def upload_photo():
 
    if len(request.files.to_dict(flat=False)) == 0:
        return "incident-default"
    
    file = request.files['photo']
    
    filename = secure_filename(file.filename)

    final_filename = f'{uuid4()}-{filename}'

    file.save(os.path.abspath( "../client/public/media/incident_reports") + "\\" + final_filename)
    return final_filename

def upload_piezoreport_photo():

    if len(request.files.to_dict(flat=False)) == 0:
        return "piezoreport-default"
    
    file = request.files['photo']
    # print(file)
    # print("name",file.filename)

    filename = secure_filename(file.filename)

    final_filename = f'{uuid4()}-{filename}'

    # print(os.path.abspath( "../client/public/media/piezometer_reports") + "\\" + final_filename)


    file.save(os.path.abspath( "../client/public/media/piezometer_reports") + "\\" + final_filename)
    return final_filename

    


@reports_routes.route("/api/v1/incident-reports", methods=["GET"])
@cross_origin()
def get_incidents():
    
    userQuery = db.session.execute(text(f"SELECT ir.id as incident_id, ir.title as incident_title, ir.photo as incident_photo,  ir.paddock as incident_paddock, ir.date as incident_date, ir.latitude as incident_latitude, ir.longitude as incident_longitude, ir.elevation as incident_elevation, ir.description as incident_description, ir.supervisors as incident_supervisors, u.username as user_username , u.user_id, u.name as user_name, u.picture user_picture FROM incident_reports as ir LEFT JOIN users as u ON ir.from_user = u.user_id;"))
    
    incident_reports = [dict(r._mapping) for r in userQuery]


    return jsonify({
        "message":"success",
        "results": len(incident_reports),
        "incidents": incident_reports
    })

@reports_routes.route("/api/v1/piezometer-reports", methods=["GET"])
@cross_origin()
def get_piezo_reports():


    userQuery = db.session.execute(text(f"SELECT pr.id as report_id, pr.title as report_title, pr.photo as report_photo, pr.paddock as report_paddock, pr.piezo as report_piezo, pr.date as report_date, pr.description as report_description, pr.supervisors as report_supervisors,  u.username as user_username , u.user_id, u.name as user_name, u.picture user_picture FROM piezometer_reports as pr LEFT JOIN users as u ON pr.from_user = u.user_id;"))
    
    piezo_reports = [dict(r._mapping) for r in userQuery]


    return jsonify({
        "message":"success",
        "results": len(piezo_reports),
        "reports": piezo_reports
    })

@reports_routes.route('/api/v1/new-incident-report', methods=['POST'])
@cross_origin()
def new_incident_report():
    
    
    from_user = request.form["from_user"]
    
    title = request.form["title"]
    paddock= request.form["paddock"]
    date= request.form["date"]
    latitude= request.form["latitude"]
    longitude= request.form["longitude"]
    elevation= request.form["elevation"]
    description=request.form["description"]
    supervisors=request.form["supervisors"].split(",")


    photo_db = upload_photo()
    report_id = uuid4()

    new_report = Incident_report(report_id, from_user, photo_db, title, paddock, date, latitude, longitude, elevation, description, supervisors )

    db.session.add( new_report )
    db.session.commit()
    return jsonify({"status":"success"})


@reports_routes.route('/api/v1/new-piezometer-report', methods=['POST'])
@cross_origin()
def new_piezometer_report():
    
    from_user = request.form["from_user"]
    
    title = request.form["title"]
    
    paddock= request.form["paddock"]
    piezo= request.form["piezo"]
    date= request.form["date"]
    description=request.form["description"]
    
    supervisors=request.form["supervisors"].split(",")
    print("supervisors",supervisors)
    
    
    photo_db = upload_piezoreport_photo()
    
    report_id = uuid4()
    
    new_report = Piezometer_report(report_id, from_user, photo_db, title, paddock, piezo, date, description, supervisors)

    db.session.add( new_report )
    db.session.commit()
    return jsonify({"status":"success"})


@reports_routes.route('/api/v1/incident-reports/<id>', methods=['GET'])
@cross_origin()
def getOneIncident(id):
    
    userQuery = db.session.execute(text(f"SELECT ir.id as incident_id, ir.title as incident_title, ir.photo as incident_photo,  ir.paddock as incident_paddock, ir.date as incident_date, ir.latitude as incident_latitude, ir.longitude as incident_longitude, ir.elevation as incident_elevation, ir.description as incident_description, ir.supervisors as incident_supervisors, u.username as user_username , u.user_id, u.name as user_name, u.picture user_picture FROM incident_reports as ir LEFT JOIN users as u ON ir.from_user = u.user_id WHERE ir.id = '{id}';"))
    
    incident_reports = [dict(r._mapping) for r in userQuery]


    if(len(incident_reports) == 0):
        return jsonify({
            "message": "error"
        }), 404


    return jsonify({
        "message":"success",
        "report": incident_reports[0]
    })

@reports_routes.route('/api/v1/piezometer-reports/<id>', methods=['GET'])
@cross_origin()
def getOnePiezoReport(id):

    userQuery = db.session.execute(text(f"SELECT pr.id as report_id, pr.title as report_title, pr.photo as report_photo, pr.paddock as report_paddock, pr.piezo as report_piezo, pr.date as report_date, pr.description as report_description, pr.supervisors as report_supervisors,  u.username as user_username , u.user_id, u.name as user_name, u.picture user_picture FROM piezometer_reports as pr LEFT JOIN users as u ON pr.from_user = u.user_id WHERE pr.id = '{id}';"))
    
    piezo_reports = [dict(r._mapping) for r in userQuery]

    if(len(piezo_reports) == 0):
        return jsonify({
            "message": "error"
        }), 404


    return jsonify({
        "message":"success",
        "report": piezo_reports[0]
    })


@reports_routes.route('/api/v1/piezometer-reports/<id>', methods=['DELETE'])
@cross_origin()
def delete_piezo_report(id):
    print(f"DELETE FROM piezometer_reports as pr WHERE pr.id = '{id}';")

    db.session.execute(text(f"DELETE FROM piezometer_reports as pr WHERE pr.id = '{id}';"))
    db.session.commit()

    return jsonify({
        "message":"report deleted successfully",
    })
