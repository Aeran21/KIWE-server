from django.shortcuts import redirect, render
from .models import Choice, Question, KeywordRelated
from datetime import date 
import json

def q(request, question_id):
    question = Question.objects.get(id=question_id)
    choices = Choice.objects.filter(question_id=question_id)
    context = {
        'question': question,
        'choices': choices,
    }

    if request.method == 'POST':
        question_id=question_id+1
        if question_id==4:
            return redirect('/keyword')
        return redirect('/q/%s' %question_id)

    return render(request, 'q.html', context)
    

    
class Rank():
    def __init__(self, keyword_id, score):
        self.keyword_id = keyword_id
        self.score = score

    def __repr__(self):
        return repr((self.keyword_id, self.score))


def kiword(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        one = data['one']
        two = data['two']
        three = data['three']
        today = date.today()
        birth = request.user.birth
        birth = (today.year - birth.year + 1)//10
        keywords = KeywordRelated.objects.filter(question='10', choice=birth).values('keyword')
        
        recomm = []

        for i in keywords:
            score = 0
            if (KeywordRelated.objects.filter(keyword_id=i['keyword'], question='2', choice=two)).exists():
                score += 1
            if (KeywordRelated.objects.filter(keyword_id=i['keyword'], question='3', choice=three)).exists():
                score += 1
            temp = Rank(score, i['keyword'])
            recomm.append(temp)

        recomm = sorted(recomm, key=lambda rank : rank.score, reverse=False)
        context = {
            'recomm': recomm
        }
        print(recomm)
            


    return render(request, 'keyword.html', context)