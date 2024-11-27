from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        for picture in data:
            return  jsonify(picture), 200
    return {"message": "Internal server error"}, 500
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture['id'] == id :
               return  jsonify(picture), 200
    return {"message": "data not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    query = request.json
    id = query['id']
    for picture in data:
        if id == picture['id']:
            return {"Message": f"picture with id {picture['id']} already present"},302
    data.append(query)        
    return {"message": "succes"}, 200
        
        
       
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    id = request.args.get('id')
    query = request.json
    for picture in data :
        if picture["id"] == id:
           picture.update(query)
        else : return {"message": "picture not found"},404    
            
   

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for picture in data:
            if picture['id'] == id:
                del picture
                return {"message":"message"},204
            else:    
                return {"message": "picture not found"},404

   
