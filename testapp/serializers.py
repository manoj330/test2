from rest_framework import  serializers
from.models import *

class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model=Skill
        fields='__all__'
    
class ProfileSerializer(serializers.ModelSerializer):
    skills=SkillSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['username','email','password','skills']
        
        