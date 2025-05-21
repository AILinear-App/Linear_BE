from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Case, CCTV
from datetime import datetime
import json
import traceback 

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
            traceback.print_exc()
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
        
@csrf_exempt
def add_cctv(request, case_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("lat")
            lng = data.get("lng")
            address = data.get("address")

            case = Case.objects.get(id=case_id)

            CCTV.objects.create(
                case=case,
                lat=lat,
                lng=lng,
                address=address
            )
            return JsonResponse({"message": "CCTV 저장 완료"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_case_route(request, case_id):
    if request.method == "GET":
        try:
            case = Case.objects.get(id=case_id)
            cctvs = CCTV.objects.filter(case=case)

            route = []   # 선을 만들고 싶으면 여기 좌표 리스트 넣어줘도 됨
            markers = [
                {"lat": c.lat, "lng": c.lng, "address": c.address}
                for c in cctvs
            ]

            return JsonResponse({
                "route": route,
                "markers": markers
            })
        except Case.DoesNotExist:
            return JsonResponse({"error": "사건이 존재하지 않음"}, status=404)
