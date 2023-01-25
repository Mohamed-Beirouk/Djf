from myappdjf.cryptoFunctions import  decrypt_message, encrypt_message
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


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
        langS = LangueMaitriseSerializer(Langues, many=True)


        # with open('myappdjf'+serializer.data['image'], "rb") as image_file:
        #     image_string =base64.b64encode(image_file.read()).decode() 

       

        # return Response(
        #     {
        #         "public":key.publickey().exportKey(),
        #     },
        #     status.HTTP_200_OK
        # )

        # message = """G\\x97\\xf7xcEyO\\xa1\\x13\\xcb\\xb5\\xa3%\\xd4c \\xc4\\xe4\\xe4\\x02i\\xfa\\xec\\\\\\xdaQ(\\x1aI\\xcf\\xae^\\x18\\x8c2\\xc5\\x84S#*\\xf1k\\xfd\\xe2X\\x89\\x06\\x93R\\x86^\\xaf{\\x90=\\x90\\xc9\\xdb\\xdf\"7pb"""
        # arr = bytes(message, 'utf-8')
        # enc = decrypt_message(arr)
        

        message = "Mohamed Beirouk"
        enc = encrypt_message(message)
        
        return Response(
            {
                'token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'id':u.id,
                'status': str(enc),
                'message':'login success',
                'informations':serializer.data,
                'langues':langS.data
            },
            status.HTTP_200_OK
        )
        # except:
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

        #         return Response(
        #             {
        #                 'status': False,
        #                 'message': 'no human as a develloper for this information',
        #                 'data': null
        #             },
        #             status.HTTP_401_UNAUTHORIZED
        #         )

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
        key = request.POST['motcle']
        localite = request.POST['pays']
        browser=webdriver.Chrome("chromedriver.exe")
        browser.get("https://www.linkedin.com/jobs/search?keywords="+key+"&location="+localite+"&position=1&pageNum=0")
        jobs_titres=browser.find_elements_by_class_name("base-search-card__title")
        tt=[] 
        iterator = islice(jobs_titres, 25)
        for i in iterator:
            tt.append(i.text)
        
        jobs_entreprises=browser.find_elements_by_class_name("base-search-card__subtitle")
        ne=[] 
        iterator = islice(jobs_entreprises, 25)
        for i in iterator:
            ne.append(i.text)
        jobs_adresses=browser.find_elements_by_class_name("job-search-card__location")
        ja=[]
        iterator = islice(jobs_adresses, 25)
        for i in iterator:
            ja.append(i.text)
        jobs_date=browser.find_elements_by_tag_name("time")
        jd=[]  
        iterator = islice(jobs_date, 25)
        for i in iterator:
            jd.append(i.text)
            
        jobs_links = browser.find_elements_by_tag_name('a')
        jl= [elem.get_attribute('href') for elem in jobs_links]
        iterator = islice(jl, 25)
        for elem in iterator:
            jl.append(elem)
        jobss=[ne,tt,ja,jd,jl]
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
        time.sleep(5)
        browser.close() 
        x=0
        y=1
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
        c= C_emploi.objects.filter(user=user).first()
        id = c.user_id
        languesm = LangueMaitrise.objects.filter(c_emploi_id=id)
        lm = []
        for i in languesm:
            lm.append(i.langue.nom)
        key=""
        for i in lm:
            key=key+" "+i
        
        browser=webdriver.Chrome("chromedriver.exe")    
        browser.get("https://www.linkedin.com/jobs/search?keywords="+key+"&position=1&pageNum=0")
        # browser.get("https://www.linkedin.com/jobs/search?keywords=springboot&location=usa&position=1&pageNum=0")
        jobs_titres=browser.find_elements_by_class_name("base-search-card__title")
        tt=[] 
        iterator = islice(jobs_titres, 25)
        for i in iterator:
            tt.append(i.text)
        
        jobs_entreprises=browser.find_elements_by_class_name("base-search-card__subtitle")
        ne=[] 
        iterator = islice(jobs_entreprises, 25)
        for i in iterator:
            ne.append(i.text)
        jobs_adresses=browser.find_elements_by_class_name("job-search-card__location")
        ja=[]
        iterator = islice(jobs_adresses, 25)
        for i in iterator:
            ja.append(i.text)
        jobs_date=browser.find_elements_by_tag_name("time")
        # jobs_date=browser.find_elements_by_class_name("job-search-card__listdate--new job-search-card__listdate")
        jd=[]  
        iterator = islice(jobs_date, 25)
        for i in iterator:
            jd.append(i.text)
            
        jobs_links = browser.find_elements_by_tag_name('a')
        jl= [elem.get_attribute('href') for elem in jobs_links]
        iterator = islice(jl, 25)
        for elem in iterator:
            jl.append(elem)
        
        images = browser.find_elements_by_tag_name('img')
        ji=[]
        iterator = islice(images, 25)
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
        time.sleep(5)
        browser.close() 
        return Response(
            listjobs,
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





















# def page_home_entreprise(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_entreprise")
#     entreprise = Entreprise.objects.get(user=request.user)
#     if request.method=="POST":   
#         email = request.POST['email']
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         telephone = request.POST['telephone']
#         sexe = request.POST['sexe']

#         entreprise.user.email = email
#         entreprise.user.first_name = first_name
#         entreprise.user.last_name = last_name
#         entreprise.phone = telephone
#         entreprise.gender = sexe
#         entreprise.save()
#         entreprise.user.save()

#         try:
#             image = request.FILES['image']
#             entreprise.image = image
#             entreprise.save()
#         except:
#             pass
#         alert = True
#         return render(request, "page_home_entreprise.html", {'alert':alert})
#     return render(request, "page_home_entreprise.html", {'entreprise':entreprise})

# def publier_annonce(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_entreprise")
#     if request.method == "POST":
#         titre = request.POST['titre']
#         date_debut = request.POST['date_debut']
#         date_fin = request.POST['date_fin']
#         salaire = request.POST['salaire']
#         experience = request.POST['experience']
#         adresse = request.POST['adresse']
#         skills = request.POST['skills']
#         description = request.POST['description']
#         user = request.user
#         entreprise = Entreprise.objects.get(user=user)
#         travail = Travail.objects.create(entreprise=entreprise, titre=titre,date_debut=date_debut, date_fin=date_fin, salaire=salaire, image=entreprise.image, experience=experience, adresse=adresse, skills=skills, description=description, date_creation=date.today())
#         travail.save()
#         alert = True
#         return render(request, "publier_annonce.html", {'alert':alert})
#     return render(request, "publier_annonce.html")

# def liste_des_annonces(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_entreprise")
#     entreprises = Entreprise.objects.get(user=request.user)
#     travails = Travail.objects.filter(entreprise=entreprises)
#     return render(request, "liste_des_annonces.html", {'travails':travails})

# def modifier_annonce(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_entreprise")
#     travail = Travail.objects.get(id=myid)
#     if request.method == "POST":
#         title = request.POST['titre']
#         start_date = request.POST['date_debut']
#         end_date = request.POST['date_fin']
#         salary = request.POST['salaire']
#         experience = request.POST['experience']
#         location = request.POST['adresse']
#         skills = request.POST['skills']
#         description = request.POST['description']

#         travail.titre = title
#         travail.salaire = salary
#         travail.experience = experience
#         travail.adresse = location
#         travail.skills = skills
#         travail.description = description

#         travail.save()
#         if start_date:
#             travail.date_debut = start_date
#             travail.save()
#         if end_date:
#             travail.date_fin = end_date
#             travail.save()
#         alert = True
#         return render(request, "modifier_annonce.html", {'alert':alert})
#     return render(request, "modifier_annonce.html", {'travail':travail})

# def logo_entreprise(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_entreprise")
#     travail = Travail.objects.get(id=myid)
#     if request.method == "POST":
#         image = request.FILES['logo']
#         travail.image = image 
#         travail.save()
#         alert = True
#         return render(request, "logo_entreprise.html", {'alert':alert})
#     return render(request, "logo_entreprise.html", {'travail':travail})

# def deconnecter(request):
#     logout(request)
#     return redirect('/')

# def connexion_administrateur(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_superuser:
#                 login(request, user)
#                 return redirect("/stat")
#         else:   
#             msg = "Les données sont  erronés,ressayer"
#             return render(request, "connexion_administrateur.html", {"msg":msg})
#     return render(request, "connexion_administrateur.html")


# def rien(request):
    
#     return render(request, "cnx_admin.html")
# def liste_chercheurs_emploi(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     c_emploi = C_emploi.objects.all()
#     return render(request, "liste_chercheurs_emploi.html", {'c_emploi':c_emploi})

# def supprimer_un_chercheur_emploi(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     c_emploi = User.objects.filter(id=myid)
#     c_emploi.delete()
#     return redirect("/liste_chercheurs_emploi")

# def entreprises_non_confirmer(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprises = Entreprise.objects.filter(status="non_confirmer")
#     return render(request, "entreprises_non_confirmer.html", {'entreprises':entreprises})

# def change_status(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprise = Entreprise.objects.get(id=myid)
#     if request.method == "POST":
#         status = request.POST['status']
#         entreprise.status=status
#         entreprise.save()
#         alert = True
#         return render(request, "change_status.html", {'alert':alert})
#     return render(request, "change_status.html", {'entreprise':entreprise})

# def entreprises_confirmer(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprises = Entreprise.objects.filter(status="Accepted")
#     return render(request, "entreprises_confirmer.html", {'entreprises':entreprises})

# def entreprises_rejeter(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprises = Entreprise.objects.filter(status="Rejected")
#     return render(request, "entreprises_rejeter.html", {'entreprises':entreprises})

# def tous_les_entreprises(request):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprises = Entreprise.objects.all()
#     return render(request, "tous_les_entreprises.html", {'entreprises':entreprises})

# def supprimer_entreprise(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_administrateur")
#     entreprise = User.objects.filter(id=myid)
#     entreprise.delete()
#     return redirect("/tous_les_entreprises")


# def freelancerHomePage(request):
#     if request.method == "POST":
#         mot = request.POST['motcle']
#         c_emplois = C_emploi.objects.filter(description__contains=mot)
#         return render(request, "freelancer/freelancer.html", {'c_emplois':c_emplois})
    
#     c_emplois = C_emploi.objects.all()
#     #     serializer = C_emploiSerializer(c_emplois, many=True), 
#     #     return Response(serializer.data)
    
#     return render(request, "freelancer/freelancer.html", {'c_emplois':c_emplois})


# def languesmaitrise(request):
#     if request.method == "POST":
#         langueid = request.POST['idid']
#         c_emploi = C_emploi.objects.get(user=request.user)
#         langue = Langue.objects.get(id=langueid)
#         id = c_emploi.user_id
        
#         lm = LangueMaitrise.objects.create(c_emploi=c_emploi, langue=langue)
#         lm.save()
        
#     c_emploi = C_emploi.objects.get(user=request.user)
#     # id = c_emploi.user_id
#     langues = LangueMaitrise.objects.filter(c_emploi=c_emploi)
#     lang = Langue.objects.all()
#     return render(request, "languesmaitrise.html", {'langues':langues, 'lang':lang})

# def detailfreelancer(request, id):
#     c_emploi = C_emploi.objects.get(id=id)
#     iddd = c_emploi.user_id
#     lm = LangueMaitrise.objects.filter(c_emploi_id=iddd)
#     k = C_emploi.objects.get(id=id)
#     return render(request, "freelancer/detailfreelancer.html", {'k':k, 'lm':lm})


# @api_view(['GET','POST'])
# def rest(request):
#     if request.method == 'GET':
#         c = Langue.objects.all()
#         serializer = LangueSerializer(c, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         try:
#             n = request.data["nom"]
#             d = request.data["description"]
#             lang = Langue.objects.create(nom=n, description=d)
#             return Response(
#             "success",
#             status=status.HTTP_201_CREATED
#         )
#         except:
#             return Response(
#                 "error, invalid data",
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
# def scrapp(request):
    
#     list=[[1,2,3],["med","sidi","ali"],["brk","psidi","pali"]]
#     listjobs=[]
#     for item in range(0,len(list[0])):
#         singlejob=[]
#         singlejob.append(list[0][item])
#         singlejob.append(list[1][item])
#         singlejob.append(list[2][item])
#         listjobs.append(singlejob)
        
#     return render(request, "jobscrapped.html",{'listjobs':listjobs})

# def index(request):
#     return render(request, "index.html")

# def stat(request):
#     t = Travail.objects.count()
#     e = Entreprise.objects.count()
#     c = C_emploi.objects.count()
#     return render(request, "statistiques.html", {'t':t, 'e':e, 'c':c})

# def connexion_chercheur_emploi(request): 
#     if request.user.is_authenticated:
#         return redirect("/page_home_chercheur_emploi")
#     else:
#         if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 user1 = C_emploi.objects.get(user=user)
#                 if user1.type == "c_emploi":
#                     login(request, user)
#                     return redirect("/page_home_chercheur_emploi")
#             else:   
#                 msg = "Les données sont  erronés, ressayer"
#                 return render(request, "connexion_chercheur_emploi.html", {"msg":msg})
#     return render(request, "connexion_chercheur_emploi.html")

# def page_home_chercheur_emploi(request):
#     if not request.user.is_authenticated:
#         return redirect('/connexion_chercheur_emploi/')
#     c_emploi = C_emploi.objects.get(user=request.user)
#     if request.method=="POST":   
#         email = request.POST['email']
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         telephone = request.POST['telephone']
#         sexe = request.POST['sexe']
#         description = request.POST['description']

#         c_emploi.user.email = email
#         c_emploi.user.first_name = first_name
#         c_emploi.user.last_name = last_name
#         c_emploi.phone = telephone
#         c_emploi.sexe = sexe
#         c_emploi.description = description
        
#         c_emploi.save()
#         c_emploi.user.save()
#         try:
#             image = request.FILES['image']
#             c_emploi.image = image
#             c_emploi.save()
#         except:
#             pass
#         alert = True
#         return render(request, "page_home_chercheur_emploi.html", {'alert':alert})
#     return render(request, "page_home_chercheur_emploi.html", {'c_emploi':c_emploi})


# def detail_annonce(request, myid):
#     travail = Travail.objects.get(id=myid)
#     return render(request, "detail_annonce.html", {'travail':travail})

# def deposer_pour_emploi(request, myid):
#     if not request.user.is_authenticated:
#         return redirect("/connexion_chercheur_emploi")
#     c_emploi = C_emploi.objects.get(user=request.user)
#     travail = Travail.objects.get(id=myid)
#     date1 = date.today()
#     if travail.date_fin < date1:
#         closed=True
#         return render(request, "deposer_pour_emploi.html", {'closed':closed})
#     elif travail.date_debut > date1:
#         notopen=True
#         return render(request, "deposer_pour_emploi.html", {'notopen':notopen})
#     else:
#         if request.method == "POST":
#             cv = request.FILES['cv']
#             Deposer.objects.create(travail=travail, entreprise=travail.entreprise, c_emploi=c_emploi, cv=cv, date_depot=date.today())
#             alert=True
#             return render(request, "deposer_pour_emploi.html", {'alert':alert})
#     return render(request, "deposer_pour_emploi.html", {'travail':travail})


# def les_interesses(request):
#     entreprise = Entreprise.objects.get(user=request.user)
#     deposer = Deposer.objects.filter(entreprise=entreprise)
#     return render(request, "les_interesses.html", {'deposer':deposer})
