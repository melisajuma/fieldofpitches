from . import db
from werkzeug import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    '''
    @login_manager.user_loader Passes in a user_id to this function
    Function queries the database and gets a user's id as a response
    '''
    return User_pitch.query.get(int(user_id))



class User_pitch(UserMixin,db.Model):
    """ class modelling the users """

    __tablename__='user_pitch'

    #create the columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    password_hash = db.Column(db.String(255))
    pitch = db.relationship("Pitch", backref="user_pitch", lazy = "dynamic")
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")
    vote = db.relationship("Votes", backref="user", lazy = "dynamic")


   
    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'

#category model
class PitchCategory(db.Model):

    __tablename__ = 'pitchCategory'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    pitch = db.relationship("Pitch", backref="pitch", lazy = "dynamic")

    # save pitches
    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = PitchCategory.query.all()
        return categories


#pitches class
class Pitch(db.Model):
    """ List of pitches in each category """

    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)
    pitchcategory_id = db.Column(db.Integer, db.ForeignKey("pitchCategory.id"))
    user_pitch_id = db.Column(db.Integer,db.ForeignKey("user_pitch.id"))
    comment = db.relationship("Comments", backref="pitch", lazy = "dynamic")
    vote = db.relationship("Votes", backref="pitch", lazy = "dynamic")



    def save_pitch(self):
        ''' Save the pitches '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    # display pitches

    def get_pitches(id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches


# comments
class Comments(db.Model):
    '''User comment model for each pitch '''

    __tablename__ = 'comments'

    # add columns
    id = db.Column(db. Integer, primary_key=True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user_pitch.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))


    def save_comment(self):
        '''
        Save the Comments/comments per pitch
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            Comments.time_posted.desc()).filter_by(pitch_id=id).all()
        return comment

#votes
class Votes(db.Model):
    '''class to model votes '''
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user_pitch.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Vote.query.filter_by(user_id=user_id, pitches_id=pitches_id).all()
        return votes
        