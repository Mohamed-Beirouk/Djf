import json , os
from Djf.settings import PublicKEYAES
from myappdjf.cryptoFunctions import  *
from . models import *
from Djf.settings import SECRET_KEY
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import date
from itertools import islice
from selenium import webdriver
import time, jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.db.models.functions import Random



class Mytoken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            uuu = request.data['username']
            ppp = request.data['password']
        except:
            return Response(
            {
                'status': False,
                'message': 'You must provide either username and password',
                'data': null
            },
            status.HTTP_400_BAD_REQUEST
            )
        null=None
        u=authenticate(username=uuu,password=ppp)
        if u is None:
            return Response(
            {
                'status': False,
                'message': 'no human for this information',
                'data': null
            },
            status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(u)
        # try:
        chercheur = C_emploi.objects.get(user=u)
        serializer = C_emploiSerializer(chercheur, many=False)
        Langues = LangueMaitrise.objects.filter(c_emploi=chercheur)
        lang = ''
        for i in Langues:
            lang = lang +" "+ i.langue.nom
        
        lm = []
        for i in Langues:
            lm.append(i.langue.nom)
        q_objects = Q()
        for substring in lm:
            q_objects |= Q(titre__icontains=substring)
        recommended = Travail.objects.filter(q_objects)
        try:
            random_order = recommended.order_by(Random())[0:7]
        except:
            random_order = recommended.order_by(Random())
        seri = TravailSerializer(random_order, many=True)

        data = {
                "token":str(refresh.access_token),
                "refresh_token": str(refresh),
                "user":serializer.data,
                "lang":lang,
                "recomended":seri.data
            }


        encrypted_data_usingAes=encryptAES(json.dumps(data),PublicKEYAES) 

        return Response(
            {
                "token":str(refresh.access_token),
                'fsf':data,
                'data': encrypted_data_usingAes,
                'key': PublicKEYAES
            },
            status.HTTP_200_OK
        )   
        
        # except:
        #         return Response(
        #         {
        #             'status': False,
        #             'message': 'no human as aa develloper for this information',
        #             'data': null
        #         },
        #         status.HTTP_401_UNAUTHORIZED
        #     )
        #     try:
        #         entreprise = Entreprise.objects.get(user=u)
        #         if entreprise.type == "entreprise" and entreprise.status == "Accepted":
        #             serializer = EntrepriseSerializer(entreprise, many=False)
        #             return Response(
        #                 {
        #                     'token': str(refresh.access_token),
        #                     'refresh_token': str(refresh),
        #                     'type':'epe',
        #                     'id':u.id,
        #                     'status': True,
        #                     'message':'login success',
        #                     'data':serializer.data
        #                 },
        #                 status.HTTP_200_OK
        #             )
                    
        #         elif entreprise.type == "entreprise" and entreprise.status == "non_confirmer":
        #             msg = "Votre entreprise a besoin de confirmation, veuillez patientez"
        #             return Response(
        #                 {
        #                     'status': False,
        #                     'message': msg,
        #                     'data': null
        #                 },
        #                 status.HTTP_401_UNAUTHORIZED
        #                 )
        #         elif entreprise.type == "entreprise" and entreprise.status == "Rejected":
        #             msg = "Votre entreprise a été rejeté."
        #             return Response(
        #                 {
        #                     'status': False,
        #                     'message': msg,
        #                     'data': null
        #                 },
        #                 status.HTTP_401_UNAUTHORIZED
        #                 )
        #     except:

                # return Response(
                #     {
                #         'status': False,
                #         'message': 'no human as a develloper for this information',
                #         'data': null
                #     },
                #     status.HTTP_401_UNAUTHORIZED
                # )

@api_view(['POST'])
def updateProfile(request):
    data= request.headers['Authorization']
    token=str.replace(str(data),'JWT ', '')
    if not token:
        return Response(
            {
                'message':'Connexion majatni jaye',
            },
            status=status.HTTP_200_OK
        )
    try:
        payload=jwt.decode(token, 'L4l_o-zEhDwXy0DVf-tcFx2LoQTIxMUfib-z_71uhMg',algorithms=["HS256"])
        print(payload)
    except jwt.ExpiredSignatureError:
        return Response(
            {
                'message':'ExpiredSignatureError',
            },
            status=status.HTTP_200_OK
        )
    user=User.objects.filter(id=payload['user_id']).first()
    chercheur= C_emploi.objects.filter(user=user).first()
    # c_emploi = C_emploi.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        telephone = request.POST['telephone']
        sexe = request.POST['sexe']
        description = request.POST['description']

        chercheur.user.email = email
        chercheur.user.first_name = first_name
        chercheur.user.last_name = last_name
        chercheur.phone = telephone
        chercheur.sexe = sexe
        chercheur.description = description
        
        chercheur.save()
        chercheur.user.save()
        try:
            image = request.FILES['image']
            chercheur.image = image
            chercheur.save()
        except:
            pass
        
        return Response(
            {
                'message':'Votre profile a été modifié avec succées',
            },
            status=status.HTTP_200_OK
        )
    return Response(
            {
                'message':'Get request hun bla vayde',
            },
            status=status.HTTP_200_OK
        )
 

class Les_annonces_emploi(APIView):

    def post(self, request):
        key = request.data['motcle']
        localite = request.data['pays']
        print(key+" :: "+localite)
        browser=webdriver.Chrome("chromedriver.exe")

        browser.get("https://www.linkedin.com/jobs/search?keywords="+key+"&location="+localite+"&position=1&pageNum=0")
        print(browser.current_url)
        jobs_titres=browser.find_elements_by_class_name("base-search-card__title")

        tt=[] 
        iterator = islice(jobs_titres, 30)
        for i in iterator:
            tt.append(i.text)
        
        jobs_entreprises=browser.find_elements_by_class_name("base-search-card__subtitle")
        ne=[] 
        iterator = islice(jobs_entreprises, 30)
        for i in iterator:
            ne.append(i.text)
        jobs_adresses=browser.find_elements_by_class_name("job-search-card__location")
        ja=[]
        iterator = islice(jobs_adresses, 30)
        for i in iterator:
            ja.append(i.text)
        jobs_date=browser.find_elements_by_tag_name("time")
        jd=[]  
        iterator = islice(jobs_date, 30)
        for i in iterator:
            jd.append(i.text)
            
        jobs_links = browser.find_elements_by_tag_name('a')
        jl= [elem.get_attribute('href') for elem in jobs_links]
        iterator = islice(jl, 30)
        for elem in iterator:
            jl.append(elem)


        images = browser.find_elements_by_tag_name('img')
        ji=[]
        iterator = islice(images, 30)
        for elem in iterator:
            ji.append(elem.get_attribute('src'))

        jobss=[ne,tt,ja,jd,jl,ji]
        listjobs=[]
        for item in range(0,len(jobss[3])):
            singlejob={
                "entreprise":jobss[0][item],
                "titre":jobss[1][item],
                "adresse":jobss[2][item],
                "date":jobss[3][item],
                "link":jobss[4][item],
                "image":jobss[5][item]
            }
            listjobs.append(singlejob)
        for item in listjobs:
            epe = item['entreprise']
            titre = item['titre']
            adr= item['adresse']
            dt = item['date']
            img = item['image'] if len(str(item['image'])) > 1 else "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAllBMVEUMZMX///8AYcQAWcFDf8nL3PIAWrzQ3vMAYcI0eclZjtAucslAgsz6/v3x9/sgbclOhM8AX8QAYsAAX70AV70AWMLm7vgAXb4sdsw5fsoRbsVmltK6z+iUt+AMZcGDrN3c6fNvnddiltWqwuPA0+r0+vyOrt+lweR9pduuyueUst9Lh81pldd1mtYdbcunxOXO4u7Z4fGRyVlRAAAEKUlEQVR4nO3ce1faMBzG8SblEpSCiUUuQrkMhsCc+v7f3Ko4KjW/yLY0WXOez9mf4Ml3vSW1NYoAAAAAAAAAAAAAAAAAAAAAAAAAAADgYiriIsqU72FURcapGnXHk5aMue+xVCCT6n56x960Z2OpMt8jsozz+Xve0Xqc+h6SXbKzYOeSfex7UBap+J591lThHI3awPxw5KGcVFUj0RayaRrI6UaUj8GTpfA9NivknApkvTC2YdwjC9lc+h6dBWpFB7JFCIXx1FDIRr6HZ0Fq2EkZewjgXNMnLhVH34a+x/fPeMdYOK3/gchvTIFsXf/ZKR+bC+u/DcW1cS/d1f84jFobU+H3ANYXadNU2PU9PAvkd0Ngz/forMgMhU/1P5Xm4h0ZmHQCOAzz68WEPNdsg9iE+ZH4QATeBTApPYqf9PvoKIh99E2qOxQ3jVvf47JHDT5fMl5GAQW+3tNvnF/4N3shwrhJc8Ljw/Q0Q13MJ4GcRc8IORjP99vZfpWlQe2gH3EZx7Gs/4IJAADqQ3DJX/+FM38vqHyKlA5Hhx+Pj49X43468P34CheEiz9Z+pTMlrvFaQ6YbNrblRpKf6vNbHRNKX2yT/kwSVd5XluzGGs//Ew9NfIGS/RYs3X2yUGzp7dpnMYu+zPql1mbp46f+XxeSCkVxrpt8+bmWJgJOTPeYP7m5QkWi4Wye0d94t3m3sNmtFao5OyLvle7zPnRaKlQCb6+IDBfXvddJ1oq5BH5WE7JXd/xwWilUKnJpYGM9a7dPk5mpfCWP18cmO+okdOtaKVwYHxm5ZP1wOWNPBuFneUfBTK2dHkzyEbhwfirco3NxOF+aqPw8rPMbzuHV34bhX+h4e6q6KnQ4ZM6ngrZyNlG9FXo7hfMvgp7zt7o8FXIDq52U2+FznbTKgovmgAsalq4mB0mQqjJYfvler98o6sWhevuYPh2C5jz4WD1ReMPR4soi4W91dmtXy7MK469o7mpvcLn8nRaSWPi9PzH/++FCXvW3LuXpoXxi6MllK1tqHtGLBMd0zccLYNtFR60W8T0wkqv7yTQVuGTfpfLuvRXkms3sxo7hQlx/yy7NayOO3Uq3MXExY148PFY6OZyYafwihqsXNJfGteoMCGXQoYfzxo1KmxSO2kkJvTLcXUq3BreraFnp3UqNLwT3aJPpnUqPNBjTV+CKDScFVv0t+pUaLiytegXq1BoCQoLKNRDYfVQWEChHgqrh8ICCvVQWD0UFlCoh8LqobCAQj0UVg+FBRTqobB6KCygUA+F1UNhAYV6KKweCgso1ENh9VBYQKEeCquHwkKAhe1SIf2UoaFwSP+/dB29FtTvUsbnH+Q3VxTDmxOq+zffskqJiOtFpZda+OV/M6uQKepLof0NWAAAAAAAAAAAAAAAAAAAAAAAAAAAgAr8Aj5RWY0PDbn2AAAAAElFTkSuQmCC"
            lnk = item['link']
            Travail.objects.create(entreprise=epe, titre=titre, adresse=adr, date=dt, image=img, link=lnk)
        
        time.sleep(5)
        browser.close() 
        x=0
        y=1
        return Response(
            listjobs,
            status=status.HTTP_200_OK
        )
    
    def get(self, request): 
        data= request.headers['Authorization']
        token=str.replace(str(data),'JWT ', '')
        if not token:
            return Response(
                {
                    'message':'Connexion majatni jaye',
                },
                status=status.HTTP_200_OK
            )
        try:
            payload=jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
            print(payload)
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    'message':'ExpiredSignatureError',
                },
                status=status.HTTP_200_OK
            )
        user=User.objects.filter(id=payload['user_id']).first()
        c= C_emploi.objects.filter(user=user).first()
        id = c.user_id
        languesm = LangueMaitrise.objects.filter(c_emploi_id=id)
        lm = []
        for i in languesm:
            lm.append(i.langue.nom)
        travail = Travail.objects.all()
        random_order = travail.order_by(Random())
        seri = TravailSerializer(random_order, many=True)
        return Response(
                seri.data,
            status=status.HTTP_200_OK
        )



class recommended(APIView):
    def get(self, request): 
        data= request.headers['Authorization']
        token=str.replace(str(data),'JWT ', '')
        if not token:
            return Response(
                {
                    'message':'Connexion majatni jaye',
                },
                status=status.HTTP_200_OK
            )
        try:
            payload=jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
            print(payload)
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    'message':'ExpiredSignatureError',
                },
                status=status.HTTP_200_OK
            )

        user=User.objects.filter(id=payload['user_id']).first()
        c= C_emploi.objects.filter(user=user).first()
        languesm = LangueMaitrise.objects.filter(c_emploi=c)
        print(languesm)
        lm = []
        for i in languesm:
            lm.append(i.langue.nom)
            print(i.langue.nom)
        try:
            q_list = [Q(titre__icontains=string) for string in lm]
            query = q_list.pop()
            for q in q_list:
                query |= q
            travails = Travail.objects.filter(query)

            random_order = travails.order_by(Random())[:7]
        except:
            travail = Travail.objects.all()[:7]
            random_order = travail.order_by(Random())
            seri = TravailSerializer(random_order, many=True)
            return Response(
                    seri.data,
                status=status.HTTP_200_OK
            )
        
        seri = TravailSerializer(random_order, many=True)
        return Response(
                seri.data,
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def inscription_chercheur_emploi(request):
    try:
        email = request.POST['email']
        username = request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        telephon = request.POST['telephone']
        sexe = request.POST['sexe']
        image = request.FILES['image']
        experience = request.POST['experience']
        adresse = request.POST['adresse']
        skills = request.POST['skills']
        description = request.POST['description']
    except:
          return Response(
                {
                    'message':'veuillez fournir tous les données',
                },
                status=status.HTTP_400_BAD_REQUEST
            )  

    if password1 != password2:
        return Response(
                {
                    'message':'les mots de passes ne sont pas conformes',
                },
                status=status.HTTP_400_BAD_REQUEST
            )  
    
    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
    c = C_emploi.objects.create(user=user, telephone=telephon, sexe=sexe, image=image, type="c_emploi",experience=experience, adresse=adresse, skills=skills, description=description)
    user.save()
    c.save()
    
    return Response(
                {
                    'message':'inscription faite avec succées, vous pouvez se connecter maintenant',
                },
                status=status.HTTP_201_CREATED
            )
    
@api_view(['POST'])
def inscription_entreprise(request):
    try:
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        telephon = request.POST['telephone']
        sexe = request.POST['sexe']
        image = request.FILES['image']
        nom_entreprise = request.POST['nom_entreprise']
    except:
          return Response(
                {
                    'message':'veuillez fournir tous les données',
                },
                status=status.HTTP_400_BAD_REQUEST
            )  

    if password1 != password2:
        return Response(
                {
                    'message':'les mots de passes ne sont pas conformes',
                },
                status=status.HTTP_400_BAD_REQUEST
            )  
    
    user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
    entreprise = Entreprise.objects.create(user=user, telephone=telephon, sexe=sexe, image=image, nom_entreprise=nom_entreprise, type="entreprise", status="non_confirmer")
    user.save()
    entreprise.save()
    
    return Response(
                {
                    'message':'inscription faite avec succées, vous pouvez se connecter maintenant',
                },
                status=status.HTTP_201_CREATED
            )
    
@permission_classes([IsAuthenticated])
class Listlangue(generics.ListCreateAPIView):    
    queryset=Langue.objects.all()
    serializer_class = LangueSerializer

@permission_classes([IsAuthenticated])
class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset=Langue.objects.all()
    serializer_class = LangueSerializer

@permission_classes([IsAuthenticated])
class ListLangueMaitrise(generics.ListCreateAPIView):    
    queryset=LangueMaitrise.objects.all()
    serializer_class = LangueMaitriseSerializer

@permission_classes([IsAuthenticated])
class DetailLangueMaitrise(generics.RetrieveUpdateDestroyAPIView):
    queryset=LangueMaitrise.objects.all()
    serializer_class = LangueMaitriseSerializer

@permission_classes([AllowAny])
class ListDocument(generics.ListCreateAPIView):    

    queryset=Document.objects.all()
    serializer_class = DocumentSerializer

@permission_classes([AllowAny])
class DetailDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset=Document.objects.all()
    serializer_class = DocumentSerializer





