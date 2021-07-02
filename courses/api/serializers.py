from rest_framework import serializers
from ..models import Subject,Course,Module,Course,Content
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self,value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Content
        fields = ['order','item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Module
        fields = ['order','title','description','contents']
class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']

class CourseEnrollView(APIView):
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course,pk=pk)
        course.students.add(request.user)
        return Response({'enrolled':True})


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order','title','description']

class COurseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True,read_only=True)
    class Meta:
        model = Course
        fields = ['id','subject','title','slug','overview','created','owner','modules']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','subject','title','slug','overview','created','owner','modules']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','title','slug']

