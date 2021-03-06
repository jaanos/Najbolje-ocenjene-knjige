#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# odkomentiraj, če želiš sporočila o napakah
# debug(True)
static_dir = "./static"

# Skrivnost za kodiranje cookijev
secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

@route('/assets/<filename:path>')
def static(filename):
    """Splošna funkcija, ki servira vse statične datoteke iz naslova
       /static/..."""
    return static_file(filename, root=static_dir)

@route("/")
def main():
    redirect("/books")
@route("/index.html")
def main():
    redirect("/books")  
@get('/books')
def index():
##    """Vrni dano število knjig (privzeto 9). Rezultat je seznam, katerega
##       elementi so oblike [knjiga_id, avtor,naslov,slika]    """
##    cur.execute("""SELECT (book_id, authors, title, original_publication_year, average_rating,image_url) FROM books ORDER BY average_rating DESC LIMIT %s""", [9])
    seznam=top_9()
    return template('index.html', najboljsi=seznam)
    ##return template('index.html', najboljsi=cur)

@route("/four-col.html")
def main():
    redirect("/all")
@get('/all')
def products():
    cur.execute ("""SELECT authors, title, average_rating, image_url FROM books ORDER BY title ASC""")
    vse = cur.fetchall()
##    query = dict(request.query)
##    try:
##        del query['page']
##    except:
##        pass
##
##    #V html ne gre (brez js) zamenjati samo dela query stringa brez da bi izgubil ostale, zato:
##    qstring = str(request.query_string)
##    qstring = re.sub('&?page=\d','', qstring, flags=re.IGNORECASE)    
##    pagenr = request.query.page or 1 #stran
    return template('four-col.html', vse=vse,#pagenr=int(pagenr),
                           #qstring=qstring,query=query
                    )

@route("/products.html")
def main():
    redirect("/zanri")
@get('/zanri')
def zanri():
    return template('products.html')

@route("/products_drama.html")
def main():
    redirect("/drama")
@get('/drama')
def zanri():
    return template('products_drama.html')

@route("/products_biography.html")
def main():
    redirect("/biography")
@get('/biography')
def zanri():
    return template('products_biography.html')

@route("/products_children.html")
def main():
    redirect("/children")
@get('/children')
def zanri():
    return template('products_children.html')

@route("/products_classics.html")
def main():
    redirect("/classics")
@get('/classics')
def zanri():
    return template('products_classics.html')

@route("/products_comics.html")
def main():
    redirect("/comics")
@get('/comics')
def zanri():
    return template('products_comics.html')

@route("/products_fiction.html")
def main():
    redirect("/fiction")
@get('/fiction')
def zanri():
    return template('products_fiction.html')

@route("/products_history.html")
def main():
    redirect("/history")
@get('/history')
def zanri():
    return template('products_history.html')

@route("/products_romance.html")
def main():
    redirect("romance/")
@get('/romance')
def zanri():
    return template('products_romance.html')

@route("/products_science.html")
def main():
    redirect("science/")
@get('/science')
def zanri():
    return template('products_science.html')

@route("/products_thriller.html")
def main():
    redirect("thriller/")
@get('/thriller')
def zanri():
    return template('products_thriller.html')

@route("/login.html")
def main():
    redirect("/login")
@get('/login')
def login():
    return template('login.html')

@route("/account.html")
def main():
    redirect("/account")
@get('/account')
def profil():
    return template('account.html')

@route("/contact.html")
def main():
    redirect("/contact")
@get('/contact')
def kontakt():
    return template('contact.html')

@route("/forget_password.html")
def main():
    redirect("/forget_password")
@get('/forget_password')
def geslo():
    return template('forget_password.html')

@route("/register.html")
def main():
    redirect("/register")
@get('/register')
def register():
    return template('register.html')

@route("/product_details.html")
def main():
    redirect("/product_details")
    
@get('/product_details')
def podrobnosti():
    cur.execute ("""SELECT authors, title, average_rating, image_url FROM books ORDER BY title ASC""")
    podatki = cur.fetchall()
    #slika
##    cur.execute(''' SELECT image_url FROM books        
##        where book_id= %s''',[bookid]) # das se v podrobnosti(bookid)
##    slike = cur.fetchall()
    return template('product_details.html', podatki=podatki, #slike=slike
                    )

def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

# Funkcija, ki v cookie spravi sporocilo
def set_sporocilo(tip, vsebina):
    response.set_cookie('message', (tip, vsebina), path='/', secret=secret)

# Funkcija, ki iz cookija dobi sporočilo, če je
def get_sporocilo():
    sporocilo = request.get_cookie('message', default=None, secret=secret)
    response.delete_cookie('message')
    return sporocilo

def get_user(auto_login = True):
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Če ni prijavljen, presumeri
       na stran za prijavo ali vrni None (odvisno od auto_login).
    """
    # Dobimo username iz piškotka
    username = request.get_cookie('username', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if username is not None:
        cur.execute("SELECT username, ime FROM uporabnik WHERE username=%s",
                  [username])
        r = cur.fetchone()
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return r
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    if auto_login:
        redirect('/login/')
    else:
        return [None,None]

def main():
        """Glavna stran."""
    # Iz cookieja dobimo uporabnika (ali ga preusmerimo na login, če
    # nima cookija)
        curuser = get_user()
    # Morebitno sporočilo za uporabnika
        sporocilo = get_sporocilo()
    # Vrnemo predlogo za glavno stran
        return template("index.html",
                        ime=ime,
                        username=username,
                        sporocilo=sporocilo
                        )
##
##@get('/transakcije/:x/')
##def transakcije(x):
##    cur.execute("SELECT * FROM transakcija WHERE znesek > %s ORDER BY znesek, id", [int(x)])
##    return template('transakcije.html', x=x, transakcije=cur)
##
##@get('/dodaj_transakcijo')
##def dodaj_transakcijo():
##    return template('dodaj_transakcijo.html', znesek='', racun='', opis='', napaka=None)
##
##@post('/dodaj_transakcijo')
##def dodaj_transakcijo_post():
##    znesek = request.forms.znesek
##    racun = request.forms.racun
##    opis = request.forms.opis
##    try:
##        cur.execute("INSERT INTO transakcija (znesek, racun, opis) VALUES (%s, %s, %s)",
##                    (znesek, racun, opis))
##    except Exception as ex:
##        return template('dodaj_transakcijo.html', znesek=znesek, racun=racun, opis=opis,
##                        napaka = 'Zgodila se je napaka: %s' % ex)
##    redirect("/")
@get("/login/")
def login_get():
    """Serviraj formo za login."""
    #curuser = get_user(auto_redir = True)
    return template("login.html", 
                           napaka=None,
                           username=None)

def logout():
    """Pobriši cookie in preusmeri na login."""
    bottle.response.delete_cookie('username')
    bottle.redirect('/login/')

@post("/login/")
def login_post():
    """Obdelaj izpolnjeno formo za prijavo"""
    # Uporabniško ime, ki ga je uporabnik vpisal v formo
    username = request.forms.username
    # Izračunamo MD5 has gesla, ki ga bomo spravili
    password = password_md5(request.forms.password)
    # Preverimo, ali se je uporabnik pravilno prijavil
    #c = baza.cursor()
    cur.execute("SELECT 1 FROM uporabnik WHERE username=%s AND password=%s",
              [username, password])
    if cur.fetchone() is None:
        # Username in geslo se ne ujemata
        return template("login.html", #template za login
                               napaka="Nepravilna prijava",
                               username=username)
    else:
        # Vse je v redu, nastavimo cookie in preusmerimo na glavno stran
        response.set_cookie('username', username, path='/', secret=secret)
        redirect("/")

@get("/register/")
def login_get():
    """Prikaži formo za registracijo."""
    #curuser = get_user(auto_redir = True)
    return template("register.html", 
                           username=None,
                           ime=None,
                           napaka=None)

@post("/register/")
def register_post():
    """Registriraj novega uporabnika."""
    username = request.forms.username
##    ime = request.forms.ime
##    priimek = request.forms.priimek
    password1 = request.forms.password1
    password2 = request.forms.password2
    #curuser = get_user(auto_redir = True)
    # Ali uporabnik že obstaja?
    #c = baza.cursor()
    cur.execute("SELECT 1 FROM uporabnik WHERE username=%s", [username])
    if cur.fetchone():
        # Uporabnik že obstaja
        return template("register.html",
                               username=username,
                               #ime=ime,
                               napaka='To uporabniško ime je že zavzeto.')
    elif not password1 == password2:
        # Gesli se ne ujemata
        return template("register.html",
                               username=username,
                               ime=ime,
                               napaka='Gesli se ne ujemata.')
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        password = password_md5(password1)
        cur.execute("INSERT INTO uporabnik (username,ime, password) VALUES (%s,%s,%s)", 
                  (username,ime, password))
        # Daj uporabniku cookie
        response.set_cookie('username', username, path='/', secret=secret)
        redirect("/")

def user_change(username):
    """Obdelaj formo za spreminjanje podatkov o uporabniku."""
    # Kdo je prijavljen?
    (username, ime) = get_user()
    # Staro geslo (je obvezno)
    password1 = password_md5(request.forms.password1)
    # Preverimo staro geslo
    cur.execute ("SELECT 1 FROM uporabnik WHERE username=%s AND password=%s",
               [username, password1])
    # Pokazali bomo eno ali več sporočil, ki jih naberemo v seznam
    sporocila = []
    if cur.fetchone():
        # Geslo je ok
        # Ali je treba spremeniti geslo?
        password2 =request.forms.password2
        password3 = request.forms.password3
        if password2 or password3:
            # Preverimo, ali se gesli ujemata
            if password2 == password3:
                # Vstavimo v bazo novo geslo
                password2 = password_md5(password2)
                cur.execute ("UPDATE uporabnik SET password=%s WHERE username =%s", [password2, username])
                sporocila.append(("alert-success", "Spremenili ste geslo."))
            else:
                sporocila.append(("alert-danger", "Gesli se ne ujemata."))
    else:
        # Geslo ni ok
        sporocila.append(("alert-danger", "Napačno staro geslo."))
    cur.close ()
    # Prikažemo stran z uporabnikom, z danimi sporočili. Kot vidimo,
    # lahko kar pokličemo funkcijo, ki servira tako stran
    #return user_wall(username, sporocila=sporocila)

def top_9(limit=21):
    """Vrni dano število knjig (privzeto 9). Rezultat je seznam, katerega
       elementi so oblike [knjiga_id, avtor,naslov,slika]    """
    cur.execute(
    """SELECT book_id, authors, title, original_publication_year, average_rating,image_url
       FROM books 
       ORDER BY average_rating DESC
       LIMIT %s
    """, [limit])
    najboljsi = cur.fetchall()
##    # Rezultat predelamo v nabor.
####    top_10 = tuple(cur)
####    # Nabor id-jev knjig, ki jih bomo vrnili
####    tids = (top[0] for top in top_10)
####    # Sedaj prenesemo rezultate poizvedbe v slovar
####    for (tid, username, ime, vsebina) in c:
####        komentar[tid].append((username, ime, vsebina))
####    c.close()
##    # Vrnemo nabor, kot je opisano v dokumentaciji funkcije:
    return(najboljsi)

######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
