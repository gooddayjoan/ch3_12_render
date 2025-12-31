from time import timezone
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from myapp.models import students
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def test(request):   
    return HttpResponse("Hello!!")

def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET['cName']
        # print(cName)
        # resultObj = students.objects.filter(cName=cName)
        resultObj = students.objects.filter(cName__contains=cName)
    else:
        resultObj= students.objects.all().order_by("-cID")
    # for d in resultObj:
    #     print(model_to_dict(d))

    # return  HttpResponse("Avo!")
    errormessage=""
    if not resultObj:
        errormessage="無此資料"
    return render(request, "search_list.html",locals())

def search_name(request):
    # return HttpResponse("Hello World")
    return render(request, "search_name.html")


def index(request):
    if 'search_for' in request.GET:
        search_for = request.GET['search_for'].strip()
        print(f"search_for={search_for}")
        if not search_for: # 排除空字串時錯誤
            return redirect("/index/")
        searchlist=search_for.split()
        print(f"searchlist={searchlist}")
        
        q_objs = Q()
        
        # for keywords in searchlist:
        #     q_objs.add(Q(cName__contains=keywords), Q.OR)
        #     q_objs |= Q(cBirthday__contains=keywords)
        #     q_objs |= Q(cEmail__contains=keywords)
        #     q_objs |= Q(cPhone__contains=keywords)
        #     q_objs |= Q(cAddr__contains=keywords)
        fields = ['cName','cBirthday','cEmail','cPhone','cAddr']
        for keywords in searchlist:
            for field in fields:
                # kwargs = {f"{field}__contains": keywords}
                # q_objs |= Q(**kwargs)
                q_objs |= Q(**{f"{field}__contains": keywords})

        resultlist =students.objects.filter(q_objs).order_by("cID")
    else:
        resultlist =students.objects.all().order_by("cID")
    data_count = len(resultlist)
    # print(data_count)
    paginator = Paginator(resultlist, 3) # 每頁顯示3筆資料
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html",locals())

def post(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName}, cSex={cSex}, cBirthday={cBirthday}, cEmail={cEmail}, cPhone={cPhone}, cAddr={cAddr}")
        # return HttpResponse("資料已新增")
        add = students(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail, cPhone=cPhone, cAddr=cAddr)
        add.save()
        return redirect("/index/")
    else:
        return render(request, "post.html", locals())
    
def edit(request,id):
    obj_data =students.objects.get(cID=id)
    print(model_to_dict(obj_data))
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName}, cSex={cSex}, cBirthday={cBirthday}, cEmail={cEmail}, cPhone={cPhone}, cAddr={cAddr}")
        # return HttpResponse("資料已修改")
        obj_data.cName = cName
        obj_data.cSex = cSex
        obj_data.cBirthday = cBirthday
        obj_data.cEmail = cEmail
        obj_data.cPhone = cPhone
        obj_data.cAddr = cAddr
        obj_data.save()
        # add.save()
        return redirect("/index/")
    else:
        return render(request, "edit.html", locals())
    
def delete(request,id):
    obj_data =students.objects.get(cID=id)
    if request.method == "POST":
        obj_data.delete()
        return redirect("/index/")
    else:
        return render(request, "delete.html", locals())   

# --------------------Json------------------------

def getAllItems(request):
    resultObj = students.objects.all().order_by("-cID")
    for r in resultObj:
        # print(type(r))
        print(model_to_dict(r))
    resultList = list(resultObj.values())
    return JsonResponse(resultList, safe=False)

    # return HttpResponse("Hi!")

def getItem(request, id):
    try:
        obj = students.objects.get(cID=id)
        resultDict= model_to_dict(obj)
        return JsonResponse(resultDict)
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=404)

# def createItem(request):
#     try:
#         if request.method == "GET":
#             cName = request.GET["cName"]
#             cSex = request.GET["cSex"]
#             cBirthday = request.GET["cBirthday"]
#             cEmail = request.GET["cEmail"]
#             cPhone = request.GET["cPhone"]
#             cAddr = request.GET["cAddr"]
#             return JsonResponse({"message":"Item created succesfully"})
#         elif request.method == "POST":
#             cName = request.POST["cName"]
#             cSex = request.POST["cSex"]
#             cBirthday = request.POST["cBirthday"]
#             cEmail = request.POST["cEmail"]
#             cPhone = request.POST["cPhone"]
#             cAddr = request.POST["cAddr"]
#         add = students(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail, cPhone=cPhone, cAddr=cAddr)
#         add.save()
#         return JsonResponse({"message":"Item created succesfully"})           
#     except Exception as e:
#         return JsonResponse({"message":str(e)})
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt #關閉csfr的內建裝飾器
def createItem(request):
    try:
        if request.method == "GET":
            data = request.GET
        elif request.method == "POST":
            data = request.POST

        add = students(
            cName=data["cName"],
            cSex=data["cSex"],
            cBirthday=data["cBirthday"],
            cEmail=data["cEmail"],
            cPhone=data["cPhone"],
            cAddr=data["cAddr"],
        )
        add.save()

        return JsonResponse({"message": "Item created succesfully"})
    except Exception as e:
        return JsonResponse({"message": str(e)})

@csrf_exempt #關閉csfr的內建裝飾器
def updateItem(request, id):
    try:
        # 1. 找到要更新的那筆學生資料
        try:
            stu = students.objects.get(cID=id)
        except students.DoesNotExist:
            return JsonResponse({"message": "Student not found"})

        # 2. 取得傳來的資料（GET 或 POST 都處理）
        data = request.GET if request.method == "GET" else request.POST

        # 3. 有傳的欄位才更新
        if "cName" in data:
            stu.cName = data["cName"]
        if "cSex" in data:
            stu.cSex = data["cSex"]
        if "cBirthday" in data:
            stu.cBirthday = data["cBirthday"]
        if "cEmail" in data:
            stu.cEmail = data["cEmail"]
        if "cPhone" in data:
            stu.cPhone = data["cPhone"]
        if "cAddr" in data:
            stu.cAddr = data["cAddr"]

        # 4. 儲存
        stu.save()

        return JsonResponse({"message": "Item updated successfully"})

    except Exception as e:
        return JsonResponse({"message": str(e)})
    
@csrf_exempt #關閉csfr的內建裝飾器
def deleteItem(request,id):
    try:
        delete_data =students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"Item deleted successfully"})
    except Exception as e:
        return JsonResponse({"message": str(e)})