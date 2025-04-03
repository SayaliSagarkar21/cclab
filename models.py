from datetime import datetime
import uuid
from firebase_config import db

class User:
    def __init__(self, id=None, email=None, password=None, name=None, google_id=None):
        self.id = id or str(uuid.uuid4())
        self.email = email
        self.password = password
        self.name = name
        self.google_id = google_id
        self.created_at = datetime.utcnow().isoformat()
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id
    
    @staticmethod
    def from_dict(data, id=None):
        user = User(
            id=id,
            email=data.get('email'),
            password=data.get('password'),
            name=data.get('name'),
            google_id=data.get('google_id')
        )
        if 'created_at' in data:
            user.created_at = data['created_at']
        return user
    
    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'google_id': self.google_id,
            'created_at': self.created_at
        }
    
    @staticmethod
    def get_by_email(email):
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1)
        results = query.stream()
        
        for user_doc in results:
            user_data = user_doc.to_dict()
            return User.from_dict(user_data, id=user_doc.id)
        
        return None
    
    @staticmethod
    def get_by_id(user_id):
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return User.from_dict(user_doc.to_dict(), id=user_doc.id)
        return None
    
    @staticmethod
    def get_by_google_id(google_id):
        users_ref = db.collection('users')
        query = users_ref.where('google_id', '==', google_id).limit(1)
        results = query.stream()
        
        for user_doc in results:
            user_data = user_doc.to_dict()
            return User.from_dict(user_data, id=user_doc.id)
        
        return None
    
    def save(self):
        db.collection('users').document(self.id).set(self.to_dict())
        return self


class WeatherSearch:
    def __init__(self, id=None, user_id=None, city=None, temperature=None, description=None):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.city = city
        self.temperature = temperature
        self.description = description
        self.search_date = datetime.utcnow().isoformat()
    
    @staticmethod
    def from_dict(data, id=None):
        search = WeatherSearch(
            id=id,
            user_id=data.get('user_id'),
            city=data.get('city'),
            temperature=data.get('temperature'),
            description=data.get('description')
        )
        if 'search_date' in data:
            search.search_date = data['search_date']
        return search
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'city': self.city,
            'temperature': self.temperature,
            'description': self.description,
            'search_date': self.search_date
        }
    
    def save(self):
        db.collection('weather_searches').document(self.id).set(self.to_dict())
        return self
    
    @staticmethod
    def get_recent_searches_by_user(user_id, limit=5):
        searches_ref = db.collection('weather_searches')
        query = searches_ref.where('user_id', '==', user_id).order_by('search_date', direction=firestore.Query.DESCENDING).limit(limit)
        searches = []
        
        for doc in query.stream():
            search_data = doc.to_dict()
            search = WeatherSearch.from_dict(search_data, id=doc.id)
            
            # Convert ISO format string back to datetime object for template rendering
            if isinstance(search.search_date, str):
                search.search_date = datetime.fromisoformat(search.search_date)
                
            searches.append(search)
            
        return searches