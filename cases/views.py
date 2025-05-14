from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Case
from datetime import datetime
import json

@csrf_exempt
def create_case(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            case = Case.objects.create(
                case_name=data['case_name'],
                officer_name=data['officer_name'],
                department=data['department'],
                occurred_at=datetime.fromisoformat(data['occurred_at']),
                subject_name=data['subject_name'],
                location=data['location'],
                memo=data.get('memo', '')
            )
            return JsonResponse({'message': '등록 완료', 'id': case.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST만 허용'}, status=405)


def get_case_list(request):
    if request.method == 'GET':
        cases = Case.objects.all().order_by('-created_at')
        data = [
            {
                'id': case.id,
                'case_name': case.case_name,
                'officer_name': case.officer_name,
                'department': case.department,
                'occurred_at': case.occurred_at.isoformat(),
                'subject_name': case.subject_name,
                'location': case.location,
                'memo': case.memo,
            }
            for case in cases
        ]
        return JsonResponse(data, safe=False)
    
def get_case_detail(request, case_id):
    if request.method == 'GET':
        try:
            case = Case.objects.get(id=case_id)
            data = {
                'id': case.id,
                'case_name': case.case_name,
                'officer_name': case.officer_name,
                'department': case.department,
                'occurred_at': case.occurred_at.isoformat(),
                'subject_name': case.subject_name,
                'location': case.location,
                'memo': case.memo,
            }
            return JsonResponse(data)
        except Case.DoesNotExist:
            return JsonResponse({'error': '사건이 존재하지 않습니다'}, status=404)

